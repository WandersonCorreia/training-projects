import os
import json
from datetime import datetime


def localiza_jason():
    ''' Localiza o arquivo JSON de controle de execuções.
    Returns:
        str: Caminho completo do arquivo JSON de controle. '''
    # busca o caminho para salvar o arquivo de controle
    project_root = os.getcwd()
    json_path = os.path.join(project_root, 'data', 'controle_execucao.json')

    # Garante que o diretório existe
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    return json_path


def ja_executou(periodo):
    ''' Verifica se a rotina do período especificado já foi executada hoje.
    Args:
        periodo (str): Período a ser verificado ('manha', 'tarde', 'noite').
        Returns:
        bool: True se a rotina já foi executada hoje, False caso contrário.'''
    json_path = localiza_jason()
    try:
        with open(json_path, "r") as f:
            controle = json.load(f)
    except FileNotFoundError:
        controle = {}

    hoje = datetime.now().strftime("%Y-%m-%d")
    return controle.get(hoje, {}).get(periodo, False)


def registrar_execucao(periodo):
    ''' Registra a execução da rotina do período especificado para hoje.
    Args:
        periodo (str): Período a ser registrado ('manha', 'tarde', 'noite').   '''
    json_path = localiza_jason()
    try:
        with open(json_path, "r") as f:
            controle = json.load(f)
    except FileNotFoundError:
        controle = {}

    hoje = datetime.now().strftime("%Y-%m-%d")
    if hoje not in controle:
        controle[hoje] = {}

    controle[hoje][periodo] = True

    with open(json_path, "w") as f:
        json.dump(controle, f)
