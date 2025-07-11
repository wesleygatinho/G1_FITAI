import 'dart:convert';
import 'package:flutter/material.dart';
import '../models/ia_interaction.dart';
import '../services/api_service.dart';
import '../services/daily_tip_cache_service.dart';

class AiProvider with ChangeNotifier {
  String? _dailyTip;
  String? _generatedPlan;
  bool _isLoadingTip = false;
  bool _isLoadingPlan = false;

  List<IAInteraction> _history = [];
  bool _isLoadingHistory = true;

  String? get dailyTip => _dailyTip;
  String? get generatedPlan => _generatedPlan;
  bool get isLoadingTip => _isLoadingTip;
  bool get isLoadingPlan => _isLoadingPlan;
  List<IAInteraction> get history => [..._history];
  bool get isLoadingHistory => _isLoadingHistory;

  AiProvider() {
    fetchDailyTip();
    fetchHistory();
  }

  Future<void> fetchDailyTip() async {
    _isLoadingTip = true;
    notifyListeners();

    try {
      // NOVA LÓGICA: Primeiro verifica se já existe uma dica para hoje
      String? cachedTip = await DailyTipCacheService.getTodaysTip();

      if (cachedTip != null) {
        // Se existe dica cached para hoje, usa ela
        _dailyTip = cachedTip;
        _isLoadingTip = false;
        notifyListeners();
        return;
      }

      // Se não existe dica cached, busca uma nova da API
      final response = await ApiService.get('ai/tips/daily');
      if (response.statusCode == 200) {
        final responseData = json.decode(utf8.decode(response.bodyBytes));
        _dailyTip = responseData['tip'];

        // Salva a nova dica no cache
        await DailyTipCacheService.saveTodaysTip(_dailyTip!);
      } else {
        _dailyTip = 'Erro ao buscar a dica do dia.';
      }
    } catch (e) {
      _dailyTip = 'Erro de conexão ao buscar a dica.';
    }

    _isLoadingTip = false;
    notifyListeners();
  }

  /// FUNÇÃO MODIFICADA: Agora força uma nova dica (ignora cache)
  Future<void> forceNewDailyTip() async {
    _isLoadingTip = true;
    notifyListeners();

    try {
      // Força buscar uma nova dica da API
      final response = await ApiService.get('ai/tips/daily');
      if (response.statusCode == 200) {
        final responseData = json.decode(utf8.decode(response.bodyBytes));
        _dailyTip = responseData['tip'];

        // Atualiza o cache com a nova dica
        await DailyTipCacheService.saveTodaysTip(_dailyTip!);
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
      final response = await ApiService.post(
        'ai/plans/generate',
        json.encode({'prompt': prompt}),
      );
      if (response.statusCode == 201) {
        final responseData = json.decode(utf8.decode(response.bodyBytes));
        _generatedPlan = responseData['plan'];
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

  Future<void> fetchHistory() async {
    _isLoadingHistory = true;
    notifyListeners();
    try {
      final response = await ApiService.get('ai/interactions/history');
      if (response.statusCode == 200) {
        final List<dynamic> responseData = json.decode(
          utf8.decode(response.bodyBytes),
        );
        _history = responseData
            .map((data) => IAInteraction.fromJson(data))
            .toList();
      }
    } catch (e) {
      print("Erro ao buscar histórico de IA: $e");
    }
    _isLoadingHistory = false;
    notifyListeners();
  }
}
