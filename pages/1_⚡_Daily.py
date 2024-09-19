import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt
import datetime as dt


st.set_page_config(page_title ='Power Consumption')
# st.header('Power Consumption')
st.subheader('')

#---------------------------------------------------------------- ALl Functions
##---------------------------- 1) Load data
def load_data(df1, df2):
    df = pd.concat([df1, df2], ignore_index=True)

    df = df.sort_values(by='created_at')
    df.reset_index(drop=True, inplace=True)
    df['entry_id'] = range(1, len(df) + 1)

    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date
    df['day'] = df['created_at'].dt.day
    df['month'] = df['created_at'].dt.month
    df['year'] = df['created_at'].dt.year
    df['field3'] = abs(df['field3']/1000).round(decimals=2)
    df['Cost_in_\u20B9'] = df['field3']*6.25

    df = df.rename(columns={'entry_id' : 'ON_records', 'field3' : 'Units', 'month' : 'Months', 'date' : 'Dates'})
    return df


# st.dataframe(df)

##------------------------------------------2) to group and select 
def to_group_and_select(df_selection):
    consp1 = (
    df_selection.groupby(by=['Dates'])[['Units']].sum()
    )
    consp2 = (
        df_selection.groupby(by=['Months'])[['Units']].sum() 
        )
    consp3 = (
        df_selection.groupby(by=['ON_records'])[['Units']].sum()
    )
    consp4 = (
        df_selection.groupby(by=['Dates'])[['Cost_in_\u20B9']].sum()
    )
    return consp1, consp2, consp3, consp4


#-------------------------------------3) Recent Highlights
def highlight_column(dataset):
    ta_d = df.groupby(by=['Dates'])[['Units']].sum()
    c_p = df.groupby(by=['Dates'])[['Cost_in_\u20B9']].sum()

    total_daily = int(ta_d.iloc[-1])
    average_daily = round(ta_d.values.mean())
    cost_perday = round(int(c_p.iloc[-1]))

    left_column, middle_column, right_column = st.columns(3, gap="large")
    with left_column:
        st.subheader("Recently Used :")
        st.subheader(f"{total_daily:,} Units")
    with middle_column:
        st.subheader("Average Usage :")
        st.subheader(f"{average_daily} Units")
    with right_column:
        st.subheader("Recent Cost :")
        st.subheader(f"\u20B9 {cost_perday}")

    st.markdown("""---""")


#-----------------------------------  4) Visualize start 
# # Power by Daily  chart 1
def visualize_chart1_daily(consp):
    fig_daily = px.scatter(
    consp,
    x=consp.index,
    y="Units",
    orientation="v",
    title="<b>Real Time Consumption</b>",
    color_discrete_sequence=["#0083B8"] * len(consp),
    template="plotly_white",
    )
    fig_daily.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
    )
    return st.plotly_chart(fig_daily, use_container_width=True)

# Power by Date chart 2
def visualize_chart2_day(consp):
    fig_day = px.bar(
        consp,
        x=consp.index,
        y="Units",
        orientation="v",
        title="<b>Daily Electricity Consumption</b>",
        color_discrete_sequence=["#0083B8"] * len(consp),
        template="plotly_white",
    )
    fig_day.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        bargap=0.20,  # Adjust this value to set the gap between bars
        
    )

    fig_day.update_xaxes(
        range=[consp.index.min(), consp1.index.max()],
        tickvals=consp.index,
        ticktext=[date.strftime("%d %b") for date in consp.index]
    )
    return st.plotly_chart(fig_day, use_container_width=True)

# Costs by Date chart 3
def visualize_chart3_cday(consp):
    fig_cday = px.bar(
        consp,
        x=consp.index,
        y="Cost_in_\u20B9",
        orientation="v",
        title="<b>Daily Cost</b>",
        color_discrete_sequence=["#0083B8"] * len(consp),
        template="plotly_white",
    )
    fig_cday.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        bargap=0.20,  # Adjust this value to set the gap between bars
        
    )
    # Formatting x-axis tick labels to display dates like "22 Jan"
    fig_cday.update_xaxes(
        range=[consp.index.min(), consp.index.max()],
        tickvals=consp.index,
        ticktext=[date.strftime("%d %b").upper() for date in consp.index]  # Using strftime to format dates and .upper() to convert to uppercase
    )
    return st.plotly_chart(fig_cday)

## --------------------------------------5) Day's Total Units and Cost Table
def days_table(table1, table4):
    left_column, right_column = st.columns(2, gap="large")
    with left_column:
        st.subheader("Day's Units Table")
        st.dataframe(table1)
    with right_column:
        st.subheader("Day's Cost Table")
        st.dataframe(table4)

#--------------------------------------------------------------Executing Functions

#----------------------------------------------------------------------------------------------------------Device 1



df1 = pd.read_csv('3.csv')
df2 = pd.read_csv('all_data.csv')
#load data
df = load_data(df1=df1, df2=df2)

# -------------SIDEBAR 

st.sidebar.header("Please select :")

day = st.sidebar.multiselect(
    "Select Day:",
    options = sorted(df['day'].unique()),
    default = sorted(df['day'].unique())   
)

Months = st.sidebar.multiselect(
    "Select Month:",
    options = sorted(df['Months'].unique()),
    default = sorted(df['Months'].unique())   
)

year = st.sidebar.multiselect(
    "Select Year:",
    options = sorted(df['year'].unique()),
    default = sorted(df['year'].unique())   
)

df_selection1 = df.query(
    "day == @day & Months == @Months & year == @year"
)

#st.dataframe(df_selection)


# ---- Page Heading----
st.title(":bar_chart: Daily Meter")
with st.container():
    image = Image.open('Images/BlackBanner.png')
    st.image(image, caption ="", use_column_width = True)

st.markdown("##")
st.subheader("Device 1 : T-Bulb")
st.markdown("""---""")


# Recent Highlights variables
consp1, consp2, consp3, consp4 = to_group_and_select(df_selection1)

#-----Recent Highlights
highlight_column(df)

#-----------------------------------Visualize start 
# Units by Daily chart [SCATTER PLOT]
visualize_chart1_daily(consp3)

# Units by Date [BAR CHART]
visualize_chart2_day(consp1)

# Costs by Date [BAR CHART]
visualize_chart3_cday(consp4)


st.markdown("""---""")
###---------------------------Visualize end

## Day's Total Units and Cost Tables
days_table(consp1, consp4)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)