import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

/// Fornece métodos estáticos para realizar requisições HTTP à API do FitAI.
///
/// Esta classe centraliza a configuração da URL base da API e a lógica
/// para montar os cabeçalhos das requisições, incluindo o token de autenticação.
/// Ela suporta alternar facilmente entre um servidor local (para emulador/web)
/// e um servidor remoto via ngrok (para testes em dispositivos físicos).
class ApiService {
  // =======================================================================
  // CONTROLO DO SERVIDOR: Mude apenas esta linha para alternar os modos.
  // =======================================================================

  /// Define como 'true' para usar o ngrok (para testes em telemóvel físico).
  /// Defina como 'false' para usar o IP padrão do emulador Android ou localhost para web.
  static const bool _useNgrok = true;

  // --- CONFIGURAÇÃO DO NGROK ---
  /// Se [_useNgrok] for 'true', cole a sua URL do ngrok aqui.
  static const String _ngrokUrl =
      "https://b210-2804-4a4-ffd6-8800-b011-d627-2d6-74e4.ngrok-free.app/api/v1";

  // --- CONFIGURAÇÃO LOCAL (EMULADOR/WEB) ---
  /// IP especial para o emulador Android aceder ao localhost do computador.
  static const String _localIp = "10.0.2.2";

  /// URL base para desenvolvimento local, que varia se a app está a correr na web ou não.
  static const String _localBaseUrl =
      kIsWeb ? 'http://localhost:8000/api/v1' : 'http://$_localIp:8000/api/v1';

  // --- URL BASE FINAL ---
  /// A URL base final que será usada para todas as requisições.
  /// Esta linha escolhe automaticamente a URL correta com base na sua escolha em [_useNgrok].
  static const String baseUrl = _useNgrok ? _ngrokUrl : _localBaseUrl;
  // =======================================================================

  /// Prepara os cabeçalhos para a requisição, incluindo o token se disponível.
  ///
  /// Busca o token de acesso no [SharedPreferences] e o adiciona ao
  /// cabeçalho 'Authorization'. Também define o 'Content-Type' apropriado.
  ///
  /// O parâmetro [isUrlEncoded] deve ser `true` para requisições
  /// do tipo 'application/x-www-form-urlencoded', como no login.
  static Future<Map<String, String>> getHeaders(
      {String? token, bool isUrlEncoded = false}) async {
    final prefs = await SharedPreferences.getInstance();
    // Usa o token fornecido, ou tenta obter um que esteja guardado.
    final finalToken = token ?? prefs.getString('token');

    final headers = {
      'Content-Type': isUrlEncoded
          ? 'application/x-www-form-urlencoded'
          : 'application/json; charset=UTF-8',
    };

    if (finalToken != null) {
      headers['Authorization'] = 'Bearer $finalToken';
    }
    return headers;
  }

  /// Realiza uma requisição GET para um endpoint específico da API.
  ///
  /// Opcionalmente, pode receber um [token] para aceder a endpoints protegidos.
  static Future<http.Response> get(String endpoint, {String? token}) async {
    final url = Uri.parse('$baseUrl/$endpoint');
    final headers = await getHeaders(token: token);
    return await http.get(url, headers: headers);
  }

  /// Realiza uma requisição POST com um corpo JSON para um endpoint da API.
  static Future<http.Response> post(String endpoint, String body,
      {String? token}) async {
    final url = Uri.parse('$baseUrl/$endpoint');
    final headers = await getHeaders(token: token);
    return await http.post(url, headers: headers, body: body);
  }

  /// Realiza uma requisição POST com o corpo codificado para formulários.
  ///
  /// Usado especificamente para endpoints que esperam dados no formato
  /// 'application/x-www-form-urlencoded', como o de login.
  static Future<http.Response> postUrlEncoded(
      String endpoint, Map<String, String> body) async {
    final url = Uri.parse('$baseUrl/$endpoint');
    final headers = await getHeaders(isUrlEncoded: true);
    return await http.post(url, headers: headers, body: body);
  }

  /// Realiza uma requisição PUT com um corpo JSON para um endpoint da API.
  static Future<http.Response> put(String endpoint, String body,
      {String? token}) async {
    final url = Uri.parse('$baseUrl/$endpoint');
    final headers = await getHeaders(token: token);
    return await http.put(url, headers: headers, body: body);
  }
}
