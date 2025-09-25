from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import os


def legendar(arq_video, contexto):
    # pegar um arquivo de video e gerar um arquivo de audio.mp3
    # arq_video = "C:\\workplace\\treinamento_python\\training-projects\\ai_agents\\audio_transcript\\doguinho_vida_loca.mp4"    # detalhe, se o arquivo não estiver dentro do projeto é preciso informar o caminho completo do video

    if not os.path.exists(arq_video):
        raise FileNotFoundError(f"Arquivo não encontrado: {arq_video}")

    # separar o nome do arquivo para pegar a extensão de forma dinâmica
    # o split separa o nome por ponto gerando uma lista ["nome_arquivo","extensao_arquivo"]
    ext_arq = arq_video.name.split(".")[1]
    # outra forma de pegar a extensão do arquivo
    ext = os.path.splitext(arq_video.name)[1][1:]

    # pegar o audio do vídeo e gerar um arquivo de audio, com tratamento de erro
    try:
        audio = AudioSegment.from_file(file=arq_video, format=ext_arq)
        audio.export("audio.mp3", format="mp3")

    except Exception as e:
        print(f"Erro ao processar o áudio: {e}")

    load_dotenv()  # carrega as variáveis de ambiente (arquivo .env) com a chave da API da OPENAI
    cliente = OpenAI()

    ''' pode-se passar um prompt para contextualizar o audio para que a IA dê uma resposta melhor
    nos casos de linguagem não formal ou girias, ao enviar no prompt a IA replica na transcrição por exemplo
    se no audio houver a palavra full stack - se não informado pode ser que a IA retorne fullstack junto'''

    # contexto = "este áudio é de um pedido de uma criança de 3 anos, pedindo mais tempo com a familia"
    # foi inserido(recebido no programa principal) no main.py e passado como parametro

    # recomendável abrir arquivos dentro de uma extrutura WHILE para não correr o risco do arquivo ficar aberto
    with open("audio.mp3", "rb") as arquivo:
        # o "rb" é um comando de abertura de leitura com bytes. que é como a IA entende
        transcricao = cliente.audio.transcriptions.create(file=arquivo,
                                                          model="whisper-1",
                                                          language='pt',         # para ajudar o Modelo informar a linguagem do audio
                                                          response_format="srt",  # formato padrão de legendas pode ser txt ou outros
                                                          prompt=contexto)

    ''' gravando a legenda em um arquivo srt, 
        importante: a legenda em portugues contém caracteres especiais ( exemplo acentuações) observar que o 
        encoding padrão do python não aceita caracteres especiais, por isso a necessidade de mudar o encoding   
    '''

    with open("legenda.srt", "w", encoding="utf-8") as arquivo_legenda:
        arquivo_legenda.write(transcricao)

    return transcricao
