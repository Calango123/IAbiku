import google.generativeai as genai
from dotenv import load_dotenv
import os

# vai carrega as variaveis suave
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# cria o chat
chat = model.start_chat()

# define promsptmt sei la escrever prpomtop
system_prompt = "Você é um modelo de previsão de alagamentos em áreas urbanas. A partir da localização fornecida (cidade, bairro ou coordenadas geográficas) e usando dados climáticos, históricos de alagamentos, infraestrutura urbana e previsão do tempo para os próximos 7 dias, analise e informe: A probabilidade de alagamento nos próximos 7 dias. Quais fatores contribuem para essa previsão, como volume de chuva, drenagem urbana deficiente, proximidade com rios/córregos, entre outros. Recomendações preventivas específicas para o local informado, caso o risco seja moderado ou alto. Responda de forma clara, objetiva e compreensível mesmo para usuários leigos. Utilize linguagem simples e, se possível, apresente a previsão em formato de nível de risco (baixo, moderado, alto) com justificativas."

try:
    # vai enviar a mensagem de cima ai pra começar o chat
    chat.send_message(system_prompt)

    regiao = input('Olá eu sou o IAbiku, estou aqui para te auxiliar com alagamentos!\nOnde você está? ')

    user_prompt = f'Estou em {regiao}, estou seguro ou há alguma previsão de chuvas fortes ou enchentes?'

    response = chat.send_message(user_prompt)
    print(response.text)
except Exception as e:
    print(f"Ocorreu um erro: {e}") 
