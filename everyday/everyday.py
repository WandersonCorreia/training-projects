from apps.navegador import marcar_ponto
from apps.helpers import log
from apps.controle import ja_executou, registrar_execucao
from apps.diversos import abrir_todos_programas
from apps.sms import envia_sms
from datetime import datetime


def executar_manha(data):
    ''' Executa a rotina da manhã: abre programas e marca ponto.'''

    log("Executando rotina da manhã...")
    abrir_todos_programas()
    marcar_ponto()

    log("Rotina da Manhã Concluida.")
    envia_sms(f"{data} Rotina da Manhã Concluída com sucesso.")


def executar_tarde(data):
    ''' Executa a rotina da tarde: marca ponto.'''

    log("Executando rotina da tarde...")
    marcar_ponto()

    log("Rotina da Tarde Concluída.")
    envia_sms(f"{data} Rotina da Tarde Concluída com sucesso.")


def main():
    ''' Função principal que determina o período do dia e executa a rotina correspondente.'''
    agora = datetime.now()
    data = datetime.now().strftime("%Y-%m-%d")

    log(f"Iniciando automação...")
    minutos_totais = agora.hour * 60 + agora.minute

    if 420 <= minutos_totais <= 719:  # Antes do meio dia 07:00 às 11:59
        periodo = "manha"
    elif 720 <= minutos_totais <= 1080:  # 12:00 = 720, 18:00 = 1080
        periodo = "tarde"
    elif 1081 <= minutos_totais <= 1320:  # 18:01 = 1081, 22:00 = 1320
        periodo = "noite"
    else:
        periodo = None

    if periodo == 'manha' and not ja_executou(periodo):
        log(f"Executando automação do período: {periodo}")
        executar_manha(data)
        registrar_execucao(periodo)
    elif periodo == 'tarde' and not ja_executou(periodo):
        log(f"Executando automação do período: {periodo}")
        executar_tarde(data)
        registrar_execucao(periodo)
    elif periodo == 'noite' and not ja_executou(periodo):
        log(f"Executando automação do período: {periodo}")
        executar_tarde(data)
        registrar_execucao(periodo)
    else:
        log(f"Automação já executada ou fora do horário.")
        envia_sms(f"{data} Automação já executada ou fora do horário.")

    log(f"Fim da automação.\n")


if __name__ == "__main__":
    main()
