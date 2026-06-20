import streamlit as st
import pandas as pd

# Настройка страницы в стиле B2B
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# --- ИНИЦИАЛИЗАЦИЯ СЕССИИ (Сохранение данных) ---
if "sm_balance" not in st.session_state: st.session_state.sm_balance = 1500.00
if "sm_premium" not in st.session_state: st.session_state.sm_premium = False
if "sm_leads" not in st.session_state:
    st.session_state.sm_leads = [
        {"name": "Иванов Иван Игоревич (СПбПУ)", "phone": "+7 (999) 111-22-33", "course": "Работа на токарных станках ЧПУ серии ИТ-42", "status": "Заморожен"},
        {"name": "Петров Петр Георгиевич (ИТМО)", "phone": "+7 (999) 444-55-66", "course": "Стандартизация промышленной гидравлики", "status": "Заморожен"}
    ]

st.title("Экосистема «ПромКачество.СПб»")
st.sidebar.title("Навигация")
option = st.sidebar.radio("Выберите вариант:", ["🔥 Вариант 4: Экосистема ДПО (Проект С.М.)"])

# ================= 🔥 ВАРИАНТ 4 (ПРОЕКТ С.М.) =================
if option == "🔥 Вариант 4: Экосистема ДПО (Проект С.М.)":
    st.header("🚀 Концепция: Промышленное ДПО + Финтех")
    sm_tab1, sm_tab2 = st.tabs(["🏢 Кабинет Завода", "🎓 Портал обучения"])
    
    with sm_tab1:
        st.subheader("📊 Финтех-панель")
        c1, c2 = st.columns(2)
        c1.metric(label="Баланс (CPA)", value=f"{st.session_state.sm_balance:,.2f} руб.")
        status_text = "АКТИВЕН" if st.session_state.sm_premium else "ПОШТУЧНО"
        c2.metric(label="Тариф", value=status_text)
        
        if not st.session_state.sm_premium and st.button("🔌 Активировать Безлимит"):
            st.session_state.sm_premium = True
            st.success("Пакет активен!")
            st.rerun()
                
        st.write("---")
        st.subheader("🎯 Поступившие Лиды")
        for idx, lead in enumerate(st.session_state.sm_leads):
            with st.container(border=True):
                col_info, col_btn = st.columns([3, 1])
                is_access = st.session_state.sm_premium or lead["status"] == "Разблокирован"
                col_info.write(f"**Курс:** {lead['course']}")
                col_info.write(f"**Специалист:** {lead['name'] if is_access else '🔒 Скрыто'}")
                if not is_access and col_btn.button("💳 Выкупить (500 р.)", key=f"sm_b_{idx}"):
                    if st.session_state.sm_balance >= 500:
                        st.session_state.sm_balance -= 500
                        st.session_state.sm_leads[idx]["status"] = "Разблокирован"
                        st.rerun()
                    else: st.error("Нет средств!")
                elif is_access: col_btn.write(f"📞 **{lead['phone']}**")

    with sm_tab2:
        st.write("🎓 Бесплатные курсы...")
