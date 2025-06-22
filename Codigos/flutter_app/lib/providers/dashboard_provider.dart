import 'dart:convert';
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DashboardProvider with ChangeNotifier {
  String? _dailyTip;
  bool _isLoading = true;
  String? _error;

  String? get dailyTip => _dailyTip;
  bool get isLoading => _isLoading;
  String? get error => _error;

  DashboardProvider() {
    fetchDashboardData();
  }

  Future<void> fetchDashboardData() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // Usar o endpoint que já criámos para as dicas
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
    notifyListeners();
  }
}
