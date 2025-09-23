# Exemplo de uso do yfinance para baixar dados
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
# Baixar dados históricos de uma ação (exemplo: PETR4.SA)
ticker = "PETR4.SA"
data = yf.download(ticker, start="2020-01-01", end="2023-01-01")
# Exibir as primeiras linhas do DataFrame
print(data.head())
# Plotar o preço de fechamento
data['Close'].plot(title=f'Preço de Fechamento de {ticker}')    
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento (R$)')
plt.show()
# Calcular retornos diários e volatilidade
data['Retorno Diário'] = data['Close'].pct_change()     
volatilidade = data['Retorno Diário'].std() * (252**0.5)  # Anualizada
print(f'Volatilidade Anualizada: {volatilidade:.2%}') 