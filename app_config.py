import streamlit as st

def init_page_config():
    """Ініціалізація сторінки та базових налаштувань."""
    st.set_page_config(
        page_title="Analytics Dashboard | Lab 5", 
        layout="wide", 
        page_icon="💎",
        initial_sidebar_state="expanded"
    )

def load_custom_css():
    """Завантаження стилів інтерфейсу."""
    st.markdown("""
    <style>
        /* Глобальні налаштування */
        .block-container { padding-top: 1.5rem; }
        
        /* KPI Метрики */
        [data-testid="stMetric"] {
            background-color: #1a1c24;
            border-left: 5px solid #00bcd4;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
        }
        
        /* Вкладки (Tabs) */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #111827;
            border: 1px solid #374151;
            color: #9ca3af;
            border-radius: 4px;
            padding: 8px 16px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #00bcd4 !important;
            color: black !important;
            font-weight: bold;
            border: none;
        }
        
        /* Контейнери */
        div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
            gap: 1rem;
        }
        
        /* Заголовки */
        h1, h2, h3 { font-family: 'Segoe UI', sans-serif; }
        h3 { color: #00bcd4 !important; }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Бокова панель навігації."""
    with st.sidebar:
        st.title("💎 Analytics Pro")
        st.caption("PCA System v2.0")
        st.markdown("---")
        st.info("**Студент:** Литвиненко Дмитро\n\n**Група:** I-23")
        
        st.markdown("### ⚙️ Налаштування")
        chart_theme = st.selectbox("Тема графіків", ["plotly_dark", "presentation"], index=0)
        st.markdown("---")
        
    return chart_theme