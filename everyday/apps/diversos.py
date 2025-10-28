import subprocess
import time
from apps.helpers import executando, log
import json
import os


def ler_dados_json():
    ''' Lê os dados do arquivo JSON que contém a lista de programas.
    Returns:
        dict: Dicionário com os dados lidos do arquivo JSON. '''
    # busca o caminho para abir abrir o arquivo de programas
    project_root = os.getcwd()
    json_path = os.path.join(project_root, 'data', 'list_programs.json')

    # Garante que o diretório existe
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    try:
        with open(json_path, "r") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        dados = {}
    return dados


def abrir_programa(nome_programa):
    ''' Abre um programa se ele não estiver em execução.
    Args:
        nome_programa (str): Nome do programa a ser aberto.
    '''
    pgm_exe = f"{nome_programa}.exe"
    if not executando(pgm_exe):
        subprocess.Popen(["start", nome_programa], shell=True)
        time.sleep(5)
        log(f'{nome_programa} iniciado.')
    else:
        log(f'{nome_programa} já está em execução.')


def abrir_todos_programas():
    ''' Abre todos os programas listados no arquivo JSON.'''
    dados = ler_dados_json()
    for nome_programa in dados.values():
        abrir_programa(nome_programa)
