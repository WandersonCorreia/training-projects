from legendador import legendar
import streamlit as st


def meu_app():
    st.header("hash legendador", divider=True)
    st.markdown("#### Gere a Legenda de qualquer Audio ou Video")

    contexto = st.text_input(label="Dê algum contexto para ajudar a legenda")
    arquivo = st.file_uploader(
        label="Selecione o Video.mp4 ou Audio.mp3 para legendar", type=["mp4", "mp3"])

    if arquivo:
        legenda = legendar(arquivo, contexto)
        st.write(f"Arquivo {arquivo.name} legendado com sucesso")
        st.write(legenda)


if __name__ == "__main__":  # Essa linha é usada para controlar a execução de um script Python. Ela verifica se o arquivo está sendo executado diretamente ou se está sendo importado como módulo em outro script.
    meu_app()

# a execução de um programa com streamlit é feito pela linha de comando: streamlit run + nome do arquivo.py
