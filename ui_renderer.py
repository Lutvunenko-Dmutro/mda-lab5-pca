import streamlit as st
import plotly.express as px
from pca_engine import PCAAnalyzer
from report_gen import generate_markdown_report

def render_kpi_block(df, variance):
    """Малює верхній блок з метриками."""
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Об'єкти", df.shape[0], help="Кількість підприємств")
        c2.metric("📈 Змінні", df.shape[1], help="Кількість вхідних параметрів")
        
        quality = variance.iloc[0]['Дисперсія (%)']
        c3.metric("🎯 Сила Фактора 1", f"{quality:.1f}%", delta="Основний вплив")
        
        total = variance.iloc[:2]['Дисперсія (%)'].sum()
        c4.metric("ℹ️ Точність моделі", f"{total:.1f}%", delta="Висока")

def render_data_analysis(df, chart_theme):
    """Малює блок аналізу вхідних даних."""
    st.write("")
    c_left, c_right = st.columns([1.2, 1])
    
    with c_left:
        st.markdown("### 📋 Вхідні дані")
        st.dataframe(
            df, 
            use_container_width=True, 
            height=450,
            column_config={
                c: st.column_config.ProgressColumn(
                    c, format="%.2f", min_value=df[c].min(), max_value=df[c].max()
                ) for c in df.columns
            }
        )
        
    with c_right:
        st.markdown("### 🔗 Кореляція показників")
        fig = px.imshow(df.corr(), text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
        fig.update_layout(template=chart_theme, margin=dict(l=0,r=0,t=0,b=0), height=300)
        st.plotly_chart(fig, use_container_width=True)

# --- ОСНОВНІ ЗМІНИ ТУТ ---
def render_pca_results(analyzer, variance, chart_theme, task_title):
    """Малює результати роботи алгоритму PCA з поясненнями."""
    st.divider()
    
    st.markdown(f"### 📍 Результати аналізу: {task_title}")
    
    st.info(f"**Що ми бачимо?** На графіку нижче кожна точка — це окреме підприємство. Їхнє розташування залежить від показників із завдання **«{task_title}»**.")

    c1, c2 = st.columns([2, 1])
    
    with c1:
        with st.container(border=True):
            if analyzer.results_df.shape[1] >= 2:
                fig = px.scatter(
                    analyzer.results_df, x='Фактор 1', y='Фактор 2', 
                    text=analyzer.results_df.index, size_max=60,
                    color=analyzer.results_df['Фактор 1'], color_continuous_scale='Viridis',
                    hover_name=analyzer.results_df.index,
                    hover_data={'Фактор 1': ':.2f', 'Фактор 2': ':.2f'}
                )
                
                # Додаємо осі (Хрест)
                fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.3)
                fig.add_vline(x=0, line_dash="dash", line_color="white", opacity=0.3)
                
                fig.update_traces(
                    textposition='top center', 
                    marker=dict(size=18, line=dict(width=2, color='#1a1c24')),
                    textfont=dict(size=14, color='white')
                )
                
                fig.update_layout(
                    template=chart_theme, height=450, margin=dict(t=40), 
                    title=f"Карта позиціонування ({task_title})",
                    xaxis_title="Фактор 1 (Ефективність)",
                    yaxis_title="Фактор 2 (Специфіка)"
                )
                st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### ⚖️ Структура")
        with st.container(border=True):
            fig_bar = px.bar(variance, x='Фактор', y='Дисперсія (%)', color='Дисперсія (%)', text_auto='.0f')
            fig_bar.update_layout(template=chart_theme, height=200, showlegend=False, margin=dict(t=30, b=0), title="Вклад факторів")
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.markdown("**Вплив змінних (Loadings)**")
            fig_heat = px.imshow(analyzer.loadings_df, text_auto=".2f", aspect="auto", color_continuous_scale='Teal')
            fig_heat.update_layout(template=chart_theme, height=200, margin=dict(t=0, b=0))
            st.plotly_chart(fig_heat, use_container_width=True)

def render_full_report_tab(data_func, task_title, chart_theme):
    """Збирає всі компоненти в одну вкладку."""
    # 1. Обчислення
    df = data_func()
    analyzer = PCAAnalyzer(df)
    analyzer.run_analysis()
    variance = analyzer.get_explained_variance()
    
    # 2. Рендеринг блоків
    render_kpi_block(df, variance)
    render_data_analysis(df, chart_theme)
    
    # ПЕРЕДАЄМО task_title В ФУНКЦІЮ!
    render_pca_results(analyzer, variance, chart_theme, task_title)
    
    # 3. Звіт
    st.markdown("### 📝 Фінальний звіт")
    with st.container(border=True):
        report = generate_markdown_report(analyzer, variance, task_title)
        st.markdown(report)