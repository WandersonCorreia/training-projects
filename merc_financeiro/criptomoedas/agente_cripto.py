import requests
import json
from datetime import datetime


class AgenteCripto:
    def __init__(self):
        # usando a api da coingecko, recebe uma lista de moedas de interesse
        self.api_base = "https://api.coingecko.com/api/v3"
        self.moedas_interesse = ["bitcoin", "ethereum", "cardano"]

    def perceber_mercado(self):
        """Coleta dados atuais do mercado"""
        print("🔍 PERCEBENDO: Coletando dados do mercado...")

        dados = {}

        # faz a pesquisa para cada uma das moedas informadas em moedas_interesse
        for moeda in self.moedas_interesse:
            url = f"{self.api_base}/simple/price"
            params = {
                'ids': moeda,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }

            try:
                response = requests.get(url, params=params)
                dados[moeda] = response.json()[moeda]
                print(f"   ✅ {moeda}: ${dados[moeda]['usd']}")
            except Exception as e:
                print(f"   ❌ Erro ao buscar {moeda}: {e}")

        return dados

    def decidir_acoes(self, dados_mercado):
        """Analisa dados e decide ações"""
        print("🧠 DECIDINDO: Analisando oportunidades...")

        acoes = []
        for moeda, info in dados_mercado.items():
            preco = info['usd']
            variacao_24h = info['usd_24h_change']

            if variacao_24h > 5:
                acoes.append({
                    'tipo': 'ALERTA_ALTA',
                    'moeda': moeda,
                    'preco': preco,
                    'variacao': variacao_24h
                })
            elif variacao_24h < -5:
                acoes.append({
                    'tipo': 'OPORTUNIDADE_COMPRA',
                    'moeda': moeda,
                    'preco': preco,
                    'variacao': variacao_24h
                })

        return acoes

    def executar_acoes(self, acoes):
        """Executa as ações determinadas"""
        print("⚡ AGINDO: Executando ações...")

        for acao in acoes:
            if acao['tipo'] == 'ALERTA_ALTA':
                self.enviar_alerta_telegram(
                    f"🚀 {acao['moeda'].upper()} subiu {acao['variacao']:.2f}% "
                    f"nas últimas 24h! Preço atual: ${acao['preco']}"
                )
            elif acao['tipo'] == 'OPORTUNIDADE_COMPRA':
                self.enviar_alerta_telegram(
                    f"📉 {acao['moeda'].upper()} caiu {abs(acao['variacao']):.2f}% "
                    f"- possível oportunidade de compra. Preço: ${acao['preco']}"
                )

    def enviar_alerta_telegram(self, mensagem):
        """Simula envio de alerta"""
        print(f"📱 TELEGRAM: {mensagem}")
        # Em produção, usaria API do Telegram

    def executar_ciclo(self):
        """Executa um ciclo completo do agente"""
        print(f"\n{'='*50}")
        print(f"⏰ CICLO INICIADO - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*50}")

        # Ciclo completo do agente
        dados = self.perceber_mercado()
        acoes = self.decidir_acoes(dados)
        self.executar_acoes(acoes)

        print("✅ CICLO CONCLUÍDO\n")


# Execução da demonstração
if __name__ == "__main__":
    agente = AgenteCripto()
    agente.executar_ciclo()
