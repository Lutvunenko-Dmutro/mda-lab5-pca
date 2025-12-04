import pandas as pd

def generate_markdown_report(analyzer, variance_df, task_name):
    """Генерує структурований текст звіту."""
    report = []
    
    # Дані
    f1 = variance_df.iloc[0]['Дисперсія (%)']
    f2 = variance_df.iloc[1]['Дисперсія (%)'] if len(variance_df) > 1 else 0
    total = f1 + f2
    quality = "високий" if total > 75 else "достатній"
    
    # Заголовок
    report.append(f"#### Аналітичне резюме: {task_name}")
    report.append("---")
    
    # Блок 1
    report.append(f"**1. Якість моделі:**\n")
    report.append(f"Модель зберігає **{total:.2f}%** інформації, що є показником рівня **«{quality}»**.")
    report.append(f"- Вплив Фактора 1: `{f1:.2f}%`")
    report.append(f"- Вплив Фактора 2: `{f2:.2f}%`\n")
    
    # Блок 2
    loadings = analyzer.loadings_df
    top_f1 = loadings['Фактор 1'].abs().idxmax()
    val_f1 = loadings.loc[top_f1, 'Фактор 1']
    
    report.append(f"**2. Інтерпретація:**\n")
    report.append(f"Ключовим драйвером диференціації є показник **«{top_f1}»** (навантаження: {val_f1:.3f}). Саме він найбільше впливає на позицію підприємства в рейтингу.")
    
    # Блок 3
    report.append(f"\n**3. Топ-3 лідерів (за Фактором 1):**")
    results = analyzer.results_df.sort_values(by='Фактор 1', ascending=False)
    for i, (idx, row) in enumerate(results.head(3).iterrows(), 1):
        report.append(f"{i}. **Підприємство №{idx}** (Індекс: {row['Фактор 1']:.3f})")
        
    return "\n".join(report)