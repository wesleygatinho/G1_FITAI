import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/auth_service.dart';
import 'screens/auth/login_screen.dart';
import 'screens/home_screen.dart';

/// Ponto de entrada principal da aplicação Flutter.
void main() {
  runApp(const MyApp());
}

/// O widget raiz da aplicação FitAI.
///
/// Este widget configura o [ChangeNotifierProvider] para o [AuthService],
/// define o tema global da aplicação e decide qual tela mostrar com base
/// no estado de autenticação do utilizador.
class MyApp extends StatelessWidget {
  /// Cria o widget da aplicação.
  const MyApp({super.key});

  /// Constrói a interface do widget.
  ///
  /// Utiliza um [Consumer] para ouvir as mudanças no [AuthService] e
  /// reconstruir a árvore de widgets quando o estado de autenticação muda.
  ///
  /// Retorna um [MaterialApp] com o tema e a rota inicial definidos.
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (ctx) => AuthService(),
      child: Consumer<AuthService>(
        builder: (ctx, auth, _) => MaterialApp(
          title: 'FitAI',

          // --- TEMA ATUALIZADO ---
          // Tema claro (branco) com laranja como cor principal.
          theme: ThemeData(
            // Define o brilho geral da aplicação para claro (fundo branco).
            brightness: Brightness.light,

            // Define a paleta de cores principal a partir de uma cor base.
            // O Flutter irá gerar tons mais claros e mais escuros a partir daqui.
            primarySwatch: Colors.orange,

            // Define o esquema de cores de forma mais detalhada.
            colorScheme: ColorScheme.fromSwatch(
              primarySwatch: Colors.orange,
              brightness: Brightness.light,
            ).copyWith(
              // A cor 'secondary' é usada para elementos de destaque, como o FloatingActionButton.
              secondary: Colors.deepOrangeAccent,
            ),

            // Estilo para os botões principais.
            elevatedButtonTheme: ElevatedButtonThemeData(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.orange, // Fundo do botão
                foregroundColor: Colors.white, // Cor do texto do botão
              ),
            ),

            // Estilo para os campos de texto.
            inputDecorationTheme: const InputDecorationTheme(
              border: OutlineInputBorder(
                borderRadius: BorderRadius.all(Radius.circular(8.0)),
              ),
            ),

            // Define a densidade visual para se adaptar a diferentes plataformas.
            visualDensity: VisualDensity.adaptivePlatformDensity,
          ),

          // Decide a tela inicial com base no estado de autenticação.
          // Se o utilizador estiver autenticado, mostra a [HomeScreen],
          // caso contrário, mostra a [LoginScreen].
          home: auth.isAuthenticated ? const HomeScreen() : const LoginScreen(),
          debugShowCheckedModeBanner: false,
        ),
      ),
    );
  }
}
