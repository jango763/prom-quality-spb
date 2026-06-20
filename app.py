import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# --- Инициализация сессии ---
if "matches_history" not in st.session_state: st.session_state.matches_history = []
if "bookings_history" not in st.session_state: st.session_state.bookings_history = []
if "parent_leads" not in st.session_state: st.session_state.parent_leads = []

# --- Финтех-данные (Вариант 4) ---
if "sm_factory_balance" not in st.session_state: st.session_state.sm_factory_balance = 1500.00
if "sm_is_premium" not in st.session_state: st.session_state.sm_is_premium = False
if "sm_courses" not in st.session_state:
    st.session_state.sm_courses = [
        {"title": "Работа на токарных станках ЧПУ", "factory": "АО 'Кировский завод'"},
        {"title": "Стандартизация промышленной гидравлики", "factory": "АО 'Силовые машины'"}
    ]
if "sm_leads" not in st.session_state:
    st.session_state.sm_leads = [
        {"name": "Иванов И.И. (СПбПУ)", "phone": "+7 (999) 111-22-33", "course": "Работа на токарных станках ЧПУ", "status": "Заморожен"},
        {"name": "Петров П.Г. (ИТМО)", "phone": "+7 (999) 444-55-66", "course": "Стандартизация гидравлики", "status": "Заморожен"}
    ]

st.title("Экосистема «ПромКачество.СПб»")

# Меню выбора концепции
option = st.sidebar.radio(
    "Выберите концепцию:",
    ("Вариант 1: Кадровый хаб",
     "Вариант 2: Шеринг R&D",
     "Вариант 3: Финтех-навигатор",
     "🔥 Вариант 4: Проект С.М. (Экосистема ДПО)",
     "📊 Панель Ассоциации")
)

# ... (Логика Вариантов 1-3 сохранена) ...

# ================= 🔥 ВАРИАНТ 4: ПРОЕКТ СЕРГЕЯ МАРКОВИЧА =================
elif option == "🔥 Вариант 4: Экосистема ДПО и Лидогенерации (Проект С.М.)":
    st.header("🏭 Экосистема ДПО, Финтеха и Лидогенерации")
    sm_tab1, sm_tab2, sm_tab3 = st.tabs(["🏢 Кабинет Завода", "🎓 Портал Граждан", "💥 Вирусный Трафик"])
    
    with sm_tab1:
        st.subheader("📊 Коммерческая панель")
        col1, col2 = st.columns(2)
        col1.metric("Баланс (CPA)", f"{st.session_state.sm_factory_balance:,.2f} руб.")
        status = "🎯 АКТИВЕН" if st.session_state.sm_is_premium else "🪙 ПОШТУЧНО"
        col2.metric("Тариф", status)
        
        if not st.session_state.sm_is_premium:
            if st.button("🔌 Перейти на безлимит", use_container_width=True):
                st.session_state.sm_is_premium = True
                st.rerun()
                
        st.subheader("🎯 Лиды (Кандидаты)")
        for idx, lead in enumerate(st.session_state.sm_leads):
            with st.container(border=True):
                c_info, c_btn = st.columns([3, 1])
                is_unlocked = st.session_state.sm_is_premium or lead["status"] == "Разблокирован"
                c_info.write(f"**Курс:** {lead['course']}")
                c_info.write(f"**Соискатель:** {lead['name'] if is_unlocked else '🔒 Скрыт'}")
                if not is_unlocked:
                    if c_btn.button("💳 500 р.", key=f"sm_buy_{idx}"):
                        if st.session_state.sm_factory_balance >= 500:
                            st.session_state.sm_factory_balance -= 500
                            st.session_state.sm_leads[idx]["status"] = "Разблокирован"
                            st.rerun()
                else: c_btn.write(f"📞 {lead['phone']}")

    with sm_tab2:
        st.subheader("🎓 Каталог обучения")
        for c_idx, course in enumerate(st.session_state.sm_courses):
            with st.container(border=True):
                st.write(f"### 📚 {course['title']}")
                if st.button("🚀 Пройти обучение", key=f"stud_btn_{c_idx}"):
                    st.session_state.sm_leads.append({"name": "Новый спец", "phone": "+7 911 000", "course": course['title'], "status": "Заморожен"})
                    st.rerun()

    with sm_tab3:
        st.error("🔥 ШОК-КОНТЕНТ: Секрет заработка 300к+ на ЧПУ")
        st.button("УЗНАТЬ ПОДРОБНОСТИ", use_container_width=True)

# ... (Логика Панели Ассоциации) ...
