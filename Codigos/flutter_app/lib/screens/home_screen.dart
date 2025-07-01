import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/dashboard_provider.dart';
import '../services/auth_service.dart';
import 'exercise/exercise_list_screen.dart';
import 'progress/progress_dashboard_screen.dart';
import 'ai/ai_generator_screen.dart';
import 'history/workout_history_screen.dart';
import 'auth/login_screen.dart';

/// A tela principal da aplicação, exibida após o login do utilizador.
///
/// Esta tela serve como um painel de navegação, fornecendo acesso rápido
/// às principais funcionalidades do FitAI, como iniciar um treino, ver o progresso,
/// consultar o histórico e interagir com a IA.
class HomeScreen extends StatelessWidget {
  /// Cria a instância da tela inicial.
  const HomeScreen({super.key});

  /// Constrói a interface do widget da tela inicial.
  ///
  /// Utiliza um [ChangeNotifierProvider] para o [DashboardProvider] que busca
  /// a dica do dia. Mostra um indicador de progresso enquanto os dados
  /// estão a ser carregados.
  @override
  Widget build(BuildContext context) {
    // Obtemos o token do nosso AuthService para passar para as telas que precisam.
    final token = Provider.of<AuthService>(context, listen: false).token;

    return ChangeNotifierProvider(
      create: (ctx) => DashboardProvider(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('FitAI Início'),
          actions: [
            IconButton(
              icon: const Icon(Icons.logout),
              tooltip: 'Sair',
              onPressed: () async {
                await Provider.of<AuthService>(context, listen: false).logout();

                // Navega para a tela de login e remove todas as rotas anteriores.
                if (context.mounted) {
                  Navigator.of(context).pushAndRemoveUntil(
                    MaterialPageRoute(
                        builder: (context) => const LoginScreen()),
                    (Route<dynamic> route) => false,
                  );
                }
              },
            ),
          ],
        ),
        body: Consumer<DashboardProvider>(
          builder: (ctx, dashboard, _) => dashboard.isLoading
              ? const Center(child: CircularProgressIndicator())
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      _buildWelcomeHeader(),
                      const SizedBox(height: 24),
                      _buildDailyTipCard(dashboard.dailyTip),
                      const SizedBox(height: 24),
                      _buildNavButton(context,
                          icon: Icons.play_circle_fill,
                          label: 'INICIAR TREINO',
                          screen: const ExerciseListScreen()),
                      const SizedBox(height: 16),
                      _buildNavButton(context,
                          icon: Icons.bar_chart,
                          label: 'VER PROGRESSO',
                          screen: ProgressDashboardScreen(token: token!),
                          isOutlined: true),
                      const SizedBox(height: 16),
                      _buildNavButton(context,
                          icon: Icons.history,
                          label: 'HISTÓRICO DE TREINOS',
                          screen: const WorkoutHistoryScreen(),
                          isOutlined: true),
                      const SizedBox(height: 16),
                      _buildNavButton(context,
                          icon: Icons.auto_awesome,
                          label: 'MAIS DICAS (IA)',
                          screen: const AiGeneratorScreen(),
                          isOutlined: true),
                    ],
                  ),
                ),
        ),
      ),
    );
  }

  /// Constrói o cabeçalho de boas-vindas da tela.
  Widget _buildWelcomeHeader() {
    return const Column(
      children: [
        Icon(Icons.home, size: 60, color: Colors.amber), // Ícone de casinha
        SizedBox(height: 8),
        Text(
          'Bem-vindo!',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }

  /// Constrói o card que exibe a dica do dia.
  ///
  /// Recebe a [tip] do [DashboardProvider] e a exibe dentro de um [Card] estilizado.
  Widget _buildDailyTipCard(String? tip) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Dica do Dia',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(tip ?? 'Carregando dica...'),
          ],
        ),
      ),
    );
  }

  /// Constrói um botão de navegação estilizado.
  ///
  /// Pode ser um [ElevatedButton] (padrão) ou um [OutlinedButton] se
  /// [isOutlined] for `true`. Ao ser pressionado, navega para a [screen] fornecida.
  Widget _buildNavButton(BuildContext context,
      {required IconData icon,
      required String label,
      required Widget screen,
      bool isOutlined = false}) {
    final Color orangeColor = Theme.of(context).colorScheme.primary;

    final style = isOutlined
        ? OutlinedButton.styleFrom(
            foregroundColor: orangeColor,
            side: BorderSide(color: orangeColor, width: 2),
            padding: const EdgeInsets.symmetric(vertical: 16),
            textStyle:
                const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          )
        : ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 16),
            textStyle:
                const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          );

    return isOutlined
        ? OutlinedButton.icon(
            icon: Icon(icon),
            label: Text(label),
            style: style,
            onPressed: () {
              Navigator.of(context)
                  .push(MaterialPageRoute(builder: (context) => screen));
            },
          )
        : ElevatedButton.icon(
            icon: Icon(icon),
            label: Text(label),
            style: style,
            onPressed: () {
              Navigator.of(context)
                  .push(MaterialPageRoute(builder: (context) => screen));
            },
          );
  }
}
