from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import seaborn as sns
from urllib.request import urlretrieve
import folium
from folium import Choropleth, Circle, Marker
from functions.data_processing import *
from functions.filters import *
from functions.graphics import *
from functions.map import generate_map
import uuid

def adjust_date(date):
    date = date.split('-')
    date = list([date[1], date[2], date[0][2:]])

    if date[0][0] == '0' and date[1][0] == '0':
        date = list([date[0][1], date[1][1], date[2]])
    elif date[0][0] == '0':
        date = list([date[0][1], date[1], date[2]])
    elif date[1][0]:
        date = list([date[0], date[1][1], date[2]])

    date = '/'.join(date)
    return date

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

urlretrieve(url, 'static/_datasets/covid_global_cases.csv')
urlretrieve(url_deaths, 'static/_datasets/covid_global_deaths.csv')

# Leitura dos dados iniciais
df_cases = pd.read_csv('static/_datasets/covid_global_cases.csv')

df = df_cases # Será utilizado para gerar o mapa

df_deaths = pd.read_csv('static/_datasets/covid_global_deaths.csv')
df_pop = pd.read_csv('static/_datasets/population_by_country_2020.csv')
df_idh = pd.read_html('https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index')[1]


#agrupando por país e região
df_cases = group_country_region(df_cases)
df_deaths = group_country_region(df_deaths)

# Realizando tratamento do df_pop
df_pop = processes_pop_dataset(df_pop, df_cases)

#Deixando apenas os dados em comum entre df_pop, df_idh, df_cases e df_deaths
df_cases = inner_join_pop(df_cases, df_pop)
df_deaths = inner_join_pop(df_deaths, df_pop)

# Adicionando as colunas no df_cases e df_deaths
df_cases['Population'] = df_pop['Population (2020)']
df_cases['Density (P/Km²)'] = df_pop['Density (P/Km²)']
df_cases['Med. Age'] = df_pop['Med. Age']

df_deaths['Population'] = df_pop['Population (2020)']
df_deaths['Density (P/Km²)'] = df_pop['Density (P/Km²)']
df_deaths['Med. Age'] = df_pop['Med. Age']

# Realizando tratamento do df_idh
df_idh = processes_idh_dataset(df_idh, df_cases)

df_cases = inner_join_hdi(df_cases, df_idh)
df_deaths = inner_join_hdi(df_deaths, df_idh)


df_cases['HDI'] = df_idh['HDI']
df_deaths['HDI'] = df_idh['HDI']

df_cases['Contaminated Population (%)'] = df_cases.apply(
    lambda row: row[-6] / row['Population'] * 100, axis=1)

df_deaths['Dead Population (%)'] = df_deaths.apply(
    lambda row: row[-6] / row['Population'] * 100, axis=1)


#Gerando Mapa
m_1 = generate_map(df)

# Plotando gráficos iniciais
contaminated_age(df_cases=df_cases)

cases_country(df_cases=df_cases)

population_cases(df_cases=df_cases)

contaminated_density(df_cases=df_cases)

contaminated_hdi(df_cases=df_cases)

hdi_cases(df_cases=df_cases)

deaths_hdi(df_deaths=df_deaths)


app = Flask(__name__)

#Rotas

@app.route('/', methods=['GET', 'POST'])
def home():
    global df_cases
    global df_deaths
    return render_template('index.html', map=m_1._repr_html_(),
                        df_cases=df_cases.set_index('Country/Region').iloc[:20, -1:-15:-1],
                        df_deaths=df_deaths.set_index('Country/Region').iloc[:20, -1:-15:-1])

@app.route('/fter', methods=['GET', 'POST'])
def filtrar():
    global df_deaths
    global df_cases

    country1 = request.args.get('country1')
    country2 = request.args.get('country2')

    date_start = request.args.get('date-start')
    date_end = request.args.get('date-end')
    

    file_name1 = str(uuid.uuid4())
    file_name2 = str(uuid.uuid4())
    file_name3 = str(uuid.uuid4())
    file_name4 = str(uuid.uuid4())
    file_name5 = str(uuid.uuid4())
    file_name6 = str(uuid.uuid4())

    if (country1 != '') and (country2 == '') and (date_start != '') and (date_end != ''):
        try:
            date_start = adjust_date(date_start)
            date_end = adjust_date(date_end)
            
            df_dev, df_user = filter_1_country(df_cases, date_start, date_end, country1)
            df_dev_deaths, df_user_deaths = filter_1_country(df_deaths, date_start, date_end, country1)

            line_plot(df_dev.iloc[0], df_dev_deaths.iloc[0], file_name1, 'Linha de Crescimento - Casos e Mortes')

            line_plot2(df_dev, df_dev_deaths, file_name2)

            gr = f'../static/images/{file_name1}.png'
            gr2 = f'../static/images/{file_name2}.png'

            return render_template('filter1.html', filter=df_user, filter2= df_user_deaths,
            gr=gr, gr2=gr2, map=m_1._repr_html_())
        except:
            return render_template('error.html')

    elif (country1 != '') and (country2 != '') and (date_start != '') and (date_end != ''):
        try:
            date_start = adjust_date(date_start)
            date_end = adjust_date(date_end)

            df_dev, df_user = filter_2_country(df_cases, date_start, date_end, country1, country2)
            df_dev_deaths, df_user_deaths = filter_2_country(df_deaths, date_start, date_end, country1, country2)

            double_growth_line(df_dev, df_dev_deaths, file_name1)
            
            line_plot(df_dev.iloc[0], df_dev_deaths.iloc[0], file_name2, 'Casos / Óbitos - ' + df_dev.iloc[0]['Country/Region'])
            
            line_plot(df_dev.iloc[1], df_dev_deaths.iloc[1], file_name3, 'Casos / Óbitos - ' + df_dev.iloc[1]['Country/Region'])
            
            compare_hdi(df_dev, file_name4)
            
            compare_population(df_dev, file_name5)
            
            compare_density(df_dev, file_name6)

            gr = f'../static/images/{file_name1}.png'
            gr2 = f'../static/images/{file_name2}.png'
            gr3 = f'../static/images/{file_name3}.png'
            gr4 = f'../static/images/{file_name4}.png'
            gr5 = f'../static/images/{file_name5}.png'
            gr6 = f'../static/images/{file_name6}.png'
            

            return render_template('filter2.html', filter=df_user, 
                                    filter2=df_user_deaths, gr=gr, gr2=gr2, gr3=gr3,
                                    gr4=gr4, gr5=gr5, gr6=gr6, map=m_1._repr_html_())
        except:
            return render_template('error.html')

    elif (country1 == '') and (country2 == '') and (date_start != '') and (date_end != ''):
        try:
            date_start = adjust_date(date_start)
            date_end = adjust_date(date_end)

            df_dev, def_user = filter_date(df_cases, date_start, date_end)
            df_dev_deaths, df_user_deaths = filter_date(df_deaths, date_start, date_end)

            line_global(df_dev, date_start, date_end, file_name1)

            gr=f'../static/images/{file_name1}.png'

            return render_template('filter3.html', filter=df_dev, filter2=df_dev_deaths, gr=gr)
        except:
            return render_template('error.html')

    elif (country1 != '') and (country2 == '') and (date_start == '') and (date_end == ''):
        try:
            df = filter_country(df_cases, country1)
            df_deaths = filter_country(df_deaths, country1)

            start_end_pandm(df, file_name1, 'Casos')
            compare_population(df, file_name2)
            compare_density(df, file_name3)
            start_end_pandm(df_deaths, file_name4, 'Óbitos', 'red', 'dashed')

            gr = f'../static/images/{file_name1}.png'
            gr2 = f'../static/images/{file_name2}.png'
            gr3 = f'../static/images/{file_name3}.png'
            gr4 = f'../static/images/{file_name4}.png'

            
            return render_template('filter4.html',filter=df, filter2=df_deaths, gr=gr, gr2=gr2, gr3=gr3, gr4=gr4)
        except:
            return render_template('error.html')
    elif (country1 != '') and (country2 != '') and (date_start == '') and (date_end == ''):
        try:
            df_dev = filter_country_2(df_cases, country1, country2)
            df_dev_deaths = filter_country_2(df_deaths, country1, country2)

            double_start_end_pandm(df_dev, file_name1, 'Casos', 'red')
            double_start_end_pandm(df_dev_deaths, file_name2, 'Óbitos', 'red', 'dashed')

            gr = f'../static/images/{file_name1}.png'
            gr2 = f'../static/images/{file_name2}.png'

            return render_template('filter5.html',filter=df_dev, filter2=df_dev_deaths, gr=gr, gr2=gr2)
        except:
            return render_template('error.html')
if __name__ == '__main__':
    app.run()