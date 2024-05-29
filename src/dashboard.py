import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

# def getPlot(options):
def getPlot(df):
    st.toast('Building a plot. Please wait...')

    fig = plt.figure(figsize=(17,6))
    # df_filtered = df[['datetime', options['parameter'], 'pos']][(df.datetime >= options['time_start']) * (df.datetime <= options['time_end']) *
    #                                                         df["acnum"] == options["acnum"]]
    
    param = df.columns[-1]
    for pos in options["pos"]:
        plt.plot(df['reportts'][df["pos"] == pos], df[param][df["pos"] == pos], linewidth = 1, label = "pos" + str(pos))
    


    plt.legend(loc="upper right", title="Legend", frameon=False)

    plt.xlabel('Date')


    #TODO полтянуть ylabel измерение параметра
    # plt.ylabel('Date')
    st.write(f"""#### {options["parameter"]} Score """)
    
    st.pyplot(fig)

    return

# ''' получение json
# with open('countries.geo.json') as json_file:
#     json_locations = json.load(json_file)
# '''


df = pd.read_excel("data.xlsx")

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

    parameter_filter = st.multiselect("Select the parameter", df.columns[7:])

    MIN_MAX_RANGE = (df["datetime"].min().date(), df["datetime"].max().date())
    PRE_SELECTED_DATES = (df["datetime"].min().date(), df["datetime"].max().date())
    selected_min, selected_max = st.slider(
        "Datetime slider",
        value=PRE_SELECTED_DATES,
        min_value=MIN_MAX_RANGE[0],
        max_value=MIN_MAX_RANGE[1],
    )


if st.sidebar.button("Update plots"):

    parameter_str = ", ".join(parameter_filter)
    pos_str = ", ".join(list(map(str, pos_parameter)))
    acnum_str = ", ".join(acnum_parameter)

    # for acnum in acnum_parameter:
    #     for param in parameter_filter:
    #     #getting dict of options
    #         options = {
    #             "parameter": param,
    #             "time_start": str(selected_min),
    #             "time_end": str(selected_max),
    #             # "date_parameter": [str(selected_min), str(selected_max)],
    #             "acnum": acnum,
    #             "pos": pos_parameter
    #         }

    options = {
            "parameter": parameter_str,
            "time_start": str(selected_min),
            "time_end": str(selected_max),
            "acnum": acnum_str,
            "pos": pos_str
        }
    
    print(options)


        
   
    # response = requests.post("http://127.0.0.1:8000/items/", json=options)

    # if response.status_code == 200:
    #     st.success(f"Ответ от сервера: {response.json()}")
    # else:
    #     st.error(f"Ошибка: {response.status_code}")

    # df = pd.DataFrame(response)
 

    with open('../data/response2.json', 'r') as json_file:
        data = json.load(json_file)
    
    df = pd.DataFrame(data)

    for acnum in acnum_parameter:
        for param in parameter_filter:
            print(param)
            getPlot(df[["reportts", "acnum", "pos", param]][df["acnum"] == acnum])
