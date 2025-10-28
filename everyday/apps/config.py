import logging
import os

# busca o caminho para salvar o arquivo de log
# Diretório raiz do projeto (onde o script é executado)
project_root = os.getcwd()
log_path = os.path.join(project_root, 'data', 'automacao.log')


# Garante que diretório existe
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# Configura o log para salvar em arquivo
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
