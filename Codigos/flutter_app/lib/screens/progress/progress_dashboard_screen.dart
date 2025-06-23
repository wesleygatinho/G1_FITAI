import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../services/auth_service.dart';
import '../../providers/progress_provider.dart';

class ProgressDashboardScreen extends StatelessWidget {
  const ProgressDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Obtém o token para passar para o provider
    final authToken = Provider.of<AuthService>(context, listen: false).token;

    return ChangeNotifierProvider(
      create: (ctx) => ProgressProvider(authToken),
      child: DefaultTabController(
        length: 3, // Número de abas
        child: Scaffold(
          appBar: AppBar(
            title: const Text('Painel de Progresso'),
            bottom: const TabBar(
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
                  _WeightView(records: progressData.weightRecords),
                  _GroupedChartView<BodyMeasureRecord>(
                    groupedRecords: progressData.groupedBodyMeasureRecords,
                    unit: 'cm',
                    emptyMessage: 'Nenhum dado de medida registado.',
                    recordToValue: (record) => record.value,
                  ),
                  _GroupedChartView<CardioRecord>(
                    groupedRecords: progressData.groupedCardioRecords,
                    unit: 'min',
                    emptyMessage: 'Nenhum dado de cardio registado.',
                    recordToValue: (record) => record.duration.toDouble(),
                  ),
                ],
              );
            },
          ),
          floatingActionButton: Builder(
            builder: (context) => FloatingActionButton(
              onPressed: () => _showAddDialog(context),
              child: const Icon(Icons.add),
            ),
          ),
        ),
      ),
    );
  }

  // Lógica para mostrar o diálogo correto dependendo da aba selecionada
  void _showAddDialog(BuildContext context) {
    final tabIndex = DefaultTabController.of(context).index;
    if (tabIndex == 0) _showAddWeightDialog(context);
    if (tabIndex == 1) _showAddMeasureDialog(context);
    if (tabIndex == 2) _showAddCardioDialog(context);
  }

  // --- DIÁLOGOS PARA ADICIONAR NOVOS REGISTOS ---

  void _showAddWeightDialog(BuildContext parentContext) {
    final weightController = TextEditingController();
    final formKey = GlobalKey<FormState>();

    showDialog(
      context: parentContext,
      builder: (ctx) => AlertDialog(
        title: const Text('Adicionar Novo Peso'),
        content: Form(
          key: formKey,
          child: TextFormField(
            controller: weightController,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
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
    final List<String> measureTypes = ['Braço', 'Glúteo', 'Coxa'];
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
                      TextFormField(
                        controller: valueController,
                        keyboardType: const TextInputType.numberWithOptions(
                            decimal: true),
                        decoration:
                            const InputDecoration(labelText: 'Valor em cm'),
                        validator: (v) =>
                            (v == null || double.tryParse(v) == null)
                                ? 'Valor inválido'
                                : null,
                      ),
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
    final List<String> cardioTypes = ['Bicicleta', 'Esteira', 'Escada'];
    String? selectedType = cardioTypes.first;
    final durationController = TextEditingController();
    final formKey = GlobalKey<FormState>();

    showDialog(
        context: parentContext,
        builder: (ctx) => AlertDialog(
              title: const Text('Adicionar Atividade Cardio'),
              content: Form(
                  key: formKey,
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
                      TextFormField(
                        controller: durationController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                            labelText: 'Duração em minutos'),
                        validator: (v) => (v == null || int.tryParse(v) == null)
                            ? 'Valor inválido'
                            : null,
                      ),
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
                          .addCardioRecord(selectedType!,
                              int.parse(durationController.text));
                      if (ctx.mounted) Navigator.of(ctx).pop();
                    }
                  },
                  child: const Text('Adicionar'),
                ),
              ],
            ));
  }
}

// --- WIDGETS REUTILIZÁVEIS PARA AS ABAS ---

class _WeightView extends StatelessWidget {
  final List<WeightRecord> records;
  const _WeightView({required this.records});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text('Evolução do Peso (kg)',
              style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 20),
          SizedBox(
            height: 300,
            child: records.isEmpty
                ? const Center(child: Text('Nenhum dado de peso registado.'))
                : LineChart(
                    _buildChartData(records.map((r) => r.weight).toList())),
          ),
        ],
      ),
    );
  }
}

class _GroupedChartView<T> extends StatelessWidget {
  final Map<String, List<T>> groupedRecords;
  final String unit;
  final String emptyMessage;
  final double Function(T) recordToValue;

  const _GroupedChartView(
      {required this.groupedRecords,
      required this.unit,
      required this.emptyMessage,
      required this.recordToValue,
      super.key});

  @override
  Widget build(BuildContext context) {
    if (groupedRecords.isEmpty) {
      return Center(
          child: Text(emptyMessage,
              style: const TextStyle(fontSize: 16, color: Colors.grey)));
    }
    return ListView(
      padding: const EdgeInsets.all(16),
      children: groupedRecords.entries.map((entry) {
        final category = entry.key;
        final records = entry.value;
        (records as List).sort((a, b) => a.date.compareTo(b.date));

        return Card(
          margin: const EdgeInsets.only(bottom: 16),
          child: ExpansionTile(
            title:
                Text(category, style: Theme.of(context).textTheme.titleLarge),
            children: [
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: SizedBox(
                  height: 200,
                  child: LineChart(
                      _buildChartData(records.map(recordToValue).toList())),
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}

// --- FUNÇÃO AUXILIAR REUTILIZÁVEL PARA CRIAR GRÁFICOS ---

LineChartData _buildChartData(List<double> dataPoints) {
  final spots = dataPoints.asMap().entries.map((entry) {
    return FlSpot(entry.key.toDouble(), entry.value);
  }).toList();

  return LineChartData(
    gridData: const FlGridData(show: false),
    titlesData: FlTitlesData(
      leftTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: true, reservedSize: 40)),
      bottomTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
      topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
      rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
    ),
    borderData: FlBorderData(
        show: true, border: Border.all(color: Colors.grey.shade400)),
    lineBarsData: [
      LineChartBarData(
        spots: spots,
        isCurved: true,
        color: Colors.orange,
        barWidth: 4,
        isStrokeCapRound: true,
        dotData: const FlDotData(show: true),
        belowBarData:
            BarAreaData(show: true, color: Colors.orange.withOpacity(0.3)),
      ),
    ],
  );
}
