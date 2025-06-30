import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:table_calendar/table_calendar.dart';
import '../../models/workout_model.dart';
import '../../providers/workout_history_provider.dart';
import '../../services/auth_service.dart';

class WorkoutHistoryScreen extends StatelessWidget {
  const WorkoutHistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final authToken = Provider.of<AuthService>(context, listen: false).token;

    return ChangeNotifierProvider(
      create: (ctx) => WorkoutHistoryProvider(authToken),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Histórico de Treinos'),
        ),
        body: Consumer<WorkoutHistoryProvider>(
          builder: (ctx, historyData, _) {
            if (historyData.isLoading) {
              return const Center(child: CircularProgressIndicator());
            }
            if (historyData.error != null) {
              return Center(child: Text(historyData.error!));
            }

            // A tela agora é uma coluna com o calendário e a lista
            return Column(
              children: [
                TableCalendar<SessaoDeTreino>(
                  firstDay: DateTime.utc(2023, 1, 1),
                  lastDay: DateTime.now().add(const Duration(days: 365)),
                  focusedDay: historyData.focusedDay,
                  selectedDayPredicate: (day) =>
                      isSameDay(historyData.selectedDay, day),
                  onDaySelected: historyData.onDaySelected,
                  eventLoader: historyData.getEventsForDay,
                  calendarStyle: CalendarStyle(
                    // Marcador para dias com treino
                    markerDecoration: BoxDecoration(
                      color: Theme.of(context).primaryColor,
                      shape: BoxShape.circle,
                    ),
                  ),
                  headerStyle: const HeaderStyle(
                    formatButtonVisible: false,
                    titleCentered: true,
                  ),
                ),
                const SizedBox(height: 8.0),
                Expanded(
                  child: _buildWorkoutList(historyData.workoutsForSelectedDay),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildWorkoutList(List<SessaoDeTreino> sessions) {
    if (sessions.isEmpty) {
      return const Center(
        child: Text('Nenhum treino registrado para este dia.'),
      );
    }
    return ListView.builder(
      padding: const EdgeInsets.all(8),
      itemCount: sessions.length,
      itemBuilder: (ctx, index) {
        final session = sessions[index];
        return Card(
          elevation: 2,
          margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 8),
          child: ExpansionTile(
            leading: const Icon(Icons.fitness_center),
            title: Text(
              'Treino às ${DateFormat('HH:mm').format(session.dataInicio.toLocal())}',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            subtitle: Text('${session.itens.length} exercícios'),
            children: session.itens.map((item) {
              return ListTile(
                dense: true,
                title: Text(item.exercicio.nome),
                trailing: Text('${item.series}x ${item.repeticoes} reps'),
              );
            }).toList(),
          ),
        );
      },
    );
  }
}
