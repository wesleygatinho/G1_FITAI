import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:collection/collection.dart';
import '../services/api_service.dart';

// --- MODELOS DE DADOS ATUALIZADOS ---

class WeightRecord {
  final DateTime date;
  final double weight;
  WeightRecord({required this.date, required this.weight});
}

class BodyMeasureRecord {
  final DateTime date;
  final String type;
  final double value;
  BodyMeasureRecord(
      {required this.date, required this.type, required this.value});
}

// O modelo CardioRecord agora inclui todos os campos
class CardioRecord {
  final DateTime date;
  final String type;
  final int duration;
  final double distance;
  final int calories;

  CardioRecord({
    required this.date,
    required this.type,
    required this.duration,
    required this.distance,
    required this.calories,
  });
}

class ProgressProvider with ChangeNotifier {
  List<WeightRecord> _weightRecords = [];
  Map<String, List<BodyMeasureRecord>> _groupedBodyMeasureRecords = {};
  Map<String, List<CardioRecord>> _groupedCardioRecords = {};
  bool _isLoading = false;
  final String? authToken;

  List<WeightRecord> get weightRecords => [..._weightRecords];
  Map<String, List<BodyMeasureRecord>> get groupedBodyMeasureRecords =>
      _groupedBodyMeasureRecords;
  Map<String, List<CardioRecord>> get groupedCardioRecords =>
      _groupedCardioRecords;
  bool get isLoading => _isLoading;

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

  Future<void> _fetchWeightRecords() async {
    try {
      final response =
          await ApiService.get('progress/weight', token: authToken);
      if (response.statusCode == 200) {
        final List<dynamic> responseData =
            json.decode(utf8.decode(response.bodyBytes));
        _weightRecords = responseData
            .map((data) => WeightRecord(
                date: DateTime.parse(data['data']),
                weight: data['peso_kg'].toDouble()))
            .toList();
        _weightRecords.sort((a, b) => a.date.compareTo(b.date));
      }
    } catch (e) {/* falha silenciosa */}
  }

  Future<void> _fetchBodyMeasureRecords() async {
    try {
      final response =
          await ApiService.get('progress/measure', token: authToken);
      if (response.statusCode == 200) {
        final List<dynamic> responseData =
            json.decode(utf8.decode(response.bodyBytes));
        final records = responseData
            .map((data) => BodyMeasureRecord(
                date: DateTime.parse(data['data']),
                type: data['tipo_medida'],
                value: data['valor_cm'].toDouble()))
            .toList();
        _groupedBodyMeasureRecords = groupBy(records, (record) => record.type);
      }
    } catch (e) {/* falha silenciosa */}
  }

  Future<void> _fetchCardioRecords() async {
    try {
      final response =
          await ApiService.get('progress/cardio', token: authToken);
      if (response.statusCode == 200) {
        final List<dynamic> responseData =
            json.decode(utf8.decode(response.bodyBytes));
        final records = responseData
            .map((data) => CardioRecord(
                  date: DateTime.parse(data['data']),
                  type: data['tipo_equipamento'] ?? 'N/A',
                  duration: data['tempo_min'],
                  distance: (data['distancia_km'] ?? 0.0).toDouble(),
                  calories: data['calorias'] ?? 0,
                ))
            .toList();
        _groupedCardioRecords = groupBy(records, (record) => record.type);
      }
    } catch (e) {/* falha silenciosa */}
  }

  Future<bool> addWeightRecord(double weight) async {
    final response = await ApiService.post(
        'progress/weight', json.encode({'peso_kg': weight}),
        token: authToken);
    if (response.statusCode == 201) {
      await fetchAllData();
      return true;
    }
    return false;
  }

  Future<bool> addBodyMeasureRecord(String type, double value) async {
    final response = await ApiService.post('progress/measure',
        json.encode({'tipo_medida': type, 'valor_cm': value}),
        token: authToken);
    if (response.statusCode == 201) {
      await fetchAllData();
      return true;
    }
    return false;
  }

  // --- MÉTODO CORRIGIDO AQUI ---
  // Agora usa parâmetros nomeados para evitar erros
  Future<bool> addCardioRecord(
      {required String type,
      required int duration,
      required double distance,
      required int calories}) async {
    final body = {
      'tipo_equipamento': type,
      'tempo_min': duration,
      'distancia_km': distance,
      'calorias': calories,
    };
    final response = await ApiService.post('progress/cardio', json.encode(body),
        token: authToken);
    if (response.statusCode == 201) {
      await fetchAllData();
      return true;
    }
    return false;
  }

  Future<Map<String, dynamic>> extractDataFromImage(
      File imageFile, String dataType) async {
    final bytes = await imageFile.readAsBytes();
    final imageBase64 = base64Encode(bytes);
    final response = await ApiService.post('progress/ocr/extract',
        json.encode({'image_base64': imageBase64, 'data_type': dataType}),
        token: authToken);
    if (response.statusCode == 200) {
      final responseData = json.decode(utf8.decode(response.bodyBytes));
      return responseData['extracted_data'] as Map<String, dynamic>;
    } else {
      throw Exception('Falha ao extrair dados da imagem');
    }
  }
}
