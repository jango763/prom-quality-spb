import streamlit as st
import streamlit.components.v1 as components
import sqlite3

# Скрываем стандартную оболочку Streamlit, освобождая экран под дизайн CodePen
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0px !important; margin: 0px !important; max-width: 100% !important;}
        iframe {border: none !important; width: 100% !important; min-height: 100vh !important;}
    </style>
""", unsafe_allow_html=True)

# Инициализация расширенной СУБД SQLite
DB_NAME = "production_control_enterprise_v5.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT, phone TEXT, email TEXT, edu TEXT,
            passport TEXT, diploma TEXT, workbook TEXT, skills TEXT, status TEXT DEFAULT 'Обучение'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inn TEXT, title TEXT, model TEXT, text TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tariff TEXT, amount REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# ПЕРЕХВАТ ДАННЫХ ИЗ ФРОНТЕНДА ЧЕРЕЗ БЕЗОПАСНЫЙ URL QUERY-МОСТ
# ==============================================================================
query_params = st.query_params

if "action" in query_params:
    action = query_params["action"]
    
    # 1. Запись полной b2c-анкеты соискателя гражданина РФ
    if action == "citizen_reg":
        conn = sqlite3.connect(DB_NAME)
        conn.execute("""
            INSERT INTO citizens (fio, phone, email, edu, passport, diploma, workbook, skills) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (query_params.get("fio"), query_params.get("phone"), query_params.get("email"), query_params.get("edu"),
              query_params.get("pass"), query_params.get("diploma"), query_params.get("work"), query_params.get("skills")))
        conn.commit()
        conn.close()
        st.toast(f"🏭 Бэкенд: Успешно сохранена анкета {query_params.get('fio')}!")
        
    # 2. Обработка теста компетенций
    elif action == "submit_test":
        is_correct = (query_params.get("q1") == "correct")
        conn = sqlite3.connect(DB_NAME)
        if is_correct:
            conn.execute("UPDATE citizens SET status = 'Железный специалист' WHERE id = (SELECT max(id) FROM citizens)")
            st.toast("🎯 Экзамен сдан! Кандидату присвоен статус 'Железный специалист'")
        else:
            st.toast("⚠️ Виртуальная авария шпинделя! Тест провален.")
        conn.commit()
        conn.close()
        
    # 3. Фиксация покупки безлимитных / поштучных тарифов заводов
    elif action == "buy_tariff":
        t_type = query_params.get("tariff")
        amt = 150000.0 if t_type == "unlimit" else 15000.0
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO payments (tariff, amount) VALUES (?, ?)", (t_type, amt))
        conn.commit()
        conn.close()
        st.toast(f"💳 Проведена транзакция пакета {t_type} на сумму {amt:,.0f} ₽!")
        
    # 4. Сохранение b2b-стандартов обучения ДПО
    elif action == "upload_dpo":
        conn = sqlite3.connect(DB_NAME)
        conn.execute("""
            INSERT INTO courses (inn, title, model, text) VALUES (?, ?, ?, ?)
        """, (query_params.get("inn"), query_params.get("title"), query_params.get("model"), query_params.get("text")))
        conn.commit()
        conn.close()
        st.toast("📥 Стандарт ДПО успешно опубликован в базе АПП!")

    # Мгновенно зачищаем URL, чтобы избежать бесконечного зацикливания СУБД при обновлении страницы
    active_panel = query_params.get("panel", "citizen")
    st.query_params.clear()
    st.query_params["panel"] = active_panel

# Извлекаем агрегированные данные из базы для вывода в шапку и таблицы Ассоциации
conn = sqlite3.connect(DB_NAME)
c_list = conn.execute("SELECT * FROM citizens").fetchall()
co_list = conn.execute("SELECT * FROM courses").fetchall()
p_list = conn.execute("SELECT * FROM payments").fetchall()
conn.close()

total_phys_val = len(c_list) if c_list else 1420
total_revenue_val = sum(p[2] for p in p_list) if p_list else 165000

# Определяем, какую вкладку отобразить активной на основе сессии Streamlit
current_panel = st.query_params.get("panel", "citizen")

# ==============================================================================
# ТОЧНАЯ ПИКСЕЛЬНАЯ КИБЕРПАНК-КОПИЯ ВЕРСТКИ С CODEPEN (Используем чистый r"")
# ==============================================================================
html_code = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <style>
        * { box-sizing: border-box; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        body { background-color: #0B0F19 !important; color: #F8FAFC !important; margin: 0; padding: 0; overflow-x: hidden; }
        .cyber-app-container { display: flex; min-height: 100vh; }
        
        .cyber-sidebar {
            width: 320px; background: #0D1322; border-right: 1px solid rgba(255, 255, 255, 0.05);
            padding: 30px 20px; display: flex; flex-direction: column; justify-content: space-between;
        }
        .sidebar-header { display: flex; align-items: center; gap: 10px; }
        .cyber-sidebar h2 { font-size: 20px; font-weight: 800; color: #10B981; margin: 0; text-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }
        .cyber-pulse-dot { width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; box-shadow: 0 0 10px #10B981; }
        .role-selector-box label { font-size: 13px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .role-selector-box select { width: 100%; padding: 12px; background: #111827; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; color: #F8FAFC; font-weight: 600; margin-top: 8px; cursor: pointer; }
        .sidebar-footer { font-size: 12px; color: #475569; font-weight: 600; }

        .cyber-main { flex-grow: 1; padding: 30px; max-width: 1200px; }
        .hero-banner { background: linear-gradient(135deg, #0F172A 0%, #111827 100%) !important; padding: 35px; border-radius: 16px; color: #FFFFFF; margin-bottom: 25px; border-left: 8px solid #10B981; box-shadow: 0 0 25px rgba(16, 185, 129, 0.15); }
        .hero-title { font-size: 28px; font-weight: 800; background: linear-gradient(90deg, #10B981, #34D399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero-subtitle { font-size: 14px; color: #94A3B8; margin-top: 8px; line-height: 1.4; }

        .cyber-panel { display: none; width: 100%; }
        .cyber-panel.active { display: block; animation: fadeIn 0.4s ease-in-out forwards; }
        .cyber-panel h3 { font-size: 22px; font-weight: 700; color: #F8FAFC; margin-bottom: 20px; }
        .glass-form { background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 14px; padding: 25px; margin-bottom: 20px; backdrop-filter: blur(12px); }
        .glass-form h4 { margin-top: 0; margin-bottom: 20px; font-size: 16px; color: #34D399; font-weight: 700; }
        
        .form-grid, .form-grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 15px; }
        .glass-card { background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px; }
        .card-title { font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-value { font-size: 24px; font-weight: 800; color: #10B981; margin-top: 5px; }
        
        .tariff-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .tariff-box { background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 25px; text-align: center; }
        .tariff-box.popular { border-color: #10B981; background: rgba(16, 185, 129, 0.02); box-shadow: 0 0 20px rgba(16, 185, 129, 0.05); }
        .price { font-size: 36px; font-weight: 900; color: #10B981; margin: 10px 0; }
        .desc { font-size: 13px; color: #94A3B8; }

        input, textarea, select { width: 100%; padding: 12px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; color: #F8FAFC; font-size: 14px; margin-bottom: 10px; }
        input:focus, textarea:focus { border-color: #10B981; outline: none; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2); }
        .question { font-weight: 600; color: #E2E8F0; }
        .radio-group label { display: block; padding: 10px; background: rgba(255, 255, 255, 0.02); margin-top: 8px; border-radius: 6px; cursor: pointer; }
        .checkbox-line { display: flex; align-items: center; gap: 8px; }
        .checkbox-line input { width: auto; margin: 0; }

        .cyber-btn, .cyber-btn-buy { background: linear-gradient(90deg, #10B981, #059669); border: none; color: white; padding: 12px 24px; font-weight: 700; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2); transition: transform 0.2s; width: 100%; font-size:14px; }
        .cyber-btn:hover, .cyber-btn-buy:hover { transform: translateY(-2px); }

        .cyber-table-container { overflow-x: auto; }
        .cyber-table { width: 100%; border-collapse: collapse; }
        .cyber-table th, .cyber-table td { padding: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); text-align: left; }
