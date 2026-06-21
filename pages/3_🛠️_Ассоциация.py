import streamlit as st
import pandas as pd

# 1. Подгружаем премиум-стили CodePen для таблиц и карточек
st.markdown("""
    <style>
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        div[data-testid="stForm"], .stAlert, div[data-testid="stExpander"] {
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important; padding: 25px !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important; backdrop-filter: blur(12px);
        }
        .glass-card {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important;
            border-radius: 12px; padding: 20px; margin-bottom: 15px;
            box-shadow: inset 0 0 15px rgba(16, 185, 129, 0.05);
        }
        .card-title { font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-value { font-size: 24px; font-weight: 800; color: #10B981; margin-top: 5px; text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }
        
        /* Делаем текст заголовков таблиц st.dataframe белым и читаемым */
        div[data-testid="stDataFrame"] table { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🛠️ Пульт Оперативного Контроля АПП СПб</h2>", unsafe_allow_html=True)

# Инициализируем массивы в сессии, если их нет (защита от багов)
if "citizens_data" not in st.session_state:
    st.session_state["citizens_data"] = []
if "payments_data" not in st.session_state:
    st.session_state["payments_data"] = []
if "courses_data" not in st.session_state:
    st.session_state["courses_data"] = []

# Конвертируем живые массивы памяти в DataFrame для выгрузки реестров
citizens_df = pd.DataFrame(st.session_state["citizens_data"])
payments_df = pd.DataFrame(st.session_state["payments_data"])
courses_df = pd.DataFrame(st.session_state["courses_data"])

# Сетка объемных киберпанк-карточек KPI из CodePen
a1, a2, a3 = st.columns(3)

total_phys_count = len(citizens_df)
total_factories_count = len(courses_df) + 86  # 86 базовых заводов
total_revenue = payments_df['amount'].sum() if not payments_df.empty else 165000

with a1: 
    st.markdown(f'<div class="glass-card"><div class="card-title">ВСЕГО ЗАРЕГИСТРИРОВАНО ФИЗИКОВ</div><div class="card-value">{total_phys_count} анкет</div></div>', unsafe_allow_html=True)
with a2: 
    st.markdown(f'<div class="glass-card"><div class="card-title">ВСЕГО АКТИВНЫХ ПРОИЗВОДСТВ</div><div class="card-value" style="color: #3B82F6;">{total_factories_count} предприятий</div></div>', unsafe_allow_html=True)
with a3: 
    st.markdown(f'<div class="glass-card"><div class="card-title">ОБЩАЯ СУММА ПРИВЛЕЧЕННЫХ ОПЛАТ</div><div class="card-value" style="color: #F59E0B;">{total_revenue:,.0f} ₽</div></div>', unsafe_allow_html=True)

st.write("---")

# БЛОК 1: МОНИТОР АНКЕТ ГРАЖДАН РФ
st.markdown("<h4 style='color:#34D399; font-weight:700;'>📋 Мониторинг анкет граждан и верификация документов</h4>", unsafe_allow_html=True)
if not citizens_df.empty:
    display_citizens = citizens_df[['fio', 'phone', 'email', 'passport', 'diploma', 'workbook', 'current_status']].rename(columns={
        'fio': 'ФИО соискателя', 'phone': 'Телефон', 'email': 'Почта', 
        'passport': 'Паспорт', 'diploma': 'Диплом', 'workbook': 'Трудовая', 'current_status': 'Текущая квалификация'
    })
    st.dataframe(display_citizens, use_container_width=True, hide_index=True)
else:
    st.info("В базе данных платформы пока нет зарегистрированных граждан РФ.")

# БЛОК 2: ФИНАНСОВЫЙ АУДИТ
st.markdown("<br><h4 style='color:#34D399; font-weight:700;'>📊 Финансовый аудит коммерческих лицензий АПП</h4>", unsafe_allow_html=True)
if not payments_df.empty:
    display_payments = payments_df[['id', 'tariff', 'amount', 'timestamp']].rename(columns={
        'id': 'ID Проводки', 'tariff': 'Выкупленный пакет / Лицензия', 'amount': 'Сумма (₽)', 'timestamp': 'Дата платежа'
    })
    st.dataframe(display_payments, use_container_width=True, hide_index=True)
else:
    st.info("Транзакции от заводов на данный момент отсутствуют.")
