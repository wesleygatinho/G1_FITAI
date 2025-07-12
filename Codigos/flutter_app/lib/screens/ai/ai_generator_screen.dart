import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/ai_provider.dart';
import 'package:table_calendar/table_calendar.dart';
import '../../models/ia_interaction.dart';

class AiGeneratorScreen extends StatelessWidget {
  const AiGeneratorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (ctx) => AiProvider(),
      child: Scaffold(
        appBar: AppBar(title: const Text('Assistente de IA')),
        body: LayoutBuilder(
          builder: (context, constraints) {
            return RefreshIndicator(
              onRefresh: () => Provider.of<AiProvider>(context, listen: false)
                  .fetchHistory(),
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                child: ConstrainedBox(
                  constraints: BoxConstraints(minHeight: constraints.maxHeight),
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(
                        16, 16, 16, 32), // bottom extra!
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        _buildDailyTipCard(),
                        const SizedBox(height: 24),
                        _buildPlanGeneratorCard(),
                        const SizedBox(height: 24),
                        const Divider(),
                        const SizedBox(height: 16),
                        Text(
                          'Histórico de Interações',
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        const SizedBox(height: 16),
                        const InteractionCalendarWidget(),
                      ],
                    ),
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

// --- DICA DO DIA ---
class _buildDailyTipCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Dica Fitness do Dia',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            Consumer<AiProvider>(
              builder: (ctx, aiData, _) {
                if (aiData.isLoadingTip) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (aiData.dailyTip != null) {
                  return Text(
                    aiData.dailyTip!,
                    style: Theme.of(context).textTheme.bodyLarge,
                  );
                }
                return const SizedBox.shrink();
              },
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              icon: const Icon(Icons.lightbulb_outline),
              label: const Text('Obter Nova Dica'),
              onPressed: () {
                Provider.of<AiProvider>(
                  context,
                  listen: false,
                ).forceNewDailyTip();
              },
            ),
          ],
        ),
      ),
    );
  }
}

// --- GERADOR DE PLANO ---
class _buildPlanGeneratorCard extends StatefulWidget {
  @override
  State<_buildPlanGeneratorCard> createState() =>
      _buildPlanGeneratorCardState();
}

class _buildPlanGeneratorCardState extends State<_buildPlanGeneratorCard> {
  final _promptController = TextEditingController();

  @override
  void dispose() {
    _promptController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_promptController.text.trim().isEmpty) return;
    Provider.of<AiProvider>(
      context,
      listen: false,
    ).generatePlan(_promptController.text);
  }

  @override
  Widget build(BuildContext context) {
    final aiProvider = Provider.of<AiProvider>(context);
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Gerador de Plano Personalizado',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _promptController,
              decoration: const InputDecoration(
                labelText: 'Descreva o seu objetivo...',
                hintText: 'Ex: "Um treino de 3 dias para hipertrofia"',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              icon: const Icon(Icons.auto_awesome),
              label: const Text('Gerar Plano'),
              onPressed: aiProvider.isLoadingPlan ? null : _submit,
            ),
            const SizedBox(height: 24),
            if (aiProvider.isLoadingPlan)
              const Center(child: CircularProgressIndicator())
            else if (aiProvider.generatedPlan != null)
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  aiProvider.generatedPlan!,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
          ],
        ),
      ),
    );
  }
}

// --- CALENDÁRIO DE INTERAÇÕES (DICAS + PLANOS) ---
class InteractionCalendarWidget extends StatefulWidget {
  const InteractionCalendarWidget({Key? key}) : super(key: key);

  @override
  State<InteractionCalendarWidget> createState() =>
      _InteractionCalendarWidgetState();
}

class _InteractionCalendarWidgetState extends State<InteractionCalendarWidget> {
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;

  @override
  Widget build(BuildContext context) {
    final aiProvider = Provider.of<AiProvider>(context);

    // Agrupa todas as interações por data
    final Map<DateTime, List<IAInteraction>> interactionsByDate = {};
    for (final interaction in aiProvider.history) {
      final date = DateTime(
        interaction.data.year,
        interaction.data.month,
        interaction.data.day,
      );
      interactionsByDate.putIfAbsent(date, () => []).add(interaction);
    }

    List<IAInteraction> _getInteractionsForDay(DateTime day) {
      final date = DateTime(day.year, day.month, day.day);
      return interactionsByDate[date] ?? [];
    }

    return Column(
      children: [
        TableCalendar<IAInteraction>(
          firstDay: DateTime.now().subtract(const Duration(days: 365)),
          lastDay: DateTime.now().add(const Duration(days: 365)),
          focusedDay: _focusedDay,
          selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
          calendarFormat: CalendarFormat.month,
          eventLoader: _getInteractionsForDay,
          onDaySelected: (selectedDay, focusedDay) {
            setState(() {
              _selectedDay = selectedDay;
              _focusedDay = focusedDay;
            });
            final interactions = _getInteractionsForDay(selectedDay);
            if (interactions.isNotEmpty) {
              showDialog(
                context: context,
                builder: (_) => AlertDialog(
                  title: Text(
                      'Interações de ${selectedDay.day}/${selectedDay.month}/${selectedDay.year}'),
                  content: SingleChildScrollView(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: interactions.map((interaction) {
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 8.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              if (interaction.promptUsuario.trim().isNotEmpty)
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text("Plano solicitado:",
                                        style: const TextStyle(
                                            fontWeight: FontWeight.bold)),
                                    Text(interaction.promptUsuario),
                                    const SizedBox(height: 4),
                                    Text("Plano:",
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold)),
                                    Text(interaction.respostaIa),
                                  ],
                                )
                              else
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text("Dica do Dia:",
                                        style: const TextStyle(
                                            fontWeight: FontWeight.bold)),
                                    Text(interaction.respostaIa),
                                  ],
                                ),
                            ],
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                ),
              );
            }
          },
          calendarStyle: const CalendarStyle(
            markerDecoration: BoxDecoration(
              color: Colors.orange,
              shape: BoxShape.circle,
            ),
          ),
          headerStyle: const HeaderStyle(
            formatButtonVisible: false,
            titleCentered: true,
          ),
        ),
        const SizedBox(height: 16),
        if (_selectedDay != null)
          ..._getInteractionsForDay(_selectedDay!).map((interaction) => Card(
                margin: const EdgeInsets.symmetric(vertical: 4),
                child: ListTile(
                  leading: Icon(interaction.promptUsuario.trim().isNotEmpty
                      ? Icons.history
                      : Icons.lightbulb),
                  title: interaction.respostaIa.isNotEmpty
                      ? Text(interaction.respostaIa)
                      : null,
                  subtitle: Text(
                      "Registrado em: ${interaction.data.day}/${interaction.data.month}/${interaction.data.year}"),
                ),
              )),
        if (_selectedDay != null &&
            _getInteractionsForDay(_selectedDay!).isEmpty)
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Text('Nenhuma interação neste dia.'),
          ),
      ],
    );
  }
}
