import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Gráfico de casos por média de idade
def contaminated_age(df_cases, save='static/images/age_contaminated3.png'):
    df_idades = df_cases[df_cases['Med. Age'] != 'N.A.'].sort_values(['Med. Age']).reset_index(drop=True)
    
    plt.figure(figsize=(8, 6))
    
    sns.scatterplot(data=df_idades, y='Contaminated Population (%)', x='Med. Age')

    plt.title('População Contaminada (%) X Idade Média', fontsize=16)

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=14)

    plt.xlabel('Idade Média', fontsize=12)
    plt.ylabel('População Contaminada (%)', fontsize=16)

    plt.tight_layout()

    plt.savefig(save, backend='agg')
    plt.close()

# Gráfico de casos por país
def cases_country(df_cases, save='static/images/cases_country1.png'):
    plt.figure(figsize=(16,6))

    sns.barplot(data=df_cases, y=df_cases.iloc[:, -6], x='Country/Region')

    plt.title('Casos/País', fontsize=16)
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=16)

    plt.xlabel('Países', fontsize=20)
    plt.ylabel('Total de Casos', fontsize=20)

    plt.tight_layout()

    plt.savefig(save, backend='agg')
    plt.close()

# Relação entre população total e população contaminada
def population_cases(df_cases, save='static/images/population_cases6.png'):
    plt.figure(figsize=(8,6))
    sns.jointplot(data=df_cases[df_cases['Population'] <= 900_000_000],
                x='Population', y='Contaminated Population (%)', kind='kde')

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.xlabel('População', fontsize=11)
    plt.ylabel('População Contaminada', fontsize=11)

    plt.tight_layout()

    plt.savefig(save, backend='agg')
    plt.close()

def contaminated_density(df_cases, save='static/images/density_contaminated2.png'):
    plt.figure(figsize=(8, 6))

    sns.scatterplot(data=df_cases[df_cases['Density (P/Km²)'] <= 800],
    y='Contaminated Population (%)', x='Density (P/Km²)')
    
    plt.title('População Contaminada (%) X Densidade Demográfica', fontsize=16)

    plt.xlabel('Densidade Demográfica (P/Km²)')
    plt.ylabel('População Contaminada (%)')

    plt.savefig(save, backend='agg')
    plt.close()

# População contaminada X IDH
def contaminated_hdi(df_cases, save='static/images/contaminated_hdi1.png'):
    plt.figure(figsize=(10, 8))
    sns.lmplot(data=df_cases, y='Contaminated Population (%)', x='HDI')

    plt.title('População Contaminada X IDH', fontsize=16)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
        
    plt.xlabel('IDH', fontsize=16)
    plt.ylabel('População Contaminada (%)', fontsize=16)

    plt.tight_layout()

    plt.savefig(save, backend='agg')
    plt.close()

# População contaminada X IDH
def hdi_cases(df_cases, save='static/images/hdi_cases3.png'):
    plt.figure(figsize=(10, 8))
    g = sns.jointplot(data=df_cases, y='Contaminated Population (%)', x='HDI')
    g.plot_joint(sns.kdeplot, color="r", zorder=0, levels=6)
    g.plot_marginals(sns.rugplot, color="r", height=-.15, clip_on=False)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.xlabel('IDH', fontsize=16)
    plt.ylabel('População Contaminada (%)', fontsize=16)

    plt.tight_layout()

    plt.savefig(save, backend='agg')
    plt.close()

# Mortes X IDH
def deaths_hdi(df_deaths, save='static/images/deaths_hdi1.png'):
    plt.figure(figsize=(12, 8))
    sns.jointplot(data=df_deaths, y='Dead Population (%)', x='HDI', kind='hex')

    plt.title('Mortes X IDH', fontsize=20)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.xlabel('IDH', fontsize=16)
    plt.ylabel('População Morta (%)', fontsize=16)

    plt.tight_layout()
    plt.savefig(save, backend='agg')
    plt.close()

# Plots para filtros

def line_plot(df, df_deaths, file, title='Linha de Crescimento'):
    '''
    Plota gráfico de linha de casos e mortos em gráficos diferentes
    '''
    plt.figure(figsize=(12,8))

    plt.subplot(2, 1, 1)
    
    plt.plot(df.iloc[5:], marker='o', label='Casos')
    plt.title(title, fontsize=20)

    plt.ylabel('Total de casos', fontsize=16)
    plt.xlabel('Data', fontsize=16)

    plt.xticks(fontsize=10, rotation=70)
    plt.yticks(fontsize=14)
    
    plt.legend()

    plt.subplot(2, 1, 2)

    plt.plot(df_deaths.iloc[5:], marker='o', color='r', linestyle='dashed', label='Mortes')

    plt.legend()
    
    plt.ylabel('Total de Óbitos', fontsize=16)
    plt.xlabel('Data', fontsize=16)

    plt.xticks(fontsize=10, rotation=70)
    plt.yticks(fontsize=14)

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png', backend='agg')
    plt.close()

def line_plot2(df, df2, file):
    '''
    Plota linha de mortes e casos no mesmo axis
    '''
    plt.figure(figsize=(12,8))

    plt.plot(df.iloc[0, 5:], marker='o', label='Casos')
    plt.plot(df2.iloc[0, 5:], marker='o', color='r', linestyle='dashed', label='Mortes')

    plt.title('Diferença entre Casos e Mortes', fontsize=20)

    plt.legend()
    
    plt.ylabel('Total de casos', fontsize=16)
    plt.xlabel('Data', fontsize=16)

    plt.xticks(fontsize=10, rotation=60)
    plt.yticks(fontsize=14)

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png', backend='agg')
    plt.close()

# gráficos para pesquisas por 2 países

def double_growth_line(df, df_deaths, file):
    plt.figure(figsize=(12,8))

    plt.subplot(2, 1, 1)

    plt.plot(df.iloc[0, 5:], marker='o', label=df.iloc[0]['Country/Region'])
    plt.plot(df.iloc[1, 5:], marker='o', label=df.iloc[1]['Country/Region'], color='yellow')

    plt.title('Casos', fontsize=20)

    plt.ylabel('Total de casos', fontsize=16)
    plt.xlabel('Data', fontsize=16)

    plt.xticks(fontsize=10, rotation=70)
    plt.yticks(fontsize=10)
    
    plt.legend()

    plt.subplot(2, 1, 2)
    
    plt.plot(df_deaths.iloc[0, 5:], marker='o', color='r', linestyle='dashed', label=df.iloc[0]['Country/Region'])
    plt.plot(df_deaths.iloc[1, 5:], marker='o', label=df.iloc[1]['Country/Region'], color='green', linestyle='dashed')

    plt.title('Mortes', fontsize=20)

    plt.ylabel('Total de óbitos', fontsize=16)
    plt.xlabel('Data', fontsize=16)

    plt.xticks(fontsize=10, rotation=70)
    plt.yticks(fontsize=10)
    
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png', backend='agg')
    plt.close()

def compare_hdi(df, file):
    plt.figure(figsize=(10,6))

    sns.barplot(data=df, x='HDI', y='Country/Region')

    plt.title('IDH / País', fontsize=22)

    plt.xlabel('IDH', fontsize=16)
    plt.ylabel('País', fontsize=16)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png')
    plt.close()

def compare_population(df, file):
    plt.figure(figsize=(10,6))

    sns.barplot(data=df, x='Population', y='Country/Region')

    plt.title('População / País', fontsize=22)

    plt.xlabel('População', fontsize=16)
    plt.ylabel('País', fontsize=16)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png')
    plt.close()

def compare_deaths(df, file):
    plt.figure(figsize=(10,6))

    sns.barplot(data=df, x=df.iloc[:, -5], y='Country/Region')

    plt.title('Mortes / País', fontsize=22)

    plt.xlabel('Total de mortes', fontsize=16)
    plt.ylabel('País', fontsize=16)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png')
    plt.close()

def compare_cases(df, file):
    plt.figure(figsize=(10,6))

    sns.barplot(data=df, x=df.iloc[:, -6], y='Country/Region')

    plt.title('Casos / País', fontsize=22)

    plt.xlabel('Total de casos', fontsize=16)
    plt.ylabel('País', fontsize=16)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png')
    plt.close()

def compare_density(df, file):
    plt.figure(figsize=(10,6))

    sns.barplot(data=df, x='Density (P/Km²)', y='Country/Region')

    plt.title('Densidade Demográfica / País', fontsize=22)

    plt.xlabel('Densidade (P/Km²)', fontsize=16)
    plt.ylabel('País', fontsize=16)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png')
    plt.close()

def line_global(df,date_start, date_end, file):
    for i in range(len(df)):
        plt.plot(df.iloc[i][date_start:date_end], label=df.iloc[i]['Country/Region'])
    
    plt.legend()

    plt.title('Linha de crescimento por país')

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png')

def start_end_pandm(df, file, name, color='blue', linestyle='-'):
    plt.figure(figsize=(8, 6))

    plt.plot(df.iloc[0, 1:-5], label='Casos', color=f'{color}', linestyle=f'{linestyle}')
    plt.xticks(ticks=np.arange(0, df.shape[1], 20), fontsize=10, rotation=60)

    plt.title(f'Linha do tempo da pandemia - {name}')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png')
    plt.close()

def double_start_end_pandm(df, file, name, color='blue', linestyle='-'):
    plt.figure(figsize=(8, 6))

    plt.plot(df.iloc[0, 1:-5], label=df.iloc[0]['Country/Region'],color='blue', linestyle=f'{linestyle}')

    plt.plot(df.iloc[1, 1:-5], label=df.iloc[1]['Country/Region'], color=f'{color}', linestyle=f'{linestyle}')
    
    plt.xticks(ticks=np.arange(0, df.shape[1], 20), fontsize=10, rotation=60)

    plt.title(f'Linha do tempo da pandemia - {name}')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'static/images/{file}.png')
    plt.close()