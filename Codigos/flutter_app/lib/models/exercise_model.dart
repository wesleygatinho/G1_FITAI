import 'package:flutter/material.dart';

class Exercise {
  final String id;
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
      id: json['id'],
      apiName: json['nome'],
      // --- TRADUÇÃO ACONTECE AQUI ---
      displayName: _getDisplayName(json['nome']),
      description: json['descricao'] ?? 'Sem descrição.',
      instructions: json['instrucoes'] ?? 'Sem instruções.',
      icon: _getIconForExercise(json['nome']),
    );
  }

  // Função auxiliar para traduzir o nome técnico para o nome de exibição
  static String _getDisplayName(String apiName) {
    switch (apiName) {
      case 'squat':
        return 'Agachamento';
      case 'push_up':
        return 'Flexão de Braço';
      case 'hammer_curl':
        return 'Rosca Martelo';
      default:
        // Se um novo exercício for adicionado, capitaliza o nome técnico como fallback
        return apiName.replaceAll('_', ' ').split(' ').map((l) => l.isEmpty ? '' : l[0].toUpperCase() + l.substring(1)).join(" ");
    }
  }

  // Função auxiliar para atribuir um ícone com base no nome do exercício
  static IconData _getIconForExercise(String apiName) {
    switch (apiName) {
      case 'squat': return Icons.accessibility_new;
      case 'push_up': return Icons.self_improvement;
      case 'hammer_curl': return Icons.fitness_center;
      default: return Icons.fitness_center;
    }
  }
}