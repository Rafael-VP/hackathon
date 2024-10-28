import streamlit as st
import os
import configparser
import speech_recognition as sr
from openai import OpenAI

config = configparser.ConfigParser()
config.read("config.ini")

r = sr.Recognizer()

client = OpenAI()
prepend = "Resuma o seguinte texto em uma lista de tarefas:\n "

st.title("Ordem de serviço:")
uploaded_files = st.file_uploader("Arquivos de áudio:", type=['ogg', 'wav'], accept_multiple_files=True)

for uploaded_file in uploaded_files:
        path = os.path.join("userdata", uploaded_file.name)
        with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
        print(path)

        file_audio = sr.AudioFile(path)

        with file_audio as source:
            audio_text = r.record(source)

        #st.write(type(audio_text))
        orders = r.recognize_google(audio_text, language="pt-BR")
        prompt = prepend + orders

        response = client.chat.completions.create(
            model="gpt-4o",
            api_key=config['Main']['gpt_key'],
            messages=[
                {"role": "user", "content":prompt}
            ]
        )
