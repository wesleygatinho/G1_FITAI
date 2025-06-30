import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:provider/provider.dart';
import '../../models/exercise_model.dart';
import '../../providers/workout_session_provider.dart';
import '../../services/api_service.dart';
import 'pose_painter.dart';

class MonitoringScreen extends StatefulWidget {
  final Exercise exercise;

  const MonitoringScreen({super.key, required this.exercise});

  @override
  State<MonitoringScreen> createState() => _MonitoringScreenState();
}

class _MonitoringScreenState extends State<MonitoringScreen> {
  CameraController? _cameraController;
  bool _isCameraInitialized = false;
  Timer? _timer;
  Map<String, dynamic>? _analysisResult;
  bool _isProcessing = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    final cameras = await availableCameras();
    final frontCamera = cameras.firstWhere(
        (c) => c.lensDirection == CameraLensDirection.front,
        orElse: () => cameras.first);
    _cameraController = CameraController(frontCamera, ResolutionPreset.medium,
        enableAudio: false);
    try {
      await _cameraController!.initialize();
      if (!mounted) return;
      setState(() => _isCameraInitialized = true);
      _startStreaming();
    } catch (e) {
      print("Erro ao inicializar a câmara: $e");
    }
  }

  void _startStreaming() {
    _timer = Timer.periodic(const Duration(milliseconds: 1000), (timer) {
      if (!_isProcessing) _analyzeFrame();
    });
  }

  Future<void> _analyzeFrame() async {
    if (!_isCameraInitialized || _cameraController == null || !mounted) return;
    setState(() {
      _isProcessing = true;
    });
    try {
      final image = await _cameraController!.takePicture();
      final imageBytes = await image.readAsBytes();
      final base64Image = base64Encode(imageBytes);
      final response = await ApiService.post(
          'exercises/analyze',
          json.encode({
            'exercise_type': widget.exercise.apiName,
            'image_b64': base64Image
          }));
      if (response.statusCode == 200 && mounted) {
        final newResult = json.decode(utf8.decode(response.bodyBytes));
        setState(() {
          _analysisResult = newResult;
        });
        final repCount = newResult['counter'] as int? ?? 0;
        Provider.of<WorkoutSessionProvider>(context, listen: false)
            .recordRepetition(repCount);
      }
    } catch (e) {
      print("Erro ao processar o frame: $e");
    }
    if (mounted) {
      setState(() {
        _isProcessing = false;
      });
    }
  }

  Future<void> _finishWorkout() async {
    final provider =
        Provider.of<WorkoutSessionProvider>(context, listen: false);
    provider
        .finishSet(); // Garante que a última série seja registrada antes de salvar
    final success = await provider.saveWorkoutSession();
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(success ? 'Treino guardado!' : 'Falha ao guardar.'),
          backgroundColor: success ? Colors.green : Colors.red));
      Navigator.of(context).pop();
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final landmarks = _analysisResult?['landmarks'] as Map<String, dynamic>?;
    return Scaffold(
      appBar: AppBar(
        title: Text('Monitorando: ${widget.exercise.displayName}'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      backgroundColor: Colors.black,
      // SafeArea é o widget que resolve o problema de sobreposição
      body: SafeArea(
        child: _isCameraInitialized
            ? Stack(fit: StackFit.expand, children: [
                CameraPreview(_cameraController!),
                if (landmarks != null)
                  CustomPaint(
                      painter: PosePainter(
                          landmarks: landmarks,
                          imageSize: _cameraController!.value.previewSize!,
                          exerciseType: widget.exercise.apiName)),
                _buildUIOverlay(),
              ])
            : const Center(child: CircularProgressIndicator()),
      ),
    );
  }

  Widget _buildUIOverlay() {
    final sessionProvider = Provider.of<WorkoutSessionProvider>(context);
    final feedback = _analysisResult?['feedback'] as String?;
    final progress = _analysisResult?['progress'] as num? ?? 0.0;
    final counter = _analysisResult?['counter'] as int? ?? 0;
    final stage = _analysisResult?['stage'] as String? ?? 'N/A';

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.5),
                borderRadius: BorderRadius.circular(10)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Exercício: ${widget.exercise.displayName}',
                    style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 18)),
                const SizedBox(height: 8),
                Text('Série: ${sessionProvider.currentSeries}',
                    style: const TextStyle(color: Colors.white, fontSize: 16)),
                const SizedBox(height: 8),
                Text('Repetições: $counter',
                    style: const TextStyle(color: Colors.white, fontSize: 16)),
                const SizedBox(height: 8),
                Text('Fase: $stage',
                    style: const TextStyle(color: Colors.white, fontSize: 16)),
                const SizedBox(height: 12),
                const Text('Progresso da Repetição:',
                    style: TextStyle(color: Colors.white)),
                const SizedBox(height: 4),
                LinearProgressIndicator(
                  value: progress / 100,
                  backgroundColor: Colors.grey[700],
                  valueColor:
                      const AlwaysStoppedAnimation<Color>(Colors.orange),
                ),
              ],
            ),
          ),
          Column(
            children: [
              if (feedback != null)
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                      color: Colors.black.withOpacity(0.7),
                      borderRadius: BorderRadius.circular(12)),
                  child: Text(feedback,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold)),
                ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ElevatedButton(
                      onPressed: () => sessionProvider.finishSet(),
                      child: const Text('Concluir Série')),
                  ElevatedButton(
                      onPressed: _finishWorkout,
                      child: const Text('Terminar Treino'),
                      style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.red)),
                ],
              ),
            ],
          )
        ],
      ),
    );
  }
}
