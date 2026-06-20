import streamlit as st
import pandas as pd
import random
import numpy as np

# ==============================================================================
# 1. СТИЛИЗАЦИЯ И ДНК БРЕНДА (Превращаем скучный UI в дорогой продукт)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Экосистема", layout="wide", page_icon="🏭")

# Инъекция фирменных стилей Ассоциации (Промышленный графит + Высокотехнологичный синий)
st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #4A5568; }
        .stTabs [data-baseweb="tab"]:hover { color: #1E3A8A; }
        .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #0284C7; border-bottom-color: #0284C7; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #0F172A; }
        .highlight-box { padding: 20px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ ДАННЫХ
# ==============================================================================
if "app_platform" not in st.session_state:
    st.session_state["app_platform"] = {
        "balance": 25000.00,
        "is_premium": False,
        "courses": [
            {"title": "Отказоустойчивость гидравлических систем", "factory": "АО 'Силовые машины'", "clicks": 1420, "leads": 84, "color": "🔵"},
            {"title": "Программирование ЧПУ циклов серии ИТ-42", "factory": "АО 'Кировский завод'", "clicks": 2850, "leads": 196, "color": "⚙️"},
            {"title": "Метрология и лазерный контроль геометрии", "factory": "Обуховский завод", "clicks": 930, "leads": 41, "color": "🔬"}
        ],
        "leads": [
            {"name": "Александров К.М. (Военмех)", "phone": "+7 (921) 345-67-89", "course": "Программирование ЧПУ циклов серии ИТ-42", "status": "Заморожен", "rating": "⭐ 4.9"},
            {"name": "Дмитриев А.В. (СПбПУ)", "phone": "+7 (911) 987-65-43", "course": "Отказоустойчивость гидравлических систем", "status": "Заморожен", "rating": "⭐ 4.7"}
        ]
    }

db = st.session_state["app_platform"]

# ==============================================================================
# 3. САЙДБАР: СТАТУСНЫЙ ИНТЕРФЕЙС АССОЦИАЦИИ
# ==============================================================================
with st.sidebar:
    st.image("https://icons8.com", width=80)
    st.title("ПромКачество")
    st.caption("Ассоциация промышленных предприятий СПб")
    st.write("---")
    
    user_role = st.selectbox(
        "⚡ Авторизация в контуре:",
        ["🏢 Предприятие / Завод (B2B)", "🎓 Гражданин / Ученик (B2C)", "💥 Маркетолог (Тизерный хаб)"]
    )
    
    st.write("---")
    st.info("ℹ️ Данный прототип демонстрирует сквозную финтех-модель ДПО и лидогенерации для ОПК Санкт-Петербурга.")

# ==============================================================================
# БИЗНЕС-ЛОГИКА: 🏢 КАБИНЕТ ЗАВОДА
# ==============================================================================
if user_role == "🏢 Предприятие / Завод (B2B)":
    st.title("🏢 Кабинет Индустриального Партнера")
    st.subheader("Мониторинг b2b-бюджета и цифрового кадрового следа")
    
    # Живые финтех-метрики
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Финтех-баланс (CPA)", value=f"{db['balance']:,.2f} ₽", delta="Пополнение активно")
    tariff_txt = "БЕЗЛИМИТ" if db["is_premium"] else "CPA (500₽/лид)"
    c2.metric(label="Текущий B2B-тариф", value=tariff_txt)
    c3.metric(label="Всего целевых лидов", value=len(db["leads"]))
    
    if not db["is_premium"]:
        if st.button("🔌 Переключить всю экосистему на Безлимитный Годовой Пакет", use_container_width=True, type="primary"):
            db["is_premium"] = True
            st.success("Экосистема переведена в режим безлимитного трафика!")
            st.rerun()

    # ЖИВАЯ ГРАФИКА (Интересно изучать)
    st.write("---")
    st.subheader("📊 Аналитика вовлечения граждан в реальном времени")
    
    # Генерируем красивый график активности
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Кликбейт-трафик', 'Обучение ДПО', 'Конверсия в Лиды']
    ).cumsum()
    st.line_chart(chart_data)

    # Кадровый резерв
    st.write("---")
    st.subheader("🎯 Поступившие горячие лиды (Кандидаты)")
    
    for idx, lead in enumerate(db["leads"]):
        st.markdown(f"""
        <div class="highlight-box">
            <h4>{lead['course']}</h4>
            <p><b>Рейтинг тестирования:</b> {lead['rating']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        c_info, c_act = st.columns([3, 1])
        is_open = db["is_premium"] or lead["status"] == "Разблокирован"
        c_info.write(f"**ФИО соискателя:** {lead['name'] if is_open else '🔒 Заблокировано финтех-системой (CPA)'}")
        
        if not is_open:
            has_cash = db["balance"] >= 500
            btn_name = "💳 Открыть контакт (500 ₽)" if has_cash else "❌ Пополните счет"
            if c_act.button(btn_name, key=f"b_l_{idx}", use_container_width=True, disabled=not has_cash):
                db["balance"] -= 500
                db["leads"][idx]["status"] = "Разблокирован"
                st.rerun()
        else:
            c_act.success(f"📞 {lead['phone']}")

# ==============================================================================
# БИЗНЕС-ЛОГИКА: 🎓 ПОРТАЛ УЧЕНИКА
# ==============================================================================
elif user_role == "🎓 Гражданин / Ученик (B2C)":
    st.title("🎓 Федеральный образовательный портал ДПО")
    st.subheader("Бесплатное обучение под стандарты крупнейших производств Санкт-Петербурга")
    
    # ЖИВАЯ КАРТА (Та самая изюминка)
    st.write("---")
    st.subheader("📍 Интерактивная карта распределения учебных центров и заводов АПП")
    st.caption("Кликните и перемещайте карту, чтобы увидеть доступные промышленные гиганты")
    
    # Координаты заводов Санкт-Петербурга для интерактива
    map_data = pd.DataFrame({
        'lat': [59.9004, 59.8821, 59.8341],
        'lon': [30.4322, 30.2743, 30.4912],
        'name': ['АО "Силовые машины"', 'АО "Кировский завод"', 'Обуховский завод']
    })
    st.map(map_data, size=40)

    # Список курсов в виде красивых карточек
    st.write("---")
    st.subheader("📋 Доступные программы опережающей подготовки:")
    
    active_key = f"active_c_{user_role}"
    
    for c_idx, course in enumerate(db["courses"]):
        with st.container(border=True):
            col_icon, col_txt, col_btn = st.columns([1, 6, 3])
            col_icon.write(f"# {course['color']}")
            col_txt.write(f"### {course['title']}")
            col_txt.write(f"🏭 Индустриальный автор: **{course['factory']}**")
            
            if col_btn.button("🚀 Начать бесплатное обучение", key=f"st_c_{c_idx}", use_container_width=True):
                st.session_state[active_key] = c_idx
                
                # Генерируем лид
                random_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
                db["leads"].append({
                    "name": f"Выпускник академии №{random.randint(100, 999)}",
                    "phone": f"+7 (931) {random_digits[:3]}-{random_digits[3:5]}-{random_digits[5:]}",
                    "course": course['title'],
                    "status": "Заморожен",
                    "rating": f"⭐ {random.uniform(4.5, 5.0):.1f}"
                })
                st.balloons()
            
            if active_key in st.session_state and st.session_state[active_key] == c_idx:
                st.success("🎯 Доступ к симулятору открыт! Ваше цифровое портфолио формируется в реальном времени.")
                st.markdown("""
                <div style="padding:15px; background-color:#ECFDF5; border-left: 5px solid #10B981; border-radius:4px;">
                    <b>Программа модуля:</b><br>
                    1. Изучение технического регламента оборудования завода.<br>
                    2. Интерактивный 3D-тест на знание ЧПУ / Гидравлики.<br>
                    3. Автоматическая отправка верифицированного резюме в HR-отдел.
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# БИЗНЕС-ЛОГИКА: 💥 МАРКЕТОЛОГ (ТИЗЕРНАЯ СЕТЬ)
# ==============================================================================
elif user_role == "💥 Маркетолог платформы (Трафик)":
    st.title("💥 Тизерный хаб вирусного трафика")
    st.subheader("Механизм сверхдешевого вовлечения граждан Российской Федерации")
    
    st.write("---")
    st.subheader("📈 Эффективность кликбейт-кампаний АПП")
    
    # Красивая сводная таблица аналитики маркетинга
    marketing_df = pd.DataFrame(db["courses"])
    st.dataframe(
        marketing_df[['title', 'factory', 'clicks', 'leads']],
        column_config={
            "title": "Целевой курс ДПО",
            "factory": "Завод-заказчик",
            "clicks": st.column_config.ProgressColumn("Общее число кликов по шок-тизерам", format="%d", min_value=0, max_value=3000),
            "leads": "Сгенерировано горячих лидов"
        },
        use_container_width=True
    )
    
    st.write("---")
    st.subheader("👀 Как это видит обычный гражданин в сети (Пример прокладки):")
    
    st.error("### 🔥 ШОК! Самойлова Оксана подала в суд на Жигана из-за...")
    st.write("...из-за того, что он втайне от неё прошел бесплатное обучение ЧПУ на платформе Ассоциации промышленных предприятий Санкт-Петербурга, устроился на Обуховский завод и скрыл миллионные доходы!")
    
    if st.button("🔗 Протестировать захват клика и переход в ДПО", use_container_width=True):
