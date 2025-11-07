# 🕒 Automação de Marcação de Ponto

Este projeto foi desenvolvido com o objetivo de automatizar a marcação do ponto eletrônico na empresa onde trabalho. Além disso, serve como exercício prático para o meu treinamento em Python, incorporando funcionalidades adicionais como abertura de programas, manipulação de arquivos json, controle de execução por período do dia e envio de SMS.

## 📁 Estrutura do Projeto
.
├── everyday.py              # Script principal que executa a rotina de automação
├── data/
│   ├── list_programs.json   # Lista de programas a serem abertos
│   ├── controle_execucao.json  # Registro de execuções por período
│   └── automacao.log        # Arquivo de log gerado pela automação
|   └── sms.log              # Arquivo de configuacao do SMS
└── apps/
|   ├── navegador.py         # Automação via Selenium para marcar o ponto
|   ├── helpers.py           # Funções auxiliares: logging e verificação de processos
|   ├── controle.py          # Controle de execução por período
|   ├── diversos.py          # Abertura de programas com base em arquivo JSON
|   └── config.py            # Configuração do sistema de logging
|   └── sms.py               # envio de SMS com resultado da automacao 

## ⚙️ Funcionalidades

- ✅ Marcação de ponto eletrônico via automação com Selenium
- ✅ Abertura de programas essenciais no início do expediente
- ✅ Controle de execução para evitar duplicidade por período (manhã, tarde, noite)
- ✅ Log de atividades com timestamp
- ✅ Verificação de processos ativos para evitar múltiplas execuções simultâneas
- ✅ Leitura dinâmica de programas a abrir via arquivo JSON

## 🧠 Lógica de Execução

O script `everyday.py` identifica o período atual com base no horário e executa a rotina correspondente:

- **Manhã (07:00 às 11:59)**: abre programas e marca o ponto
- **Tarde (12:00 às 18:00)**: apenas marca o ponto
- **Noite (18:01 às 22:00)**: apenas marca o ponto
- Fora desses horários, nenhuma ação é tomada

## 🌐 Automação com Selenium

O módulo `navegador.py` utiliza o Selenium para:

1. Abrir o navegador (Edge, Chrome ou Firefox)
2. Acessar o portal RH da empresa
3. Clicar no botão "Marcar Ponto"
4. Trocar o foco para a nova janela/modal
5. Confirmar a marcação do ponto

Em caso de erro, o sistema registra no log e encerra o navegador com segurança.

## 🧰 Utilitários

### helpers.py

- `log(mensagem)`: registra mensagens com timestamp no log
- `executando(nome_processo)`: verifica se um processo está ativo no sistema usando `psutil`

### diversos.py

- `ler_dados_json()`: lê os programas a abrir do arquivo `list_programs.json`
- `abrir_programa(nome_programa)`: abre o programa se não estiver em execução
- `abrir_todos_programas()`: executa todos os programas listados

### controle.py

- `ja_executou(periodo)`: verifica se a rotina já foi executada no dia
- `registrar_execucao(periodo)`: registra a execução da rotina no controle

### config.py

- Configura o sistema de logging para registrar mensagens no arquivo `automacao.log` dentro da pasta `data`

### sms.py
- `ler_dados_json()`: carrega os dados do arquivo `sms.json` execucao da API do twilio
- `envia_sms(mensagem)`: envia mensagem de texto, via twilio, com o resultado do processamento

## 🚀 Como Executar

Certifique-se de que todas as dependências estejam instaladas e execute o script principal:

```bash
python everyday.py

A automação pode ser agendada via agendador de tarefas do sistema operacional para rodar nos horários desejados.
ou pode-se gerar um executável.
🛠️ Tecnologias Utilizadas

Python 3.x
Selenium WebDriver
psutil
twilio
subprocess
Módulos padrão (datetime, time, json, os, logging)

👤 Autor
Wanderson de Correia
Custom Software Engineering Assoc Mgr
Belo Horizonte, MG

Obs: os dados da conta do twilio e o endereço WEB do relógio foram omitidos. 
     Por ser uma aplicação expecífica, a navegação WEB deve ser ajustada para cada caso.