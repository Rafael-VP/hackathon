import streamlit as st
import os
import configparser
import speech_recognition as sr
from openai import OpenAI
from pydub import AudioSegment

config = configparser.ConfigParser()
config.read("config.ini")

r = sr.Recognizer()

client = OpenAI(api_key=config['Main']['gpt_key'])
prepend = "Resuma o seguinte texto em uma lista de tarefas:\n "

st.title("Ordem de serviço:")
uploaded_files = st.file_uploader("Arquivos de áudio:", type=['ogg', 'wav'], accept_multiple_files=True)

for uploaded_file in uploaded_files:
        # Salvando arquivo ogg
        path = os.path.join("userdata", uploaded_file.name)
        with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
        print(path)

        # Convertendo arquivo para WAV
        audio = AudioSegment.from_ogg(path)
        path = path.replace("ogg", "wav")
        audio.export(path, format="wav")

        # Convertendo áudio para texto
        file_audio = sr.AudioFile(path)

        with file_audio as source:
            audio_text = r.record(source)

        #st.write(type(audio_text))
        st.write("Ouvindo áudio...")
        orders = r.recognize_google(audio_text, language="pt-BR")
        prompt = prepend + orders

        st.write("Interpretando ordem de serviço...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content":prompt}
            ]
        )

        st.write(response.choices[0].message.content)

