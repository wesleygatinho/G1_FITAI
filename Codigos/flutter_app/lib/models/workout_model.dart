// Modelo simples para o exercício dentro da sessão de histórico
class ExercicioHistorico {
  final String nome;

  ExercicioHistorico({required this.nome});

  factory ExercicioHistorico.fromJson(Map<String, dynamic> json) {
    // A API retorna um campo 'nome' dentro do objeto 'exercicio'
    return ExercicioHistorico(
      nome: (json['nome'] as String)
          .replaceAll('_', ' ')
          .split(' ')
          .map((l) => l[0].toUpperCase() + l.substring(1))
          .join(" "),
    );
  }
}

class ItemSessao {
  final ExercicioHistorico exercicio;
  final int series;
  final int repeticoes;

  ItemSessao({
    required this.exercicio,
    required this.series,
    required this.repeticoes,
  });

  factory ItemSessao.fromJson(Map<String, dynamic> json) {
    return ItemSessao(
      exercicio: ExercicioHistorico.fromJson(json['exercicio']),
      series: json['series'],
      repeticoes: json['repeticoes'],
    );
  }
}

class SessaoDeTreino {
  final String id;
  final DateTime dataInicio;
  final List<ItemSessao> itens;

  SessaoDeTreino({
    required this.id,
    required this.dataInicio,
    required this.itens,
  });

  factory SessaoDeTreino.fromJson(Map<String, dynamic> json) {
    var itemsList = json['itens'] as List;
    List<ItemSessao> parsedItems =
        itemsList.map((i) => ItemSessao.fromJson(i)).toList();

    final dataString = json['data_inicio'] as String;

    return SessaoDeTreino(
      id: json['id'],
      dataInicio: DateTime.parse('${dataString}Z'),
      itens: parsedItems,
    );
  }
}
