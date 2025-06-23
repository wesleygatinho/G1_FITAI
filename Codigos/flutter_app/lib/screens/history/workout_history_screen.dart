import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../services/auth_service.dart';
import '../../providers/workout_history_provider.dart';

class WorkoutHistoryScreen extends StatelessWidget {
  const WorkoutHistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Obtém o token para o provider, garantindo que as chamadas são autenticadas
    final authToken = Provider.of<AuthService>(context, listen: false).token;

    return ChangeNotifierProvider(
      create: (ctx) => WorkoutHistoryProvider(authToken), // Passa o token
      child: Scaffold(
        appBar: AppBar(title: const Text('Histórico de Treinos')),
        body: Consumer<WorkoutHistoryProvider>(
          builder: (ctx, historyData, _) {
            if (historyData.isLoading) {
              return const Center(child: CircularProgressIndicator());
            }
            if (historyData.error != null) {
              return Center(child: Text(historyData.error!));
            }
            if (historyData.history.isEmpty) {
              return const Center(child: Text('Nenhum treino guardado ainda.'));
            }
            return ListView.builder(
              padding: const EdgeInsets.all(8),
              itemCount: historyData.history.length,
              itemBuilder: (ctx, index) {
                final session = historyData.history[index];
                return Card(
                  elevation: 2,
                  margin:
                      const EdgeInsets.symmetric(vertical: 6, horizontal: 8),
                  child: ExpansionTile(
                    leading: const Icon(Icons.fitness_center),
                    title: Text(
                      'Treino de ${DateFormat('dd/MM/yyyy \'às\' HH:mm').format(session.dataInicio)}',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    children: session.itens.map((item) {
                      return ListTile(
                        dense: true,
                        // --- CORREÇÃO AQUI ---
                        // Acede ao nome do exercício através do objeto 'exercicio'
                        title: Text(item.exercicio.nome),
                        trailing:
                            Text('${item.series}x ${item.repeticoes} reps'),
                      );
                    }).toList(),
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
