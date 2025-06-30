import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  /* UTILIZE ESTE SERVIÇO PARA REALIZAR AS REQUISIÇÕES HTTP PARA O BACKEND

  // Se estiver a testar no emulador, pode usar 'localhost'  
  // Substitua "SEU_IP_AQUI" pelo IP da sua máquina se estiver a testar num dispositivo físico.
  
  static const String _localIp = "192.168.100.160";

  static const String baseUrl =
      kIsWeb ? 'http://localhost:8000/api/v1' : 'http://$_localIp:8000/api/v1';

  */

  // Se estiver a usar o ngrok, substitua a URL abaixo pela URL gerada pelo ngrok.
  // Exemplo: static const String baseUrl = 'https://seu_ngrok_url

  // Substitua pela URL gerada pelo ngrok
  static const String baseUrl =
      "https://73cc-2804-d4b-7737-c100-b8ee-3266-6d58-514a.ngrok-free.app/api/v1";

  /// Prepara os headers para a requisição, incluindo o token se disponível.
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

  /// Realiza uma requisição GET, agora aceitando um token para endpoints protegidos.
  static Future<http.Response> get(String endpoint, {String? token}) async {
    final url = Uri.parse('$baseUrl/$endpoint');
    final headers = await getHeaders(token: token);
    return await http.get(url, headers: headers);
  }

  // --- Outros métodos (post, put, etc.) ---
  static Future<http.Response> post(String endpoint, String body,
      {String? token}) async {
    final url = Uri.parse('$baseUrl/$endpoint');
    final headers = await getHeaders(token: token);
    return await http.post(url, headers: headers, body: body);
  }

  static Future<http.Response> postUrlEncoded(
      String endpoint, Map<String, String> body) async {
    final url = Uri.parse('$baseUrl/$endpoint');
    final headers = await getHeaders(isUrlEncoded: true);
    return await http.post(url, headers: headers, body: body);
  }

  static Future<http.Response> put(String endpoint, String body,
      {String? token}) async {
    final url = Uri.parse('$baseUrl/$endpoint');
    final headers = await getHeaders(token: token);
    return await http.put(url, headers: headers, body: body);
  }
}
