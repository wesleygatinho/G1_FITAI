from fastapi import APIRouter
from .endpoints import auth, exercises, progress, ai_generator, session, users, exercicio

api_router = APIRouter()

# Roteador de Autenticação
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Roteador de Análise de Exercícios
api_router.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])

# Roteador do Gerador com IA
api_router.include_router(ai_generator.router, prefix="/ai", tags=["AI Generator"])

# Roteador para Registo de Progresso
api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])

# NOVO ROTEADOR PARA SESSÕES DE TREINO
api_router.include_router(session.router, prefix="/sessions", tags=["Workout Sessions"])

# Roteador de Utilizadores
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Roteador de Exercícios
api_router.include_router(exercicio.router, prefix="/exercicios", tags=["Exercises Management"])