import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../../providers/ai_provider.dart';

class AiGeneratorScreen extends StatelessWidget {
  const AiGeneratorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (ctx) => AiProvider(),
      child: Scaffold(
        appBar: AppBar(title: const Text('Assistente de IA')),
        body: RefreshIndicator(
          onRefresh: () =>
              Provider.of<AiProvider>(context, listen: false).fetchHistory(),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildDailyTipCard(),
                const SizedBox(height: 24),
                _buildPlanGeneratorCard(),
                const SizedBox(height: 24),
                const Divider(),
                const SizedBox(height: 16),
                Text(
                  'Histórico de Interações',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 16),
                _buildHistoryList(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// ignore: camel_case_types
class _buildDailyTipCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Dica Fitness do Dia',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            Consumer<AiProvider>(
              builder: (ctx, aiData, _) {
                if (aiData.isLoadingTip) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (aiData.dailyTip != null) {
                  return Text(
                    aiData.dailyTip!,
                    style: Theme.of(context).textTheme.bodyLarge,
                  );
                }
                return const SizedBox.shrink();
              },
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              icon: const Icon(Icons.lightbulb_outline),
              label: const Text('Obter Nova Dica'),
              onPressed: () {
                Provider.of<AiProvider>(
                  context,
                  listen: false,
                ).forceNewDailyTip();
              },
            ),
          ],
        ),
      ),
    );
  }
}

// ignore: camel_case_types
class _buildPlanGeneratorCard extends StatefulWidget {
  @override
  State<_buildPlanGeneratorCard> createState() =>
      _buildPlanGeneratorCardState();
}

// ignore: camel_case_types
class _buildPlanGeneratorCardState extends State<_buildPlanGeneratorCard> {
  final _promptController = TextEditingController();

  @override
  void dispose() {
    _promptController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_promptController.text.trim().isEmpty) return;
    Provider.of<AiProvider>(
      context,
      listen: false,
    ).generatePlan(_promptController.text);
  }

  @override
  Widget build(BuildContext context) {
    final aiProvider = Provider.of<AiProvider>(context);
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Gerador de Plano Personalizado',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _promptController,
              decoration: const InputDecoration(
                labelText: 'Descreva o seu objetivo...',
                hintText: 'Ex: "Um treino de 3 dias para hipertrofia"',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              icon: const Icon(Icons.auto_awesome),
              label: const Text('Gerar Plano'),
              onPressed: aiProvider.isLoadingPlan ? null : _submit,
            ),
            const SizedBox(height: 24),
            if (aiProvider.isLoadingPlan)
              const Center(child: CircularProgressIndicator())
            else if (aiProvider.generatedPlan != null)
              Container(
                padding: const EdgeInsets.all(12),
                // ignore: deprecated_member_use
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  aiProvider.generatedPlan!,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
          ],
        ),
      ),
    );
  }
}

// --- NOVO WIDGET PARA EXIBIR O HISTÓRICO ---
// ignore: camel_case_types
class _buildHistoryList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<AiProvider>(
      builder: (ctx, aiData, _) {
        if (aiData.isLoadingHistory) {
          return const Center(child: CircularProgressIndicator());
        }
        if (aiData.history.isEmpty) {
          return const Center(child: Text('Nenhuma interação guardada ainda.'));
        }
        return ListView.builder(
          shrinkWrap:
              true, // Para que a ListView funcione dentro de uma SingleChildScrollView
          physics:
              const NeverScrollableScrollPhysics(), // Desativa o scroll da ListView
          itemCount: aiData.history.length,
          itemBuilder: (ctx, index) {
            final interaction = aiData.history[index];
            return Card(
              margin: const EdgeInsets.symmetric(vertical: 6),
              child: ExpansionTile(
                leading: const Icon(Icons.history),
                title: Text(
                  'Interação de ${DateFormat('dd/MM/yyyy').format(interaction.data)}',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                subtitle: Text(
                  interaction.promptUsuario,
                  overflow: TextOverflow.ellipsis,
                ),
                children: [
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'O seu pedido:',
                          style: Theme.of(context).textTheme.titleSmall,
                        ),
                        Text(interaction.promptUsuario),
                        const Divider(height: 24),
                        Text(
                          'Resposta da IA:',
                          style: Theme.of(context).textTheme.titleSmall,
                        ),
                        Text(interaction.respostaIa),
                      ],
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}
