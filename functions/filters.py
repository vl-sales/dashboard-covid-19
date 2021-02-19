import pandas as pd

# df_user -> df que aprecerá para o usuário
# df3 -> df utilizado para plotar os gráficos

# Filtro para quando é passado 1 país e as datas
def filter_1_country(df, date_start, date_end, country):
    df1 = df[df['Country/Region'] == country].loc[:, ['Country/Region', 'Population',
                                                                    'Density (P/Km²)', 'HDI']]
    df2 = df[df['Country/Region'] == country].loc[:, date_start :date_end]

    df3 = pd.concat([df1, df2], axis=1).reset_index(drop=True)

    df_user = pd.DataFrame(df3[['Country/Region', 'Population','Density (P/Km²)', 'HDI']]).reset_index(drop=True)
    df_user[f'casos até {date_end}'] = df3.iloc[:, -1]

    return df3, df_user


# Filtro para 2 países e com as datas
def filter_2_country(df, date_start, date_end, country, country2):
    df1 = df[(df['Country/Region'] == country) |
    (df['Country/Region'] == country2)].loc[:, ['Country/Region', 'Population','Density (P/Km²)', 'HDI']]

    df2 = df[(df['Country/Region'] == country) |
    (df['Country/Region'] == country2)].loc[:, date_start :date_end]

    df3 = pd.concat([df1,df2], axis=1).reset_index(drop=True)

    df_user = pd.DataFrame(df3[['Country/Region', 'Population',
    'Density (P/Km²)', 'HDI']])

    df_user[f'casos até {date_end}'] = df3.loc[:, date_end]

    return df3, df_user

# Filtrar somente por datas
def filter_date(df, date_start, date_end):
    df1 = df.loc[:, ['Country/Region', 'Population', 'Density (P/Km²)', 'HDI']]

    df2 = df.loc[:, date_start :date_end]

    df3 = pd.concat([df1,df2], axis=1)

    df_user = pd.DataFrame(df3[['Country/Region', 'Population',
    'Density (P/Km²)', 'HDI']])

    df_user[f'casos até {date_end}'] = df3.loc[:, date_end]

    return df3, df_user

def filter_country(df, country):
    df = df[df['Country/Region'] == country]
    return df

def filter_country_2(df, country, country2):
    '''
    Filtra dois países
    '''
    df = df[(df['Country/Region'] == country) | (df['Country/Region'] == country2)]

    return df
    