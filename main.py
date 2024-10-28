import streamlit as st
import os
import configparser
import speech_recognition as sr
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from pydub import AudioSegment
import PyPDF2

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content":prompt}
        ]
    )

    return response.choices[0].message.content

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

condition = 0

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
        response = ask_gpt(prompt)
        
        with st.expander("Transcrição completa da ordem de serviço:", expanded=False):
            st.write(orders)

        st.write("Resumo da ordem de serviço:")
        st.write(response)

        # Gerando ordem de serviço para download
        pdf_path="userdata/service_order.pdf"
        create_pdf(pdf_path, response)

        #f.write(orders)
        with open(pdf_path, "rb") as f:
            st.download_button("Baixar ordem de serviço", f, file_name="service_order.pdf")

        condition = 1

# Checando se o botão passado foi ativado
if(condition == 1):
    uploaded_pdfs = st.file_uploader("Insira manuais para conserto das peças acima:", type=['pdf'], accept_multiple_files=True)
else:
    uploaded_pdfs = 0

if uploaded_pdfs:  
    detected_text = ''

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
    prepend2 = "Procure nesse manual como consertar as máquinas descritas na lista com o máximo de informação possível"
    prompt2 = prepend2 + detected_text  + response

    # Resposta do chatgpt
    response2 = ask_gpt(prompt2)

    # Mostrando a Resposta
    st.write("Explicações de Conserto das Peças anteriorimente pedidas:")
    st.write(response2)
