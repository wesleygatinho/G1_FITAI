import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:convert';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;

import '../../services/auth_service.dart';
import '../../services/api_service.dart';
import '../../widgets/custom_text_field.dart';
import '../home_screen.dart';


class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  var _isLoginMode = true;
  var _isLoading = false;

  String _email = '';
  String _password = '';
  String _nome = '';

  void _showErrorDialog(String message) {
    if (!mounted) return;
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Ocorreu um Erro'),
        content: Text(message),
        actions: <Widget>[
          TextButton(
            child: const Text('Ok'),
            onPressed: () {
              Navigator.of(ctx).pop();
            },
          )
        ],
      ),
    );
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }
    _formKey.currentState!.save();
    setState(() {
      _isLoading = true;
    });

    final authService = Provider.of<AuthService>(context, listen: false);

    try {
      if (_isLoginMode) {
        await authService.login(_email, _password);
      } else {
        await authService.register(_nome, _email, _password);
      }
      if (mounted) {
        Navigator.of(context).pushReplacement(
            MaterialPageRoute(builder: (context) => const HomeScreen()));
      }
    } catch (error) {
      _showErrorDialog(error.toString());
    }

    if (mounted) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _googleSignIn() async {
    setState(() => _isLoading = true);

    try {
      const String webClientId = "494510060624-r7fuq8tbpu75qfekjvrr84suee676it9.apps.googleusercontent.com";

      final GoogleSignIn googleSignIn = GoogleSignIn(
        serverClientId: webClientId,
      );

      final GoogleSignInAccount? googleUser = await googleSignIn.signIn();

      if (googleUser == null) {
        if (mounted) setState(() => _isLoading = false);
        return;
      }

      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      final String? idToken = googleAuth.idToken;

      if (idToken == null) {
        throw 'Não foi possível obter o token do Google. Verifique a configuração.';
      }

      final response = await http.post(
        Uri.parse('${ApiService.baseUrl}/auth/google/token'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'token': idToken}),
      );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        final authService = Provider.of<AuthService>(context, listen: false);
        await authService.loginSuccess(responseData['access_token']);
        
        if (mounted) {
            Navigator.of(context).pushReplacement(
                MaterialPageRoute(builder: (context) => const HomeScreen()));
        }

      } else {
        final errorData = jsonDecode(response.body);
        throw errorData['detail'] ?? 'Erro ao autenticar com o servidor.';
      }
    } catch (error) {
      _showErrorDialog(error.toString());
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Usando um ícone padrão para evitar erros de asset
                  Icon(Icons.fitness_center, size: 80, color: Theme.of(context).colorScheme.primary),
                  const SizedBox(height: 16),
                  Text(
                    _isLoginMode ? 'Bem-vindo de volta!' : 'Crie sua conta',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  const SizedBox(height: 24),
                  if (!_isLoginMode)
                    CustomTextField(
                      label: 'Nome completo',
                      icon: Icons.person,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Por favor, insira seu nome.';
                        }
                        return null;
                      },
                      onSaved: (value) => _nome = value!,
                    ),
                  if (!_isLoginMode) const SizedBox(height: 16),
                  CustomTextField(
                    label: 'E-mail',
                    icon: Icons.email,
                    keyboardType: TextInputType.emailAddress,
                    validator: (value) {
                      if (value == null || !value.contains('@')) {
                        return 'Por favor, insira um e-mail válido.';
                      }
                      return null;
                    },
                    onSaved: (value) => _email = value!,
                  ),
                  const SizedBox(height: 16),
                  CustomTextField(
                    label: 'Senha',
                    icon: Icons.lock,
                    obscureText: true,
                    validator: (value) {
                      if (value == null || value.length < 6) {
                        return 'A senha deve ter pelo menos 6 caracteres.';
                      }
                      return null;
                    },
                    onSaved: (value) => _password = value!,
                  ),
                  const SizedBox(height: 24),
                  if (_isLoading)
                    const Center(child: CircularProgressIndicator())
                  else
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        ElevatedButton(
                          onPressed: _submit,
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                          child: Text(_isLoginMode ? 'LOGIN' : 'REGISTRAR'),
                        ),
                        const SizedBox(height: 12),
                        ElevatedButton.icon(
                          icon: Image.asset(
                            'assets/images/google_logo.png',
                            height: 22.0, // Ajuste a altura conforme necessário
                            width: 22.0,
                          ),
                          label: const Text('Entrar com Google'),
                          onPressed: _googleSignIn,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.white,
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(vertical: 12),
                            textStyle: const TextStyle(fontSize: 16),
                          ),
                        ),
                      ],
                    ),
                  TextButton(
                    onPressed: () {
                      if (_isLoading) return;
                      setState(() {
                        _isLoginMode = !_isLoginMode;
                      });
                    },
                    child: Text(
                        _isLoginMode ? 'Criar nova conta' : 'Já tenho uma conta'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}