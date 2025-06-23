import 'package:flutter/material.dart';
import 'package:flutter_app/providers/profile_provider.dart';
import 'package:provider/provider.dart';
import 'edit_profile_screen.dart'; // Importar a nova tela

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (ctx) => ProfileProvider(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('O Meu Perfil'),
          // BOTÃO DE EDIÇÃO
          actions: [
            Consumer<ProfileProvider>(
              builder: (ctx, profileData, _) => IconButton(
                icon: const Icon(Icons.edit),
                onPressed: profileData.user == null
                    ? null
                    : () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => ChangeNotifierProvider.value(
                              value: profileData, // Reutiliza o mesmo provider
                              child: EditProfileScreen(user: profileData.user!),
                            ),
                          ),
                        );
                      },
              ),
            ),
          ],
        ),
        body: Consumer<ProfileProvider>(
          builder: (ctx, profileData, _) {
            if (profileData.isLoading) {
              return const Center(child: CircularProgressIndicator());
            }
            if (profileData.error != null || profileData.user == null) {
              return Center(
                  child: Text(profileData.error ?? 'Ocorreu um erro.'));
            }

            final user = profileData.user!;
            return RefreshIndicator(
              onRefresh: () => profileData.fetchUserProfile(),
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  const CircleAvatar(
                      radius: 50, child: Icon(Icons.person, size: 50)),
                  const SizedBox(height: 16),
                  Center(
                    child: Text(user.nome ?? 'Utilizador',
                        style: Theme.of(context).textTheme.headlineSmall),
                  ),
                  const SizedBox(height: 8),
                  Center(child: Text(user.email)),
                  const SizedBox(height: 24),
                  const Divider(),
                  ListTile(
                    leading: const Icon(Icons.cake),
                    title: const Text('Data de Nascimento'),
                    subtitle: Text(user.dataNascimento
                            ?.toLocal()
                            .toString()
                            .split(' ')[0] ??
                        'Não definido'),
                  ),
                  ListTile(
                    leading: const Icon(Icons.height),
                    title: const Text('Altura'),
                    subtitle: Text(user.alturaCm != null
                        ? '${user.alturaCm} cm'
                        : 'Não definido'),
                  ),
                  ListTile(
                    leading: const Icon(Icons.monitor_weight),
                    title: const Text('Peso'),
                    subtitle: Text(user.pesoKg != null
                        ? '${user.pesoKg} kg'
                        : 'Não definido'),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
