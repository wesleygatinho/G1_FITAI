import google.generativeai as genai
from app.core.config import settings

# --- Configuração da API do Google Gemini ---
api_key = settings.GOOGLE_API_KEY
model = None

if api_key and api_key != "CHAVE_NAO_CONFIGURADA":
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("API do Google Gemini configurada com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o cliente do Gemini: {e}")
else:
    print("Aviso: A chave da API do Google não está configurada no ficheiro .env.")


def get_daily_fitness_tip():
    """
    Gera uma dica de fitness. 
    Retorna um dicionário com o prompt e a resposta, mas não guarda nada.
    """
    if not model:
        return {"error": "A API do Google Gemini não está configurada corretamente."}

    prompt = "Aja como um personal trainer e nutricionista motivacional que fala em português do Brasil. Forneça uma dica de fitness curta, motivacional e prática para hoje."
    
    try:
        response = model.generate_content(prompt)
        resposta_ia = response.text
        # Retorna os dados para o endpoint poder guardá-los
        return {"prompt_usuario": prompt, "resposta_ia": resposta_ia}
    except Exception as e:
        print(f"Erro detalhado ao chamar a API para a dica: {e}")
        return {"error": "Erro ao contatar a IA."}


def generate_custom_workout_plan(prompt: str):
    """
    Gera um plano de treino personalizado.
    Retorna um dicionário com o prompt e a resposta, mas não guarda nada.
    """
    if not model:
        return {"error": "A API do Google Gemini não está configurada corretamente."}

    full_prompt = f"Aja como um personal trainer de elite que cria planos de treino detalhados e estruturados em português do Brasil. O utilizador pediu o seguinte: '{prompt}'."
    
    try:
        response = model.generate_content(full_prompt)
        resposta_ia = response.text
        # Retorna os dados para o endpoint poder guardá-los
        return {"prompt_usuario": prompt, "resposta_ia": resposta_ia}
    except Exception as e:
        print(f"Erro detalhado ao chamar a API para o plano: {e}")
        return {"error": "Erro ao contatar a IA."}
