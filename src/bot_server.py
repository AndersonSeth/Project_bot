import os
from dotenv import load_dotenv  # Importa o dotenv
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)

# Função para enviar e-mail
def enviar_email(assunto, mensagem, destinatario):
    remetente = "anderson.chga@gmail.com"
    senha = os.getenv("EMAIL_PASSWORD")  # Obtém a senha do .env

    if not senha:
        print("Erro: Senha do e-mail não configurada.")
        return False

    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
        return True
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False

# Rota para receber solicitações do Watsonx Assistant
@app.route("/solicitar", methods=["POST"])
def solicitar():
    data = request.json  # Recebe os dados em formato JSON do Watsonx Assistant
    tipo = data.get("tipo")  # Tipo de solicitação (motoboy, correios, manutencao)
    info = data.get("info")  # Detalhes da solicitação

    if tipo == "motoboy":
        destinatario = "anderson.silva@bshlaw.com.br"
        assunto = "Nova Solicitação de Motoboy"
    elif tipo == "correios":
        destinatario = "anderson.silva@bshlaw.com.br"
        assunto = "Nova Solicitação de Envio aos Correios"
    elif tipo == "manutencao":
        destinatario = "anderson.silva@bshlaw.com.br"
        assunto = "Nova Solicitação de Manutenção"
    else:
        return jsonify({"erro": "Tipo de solicitação inválido"}), 400

    mensagem = f"Solicitação recebida:\n{info}"

    if enviar_email(assunto, mensagem, destinatario):
        return jsonify({"mensagem": "Solicitação enviada com sucesso"}), 200
    else:
        return jsonify({"erro": "Falha no envio do e-mail"}), 500

if __name__ == "__main__":
    app.run(host="localhost", port=5002, debug=True)
