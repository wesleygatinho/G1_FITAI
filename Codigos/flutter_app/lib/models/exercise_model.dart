import 'package:flutter/material.dart';

class Exercise {
  final String id; // O ID é um UUID em formato de String
  final String apiName; // O nome técnico para a API (ex: "push_up")
  final String displayName; // O nome para exibir ao utilizador (ex: "Flexão de Braço")
  final String description;
  final String instructions;
  final IconData icon;

  Exercise({
    required this.id,
    required this.apiName,
    required this.displayName,
    required this.description,
    required this.instructions,
    required this.icon,
  });

  // Factory para criar um Exercício a partir do JSON da API
  factory Exercise.fromJson(Map<String, dynamic> json) {
    return Exercise(
      id: json['id'], // --- CORREÇÃO: Usar o 'id' (UUID) que vem da API ---
      apiName: json['nome'],
      displayName: _capitalize(json['nome'].replaceAll('_', ' ')),
      description: json['descricao'] ?? 'Sem descrição.',
      instructions: json['instrucoes'] ?? 'Sem instruções.',
      icon: _getIconForExercise(json['nome']),
    );
  }

  static String _capitalize(String s) => (s.isEmpty) ? '' : s[0].toUpperCase() + s.substring(1);

  static IconData _getIconForExercise(String exerciseName) {
    switch (exerciseName) {
      case 'squat': return Icons.accessibility_new;
      case 'push_up': return Icons.self_improvement;
      case 'hammer_curl': return Icons.fitness_center;
      default: return Icons.fitness_center;
    }
  }
}
