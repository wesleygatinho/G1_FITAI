import 'dart:convert';
import 'package:collection/collection.dart'; // CAMINHO CORRIGIDO
import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart'; // IMPORTAÇÃO ADICIONADA
import '../services/api_service.dart';
import '../models/workout_model.dart';

class WorkoutHistoryProvider with ChangeNotifier {
  List<SessaoDeTreino> _history = [];
  bool _isLoading = false;
  String? _error;
  final String? authToken;

  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;
  late Map<DateTime, List<SessaoDeTreino>> _events;

  List<SessaoDeTreino> get history => [..._history];
  bool get isLoading => _isLoading;
  String? get error => _error;
  DateTime get focusedDay => _focusedDay;
  DateTime? get selectedDay => _selectedDay;

  WorkoutHistoryProvider(this.authToken) {
    _selectedDay = _focusedDay;
    _events = {};
    if (authToken != null && authToken!.isNotEmpty) {
      fetchHistory();
    } else {
      _isLoading = false;
      _error = "Utilizador não autenticado.";
    }
  }

  List<SessaoDeTreino> getEventsForDay(DateTime day) {
    final dateOnly = DateTime.utc(day.year, day.month, day.day);
    return _events[dateOnly] ?? [];
  }

  List<SessaoDeTreino> get workoutsForSelectedDay {
    return getEventsForDay(_selectedDay ?? _focusedDay);
  }

  void onDaySelected(DateTime selectedDay, DateTime focusedDay) {
    // A função isSameDay agora é reconhecida por causa da nova importação
    if (!isSameDay(_selectedDay, selectedDay)) {
      _selectedDay = selectedDay;
      _focusedDay = focusedDay;
      notifyListeners();
    }
  }

  Future<void> fetchHistory() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiService.get('sessions/', token: authToken);
      if (response.statusCode == 200) {
        final List<dynamic> responseData =
            json.decode(utf8.decode(response.bodyBytes));
        _history =
            responseData.map((data) => SessaoDeTreino.fromJson(data)).toList();

        // A função groupBy agora é reconhecida por causa da importação correta
        _events = groupBy(
            _history,
            (sessao) => DateTime.utc(sessao.dataInicio.year,
                sessao.dataInicio.month, sessao.dataInicio.day));
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
