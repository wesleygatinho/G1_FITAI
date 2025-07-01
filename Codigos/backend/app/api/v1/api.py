"""
@file api.py
@brief Agrega todos os roteadores de endpoints da API v1.
@author Gemini AI <example@example.com>
"""

from fastapi import APIRouter
from .endpoints import auth, exercises, progress, ai_generator, session, users, exercicio

# Cria o roteador principal da API v1, que incluirá todos os outros.
api_router = APIRouter()

# Inclui o roteador de autenticação (login, etc.) com o prefixo /auth.
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Inclui o roteador para a análise de frames de exercícios em tempo real.
api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])

# Inclui o roteador para interações com a IA generativa (dicas, planos de treino, OCR).
api_router.include_router(ai_generator.router, prefix="/ai", tags=["AI Generator"])

# Inclui o roteador para o registo de progresso (peso, medidas, cardio).
api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])

# Inclui o roteador para a gestão de sessões de treino.
api_router.include_router(session.router, prefix="/sessions", tags=["Workout Sessions"])

# Inclui o roteador para a gestão de utilizadores (perfis, etc.).
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Inclui o roteador para a gestão de exercícios (CRUD de exercícios).
api_router.include_router(exercicio.router, prefix="/exercicios", tags=["Exercises Management"])