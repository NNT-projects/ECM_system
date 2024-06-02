import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json


def getPlot(options):
    st.toast('Building a plot. Please wait...')

    fig = plt.figure(figsize=(17, 6))
    df_filtered = df[['reportts', options['parameter'], 'pos']][
        (df.reportts >= options['time_start']) * (df.reportts <= options['time_end']) *
        df["acnum"] == options["acnum"]]

    for pos in options["pos"]:
        plt.plot(df_filtered['reportts'][df_filtered["pos"] == pos],
                 df_filtered[options['parameter']][df_filtered["pos"] == pos], linewidth=1, label="pos" + str(pos))

    plt.legend(loc="upper right", title="Legend", frameon=False)

    plt.xlabel('Date')

    # TODO полтянуть ylabel измерение параметра
    # plt.ylabel('Date')
    st.write(f"""#### {options["parameter"]} Score """)

    st.pyplot(fig)

    return


# ''' получение json
# with open('countries.geo.json') as json_file:
#     json_locations = json.load(json_file)
# '''


df = pd.read_csv("../data/data.csv")

st.set_page_config(
    page_title="Dashboard",
    layout="wide",
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
    # getting dict of options
    options = {
        "parameter": param_str,
        "time_start": str(selected_min),
        "time_end": str(selected_max),
        # "date_parameter": [str(selected_min), str(selected_max)],
        "acnum": acnum_str,
        "pos": pos_str
    }

    st.write("PARAMETES:")
    st.write(options)

    ## -------------------------------------------------------- 

    # ТЕСТИТЬ ПРИ РАБОЧЕМ БЭКЕ !!!!!!!

    response = requests.post("http://127.0.0.1:8000/items/", json=options)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response

        response_json = response.json()

        df = pd.DataFrame(response_json)

        # Display the JSON response in Streamlit
        st.write(df)
        st.json(response_json)
    else:
        st.write(f"Request failed with status code: {response.status_code}")

    ## -------------------------------------------------------- 

    ## ТЕСТИТЬ БЕЗ БЭКА !!!!!!!

    # with open('./data/response2.json', 'r') as json_file:
    #     data = json.load(json_file)

    # df = pd.DataFrame(data)

    # st.write(df)

    # st.json(data)

    ## -------------------------------------------------------- 

    # getPlot(options)
