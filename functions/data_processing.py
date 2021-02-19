def group_country_region(df):
    df_group = df.groupby('Country/Region').sum()
    df_group.reset_index(inplace=True)
    df_group.drop(['Lat', 'Long'], axis=1, inplace=True)
    return df_group

def processes_pop_dataset(df_pop, df_cases):
    df_pop['Country (or dependency)'] = df_pop['Country (or dependency)'].apply(
    lambda x: 'US' if x == 'United States' else x)

    # Deixando apenas os paises em comunm no df_pop
    df_pop = df_pop[df_pop['Country (or dependency)'].isin(df_cases['Country/Region'])]

    # Ordenação dos dados por ordem alfabetica dos paises igual no df_cases e df_deaths
    df_pop = df_pop.sort_values('Country (or dependency)').reset_index(drop=True)

    return df_pop

def change_name(country):
    if country == 'United States':
        return 'US'
    elif country == 'Cape Verde':
        return 'Cabo Verde'
    else:
        return country

def processes_idh_dataset(df_idh, df_cases):
    df_idh.drop(['Rank', 'Unnamed: 5_level_0'], axis=1, inplace=True)
    df_idh.columns = ['Country or Territory', 'HDI', 'Average annual HDI growth (2010-2019)']
    
    df_idh['Country or Territory'] = df_idh['Country or Territory'].apply(change_name)

    df_idh = df_idh.sort_values('Country or Territory').reset_index(drop=True)
    df_idh.sort_values('Country or Territory')
    df_idh = df_idh[df_idh['Country or Territory'].isin(df_cases['Country/Region'])].reset_index(drop=True)


    df_idh['HDI'] = df_idh['HDI'].astype('float64')

    return df_idh

def inner_join_pop(df, df2):
    df = df[df['Country/Region'].isin(df2['Country (or dependency)'])].sort_values('Country/Region').reset_index(drop=True)
    return df

def inner_join_hdi(df, df2):
    df = df[df['Country/Region'].isin(df2['Country or Territory'])].reset_index(drop=True)
    return df
