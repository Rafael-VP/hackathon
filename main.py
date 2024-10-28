import streamlit as st
import os
import configparser
import speech_recognition as sr
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from pydub import AudioSegment

def create_pdf(filename, text, font_name="Helvetica", font_size=12, margin=100):
    # Define the canvas
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set font and calculate line height
    c.setFont(font_name, font_size)
    line_height = font_size + 2  # Space between lines

    # Calculate maximum text width (page width minus margins)
    max_text_width = width - 2 * margin

    # Split text into lines that fit within the max width
    x, y = margin, height - margin
    for paragraph in text.splitlines():
        # Split paragraph into lines that fit within max_text_width
        words = paragraph.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            # Check if line width exceeds max_text_width
            if c.stringWidth(test_line, font_name, font_size) <= max_text_width:
                line = test_line
            else:
                # Draw current line and start a new one
                c.drawString(x, y, line)
                y -= line_height
                line = word
        # Draw any remaining text in line
        if line:
            c.drawString(x, y, line)
            y -= line_height

    # Save the PDF
    c.save()

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
        
        with st.expander("Transcrição completa da ordem de serviço:", expanded=False):
            st.write(orders)

        st.write("Resumo da ordem de serviço:")
        st.write(response.choices[0].message.content)

        # Gerando ordem de serviço para download
        pdf_path="userdata/service_order.pdf"
        create_pdf(pdf_path, response.choices[0].message.content)

        #f.write(orders)
        with open(pdf_path, "rb") as f:
            st.download_button("Baixar ordem de serviço", f, filename="service_order.pdf")

        st.write(response.choices[0].message.content)
