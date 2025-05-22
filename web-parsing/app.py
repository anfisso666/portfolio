import dash
from dash import dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import numpy as np
import os
from dash import dcc, html, Input, Output, State, callback, dash_table
import numpy as np
import os
from dash import dcc, html, Input, Output, State, callback, dash_table
from sklearn.linear_model import LinearRegression

# Initialize the Dash app with Bootstrap for responsive layout
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True
)
# Load the data with error handling
try:
    data_file = 'data_f.csv'
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
        print(f"Данные загружены успешно. {len(df)} строк.")
        # Проверка наличия всех необходимых столбцов
        required_columns = ["Город", "Тип жилья", "Площадь", "Стоимость. ₽/мес.", "Стоимость 1 кв.м. (покупка)", "ROI", "Срок окупаемости"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"ВНИМАНИЕ: Отсутствуют столбцы: {missing_columns}")
            # Создаем заглушку для отсутствующих столбцов
            for col in missing_columns:
                df[col] = 0 if col in ["Площадь", "Стоимость. ₽/мес.", "Стоимость 1 кв.м. (покупка)", "ROI", "Срок окупаемости"] else "Неизвестно"
    else:
        print(f"ОШИБКА: Файл {data_file} не найден. Создаем тестовые данные.")

        
except Exception as e:
    print(f"Произошла ошибка при загрузке данных: {e}")

# Color palette
colors = [ "#0969da", "#1f883d", "#cf222e", "#fb8500", "#8250df", "#0550ae", "#656d76", "#24292f", "#54aeff","#2da44e"]



# Define the app layout
app.layout = html.Div(
    className="main-container",  # Добавлен класс для основного контейнера
    children=[
        # Header Section
        html.Div(
            className="header",
            children=[
                # Title moved to header
                html.H2("Анализ рентабельности аренды недвижимости"),
                # Filter Section
                html.Div(
                    className="filter",
                    children=[
                        html.Div(
                            children=[
                                html.Label("   "),
                                dcc.Dropdown(
                                    id="city-filter",
                                    options=[{"label": city, "value": city} for city in sorted(df["Город"].unique())],
                                    value=[],
                                    placeholder="Выберите город(а)",
                                    multi=True
                                )]),
                                html.Div(
                            children=[
                                html.Label("   "),
                                dcc.Dropdown(
                                    id="property-type-filter",
                                    options=[{"label": prop_type, "value": prop_type} for prop_type in sorted(df["Тип жилья"].unique())],
                                    value=[],
                                    placeholder="Выберите тип жилья",
                                    multi=True
                                )]),
                                    html.Div(
                                    children=[
                                        html.Label("Площадь (кв.м.):"),
                                        dcc.RangeSlider(
                                            id="area-range-filter",
                                            min=int(df["Площадь"].min()),
                                            max=int(df["Площадь"].max()),
                                            step=1,
                                            marks={
                                                int(df["Площадь"].min()): {'label': str(int(df["Площадь"].min())),
                                                                        'style': {'color': '#ecf0f1', 'font-weight': 'bold'}},
                                                int(df["Площадь"].max()): {'label': str(int(df["Площадь"].max())),
                                                                        'style': {'color': '#ecf0f1', 'font-weight': 'bold'}}
                                            },
                                            value=[int(df["Площадь"].min()), int(df["Площадь"].max())]
                                        ),
                                    ]
                                ),
                                # ROI Range Filter
                                html.Div(
                                    children=[
                                        html.Label("ROI:"),
                                        dcc.RangeSlider(
                                            id="roi-range-filter",
                                            min=int(df["ROI"].min()),
                                            max=int(df["ROI"].max()),
                                            step=1,
                                            marks={
                                                int(df["ROI"].min()): {'label': str(int(df["ROI"].min())),
                                                                        'style': {'color': '#ecf0f1', 'font-weight': 'bold'}},
                                                int(df["ROI"].max()): {'label': str(int(df["ROI"].max())),
                                                                        'style': {'color': '#ecf0f1', 'font-weight': 'bold'}}
                                            },
                                            value=[int(df["ROI"].min()), int(df["ROI"].max())]
                                        ),
                                    ]
                                ),
                        #     ]
                        # ),
                    ]
                ),
                
                
                
            ]
        ),
           html.Div(id="kpi-line"),
        # KPI Section
        html.Div(
            className="kpi",
            children=[
                html.Div(id="kpi-section"),
            ]
        ),
        
        # Main Content Section
        html.Div(
            className="main",
            children=[
                # ROI Factors Analysis Section
                html.Div(
                    children=[
                        html.H3("Анализ факторов, влияющих на ROI"),
                        html.Div(
                            id="roi-factors-analysis-container"
                        )
                    ]
                ),
                
                # Overview Section
                html.Div(
                    children=[
                        html.Div(
                            id="overview-content"
                        )
                    ]
                ),
                
                # Top Objects Section
                html.Div(
                    children=[
                        html.H3("ТОП-10 объектов по ROI"),
                        html.Div(
                            id="top-objects-table-container"
                        )
                    ]
                ),
                
                # Comparative Analysis Section
                html.Div(
                    children=[
                        html.H3("Сравнительный анализ по типам жилья и городам"),
                        html.Div(
                            id="comparative-analysis-container"
                        )
                    ]
                ),
                
                # ROI Range Chart Section
                html.Div(
                    children=[
                        html.H3("Диапазон значений ROI по городам"),
                        html.Div(
                            id="roi-range-chart-container"
                        )
                    ]
                ),
            ]
        )
    ]
)


# :first-child 
# :last-child -
# :nth-child(n)





@app.callback(
    Output("area-range-filter", "marks"),
    Input("area-range-filter", "value")
)
def update_area_marks(value):
    return {
        value[0]: {'label': str(value[0]), 'style': {'color': '#b2b2b2', 'font-weight': 'bold'}},
        value[1]: {'label': str(value[1]), 'style': {'color': '#b2b2b2', 'font-weight': 'bold'}}
    }

# Callback for updating ROI range slider marks
@app.callback(
    Output("roi-range-filter", "marks"),
    Input("roi-range-filter", "value")
)
def update_roi_marks(value):
    return {
        value[0]: {'label': str(value[0]), 'style': {'color': '#b2b2b2', 'font-weight': 'bold'}},
        value[1]: {'label': str(value[1]), 'style': {'color': '#b2b2b2', 'font-weight': 'bold'}}
    }


# Функция для создания KPI-карточек с округлением и форматированием
def create_kpi_card(title, value, unit):
    # Округляем до целого числа
    value_rounded = int(round(value))
    
    # Форматируем число с пробелами между тысячами
    formatted_value = f"{value_rounded:,}".replace(",", " ")
    
    return html.Div(
        children=[
            html.H5(title, style={"margin-bottom": "10px", "font-size": "1vw"}),
            html.Div([
                html.Span(
                    f"{formatted_value} {unit}",
                    style={"font-size": "1.2vw", "font-weight": "bold", "color": "#163E60"}
                )
            ])
        ]
    )

# Callback to update KPI section
@app.callback(
    Output("kpi-section", "children"),
    [
        Input("city-filter", "value"),
        Input("property-type-filter", "value"),
        Input("area-range-filter", "value"),
        Input("roi-range-filter", "value")
    ]
)
def update_kpi_section(selected_cities, selected_property_types, area_range, roi_range): #, rent_range): #
    try:
        filtered_df = df.copy()
        
        if selected_cities and len(selected_cities) > 0:
            filtered_df = filtered_df[filtered_df["Город"].isin(selected_cities)]
        
        if selected_property_types and len(selected_property_types) > 0:
            filtered_df = filtered_df[filtered_df["Тип жилья"].isin(selected_property_types)]
        
        filtered_df = filtered_df[(filtered_df["Площадь"] >= area_range[0]) & (filtered_df["Площадь"] <= area_range[1])]
        filtered_df = filtered_df[(filtered_df["ROI"] >= roi_range[0]) & (filtered_df["ROI"] <= roi_range[1])]
        # filtered_df = filtered_df[(filtered_df["Стоимость. ₽/мес."] >= rent_range[0]) & (filtered_df["Стоимость. ₽/мес."] <= rent_range[1])]
        
        avg_rent = filtered_df["Стоимость. ₽/мес."].mean() if not filtered_df.empty else 0
        avg_price_per_sqm = filtered_df["Стоимость 1 кв.м. (покупка)"].mean() if not filtered_df.empty else 0
        avg_area = filtered_df["Площадь"].mean() if not filtered_df.empty else 0
        
        return html.Div([
            create_kpi_card("Средняя стоимость аренды", avg_rent, "₽/мес."),
            create_kpi_card("Средняя стоимость 1 кв.м.", avg_price_per_sqm, "₽"),
            create_kpi_card("Средняя площадь", avg_area, "кв.м.")
        ])
    except Exception as e:
        return html.Div(f"Ошибка при расчете KPI: {str(e)}")

# Callback to update overview section
@app.callback(
    Output("overview-content", "children"),
    [
        Input("city-filter", "value"),
        Input("property-type-filter", "value"),
        Input("area-range-filter", "value"),
        Input("roi-range-filter", "value")
    ]
)
def update_overview_content(selected_cities, selected_property_types, area_range, roi_range): #, rent_range):
    try:
        filtered_df = df.copy()
        
        if selected_cities and len(selected_cities) > 0:
            filtered_df = filtered_df[filtered_df["Город"].isin(selected_cities)]
        
        if selected_property_types and len(selected_property_types) > 0:
            filtered_df = filtered_df[filtered_df["Тип жилья"].isin(selected_property_types)]
        
        filtered_df = filtered_df[(filtered_df["Площадь"] >= area_range[0]) & (filtered_df["Площадь"] <= area_range[1])]
        filtered_df = filtered_df[(filtered_df["ROI"] >= roi_range[0]) & (filtered_df["ROI"] <= roi_range[1])]
        # filtered_df = filtered_df[(filtered_df["Стоимость. ₽/мес."] >= rent_range[0]) & (filtered_df["Стоимость. ₽/мес."] <= rent_range[1])]
        
        boxplot_fig = go.Figure()
        
        cities_in_data = filtered_df["Город"].unique()
        
        if cities_in_data.size > 0:
            boxplot_data = []
            
            for i, city in enumerate(cities_in_data):
                city_data = filtered_df[filtered_df["Город"] == city]["Стоимость. ₽/мес."]
                
                if not city_data.empty:
                    boxplot_data.append(go.Box(
                        y=city_data,
                        name=city,
                        marker=dict(color=colors[i % len(colors)]),
                        boxmean=True
                    ))
            
            if boxplot_data:
                boxplot_fig = go.Figure(data=boxplot_data)
                boxplot_fig.update_layout(
                    title="Распределение стоимости аренды по городам",
                    yaxis_title="Стоимость. ₽/мес.",
                    showlegend=False,
                    height=500,
                    plot_bgcolor="white",
                    paper_bgcolor="white"
                )
            else:
                boxplot_fig.update_layout(
                    title="Нет данных для отображения",
                    height=500,
                    plot_bgcolor="white",
                    paper_bgcolor="white"
                )
        else:
            boxplot_fig.update_layout(
                title="Нет данных для отображения",
                height=500,
                plot_bgcolor="white",
                paper_bgcolor="white"
            )
        
        return dcc.Graph(
            figure=boxplot_fig,
            config={'displayModeBar': False}
        )
    except Exception as e:
        return html.Div(f"Ошибка при создании обзорного графика: {str(e)}")



# Callback to update comparative analysis
@app.callback(
    Output("comparative-analysis-container", "children"),
    [
        Input("city-filter", "value"),
        Input("property-type-filter", "value"),
        Input("area-range-filter", "value"),
        Input("roi-range-filter", "value")
    ]
)
def update_comparative_analysis(selected_cities, selected_property_types, area_range, roi_range): #, rent_range):
    try:
        filtered_df = df.copy()
        
        # Проверяем наличие столбца "Стоимость 1 кв.м. (аренда)"
        if "Стоимость 1 кв.м. (аренда)" not in filtered_df.columns:
            # Если столбца нет, создаем его из имеющихся данных
            filtered_df["Стоимость 1 кв.м. (аренда)"] = filtered_df["Стоимость. ₽/мес."] / filtered_df["Площадь"]
            print("Создан столбец 'Стоимость 1 кв.м. (аренда)' из доступных данных")
        
        if selected_cities and len(selected_cities) > 0:
            filtered_df = filtered_df[filtered_df["Город"].isin(selected_cities)]
        else:
            # Если города не выбраны, берем 4 наиболее представленных города
            top_cities = filtered_df["Город"].value_counts().nlargest(10).index.tolist()
            filtered_df = filtered_df[filtered_df["Город"].isin(top_cities)]
        
        if selected_property_types and len(selected_property_types) > 0:
            filtered_df = filtered_df[filtered_df["Тип жилья"].isin(selected_property_types)]
        
        filtered_df = filtered_df[(filtered_df["Площадь"] >= area_range[0]) & (filtered_df["Площадь"] <= area_range[1])]
        filtered_df = filtered_df[(filtered_df["ROI"] >= roi_range[0]) & (filtered_df["ROI"] <= roi_range[1])]
        # filtered_df = filtered_df[(filtered_df["Стоимость. ₽/мес."] >= rent_range[0]) & (filtered_df["Стоимость. ₽/мес."] <= rent_range[1])]
        
        if filtered_df.empty:
            return html.Div("Нет данных для отображения после применения фильтров")
        
        # Создаем комбинированный box plot
        fig = go.Figure()
        
        # Получаем уникальные города и типы жилья
        cities = filtered_df["Город"].unique()
        property_types = filtered_df["Тип жилья"].unique()
       
        # Расчет позиций для групп по городам и боксплотов внутри групп
        city_gap = 0.5  # Уменьшено расстояние между группами городов
        box_gap = 0.32  # Увеличено расстояние между боксплотами внутри группы
        total_width = box_gap * (len(property_types) - 1)  # Общая ширина группы боксплотов
        
        # Создание словаря цветов для типов жилья
        prop_type_colors = {prop_type: colors[i % len(colors)] for i, prop_type in enumerate(property_types)}
        
        # Создаем x-координаты для боксплотов каждого города
        city_positions = [i * (1 + city_gap) for i in range(len(cities))]
        
        for city_idx, city in enumerate(cities):
            city_data = filtered_df[filtered_df["Город"] == city]
            city_pos = city_positions[city_idx]
            
            # Рассчитываем позиции для боксплотов этого города
            start_pos = city_pos - total_width/2
            
            for prop_idx, prop_type in enumerate(property_types):
                prop_data = city_data[city_data["Тип жилья"] == prop_type]["Стоимость 1 кв.м. (аренда)"]
                
                if not prop_data.empty:
                    box_pos = start_pos + prop_idx * box_gap
                    
                    fig.add_trace(go.Box(
                        y=prop_data,
                        x0=box_pos,
                        name=prop_type,  # Устанавливаем имя только как тип жилья для легенды
                        marker=dict(color=prop_type_colors[prop_type]),
                        boxmean=True,
                        legendgroup=prop_type,
                        showlegend=city_idx == 0,  # Показываем в легенде только один раз для каждого типа жилья
                        offsetgroup=prop_type,
                        width=box_gap * 0.8  # Ширина боксплота
                    ))
        
        # Настраиваем оси и легенду
        fig.update_layout(
            title="Распределение стоимости 1 кв.м. аренды по типам жилья и городам",
            yaxis_title="Стоимость 1 кв.м. (₽/мес)",
            xaxis=dict(
                tickmode='array',
                tickvals=city_positions,
                ticktext=cities,
                tickangle=-45
            ),
            height=600,
            plot_bgcolor="white",
            paper_bgcolor="white",
            boxmode='group',
            boxgap=0,  # Убираем стандартный промежуток между группами
            boxgroupgap=0,  # Убираем стандартный промежуток внутри групп
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Добавляем вертикальные линии для разделения групп городов
        for i in range(1, len(cities)):
            pos = (city_positions[i-1] + city_positions[i]) / 2
            fig.add_shape(
                type="line",
                x0=pos,
                y0=filtered_df["Стоимость 1 кв.м. (аренда)"].min() * 0.9,
                x1=pos,
                y1=filtered_df["Стоимость 1 кв.м. (аренда)"].max() * 1.1,
                line=dict(color="lightgray", width=1, dash="dash")
            )
        
        return dcc.Graph(
            figure=fig,
            config={'displayModeBar': False}
        )
    except Exception as e:
        return html.Div(f"Ошибка при создании сравнительного анализа: {str(e)}")

# Callback to update top objects table
@app.callback(
    Output("top-objects-table-container", "children"),
    [
        Input("city-filter", "value"),
        Input("property-type-filter", "value"),
        Input("area-range-filter", "value"),
        Input("roi-range-filter", "value")
    ]
)     
def update_top_objects_table(selected_cities, selected_property_types, area_range, roi_range): #, rent_range):
    try:
        filtered_df = df.copy()
        
        if selected_cities and len(selected_cities) > 0:
            filtered_df = filtered_df[filtered_df["Город"].isin(selected_cities)]
        
        if selected_property_types and len(selected_property_types) > 0:
            filtered_df = filtered_df[filtered_df["Тип жилья"].isin(selected_property_types)]
        
        filtered_df = filtered_df[(filtered_df["Площадь"] >= area_range[0]) & (filtered_df["Площадь"] <= area_range[1])]
        filtered_df = filtered_df[(filtered_df["ROI"] >= roi_range[0]) & (filtered_df["ROI"] <= roi_range[1])]
        # filtered_df = filtered_df[(filtered_df["Стоимость. ₽/мес."] >= rent_range[0]) & (filtered_df["Стоимость. ₽/мес."] <= rent_range[1])]
        
        if filtered_df.empty:
            return html.Div("Нет данных для отображения после применения фильтров")
        
        # Проверяем наличие необходимых столбцов
        required_columns = ["Город", "Адрес", "Площадь", "Стоимость. ₽/мес.",  "ROI", "Срок окупаемости", "Ссылка"]
        missing_columns = [col for col in required_columns if col not in filtered_df.columns]
        
        # Если отсутствуют столбцы, добавляем их с заглушками
        for col in missing_columns:
            if col == "Адрес":
                filtered_df[col] = "Адрес недоступен"
            elif col == "Ссылка":
                filtered_df[col] = "#"
        
        # Сортируем по ROI и берем ТОП-10
        top_objects = filtered_df.sort_values(by="ROI", ascending=False).head(10)
        
        # Форматируем данные для отображения
        display_df = top_objects[required_columns].copy()
        
        # Форматируем числовые столбцы
        if "Площадь" in display_df.columns:
            display_df["Площадь"] = display_df["Площадь"].round(1).astype(str) + " кв.м."
            
        if "Стоимость. ₽/мес." in display_df.columns:
            display_df["Стоимость. ₽/мес."] = display_df["Стоимость. ₽/мес."].round(0).astype(int).apply(lambda x: f"{x:,} ₽".replace(",", " "))
            # -
        # if "Стоимость покупки" in display_df.columns:
        #     display_df["Стоимость покупки"] = display_df["Стоимость покупки"].round(0).astype(int).apply(lambda x: f"{x:,} ₽".replace(",", " "))
            
        if "ROI" in display_df.columns:
            display_df["ROI"] = display_df["ROI"].round(1).astype(str) + "%"
            
        if "Срок окупаемости" in display_df.columns:
            display_df["Срок окупаемости"] = display_df["Срок окупаемости"].round(1).astype(str) + " лет"
        
        # Подготовка данных для таблицы с правильными ссылками
        table_data = []
        
        # Создаем форматированные ссылки в формате markdown для столбца "Ссылка"
        for i, row in display_df.iterrows():
            # Копируем все данные строки
            row_data = row.to_dict()
            
            # Обрабатываем ссылку для правильного отображения
            link = row_data["Ссылка"]
            if isinstance(link, str) and link != "#":
                try:
                    from urllib.parse import urlparse
                    parsed_url = urlparse(link)
                    domain = parsed_url.netloc
                    if domain.startswith('www.'):
                        domain = domain[4:]  # Убираем www. если есть
                    
                    # Форматируем ссылку в формате markdown - это будет правильно обработано с target="_blank"
                    row_data["Ссылка"] = f"[{domain}]({link})"
                except:
                    row_data["Ссылка"] = f"[ciar.ru]({link})"
            else:
                row_data["Ссылка"] = "Н/Д"
            
            # Добавляем номер строки
            row_data["index"] = i + 1
            
            # Добавляем строку в данные таблицы
            table_data.append(row_data)
        
        # Создаем колонки таблицы, включая специальную колонку для ссылок
        columns = [
            {"name": "№", "id": "index"},
        ]
        
        # Добавляем остальные колонки данных
        for col in display_df.columns:
            if col == "Ссылка":
                # Для колонки Ссылка указываем специальный тип представления и target="_blank"
                columns.append({
                    "name": col, 
                    "id": col, 
                    "presentation": "markdown",
                    "type": "text"
                })
            else:
                columns.append({"name": col, "id": col})
        






        # Создаем таблицу с настроенными колонками и данными

        table = dash_table.DataTable(
        id='data-table',
        columns=columns,
        data=table_data,
        markdown_options={"link_target": "_blank"},
        
        # Основные стили таблицы
        style_table={
            'overflowX': 'auto',
            'width': '100%',
            'border': '1px solid #e5e5e5',
            'borderRadius': '4px',
            'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.1)',
            'backgroundColor': '#ffffff'
        },
        
        # Стили ячеек
        style_cell={
            'textAlign': 'left',
            'padding': '12px 16px',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            'fontSize': '14px',
            'lineHeight': '1.4',
            'color': '#212529',
            'border': '1px solid #f1f3f4',
            'backgroundColor': '#ffffff'
        },
        
        # Стили заголовков
        style_header={
            'backgroundColor': '#f8f9fa',
            'color': '#E8E8E8',
            'fontWeight': '600',
            'textAlign': 'left',
            'textTransform': 'uppercase',
            'fontSize': '12px',
            'letterSpacing': '0.5px',
            'padding': '12px 16px',
            'border': '1px solid #e5e5e5',
            'borderBottom': '2px solid #e5e5e5'
        },
        
        # Условная стилизация данных
        style_data_conditional=[
            # Зебра-раскраска строк
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#fafbfc'
            },
            # Hover эффект (работает ограниченно в Dash)
            {
                'if': {'state': 'selected'},
                'backgroundColor': '#e3f2fd',
                'border': '1px solid #2196f3'
            }
        ],
        
        
        # Настройки функциональности
        page_size=10,
        sort_action='native',
        filter_action='native',
        style_as_list_view=True,
        
        # Стили для пагинации и фильтров
        css=[
            {
                'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner input',
                'rule': '''
                    border: 1px solid #e5e5e5;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                '''
            },
            {           
                'selector': '.dash-table-container .previous-next-container .previous-page, .dash-table-container .previous-next-container .next-page',
                'rule': '''
                    background-color: #f8f9fa;
                    border: 1px solid #e5e5e5;
                    color: #E8E8E8; 
                    border-radius: 4px;
                    padding: 4px 8px;
                    margin: 0 2px;
                '''
            }
        ]
    )
        # table = dash_table.DataTable(
        #     id='data-table',
        #     columns=columns,
        #     data=table_data,
        #     markdown_options={"link_target": "_blank"},  # Важно! Это заставляет все ссылки открываться в новой вкладке
        #     style_table={
        #         'overflowX': 'auto',
        #         'width': '100%'
        #     },
        #     style_cell={
        #         'textAlign': 'left',
        #         'padding': '8px',
        #         'fontFamily': 'Arial, sans-serif'
        #     },
        #     style_header={
        #         'backgroundColor': '#163E60',
        #         'color': 'white',
        #         'fontWeight': 'bold',
        #         'textAlign': 'center'
        #     },
        #     style_data_conditional=[
        #         {
        #             'if': {'row_index': 'odd'},
        #             'backgroundColor': '#f2f2f2'
        #         }
        #     ],
        #     style_cell_conditional=[
        #         {
        #             'if': {'column_id': 'Ссылка'},
        #             'color': '#0066cc',
        #             'textDecoration': 'underline',
        #             'cursor': 'pointer'
        #         }
        #     ],
        #     page_size=10,
        #     sort_action='native',
        #     filter_action='native',
        #     style_as_list_view=True
        # )
        
        return table
        
    except Exception as e:
        return html.Div(f"Ошибка при создании таблицы: {str(e)}")


# Callback для анализа факторов, влияющих на ROI
@app.callback(
    Output("roi-factors-analysis-container", "children"),
    [
        Input("city-filter", "value"),
        Input("property-type-filter", "value"),
        Input("area-range-filter", "value"),
        Input("roi-range-filter", "value")
    ]
)
def update_roi_factors_analysis(selected_cities, selected_property_types, area_range, roi_range): #, rent_range):
    try:
        filtered_df = df.copy()
        
        if selected_cities and len(selected_cities) > 0:
            filtered_df = filtered_df[filtered_df["Город"].isin(selected_cities)]
        
        if selected_property_types and len(selected_property_types) > 0:
            filtered_df = filtered_df[filtered_df["Тип жилья"].isin(selected_property_types)]
        
        filtered_df = filtered_df[(filtered_df["Площадь"] >= area_range[0]) & (filtered_df["Площадь"] <= area_range[1])]
        filtered_df = filtered_df[(filtered_df["ROI"] >= roi_range[0]) & (filtered_df["ROI"] <= roi_range[1])]
        # filtered_df = filtered_df[(filtered_df["Стоимость. ₽/мес."] >= rent_range[0]) & (filtered_df["Стоимость. ₽/мес."] <= rent_range[1])]
        
        if filtered_df.empty:
            return html.Div("Нет данных для анализа после применения фильтров")
        
        # Проверка наличия всех необходимых столбцов
        required_columns = ["Площадь", "Тип жилья", "Этаж", "Этажность дома", "Срок аренды", "Коммунальные включены", "ROI"]
        missing_columns = []
        
        for column in required_columns:
            if column not in filtered_df.columns:
                missing_columns.append(column)
                
        if missing_columns:
            return html.Div(f"Для анализа факторов не хватает следующих столбцов: {', '.join(missing_columns)}")
        
        # Подготовка данных для анализа
        analysis_df = filtered_df.copy()
        
        # Определение категориальных переменных 
        categorical_features = ["Тип жилья", "Срок аренды", "Город"]
        numerical_features = ["Площадь", "Этаж", "Этажность дома"]
        boolean_features = ["Коммунальные включены"]
        
        # Проверка наличия столбцов в данных
        categorical_features = [col for col in categorical_features if col in analysis_df.columns]
        numerical_features = [col for col in numerical_features if col in analysis_df.columns]
        boolean_features = [col for col in boolean_features if col in analysis_df.columns]
        
        # Создаем словарь для отслеживания, какие столбцы относятся к каким категориальным признакам
        categorical_columns_map = {}
        
        # Обработка категориальных признаков
        for feature in categorical_features:
            # Заполнение пропущенных значений
            analysis_df[feature] = analysis_df[feature].fillna(analysis_df[feature].mode()[0])
            
            # Стандартизация значений для более корректного сравнения
            analysis_df[feature] = analysis_df[feature].astype(str).str.lower().str.strip()
            
            # Специальная обработка для срока аренды
            if feature == "Срок аренды":
                def categorize_rental_term(value):
                    value = str(value).lower().strip()
                    if 'кратк' in value or 'корот' in value or 'посут' in value or 'сутк' in value:
                        return 'краткосрочные'
                    else:
                        return 'долгосрочные'
                
                analysis_df[feature] = analysis_df[feature].apply(categorize_rental_term)
        
        # Обработка булевых признаков
        for feature in boolean_features:
            if analysis_df[feature].dtype == 'object':
                # Преобразуем текстовые значения в числовые (0/1)
                analysis_df[feature] = analysis_df[feature].apply(
                    lambda x: 1 if str(x).lower() in ['да', 'true', '1', 'yes'] else 0
                )
            analysis_df[feature] = analysis_df[feature].fillna(0)
        
        # Обработка числовых признаков
        for feature in numerical_features:
            # Заполнение пропущенных значений средними
            analysis_df[feature] = analysis_df[feature].fillna(analysis_df[feature].mean())
        
        # Создание дамми-переменных для категориальных признаков и отслеживание их
        X_encoded = analysis_df.copy()
        
        # Словарь для хранения информации о том, какие дамми-переменные соответствуют каким категориальным признакам
        dummies_map = {}
        
        for feature in categorical_features:
            # Получаем уникальные значения категории для описания в итоговом графике
            unique_values = analysis_df[feature].unique()
            
            # Создаем дамми-переменные
            dummies = pd.get_dummies(analysis_df[feature], prefix=feature, drop_first=False)
            
            # Запоминаем, какие столбцы соответствуют текущей категории
            dummies_map[feature] = list(dummies.columns)
            
            # Добавляем дамми-переменные в набор данных
            X_encoded = pd.concat([X_encoded, dummies], axis=1)
        
        # Формирование массива признаков
        # Добавляем числовые и булевы признаки
        feature_columns = numerical_features + boolean_features
        
        # Добавляем дамми-переменные для категориальных признаков
        for feature_dummies in dummies_map.values():
            feature_columns.extend(feature_dummies)
        
        # Проверяем, что все колонки есть в наборе данных
        feature_columns = [col for col in feature_columns if col in X_encoded.columns]
        
        # Подготовка данных для моделирования
        X = X_encoded[feature_columns]
        y = analysis_df["ROI"]
        
        # Проверка наличия данных
        if X.empty or len(feature_columns) < 1:
            return html.Div("Недостаточно данных для построения модели регрессии")
        
        # Обучение линейной регрессии
        model = LinearRegression()
        model.fit(X, y)
        
        # Получение коэффициентов
        coefs = model.coef_
        
        # Создаем словарь для хранения важности категориальных признаков в целом
        feature_importance = {}
        
        # Добавляем числовые и булевы признаки
        for i, feature in enumerate(numerical_features + boolean_features):
            if feature in X.columns:
                idx = list(X.columns).index(feature)
                feature_importance[feature] = abs(coefs[idx])
        
        # Теперь рассчитываем суммарную важность для каждого категориального признака
        for feature, feature_dummies in dummies_map.items():
            # Отфильтровываем дамми-переменные, которые есть в X
            valid_dummies = [col for col in feature_dummies if col in X.columns]
            
            if valid_dummies:
                # Получаем индексы дамми-переменных в X
                dummy_indices = [list(X.columns).index(col) for col in valid_dummies]
                
                # Суммируем абсолютные значения коэффициентов
                importance_sum = sum(abs(coefs[idx]) for idx in dummy_indices)
                
                # Сохраняем суммарную важность
                feature_importance[feature] = importance_sum
        
        # Создаем DataFrame для визуализации
        importance_df = pd.DataFrame({
            'Фактор': list(feature_importance.keys()),
            'Важность': list(feature_importance.values())
        })
        
        # Переименовываем факторы для более понятного отображения на русском
        factor_rename_map = {
            "Площадь": "Площадь",
            "Тип жилья": "Тип жилья",
            "Этаж": "Этаж",
            "Этажность дома": "Этажность дома",
            "Срок аренды": "Срок аренды",
            "Коммунальные включены": "Коммунальные включены",
            "Город": "Город"
        }
        
        importance_df['Фактор'] = importance_df['Фактор'].map(
            lambda x: factor_rename_map.get(x, x)
        )
        
        # Нормализуем важность (0-100%)
        if importance_df['Важность'].sum() > 0:
            importance_df['Важность'] = (importance_df['Важность'] / importance_df['Важность'].sum()) * 100
        
        # Сортируем по важности
        importance_df = importance_df.sort_values('Важность', ascending=True)
        
        # Создаем горизонтальную столбчатую диаграмму
        fig = go.Figure()
        
        # Добавляем полосы для каждого фактора
        fig.add_trace(go.Bar(
            y=importance_df['Фактор'],
            x=importance_df['Важность'],
            orientation='h',
            marker=dict(
                color=colors[:len(importance_df)],
                line=dict(color='rgba(0,0,0,0)', width=2)
            )
        ))
        
        # Настраиваем макет диаграммы
        fig.update_layout(
            title="Важность факторов, влияющих на ROI",
            xaxis_title="Важность (%)",
            yaxis_title="Фактор",
            height=500,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=200, r=20, t=50, b=50),
            xaxis=dict(
                tickformat=".1f",
                ticksuffix="%"
            )
        )
        
        # Добавляем аннотации с процентами
        for i, row in importance_df.iterrows():
            fig.add_annotation(
                x=row['Важность'] + max(importance_df['Важность']) * 0.02,  # Небольшой отступ
                y=row['Фактор'],
                text=f"{row['Важность']:.1f}%",
                showarrow=False,
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                ),
                align="left"
            )
        
        # Добавляем пояснение о методологии
        methodology_text = html.Div([
            html.P("Методология: Каждый фактор (независимо от типа) оценивается по его совокупному влиянию на ROI на основе линейной регрессии. Для категориальных переменных (тип жилья, город и т.д.) рассчитывается суммарное влияние всех значений данной категории.", 
                   style={"font-style": "italic", "color": "#555", "margin-top": "15px"}),
            html.P("Чем выше процент, тем значительнее фактор влияет на доходность объекта.", 
                   style={"font-style": "italic", "color": "#555"})
        ])
        
        return html.Div([
            dcc.Graph(
                figure=fig,
                config={'displayModeBar': False}
            ),
            methodology_text
        ])
        
    except Exception as e:
        return html.Div(f"Ошибка при анализе факторов: {str(e)}")

# Callback to update ROI range chart
@app.callback(
    Output("roi-range-chart-container", "children"),
    [
        Input("city-filter", "value"),
        Input("property-type-filter", "value"),
        Input("area-range-filter", "value"),
        Input("roi-range-filter", "value")
    ]
)
def update_roi_range_chart(selected_cities, selected_property_types, area_range, roi_range): #, rent_range):
    try:
        filtered_df = df.copy()
        
        if selected_cities and len(selected_cities) > 0:
            filtered_df = filtered_df[filtered_df["Город"].isin(selected_cities)]
        
        if selected_property_types and len(selected_property_types) > 0:
            filtered_df = filtered_df[filtered_df["Тип жилья"].isin(selected_property_types)]
        
        filtered_df = filtered_df[(filtered_df["Площадь"] >= area_range[0]) & (filtered_df["Площадь"] <= area_range[1])]
        filtered_df = filtered_df[(filtered_df["ROI"] >= roi_range[0]) & (filtered_df["ROI"] <= roi_range[1])]
        # filtered_df = filtered_df[(filtered_df["Стоимость. ₽/мес."] >= rent_range[0]) & (filtered_df["Стоимость. ₽/мес."] <= rent_range[1])]
        
        if filtered_df.empty:
            return html.Div("Нет данных для отображения после применения фильтров")
        
        # Создаем сводную таблицу с мин, макс и средним значением ROI по городам
        roi_summary = filtered_df.groupby('Город')['ROI'].agg(['min', 'max', 'mean']).reset_index()
        roi_summary.columns = ['Город', 'Минимальный ROI (%)', 'Максимальный ROI (%)', 'Средний ROI (%)']
        
        # Сортируем по среднему ROI по убыванию
        roi_summary = roi_summary.sort_values('Средний ROI (%)', ascending=False)
        
        # Создаем визуализацию диапазонов ROI
        fig_roi_range = go.Figure()
        
        # Добавляем линии диапазона
        for i, row in roi_summary.iterrows():
            fig_roi_range.add_trace(go.Scatter(
                x=[row['Минимальный ROI (%)'], row['Максимальный ROI (%)']],
                y=[row['Город'], row['Город']],
                mode='lines+markers',
                name=row['Город'],
                line=dict(color='gray', width=2),
                marker=dict(size=8)
            ))
        
            # Добавляем средние значения
            fig_roi_range.add_trace(go.Scatter(
                x=[row['Средний ROI (%)']],
                y=[row['Город']],
                mode='markers',
                name=f"{row['Город']} (среднее)",
                marker=dict(color='#0969da', size=10, symbol='diamond'),
                showlegend=False
            ))
        
        # Настраиваем макет диаграммы
        fig_roi_range.update_layout(
            # title='Диапазон значений ROI по городам',
            xaxis_title='ROI (%)',
            yaxis_title='Город',
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            margin=dict(l=100, r=20, t=50, b=50)
        )
        
        # Добавляем сетку
        fig_roi_range.update_xaxes(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#e0e0e0'
        )
        
        fig_roi_range.update_yaxes(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#e0e0e0'
        )
        
        return dcc.Graph(
            figure=fig_roi_range,
            config={'displayModeBar': False}
        )
        
    except Exception as e:
        return html.Div(f"Ошибка при создании графика диапазонов ROI: {str(e)}")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)