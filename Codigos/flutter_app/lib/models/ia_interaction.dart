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

  factory IAInteraction.fromJson(Map<String, dynamic> json) {
    return IAInteraction(
      id: json['id'].toString(),
      data: DateTime.parse(json['data']),
      promptUsuario: json['prompt_usuario'] ?? "",
      respostaIa: json['resposta_ia'] ?? "",
    );
  }

  bool get isPlanoPersonalizado => promptUsuario.trim().isNotEmpty;
  bool get isDica => promptUsuario.trim().isEmpty;
}
