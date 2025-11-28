import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Importação Ajustada para Nuvem
try:
    from conector import carregar_dados as carregar_dados_pacientes
except ImportError:
    st.error("Erro ao carregar conector de dados.")
    st.stop()

# --- DICIONÁRIO GENÔMICO ---
GENOMICA_INFO = {
    "IDH1": {"nome": "Isocitrato Desidrogenase 1", "tipo": "Metabolismo", "desc": "Mutação 'Driver'. Em GBM, IDH mutado (R132H) indica melhor prognóstico e sensibilidade à Temozolomida."},
    "TP53": {"nome": "Tumor Protein 53", "tipo": "Supressor Tumoral", "desc": "Guardião do genoma. Impede correção de erros no DNA. Comum em GBMs secundários."},
    "ATRX": {"nome": "ATRX Chromatin Remodeler", "tipo": "Cromatina", "desc": "Ligado à manutenção alternativa dos telômeros (ALT). Co-ocorre com IDH."},
    "EGFR": {"nome": "Epidermal Growth Factor Receptor", "tipo": "RTK", "desc": "Amplificação clássica em GBM IDH-selvagem. Sinaliza crescimento agressivo."},
    "PTEN": {"nome": "Phosphatase and Tensin Homolog", "tipo": "Supressor", "desc": "Freia via PI3K/AKT. Sua perda torna o tumor mais agressivo."},
    "TERT": {"nome": "Telomerase Reverse Transcriptase", "tipo": "Telômeros", "desc": "Reativação da telomerase. Pior prognóstico em IDH-selvagem."},
    "NF1": {"nome": "Neurofibromin 1", "tipo": "Regulador RAS", "desc": "Define subtipo mesenquimal, associado a resistência."}
}

# --- FUNÇÕES UI ---
def criar_card_explicativo(titulo, valor, explicacao, icone="ℹ️", cor_valor="#00d4ff"):
    st.markdown(f"""<div style="background-color: #1E1E1E; border: 1px solid #333; border-radius: 10px; padding: 15px; margin-bottom: 10px;"><h4 style="margin: 0; color: #aaa; font-size: 0.9em;">{icone} {titulo}</h4><h2 style="margin: 5px 0; color: {cor_valor};">{valor}</h2></div>""", unsafe_allow_html=True)
    with st.expander(f"📚 Entenda: {titulo}"): st.info(explicacao)

def criar_gauge_risco(grupo_risco):
    mapa = {"Baixo": 15, "Médio": 50, "Médio-Alto": 75, "Alto": 85, "Altíssimo": 95}
    valor = mapa.get(grupo_risco, 50)
    fig = go.Figure(go.Indicator(mode="gauge+number", value=valor, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': "Espectro de Risco", 'font': {'size': 16, 'color': '#ccc'}}, gauge={'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#333"}, 'bar': {'color': "rgba(0,0,0,0)"}, 'bgcolor': "rgba(0,0,0,0)", 'borderwidth': 0, 'steps': [{'range': [0, 40], 'color': '#00c853'}, {'range': [40, 75], 'color': '#ffd600'}, {'range': [75, 100], 'color': '#d50000'}], 'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': valor}}))
    fig.update_layout(height=220, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
    return fig

def render_em_construcao(titulo, descricao_cientifica, tecnologias):
    st.markdown(f"""<div style="text-align: center; padding: 50px; background-color: #1a1c24; border: 1px dashed #444; border-radius: 15px; margin-top: 20px;"><div style="font-size: 50px; margin-bottom: 20px;">🚧</div><h2 style="color: #00d4ff; margin-bottom: 10px;">{titulo}</h2><span style="background: #333; color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 0.75em; font-weight: bold; letter-spacing: 1px;">EM CONSTRUÇÃO • ROADMAP DOUTORADO</span><p style="color: #ccc; margin-top: 25px; font-size: 1.1em; line-height: 1.6; max-width: 800px; margin-left: auto; margin-right: auto;">{descricao_cientifica}</p><div style="margin-top: 30px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto; background: #22252b; padding: 20px; border-radius: 10px;"><h5 style="color: #888; margin-bottom: 10px; font-size: 0.9em; text-transform: uppercase;">Tecnologias Previstas:</h5><div style="display: flex; flex-wrap: wrap; gap: 10px;">{''.join([f"<span style='background: #444; color: #aaa; padding: 5px 10px; border-radius: 5px; font-size: 0.8em;'>{tech}</span>" for tech in tecnologias])}</div></div></div>""", unsafe_allow_html=True)

# --- SETUP ---
st.set_page_config(page_title="GBM Precision Oncology", page_icon="🧬", layout="wide")
st.markdown("""<style>.stApp { background-color: #0e1117; } h1, h2, h3, h4, p, div, span { font-family: 'Segoe UI', sans-serif; color: #e0e0e0; } .medical-card { background-color: #1a1c24; border: 1px solid #2d303e; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); } div[data-testid="stMetric"] { background-color: #22252b !important; border-left: 4px solid #00d4ff; border-radius: 8px; padding: 10px 15px !important; } .risk-badge-high { background-color: #d32f2f; color: white; padding: 8px 20px; border-radius: 8px; font-weight: bold; white-space: nowrap; } .risk-badge-low { background-color: #2e7d32; color: white; padding: 8px 20px; border-radius: 8px; font-weight: bold; white-space: nowrap; } button[data-baseweb="tab"] { background-color: #161920 !important; border: 1px solid #2d303e !important; color: #aaa !important; margin-right: 2px; } button[data-baseweb="tab"][aria-selected="true"] { background-color: #00d4ff !important; color: #000 !important; font-weight: bold !important; border: none !important; } .dev-profile-card { background-color: #1a1c24; border: 1px solid #00d4ff; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 25px; box-shadow: 0 0 15px rgba(0, 212, 255, 0.15); } .dev-role { color: #888; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; } .dev-name { color: #fff; font-size: 1.1em; font-weight: bold; margin-bottom: 10px; } .linkedin-btn { background-color: #0077b5; color: white; text-decoration: none; padding: 8px 15px; border-radius: 5px; font-size: 0.85em; font-weight: bold; display: inline-block; transition: all 0.3s; } .linkedin-btn:hover { background-color: #005e93; color: white; transform: scale(1.05); }</style>""", unsafe_allow_html=True)

pacientes = carregar_dados_pacientes()
if not pacientes: st.stop()

with st.sidebar:
    st.markdown("""<div class="dev-profile-card"><div class="dev-role">Software & Research</div><div class="dev-name">Farm. Thiago Abranches</div><a href="https://www.linkedin.com/in/thiago-abranches/" target="_blank" class="linkedin-btn">🔗 Conectar no LinkedIn</a></div>""", unsafe_allow_html=True)
    st.title("🧬 GBM Precision")
    st.caption("Oncologia de Precisão Integrada | Beta v2.3")
    st.markdown("---")
    paciente_id = st.selectbox("🔎 Selecionar Prontuário", list(pacientes.keys()))
    dados = pacientes[paciente_id]
    info = dados['info_pessoal']
    st.markdown(f"""<div style="background: #22252b; padding: 15px; border-radius: 10px; display: flex; align-items: center; gap: 15px; margin-top: 10px;"><div style="background: #444; width: 45px; height: 45px; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-weight: bold;">{info['nome'][0]}</div><div><div style="color: white; font-weight: bold;">{info['nome']}</div><div style="color: #aaa; font-size: 0.8em;">ID: {dados['id']} | {info['idade']} anos</div></div></div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    kps = info['kps_performance']
    st.metric("Performance KPS", f"{kps}%")
    st.progress(kps/100)
    st.info("Status: Online")

m1 = dados['modulo_1_estatistica']
risco = m1['grupo_risco']
classe_risco = "risk-badge-high" if risco in ["Alto", "Altíssimo", "Médio-Alto"] else "risk-badge-low"

c1, c2 = st.columns([2.5, 1.5])
with c1:
    st.title("Painel de Decisão Multimodal")
    st.markdown("**Protocolo Clínico Integrado** | Suporte à Decisão Terapêutica")
with c2:
    st.markdown(f"<div style='display: flex; justify-content: flex-end; align-items: center; height: 100%; padding-top: 10px;'><div class='{classe_risco}'>GRUPAMENTO DE RISCO: {risco.upper()}</div></div>", unsafe_allow_html=True)
st.divider()

col_radar, col_kpi = st.columns([2, 3])
m3 = dados['modulo_3_teranostica']
m4 = dados['modulo_4_ml_features']
vol_total = m4['mri_t1_gd_vol'] + m4['mri_t2_flair_vol']
score_imagem = max(10, 100 - (vol_total / 10))

with col_radar:
    fig = go.Figure(data=go.Scatterpolar(r=[info['kps_performance'], m3['viabilidade_terapia'], score_imagem, m1['sobrevida_esperada_meses']*4], theta=['Clínica (KPS)', 'Teranóstico', 'Saúde (Img)', 'Sobrevida'], fill='toself', line_color='#00d4ff', opacity=0.6))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="#333"), bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20), height=300, font=dict(color="#aaa"))
    st.plotly_chart(fig, use_container_width=True)

with col_kpi:
    k1, k2, k3 = st.columns(3)
    k1.metric("Sobrevida Mediana", f"{m1['sobrevida_esperada_meses']} meses", "Estimativa M1")
    k2.metric("Volume Tumoral", f"{vol_total:.1f} cm³", "IA M4")
    k3.metric("Score Teranóstico", f"{m3['viabilidade_terapia']}%", f"SUV: {m3['pet_suv_max']}")
    if m3['viabilidade_terapia'] > 70: st.success("✅ **Oportunidade Terapêutica:** Elegível para Lutécio-177.")

st.write("")
st.subheader("🔍 Módulos de Análise")
abas = ["Análise Estatística", "Radiofármacos", "Sistema Teranóstico", "Machine Learning", "Priorização de Drogas", "Modelo Preditivo", "Análise Genômica", "Análise de Imagens", "Processamento de Laudos", "Séries Temporais", "Outros Parâmetros Ômicos", "Alertas Clínicos"]
tabs = st.tabs(abas)

with tabs[0]:
    c1, c2 = st.columns([1, 2])
    with c1: st.plotly_chart(criar_gauge_risco(risco), use_container_width=True)
    with c2: criar_card_explicativo("Sobrevida Mediana", f"{m1['sobrevida_esperada_meses']} Meses", "Estimativa baseada em nomogramas multivariáveis.")

with tabs[1]:
    m2 = dados['modulo_2_radiofarmacos']
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Elegibilidade")
        if m2['indicacao_lutetium']: st.success("✅ **APROVADO (Lu-177)**")
        else: st.error("🚫 **NÃO ELEGÍVEL**")
        st.metric("Peso", f"{m2['peso_kg']} kg")
    with c2: st.metric("Expressão SSTR2", m2['expressao_sstr2'])

with tabs[2]:
    suv = m3['pet_suv_max']
    cor = "red" if suv > 7 else "orange"
    st.markdown("#### Quantificação SUVmax (PET/CT)")
    st.markdown(f"<div style='border:1px solid {cor}; padding:20px; border-radius:10px; text-align:center; color:{cor}; font-size: 1.5em; font-weight:bold;'>SUV detectado: {suv}</div>", unsafe_allow_html=True)
    st.progress(m3['viabilidade_terapia']/100)
    st.caption(f"Score de Viabilidade: {m3['viabilidade_terapia']}%")

with tabs[3]:
    c1, c2, c3 = st.columns(3)
    c1.metric("Volume T1Gd", f"{m4['mri_t1_gd_vol']} cm³")
    c2.metric("Volume FLAIR", f"{m4['mri_t2_flair_vol']} cm³")
    c3.metric("Status MGMT", m4['mgmt_methylation'])
    st.info("ℹ️ Dados volumétricos extraídos via U-Net.")

with tabs[4]:
    m5 = dados['modulo_5_genomica']
    st.markdown("#### 💊 Farmacogenômica")
    if m5['resistencias_conhecidas']:
        st.error("🚨 **Resistências Previstas:**")
        for r in m5['resistencias_conhecidas']: st.markdown(f"- {r}")
    else: st.success("✅ Nenhuma resistência crítica a protocolos padrão.")

with tabs[5]: render_em_construcao("Modelo Preditivo Avançado", "Algoritmos de Ensemble Learning (XGBoost/LightGBM) para refinar a predição de sobrevida global.", ["XGBoost", "Kaplan-Meier Neural"])
with tabs[6]:
    m5 = dados['modulo_5_genomica']
    st.markdown("#### Painel NGS (Atual)")
    mutacoes = m5['mutacoes_detectadas']
    if mutacoes:
        cols = st.columns(len(mutacoes))
        for i, mut in enumerate(mutacoes):
            with cols[i]:
                info_gen = GENOMICA_INFO.get(mut, {"nome": "Gene", "tipo": "-", "desc": "..."})
                st.markdown(f"<div style='background:#222; padding:10px; border-radius:5px; text-align:center; border:1px solid #444;'><b>{mut}</b><br><small>{info_gen['tipo']}</small></div>", unsafe_allow_html=True)
    st.markdown("---")
    render_em_construcao("Expansão Genômica (WES)", "Pipeline para Whole Exome Sequencing (WES) visando identificar carga mutacional tumoral (TMB).", ["GATK Pipeline", "Variant Calling"])
with tabs[7]: render_em_construcao("Radiômica Avançada", "Extração de features radiômicas de alta ordem (textura, forma, wavelet).", ["PyRadiomics", "Habitat Clustering"])
with tabs[8]: render_em_construcao("NLP Clínico", "Mineração de texto em laudos histopatológicos utilizando LLMs.", ["BioBERT pt-br", "NER"])
with tabs[9]: render_em_construcao("Delta-Radiômica", "Análise longitudinal da evolução tumoral e resposta terapêutica.", ["Time-Series", "Delta-Features"])
with tabs[10]: render_em_construcao("Integração Multi-Ômica", "Fusão de dados de proteômica e metabolômica.", ["Data Fusion", "Network Biology"])
with tabs[11]: render_em_construcao("CDSS & Farmacovigilância", "Suporte à decisão para interações medicamentosas.", ["Drug-Interaction API", "Real-time Alerts"])
