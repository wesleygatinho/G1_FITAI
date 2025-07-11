import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:google_sign_in/google_sign_in.dart';

import 'api_service.dart';

/// Gerencia o estado de autenticação do utilizador em toda a aplicação.
///
/// Esta classe usa o padrão [ChangeNotifier] para notificar os widgets
/// sobre mudanças no estado de autenticação (ex: login, logout).
/// Ela lida com o registo, login com e-mail/senha, auto-login e logout.
class AuthService with ChangeNotifier {
  String? _token;
  bool _isAuthenticated = false;
  bool _isLoading = true; // NOVO: controla o estado de carregamento inicial

  /// Retorna `true` se o utilizador estiver autenticado.
  bool get isAuthenticated => _isAuthenticated;

  /// Retorna o token de acesso do utilizador, ou `null` se não estiver autenticado.
  String? get token => _token;

  /// NOVO: Retorna `true` se ainda estiver verificando a autenticação inicial.
  bool get isLoading => _isLoading;

  /// NOVO: Construtor que automaticamente verifica a autenticação ao criar o serviço.
  AuthService() {
    _checkInitialAuth();
  }

  /// NOVO: Verifica se o utilizador já está autenticado ao iniciar a aplicação.
  Future<void> _checkInitialAuth() async {
    await tryAutoLogin();
    _isLoading = false;
    notifyListeners();
  }

  /// Atualiza o estado da aplicação após um login bem-sucedido.
  ///
  /// Armazena o [token] no [SharedPreferences] para persistência e
  /// notifica os listeners sobre a mudança no estado de autenticação.
  Future<void> loginSuccess(String token) async {
    _token = token;
    _isAuthenticated = true;

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', token);

    notifyListeners();
  }

  /// Regista um novo utilizador e, em caso de sucesso, realiza o login automaticamente.
  ///
  /// Lança uma [Exception] com a mensagem de erro da API se o registo falhar.
  Future<void> register(String nome, String email, String password) async {
    final url = Uri.parse('${ApiService.baseUrl}/auth/register');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'nome': nome, 'email': email, 'password': password}),
      );

      if (response.statusCode != 201) {
        final errorData = json.decode(response.body);
        throw errorData['detail'] ?? 'Erro desconhecido ao registrar.';
      }
      // Após registrar com sucesso, faz o login para obter o token.
      await login(email, password);
    } catch (error) {
      rethrow;
    }
  }

  /// Autentica um utilizador com e-mail e senha.
  ///
  /// Em caso de sucesso, chama [loginSuccess] para atualizar o estado da aplicação.
  /// Lança uma [Exception] com a mensagem de erro da API se o login falhar.
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
        // Usa o método centralizado para lidar com o sucesso.
        await loginSuccess(responseData['access_token']);
      } else {
        final errorData = json.decode(response.body);
        throw errorData['detail'] ?? 'Falha no login';
      }
    } catch (error) {
      rethrow;
    }
  }

  /// Tenta realizar o login automático do utilizador ao iniciar a aplicação.
  ///
  /// Verifica se um token está guardado no [SharedPreferences] e, se estiver,
  /// atualiza o estado de autenticação sem precisar de uma nova requisição à API.
  Future<void> tryAutoLogin() async {
    final prefs = await SharedPreferences.getInstance();
    if (!prefs.containsKey('token')) {
      return;
    }
    _token = prefs.getString('token');
    _isAuthenticated = true;
    notifyListeners();
  }

  /// Realiza o logout do utilizador.
  ///
  /// Limpa o estado de autenticação, faz logout do Google Sign-In,
  /// remove o token do [SharedPreferences] e notifica os listeners.
  Future<void> logout() async {
    _token = null;
    _isAuthenticated = false;
    await GoogleSignIn().signOut();
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
    notifyListeners();
  }
}
