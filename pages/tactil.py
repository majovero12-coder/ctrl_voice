import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# --- Configuración de la página ---
st.set_page_config(
    page_title="MQTT Control",
    page_icon="⚙️",
    layout="centered"
)

# --- Estilos personalizados ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #f9fafc, #e7ecf5);
        color: #0b0b0b;
    }

    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #1f3b73; /* Azul oscuro elegante */
        font-weight: 700;
    }

    /* Slider */
    .stSlider {
        background-color: transparent !important;
    }

    /* Botones */
    div.stButton > button {
        background-color: #FFD700; /* Dorado */
        color: #0b0b0b;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        transition: 0.3s;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        background-color: #ffcc00;
        color: black;
        transform: scale(1.05);
        box-shadow: 0px 3px 6px rgba(0,0,0,0.3);
    }

    /* Mensajes */
    .stMarkdown {
        color: #1f3b73;
        font-size: 1rem;
    }

    /* Slider label */
    .stSlider label {
        color: #1f3b73 !important;
        font-weight: 600;
    }

    /* Version text */
    .stWrite {
        color: #333;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# --- Mostrar versión de Python ---
st.write("🧩 **Versión de Python:**", platform.python_version())

# --- Variables iniciales ---
values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("El dato ha sido publicado.\n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# --- Configuración MQTT ---
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# --- Interfaz principal ---
st.title("⚙️ Control de Dispositivo MQTT")
st.markdown("Usa los botones para enviar comandos al broker MQTT y controlar el dispositivo conectado.")

st.divider()

# --- Botón ON ---
if st.button('🟢 ENCENDER (ON)', use_container_width=True):
    act1 = "ON"
    client1 = paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker, port)  
    message = json.dumps({"Act1": act1})
    ret = client1.publish("cmqtt_s", message)
    st.success("Comando **ON** enviado correctamente.")
else:
    st.write('')

# --- Botón OFF ---
if st.button('🔴 APAGAR (OFF)', use_container_width=True):
    act1 = "OFF"
    client1 = paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker, port)  
    message = json.dumps({"Act1": act1})
    ret = client1.publish("cmqtt_s", message)
    st.error("Comando **OFF** enviado correctamente.")
else:
    st.write('')

st.divider()

# --- Slider de valor analógico ---
values = st.slider('⚡ Selecciona un valor analógico', 0.0, 100.0)
st.write(f'Valor actual seleccionado: **{values}**')

# --- Botón para enviar valor ---
if st.button('📤 Enviar Valor Analógico', use_container_width=True):
    client1 = paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker, port)   
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_a", message)
    st.info(f"Valor analógico **{values}** enviado correctamente.")
else:
    st.write('')



