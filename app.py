import streamlit as st
import pandas as pd
import random
import numpy as np

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТИЛИ
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Экосистема", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #4A5568; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #0F172A; }
        .highlight-box { padding: 20px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ ИЗ ТРЕБОВАНИЙ АУДИТА (Группировка State)
# ==============================================================================
if "app_platform" not in st.session_state:
    st.session_state["app_platform"] = {
        "balance": 25000.00,
        "is_premium": False,
        "courses": [
            {"id": "c1", "title": "Отказоустойчивость гидравлических систем", "factory": "АО 'Силовые машины'", "clicks": 1420, "leads": 84, "color": "🔵"},
            {"id": "c2", "title": "Программирование ЧПУ циклов серии ИТ-42", "factory": "АО 'Кировский завод'", "clicks": 2850, "leads": 196, "color": "⚙️"},
            {"id": "c3", "title": "Метрология и лазерный контроль геометрии", "factory": "Обуховский завод", "clicks": 930, "leads": 41, "color": "🔬"}
        ],
        "leads": [
            {"id": "l1", "name": "Александров К.М. (Военмех)", "phone": "+7 (921) 345-67-89", "course": "Программирование ЧПУ циклов серии ИТ-42", "status": "Заморожен", "rating": "⭐ 4.9"},
            {"id": "l2", "name": "Дмитриев А.В. (СПбПУ)", "phone": "+7 (911) 987-65-43", "course": "Отказоустойчивость гидравлических систем", "status": "Заморожен", "rating": "⭐ 4.7"}
        ]
    }

# FIX #1: Защита от «Жёсткого сброса». Храним вводы данных студента в глобальной сессии, а не в виджетах
if "student_form_cache" not in st.session_state:
    st.session_state["student_form_cache"] = {"active_course_id": None, "test_passed": False}

db = st.session_state["app_platform"]
cache = st.session_state["student_form_cache"]

# ==============================================================================
# 3. УПРАВЛЕНИЕ ДОСТУПОМ (Сайдбар)
# ==============================================================================
with st.sidebar:
    st.title("ПромКачество")
    st.caption("Ассоциация промышленных предприятий СПб")
    st.write("---")
    user_role = st.selectbox(
        "⚡ Авторизация в контуре:",
        ["🏢 Предприятие / Завод (B2B)", "🎓 Гражданин / Ученик (B2C)", "💥 Маркетолог (Тизерный хаб)"]
    )
    st.write("---")
    st.info("ℹ️ Демонстрация сквозной финтех-модели ДПО для ОПК Санкт-Петербурга.")

st.title("🏭 Цифровая экосистема «ПромКачество.СПб»")
st.caption("Федеральный каркас опережающего ДПО и автоматической лидогенерации")

# ==============================================================================
# 🏢 ИНТЕРФЕЙС РОЛИ: ЗАВОД
# ==============================================================================
if user_role == "🏢 Предприятие / Завод (B2B)":
    st.subheader("Мониторинг b2b-бюджета и цифрового кадрового следа")
    
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Финтех-баланс (CPA)", value=f"{db['balance']:,.2f} ₽")
    tariff_txt = "БЕЗЛИМИТ" if db["is_premium"] else "CPA (500₽/лид)"
    c2.metric(label="Текущий B2B-тариф", value=tariff_txt)
    c3.metric(label="Всего целевых лидов", value=len(db["leads"]))
    
    if not db["is_premium"]:
        if st.button("🔌 Переключить всю экосистему на Безлимитный Годовой Пакет", use_container_width=True, type="primary"):
            db["is_premium"] = True
            st.success("Экосистема переведена в режим безлимитного трафика!")
            st.rerun()

    st.write("---")
    st.subheader("📊 Аналитика вовлечения граждан")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Кликбейт', 'ДПО', 'Лиды']).cumsum()
    st.line_chart(chart_data)

    st.write("---")
    st.subheader("🎯 Поступившие горячие лиды (Кандидаты)")
    
    # FIX #3: Empty States UX. Если список лидов пуст — выводим понятную b2b-заглушку
    if not db["leads"]:
        st.info("💡 На данный момент поступивших лидов нет. Сгенерируйте их, пройдя курс во вкладке 'Гражданин / Ученик'.")
    else:
        for idx, lead in enumerate(db["leads"]):
            with st.container(border=True):
                st.markdown(f"**Курс:** {lead['course']} | **Рейтинг:** {lead['rating']}")
                c_info, c_act = st.columns(2)
                is_open = db["is_premium"] or lead["status"] == "Разблокирован"
                c_info.write(f"**ФИО соискателя:** {lead['name'] if is_open else '🔒 Скрыто системой CPA'}")
                
                if not is_open:
                    # FIX #2: Уникальный ID кнопки через динамический префикс + ID лида
                    has_cash = db["balance"] >= 500
                    btn_name = "💳 Открыть контакт (500 ₽)" if has_cash else "❌ Пополните счет"
                    if c_act.button(btn_name, key=f"factory_buy_{lead['id']}_{idx}", use_container_width=True, disabled=not has_cash):
                        db["balance"] -= 500
                        db["leads"][idx]["status"] = "Разблокирован"
                        st.rerun()
                else:
                    c_act.success(f"📞 {lead['phone']}")

# ==============================================================================
# 🎓 ИНТЕРФЕЙС РОЛИ: УЧЕНИК
# ==============================================================================
elif user_role == "🎓 Гражданин / Ученик (B2C)":
    st.subheader("Бесплатное обучение под стандарты крупнейших производств Санкт-Петербурга")
    
    st.write("---")
    st.subheader("📍 Интерактивная карта заводов АПП")
    map_data = pd.DataFrame({'lat': [59.9004, 59.8821, 59.8341], 'lon': [30.4322, 30.2743, 30.4912]})
    st.map(map_data, size=40)

    st.write("---")
    st.subheader("📋 Доступные программы опережающей подготовки:")
    
    # FIX #3: Empty States UX для каталога курсов
    if not db["courses"]:
        st.warning("⚠️ Каталог курсов пуст. Добавьте программы через административную панель.")
    else:
        for idx, course in enumerate(db["courses"]):
            with st.container(border=True):
                col_icon, col_txt, col_btn = st.columns([1, 5, 2])
                col_icon.write(f"# {course['color']}")
                col_txt.write(f"### {course['title']}")
                col_txt.write(f"🏭 Индустриальный автор: **{course['factory']}**")
                
                # FIX #2: Уникальный ID кнопки курса, предотвращающий падение DuplicateWidgetID
                if col_btn.button("🚀 Начать бесплатное обучение", key=f"student_start_{course['id']}_{idx}", use_container_width=True):
                    cache["active_course_id"] = course['id']
                    cache["test_passed"] = True
                    
                    random_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
                    db["leads"].append({
                        "id": f"gen_l_{random.randint(1000, 9999)}",
                        "name": f"Выпускник академии №{random.randint(100, 999)}",
                        "phone": f"+7 (9xx) {random_digits[:3]}-{random_digits[3:5]}-{random_digits[5:]}",
                        "course": course['title'],
                        "status": "Заморожен",
                        "rating": f"⭐ {random.uniform(4.5, 5.0):.1f}"
                    })
                    st.balloons()
                    st.rerun()
                
                # FIX #1: Логика отрисовки учебного блока опирается строго на сохраненный кэш сессии
                if cache["active_course_id"] == course['id'] and cache["test_passed"]:
                    st.success("🎯 Доступ к симулятору открыт! Ваше цифровое резюме направлено в HR-отдел завода.")
                    st.markdown("""
                    <div style="padding:15px; background-color:#ECFDF5; border-left: 5px solid #10B981; border-radius:4px;">
                        <b>Программа запущенного модуля:</b><br>
                        1. Изучение технического регламента оборудования завода.<br>
                        2. Автоматическая отправка верифицированного резюме в HR-отдел после теста.
                    </div>
                    """, unsafe_allow_html=True)

# ==============================================================================
# 💥 ИНТЕРФЕЙС РОЛИ: МАРКЕТОЛОГ
# ==============================================================================
elif user_role == "💥 Маркетолог платформы (Трафик)":
    st.subheader("Механизм сверхдешевого вовлечения граждан Российской Федерации")
    
    st.write("---")
    st.subheader("📈 Эффективность кликбейт-кампаний АПП")
    
    # FIX #3: Empty States UX. Если данных для графиков маркетинга нет — не ломаем верстку пустой таблицей
    if not db["courses"]:
        st.info("📊 Сводная таблица аналитики пуста. Добавьте курсы в систему.")
    else:
        marketing_df = pd.DataFrame(db["courses"])
        st.dataframe(
            marketing_df[['title', 'factory', 'clicks', 'leads']],
            column_config={
                "title": "Целевой курс ДПО", "factory": "Завод-заказчик",
                "clicks": st.column_config.ProgressColumn("Общее число кликов по шок-тизерам", format="%d", min_value=0, max_value=3000),
                "leads": "Сгенерировано горячих лидов"
            },
            use_container_width=True
        )
    
    st.write("---")
    st.subheader("👀 Как это видит обычный гражданин в сети (Пример прокладки):")
    st.error("### 🔥 ШОК! Самойлова Оксана подала в суд на Жигана из-за...")
