import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("GIT-HUBC")
client1.on_message = on_message



st.title("INTERFACES MULTIMODALES")
st.subheader("CONTROL POR VOZ")

st.markdown("""
    <style>
    /* Fondo degradado */
    .stApp {
        background: linear-gradient(135deg, #f0f8ff, #e6e6fa);
        font-family: 'Segoe UI', sans-serif;
        color: #2d2d2d;
    }

    /* Títulos con sombra */
    h1, h2 {
        color: #4b0082;
        text-shadow: 1px 1px 5px rgba(75, 0, 130, 0.2);
    }

    /* Botón Bokeh */
    button {
        background: linear-gradient(90deg, #ff7f50, #ff6347);
        color: white !important;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s ease;
    }
    button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 99, 71, 0.4);
    }

    /* Imagen centrada */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }

    /* Texto explicativo */
    p, label, span {
        font-size: 16px;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

image = Image.open('voice_ctrl.jpg')

st.image(image, width=300)

st.markdown("<h3 style='text-align:center; color:#4b0082;'>🎤 Pulsa el botón y habla para enviar tu comando</h3>", unsafe_allow_html=True)

stt_button = Button(label=" Inicio ", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act1":result.get("GET_TEXT").strip()})
        ret= client1.publish("voice_ctrl", message)

    
    try:
        os.mkdir("temp")
    except:
        pass
