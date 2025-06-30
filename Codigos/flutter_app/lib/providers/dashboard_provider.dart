import 'dart:convert';
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DashboardProvider with ChangeNotifier {
  String? _dailyTip;
  bool _isLoading = true;
  String? _error;
  bool _isDisposed = false; // Adicionamos um flag

  String? get dailyTip => _dailyTip;
  bool get isLoading => _isLoading;
  String? get error => _error;

  DashboardProvider() {
    fetchDashboardData();
  }

  @override
  void dispose() {
    _isDisposed = true; // Marcamos como "destruído"
    super.dispose();
  }

  Future<void> fetchDashboardData() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiService.get('ai/tips/daily');
      if (response.statusCode == 200) {
        final responseData = json.decode(utf8.decode(response.bodyBytes));
        _dailyTip = responseData['tip'];
      } else {
        _error = 'Não foi possível carregar a dica do dia.';
      }
    } catch (e) {
      _error = 'Erro de conexão. Verifique a sua internet.';
    }

    _isLoading = false;
    
    // Só notifica se o provider ainda estiver "vivo"
    if (!_isDisposed) {
      notifyListeners();
    }
  }
}