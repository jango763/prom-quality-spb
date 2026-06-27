import streamlit as st

st.markdown("""
    <style>
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        div[data-testid="stForm"], .stAlert { background: rgba(30, 41, 59, 0.7) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 12px !important; padding: 25px !important; backdrop-filter: blur(10px); }
        .glass-card { background: rgba(30, 41, 59, 0.4) !important; border: 1px solid rgba(6, 182, 212, 0.2) !important; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .card-title { font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; }
        .card-value { font-size: 24px; font-weight: 800; color: #06B6D4; margin-top: 5px; }
        .tariff-box { background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.05) !important; border-radius: 12px; padding: 25px; text-align: center; margin-bottom: 15px; }
        .tariff-box.popular { border-color: #06B6D4 !important; background: rgba(6, 182, 212, 0.02) !important; box-shadow: 0 0 25px rgba(6, 182, 212, 0.1) !important; }
        .price { font-size: 36px; font-weight: 900; color: #06B6D4; margin: 10px 0; }
        .desc { font-size: 13px; color: #94A3B8; }
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] { background-color: rgba(15, 23, 42, 0.8) !important; color: #FFFFFF !important; border: 1px solid rgba(6, 182, 212, 0.2) !important; border-radius: 8px !important; }
        div[data-testid="stWidgetLabel"] p, label p { color: #FFFFFF !important; font-weight: 600 !important; }
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #94A3B8; }
        .stTabs [aria-selected="true"] { color: #06B6D4 !important; border-bottom-color: #06B6D4 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3>🏢 Портал Партнеров и Интеграторов оборудования</h3>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown('<div class="glass-card"><div class="card-title">ЛИЦЕНЗИЯ КОМПАНИИ</div><div class="card-value">ПОШТУЧНЫЙ НАЙМ</div></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="glass-card"><div class="card-title">ДОСТУПНО ВЫГРУЗОК</div><div class="card-value" style="color: #3B82F6;">5 ЭКСПЕРТОВ</div></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="glass-card"><div class="card-title">ЦЕНТР КОМПЕТЕНЦИЙ</div><div class="card-value" style="color: #EF4444;">❌ НЕ СОЗДАН</div></div>', unsafe_allow_html=True)

tab_tariffs, tab_dpo = st.tabs(["💳 Тарифные программы обучения", "📥 Публикация стандартов ДПО"])

with tab_tariffs:
    st.markdown("<br>", unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="tariff-box"><h5>📦 Штучный b2b-курс</h5><div class="price">19 990 ₽</div><div class="desc">Доступ к профильной программе автоматизации и 1 сертификату</div></div>', unsafe_allow_html=True)
        if st.button("Купить штучный курс", use_container_width=True):
            st.session_state["payments_data"].append({"id": len(st.session_state["payments_data"])+1, "tariff": "Штучный курс", "amount": 19990.0, "timestamp": "Только что"})
            st.toast("✓ Транзакция зафиксирована!")
            st.rerun()
    with col_t2:
        st.markdown('<div class="tariff-box popular"><h5>⚔️ Корпоративный Безлимит</h5><div class="price">150 000 ₽</div><div class="desc">Полное обучение и сертификация до 50 внутренних экспертов компании</div></div>', unsafe_allow_html=True)
        if st.button("Активировать Безлимит", use_container_width=True, type="primary"):
            st.session_state["payments_data"].append({"id": len(st.session_state["payments_data"])+1, "tariff": "Корпоративный Безлимит", "amount": 150000.0, "timestamp": "Только что"})
            st.toast("✓ Годовая b2b-подписка активирована!")
            st.rerun()

with tab_dpo:
    with st.form("dpo_upload_v3"):
        st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>📥 Загрузка новой программы опережающего ДПО</h4>", unsafe_allow_html=True)
        f_inn = st.text_input("ИНН предприятия-партнера:")
        f_title = st.text_input("Название обучающего трека:")
        f_model = st.text_input("Модель промышленного оборудования ЧПУ:")
        f_text = st.text_area("Развернутые регламенты безопасности и low-code скрипты:")
        if st.form_submit_button("Опубликовать курс в Академии", use_container_width=True):
            if f_inn.strip() and f_title.strip():
                st.session_state["courses_data"].append({"inn": f_inn.strip(), "title": f_title.strip(), "model": f_model.strip(), "text": f_text.strip()})
                st.success("✓ Новый обучающий трек успешно занесен в реестр Академии!")
                st.rerun()
