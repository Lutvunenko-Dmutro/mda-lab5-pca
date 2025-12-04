import streamlit as st
from data_loader import *
from app_config import init_page_config, load_custom_css, render_sidebar
from ui_renderer import render_full_report_tab

# --- 1. Ініціалізація (Config Layer) ---
init_page_config()
load_custom_css()
chart_theme = render_sidebar()

# --- 2. Головний екран ---
st.title("Аналіз фінансово-економічних показників")
st.markdown("##### Практична робота №5 • Метод головних компонент")

# --- 3. Навігація (Tabs) ---
tabs = st.tabs([
    "🏭 Фондоозброєність", 
    "💰 Премії", 
    "🚀 Продуктивність", 
    "🏗️ Фондовіддача", 
    "🏢 ОВФ"
])

# --- 4. Рендеринг контенту (View Layer) ---
with tabs[0]: 
    render_full_report_tab(get_data_task_1, "Завдання 1", chart_theme)
    
with tabs[1]: 
    render_full_report_tab(get_data_task_2, "Завдання 2", chart_theme)
    
with tabs[2]: 
    render_full_report_tab(get_data_task_3, "Завдання 3", chart_theme)
    
with tabs[3]: 
    render_full_report_tab(get_data_task_4, "Завдання 4", chart_theme)
    
with tabs[4]: 
    render_full_report_tab(get_data_task_5, "Завдання 5", chart_theme)