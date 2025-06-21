class IAInteraction {
  final String id;
  final DateTime data;
  final String promptUsuario;
  final String respostaIa;

  IAInteraction({
    required this.id,
    required this.data,
    required this.promptUsuario,
    required this.respostaIa,
  });

  // Factory para criar um IAInteraction a partir do JSON da API
  factory IAInteraction.fromJson(Map<String, dynamic> json) {
    return IAInteraction(
      id: json['id'],
      data: DateTime.parse(json['data']),
      promptUsuario: json['prompt_usuario'],
      respostaIa: json['resposta_ia'],
    );
  }
}
