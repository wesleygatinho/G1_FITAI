import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/dashboard_provider.dart';
import '../services/auth_service.dart';
import 'exercise/exercise_list_screen.dart';
import 'progress/progress_dashboard_screen.dart';
import 'ai/ai_generator_screen.dart';
import 'history/workout_history_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Envolvemos a tela com o novo provider para o painel
    return ChangeNotifierProvider(
      create: (ctx) => DashboardProvider(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('FitAI Início'),
          actions: [
            IconButton(
              icon: const Icon(Icons.logout),
              tooltip: 'Sair',
              onPressed: () {
                Provider.of<AuthService>(context, listen: false).logout();
              },
            ),
          ],
        ),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildWelcomeHeader(),
              const SizedBox(height: 24),
              _buildDailyTipCard(),
              const SizedBox(height: 24),
              _buildNavButton(context,
                  icon: Icons.play_circle_fill,
                  label: 'INICIAR TREINO',
                  screen: const ExerciseListScreen()),
              const SizedBox(height: 16),
              _buildNavButton(context,
                  icon: Icons.bar_chart,
                  label: 'VER PROGRESSO',
                  screen: const ProgressDashboardScreen(),
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
    );
  }

  Widget _buildWelcomeHeader() {
    return const Column(
      children: [
        Icon(Icons.home, size: 60, color: Colors.amber),
        SizedBox(height: 8),
        Text(
          'Bem-vindo!',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }

  Widget _buildDailyTipCard() {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Consumer<DashboardProvider>(
          builder: (ctx, dashboardData, _) {
            if (dashboardData.isLoading) {
              return const Center(child: CircularProgressIndicator());
            }
            if (dashboardData.error != null) {
              return Text(dashboardData.error!,
                  style: const TextStyle(color: Colors.red));
            }
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.lightbulb_outline, color: Colors.amber),
                    SizedBox(width: 8),
                    Text('Dica do Dia',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold)),
                  ],
                ),
                const SizedBox(height: 12),
                Text(
                  dashboardData.dailyTip ?? 'Não foi possível carregar a dica.',
                  style: const TextStyle(fontSize: 16, height: 1.5),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildNavButton(BuildContext context,
      {required IconData icon,
      required String label,
      required Widget screen,
      bool isOutlined = false}) {
    final baseStyle = ButtonStyle(
      padding:
          MaterialStateProperty.all(const EdgeInsets.symmetric(vertical: 16)),
      textStyle: MaterialStateProperty.all(const TextStyle(fontSize: 18)),
    );

    final button = isOutlined
        ? OutlinedButton.icon(
            icon: Icon(icon),
            label: Text(label),
            style: OutlinedButton.styleFrom(
              side: BorderSide(color: Theme.of(context).colorScheme.secondary),
            ).merge(baseStyle),
            onPressed: () => Navigator.of(context)
                .push(MaterialPageRoute(builder: (_) => screen)),
          )
        : ElevatedButton.icon(
            icon: Icon(icon),
            label: Text(label),
            style: baseStyle,
            onPressed: () => Navigator.of(context)
                .push(MaterialPageRoute(builder: (_) => screen)),
          );

    return button;
  }
}
