"""
@file ai_generation_service.py
@brief Fornece uma classe de serviço para interagir com a API do Google Gemini.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import google.generativeai as genai
from app.core.config import settings
import base64
import json
import re

class AIGenerationService:
    """Encapsula a lógica para fazer chamadas à API do Google Gemini.

    Esta classe gerencia a configuração do modelo, a geração de conteúdo de texto
    e a extração de dados de imagens (OCR) usando o Gemini.

    Attributes:
        api_key (str): A chave da API do Google carregada a partir das configurações.
        model (genai.GenerativeModel): A instância do modelo generativo 'gemini-1.5-flash',
                                       ou None se a configuração falhar.
    """
    def __init__(self):
        """Inicializa o serviço de geração de IA.

        Configura o cliente do Google Gemini com a chave da API fornecida nas
        configurações. Lida com exceções e avisa se a chave não estiver configurada.
        """
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
        """Gera uma dica de fitness diária usando a IA.

        Envia um prompt para a IA solicitando uma dica motivacional e prática.

        :return (dict): Um dicionário contendo a dica gerada ou uma mensagem de erro.
        """
        if not self.model:
            return {"error": "A API do Google Gemini não está configurada corretamente."}

        prompt = "Aja como um personal trainer e nutricionista motivacional que fala em português do Brasil. Forneça uma dica de fitness curta, motivacional e prática para hoje."
        
        try:
            response = self.model.generate_content(prompt)
            return {"prompt_usuario": prompt, "resposta_ia": response.text}
        except Exception as e:
            return {"error": f"Erro ao contatar a IA: {e}"}

    def generate_custom_workout_plan(self, prompt: str):
        """Cria um plano de treino personalizado com base em um prompt do usuário.

        :param (str) prompt: A solicitação do usuário para o plano de treino.
        :return (dict): Um dicionário contendo o plano gerado ou uma mensagem de erro.
        """
        if not self.model:
            return {"error": "A API do Google Gemini não está configurada corretamente."}

        full_prompt = f"Aja como um personal trainer de elite que cria planos de treino detalhados e estruturados em português do Brasil. O utilizador pediu o seguinte: '{prompt}'."
        
        try:
            response = self.model.generate_content(full_prompt)
            return {"prompt_usuario": prompt, "resposta_ia": response.text}
        except Exception as e:
            return {"error": f"Erro ao contatar a IA: {e}"}

    def extract_data_from_image_with_gemini(self, image_base64: str, data_type: str):
        """Extrai dados estruturados de uma imagem usando o modelo multimodal do Gemini.

        Decodifica uma imagem em base64 e a envia para a IA com um prompt específico
        para extrair dados de peso, cardio ou medidas, retornando um JSON estruturado.

        :param (str) image_base64: A imagem codificada em formato base64.
        :param (str) data_type: O tipo de dado a extrair ('weight', 'cardio', 'measure').
        :return (dict): Um dicionário JSON com os dados extraídos ou uma mensagem de erro.
        """
        if not self.model:
            return {"error": "A API do Google Gemini não está configurada corretamente."}

        try:
            image_bytes = base64.b64decode(image_base64)
            image_part = {"mime_type": "image/jpeg", "data": image_bytes}
            
            if data_type == 'weight':
                prompt = "Analise a imagem de uma balança e extraia o peso. Se a unidade for 'lb' (libras), converta para quilogramas (1 lb = 0.453592 kg). Retorne um JSON com a chave 'peso_kg' (float)."
            elif data_type == 'cardio':
                prompt = (
                    "Aja como um especialista em análise de imagens de equipamentos de ginástica. Analise a imagem de um painel de esteira ou bicicleta e extraia três valores: tempo, distância e calorias.\n"
                    "1.  **Tempo**: Encontre o valor principal de tempo (ex: 17:40). Retorne **apenas o número inteiro de minutos**.\n"
                    "2.  **Distância**: Encontre o valor de distância. Procure pela unidade ('km' ou 'mi'). Se for milhas, converta para km (1 mi = 1.60934 km).\n"
                    "3.  **Calorias**: Encontre o valor rotulado como 'KCAL' ou 'CALORIES'.\n"
                    "Retorne um JSON estritamente com as chaves 'tempo_min' (integer), 'distancia_km' (float), e 'calorias' (integer)."
                )
            elif data_type == 'measure':
                prompt = "Analise a imagem de uma fita métrica medindo uma parte do corpo e extraia o valor em centímetros. Retorne um JSON com a chave 'valor_cm' (float)."
            else:
                return {"error": "Tipo de dado para OCR não suportado."}

            response = self.model.generate_content([prompt, image_part])
            
            print(f"--- RESPOSTA BRUTA DA API GEMINI ({data_type}) ---\n{response.text}\n------------------------------------------")
            
            # Limpa a resposta para garantir que seja um JSON válido
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

# Cria uma instância única (singleton) do serviço para ser usada em toda a aplicação.
ai_generation_service = AIGenerationService()
