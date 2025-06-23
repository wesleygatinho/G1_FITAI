import 'package:flutter/material.dart';

class PosePainter extends CustomPainter {
  final Map<String, dynamic> landmarks;
  final Size imageSize;
  final String exerciseType; // Novo: para saber o que desenhar

  PosePainter({
    required this.landmarks,
    required this.imageSize,
    required this.exerciseType,
  });

  @override
  void paint(Canvas canvas, Size size) {
    // Escolhe a função de desenho correta com base no tipo de exercício
    switch (exerciseType) {
      case 'squat':
        _drawSquat(canvas, size);
        break;
      case 'push_up':
      case 'hammer_curl':
        _drawUpperBody(canvas, size);
        break;
      default:
        // Não desenha nada se o exercício for desconhecido
        break;
    }
  }

  // Função para desenhar o esqueleto de um agachamento
  void _drawSquat(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.amber
      ..strokeWidth = 4
      ..strokeCap = StrokeCap.round;
    final circlePaint = Paint()..color = Colors.indigo.shade300;

    Offset toCanvasCoord(dynamic point) {
      if (point == null) return Offset.zero;
      // As coordenadas são normalizadas (0.0 a 1.0), por isso multiplicamos pelo tamanho da tela
      return Offset(point[0] * size.width, point[1] * size.height);
    }

    final shoulder = toCanvasCoord(landmarks['shoulder']);
    final hip = toCanvasCoord(landmarks['hip']);
    final knee = toCanvasCoord(landmarks['knee']);
    final ankle = toCanvasCoord(landmarks['ankle']);

    // Desenha as linhas que ligam as articulações
    if (shoulder != Offset.zero && hip != Offset.zero)
      canvas.drawLine(shoulder, hip, paint);
    if (hip != Offset.zero && knee != Offset.zero)
      canvas.drawLine(hip, knee, paint);
    if (knee != Offset.zero && ankle != Offset.zero)
      canvas.drawLine(knee, ankle, paint);

    // Desenha os círculos nas articulações
    canvas.drawCircle(shoulder, 8, circlePaint);
    canvas.drawCircle(hip, 8, circlePaint);
    canvas.drawCircle(knee, 8, circlePaint);
    canvas.drawCircle(ankle, 8, circlePaint);
  }

  // Função para desenhar o esqueleto da parte superior do corpo
  void _drawUpperBody(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.amber
      ..strokeWidth = 4
      ..strokeCap = StrokeCap.round;
    final circlePaint = Paint()..color = Colors.indigo.shade300;

    Offset toCanvasCoord(dynamic point) {
      if (point == null) return Offset.zero;
      return Offset(point[0] * size.width, point[1] * size.height);
    }

    // Pontos do braço esquerdo
    final shoulderLeft = toCanvasCoord(landmarks['shoulder_left']);
    final elbowLeft = toCanvasCoord(landmarks['elbow_left']);
    final wristLeft = toCanvasCoord(landmarks['wrist_left']);

    // Pontos do braço direito
    final shoulderRight = toCanvasCoord(landmarks['shoulder_right']);
    final elbowRight = toCanvasCoord(landmarks['elbow_right']);
    final wristRight = toCanvasCoord(landmarks['wrist_right']);

    // Desenha o braço esquerdo
    if (shoulderLeft != Offset.zero && elbowLeft != Offset.zero)
      canvas.drawLine(shoulderLeft, elbowLeft, paint);
    if (elbowLeft != Offset.zero && wristLeft != Offset.zero)
      canvas.drawLine(elbowLeft, wristLeft, paint);

    // Desenha o braço direito
    if (shoulderRight != Offset.zero && elbowRight != Offset.zero)
      canvas.drawLine(shoulderRight, elbowRight, paint);
    if (elbowRight != Offset.zero && wristRight != Offset.zero)
      canvas.drawLine(elbowRight, wristRight, paint);

    // Desenha os círculos nas articulações
    canvas.drawCircle(shoulderLeft, 8, circlePaint);
    canvas.drawCircle(elbowLeft, 8, circlePaint);
    canvas.drawCircle(wristLeft, 8, circlePaint);
    canvas.drawCircle(shoulderRight, 8, circlePaint);
    canvas.drawCircle(elbowRight, 8, circlePaint);
    canvas.drawCircle(wristRight, 8, circlePaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true; // Redesenha sempre que os dados mudam
  }
}
