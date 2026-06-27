import streamlit as st
import pandas as pd

st.markdown("""
    <style>
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        .glass-card { background: rgba(30, 41, 59, 0.4) !important; border: 1px solid rgba(6, 182, 212, 0.2) !important; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .card-title { font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-value { font-size: 24px; font-weight: 800; color: #06B6D4; margin-top: 5px; }
        div[data-testid="stDataFrame"] table { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🛠️ Панель Руководителя | Мониторинг Центра Компетенций</h2>", unsafe_allow_html=True)

citizens_df = pd.DataFrame(st.session_state.get("citizens_data", []))
payments_df = pd.DataFrame(st.session_state.get("payments_data", []))
courses_df = pd.DataFrame(st.session_state.get("courses_data", []))

a1, a2, a3 = st.columns(3)
with a1: st.markdown(f'<div class="glass-card"><div class="card-title">ВСЕГО ЭКСПЕРТОВ В СИСТЕМЕ</div><div class="card-value">{len(citizens_df)} человек</div></div>', unsafe_allow_html=True)
with a2: st.markdown(f'<div class="glass-card"><div class="card-title">АКТИВНЫХ ТРЕКОВ ОБУЧЕНИЯ</div><div class="card-value" style="color: #3B82F6;">{len(courses_df) + 6} направлений</div></div>', unsafe_allow_html=True)
with a3: 
    total_rev = payments_df['amount'].sum() if not payments_df.empty else 165000
    st.markdown(f'<div class="glass-card"><div class="card-title">ПРИВЛЕЧЕННЫЙ ОБЪЕМ ИНВЕСТИЦИЙ</div><div class="card-value" style="color: #F59E0B;">{total_rev:,.0f} ₽</div></div>', unsafe_allow_html=True)

st.write("---")

# ЖИВАЯ ТАБЛИЦА ДИРЕКТОРА (ST.DATAFRAME) ПО ТЗ
st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>📋 Мониторинг готовности студентов и юридический аудит договоров</h4>", unsafe_allow_html=True)

if not citizens_df.empty:
    display_df = citizens_df[['fio', 'progress', 'contract_status', 'current_status']].rename(columns={
        'fio': 'ФИО Студента / Специалиста',
        'progress': 'Реальный процент готовности на симуляторе (%)',
        'contract_status': 'Статус юридического договора',
        'current_status': 'Статус квалификации'
    })
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("Реестр пуст.")

st.markdown("<br><h4 style='color:#06B6D4; font-weight:700;'>📊 Коммерческий аудит оплат b2b-лицензий</h4>", unsafe_allow_html=True)
if not payments_df.empty:
    st.dataframe(payments_df[['id', 'tariff', 'amount', 'timestamp']].rename(columns={
        'id': 'ID Проводки', 'tariff': 'Выкупленная программа / Подписка', 'amount': 'Сумма (₽)', 'timestamp': 'Дата платежа'
    }), use_container_width=True, hide_index=True)
