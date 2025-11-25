import streamlit as st
import pandas as pd
import plotly.express as px
import base64


st.set_page_config(page_title="Data Visualization", layout="wide")
st.title("Données qui ne sont pas dans la base de diotali")

# Fonction pour convertir une image locale en base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Charger ton logo
logo_base64 = get_base64_of_image("assets/logo.png")

with st.sidebar:

        ### affichage du logo
        st.markdown(
        f"""
        <div style="text-align: center; margin-top: -20px; margin-bottom: 20px;">
            <img src="data:image/png;base64,{logo_base64}" 
                 style="border-radius: 50%; width:90px; height:90px; margin:10px;">
        </div>
        """,
        unsafe_allow_html=True
        )
logo_base64 = get_base64_of_image("assets/logo.png")

st.sidebar.markdown("---")

df = pd.read_csv("absent.csv")


st.sidebar.write('Filtrer par :')
client = df['Client'].unique().tolist()
model = st.sidebar.multiselect("Unité organisationnelle", client)
if model:
    df = df[df['Client'].isin(model)]


total_ventes = df['Montant'].sum()
nb_clients = df['Numero'].nunique()
nb_commandes = df['Client'].nunique()

# Fonction pour créer une carte
def kpi_card(title, value, emoji):
    st.markdown(f"""
        <div style='
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        '>
            <div style='font-size:16px; color:#555;'>{emoji} {title}</div>
            <div style='font-size:32px; font-weight:bold; color:#1f77b4;'>{value}</div>
        </div>
    """, unsafe_allow_html=True)

# Affichage en colonnes
col1, col2, col3 = st.columns(3)

with col1:
    kpi_card("Montant", f"{total_ventes:,.0f}", "💰")

with col2:
    kpi_card("Nombre de Numero", nb_clients, "👥")

with col3:
    kpi_card("Unité organisationnelle", nb_commandes, "🧾")

st.write("---")
st.write("tableau des donnees")


st.dataframe(df)

if "Client" in df.columns:
        marque_counts = df["Client"].astype(str).value_counts().reset_index()
        marque_counts.columns = ["Client", "count"]
        fig_marque = px.bar(
            marque_counts.head(30),
            x="Client",
            y="count",
            title="numero manquant par unité organisationnelle",
            color="count",
            color_continuous_scale="teal",
        )
        fig_marque.update_layout(template="plotly_dark", height=420, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_marque, width='stretch')
