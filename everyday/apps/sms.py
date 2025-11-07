from twilio.rest import Client
import os
import json


def ler_dados_json():
    ''' Lê os dados do arquivo JSON que contém os dados do SMS.
    Returns:
        dict: Dicionário com os dados lidos do arquivo JSON. '''

    project_root = os.getcwd()
    json_path = os.path.join(project_root, 'data', 'sms.json')

    # Garante que o diretório existe
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    try:
        with open(json_path, "r") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        dados = {}
    return dados


def envia_sms(mensagem):
    ''' Envia um SMS com a mensagem fornecida.'''
    # Configurações da conta Twilio
    dados_sms = ler_dados_json()

    account_sid = dados_sms['conta']
    auth_token = dados_sms['token']
    from_number = dados_sms['numero_de']
    to_number = dados_sms['numero_para']

    if auth_token:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=mensagem,
            from_=from_number,
            to=to_number
        )
