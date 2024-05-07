import streamlit as st
# import altair as alt
import pandas as pd
import matplotlib.pyplot as plt

def getPlot(options):
    st.toast('Building a plot. Please wait...')

    fig = plt.figure(figsize=(17,6))
    df_filtered = df[['datetime', options['parameter'], 'pos']][(df.datetime >= options['date_parameter'][0]) * (df.datetime <= options['date_parameter'][1]) *
                                                            df["acnum"] == options["acnum"]]
    
    for pos in options["pos"]:
        plt.plot(df_filtered['datetime'][df_filtered["pos"] == pos], df_filtered[options['parameter']][df_filtered["pos"] == pos], linewidth = 1, label = "pos" + str(pos))
    
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

    acnum_parameter = st.selectbox("Select the acnum", pd.unique(df["acnum"]))

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

    for param in parameter_filter:
 #getting dict of options
        options = {
            "parameter": param,
            "date_parameter": [str(selected_min), str(selected_max)],
            "acnum": acnum_parameter,
            "pos": pos_parameter
        }
        
        
        getPlot(options)


# col = st.columns(1)
# with col[0]:
#     st.write('hi')

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
# print(chart_data)
# chart_data = pd.concat([df['datetime'], df['alt']])
# st.area_chart(chart_data)

# fig = plt.figure(figsize=(17,6))
# plt.plot(df["datetime"], df["alt"], linewidth = 1)
# st.pyplot(fig)

# st.write(text)