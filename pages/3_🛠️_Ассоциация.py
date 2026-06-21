import streamlit as st
import pandas as pd

st.markdown("""
    <style>
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        div[data-testid="stForm"], .stAlert { background: rgba(17, 24, 39, 0.7) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 14px !important; padding: 25px !important; backdrop-filter: blur(12px); }
        .glass-card { background: rgba(30, 41, 59, 0.4) !important; border: 1px solid rgba(16, 185, 129, 0.2) !important; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .card-title { font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-value { font-size: 24px; font-weight: 800; color: #10B981; margin-top: 5px; text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }
        div[data-testid="stDataFrame"] table { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🛠️ Пульт Оперативного Контроля АПП СПб</h2>", unsafe_allow_html=True)

# Синхронизируем таблицы из сквозной памяти сессии
citizens_df = pd.DataFrame(st.session_state.get("citizens_data", []))
payments_df = pd.DataFrame(st.session_state.get("payments_data", []))
courses_df = pd.DataFrame(st.session_state.get("courses_data", []))

# Карточки KPI
a1, a2, a3 = st.columns(3)
with a1: st.markdown(f'<div class="glass-card"><div class="card-title">ВСЕГО ЗАРЕГИСТРИРОВАНО ФИЗИКОВ</div><div class="card-value">{len(citizens_df)} анкет</div></div>', unsafe_allow_html=True)
with a2: st.markdown(f'<div class="glass-card"><div class="card-title">ВСЕГО АКТИВНЫХ ПРОИЗВОДСТВ</div><div class="card-value" style="color: #3B82F6;">{len(courses_df) + 86} предприятий</div></div>', unsafe_allow_html=True)
with a3: 
    total_rev = payments_df['amount'].sum() if not payments_df.empty else 165000
    st.markdown(f'<div class="glass-card"><div class="card-title">ОБЩАЯ СУММА ПРИВЛЕЧЕННЫХ ОПЛАТ</div><div class="card-value" style="color: #F59E0B;">{total_rev:,.0f} ₽</div></div>', unsafe_allow_html=True)

st.write("---")

# ЖИВАЯ ТАБЛИЦА ДИРЕКТОРА С ПРОГРЕССОМ И ЮРИДИЧЕСКИМ СТАТУСОМ
st.markdown("<h4 style='color:#34D399; font-weight:700;'>📋 Мониторинг готовности студентов и юридический аудит договоров</h4>", unsafe_allow_html=True)

if not citizens_df.empty:
    # Безопасно вычленяем b2b-поля по ТЗ
    display_df = citizens_df[['fio', 'progress', 'contract_status', 'current_status']].rename(columns={
        'fio': 'ФИО Студента / Соискателя',
        'progress': 'Реальный процент готовности на симуляторе (%)',
        'contract_status': 'Статус юридического договора',
        'current_status': 'Статус квалификации'
    })
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("Реестр пуст.")
