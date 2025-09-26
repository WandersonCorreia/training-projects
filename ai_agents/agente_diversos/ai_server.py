"""
Aether Architect (Modo Multi-Backend)

Este script conecta a uma API compatível com OpenAIou a uma instância Ollama local
para gerar um site ao vivo.

--- CONFIGURAÇÃO ---
Instale a biblioteca necessária para o seu backend escolhido:
- Para OpenAI: pip install openai
- Para Ollama: pip install ollama

--- USO ---
Você deve especificar um backend ('openai' ou 'ollama') e um modelo.

# Exemplo para OLLAMA:
python ai_server.py ollama --model llama3

# Exemplo para compatível com OpenAI(ex: LM Studio):
python ai_server.py openai --model "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"
"""
import http.server
import socketserver
import os
import argparse
import re
from urllib.parse import urlparse, parse_qs

# Importa bibliotecas condicionalmente
try:
    import openai
except ImportError:
    openai = None
try:
    import ollama
except ImportError:
    ollama = None

# --- 1. PROMPT DE SISTEMA DETALHADO E ULTRA-ESTRITO ---
SYSTEM_PROMPT_BRAND_CUSTODIAN = """
Você é The Brand Custodian, um desenvolvedor front-end de IA especializado. Seu único propósito é construir e manter o site oficial de uma empresa específica e predefinida. Você deve garantir que cada pedaço de conteúdo, cada escolha de design e cada interação que você cria esteja perfeitamente alinhado com a identidade e a história detalhadas da marca fornecidas abaixo. Seu objetivo é consistência e representação fiel.

---
### 1. O CLIENTE: Terranexa (Marca e História)
*   **Nome da Empresa:** **Terranexa**
*   **Fundadores:** Dr. Aris Thorne (biólogo visionário), Lena Petrova (engenheira de sistemas pragmática).
*   **Fundada:** 2019
*   **História de Origem:** Se conheceram em uma conferência de tecnologia climática, frustrados com soluções que tratavam a natureza como um recurso. Esboçaram o conceito "Symbiotic Grid" em um guardanapo.
*   **Missão:** Criar ecossistemas autossustentáveis, harmonizando tecnologia com a natureza.
*   **Visão:** Um mundo onde ambientes urbanos e naturais prosperam em perfeita simbiose.
*   **Princípios Fundamentais:** 1. Design Simbiótico, 2. Transparência Radical (dados de código aberto), 3. Resiliência de Longo Prazo.
*   **Tecnologias Essenciais:** Sensores biodegradáveis, gerenciamento de recursos baseado em IA, agricultura vertical urbana, captação de umidade atmosférica.

---
### 2. REGRAS ESTRUTURAIS OBRIGATÓRIAS
**A. Barra de Navegação Fixa:**
*   Uma única barra de navegação fixa na parte superior da janela de visualização.
*   DEVE conter estes 5 links em ordem: Home, Nossa Tecnologia, Sustentabilidade, Sobre Nós, Contato. (Use links de consulta adequados: /?prompt=...).
**B. Ano de Copyright:**
*   Se existir um rodapé, o ano de copyright DEVE ser **2025**.

---
### 3. DIRETIVAS TÉCNICAS E CRIATIVAS
**A. Mandato Estrito de Arquivo Único (CRÍTICO):**
*   Sua resposta inteira **DEVE** ser um único arquivo HTML.
*   Você **NÃO DEVE** sob nenhuma circunstância vincular a arquivos externos. Isso significa especificamente **SEM tags `<link rel="stylesheet" ...>` e SEM tags `<script src="..."></script>` .**
*   Todo CSS **DEVE** ser colocado dentro de uma única tag `<style>` dentro da tag `<head>`HTML.
*   Todo JavaScript **DEVE** ser colocado dentro de uma tag `<script>` , de preferência antes da tag `</body>` de fechamento.

**B. Sem Sintaxe Markdown (Estritamente Aplicado):**
*   Você **NÃO DEVE** usar nenhuma sintaxe Markdown. Use tags HTML para toda a formatação (`<em>`, `<strong>`, `<h1>`, `<ul>`, etc.).

**C. Design Visual:**
*   O estilo deve estar alinhado com a marca Terranexa: inovador, orgânico, limpo, confiável.
"""

# Globais que serão configurados por argumentos de linha de comando
CLIENTE = None
MODELO_NOME = None
AI_BACKEND = None

# --- MANIPULADOR DO SERVIDOR WEB ---


class AIWebsiteHandler(http.server.BaseHTTPRequestHandler):
    BLOCKED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif',
                          '.svg', '.ico', '.css', '.js', '.woff', '.woff2', '.ttf')

    def do_GET(self):
        global CLIENTE, MODELO_NOME, AI_BACKEND
        try:
            parsed_url = urlparse(self.path)
            path_component = parsed_url.path.lower()

            if path_component.endswith(self.BLOCKED_EXTENSIONS):
                self.send_error(404, "Arquivo Não Encontrado")
                return

            if not CLIENTE:
                self.send_error(503, "Serviço de IA Não Configurado")
                return

            query_components = parse_qs(parsed_url.query)
            user_prompt = query_components.get("prompt", [None])[0]

            if not user_prompt:
                user_prompt = "Gere a página inicial para a Terranexa. Ela deve ter uma seção de herói forte que apresente a visão e a missão da empresa com base em sua história principal."

            print(
                f"\n🚀 Recebida solicitação de página válida para o backend '{AI_BACKEND}': {self.path}")
            print(
                f"💬 Enviando prompt para o modelo '{MODELO_NOME}': '{user_prompt}'")

            messages = [{"role": "system", "content": SYSTEM_PROMPT_BRAND_CUSTODIAN}, {
                "role": "user", "content": user_prompt}]

            raw_content = None
            # --- CHAMADA DE API DE BACKEND DUPLO ---
            if AI_BACKEND == 'openai':
                response = CLIENTE.chat.completions.create(
                    model=MODELO_NOME, messages=messages, temperature=0.7)
                raw_content = response.choices[0].message.content
            elif AI_BACKEND == 'ollama':
                response = CLIENTE.chat(model=MODELO_NOME, messages=messages)
                raw_content = response['message']['content']

            # --- LIMPEZA INTELIGENTE DE CONTEÚDO ---
            html_content = ""
            if isinstance(raw_content, str):
                html_content = raw_content
            elif isinstance(raw_content, dict) and 'String' in raw_content:
                html_content = raw_content['String']
            else:
                html_content = str(raw_content)

            html_content = re.sub(r'<think>.*?</think>',
                                  '', html_content, flags=re.DOTALL).strip()
            if html_content.startswith("```html"):
                html_content = html_content[7:-3].strip()
            elif html_content.startswith("```"):
                html_content = html_content[3:-3].strip()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
            print("✅ Página gerada e servida com sucesso.")

        except BrokenPipeError:
            print(
                f"🔶 [BrokenPipeError] Cliente desconectado para o caminho: {self.path}. Solicitação abortada.")
        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado: {e}")
            try:
                self.send_error(500, f"Erro do Servidor: {e}")
            except Exception as e2:
                print(
                    f"🔴 Ocorreu um erro adicional ao lidar com o erro inicial: {e2}")


# --- BLOCO DE EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aether Architect: Servidor Web de IA Multi-Backend", formatter_class=argparse.RawTextHelpFormatter)

    # Escolha do backend
    parser.add_argument('backend', choices=[
                        'openai', 'ollama'], help='O backend de IA a ser usado.')

    # Argumentos comuns
    parser.add_argument("--model", type=str, required=True,
                        help="O identificador do modelo a ser usado (por exemplo, 'llama3').")
    parser.add_argument("--port", type=int, default=8000,
                        help="Porta para executar o servidor web.")

    # Argumentos específicos do backend
    openai_group = parser.add_argument_group(
        'Opções OpenAI (para o backend "openai")')
    openai_group.add_argument("--api-base", type=str, default="http://localhost:1234/v1",
                              help="URL base do servidor de API compatível com OpenAI.")
    openai_group.add_argument(
        "--api-key", type=str, default="not-needed", help="Chave de API para o serviço.")

    ollama_group = parser.add_argument_group(
        'Opções Ollama (para o backend "ollama")')
    ollama_group.add_argument("--ollama-host", type=str, default="http://127.0.0.1:11434",
                              help="Endereço do host para o servidor Ollama.")

    args = parser.parse_args()

    PORT = args.port
    MODELO_NOME = args.model
    AI_BACKEND = args.backend

    # --- INICIALIZAÇÃO DO CLIENTE ---
    if AI_BACKEND == 'openai':
        if not openai:
            print("🔴 Backend 'openai' escolhido, mas a biblioteca não foi encontrada. Execute 'pip install openai'")
            exit(1)
        try:
            print(
                f"🔗 Conectando ao servidor compatível com OpenAIem: {args.api_base}")
            CLIENTE = openai.OpenAI(
                base_url=args.api_base, api_key=args.api_key)
            print(
                f"✅ Cliente OpenAI configurado para usar o modelo: '{MODELO_NOME}'")
        except Exception as e:
            print(f"🔴 Falha ao configurar o cliente OpenAI : {e}")
            exit(1)

    elif AI_BACKEND == 'ollama':
        if not ollama:
            print("🔴 Backend 'ollama' escolhido, mas a biblioteca não foi encontrada. Execute 'pip install ollama'")
            exit(1)
        try:
            print(f"🔗 Conectando ao servidor Ollama em: {args.ollama_host}")
            CLIENTE = ollama.Client(host=args.ollama_host)
            # Verifique a conexão listando os modelos locais
            CLIENTE.list()
            print(
                f"✅ Cliente Ollama configurado para usar o modelo: '{MODELO_NOME}'")
        except Exception as e:
            print(f"🔴 Falha ao conectar ao servidor Ollama. Ele está rodando?")
            print(f"   Erro: {e}")
            exit(1)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), AIWebsiteHandler) as httpd:
        print(f"\n✨ The Brand Custodian está no ar em http://localhost:{PORT}")
        print(
            f"   (Usando o backend '{AI_BACKEND}' com o modelo '{MODELO_NOME}')")
        print("   (Pressione Ctrl+C para parar o servidor)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n desligando o servidor.")
            httpd.shutdown()
