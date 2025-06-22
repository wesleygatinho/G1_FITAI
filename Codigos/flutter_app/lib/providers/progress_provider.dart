import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:collection/collection.dart'; // Importar o pacote 'collection'
import '../services/api_service.dart';

// Modelos de dados
class WeightRecord {
  final DateTime date;
  final double weight;
  WeightRecord({required this.date, required this.weight});
}

class BodyMeasureRecord {
  final DateTime date;
  final String type;
  final double value;
  BodyMeasureRecord({required this.date, required this.type, required this.value});
}

class CardioRecord {
  final DateTime date;
  final String type;
  final int duration;
  CardioRecord({required this.date, required this.type, required this.duration});
}

class ProgressProvider with ChangeNotifier {
  List<WeightRecord> _weightRecords = [];
  Map<String, List<BodyMeasureRecord>> _groupedBodyMeasureRecords = {};
  Map<String, List<CardioRecord>> _groupedCardioRecords = {};
  bool _isLoading = false;
  final String? authToken; // Propriedade para guardar o token

  // Getters
  List<WeightRecord> get weightRecords => [..._weightRecords];
  Map<String, List<BodyMeasureRecord>> get groupedBodyMeasureRecords => _groupedBodyMeasureRecords;
  Map<String, List<CardioRecord>> get groupedCardioRecords => _groupedCardioRecords;
  bool get isLoading => _isLoading;

  // O construtor agora requer o token de autenticação
  ProgressProvider(this.authToken) {
    if (authToken != null && authToken!.isNotEmpty) {
      fetchAllData();
    } else {
      _isLoading = false;
    }
  }
  
  Future<void> fetchAllData() async {
    _isLoading = true;
    notifyListeners();
    await Future.wait([
      _fetchWeightRecords(),
      _fetchBodyMeasureRecords(),
      _fetchCardioRecords(),
    ]);
    _isLoading = false;
    notifyListeners();
  }

  // --- Funções de busca de dados com autenticação ---

  Future<void> _fetchWeightRecords() async {
    try {
      final response = await ApiService.get('progress/weight', token: authToken); // Passa o token
      if (response.statusCode == 200) {
        final List<dynamic> responseData = json.decode(utf8.decode(response.bodyBytes));
        _weightRecords = responseData.map((data) => WeightRecord(date: DateTime.parse(data['data']), weight: data['peso_kg'])).toList();
        _weightRecords.sort((a, b) => a.date.compareTo(b.date));
      }
    } catch (e) { /* falha silenciosa */ }
  }
  
  Future<void> _fetchBodyMeasureRecords() async {
    try {
      final response = await ApiService.get('progress/measure', token: authToken); // Passa o token
      if (response.statusCode == 200) {
        final List<dynamic> responseData = json.decode(utf8.decode(response.bodyBytes));
        final records = responseData.map((data) => BodyMeasureRecord(date: DateTime.parse(data['data']), type: data['tipo_medida'], value: data['valor_cm'])).toList();
        _groupedBodyMeasureRecords = groupBy(records, (record) => record.type);
      }
    } catch (e) { /* falha silenciosa */ }
  }

  Future<void> _fetchCardioRecords() async {
    try {
      final response = await ApiService.get('progress/cardio', token: authToken); // Passa o token
      if (response.statusCode == 200) {
        final List<dynamic> responseData = json.decode(utf8.decode(response.bodyBytes));
        final records = responseData.map((data) => CardioRecord(date: DateTime.parse(data['data']), type: data['tipo_equipamento'], duration: data['tempo_min'])).toList();
        _groupedCardioRecords = groupBy(records, (record) => record.type);
      }
    } catch (e) { /* falha silenciosa */ }
  }

  // --- Funções para adicionar registos com autenticação ---

  Future<bool> addWeightRecord(double weight) async {
    final response = await ApiService.post('progress/weight', json.encode({'peso_kg': weight}), token: authToken);
    if (response.statusCode == 201) {
      await fetchAllData();
      return true;
    }
    return false;
  }
  
  Future<bool> addBodyMeasureRecord(String type, double value) async {
    final response = await ApiService.post('progress/measure', json.encode({'tipo_medida': type, 'valor_cm': value}), token: authToken);
    if (response.statusCode == 201) {
      await fetchAllData();
      return true;
    }
    return false;
  }
  
  Future<bool> addCardioRecord(String type, int duration) async {
    final response = await ApiService.post('progress/cardio', json.encode({'tipo_equipamento': type, 'tempo_min': duration}), token: authToken);
    if (response.statusCode == 201) {
      await fetchAllData();
      return true;
    }
    return false;
  }
}
