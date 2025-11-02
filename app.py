from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import logging
import os
import re

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

PROMPT_IA = (
    "Você é um especialista em previsão de alagamentos urbanos. "
    "Baseie suas respostas em padrões climáticos históricos e características geográficas. "
    "Siga estas regras:\n"
    "1. ANALISE a localização fornecida (ex: 'Vergueiro, SP' = área urbana com declives)\n"
    "2. CONSIDERE a época do ano (chuvas de verão, etc)\n"
    "3. DÊ 1-2 frases de contexto sobre a região\n"
    "4. PREVISÃO para 7 dias (use termos como 'probabilidade' e 'risco moderado')\n"
    "5. RECOMENDAÇÕES práticas (3 itens com emojis)\n"
    "6. FORMATE com emojis e negrito nos títulos\n\n"
    "Exemplo para São Paulo:\n"
    "🌧️ **Previsão Próximos 7 Dias:** \n"
    "Probabilidade de chuva intensa (70%) entre quinta e sábado, com risco alto de alagamentos em áreas baixas.\n\n"
    "⚠️ **Risco Atual:** \n"
    "Moderado (histórico de alagamentos na região em chuvas >50mm/h)\n\n"
    "🏠 **Recomendações:** \n"
    "• Evite a Av. 23 de Maio entre 14h-18h\n"
    "• Verifique rotas alternativas no Waze\n"
    "• Tenha kit emergência em casa\n"
    "Atualize com @climasp antes de sair!"
    "ADAPTE a linguagem que o usuario está se comunicando com você, se a mensagem for em inglês você DEVE responder em inglês, assim com todas as outras línguas."
)

def formatar_resposta(texto):
    """Formata a resposta da IA para remover markdown desnecessário"""
    texto = re.sub(r"\*\*(.*?)\*\*", r"\1", texto)
    texto = re.sub(r"^\s*\d+\.\s*", "👉 ", texto, flags=re.MULTILINE)
    texto = texto.replace("*", "")
    return texto.strip()

@app.route('/')
def home():
    return render_template('index.html', title='Início')

@app.route('/equipe')
def equipe():
    return render_template('equipe.html', title='Equipe')

@app.route('/ia')
def pagina_ia():
    return render_template('ia.html', title='IA Simples')

@app.route('/chat')
def pagina_chat():
    return render_template('chat.html', title='Chat IA')

@app.route('/api/chat', methods=['POST'])
def consulta_ia():
    try:
        data = request.get_json()
        if not data or 'local' not in data:
            return jsonify({'error': 'Localização não informada.'}), 400
        
        local = data['local'].strip()
        if len(local) < 2:
            return jsonify({'error': 'Localização muito curta.'}), 400
            
        if local == "67":
            return jsonify({'resposta': 'six sevennn ⁶🤷⁷ 🙏🙏😭😭'})

        chat = model.start_chat()
        chat.send_message(PROMPT_IA)
        pergunta = f"Estou em {local}, há risco de alagamento ou chuvas fortes?"
        
        resposta_bruta = chat.send_message(pergunta).text
        
        if not resposta_bruta or "não há dados suficientes" in resposta_bruta.lower() or "não consigo" in resposta_bruta.lower():
            resposta_formatada = "Desculpe, não consegui obter uma previsão detalhada para esta localização. Por favor, tente uma localização mais específica ou verifique a ortografia."
        else:
            resposta_formatada = formatar_resposta(resposta_bruta)
        
        logger.info(f"Consulta para: {local}")
        return jsonify({'resposta': resposta_formatada})

    except Exception as e:
        logger.error(f"Erro na consulta: {str(e)}", exc_info=True)
        return jsonify({'error': 'Ocorreu um erro interno. Tente novamente.'}), 500

@app.context_processor
def inject_global_vars():
    return {
        'site_name': 'IAbiku',
        'current_year': 2025
    }