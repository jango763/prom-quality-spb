import sys
import os

# Защита от ModuleNotFoundError на удаленном сервере
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import streamlit as st
import pandas as pd
import sqlite3
import io

# Импортируем нашу трехкабинетную СУБД структуру
import db_layer

# Инициализация структуры таблиц базы данных
db_layer.init_db()

# ==============================================================================
# 1. СИНХРОНИЗАЦИЯ СТИЛЕЙ И JS ИЗ CODEPEN (myREwOO)
# ==============================================================================
if os.path.exists("styles.css"):
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Считываем html баннер и подключаем js
html_banner = ""
if os.path.exists("layout.html"):
    with open("layout.html", "r", encoding="utf-8") as f:
        html_banner = f.read()

js_script = ""
if os.path.exists("script.js"):
    with open("script.js", "r", encoding="utf-8") as f:
        js_script = f.read()

st.markdown(f"{html_banner}<script>{js_script}</script>", unsafe_allow_html=True)

# ==============================================================================
# 2. ОФИЦИАЛЬНАЯ НАВИГАЦИЯ АПП (Сайдбар)
# ==============================================================================
with st.sidebar:
    st.title("🔒 Контур Допусков АПП")
    user_role = st.selectbox(
        "Выберите ваш личный кабинет:",
        [
            "🎓 Личный кабинет Физического лица", 
            "🏢 Личный кабинет Производства", 
            "🛠️ Кабинет Ассоциации (Управление)"
        ]
    )
    st.write("---")
    st.caption("Промышленная ИТ-платформа Санкт-Петербурга")

# Вытягиваем свежие данные из базы данных v5
courses_list = db_layer.execute_read("SELECT * FROM courses")
citizens_list = db_layer.execute_read("SELECT * FROM citizens")
factories_list = db_layer.execute_read("SELECT * FROM factories")
transactions_list = db_layer.execute_read("SELECT * FROM transactions")

# Глобальные счетчики KPI АПП
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Развернуто b2b-стандартов", value=f"{len(courses_list)} моделей")
kpi2.metric(label="Зарегистрировано граждан", value=f"{len(citizens_list)} анкет")
kpi3.metric(label="Активных заводов-заказчиков", value=f"{len(factories_list)} предприятий")
st.write("---")

# ==============================================================================
# КОНТУР 1: ФИЗИЧЕСКИЕ ЛИЦА (СОИСКАТЕЛИ)
# ==============================================================================
if user_role == "🎓 Личный кабинет Физического лица":
    st.header("🎓 Личный кабинет Физического лица")
    
    # Форма анкеты в стиле Glassmorphism
    st.markdown('<div class="glass-form">', unsafe_allow_html=True)
    with st.form("citizen_profile_form"):
        st.subheader("📝 Профильная анкета и загрузка документов")
        c_fio = st.text_input("ФИО полностью:", value="Иванов Игорь Игоревич")
        c_phone = st.text_input("Номер телефона:", value="+7(900)111-22-33")
        c_email = st.text_input("E-mail:", value="ivanov@spb.ru")
        c_edu_place = st.text_input("Где учились (ВУЗ / Колледж):", value="СПбПУ")
        
        col_doc1, col_doc2, col_doc3 = st.columns(3)
        c_passport = col_doc1.text_input("Паспорт (Серия, Номер):")
        c_diploma = col_doc2.text_input("Диплом (Серия, Номер):")
        c_workbook = col_doc3.text_input("Трудовая книжка (Номер):")
        
        c_skills = st.text_area("Расскажите о ваших навыках и опыте работы:")
        c_gdpr = st.checkbox("Согласие на обработку персональных данных граждан РФ", value=True)
        
        if st.form_submit_button("Сохранить анкету соискателя", use_container_width=True):
            if c_fio.strip() and c_phone.strip():
                # Проверяем, есть ли уже такой телефон
                check_user = db_layer.execute_read("SELECT id FROM citizens WHERE phone = ?", (c_phone.strip(),))
                if not check_user:
                    db_layer.execute_write("""
                        INSERT INTO citizens (fio, phone, email, district, skills_about, education_place, passport_serial_num, diploma_serial_num, workbook_serial_num, gdpr_consent) 
                        VALUES (?, ?, ?, 'Кировский район', ?, ?, ?, ?, ?, ?)
                    """, (c_fio.strip(), c_phone.strip(), c_email.strip(), c_skills.strip(), c_edu_place.strip(), c_passport.strip(), c_diploma.strip(), c_workbook.strip(), 1 if c_gdpr else 0))
                st.success("Анкета успешно зафиксирована в СУБД!")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Тест компетенций
    st.markdown('<div class="glass-form">', unsafe_allow_html=True)
    with st.form("competence_test_form"):
        st.subheader("🤖 Тест компетенций на производстве")
        st.markdown("**КРИТИЧЕСКАЯ СИТУАЦИЯ:** Датчик стойки управления Syntec выдал перегрев шпинделя станка ЧПУ за 20 млн рублей. Ваши действия?")
        sim_ans = st.radio("Выберите правильный алгоритм действий:", [
            "Игнорировать и закончить деталь",
            "Нажать аварийную кнопку STOP, перекрыть СОЖ и вызвать мастера",
            "Снизить обороты шпинделя вручную на 20%"
        ], index=None)
        
        if st.form_submit_button("Отправить ответы экзамена", use_container_width=True):
            if sim_ans == "Нажать аварийную кнопку STOP, перекрыть СОЖ и вызвать мастера":
                db_layer.execute_write("UPDATE citizens SET competence_test_score = 100, current_status = 'Железный специалист' WHERE phone = '+7(900)111-22-33'")
                st.success("🎯 Ответ верный! Вам присвоен статус: ЖЕЛЕЗНЫЙ СПЕЦИАЛИСТ.")
                st.rerun()
            else:
                st.error("⚠️ Ошибка! Алгоритм неверен, зафиксирована авария шпинделя.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# КОНТУР 2: ЮРИДИЧЕСКИЕ ЛИЦА (ПРОИЗВОДСТВА)
# ==============================================================================
elif user_role == "🏢 Личный кабинет Производства":
    st.header("🏢 Личный кабинет Завода-Производителя оборудования")
    
    # Отрисовка объемных b2b-карточек тарифов из CodePen
    col_card1, col_card2, col_card3 = st.columns(3)
    with col_card1:
        st.markdown('<div class="glass-card"><div class="card-title">ТЕКУЩИЙ ТАРИФ</div><div class="card-value">ПОШТУЧНЫЙ ВЫКУП</div></div>', unsafe_allow_html=True)
    with col_card2:
        st.markdown('<div class="glass-card"><div class="card-title">ОСТАТОК АНКЕТ</div><div class="card-value" style="color: #3B82F6;">5 ШТ.</div></div>', unsafe_allow_html=True)
    with col_card3:
        st.markdown('<div class="glass-card"><div class="card-title">БЕЗЛИМИТНЫЙ ДОСТУП</div><div class="card-value" style="color: #EF4444;">❌ ВЫКЛ.</div></div>', unsafe_allow_html=True)

    tab_tariffs, tab_upload_dpo = st.tabs(["💳 Тарифная сетка и покупка лицензии", "📥 Загрузка b2b-стандарта ДПО"])
    
    with tab_tariffs:
        st.markdown('<div class="glass-form">', unsafe_allow_html=True)
        st.subheader("💳 Доступные коммерческие лицензии АПП:")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown('<div class="tariff-box"><h5>📦 Штучный пакет</h5><p class="price">15 000 ₽</p><p class="desc">Доступ к 5 проверенным анкетам соискателей</p></div>', unsafe_allow_html=True)
            if st.button("Купить штучный пакет", key="buy_pack", use_container_width=True):
                db_layer.execute_write("INSERT INTO transactions (factory_id, amount, payment_type) VALUES (2, 15000.0, '5_Анкет')")
                st.toast("Пакет куплен! Проводка отправлена в АПП.")
        with col_t2:
            st.markdown('<div class="tariff-box popular"><h5>⚔️ Безлимитный Год</h5><p class="price">150 000 ₽</p><p class="desc">Полный безлимит на выгрузку "Железных мастеров"</p></div>', unsafe_allow_html=True)
            if st.button("Активировать Безлимит", key="buy_unlim", use_container_width=True, type="primary"):
                db_layer.execute_write("INSERT INTO transactions (factory_id, amount, payment_type) VALUES (1, 150000.0, 'Безлимит_Год')")
                st.toast("Безлимит активирован! Проводка отправлена в АПП.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_upload_dpo:
        st.markdown('<div class="glass-form">', unsafe_allow_html=True)
        with st.form("factory_dpo_form"):
            st.subheader("📥 Загрузка b2b-стандарта ДПО")
            f_inn = st.text_input("ИНН предприятия:")
            f_title = st.text_input("Название программы обучения:")
            f_model = st.text_input("Модель промышленного станка:")
            f_text = st.text_area("Введите развернутые пошаговые инструкции и регламенты безопасности:")
            
            if st.form_submit_button("Опубликовать стандарт завода", use_container_width=True):
                if f_inn.strip() and f_title.strip():
                    db_layer.execute_write("""
                        INSERT INTO courses (factory_id, course_title, equipment_model, safety_instructions, secret_question, secret_answer) 
                        VALUES (1, ?, ?, ?, 'Какое давление критическое?', 'Выше 5 МПа')
                    """, (f_title.strip(), f_model.strip(), f_text.strip()))
                    st.success("Стандарт завода успешно зафиксирован в SQLite!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# КОНТУР 3: АССОЦИАЦИЯ (УПРАВЛЕНИЕ)
# ==============================================================================
elif user_role == "🛠️ Кабинет Ассоциации (Управление)":
    st.header("🛠️ Пульт Оперативного Контроля АПП СПб")
    
    # Сеткa KPI Ассоциации
