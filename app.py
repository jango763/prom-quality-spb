import streamlit as st
import pandas as pd

# ==============================================================================
# 1. ТОТАЛЬНЫЙ КУРС НА ПРЕМИУМ-ДИЗАЙН (ИТ-Академия: Графит, Неон, Glassmorphism)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Единая Платформа ДПО", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        /* Импортируем дорогой b2b-шрифт Inter */
        @import url('https://googleapis.com');
        
        /* Полный сброс стилей под концепцию глубокого графита */
        .stApp { 
            background-color: #060913 !important; 
            color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Фикс подписей label: чистый, яркий белый цвет, без серости */
        div[data-testid="stWidgetLabel"] p, label p {
            color: #FFFFFF !important; 
            font-weight: 600 !important; 
            font-size: 14px !important;
            letter-spacing: 0.3px;
        }
        
        /* Премиальный b2b Hero-баннер со сложным градиентом */
        .academy-banner {
            background: linear-gradient(135deg, #0F172A 0%, #020617 100%) !important;
            padding: 45px; 
            border-radius: 20px; 
            color: #FFFFFF; 
            margin-bottom: 35px;
            border: 1px solid rgba(6, 182, 212, 0.15);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7), 0 0 30px rgba(6, 182, 212, 0.05);
        }
        .academy-title { 
            font-size: 32px; 
            font-weight: 800; 
            background: linear-gradient(90deg, #FFFFFF, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        .academy-subtitle { 
            font-size: 15px; 
            color: #94A3B8; 
            margin-top: 12px; 
            line-height: 1.6; 
            font-weight: 400;
        }

        /* Ультра-Glassmorphism контейнеры для форм (эффект матового b2b-стекла) */
        div[data-testid="stForm"], .stAlert {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 16px !important; 
            padding: 35px !important;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8) !important; 
            backdrop-filter: blur(20px) !important;
        }

        /* Объемные карточки KPI с мягким неоновым бирюзовым контуром */
        .pyrus-card {
            background: linear-gradient(145deg, #0F172A, #1E293B) !important;
            border: 1px solid rgba(6, 182, 212, 0.15) !important;
            border-radius: 16px; 
            padding: 25px; 
            margin-bottom: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5), inset 0 0 20px rgba(6, 182, 212, 0.02);
        }
        .pyrus-card-title { 
            font-size: 11px; 
            font-weight: 700; 
            color: #64748B; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
        }
        .pyrus-card-value { 
            font-size: 28px; 
            font-weight: 800; 
            color: #06B6D4; 
            margin-top: 8px; 
            text-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
        }
        
        /* Коробки коммерческих тарифов в стиле ИТ-продуктов */
        .tariff-box {
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            border-radius: 16px; 
            padding: 30px; 
            text-align: center; 
            margin-bottom: 20px;
        }
        .tariff-box.popular {
            border-color: #06B6D4 !important;
            background: rgba(6, 182, 212, 0.02) !important;
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.08) !important;
        }
        .price { 
            font-size: 40px; 
            font-weight: 900; 
            color: #06B6D4; 
            margin: 15px 0; 
            text-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
        }
        .desc { font-size: 13px; color: #64748B; line-height: 1.4; }

        /* Идеальные матовые поля ввода с бирюзовым фокусом */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(2, 6, 17, 0.7) !important; 
            color: #FFFFFF !important;
            font-weight: 500 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important; 
            border-radius: 10px !important;
            padding: 12px !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #06B6D4 !important;
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.25) !important;
        }

        /* Интерактивные вкладки навигации (Tabs) */
        .stTabs [data-baseweb="tab"] { 
            font-size: 16px; 
            font-weight: 600; 
            color: #64748B; 
            padding: 12px 20px !important;
        }
        .stTabs [aria-selected="true"] { 
            color: #06B6D4 !important; 
            border-bottom-color: #06B6D4 !important; 
        }

        /* Текст радио-кнопки */
        div[data-testid="stMarkdownContainer"] p { color: #CBD5E1 !important; font-size: 15px; }
        
        /* Хедер Паспорта навыков */
        .passport-header { 
            background: linear-gradient(90deg, rgba(6, 182, 212, 0.08), transparent); 
            border: 1px solid rgba(6, 182, 212, 0.2); 
            padding: 25px; 
            border-radius: 12px; 
            margin-bottom: 20px; 
        }

        /* Кастомизация прогресс-бара Streamlit под премиум-стандарт */
        div[data-testid="stProgress"] div[role="progressbar"] > div {
            background: linear-gradient(90deg, #38BDF8, #06B6D4) !important;
        }
        
        /* Сайдбар */
        section[data-testid="stSidebar"] { background-color: #030712 !important; border-right: 1px solid rgba(255,255,255,0.03); }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ СКВОЗНОЙ ОПЕРАТИВНОЙ ПАМЯТИ ПЛАТФОРМЫ
# ==============================================================================
if "citizens_data" not in st.session_state:
    st.session_state["citizens_data"] = [
        {"fio": "Никифоров Артур Владимирович", "phone": "+7(921)555-44-33", "email": "artur@mail.ru", "education": "Оператор станков с ЧПУ (5 разряд)", "passport": "4012 987654", "diploma": "№78-05", "workbook": "№ТК-12", "contract_status": "Подписан", "progress": 100, "current_status": "Сертифицированный специалист"}
    ]

if "payments_data" not in st.session_state:
    st.session_state["payments_data"] = [
        {"id": 1, "tariff": "Корпоративный Безлимит", "amount": 150000.0, "timestamp": "2026-03-15 12:00:00"}
    ]

if "courses_data" not in st.session_state:
    st.session_state["courses_data"] = []

# Конвертируем массивы сессии в DataFrame
citizens_df = pd.DataFrame(st.session_state["citizens_data"])
payments_df = pd.DataFrame(st.session_state["payments_data"])
courses_df = pd.DataFrame(st.session_state["courses_data"])
# ==============================================================================
# 3. НАВИГАЦИОННЫЙ СЕЛЕКТОР РОЛЕЙ В САЙДБАРЕ (СТРОГО 2 КАБИНЕТА)
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#06B6D4; font-weight:800; text-shadow: 0 0 15px rgba(6, 182, 212, 0.3);'>🔒 КОНТУР УПРАВЛЕНИЯ</h2>", unsafe_allow_html=True)
    user_role = st.selectbox(
        "Выберите личный кабинет:",
        [
            "🎓 Личный кабинет Гражданина РФ", 
            "🏢 Личный кабинет Производства"
        ]
    )
    st.write("---")
    st.caption("ПромКачество.СПб v3.0")

# Вывод главного индустриального баннера
st.markdown("""
    <div class="academy-banner">
        <div class="academy-title">🏭 Цифровая экосистема опережающего ДПО «ПромКачество»</div>
        <div class="academy-subtitle">Промышленный механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ. Используйте левое меню для переключения между контурами.</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# КОНТУР №1: ГРАЖДАНЕ РФ / СТУДЕНТЫ (Документы, st.progress и тренажер)
# ==============================================================================
if user_role == "🎓 Личный кабинет Гражданина РФ":
    st.markdown("<h3 style='color:#FFFFFF; font-weight:700;'>🎓 Портал обучения и Цифровой Паспорт Навыков</h3>", unsafe_allow_html=True)
    tab_anketa, tab_exam = st.tabs(["📝 Профильная анкета и b2b-верификация", "🤖 Интерактивный mini-тренажер ЧПУ"])
    
    with tab_anketa:
        with st.form("student_form_mono", clear_on_submit=False):
            st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>📂 Загрузка документов соискателя цеха</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            c_fio = col1.text_input("ФИО специалиста полностью:", value="Иванов Игорь Игоревич")
            c_phone = col2.text_input("Номер телефона для связи:", value="+7(900)111-22-33")
            c_email = col3.text_input("Электронная почта (E-mail):", value="ivanov@spb.ru")
            
            col4, col5, col6 = st.columns(3)
            c_pass = col4.text_input("Паспорт РФ (Серия, Номер):", placeholder="4011 123456")
            c_diploma = col5.text_input("Диплом об образовании:", placeholder="№78-01")
            c_work = col6.text_input("Трудовая книжка (Номер):", placeholder="№ТК-99")
            
            c_edu_place = st.selectbox("Направление специализации ДПО:", [
                "Оператор станков с ЧПУ (Токарная группа / стойка Syntec)", 
                "Наладчик станков и манипуляторов с ЧПУ (Фрезерная группа)", 
                "Программирование CAD/CAM систем и симуляция обработки"
            ])
            c_contract = st.selectbox("Статус юридического ученического договора с заводом:", ["Подписан", "Не подписан"])
            c_gdpr = st.checkbox("Согласие на обработку персональных данных сотрудников", value=True)
            
            if st.form_submit_button("Зафиксировать Паспорт Навыков", type="primary"):
                if c_fio.strip() and c_phone.strip():
                    progress = 25
                    if c_pass.strip(): progress += 25
                    if c_diploma.strip(): progress += 25
                    if c_work.strip(): progress += 25
                    if progress > 100: progress = 100
                    
                    st.session_state["citizens_data"].append({
                        "fio": c_fio.strip(), "phone": c_phone.strip(), "email": c_email.strip(), 
                        "education": c_edu_place, "passport": c_pass.strip(), "diploma": c_diploma.strip(), 
                        "workbook": c_work.strip(), "contract_status": c_contract, "progress": progress, "current_status": "Обучение"
                    })
                    st.toast("✓ Документы соискателя успешно зафиксированы!")
                    st.rerun()

        if st.session_state["citizens_data"]:
            curr = st.session_state["citizens_data"][-1]
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="passport-header">
                    <span style='color:#06B6D4; font-weight:700;'>💳 ЦИФРОВОЙ ПАСПОРТ НАВЫКОВ ЭКСПЕРТА:</span> {curr['fio']}<br>
                    <small style='color:#FFFFFF;'>Курс ДПО: {curr.get('education', 'Общий')} | Юридический договор: {curr.get('contract_status', 'Не подписан')}</small>
                </div>
            """, unsafe_allow_html=True)
            prog_val = int(curr.get("progress", 25))
            st.write(f"📊 Текущий процент готовности соискателя на симуляторе: **{prog_val}%**")
            st.progress(prog_val / 100)

    with tab_exam:
        with st.form("exam_form_mono"):
            st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>🤖 Проверка знаний и финальное тестирование ТБ</h4>", unsafe_allow_html=True)
            st.info("КЕЙС: На пульте управления дорогостоящего станка ЧПУ датчик стойки Syntec выдал критический перегрев шпинделя за 20 млн рублей. Каковы ваши экстренные действия в цеху?")
            ans = st.radio("Выберите строго один правильный алгоритм действий:", [
                "Игнорировать предупреждение автоматики и закончить фрезеровку детали",
                "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха",
                "Вручную снизить обороты шпинделя на 20% через потенциометр пульта"
            ], index=None)
            
            if st.form_submit_button("Отправить ответы на проверку экспертам", type="primary"):
                if ans == "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха":
                    if st.session_state["citizens_data"]:
                        st.session_state["citizens_data"][-1]["current_status"] = "Сертифицированный специалист"
                        st.session_state["citizens_data"][-1]["progress"] = 100
                    st.balloons()
                    st.success("🎯 ТЕСТИРОВАНИЕ ПРОЙДЕНО НА 100%! Прогресс на симуляторе выведен на 100%. Вам присвоен статус: СЕРТИФИЦИРОВАННЫЙ СПЕЦИАЛИСТ.")
                else:
                    st.error("❌ ОШИБКА В РЕГЛАМЕНТЕ! Произошла авария шпинделя. Допуск заблокирован. Повторите технику безопасности.")

# ==============================================================================
# КОНТУР №2: ПРОИЗВОДСТВА (ЗАВОДЫ)
# ==============================================================================
elif user_role == "🏢 Личный кабинет Производства":
    st.markdown("<h3 style='color:#FFFFFF; font-weight:700;'>🏢 Портал Партнеров и Интеграторов промышленного оборудования</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="pyrus-card"><div class="pyrus-card-title">ЛИЦЕНЗИЯ ПРЕДПРИЯТИЯ</div><div class="pyrus-card-value">ПОШТУЧНЫЙ НАЙМ</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="pyrus-card"><div class="pyrus-card-title">ДОСТУПНО ВЫГРУЗОК HR</div><div class="pyrus-card-value" style="color: #3B82F6;">5 ЭКСПЕРТОВ</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="pyrus-card"><div class="pyrus-card-title">ЦЕНТР КОМПЕТЕНЦИЙ</div><div class="pyrus-card-value" style="color: #EF4444;">❌ НЕ СОЗДАН</div></div>', unsafe_allow_html=True)

    tab_tariffs, tab_dpo = st.tabs(["💳 Тарифные программы обучения", "📥 Публикация стандартов ДПО Завода"])
    
    with tab_tariffs:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown('<div class="tariff-box"><h5>📦 Штучный пакет обучения</h5><div class="price">19 990 ₽</div><div class="desc">Доступ к профильной программе автоматизации цеха и 1 допуску соискателя</div></div>', unsafe_allow_html=True)
            if st.button("Купить штучный пакет", key="b1_mono", use_container_width=True):
                st.session_state["payments_data"].append({"id": len(st.session_state["payments_data"])+1, "tariff": "Штучный курс", "amount": 19990.0, "timestamp": "Только что"})
                st.toast("✓ Транзакция зафиксирована!")
                st.rerun()
        with col_t2:
            st.markdown('<div class="tariff-box popular"><h5>⚔️ Корпоративный Безлимит</h5><div class="price">150 000 ₽</div><div class="desc">Полное обучение и сертификация до 50 внутренних экспертов предприятия</div></div>', unsafe_allow_html=True)
            if st.button("Активировать Безлимит", key="b2_mono", use_container_width=True, type="primary"):
                st.session_state["payments_data"].append({"id": len(st.session_state["payments_data"])+1, "tariff": "Корпоративный Безлимит", "amount": 150000.0, "timestamp": "Только что"})
                st.toast("✓ Годовая b2b-подписка активирована!")
                st.rerun()

    with tab_dpo:
        with st.form("dpo_form_m"):
            st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>📥 Загрузка новой программы опережающего ДПО под станки</h4>", unsafe_allow_html=True)
            f_inn = st.text_input("ИНН промышленного предприятия:")
            f_title = st.text_input("Название обучающего трека ДПО:")
            f_model = st.text_input("Модель отечественного станка ЧПУ:")
            f_text = st.text_area("Введите инструкции и регламенты безопасности:")
            
            if st.form_submit_button("Опубликовать стандарт завода", use_container_width=True):
                if f_inn.strip() and f_title.strip():
                    st.session_state["courses_data"].append({"inn": f_inn.strip(), "title": f_title.strip(), "model": f_model.strip(), "text": f_text.strip()})
                    st.success("✓ Новый промышленный стандарт ДПО успешно занесен в реестр платформы!")
                    st.rerun()
