import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json

def getPlot(df):
    st.toast('Building a plot. Please wait...')

    fig = plt.figure(figsize=(17,6))
    # df_filtered = df[['datetime', options['parameter'], 'pos']][(df.datetime >= options['time_start']) * (df.datetime <= options['time_end']) *
    #          
    #                                                df["acnum"] == options["acnum"]]
    
    ax = plt.gca()

    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Основные деления - месяцы
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())  # Вспомогательные деления - дни недели
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Формат даты

    param = df.columns[-1]
    for pos in pd.unique(df["pos"]):
        plt.plot(df['reportts'][df["pos"] == pos], df[param][df["pos"] == pos], linewidth = 1, label = "pos" + str(pos))
    


    plt.legend(loc="upper right", title="Legend", frameon=False)

    plt.xlabel('Date')


    #TODO полтянуть ylabel измерение параметра
    # plt.ylabel('Date')
    st.write(f"""#### {param} Score """)
    
    st.pyplot(fig)

    return

with open('../data/response2.json', 'r') as json_file:
    data = json.load(json_file)
    
df = pd.DataFrame(data)

acnum_parameter = list(pd.unique(df["acnum"]))
parameter_filter = df.columns[3:]

for acnum in acnum_parameter:
    for param in parameter_filter:
        print(param)
        getPlot(df[["reportts", "acnum", "pos", param]][df["acnum"] == acnum])