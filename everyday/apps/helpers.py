import psutil
import logging
from datetime import datetime
from apps.config import logging


def log(mensagem):
    ''' Registra uma mensagem no log com timestamp.
    Args:
        mensagem (str): Mensagem a ser registrada no log.'''
    logging.info(mensagem)

# valida se o processo pesquisado (nome_processo) já esta em execução, caso positivo retorna true


def executando(nome_processo):
    ''' Verifica se um processo com o nome especificado está em execução.
    Args:
        nome_processo (str): Nome do processo a ser verificado.
        Returns:
        bool: True se o processo estiver em execução, False caso contrário.'''
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and nome_processo.lower() in proc.info['name'].lower():
            return True
