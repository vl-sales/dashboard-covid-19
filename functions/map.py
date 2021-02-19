import folium

def lat_long(country, lat, long, df_cases):
    df_cases.loc[country] = df_cases.loc[country].replace([df_cases.loc[country].Lat,
                                                             df_cases.loc[country].Long],
                                                            [lat, long])

def generate_map(df):
    df_cases = df.groupby('Country/Region').sum()

    lat_long('Australia', -24.7761086, 134.755, df_cases)
    lat_long('Canada', 61.0666922, -107.9917071, df_cases)
    lat_long('China', 34.2189, 104.9732, df_cases)
    lat_long('France', 46.603354, 1.8883335, df_cases)
    lat_long('United Kingdom', 54.7023545, -3.2765753, df_cases)
    lat_long('Netherlands', 52.4253, 5.5492, df_cases)
    lat_long('Denmark', 55.6646, 9.3946, df_cases)
    

    df_cases.reset_index(inplace=True)

    lat_br = df_cases[df_cases['Country/Region'] == 'Brazil'].Lat
    long_br = df_cases[df_cases['Country/Region'] == 'Brazil'].Long

    m_1 = folium.Map(location=[lat_br.values[0], long_br.values[0]], tiles='cartodbpositron', zoom_start=2)

    for idx, row in df_cases.iterrows():
        folium.CircleMarker(location=(row['Lat'], row['Long']), radius=row[-1]*300/df_cases.iloc[:, -1].sum(),
                            color='blue', fill=True, fillcolor='lightblue',
                            tooltip= f'{df_cases.iloc[idx][0]}: {row[-1]}').add_to(m_1)
    
    return m_1
