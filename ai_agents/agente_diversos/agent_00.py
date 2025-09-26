import json
import requests
from datetime import datetime
import openai
import base64
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis do .env


class AgenteSimples:
    def __init__(self, api_key=None):
        """
        Inicializa o agente com suas ferramentas e memória
        """
        self.api_key = os.getenv("OPENAI_API_KEY")

        if self.api_key:
            self.openai_client = openai.OpenAI(api_key=self.api_key)
        else:
            self.openai_client = None
        self.memoria = []  # Histórico de conversas
        self.ferramentas = {
            "buscar_cep": self.buscar_cep,
            "calcular": self.calcular,
            "obter_data_hora": self.obter_data_hora,
            "validar_sql": self.validar_sql
        }

    def buscar_cep(self, cep):
        """Ferramenta para buscar informações de CEP"""
        try:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "erro" not in data:
                    return f"CEP {cep}: {data['logradouro']}, {data['bairro']}, {data['localidade']}-{data['uf']}"
                else:
                    return f"CEP {cep} não encontrado"
            else:
                return "Erro ao consultar CEP"
        except Exception as e:
            return f"Erro: {str(e)}"

    def calcular(self, expressao):
        """Ferramenta para realizar cálculos simples"""
        try:
            # Validação básica de segurança
            caracteres_permitidos = "0123456789+-*/()., "
            if all(c in caracteres_permitidos for c in expressao):
                resultado = eval(expressao)
                return f"Resultado: {resultado}"
            else:
                return "Expressão contém caracteres não permitidos"
        except Exception as e:
            return f"Erro no cálculo: {str(e)}"

    def obter_data_hora(self):
        """Ferramenta para obter data e hora atual"""
        agora = datetime.now()
        return f"Data e hora atual: {agora.strftime('%d/%m/%Y %H:%M:%S')}"

    def validar_sql(self, caminho_sql):
        """Função para ler um arquivo SQL e submeter o código para validação usando GPT-4o."""
        if not self.openai_client:
            return "Erro: A chave de API da OpenAI não foi configurada."

        try:
            # 1. Lê o conteúdo do arquivo SQL como texto (modo 'r')
            with open(caminho_sql, "r", encoding="utf-8") as f:
                codigo_sql = f.read()

            # 2. Cria o prompt de validação para a LLM
            prompt = f"""
            Você é um especialista em validação de código SQL. Analise o seguinte código SQL com base nos seguintes critérios:
            
            1.  **Sintaxe:** Verifique se há erros de sintaxe (palavras-chave incorretas, pontuação, etc.).
            2.  **Boas Práticas:** Avalie se o código segue boas práticas de escrita, como uso de aliases, formatação e legibilidade.
            3.  **Otimização:** Identifique possíveis gargalos de desempenho (ex: SELECT *, uso excessivo de JOINs, subqueries ineficientes).
            4.  **Segurança:** Aponte vulnerabilidades de segurança (ex: injeção de SQL).
            
            Retorne um relatório claro e conciso, listando os problemas encontrados e sugerindo soluções para cada um. Se o código estiver correto e seguir as boas práticas, apenas retorne "Código SQL validado com sucesso. Nenhuma melhoria significativa necessária."
            
            ---
            
            Código SQL a ser analisado:
            {codigo_sql}
            """

            # 3. Faz a chamada à API com a mensagem de texto
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500  # Aumentado para um relatório mais detalhado
            )

            conteudo = response.choices[0].message.content
            return f"Relatório de Validação SQL:\n\n{conteudo}"

        except FileNotFoundError:
            return f"Erro: Arquivo não encontrado no caminho: {caminho_sql}"
        except Exception as e:
            return f"Erro na OCRização: {str(e)}. Verifique sua chave de API."

    def analisar_intent(self, mensagem):
        """
        Analisa a intenção do usuário e decide qual ferramenta usar
        Em um cenário real, isso seria feito por um LLM
        """
        mensagem_lower = mensagem.lower()

        # Detecção de CEP (formato simples)
        if "cep" in mensagem_lower or any(char.isdigit() for char in mensagem if len([c for c in mensagem if c.isdigit()]) == 8):
            cep = ''.join(filter(str.isdigit, mensagem))
            if len(cep) == 8:
                return "buscar_cep", cep

        # Detecção de cálculo
        if any(op in mensagem for op in ["+", "-", "*", "/", "calcul", "soma", "multiplicação"]):
            # Extrai números e operadores da mensagem
            import re
            expressao = re.findall(r'[\d+\-*/().]+', mensagem)
            if expressao:
                return "calcular", ''.join(expressao)

        # Detecção de solicitação de data/hora
        if any(palavra in mensagem_lower for palavra in ["hora", "data", "agora", "hoje", "tempo"]):
            return "obter_data_hora", None

        # Detecção de OCR por palavras-chave e extensão de arquivo
        if any(p in mensagem_lower for p in ["valide", "validar", "verificar"]):
            partes = mensagem.split()
            for parte in partes:
                if parte.endswith(('.sql', '.sqlx')):
                    return "validar_sql", parte

        return None, None

    def processar_mensagem(self, mensagem):
        """
        Processa uma mensagem do usuário
        """
        # Adiciona à memória
        self.memoria.append(
            {"tipo": "usuario", "conteudo": mensagem, "timestamp": datetime.now()})

        # Analisa intenção
        ferramenta, parametro = self.analisar_intent(mensagem)

        if ferramenta and ferramenta in self.ferramentas:
            # Executa a ferramenta
            if parametro:
                resultado = self.ferramentas[ferramenta](parametro)
            else:
                resultado = self.ferramentas[ferramenta]()

            resposta = f"🤖 Executei a ferramenta '{ferramenta}': {resultado}"
        else:
            # Resposta padrão quando não identifica uma ferramenta específica
            resposta = f"🤖 Recebi sua mensagem: '{mensagem}'. Posso ajudar com consulta de CEP, cálculos simples ou informar data/hora atual."

        # Adiciona resposta à memória
        self.memoria.append(
            {"tipo": "agente", "conteudo": resposta, "timestamp": datetime.now()})

        return resposta

    def mostrar_memoria(self):
        """Exibe o histórico da conversa"""
        print("\n📚 HISTÓRICO DA CONVERSA:")
        print("-" * 50)
        for entrada in self.memoria:
            tipo = "👤 USUÁRIO" if entrada["tipo"] == "usuario" else "🤖 AGENTE"
            print(f"{tipo}: {entrada['conteudo']}")
            print(f"   ⏰ {entrada['timestamp'].strftime('%H:%M:%S')}")
            print()


def main():
    """Função principal para demonstração"""
    print("🚀 AGENTE SIMPLES - DEMONSTRAÇÃO PRÁTICA")
    print("=" * 50)
    print("Funcionalidades disponíveis:")
    print("• Consulta de CEP (digite um CEP de 8 dígitos)")
    print("• Cálculos simples (ex: 10 + 5 * 2)")
    print("• Data/hora atual (pergunte 'que horas são?')")
    print("• Validacao de SQL (ex: 'valide script.sql')")
    print("• Digite 'memoria' para ver o histórico")
    print("• Digite 'sair' para encerrar")
    print("-" * 50)

    # Inicializa o agente
    agente = AgenteSimples()

    while True:
        try:
            mensagem = input("\n👤 Você: ").strip()

            if mensagem.lower() == 'sair':
                print("👋 Encerrando o agente. Até logo!")
                break
            elif mensagem.lower() == 'memoria':
                agente.mostrar_memoria()
                continue
            elif not mensagem:
                continue

            # Processa a mensagem
            resposta = agente.processar_mensagem(mensagem)
            print(resposta)

        except KeyboardInterrupt:
            print("\n\n👋 Agente interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro: {str(e)}")


if __name__ == "__main__":  # Essa linha é usada para controlar a execução de um script Python. Ela verifica se o arquivo está sendo executado diretamente ou se está sendo importado como módulo em outro script.
    main()
