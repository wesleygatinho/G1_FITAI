import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:provider/provider.dart';
import '../../models/exercise_model.dart';
import '../../services/auth_service.dart';
import '../../providers/workout_session_provider.dart';
import '../../services/api_service.dart';
import 'monitoring_screen.dart';

class ExerciseDetailScreen extends StatefulWidget {
  final Exercise exercise;

  const ExerciseDetailScreen({super.key, required this.exercise});

  @override
  State<ExerciseDetailScreen> createState() => _ExerciseDetailScreenState();
}

class _ExerciseDetailScreenState extends State<ExerciseDetailScreen> {
  String? _instructions;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchInstructions();
  }

  Future<void> _fetchInstructions() async {
    // Obtém o token para a chamada de API
    final authToken = Provider.of<AuthService>(context, listen: false).token;

    try {
      // --- CORREÇÃO AQUI: Usa apiName para a chamada de API e passa o token ---
      final response = await ApiService.get(
          'exercicios/${widget.exercise.apiName}/instructions',
          token: authToken);
      if (response.statusCode == 200 && mounted) {
        setState(() {
          _instructions =
              json.decode(utf8.decode(response.bodyBytes))['instructions'];
          _isLoading = false;
        });
      } else {
        setState(() {
          _instructions = 'Não foi possível carregar as instruções.';
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _instructions = 'Erro de conexão. Tente novamente.';
          _isLoading = false;
        });
      }
    }
  }

  void _startMonitoring(BuildContext context) {
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => ChangeNotifierProvider(
          // --- CORREÇÃO AQUI: Usa displayName para a UI ---
          create: (ctx) => WorkoutSessionProvider(
            exerciseId: widget.exercise.id,
            exerciseName: widget.exercise.displayName,
          ),
          child: MonitoringScreen(exercise: widget.exercise),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // --- CORREÇÃO AQUI: Usa displayName para a UI ---
        title: Text(widget.exercise.displayName),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Instruções de Execução',
                    style: Theme.of(context)
                        .textTheme
                        .headlineSmall
                        ?.copyWith(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  if (_instructions != null)
                    MarkdownBody(
                      data: _instructions!,
                      styleSheet:
                          MarkdownStyleSheet.fromTheme(Theme.of(context))
                              .copyWith(
                        p: Theme.of(context).textTheme.bodyLarge,
                      ),
                    ),
                ],
              ),
            ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _startMonitoring(context),
        label: const Text('INICIAR MONITORAMENTO'),
        icon: const Icon(Icons.videocam),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}
