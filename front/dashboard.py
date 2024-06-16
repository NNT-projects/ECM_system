import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
# from matplotlib.ticker import MaxNLocator
# from matplotlib.ticker import MultipleLocator

def getPlot(df_filtered):
    st.toast('Building a plot. Please wait...')

    param = df_filtered.columns[-1]

    # Преобразование столбцов в соответствующие типы данных
    df_filtered['reportts'] = pd.to_datetime(df_filtered['reportts'])
    df_filtered[param] = df_filtered[param].astype(float)

    fig = plt.figure(figsize=(17, 6))
    sns.lineplot(x='reportts', y=param, hue='pos', data=df_filtered, alpha=0.7)

    # Настройка меток осей и заголовка
    plt.xlabel('Time')
    plt.ylabel('EGTM')
    plt.title('EGTM Over Time for Different Positions')

    # Добавление сетки
    plt.grid(True)

    # Отображение графика
    st.pyplot(fig)

def getPlot1(df_filtered):
    st.toast('Building a plot. Please wait...')

    fig, ax = plt.subplots(figsize=(17,6))
    # ax.plot(x, y)

    # Преобразование столбцов в соответствующие типы данных
    df_filtered['reportts'] = pd.to_datetime(df_filtered['reportts'])
    df_filtered[param] = df_filtered[param].astype(float)

    # fig = plt.figure(figsize=(17,6))
    # df_filtered = df[['reportts', options['parameters'], 'pos']][(df.reportts >= options['time_start']) * (df.reportts <= options['time_end'])]
    
    param = df_filtered.columns[-1]
    all_pos = pd.unique(df_filtered['pos'])

    for pos in all_pos:
        # ax.plot(df_filtered['reportts'][df_filtered["pos"] == pos].dt.date, df_filtered[param][df_filtered["pos"] == pos], linestyle='-', alpha=0.7, linewidth = 2, label = "pos" + str(pos))
        # ax.grid(True)
        plt.plot(df_filtered['reportts'][df_filtered["pos"] == pos].dt.date, df_filtered[param][df_filtered["pos"] == pos], linestyle='-', alpha=0.7, linewidth = 2, label = "pos" + str(pos))


    # ax.yaxis.set_major_locator(MaxNLocator(nbins=5))  # nbins - максимальное количество делений
    # ax.yaxis.set_major_locator(MultipleLocator(0.5))  # Шаг между делениями


    plt.legend(loc="upper right", title="Legend", frameon=False)

    plt.xlabel('Date')


    #TODO полтянуть ylabel измерение параметра
    # plt.ylabel('Date')
    st.write(f"""#### {param} Score """)
    
    st.pyplot(fig)

    return

# ''' получение json
# with open('countries.geo.json') as json_file:
#     json_locations = json.load(json_file)
# '''


df = pd.read_csv("../data/X_with_predictions_BDU.csv")

st.set_page_config(
    page_title = "Dashboard",
    layout = "wide",
    initial_sidebar_state="expanded"
)

# alt.themes.enable("dark")
with st.sidebar:

    st.header("Options")

    sort_acnum = pd.unique(df["acnum"])
    acnum_parameter = st.multiselect("Select the acnum", sort_acnum, default=sort_acnum[0])

    sort_pos = pd.unique(df['pos'])
    pos_parameter = st.multiselect("Select the pos", sort_pos, default=sort_pos)

    parameter_filter = st.multiselect("Select the parameter", df.columns[7:], default=['alt','acct','egtm'])
    df['reportts'] = pd.to_datetime(df['reportts'])
    MIN_MAX_RANGE = (df["reportts"].min().date(), df["reportts"].max().date())
    PRE_SELECTED_DATES = (df["reportts"].min().date(), df["reportts"].max().date())
    selected_min, selected_max = st.slider(
        "Datetime slider",
        value=PRE_SELECTED_DATES,
        min_value=MIN_MAX_RANGE[0],
        max_value=MIN_MAX_RANGE[1],
    )


if st.sidebar.button("Update plots"):

    pos_str = ', '.join(map(str, pos_parameter))
    param_str = ', '.join(map(str, parameter_filter))
    acnum_str = ', '.join(map(str, acnum_parameter))

    # for acnum in acnum_parameter:
    #     for param in parameter_filter:
        #getting dict of options
    options = {
        "parameters": param_str,
        "time_start": str(selected_min),
        "time_end": str(selected_max),
        # "date_parameter": [str(selected_min), str(selected_max)],
        "acnum": acnum_str,
        "pos": pos_str
    }

    st.write("PARAMETES:")
    st.write(options)

    # -------------------------------------------------------- 

    # ТЕСТИТЬ ПРИ РАБОЧЕМ БЭКЕ !!!!!!!

    response = requests.post("http://127.0.0.1:8000/items/", json=options)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response

        response_json = response.json()

        df = pd.DataFrame(response_json)
        df['reportts'] = pd.to_datetime(df['reportts'])

        # Display the JSON response in Streamlit
        st.write(df)
        st.json(response_json)
    else:
        st.write(f"Request failed with status code: {response.status_code}")
    # --------------------------------------------------------

    # ## ТЕСТИТЬ БЕЗ БЭКА !!!!!!!
    # options = {
    #     "parameters": "ffr, foc",
    #     "time_start": "2018-12-24",
    #     "time_end": "2019-03-05",
    #     "acnum": "VQ-BDU",
    #     "pos": "1, 2"
    # }
    # acnum_parameter = ['VQ-BDU']
    # parameter_filter = ['ffr', 'foc']
    
    # with open('../data/response2.json', 'r') as json_file:
    #     data = json.load(json_file)

    # df = pd.DataFrame(data)

    # st.write(df)

    # st.json(data)

    ## -------------------------------------------------------- 

    for acnum in acnum_parameter:
        for param in parameter_filter:
            print(df[['reportts', 'acnum', 'pos', param]][(df['acnum'] == acnum) * 
                (df['reportts'] >= options['time_start']) * (df['reportts'] <= options['time_end'])].head(30))
            getPlot(df[['reportts', 'acnum', 'pos', param]][(df['acnum'] == acnum) * 
                (df['reportts'] >= options['time_start']) * (df['reportts'] <= options['time_end'])])