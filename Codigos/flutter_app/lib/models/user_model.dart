class User {
  final String id;
  final String email;
  final String? nome;
  final DateTime? dataNascimento;
  final double? alturaCm;
  final double? pesoKg;

  User({
    required this.id,
    required this.email,
    this.nome,
    this.dataNascimento,
    this.alturaCm,
    this.pesoKg,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      nome: json['nome'],
      dataNascimento: json['data_nascimento'] != null 
          ? DateTime.parse(json['data_nascimento']) 
          : null,
      alturaCm: json['altura_cm']?.toDouble(),
      pesoKg: json['peso_kg']?.toDouble(),
    );
  }
}
