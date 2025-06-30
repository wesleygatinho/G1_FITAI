import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:google_sign_in/google_sign_in.dart';

import 'api_service.dart';

class AuthService with ChangeNotifier {
  String? _token;
  bool _isAuthenticated = false;

  bool get isAuthenticated => _isAuthenticated;
  String? get token => _token;

  // Centraliza a lógica de sucesso de login para ser usada tanto pelo
  // login normal quanto pelo login com Google.
  Future<void> loginSuccess(String token) async {
    _token = token;
    _isAuthenticated = true;

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', token);

    notifyListeners();
  }

  Future<void> register(String nome, String email, String password) async {
    final url = Uri.parse('${ApiService.baseUrl}/auth/register');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'nome': nome,
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode != 201) {
        final errorData = json.decode(response.body);
        throw errorData['detail'] ?? 'Erro desconhecido ao registrar.';
      }
      // Após registrar com sucesso, faz o login para obter o token
      await login(email, password);
    } catch (error) {
      rethrow;
    }
  }

  Future<void> login(String email, String password) async {
    final url = Uri.parse('${ApiService.baseUrl}/auth/login');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {'username': email, 'password': password},
      );

      if (response.statusCode == 200) {
        final responseData = json.decode(response.body);
        // Usa o novo método para lidar com o sucesso
        await loginSuccess(responseData['access_token']);
      } else {
        final errorData = json.decode(response.body);
        throw errorData['detail'] ?? 'Falha no login';
      }
    } catch (error) {
      rethrow;
    }
  }

  Future<void> tryAutoLogin() async {
    final prefs = await SharedPreferences.getInstance();
    if (!prefs.containsKey('token')) {
      return;
    }
    _token = prefs.getString('token');
    _isAuthenticated = true;
    notifyListeners();
  }

  Future<void> logout() async {
    _token = null;
    _isAuthenticated = false;
    await GoogleSignIn().signOut();
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
    notifyListeners();
  }
}