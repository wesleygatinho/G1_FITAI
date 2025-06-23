import 'dart:convert';
import 'package:flutter/material.dart';
import '../services/api_service.dart';

/// Representa uma única série de um exercício, com o número de repetições.
class ExerciseSet {
  final int series;
  final int repetitions;

  ExerciseSet({required this.series, required this.repetitions});
}

/// Gere o estado de uma sessão de treino em andamento.
class WorkoutSessionProvider with ChangeNotifier {
  final String exerciseId; // O ID (UUID) do exercício, vindo do backend.
  final String exerciseName; // O nome do exercício (para UI, ex: "Agachamento").

  final List<ExerciseSet> _completedSets = [];
  int _currentSeries = 1;
  int _lastRepCount = 0;
  bool _isSaving = false;

  // Getters públicos para a UI aceder ao estado.
  List<ExerciseSet> get completedSets => [..._completedSets];
  bool get isSaving => _isSaving;
  int get currentSeries => _currentSeries;

  WorkoutSessionProvider({required this.exerciseId, required this.exerciseName});

  /// Atualiza a contagem de repetições da série atual com base no feedback da IA.
  void recordRepetition(int newRepCount) {
    _lastRepCount = newRepCount;
  }

  /// Finaliza a série atual, adiciona-a à lista de séries completas
  /// e prepara para a próxima.
  void finishSet() {
    // Só adiciona a série se pelo menos uma repetição foi contada.
    if (_lastRepCount > 0) {
      _completedSets.add(ExerciseSet(series: _currentSeries, repetitions: _lastRepCount));
      _currentSeries++;
      _lastRepCount = 0; // Zera a contagem para a próxima série
      notifyListeners();
    }
  }

  /// Envia a sessão de treino completa para o backend para ser guardada.
  Future<bool> saveWorkoutSession() async {
    // Garante que a última série em progresso seja adicionada antes de guardar.
    if (_lastRepCount > 0) {
      finishSet();
    }
    // Não guarda uma sessão vazia.
    if (_completedSets.isEmpty) return false;

    _isSaving = true;
    notifyListeners();

    // --- CORREÇÃO PRINCIPAL ---
    // Prepara a lista de itens para enviar à API.
    // O backend espera um campo 'exercicio_id' com o UUID do exercício.
    final items = _completedSets.map((set) {
      return {
        'exercicio_id': exerciseId, // Usa o ID do exercício (UUID) que foi recebido.
        'series': set.series,
        'repeticoes': set.repetitions,
        'feedback_ia': 'Feedback a ser implementado', // Placeholder
      };
    }).toList();

    final sessionData = {'itens': items};

    try {
      final response = await ApiService.post('sessions/', json.encode(sessionData));
      _isSaving = false;
      notifyListeners();
      // O backend retorna 201 (Created) em caso de sucesso.
      return response.statusCode == 201;
    } catch (e) {
      _isSaving = false;
      notifyListeners();
      return false;
    }
  }
}
