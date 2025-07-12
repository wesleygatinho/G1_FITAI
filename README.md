# G1_FITAI

## Visão Geral

* Nosso projeto, o FitAI, ataca a dificuldade de obter orientação de treinos personalizados e acessíveis. A solução é um aplicativo mobile que funciona como um personal trainer virtual, utilizando a API Gemini do Google para gerar treinos customizados e a biblioteca MediaPipe para fazer a contagem de repetições e monitorar a execução dos exercícios em tempo real, garantindo a forma correta. O aplicativo é desenvolvido em Flutter, com o backend em Python utilizando FastAPI para a comunicação e gerenciamento dos dados dos usuários e seus treinos.

## Mapa do Repositório

* [documentos/](https://github.com/wesleygatinho/G1_FITAI/tree/main/Documentos): Contém a documentação do projeto, incluindo apresentações, o documento do projeto, entrevistas, e os manuais do usuário e de instalação.
* [codigo/](https://github.com/wesleygatinho/G1_FITAI/tree/main/Codigos): Contém todo o código-fonte do projeto.
* [gestao/](https://github.com/wesleygatinho/G1_FITAI/tree/main/gestao): Inclui artefatos de gerenciamento de projeto, como o registro de atividades e relatórios do Jira.

## Módulos do Projeto

Para detalhes específicos sobre cada parte do projeto, consulte os respectivos READMEs:

* **Backend:** [Consulte o README do Backend](https://github.com/wesleygatinho/G1_FITAI/blob/main/Codigos/backend/README.md)
* **App Flutter:** [Consulte o README do App Flutter](https://github.com/wesleygatinho/G1_FITAI/blob/main/Codigos/flutter_app/README.md)
* **Pasta Adicional:** [Pasta APK do APP FITAI](https://drive.google.com/drive/folders/1yXh-N1C-jJqAhx7zjTAPUkgJtsq_k0RJ?usp=sharing)
## Como Rodar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/wesleygatinho/G1_FITAI.git
    ```
2.  **Crie e ative um ambiente virtual (para o backend):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Windows, use `venv\Scripts\activate`
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o projeto:**
    Acesse a pasta do backend e execute em um terminal com o ambiente virtual ativado:

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

    Depois, em outro terminal, acesse a pasta flutter_app e execute:
    ```bash
    flutter pub get
    flutter run
    ```

    Obs: Acesse os README.md da pasta do backend e do flutter_app para mais informações.

---

# Reconhecimentos e Direitos Autorais
 
@autor: ANDRE LUIS AGUIAR DO NASCIMENTO, LEONARDO SAMPAIO SERRA, HUGO SAMUEL DE LIMA OLIVEIRA, LUCAS EMANOEL AMARAL GOMES, WESLEY DOS SANTOS GATINHO

@contato: andre.aguiar@discente.ufma.br, leonardo.sampaio@discente.ufma.br, hugo.samuel@discente.ufma.br, lucas.amaral@discente.ufma.br, wesley.gatinho@discente.ufma.br

@data última versão: 01/07/2025

@versão: 1.3

@outros repositórios: https://github.com/wesleygatinho/G1_FITAI.git

@Agradecimentos: Universidade Federal do Maranhão (UFMA), Professor Doutor Thales Levi Azevedo Valente, e colegas de curso.
 
Copyright/License
 
Este material é resultado de um trabalho acadêmico para a disciplina PROJETO E DESENVOLVIMENTO DE SOFTWARE, sob a orientação do professor Dr. THALES LEVI AZEVEDO VALENTE, semestre letivo 2025.1, curso Engenharia da Computação, na Universidade Federal do Maranhão (UFMA). Todo o material sob esta licença é software livre: pode ser usado para fins acadêmicos e comerciais sem nenhum custo. Não há papelada, nem royalties, nem restrições de "copyleft" do tipo GNU. Ele é licenciado sob os termos da Licença MIT, conforme descrito abaixo, e, portanto, é compatível com a GPL e também se qualifica como software de código aberto. É de domínio público. Os detalhes legais estão abaixo. O espírito desta licença é que você é livre para usar este material para qualquer finalidade, sem nenhum custo. O único requisito é que, se você usá-los, nos dê crédito.
 
Licenciado sob a Licença MIT. Permissão é concedida, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados (o "Software"), para lidar no Software sem restrição, incluindo sem limitação os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software, e permitir pessoas a quem o Software é fornecido a fazê-lo, sujeito às seguintes condições:
 
Este aviso de direitos autorais e este aviso de permissão devem ser incluídos em todas as cópias ou partes substanciais do Software.
 
O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO INFRINGÊNCIA. EM NENHUM CASO OS AUTORES OU DETENTORES DE DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER RECLAMAÇÃO, DANOS OU OUTRA RESPONSABILIDADE, SEJA EM AÇÃO DE CONTRATO, TORT OU OUTRA FORMA, DECORRENTE DE, FORA DE OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.

Para mais informações sobre a Licença MIT: https://opensource.org/licenses/MIT.
