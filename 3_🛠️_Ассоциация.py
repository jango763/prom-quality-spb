import streamlit as st
import sqlite3
import pandas as pd

# Подгружаем фирменные b2b-стили CodePen
st.markdown("""
    <style>
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        div[data-testid="stForm"], .stAlert {
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 14px !important; padding: 25px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important; backdrop-filter: blur(12px);
        }
        .glass-card {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px; padding: 20px; margin-bottom: 15px;
        }
        .card-title { font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-value { font-size: 24px; font-weight: 800; color: #10B981; margin-top: 5px; }
        
        .tariff-box {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px; padding: 25px; text-align: center; margin-bottom: 15px;
        }
        .tariff-box.popular {
            border-color: #10B981; background: rgba(16, 185, 129, 0.02);
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.05);
        }
        .price { font-size: 36px; font-weight: 900; color: #10B981; margin: 10px 0; }
        .desc { font-size: 13px; color: #94A3B8; }
        .stTextInput input, .stTextArea textarea, .stSelectbox div {
            background-color: rgba(15, 23, 42, 0.6) !important; color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #94A3B8; }
        .stTabs [aria-selected="true"] { color: #10B981 !important; border-bottom-color: #10B981 !important; }
    </style>
""", unsafe_allow_html=True)

DB_NAME = "production_control_enterprise_final_v1.db"

st.markdown("<h2>🏢 Личный кабинет Завода-Производителя оборудования</h2>", unsafe_allow_html=True)

# Сетка объемных b2b-карточек KPI из CodePen
c1, c2, c3 = st.columns(3)
with c1: st.markdown('<div class="glass-card"><div class="card-title">ТЕКУЩИЙ ТАРИФ ИНДУСТРИИ</div><div class="card-value">ПОШТУЧНЫЙ ВЫКУП</div></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="glass-card"><div class="card-title">ОСТАТОК ПРОВЕРЕННЫХ АНКЕТ</div><div class="card-value" style="color: #3B82F6;">5 ШТ.</div></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="glass-card"><div class="card-title">БЕЗЛИМИТНЫЙ ДОСТУП АПП</div><div class="card-value" style="color: #EF4444;">❌ ВЫКЛ.</div></div>', unsafe_allow_html=True)

tab_tariffs, tab_dpo = st.tabs(["💳 Тарифная сетка и коммерческие подписки", "📥 Загрузка b2b-стандарта ДПО"])

with tab_tariffs:
    st.markdown("<br>", unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown('<div class="tariff-box"><h5>📦 Штучный пакет анкет</h5><div class="price">15 000 ₽</div><div class="desc">Разовый выкуп контактов 5 верифицированных мастеров</div></div>', unsafe_allow_html=True)
        if st.button("Купить поштучный пакет (5 шт)", key="buy_piece_btn", use_container_width=True):
            conn = sqlite3.connect(DB_NAME)
            conn.execute("INSERT INTO payments (tariff, amount) VALUES ('Поштучно (5 шт)', 15000.0)")
            conn.commit()
            conn.close()
            st.toast("✓ Проводка штучной лицензии отправлена в Ассоциацию!")
            st.rerun()
            
    with col_t2:
        st.markdown('<div class="tariff-box popular"><h5>⚔️ Безлимитный Год найма</h5><div class="price">150 000 ₽</div><div class="desc">Полный безлимитный доступ к базе "Железных специалистов" на 365 дней</div></div>', unsafe_allow_html=True)
        if st.button("Активировать Безлимитную лицензию", key="buy_unlim_btn", use_container_width=True, type="primary"):
            conn = sqlite3.connect(DB_NAME)
            conn.execute("INSERT INTO payments (tariff, amount) VALUES ('Безлимитный Год', 150000.0)")
            conn.commit()
            conn.close()
            st.toast("✓ Годовая b2b-подписка успешно активирована!")
            st.rerun()

with tab_dpo:
    with st.form("factory_dpo_upload_form"):
        st.markdown("<h4 style='color:#34D399; font-weight:700;'>📥 Конструктор программы обучения под оборудование</h4>", unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns(2)
        f_inn = col_f1.text_input("Верифицированный ИНН предприятия:", placeholder="7805041230")
        f_phone = col_f2.text_input("Контактный телефон отдела кадров:", value="+7(812)111-22-33")
        f_email = st.text_input("E-mail для получения кадровых уведомлений:", value="hr@factory.spb.ru")
        
        f_title = st.text_input("Название новой программы опережающего ДПО:")
        f_model = st.text_input("Модель дорогостоящего станка (под формирование сбыта):", value="Станок ЧПУ 20млн+ рублей")
        
        f_text = st.text_area("Развернутый текст регламента безопасности и эксплуатации станка (инструкции ТБ):", placeholder="1. Проверить давление пресса...\n2. Использовать быстрый ход G00 запрещено...")
        
        if st.form_submit_button("Опубликовать b2b-стандарт завода", use_container_width=True):
            if not f_inn.strip() or not f_title.strip():
                st.error("Заполните ИНН и Название программы обучения!")
            else:
                conn = sqlite3.connect(DB_NAME)
                conn.execute("INSERT INTO courses (inn, title, model, text) VALUES (?, ?, ?, ?)", (f_inn.strip(), f_title.strip(), f_model.strip(), f_text.strip()))
                conn.commit()
                conn.close()
                st.success("✓ Программа опережающего обучения успешно опубликована на витрине ДПО!")
                st.rerun()
