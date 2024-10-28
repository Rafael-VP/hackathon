import streamlit as st
import os
import configparser
import speech_recognition as sr
from pydub import AudioSegment
from openai import OpenAI
from modules.pdf import create_pdf
import PyPDF2


def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content":prompt}
        ]
    )

    return response.choices[0].message.content


st.set_page_config(
    page_title="Tractian",
    page_icon="data/tractian.jpg",  # You can replace with a favicon path or emoji
    #initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        border: 5px inset #0468f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px; /* Added space between elements */
        display: flex; /* Use flexbox for layout */
        justify-content: center; /* Center items horizontally */
        align-items: center; /* Center items vertically */
    }
    .logo {
        margin-right: 20px; /* Space between logo and title */
    }
    .stFileUploader {
        background-color: #282434;
        border: 5px inset #0468f6;
        border-radius: 10px;
        padding: 10px;
        margin-top: 20px; /* Added space between elements */
    }
    .stFileUploader p {
        color: #0468f6;
    }
    .css-1d391kg {  /* The title class */
        text-align: center;
        color: #0468f6;
    }
    </style>
    <div class="main">
        <img class="logo" src="https://yt3.googleusercontent.com/RcyFXjXXaec7Bc_PS8pUtmlrJP28XxqeSBp0oGHLjEE9bHhYxiYr_FeDVQSOmg4G3L3uET0B6ao=s900-c-k-c0x00ffffff-no-rj" alt="Logo" style="width:100px;height:auto;">
        <div class="css-1d391kg">
            <h1>Hackathon Tractian 2024</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>-> MAINTENANCE COMPANION <-</h1>", unsafe_allow_html=True)


config = configparser.ConfigParser()
config.read("config.ini")

r = sr.Recognizer()

client = OpenAI(api_key=config['Main']['gpt_key'])
prepend = "Resuma o seguinte texto em uma lista de tarefas:\n "

uploaded_files = st.file_uploader("Arquivos de áudio:", type=['ogg'], accept_multiple_files=True)


pressed = 0
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Salvando arquivo ogg
        path = os.path.join("userdata", uploaded_file.name)
        with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())

        # Convertendo arquivo para WAV
        audio = AudioSegment.from_ogg(path)
        path = path.replace("ogg", "wav")
        audio.export(path, format="wav")

        # Convertendo áudio para texto
        file_audio = sr.AudioFile(path)

        with file_audio as source:
            audio_text = r.record(source)

        st.write("Ouvindo áudio...")
        orders = r.recognize_google(audio_text, language="pt-BR")
        prompt = prepend + orders

        # Resumindo áudio com GPT
        st.write("Interpretando ordem de serviço...")
        response = ask_gpt(prompt)
        
        with st.expander("Transcrição completa da ordem de serviço:", expanded=False):
            st.write(orders)

        st.write("Resumo da ordem de serviço:")
        st.write(response)

        pressed = 1
        uploaded_files.clear()

if pressed:
    order_text = "**# RESUMO:**\n" + response
    uploaded_pdfs = []
    uploaded_pdfs = st.file_uploader("Insira manuais para conserto das peças acima:", type=['pdf'], accept_multiple_files=True)
    detected_text = ''

    if uploaded_pdfs:
        st.write("Lendo PDF...")
        for pdf in uploaded_pdfs:
            # Salvando os arquivos pdf
            path = os.path.join("userdata", pdf.name)
            with open(path, "wb") as f:
                f.write(pdf.getvalue())

            # Abrindo os arquivos pdf para leitura
            with open(path, 'rb') as pdf_file_obj:
                pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
                num_pages = len(pdf_reader.pages)

                # Transformando pdf em texto
                for page_num in range(num_pages):
                    page_obj = pdf_reader.pages[page_num]
                    detected_text += page_obj.extract_text() + '\n\n'

        # Preparando o prompt
        st.write("Interpretando texto...")
        prepend2 = "Procure nesse manual como consertar as máquinas descritas na lista com o máximo de informação possível"
        prompt = prepend2 + detected_text + response

        # Resposta do chatgpt
        response = ask_gpt(prompt)

        # Mostrando a Resposta
        st.write("Explicações de Conserto das Peças anteriorimente pedidas:")
        st.write(response)

        order_text += "\n\n# INSTRUÇÕES COMPLETAS:\n" + response

        # Gerando ordem de serviço para download
        pdf_path="userdata/service_order.pdf"
        create_pdf(pdf_path, order_text)

        #f.write(orders)
        with open(pdf_path, "rb") as f:
            st.download_button("Baixar ordem de serviço", f, file_name="service_order.pdf")
        
        uploaded_pdfs = []

