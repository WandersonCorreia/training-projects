🤖 AgenteSimples
Um agente interativo em Python com funcionalidades básicas como consulta de CEP, cálculos simples, obtenção de data/hora atual e validação de scripts SQL usando a API da OpenAI.

🚀 Funcionalidades
🔍 Consulta de CEP via ViaCEP
➗ Cálculos matemáticos simples
🕒 Data e hora atual
🧠 Validação de scripts SQL com análise de sintaxe, boas práticas, otimização e segurança usando GPT-4o
🧾 Histórico de conversa armazenado em memória
⚙️ Requisitos
Python 3.8+
Biblioteca python-dotenv para carregar variáveis de ambiente
Biblioteca openai para integração com a API da OpenAI
Conexão com a internet para chamadas à API e consulta de CEP
📦 Instalação
Clone o repositório ou copie os arquivos do projeto.
Instale as dependências:



Shell
pip install openai python-dotenv requests

Crie um arquivo .env na raiz do projeto com sua chave da OpenAI:



Shell
env isn’t fully supported. Syntax highlighting is based on Shell.

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
▶️ Como usar
Execute o script principal:




Shell
python agente_simples.py
Você poderá interagir com o agente digitando mensagens como:

01001000 → Consulta de CEP
10 + 5 * 2 → Cálculo
Que horas são? → Data/hora atual
Valide meu_script.sql → Validação de SQL
memoria → Exibe o histórico da conversa
sair → Encerra o agente
📁 Estrutura do Projeto
agente_simples.py
.env
README.md
🧠 Observações
A validação de SQL depende da chave da OpenAI estar corretamente configurada.
O agente usa uma lógica simples para detectar intenções com base em palavras-chave.