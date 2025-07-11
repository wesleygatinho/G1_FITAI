import 'dart:convert';
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/daily_tip_cache_service.dart';

class DashboardProvider with ChangeNotifier {
  String? _dailyTip;
  bool _isLoading = true;
  String? _error;
  bool _isDisposed = false;

  String? get dailyTip => _dailyTip;
  bool get isLoading => _isLoading;
  String? get error => _error;

  DashboardProvider() {
    fetchDashboardData();
  }

  @override
  void dispose() {
    _isDisposed = true;
    super.dispose();
  }

  Future<void> fetchDashboardData() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // NOVA LÓGICA: Primeiro verifica se já existe uma dica para hoje
      String? cachedTip = await DailyTipCacheService.getTodaysTip();

      if (cachedTip != null) {
        // Se existe dica cached para hoje, usa ela
        _dailyTip = cachedTip;
        _isLoading = false;
        if (!_isDisposed) {
          notifyListeners();
        }
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
        _error = 'Não foi possível carregar a dica do dia.';
      }
    } catch (e) {
      _error = 'Erro de conexão. Verifique a sua internet.';
    }

    _isLoading = false;

    if (!_isDisposed) {
      notifyListeners();
    }
  }

  /// NOVA FUNÇÃO: Força buscar uma nova dica (ignora cache)
  Future<void> forceRefreshTip() async {
    await DailyTipCacheService.clearCache();
    await fetchDashboardData();
  }
}
