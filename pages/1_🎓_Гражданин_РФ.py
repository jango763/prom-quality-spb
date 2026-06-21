import streamlit as st
import sqlite3
import pandas as pd

# Подгружаем стили CodePen из главного окна для сохранения внешки
st.markdown("""
    <style>
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        div[data-testid="stForm"], .stAlert {
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 14px !important; padding: 25px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important; backdrop-filter: blur(12px);
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox div {
            background-color: rgba(15, 23, 42, 0.6) !important; color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #94A3B8; }
        .stTabs [aria-selected="true"] { color: #10B981 !important; border-bottom-color: #10B981 !important; }
    </style>
""", unsafe_allow_html=True)

DB_NAME = "production_control_enterprise_final_v1.db"

st.markdown("<h2>🎓 Портал обучения граждан РФ и Паспорт Навыков</h2>", unsafe_allow_html=True)

# Использование табов внутри кабинета для расширения интерактива
tab_anketa, tab_exam = st.tabs(["📝 Профильная анкета и документы", "🤖 Тест компетенций на производстве"])

with tab_anketa:
    with st.form("citizen_reg_form", clear_on_submit=False):
        st.markdown("<h4 style='color:#34D399; font-weight:700;'>📂 Ввод персональных данных и квалификации</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        fio = col1.text_input("ФИО соискателя полностью:", value="Иванов Игорь Игоревич")
        phone = col2.text_input("Номер мобильного телефона:", value="+7(900)111-22-33")
        email = col3.text_input("Электронная почта (E-mail):", value="ivanov@spb.ru")
        
        col4, col5, col6 = st.columns(3)
        passport = col4.text_input("Паспорт гражданина РФ (Серия, Номер):", placeholder="4011 123456")
        diploma = col5.text_input("Диплом об образовании (Серия, Номер):", placeholder="№78-01")
        workbook = col6.text_input("Трудовая книжка (Серия, Номер):", placeholder="№ТК-99")
        
        edu_place = st.selectbox("Укажите ваше учебное заведение (ДПО/ВУЗ):", ["СПбПУ (Политех)", "Университет ИТМО", "Колледж ТКУиК", "Другое профильное"])
        skills = st.text_area("Анкета о себе (Ваши навыки, разряды, работа на станках ЧПУ):", placeholder="Оператор ЧПУ 3 разряда, знаю стойки стойки Syntec и Fanuc...")
        
        gdpr = st.checkbox("Я даю полное согласие на обработку моих персональных данных Ассоциацией АПП СПб", value=True)
        
        if st.form_submit_button("Сохранить анкету соискателя", type="primary"):
            if not fio.strip() or not phone.strip():
                st.error("Поля 'ФИО' и 'Телефон' являются обязательными для b2b-верификации!")
            elif not gdpr:
                st.warning("Необходимо дать согласие на обработку данных граждан РФ!")
            else:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                # Проверяем на дубликат телефона
                cursor.execute("SELECT id FROM citizens WHERE phone = ?", (phone.strip(),))
                if cursor.fetchone():
                    st.warning("Гражданин с таким номером телефона уже зарегистрирован в системе!")
                    conn.close()
                else:
                    cursor.execute("""
                        INSERT INTO citizens (fio, phone, email, education, passport, diploma, workbook, skills, gdpr, current_status) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Обучение')
                    """, (fio.strip(), phone.strip(), email.strip(), edu_place, passport.strip(), diploma.strip(), workbook.strip(), skills.strip(), 1 if gdpr else 0))
                    conn.commit()
                    conn.close()
                    st.success("✓ Данные анкеты и скан-номера документов успешно внесены в реляционную СУБД SQLite!")

with tab_exam:
    st.markdown("<h4 style='color:#34D399; font-weight:700;'>🖥️ Автоматизированный экзаменационный барьер ТБ</h4>", unsafe_allow_html=True)
    
    with st.form("exam_test_form"):
        st.info("КЕЙС: На пульте управления дорогостоящего станка ЧПУ (стоимость 20 млн+ рублей) датчик стойки Syntec выдал критический перегрев температурного режима шпинделя. Каковы ваши экстренные действия в цеху?")
        
        ans = st.radio("Выберите строго один правильный алгоритм действий:", [
            "Игнорировать предупреждение автоматики и закончить фрезеровку текущей детали",
            "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха",
            "Вручную снизить обороты шпинделя на 20% через потенциометр пульта"
        ], index=None)
        
        if st.form_submit_button("Отправить ответы экзамена на проверку", type="primary"):
            if ans is None:
                st.warning("Выберите один из вариантов ответа!")
            elif ans == "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха":
                conn = sqlite3.connect(DB_NAME)
                # Переводим последнюю добавленную запись на статус Железного специалиста
                conn.execute("UPDATE citizens SET score = 100, current_status = 'Железный специалист' WHERE id = (SELECT max(id) FROM citizens)")
                conn.commit()
                conn.close()
                st.success("🎯 ЭКЗАМЕН СДАН НА 100%! Алгоритм абсолютно верен. Вам присвоен статус: ЖЕЛЕЗНЫЙ СПЕЦИАЛИСТ. Допуск в цех открыт.")
            else:
                conn = sqlite3.connect(DB_NAME)
                conn.execute("UPDATE citizens SET score = 0, current_status = 'Обучение' WHERE id = (SELECT max(id) FROM citizens)")
                conn.commit()
                conn.close()
                st.error("⚠️ ВИРТУАЛЬНАЯ АВАРИЯ! Шпиндель заклинило от перегрева. Ущерб оборудованию: 4,500,000 ₽. Допуск закрыт. Повторите регламент ТБ.")
