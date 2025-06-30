import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../providers/progress_provider.dart';

// Classe auxiliar para definir múltiplas séries de dados em um único gráfico
class ChartSeries<T> {
  final String name;
  final Color color;
  final double Function(T) valueExtractor;

  ChartSeries(
      {required this.name, required this.color, required this.valueExtractor});
}

class ProgressDashboardScreen extends StatelessWidget {
  final String token;
  const ProgressDashboardScreen({super.key, required this.token});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (ctx) => ProgressProvider(token),
      child: DefaultTabController(
        length: 3,
        child: Scaffold(
          appBar: AppBar(
            title: const Text('Painel de Progresso'),
            bottom: const TabBar(
              indicatorColor: Colors.orange,
              labelColor: Colors.orange,
              unselectedLabelColor: Colors.grey,
              tabs: [
                Tab(icon: Icon(Icons.monitor_weight), text: 'Peso'),
                Tab(icon: Icon(Icons.straighten), text: 'Medidas'),
                Tab(icon: Icon(Icons.directions_run), text: 'Cardio'),
              ],
            ),
          ),
          body: Consumer<ProgressProvider>(
            builder: (ctx, progressData, _) {
              if (progressData.isLoading) {
                return const Center(child: CircularProgressIndicator());
              }
              return TabBarView(
                children: [
                  _GroupedChartView<WeightRecord>(
                    groupedRecords: {
                      'Evolução do Peso': progressData.weightRecords
                    },
                    seriesList: [
                      ChartSeries<WeightRecord>(
                          name: 'Peso (kg)',
                          color: Colors.orange,
                          valueExtractor: (r) => r.weight),
                    ],
                    emptyMessage: 'Nenhum dado de peso registado.',
                  ),
                  _GroupedChartView<BodyMeasureRecord>(
                    groupedRecords: progressData.groupedBodyMeasureRecords,
                    seriesList: [
                      ChartSeries<BodyMeasureRecord>(
                          name: 'Valor (cm)',
                          color: Colors.teal,
                          valueExtractor: (r) => r.value),
                    ],
                    emptyMessage: 'Nenhum dado de medida registado.',
                  ),
                  _GroupedChartView<CardioRecord>(
                    groupedRecords: progressData.groupedCardioRecords,
                    seriesList: [
                      ChartSeries<CardioRecord>(
                          name: 'Duração (min)',
                          color: Colors.blue,
                          valueExtractor: (r) => r.duration.toDouble()),
                      ChartSeries<CardioRecord>(
                          name: 'Distância (km)',
                          color: Colors.red,
                          valueExtractor: (r) => r.distance),
                    ],
                    emptyMessage: 'Nenhum dado de cardio registado.',
                  ),
                ],
              );
            },
          ),
          floatingActionButton: Builder(
            builder: (context) => FloatingActionButton(
              onPressed: () => _showAddDialog(context),
              backgroundColor: Colors.orange,
              child: const Icon(Icons.add),
            ),
          ),
        ),
      ),
    );
  }

  // Todos os outros métodos da classe ProgressDashboardScreen permanecem iguais...
  void _showAddDialog(BuildContext context) {
    final tabIndex = DefaultTabController.of(context).index;
    if (tabIndex == 0) _showAddWeightDialog(context);
    if (tabIndex == 1) _showAddMeasureDialog(context);
    if (tabIndex == 2) _showAddCardioDialog(context);
  }

  Future<void> _pickAndExtractImage(
    BuildContext context,
    String dataType, {
    TextEditingController? weightController,
    TextEditingController? measureValueController,
    TextEditingController? durationController,
    TextEditingController? distanceController,
    TextEditingController? caloriesController,
  }) async {
    final picker = ImagePicker();
    final pickedFile =
        await picker.pickImage(source: ImageSource.gallery, imageQuality: 50);

    if (pickedFile != null) {
      final imageFile = File(pickedFile.path);
      try {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
              content:
                  Text('Analisando imagem... Isso pode levar um momento.')),
        );
        final extractedData =
            await Provider.of<ProgressProvider>(context, listen: false)
                .extractDataFromImage(imageFile, dataType);

        if (context.mounted) {
          if (dataType == 'weight') {
            weightController?.text =
                (extractedData['peso_kg'] ?? '').toString();
          } else if (dataType == 'measure') {
            measureValueController?.text =
                (extractedData['valor_cm'] ?? '').toString();
          } else if (dataType == 'cardio') {
            durationController?.text =
                (extractedData['tempo_min'] ?? '').toString();
            distanceController?.text =
                (extractedData['distancia_km'] ?? '').toString();
            caloriesController?.text =
                (extractedData['calorias'] ?? '').toString();
          }
        }
      } catch (e) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Erro ao extrair dados: ${e.toString()}')),
          );
        }
      }
    }
  }

  void _showAddWeightDialog(BuildContext parentContext) {
    final weightController = TextEditingController();
    final formKey = GlobalKey<FormState>();

    showDialog(
      context: parentContext,
      builder: (ctx) => AlertDialog(
        title: const Text('Adicionar Novo Peso'),
        content: Form(
          key: formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: weightController,
                keyboardType:
                    const TextInputType.numberWithOptions(decimal: true),
                decoration: const InputDecoration(labelText: 'Peso em kg'),
                validator: (value) {
                  if (value == null ||
                      double.tryParse(value) == null ||
                      double.parse(value) <= 0) {
                    return 'Por favor, insira um peso válido.';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: () => _pickAndExtractImage(parentContext, 'weight',
                    weightController: weightController),
                icon: const Icon(Icons.camera_alt),
                label: const Text("Extrair da Foto"),
              )
            ],
          ),
        ),
        actions: [
          TextButton(
              onPressed: () => Navigator.of(ctx).pop(),
              child: const Text('Cancelar')),
          ElevatedButton(
            onPressed: () async {
              if (formKey.currentState!.validate()) {
                final weight = double.parse(weightController.text);
                await Provider.of<ProgressProvider>(parentContext,
                        listen: false)
                    .addWeightRecord(weight);
                if (ctx.mounted) Navigator.of(ctx).pop();
              }
            },
            child: const Text('Adicionar'),
          ),
        ],
      ),
    );
  }

  void _showAddMeasureDialog(BuildContext parentContext) {
    final List<String> measureTypes = [
      'Braço',
      'Peito',
      'Cintura',
      'Quadril',
      'Coxa',
      'Panturrilha'
    ];
    String? selectedType = measureTypes.first;
    final valueController = TextEditingController();
    final formKey = GlobalKey<FormState>();

    showDialog(
        context: parentContext,
        builder: (ctx) => AlertDialog(
              title: const Text('Adicionar Nova Medida'),
              content: Form(
                  key: formKey,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      DropdownButtonFormField<String>(
                        value: selectedType,
                        items: measureTypes
                            .map((type) => DropdownMenuItem(
                                value: type, child: Text(type)))
                            .toList(),
                        onChanged: (value) => selectedType = value,
                        decoration:
                            const InputDecoration(labelText: 'Parte do Corpo'),
                      ),
                      const SizedBox(height: 12),
                      TextFormField(
                        controller: valueController,
                        keyboardType: const TextInputType.numberWithOptions(
                            decimal: true),
                        decoration:
                            const InputDecoration(labelText: 'Valor em cm'),
                        validator: (v) => (v == null ||
                                v.trim().isEmpty ||
                                double.tryParse(v) == null)
                            ? 'Valor inválido'
                            : null,
                      ),
                      const SizedBox(height: 20),
                      ElevatedButton.icon(
                        onPressed: () => _pickAndExtractImage(
                            parentContext, 'measure',
                            measureValueController: valueController),
                        icon: const Icon(Icons.camera_alt),
                        label: const Text("Extrair da Foto"),
                      )
                    ],
                  )),
              actions: [
                TextButton(
                    onPressed: () => Navigator.of(ctx).pop(),
                    child: const Text('Cancelar')),
                ElevatedButton(
                  onPressed: () async {
                    if (formKey.currentState!.validate()) {
                      await Provider.of<ProgressProvider>(parentContext,
                              listen: false)
                          .addBodyMeasureRecord(selectedType!,
                              double.parse(valueController.text));
                      if (ctx.mounted) Navigator.of(ctx).pop();
                    }
                  },
                  child: const Text('Adicionar'),
                ),
              ],
            ));
  }

  void _showAddCardioDialog(BuildContext parentContext) {
    final List<String> cardioTypes = [
      'Esteira',
      'Bicicleta',
      'Escada',
      'Corrida'
    ];
    String? selectedType = cardioTypes.first;
    final durationController = TextEditingController();
    final distanceController = TextEditingController();
    final caloriesController = TextEditingController();
    final formKey = GlobalKey<FormState>();

    showDialog(
        context: parentContext,
        builder: (ctx) => AlertDialog(
              title: const Text('Adicionar Atividade Cardio'),
              content: Form(
                  key: formKey,
                  child: SingleChildScrollView(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        DropdownButtonFormField<String>(
                          value: selectedType,
                          items: cardioTypes
                              .map((type) => DropdownMenuItem(
                                  value: type, child: Text(type)))
                              .toList(),
                          onChanged: (value) => selectedType = value,
                          decoration:
                              const InputDecoration(labelText: 'Aparelho'),
                        ),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: durationController,
                          keyboardType: TextInputType.number,
                          decoration: const InputDecoration(
                              labelText: 'Duração em minutos'),
                          validator: (v) => (v == null ||
                                  v.trim().isEmpty ||
                                  int.tryParse(v) == null)
                              ? 'Valor inválido'
                              : null,
                        ),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: distanceController,
                          keyboardType: const TextInputType.numberWithOptions(
                              decimal: true),
                          decoration: const InputDecoration(
                              labelText: 'Distância em km'),
                          validator: (v) => (v == null ||
                                  v.trim().isEmpty ||
                                  double.tryParse(v) == null)
                              ? 'Valor inválido'
                              : null,
                        ),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: caloriesController,
                          keyboardType: TextInputType.number,
                          decoration: const InputDecoration(
                              labelText: 'Calorias Queimadas'),
                          validator: (v) => (v == null ||
                                  v.trim().isEmpty ||
                                  int.tryParse(v) == null)
                              ? 'Valor inválido'
                              : null,
                        ),
                        const SizedBox(height: 20),
                        ElevatedButton.icon(
                          onPressed: () => _pickAndExtractImage(
                            parentContext,
                            'cardio',
                            durationController: durationController,
                            distanceController: distanceController,
                            caloriesController: caloriesController,
                          ),
                          icon: const Icon(Icons.camera_alt),
                          label: const Text("Extrair da Foto"),
                        )
                      ],
                    ),
                  )),
              actions: [
                TextButton(
                    onPressed: () => Navigator.of(ctx).pop(),
                    child: const Text('Cancelar')),
                ElevatedButton(
                  onPressed: () async {
                    if (formKey.currentState!.validate()) {
                      await Provider.of<ProgressProvider>(parentContext,
                              listen: false)
                          .addCardioRecord(
                              type: selectedType!,
                              duration: int.parse(durationController.text),
                              distance: double.parse(distanceController.text),
                              calories: int.parse(caloriesController.text));
                      if (ctx.mounted) Navigator.of(ctx).pop();
                    }
                  },
                  child: const Text('Adicionar'),
                ),
              ],
            ));
  }
}

class _GroupedChartView<T> extends StatelessWidget {
  final Map<String, List<T>> groupedRecords;
  final List<ChartSeries<T>> seriesList;
  final String emptyMessage;

  const _GroupedChartView(
      {required this.groupedRecords,
      required this.seriesList,
      required this.emptyMessage,
      super.key});

  // --- WIDGET DA LEGENDA CORRIGIDO ---
  Widget _buildLegend(BuildContext context) {
    if (seriesList.length < 2) return const SizedBox.shrink();

    return Padding(
      padding: const EdgeInsets.only(top: 16.0),
      child: Wrap(
        spacing: 16,
        runSpacing: 8,
        alignment: WrapAlignment.center,
        children: seriesList.map((series) {
          return Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 12,
                height: 12,
                // A propriedade 'color' foi removida daqui
                decoration: BoxDecoration(
                    color: series
                        .color, // A cor agora está apenas dentro do BoxDecoration
                    border: Border.all(color: Colors.black54, width: 0.5),
                    borderRadius: BorderRadius.circular(2)),
              ),
              const SizedBox(width: 6),
              Text(series.name, style: Theme.of(context).textTheme.bodySmall),
            ],
          );
        }).toList(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (groupedRecords.isEmpty ||
        groupedRecords.values.every((list) => list.isEmpty)) {
      return Center(
          child: Text(emptyMessage,
              style: const TextStyle(fontSize: 16, color: Colors.grey)));
    }
    return ListView(
      padding: const EdgeInsets.all(16),
      children: groupedRecords.entries.map((entry) {
        final category = entry.key;
        final records = entry.value;
        if (records.isEmpty) return const SizedBox.shrink();

        (records as List).sort((a, b) {
          final dateA = (a as dynamic).date as DateTime;
          final dateB = (b as dynamic).date as DateTime;
          return dateA.compareTo(dateB);
        });

        return Card(
          margin: const EdgeInsets.only(bottom: 16),
          elevation: 2,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: ExpansionTile(
            title:
                Text(category, style: Theme.of(context).textTheme.titleLarge),
            initiallyExpanded: true,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
                child: Column(
                  children: [
                    SizedBox(
                      height: 250,
                      child: LineChart(_buildChartData(records, seriesList)),
                    ),
                    _buildLegend(context),
                  ],
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}

LineChartData _buildChartData<T>(
    List<T> records, List<ChartSeries<T>> seriesList) {
  return LineChartData(
    lineTouchData: LineTouchData(
      handleBuiltInTouches: true,
      touchTooltipData: LineTouchTooltipData(
        tooltipBgColor: Colors.blueGrey.withOpacity(0.8),
        getTooltipItems: (List<LineBarSpot> touchedBarSpots) {
          return touchedBarSpots.map((barSpot) {
            final series = seriesList[barSpot.barIndex];

            String text;
            if (series.name.toLowerCase().contains('km')) {
              text = '${barSpot.y.toStringAsFixed(1)} km';
            } else if (series.name.toLowerCase().contains('min')) {
              text = '${barSpot.y.toInt()} min';
            } else {
              text = barSpot.y.toStringAsFixed(1);
            }

            return LineTooltipItem(
              text,
              TextStyle(
                color: series.color,
                fontWeight: FontWeight.bold,
              ),
            );
          }).toList();
        },
      ),
    ),
    gridData: const FlGridData(show: false),
    titlesData: const FlTitlesData(
      leftTitles: AxisTitles(
          sideTitles: SideTitles(showTitles: true, reservedSize: 40)),
      bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
      topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
      rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
    ),
    borderData: FlBorderData(
        show: true, border: Border.all(color: Colors.grey.shade300)),
    lineBarsData: seriesList.map((series) {
      final spots = records.asMap().entries.map((entry) {
        return FlSpot(entry.key.toDouble(), series.valueExtractor(entry.value));
      }).toList();

      return LineChartBarData(
        spots: spots,
        isCurved: true,
        color: series.color,
        barWidth: 4,
        isStrokeCapRound: true,
        dotData: const FlDotData(show: true),
        belowBarData:
            BarAreaData(show: true, color: series.color.withOpacity(0.3)),
      );
    }).toList(),
  );
}
