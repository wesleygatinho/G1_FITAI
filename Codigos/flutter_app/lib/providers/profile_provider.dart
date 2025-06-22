import 'dart:convert';
import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';

class ProfileProvider with ChangeNotifier {
  User? _user;
  bool _isLoading = true;
  String? _error;

  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;

  ProfileProvider() {
    fetchUserProfile();
  }

  Future<void> fetchUserProfile() async {
    _isLoading = true;
    notifyListeners();
    try {
      final response = await ApiService.get('users/me');
      if (response.statusCode == 200) {
        _user = User.fromJson(json.decode(utf8.decode(response.bodyBytes)));
        _error = null;
      } else {
        _error = "Falha ao carregar o perfil.";
      }
    } catch (e) {
      _error = "Erro de conexão.";
    }
    _isLoading = false;
    notifyListeners();
  }

  // --- NOVA FUNÇÃO PARA ATUALIZAR O PERFIL ---
  Future<bool> updateUserProfile(Map<String, dynamic> dataToUpdate) async {
    try {
      final response = await ApiService.put(
        'users/me',
        json.encode(dataToUpdate),
      );

      if (response.statusCode == 200) {
        // Atualiza os dados locais do utilizador com a resposta da API
        _user = User.fromJson(json.decode(utf8.decode(response.bodyBytes)));
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}
