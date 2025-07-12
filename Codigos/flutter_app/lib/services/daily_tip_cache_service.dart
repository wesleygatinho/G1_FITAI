import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

/// Serviço para cache de dicas do dia, evitando múltiplas requisições
class DailyTipCacheService {
  static const String _tipKey = 'daily_tip';
  static const String _tipDateKey = 'daily_tip_date';

  /// Verifica se existe uma dica válida para hoje
  static Future<String?> getTodaysTip() async {
    final prefs = await SharedPreferences.getInstance();
    final tipDate = prefs.getString(_tipDateKey);
    final today = DateTime.now().toIso8601String().split('T')[0]; // YYYY-MM-DD

    // Se a data da dica for hoje, retorna a dica cached
    if (tipDate == today) {
      return prefs.getString(_tipKey);
    }

    // Se não for hoje ou não existir, retorna null
    return null;
  }

  /// Salva a dica do dia com a data atual
  static Future<void> saveTodaysTip(String tip) async {
    final prefs = await SharedPreferences.getInstance();
    final today = DateTime.now().toIso8601String().split('T')[0]; // YYYY-MM-DD

    await prefs.setString(_tipKey, tip);
    await prefs.setString(_tipDateKey, today);
  }

  /// Limpa o cache (útil para testes ou forçar nova dica)
  static Future<void> clearCache() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tipKey);
    await prefs.remove(_tipDateKey);
  }
}
