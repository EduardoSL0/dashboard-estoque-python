import streamlit as st
import pandas as pd

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Controle de Estoque", layout="wide")

# ==============================
# ESTILO DARK MODERNO
# ==============================
st.markdown("""
<style>
.stApp {
    background-color: #0F172A;
    color: #E2E8F0;
}

h1 {
    color: #F8FAFC;
}

/* CARDS */
.card {
    padding: 25px;
    border-radius: 15px;
    background: linear-gradient(135deg, #1E293B, #0F172A);
    border: 1px solid #334155;
    text-align: center;
}

/* NÚMEROS */
.big-number {
    font-size: 36px;
    font-weight: bold;
}

.green { color: #22C55E; }
.red { color: #EF4444; }

/* INPUT */
input {
    background-color: #1E293B !important;
    color: white !important;
}

/* TABELA */
[data-testid="stDataFrame"] {
    background-color: #1E293B;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# TÍTULO
# ==============================
st.title("📦 Controle de Estoque")

# ==============================
# ESCOLHA DE FONTE (VISÍVEL)
# ==============================
st.subheader("📂 Fonte dos dados")

modo = st.radio(
    "Escolha como deseja carregar os dados:",
    ["Usar arquivo padrão (estoque.xlsx)", "Enviar planilha Excel"]
)

# ==============================
# LEITURA DOS DADOS
# ==============================
if modo == "Enviar planilha Excel":
    
    arquivo = st.file_uploader(
        "📂 Envie sua planilha Excel",
        type=["xlsx"]
    )

    if arquivo:
        df = pd.read_excel(arquivo)
    else:
        st.info("Envie um arquivo para continuar")
        st.stop()

else:
    try:
        df = pd.read_excel("estoque.xlsx")
    except:
        st.error("Arquivo 'estoque.xlsx' não encontrado")
        st.stop()

# ==============================
# TRATAMENTO
# ==============================
df.columns = df.columns.str.strip()

if "Produto" not in df.columns or "Quantidade" not in df.columns:
    st.error("A planilha precisa ter: Produto e Quantidade")
    st.stop()

# ==============================
# CLASSIFICAÇÃO
# ==============================
def classificar(qtd):
    if qtd < 20:
        return "Baixo"
    elif qtd < 80:
        return "Médio"
    else:
        return "Alto"

df["Status"] = df["Quantidade"].apply(classificar)

# ==============================
# KPIs
# ==============================
total = df["Quantidade"].sum()
baixo = df[df["Status"] == "Baixo"]

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="big-number green">{total}</div>
        <div>Total em estoque</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="big-number red">{len(baixo)}</div>
        <div>Itens críticos</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# ALERTA
# ==============================
if len(baixo) > 0:
    st.error("⚠️ Produtos com estoque baixo!")

# ==============================
# BUSCA
# ==============================
st.subheader("🔎 Buscar produto")

busca = st.text_input("Digite o nome do produto")

df_filtrado = df.copy()

if busca:
    df_filtrado = df[df["Produto"].str.contains(busca, case=False)]

# ==============================
# PRODUTOS CRÍTICOS
# ==============================
st.subheader("⚠️ Produtos críticos")

st.dataframe(
    baixo.sort_values(by="Quantidade"),
    use_container_width=True
)

# ==============================
# TODOS PRODUTOS
# ==============================
with st.expander("📋 Ver todos os produtos"):
    st.dataframe(df_filtrado, use_container_width=True)