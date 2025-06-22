import 'dart:convert';
import 'package:flutter/material.dart';
import '../models/exercise_model.dart';
import '../services/api_service.dart';

class ExercicioProvider with ChangeNotifier {
  List<Exercise> _exercises = [];
  bool _isLoading = true;
  String? _error;
  final String? authToken; // Propriedade para guardar o token de autenticação

  List<Exercise> get exercises => [..._exercises];
  bool get isLoading => _isLoading;
  String? get error => _error;

  // O construtor agora requer o token para funcionar
  ExercicioProvider(this.authToken) {
    // Só tenta buscar os exercícios se houver um token
    if (authToken != null && authToken!.isNotEmpty) {
      fetchExercises();
    } else {
      _isLoading = false;
      _error = "Utilizador não autenticado. Por favor, faça login novamente.";
      notifyListeners();
    }
  }

  /// Busca a lista de exercícios da API, enviando o token de autenticação.
  Future<void> fetchExercises() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // Passa o token para a chamada da API
      final response = await ApiService.get('exercicios/', token: authToken);
      if (response.statusCode == 200) {
        final List<dynamic> responseData = json.decode(utf8.decode(response.bodyBytes));
        _exercises = responseData.map((data) => Exercise.fromJson(data)).toList();
      } else {
        _error = "Não foi possível carregar a lista de exercícios. (Erro: ${response.statusCode})";
      }
    } catch (e) {
      _error = "Erro de conexão ao buscar exercícios.";
    }

    _isLoading = false;
    notifyListeners();
  }
}
