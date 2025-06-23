import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/exercise_model.dart';
import '../../services/auth_service.dart';
import '../../providers/exercicio_provider.dart';
import 'exercise_detail_screen.dart';

class ExerciseListScreen extends StatelessWidget {
  const ExerciseListScreen({super.key});

  void _selectExercise(BuildContext context, Exercise exercise) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => ExerciseDetailScreen(exercise: exercise),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Obtém o token do AuthService que está disponível na árvore de widgets
    final authToken = Provider.of<AuthService>(context, listen: false).token;

    // Usa o ChangeNotifierProvider para criar o ExercicioProvider
    // e passar o token para ele de forma segura.
    return ChangeNotifierProvider(
      create: (ctx) => ExercicioProvider(authToken),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Selecione um Exercício'),
        ),
        body: Consumer<ExercicioProvider>(
          builder: (ctx, exercicioData, child) {
            if (exercicioData.isLoading) {
              return const Center(child: CircularProgressIndicator());
            }
            if (exercicioData.error != null) {
              return Center(child: Text(exercicioData.error!));
            }
            return ListView.builder(
              itemCount: exercicioData.exercises.length,
              itemBuilder: (ctx, index) {
                final exercise = exercicioData.exercises[index];
                return Card(
                  margin:
                      const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                  child: ListTile(
                    leading: CircleAvatar(
                      child: Icon(exercise.icon),
                    ),
                    title: Text(exercise.displayName,
                        style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(exercise.description),
                    trailing: const Icon(Icons.arrow_forward_ios),
                    onTap: () => _selectExercise(context, exercise),
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
