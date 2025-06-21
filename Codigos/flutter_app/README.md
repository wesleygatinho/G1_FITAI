# FitAI - Aplicativo Flutter

Este é o aplicativo móvel do projeto FitAI, desenvolvido com Flutter. O app oferece uma interface de usuário rica e interativa para que os usuários possam monitorar seus treinos, acompanhar o progresso e interagir com funcionalidades de inteligência artificial.

## 🌟 Funcionalidades

* **Interface Intuitiva**: Telas limpas e fáceis de usar para uma ótima experiência do usuário.
* **Autenticação Segura**: Login e registro de usuários.
* **Acompanhamento de Exercícios**: Inicie uma sessão de treino e receba feedback em tempo real.
* **Dashboard de Progresso**: Visualize seu progresso com gráficos e dados históricos sobre peso e medidas.
* **Histórico de Treinos**: Acesse um registro completo de todas as suas sessões de treino passadas.
* **Interação com IA**: Obtenha dicas diárias e gere planos de treino personalizados através da integração com o backend.
* **Lista de Exercícios**: Navegue pelos exercícios disponíveis e veja as instruções de como executá-los corretamente.

## 🛠️ Tecnologias e Pacotes Utilizados

* **Framework**: Flutter
* **Gerenciamento de Estado**: Provider
* **Requisições HTTP**: `http`
* **Armazenamento Local**: `shared_preferences`
* **Gráficos**: `fl_chart`
* **Câmera**: `camera`
* **Renderização de Markdown**: `flutter_markdown`
* **Formatação de Datas**: `intl`

## 🚀 Começando

Siga estas instruções para configurar e executar o projeto localmente em um emulador ou dispositivo físico.

### Pré-requisitos

* Flutter SDK (versão 3.0.0 ou superior)
* Dart SDK (versão 3.0.0 ou superior)
* Um emulador Android ou iOS configurado, ou um dispositivo físico.
* O [servidor backend](#link-para-o-readme-do-backend) deve estar em execução.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/wesleygatinho/G1_FITAI.git
    cd G1_FITAI/Codigos/flutter_app
    ```

2.  **Instale as dependências do Flutter:**
    ```bash
    flutter pub get
    ```

3.  **Configure a Conexão com a API:**
    Abra o arquivo `lib/services/api_service.dart` e atualize a constante `_localIp` com o endereço IP da máquina onde o backend está rodando, caso esteja testando em um dispositivo físico.
    ```dart
    // Substitua "SEU_IP_AQUI" pelo IP da sua máquina.
    static const String _localIp = "SEU_IP_AQUI";
    ```

### Executando o Aplicativo

Com o emulador em execução ou um dispositivo conectado, rode o seguinte comando na raiz da pasta `flutter_app`:

```bash
flutter run
```

O aplicativo será compilado e instalado no dispositivo selecionado.

## 📁 Estrutura do Projeto

* ```lib/main.dart```: Ponto de entrada principal da aplicação.
* ```lib/providers/```: Provedores de estado para gerenciar a lógica da UI.
* ```lib/screens/```: Contém todas as telas (widgets de página) da aplicação, organizadas por funcionalidade.
* ```lib/services/```: Classes responsáveis pela comunicação com a API e outros serviços externos.
* ```pubspec.yaml```: Arquivo de configuração do projeto Flutter, onde as dependências são declaradas.

## 📄 Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo [README.md](#https://github.com/wesleygatinho/G1_FITAI) na raiz do projeto para mais detalhes.

## 🧑‍💻 Autores

* **André Luis Aguiar do Nascimento**
* **Hugo Samuel de Lima Oliveira**
* **Leonardo Sampaio Serra**
* **Lucas Emanoel Amaral Gomes**
* **Wesley dos Santos Gatinho**