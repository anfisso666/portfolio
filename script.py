import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List
import warnings
import io
import base64
from IPython.display import display, HTML
warnings.filterwarnings('ignore')
import altair as alt

def create_pie_charts(df):
    """
    Создает три круговые диаграммы для анализа зарплат
    """
    # Создаем фигуру с тремя подграфиками
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Цветовые палитры для каждой диаграммы
    colors1 = plt.cm.Set3(np.linspace(0, 1, 12))
    colors2 = plt.cm.Pastel1(np.linspace(0, 1, 12))
    colors3 = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # 1. Диаграмма по должностям (job_title)
    job_salary = df.groupby('job_title')['salary_in_usd'].sum()
    # Берем топ-10 должностей для читаемости
    job_salary_top = job_salary.nlargest(10)
    
    wedges1, texts1, autotexts1 = axes[0].pie(
        job_salary_top.values, 
        labels=job_salary_top.index,
        autopct='%1.1f%%',
        colors=colors1,
        startangle=90,
        textprops={'fontsize': 8}
    )
    axes[0].set_title('Распределение зарплат по должностям\n(топ-10)', fontsize=12, fontweight='bold')
    
    # Делаем текст процентов более заметным
    for autotext in autotexts1:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    # 2. Диаграмма по странам (employee_residence)
    df_countries = df.copy()
    df_countries['country_name'] = df_countries['employee_residence'].map(sc.country_codes)
    df_countries['country_name'] = df_countries['country_name'].fillna(df_countries['employee_residence'])
    
    country_salary = df_countries.groupby('country_name')['salary_in_usd'].sum()
    # Берем топ-10 стран для читаемости
    country_salary_top = country_salary.nlargest(10)
    
    wedges2, texts2, autotexts2 = axes[1].pie(
        country_salary_top.values,
        labels=country_salary_top.index,
        autopct='%1.1f%%',
        colors=colors2,
        startangle=90,
        textprops={'fontsize': 8}
    )
    axes[1].set_title('Распределение зарплат по странам\n(топ-10)', fontsize=12, fontweight='bold')
    
    # Делаем текст процентов более заметным
    for autotext in autotexts2:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    # 3. Диаграмма по типу работы (remote_ratio)
    df_remote = df.copy()
    df_remote['work_type'] = df_remote['remote_ratio'].map(sc.remote_ratio_dict)
    
    remote_salary = df_remote.groupby('work_type')['salary_in_usd'].sum()
    
    wedges3, texts3, autotexts3 = axes[2].pie(
        remote_salary.values,
        labels=remote_salary.index,
        autopct='%1.1f%%',
        colors=colors3,
        startangle=90,
        textprops={'fontsize': 10}
    )
    axes[2].set_title('Распределение зарплат по типу работы', fontsize=12, fontweight='bold')
    
    # Делаем текст процентов более заметным
    for autotext in autotexts3:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # Настройка общего вида
    plt.tight_layout()
    plt.suptitle('Анализ распределения зарплат по различным категориям', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    # Показываем график
    plt.show()

def prepare_data(df):
    """Подготовка данных для анализа"""
    # Создаем копию данных
    df_clean = df.copy()
    
    # Преобразуем коды стран в названия
    df_clean['country_name'] = df_clean['employee_residence'].map(sc.country_codes)
    df_clean['country_name'] = df_clean['country_name'].fillna(df_clean['employee_residence'])
    
    # Преобразуем remote_ratio в текстовые описания
    df_clean['remote_work'] = df_clean['remote_ratio'].map(sc.remote_ratio_dict)
    df_clean['remote_work'] = df_clean['remote_work'].fillna('Неизвестно')
    
    return df_clean

def analyze_top_performers(df):
    """Анализ топовых специалистов, стран и форматов работы"""
    
    # ТОП-5 самых высокооплачиваемых должностей
    top_jobs = df.groupby('job_title')['salary_in_usd'].agg(['mean', 'count']).reset_index()
    top_jobs = top_jobs[top_jobs['count'] >= 5]  # Фильтруем должности с минимум 5 записями
    top_jobs = top_jobs.sort_values('mean', ascending=False).head(5)
    
    # ТОП-5 самых высокооплачиваемых стран
    top_countries = df.groupby('country_name')['salary_in_usd'].agg(['mean', 'count']).reset_index()
    top_countries = top_countries[top_countries['count'] >= 5]  # Фильтруем страны с минимум 5 записями
    top_countries = top_countries.sort_values('mean', ascending=False).head(5)
    
    # Наиболее высокооплачиваемый формат работы
    remote_analysis = df.groupby('remote_work')['salary_in_usd'].agg(['mean', 'count']).reset_index()
    remote_analysis = remote_analysis.sort_values('mean', ascending=False)
    
    return top_jobs, top_countries, remote_analysis

def create_portrait(df):
    """Создание портрета идеального специалиста"""
    
    # Находим характеристики с самой высокой средней зарплатой
    best_job = df.groupby('job_title')['salary_in_usd'].mean().idxmax()
    best_country = df.groupby('country_name')['salary_in_usd'].mean().idxmax()
    best_remote = df.groupby('remote_work')['salary_in_usd'].mean().idxmax()
    
    # Получаем значения зарплат
    job_salary = df.groupby('job_title')['salary_in_usd'].mean().max()
    country_salary = df.groupby('country_name')['salary_in_usd'].mean().max()
    remote_salary = df.groupby('remote_work')['salary_in_usd'].mean().max()
    
    return {
        'job': (best_job, job_salary),
        'country': (best_country, country_salary),
        'remote': (best_remote, remote_salary)
    }

def portrait_main_analysis(df):
    """Основная функция анализа"""
    
    # # Подготавливаем данные
    df_clean = prepare_data(df)
    
    # Анализируем топовых исполнителей
    top_jobs, top_countries, remote_analysis = analyze_top_performers(df_clean)
    
    # Создаем портрет идеального специалиста
    portrait = create_portrait(df_clean)
    
    # Выводим результаты
    print("\nПОРТРЕТ ИДЕАЛЬНОГО СПЕЦИАЛИСТА:")
    print(f"   Должность: {portrait['job'][0]} (средняя зарплата: ${portrait['job'][1]:,.0f})")
    print(f"   Страна проживания: {portrait['country'][0]} (средняя зарплата: ${portrait['country'][1]:,.0f})")
    print(f"   Формат работы: {portrait['remote'][0]} (средняя зарплата: ${portrait['remote'][1]:,.0f})")
    
    print("\nТОП-5 САМЫХ ВЫСОКООПЛАЧИВАЕМЫХ ДОЛЖНОСТЕЙ:")
    for i, row in top_jobs.iterrows():
        print(f"   {top_jobs.index.get_loc(i)+1}. {row['job_title']}: ${row['mean']:,.0f} (выборка: {row['count']} чел.)")
    
    print("\nТОП-5 САМЫХ ВЫСОКООПЛАЧИВАЕМЫХ СТРАН:")
    for i, row in top_countries.iterrows():
        print(f"   {top_countries.index.get_loc(i)+1}. {row['country_name']}: ${row['mean']:,.0f} (выборка: {row['count']} чел.)")
    
    print("\nРЕЙТИНГ ФОРМАТОВ РАБОТЫ ПО ЗАРПЛАТЕ:")
    for i, row in remote_analysis.iterrows():
        print(f"   {remote_analysis.index.get_loc(i)+1}. {row['remote_work']}: ${row['mean']:,.0f} (выборка: {row['count']} чел.)")
    
    return df_clean

def analyze_international_work(df):
    """
    Анализ международной работы и удаленной занятости
    """
    
    # Словарь для замены кодов стран на названия
    country_codes = {
        'ES': 'Испания', 'US': 'Соединенные Штаты Америки', 'CA': 'Канада', 'DE': 'Германия', 'GB': 'Великобритания', 'NG': 'Нигерия', 
        'IN': 'Индия', 'HK': 'Гонконг', 'PT': 'Португалия', 'NL': 'Нидерланды', 'CH': 'Швейцария', 'CF': 'Центральноафриканская Республика', 
        'FR': 'Франция', 'AU': 'Австралия', 'FI': 'Финляндия', 'UA': 'Украина', 'IE': 'Ирландия', 'IL': 'Израиль', 'GH': 'Гана', 'AT': 'Австрия',
        'CO': 'Колумбия', 'SG': 'Сингапур', 'SE': 'Швеция', 'SI': 'Словения', 'MX': 'Мексика', 'UZ': 'Узбекистан', 'BR': 'Бразилия', 
        'TH': 'Таиланд', 'HR': 'Хорватия', 'PL': 'Польша', 'KW': 'Кувейт', 'VN': 'Вьетнам', 'CY': 'Кипр', 'AR': 'Аргентина', 'AM': 'Армения', 
        'BA': 'Босния и Герцеговина', 'KE': 'Кения', 'GR': 'Греция', 'MK': 'Северная Македония', 'LV': 'Латвия', 'RO': 'Румыния', 
        'PK': 'Пакистан', 'IT': 'Италия', 'MA': 'Марокко', 'LT': 'Литва', 'BE': 'Бельгия', 'AS': 'Американское Самоа', 'IR': 'Иран', 
        'HU': 'Венгрия', 'SK': 'Словакия', 'CN': 'Китай', 'CZ': 'Чехия', 'CR': 'Коста-Рика', 'TR': 'Турция', 'CL': 'Чили', 'PR': 'Пуэрто-Рико', 
        'DK': 'Дания', 'BO': 'Боливия', 'PH': 'Филиппины', 'DO': 'Доминиканская Республика', 'EG': 'Египет', 'ID': 'Индонезия', 
        'AE': 'Объединенные Арабские Эмираты', 'MY': 'Малайзия', 'JP': 'Япония', 'EE': 'Эстония', 'HN': 'Гондурас', 'TN': 'Тунис', 
        'RU': 'Россия', 'DZ': 'Алжир', 'IQ': 'Ирак', 'BG': 'Болгария', 'JE': 'Джерси', 'RS': 'Сербия', 'NZ': 'Новая Зеландия', 'MD': 'Молдова', 
        'LU': 'Люксембург', 'MT': 'Мальта'
    }
    
    # Заменяем коды стран в salary_currency на названия
    if 'salary_currency' in df.columns:
        df['salary_currency'] = df['salary_currency'].map(country_codes).fillna(df['salary_currency'])
    
    # Создаем признак "работает в другой стране"
    df['works_internationally'] = df['employee_residence'] != df['company_location']
    
    international_workers = df['works_internationally'].sum()
    
    # Анализ по странам проживания
    print("\n=== ТОП-10 СТРАН ПО КОЛИЧЕСТВУ ПРОЖИВАЮЩИХ ===")
    residence_stats = df.groupby('employee_residence').agg({
        'works_internationally': ['count', 'sum', 'mean'],
        'remote_ratio': 'mean'
    }).round(3)
    
    residence_stats.columns = ['total_people', 'international_workers', 
                              'international_rate', 'avg_remote_ratio']
    
    # Сортируем по количеству людей
    top_countries = residence_stats.sort_values('total_people', ascending=False).head(10)
    
    for country, row in top_countries.iterrows():
        country_name = country_codes.get(country, country)
        print(f"{country_name}: {int(row['total_people'])} чел., "
              f"{row['international_rate']:.1%} работают международно")
    
    return top_countries, df

def create_visualizations(df, top_countries):
    """
    Создание визуализаций с fallback 
    """
    
    # Словарь для замены кодов стран
    country_codes = {
        'ES': 'Испания', 'US': 'Соединенные Штаты Америки', 'CA': 'Канада', 'DE': 'Германия', 'GB': 'Великобритания', 'NG': 'Нигерия', 
        'IN': 'Индия', 'HK': 'Гонконг', 'PT': 'Португалия', 'NL': 'Нидерланды', 'CH': 'Швейцария', 'CF': 'Центральноафриканская Республика', 
        'FR': 'Франция', 'AU': 'Австралия', 'FI': 'Финляндия', 'UA': 'Украина', 'IE': 'Ирландия', 'IL': 'Израиль', 'GH': 'Гана', 'AT': 'Австрия',
        'CO': 'Колумбия', 'SG': 'Сингапур', 'SE': 'Швеция', 'SI': 'Словения', 'MX': 'Мексика', 'UZ': 'Узбекистан', 'BR': 'Бразилия', 
        'TH': 'Таиланд', 'HR': 'Хорватия', 'PL': 'Польша', 'KW': 'Кувейт', 'VN': 'Вьетнам', 'CY': 'Кипр', 'AR': 'Аргентина', 'AM': 'Армения', 
        'BA': 'Босния и Герцеговина', 'KE': 'Кения', 'GR': 'Греция', 'MK': 'Северная Македония', 'LV': 'Латвия', 'RO': 'Румыния', 
        'PK': 'Пакистан', 'IT': 'Италия', 'MA': 'Марокко', 'LT': 'Литва', 'BE': 'Бельгия', 'AS': 'Американское Самоа', 'IR': 'Иран', 
        'HU': 'Венгрия', 'SK': 'Словакия', 'CN': 'Китай', 'CZ': 'Чехия', 'CR': 'Коста-Рика', 'TR': 'Турция', 'CL': 'Чили', 'PR': 'Пуэрто-Рико', 
        'DK': 'Дания', 'BO': 'Боливия', 'PH': 'Филиппины', 'DO': 'Доминиканская Республика', 'EG': 'Египет', 'ID': 'Индонезия', 
        'AE': 'Объединенные Арабские Эмираты', 'MY': 'Малайзия', 'JP': 'Япония', 'EE': 'Эстония', 'HN': 'Гондурас', 'TN': 'Тунис', 
        'RU': 'Россия', 'DZ': 'Алжир', 'IQ': 'Ирак', 'BG': 'Болгария', 'JE': 'Джерси', 'RS': 'Сербия', 'NZ': 'Новая Зеландия', 'MD': 'Молдова', 
        'LU': 'Люксембург', 'MT': 'Мальта'
    }
    
    # График 1: Международные работники по странам
    chart1_data = top_countries.reset_index()
    chart1_data['country_name'] = chart1_data['employee_residence'].map(country_codes).fillna(chart1_data['employee_residence'])
    
    chart1 = alt.Chart(chart1_data).mark_bar().encode(
        x=alt.X('country_name:N', sort='-y', title='Страна проживания'),
        y=alt.Y('international_rate:Q', title='Доля международных работников'),
        color=alt.Color('international_rate:Q', scale=alt.Scale(scheme='viridis')),
        tooltip=['country_name', 'total_people', 'international_rate']
    ).properties(
        title='Доля людей, работающих в другой стране (топ-10 стран)',
        width=600,
        height=400
    )
   
    return chart1.show()
        
def f_main_analysis(df):
    """
    Главная функция для полного анализа
    """
    
    # Выполняем анализ
    top_countries, df_enhanced = analyze_international_work(df)
    
    # Создаем визуализации
    charts = create_visualizations(df_enhanced, top_countries)
    
    # Выводы
    print("\n" + "=" * 60)
    print("ВЫВОДЫ:")
    print("=" * 60)
    
    international_rate = (df_enhanced['works_internationally'].sum() / len(df_enhanced)) * 100
    
    print(f"1. {international_rate:.1f}% работников трудятся в другой стране от места проживания")
    
    # Словарь для замены кодов стран в выводах
    country_codes = {
        'ES': 'Испания', 'US': 'Соединенные Штаты Америки', 'CA': 'Канада', 'DE': 'Германия', 'GB': 'Великобритания', 'NG': 'Нигерия', 
        'IN': 'Индия', 'HK': 'Гонконг', 'PT': 'Португалия', 'NL': 'Нидерланды', 'CH': 'Швейцария', 'CF': 'Центральноафриканская Республика', 
        'FR': 'Франция', 'AU': 'Австралия', 'FI': 'Финляндия', 'UA': 'Украина', 'IE': 'Ирландия', 'IL': 'Израиль', 'GH': 'Гана', 'AT': 'Австрия',
        'CO': 'Колумбия', 'SG': 'Сингапур', 'SE': 'Швеция', 'SI': 'Словения', 'MX': 'Мексика', 'UZ': 'Узбекистан', 'BR': 'Бразилия', 
        'TH': 'Таиланд', 'HR': 'Хорватия', 'PL': 'Польша', 'KW': 'Кувейт', 'VN': 'Вьетнам', 'CY': 'Кипр', 'AR': 'Аргентина', 'AM': 'Армения', 
        'BA': 'Босния и Герцеговина', 'KE': 'Кения', 'GR': 'Греция', 'MK': 'Северная Македония', 'LV': 'Латвия', 'RO': 'Румыния', 
        'PK': 'Пакистан', 'IT': 'Италия', 'MA': 'Марокко', 'LT': 'Литва', 'BE': 'Бельгия', 'AS': 'Американское Самоа', 'IR': 'Иран', 
        'HU': 'Венгрия', 'SK': 'Словакия', 'CN': 'Китай', 'CZ': 'Чехия', 'CR': 'Коста-Рика', 'TR': 'Турция', 'CL': 'Чили', 'PR': 'Пуэрто-Рико', 
        'DK': 'Дания', 'BO': 'Боливия', 'PH': 'Филиппины', 'DO': 'Доминиканская Республика', 'EG': 'Египет', 'ID': 'Индонезия', 
        'AE': 'Объединенные Арабские Эмираты', 'MY': 'Малайзия', 'JP': 'Япония', 'EE': 'Эстония', 'HN': 'Гондурас', 'TN': 'Тунис', 
        'RU': 'Россия', 'DZ': 'Алжир', 'IQ': 'Ирак', 'BG': 'Болгария', 'JE': 'Джерси', 'RS': 'Сербия', 'NZ': 'Новая Зеландия', 'MD': 'Молдова', 
        'LU': 'Люксембург', 'MT': 'Мальта'
    }
    
    top_country = top_countries.index[0]
    top_country_name = country_codes.get(top_country, top_country)
    top_country_rate = top_countries.iloc[0]['international_rate']
    print(f"2. Больше всего специалистов проживает в {top_country_name}")
    print(f"   Из них {top_country_rate:.1%} работают в другой стране")
    
    # Анализ удаленности для международных работников
    intl_workers = df_enhanced[df_enhanced['works_internationally']]
    fully_remote_intl = (intl_workers['remote_ratio'] == 100).sum()
    fully_remote_pct = (fully_remote_intl / len(intl_workers)) * 100
    
    print(f"3. Среди международных работников {fully_remote_pct:.1f}% работают полностью удаленно")
    
    avg_remote_intl = intl_workers['remote_ratio'].mean()
    avg_remote_domestic = df_enhanced[~df_enhanced['works_internationally']]['remote_ratio'].mean()
    
    return df_enhanced, top_countries

class DataAnalyzerTable:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.column_descriptions = {
            'work_year': 'Год выплаты зарплаты',
            'experience_level': 'Уровень опыта работы',
            'employment_type': 'Тип занятости',
            'job_title': 'Должность сотрудника',
            'salary': 'Сумма зарплаты (GROSS)',
            'salary_currency': 'Валюта зарплаты (ISO 4217)',
            'salary_in_usd': 'Зарплата в USD (целевая)',
            'employee_residence': 'Страна сотрудника (ISO 3166)',
            'remote_ratio': 'Доля удалённой работы',
            'company_location': 'Страна компании',
            'company_size': 'Средний размер компании'
        }
    
    def get_unique_data_types(self, series: pd.Series) -> List[str]:
        """Получить список уникальных типов данных в столбце"""
        unique_types = set(type(x).__name__ for x in series)
        return sorted(list(unique_types))
    def get_unique_values_summary(self, series: pd.Series, max_show: int = 5) -> str:
        """Получить краткое описание уникальных значений"""
        unique_vals = series.dropna().unique()
        total_unique = len(unique_vals)
        
        if total_unique == 0:
            return "Нет данных"
        elif total_unique <= max_show:
            return f"Все ({total_unique}): {list(unique_vals)}"
        else:
            sample = list(unique_vals[:max_show])
            return f"Примеры ({total_unique} всего): {sample}..."
    
    
    def create_analysis_table(self) -> pd.DataFrame:
        """Создать сводную таблицу анализа"""
        analysis_data = []
        
        for column in self.df.columns:
            series = self.df[column]
            
            row = {
                'Столбец': column,
                'Описание': self.column_descriptions.get(column, 'Описание не найдено'),
                'Кол-во значений': len(series),
                'Типы данных': ', '.join(self.get_unique_data_types(series)),
                'NaN (%)': round((series.isnull().sum() / len(series)) * 100, 2),
                'Кол-во уникальных': series.nunique(),
                'Примеры значений': self.get_unique_values_summary(series)
            }
            
            analysis_data.append(row)
        
        return pd.DataFrame(analysis_data)
    
    def display_analysis_table(self):
        """Отобразить таблицу анализа с красивым форматированием"""
        df_analysis = self.create_analysis_table()
        
        print("🔍 СВОДНАЯ ТАБЛИЦА АНАЛИЗА ДАННЫХ")
        print("=" * 120)
        print(f"📊 Датасет: {self.df.shape[0]:,} строк × {self.df.shape[1]} столбцов")
        print(f"💾 Размер в памяти: {self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        print("=" * 120)
        
        # Настраиваем отображение pandas
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', 50)
        pd.set_option('display.width', None)
        
        # Выводим таблицу
        display(df_analysis)
def count_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return ((series < lower) | (series > upper)).sum()
# Словарь кодов стран
country_codes = {
    'ES': 'Испания', 'US': 'Соединенные Штаты Америки', 'CA': 'Канада', 'DE': 'Германия', 'GB': 'Великобритания', 'NG': 'Нигерия', 
    'IN': 'Индия', 'HK': 'Гонконг', 'PT': 'Португалия', 'NL': 'Нидерланды', 'CH': 'Швейцария', 'CF': 'Центральноафриканская Республика', 
    'FR': 'Франция', 'AU': 'Австралия', 'FI': 'Финляндия', 'UA': 'Украина', 'IE': 'Ирландия', 'IL': 'Израиль', 'GH': 'Гана', 'AT': 'Австрия',
    'CO': 'Колумбия', 'SG': 'Сингапур', 'SE': 'Швеция', 'SI': 'Словения', 'MX': 'Мексика', 'UZ': 'Узбекистан', 'BR': 'Бразилия', 
    'TH': 'Таиланд', 'HR': 'Хорватия', 'PL': 'Польша', 'KW': 'Кувейт', 'VN': 'Вьетнам', 'CY': 'Кипр', 'AR': 'Аргентина', 'AM': 'Армения', 
    'BA': 'Босния и Герцеговина', 'KE': 'Кения', 'GR': 'Греция', 'MK': 'Северная Македония', 'LV': 'Латвия', 'RO': 'Румыния', 
    'PK': 'Пакистан', 'IT': 'Италия', 'MA': 'Марокко', 'LT': 'Литва', 'BE': 'Бельгия', 'AS': 'Американское Самоа', 'IR': 'Иран', 
    'HU': 'Венгрия', 'SK': 'Словакия', 'CN': 'Китай', 'CZ': 'Чехия', 'CR': 'Коста-Рика', 'TR': 'Турция', 'CL': 'Чили', 'PR': 'Пуэрто-Рико', 
    'DK': 'Дания', 'BO': 'Боливия', 'PH': 'Филиппины', 'DO': 'Доминиканская Республика', 'EG': 'Египет', 'ID': 'Индонезия', 
    'AE': 'Объединенные Арабские Эмираты', 'MY': 'Малайзия', 'JP': 'Япония', 'EE': 'Эстония', 'HN': 'Гондурас', 'TN': 'Тунис', 
    'RU': 'Россия', 'DZ': 'Алжир', 'IQ': 'Ирак', 'BG': 'Болгария', 'JE': 'Джерси', 'RS': 'Сербия', 'NZ': 'Новая Зеландия', 'MD': 'Молдова', 
    'LU': 'Люксембург', 'MT': 'Мальта'}
remote_ratio_dict = {0: 'Офис', 50: 'Гибрид', 100: 'Удалённый'}

# Функция для создания прокручивающейся таблицы
def make_scrollable_table(df, height="235px"):
    return HTML(f"""
    <div style="height: {height}; overflow: auto; border: 1px solid #ccc;">
        {df.to_html(classes='table table-striped', table_id='scrollable-table')}
    </div>
    <style>
        #scrollable-table {{
            margin: 0;
            font-family: Arial, sans-serif;
            width: auto;
            table-layout: fixed;
        }}
        #scrollable-table th {{
            position: sticky;
            top: 0;
            background-color: #f8f9fa;
            z-index: 10;
            font-weight: bold;
            text-align: center;
            padding: 12px 8px;
        }}
        #scrollable-table td {{
            padding: 8px 12px;
            text-align: left;
        }}
        #scrollable-table td:last-child {{
            text-align: right;
        }}
        #scrollable-table tbody tr:hover {{
            background-color: #e8f4fd;
        }}
        .table-striped tbody tr:nth-of-type(odd) {{
            background-color: rgba(0,0,0,.05);
        }}
        #scrollable-table th:first-child,
        #scrollable-table td:first-child {{
            width: 10px;
            max-width: 50px;
            text-align: center;
            font-size: 12px;
            color: #6c757d;
        }}
        #scrollable-table th:nth-child(2),
        #scrollable-table td:nth-child(2) {{
            width: 230px;
            max-width: 300px;
            text-align: left;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        #scrollable-table th:nth-child(3),
        #scrollable-table td:nth-child(3) {{
            width: 140px;
            max-width: 170px;
            text-align: right;
        }}
    </style>
    """)

