import 'dart:convert';
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/workout_model.dart';

class WorkoutHistoryProvider with ChangeNotifier {
  List<SessaoDeTreino> _history = [];
  bool _isLoading = false;
  String? _error;
  final String? authToken; // Nova propriedade para guardar o token

  List<SessaoDeTreino> get history => [..._history];
  bool get isLoading => _isLoading;
  String? get error => _error;

  // O construtor agora requer o token para funcionar
  WorkoutHistoryProvider(this.authToken) {
    if (authToken != null && authToken!.isNotEmpty) {
      fetchHistory();
    } else {
      _isLoading = false;
      _error = "Utilizador não autenticado.";
    }
  }

  Future<void> fetchHistory() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // Passa o token para a chamada da API
      final response = await ApiService.get('sessions/', token: authToken);
      if (response.statusCode == 200) {
        final List<dynamic> responseData = json.decode(utf8.decode(response.bodyBytes));
        _history = responseData.map((data) => SessaoDeTreino.fromJson(data)).toList();
      } else {
        _error = "Erro ao carregar o histórico: ${response.statusCode}";
      }
    } catch (e, stacktrace) {
      print('Erro ao buscar histórico de treinos: $e');
      print('Stacktrace: $stacktrace');
      _error = "Não foi possível processar os dados do histórico.";
    }

    _isLoading = false;
    notifyListeners();
  }
}
