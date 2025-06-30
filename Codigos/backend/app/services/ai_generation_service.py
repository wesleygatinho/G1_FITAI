import google.generativeai as genai
from app.core.config import settings
import base64
import json
import re

class AIGenerationService:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        self.model = None
        if self.api_key and self.api_key != "CHAVE_NAO_CONFIGURADA":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("API do Google Gemini configurada com sucesso.")
            except Exception as e:
                print(f"Erro ao inicializar o cliente do Gemini: {e}")
        else:
            print("Aviso: A chave da API do Google não está configurada no ficheiro .env.")

    def get_daily_fitness_tip(self):
        if not self.model:
            return {"error": "A API do Google Gemini não está configurada corretamente."}

        prompt = "Aja como um personal trainer e nutricionista motivacional que fala em português do Brasil. Forneça uma dica de fitness curta, motivacional e prática para hoje."
        
        try:
            response = self.model.generate_content(prompt)
            resposta_ia = response.text
            return {"prompt_usuario": prompt, "resposta_ia": resposta_ia}
        except Exception as e:
            return {"error": "Erro ao contatar a IA."}

    def generate_custom_workout_plan(self, prompt: str):
        if not self.model:
            return {"error": "A API do Google Gemini não está configurada corretamente."}

        full_prompt = f"Aja como um personal trainer de elite que cria planos de treino detalhados e estruturados em português do Brasil. O utilizador pediu o seguinte: '{prompt}'."
        
        try:
            response = self.model.generate_content(full_prompt)
            resposta_ia = response.text
            return {"prompt_usuario": prompt, "resposta_ia": resposta_ia}
        except Exception as e:
            return {"error": "Erro ao contatar a IA."}

    # --- FUNÇÃO CORRIGIDA COM LOGS E MAIS SEGURANÇA ---
    def extract_data_from_image_with_gemini(self, image_base64: str, data_type: str):
        if not self.model:
            return {"error": "A API do Google Gemini não está configurada corretamente."}

        try:
            image_bytes = base64.b64decode(image_base64)
            image_part = {"mime_type": "image/jpeg", "data": image_bytes}
            
            # Seus prompts excelentes são mantidos
            if data_type == 'weight':
                prompt = "Analise a imagem de uma balança e extraia o peso. Se a unidade for 'lb' (libras), converta para quilogramas (1 lb = 0.453592 kg). Retorne um JSON com a chave 'peso_kg' (float)."
            elif data_type == 'cardio':
                prompt = (
                    "Aja como um especialista em análise de imagens de equipamentos de ginástica. Analise a imagem de um painel de esteira ou bicicleta e extraia três valores: tempo, distância e calorias.\n"
                    "1.  **Tempo**: Encontre o valor principal de tempo, que geralmente está no formato 'minutos:segundos' ou 'minutos.segundos' (ex: 17:40). Extraia e retorne **apenas o número inteiro de minutos**.\n"
                    "2.  **Distância**: Encontre o valor principal de distância. Depois, examine a imagem inteira em busca de pistas sobre a unidade. A pista pode ser 'km', 'mi', ou 'miles'. Muitas vezes, a pista está em um texto menor ou em uma tabela de referência (ex: '400 Meters | 0.25 Miles'). Se a unidade inferida for **milhas**, converta o valor para quilômetros (1 milha = 1.60934 km) e arredonde para duas casas decimais. Se for km, use o valor como está.\n"
                    "3.  **Calorias**: Encontre o valor rotulado como 'KCAL' ou 'CALORIES'.\n"
                    "Retorne um JSON estritamente com as chaves 'tempo_min' (integer), 'distancia_km' (float), e 'calorias' (integer)."
                )
            elif data_type == 'measure':
                prompt = "Analise a imagem de uma fita métrica medindo uma parte do corpo e extraia o valor em centímetros. Retorne um JSON com a chave 'valor_cm' (float)."
            else:
                return {"error": "Tipo de dado para OCR não suportado."}

            response = self.model.generate_content([prompt, image_part])
            
            # Log para vermos o que a IA está respondendo
            print("--- RESPOSTA BRUTA DA API GEMINI (OCR) ---")
            print(response.text)
            print("------------------------------------------")
            
            # Limpeza robusta da resposta para garantir que seja um JSON válido
            cleaned_text = response.text.strip()
            json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                print("ERRO: A resposta da IA não continha um JSON válido.")
                return {"error": "A IA não conseguiu extrair os dados em um formato reconhecível."}

        except Exception as e:
            print(f"ERRO CRÍTICO na função extract_data_from_image_with_gemini: {e}")
            return {"error": "Ocorreu uma falha inesperada ao analisar a imagem."}

ai_generation_service = AIGenerationService()