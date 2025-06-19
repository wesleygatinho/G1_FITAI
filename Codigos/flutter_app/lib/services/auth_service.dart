import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';

class AuthService extends ChangeNotifier {
  bool _isAuthenticated = false;
  String? _token;

  bool get isAuthenticated => _isAuthenticated;
  String? get token => _token;

  AuthService() {
    _tryAutoLogin();
  }

  Future<void> _tryAutoLogin() async {
    final prefs = await SharedPreferences.getInstance();
    if (prefs.containsKey('token')) {
      _token = prefs.getString('token');
      _isAuthenticated = true;
      notifyListeners();
    }
  }

  // --- CORREÇÃO: O método login agora usa o ApiService ---
  Future<bool> login(String email, String password) async {
    // A API espera 'username' e 'password' para o login via formulário
    final response = await ApiService.postUrlEncoded('auth/login', {
      'username': email,
      'password': password,
    });

    if (response.statusCode == 200) {
      final responseData = json.decode(response.body);
      _token = responseData['access_token'];
      _isAuthenticated = true;

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', _token!);

      notifyListeners();
      return true;
    }
    return false;
  }

  Future<bool> register(String email, String password, String nome) async {
    final response = await ApiService.post(
        'auth/register',
        json.encode({
          'email': email,
          'password': password,
          'nome': nome,
        }));

    if (response.statusCode == 201) {
      return await login(email, password);
    }
    return false;
  }

  Future<void> logout() async {
    _token = null;
    _isAuthenticated = false;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');

    notifyListeners();
  }
}
