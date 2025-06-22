import 'dart:convert';
import 'package:flutter/material.dart';
import '../models/ia_interaction.dart'; // Importar o novo modelo
import '../services/api_service.dart';

class AiProvider with ChangeNotifier {
  String? _dailyTip;
  String? _generatedPlan;
  bool _isLoadingTip = false;
  bool _isLoadingPlan = false;

  // --- NOVAS PROPRIEDADES PARA O HISTÓRICO ---
  List<IAInteraction> _history = [];
  bool _isLoadingHistory = true;

  // --- Getters ---
  String? get dailyTip => _dailyTip;
  String? get generatedPlan => _generatedPlan;
  bool get isLoadingTip => _isLoadingTip;
  bool get isLoadingPlan => _isLoadingPlan;
  List<IAInteraction> get history => [..._history];
  bool get isLoadingHistory => _isLoadingHistory;

  // Ao iniciar o provider, busca a dica do dia e o histórico
  AiProvider() {
    fetchDailyTip();
    fetchHistory();
  }

  Future<void> fetchDailyTip() async {
    _isLoadingTip = true;
    notifyListeners();
    try {
      final response = await ApiService.get('ai/tips/daily');
      if (response.statusCode == 200) {
        final responseData = json.decode(utf8.decode(response.bodyBytes));
        _dailyTip = responseData['tip'];
      } else {
        _dailyTip = 'Erro ao buscar a dica do dia.';
      }
    } catch (e) {
      _dailyTip = 'Erro de conexão ao buscar a dica.';
    }
    _isLoadingTip = false;
    notifyListeners();
  }

  Future<void> generatePlan(String prompt) async {
    _isLoadingPlan = true;
    _generatedPlan = null;
    notifyListeners();
    try {
      final response = await ApiService.post('ai/plans/generate', json.encode({'prompt': prompt}));
      if (response.statusCode == 201) {
        final responseData = json.decode(utf8.decode(response.bodyBytes));
        _generatedPlan = responseData['plan'];
        // Após gerar um novo plano, atualiza o histórico
        await fetchHistory();
      } else {
        final errorData = json.decode(response.body);
        _generatedPlan = 'Erro: ${errorData['detail']}';
      }
    } catch (e) {
      _generatedPlan = 'Erro de conexão ao gerar o plano.';
    }
    _isLoadingPlan = false;
    notifyListeners();
  }

  // --- NOVA FUNÇÃO PARA BUSCAR O HISTÓRICO ---
  Future<void> fetchHistory() async {
    _isLoadingHistory = true;
    notifyListeners();
    try {
      final response = await ApiService.get('ai/interactions/history');
      if (response.statusCode == 200) {
        final List<dynamic> responseData = json.decode(utf8.decode(response.bodyBytes));
        _history = responseData.map((data) => IAInteraction.fromJson(data)).toList();
      }
    } catch (e) {
      // Ignora o erro silenciosamente para não interromper a UI principal
      print("Erro ao buscar histórico de IA: $e");
    }
    _isLoadingHistory = false;
    notifyListeners();
  }
}
