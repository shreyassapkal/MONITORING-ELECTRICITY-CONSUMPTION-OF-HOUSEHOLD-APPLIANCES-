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

    df = df.rename(columns={'entry_id' : 'on_records', 'field3' : 'Units', 'month' : 'Months', 'date' : 'Dates'})
    return df


# st.dataframe(df)

##------------------------------------------2) to group and select 
def to_group_and_select(df_selection):
    consp1 = (
        df_selection.groupby(by=['year'])[['Units']].sum()
        )
    consp2 = (
        df_selection.groupby(by=["Months"])[["Units"]].sum() 
        )
    consp3 = (
        df_selection.groupby(by=['Months'])[['Cost_in_\u20B9']].sum()
    )
    return consp1, consp2, consp3


#-------------------------------------3) Recent Highlights
def highlight_column(dataset):
    t_y = df.groupby(by=['year'])[['Units']].sum()
    r_c = df.groupby(by=["Months"])[["Units"]].sum() 
    c_p = df.groupby(by=['Months'])[['Cost_in_\u20B9']].sum()

    total_yearly = int(t_y.iloc[-1])
    recent_month = round(int(r_c.iloc[-1]))
    average_monthly = round(r_c.values.mean())
    cost_permonth = abs(int(c_p.iloc[-1]))

    col1, col2, col3, col4 = st.columns(4, gap='large')

    with col1:
        st.subheader("Recent Usage :")
        st.subheader(f"{recent_month} Units")
    with col2:
        st.subheader("Average Usage :")
        st.subheader(f"{average_monthly} Units")
    with col3:
        st.subheader("Yearly Total :")
        st.subheader(f"{total_yearly} Units")
    with col4:
        st.subheader("Recent Cost :")
        st.subheader(f"\u20B9 {cost_permonth}")

    st.markdown("""---""")


#-----------------------------------  4) Visualize start 
months_dict = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MAY",
    6: "JUN",
    7: "JUL",
    8: "AUG",
    9: "SEP",
    10: "OCT",
    11: "NOV",
    12: "DEC"
}

# # Units by Month chart 1 [BAR CHART]
def visualize_chart1_monthlybar(consp):

    fig_month = px.bar(
        consp,
        x=consp.index,
        y="Units",
        orientation="v",
        title="<b>Monthly Electricity Consumption</b>",
        color_discrete_sequence=["#0083B8"] * len(consp2),
        template="plotly_white",
    )
    fig_month.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        bargap=0.1,  # Adjust this value to set the gap between bars
        bargroupgap=0.1
    )
    fig_month.update_xaxes(
        tickvals=consp.index,
        ticktext=[months_dict[month] for month in consp.index]
    )

    return st.plotly_chart(fig_month, use_container_width=True)

# Units by Month chart 2 [PIE CHART]
def visualize_chart2_monthlypie(consp):

    fig_month_pie = px.pie(
        values=consp["Units"],
        names=[months_dict[Months] for Months in consp.index],  
        title="<b>Monthly Electricity Consumption</b>",
        color_discrete_sequence=px.colors.sequential.Plasma,  # Set of 12 visually distinct colors
        template="plotly_white"
    )
    fig_month_pie.update_traces(textinfo='percent+label') 

    return st.plotly_chart(fig_month_pie, use_container_width=True)

# Costs by Months chart 3 [BAR CHART]
def visualize_chart3_mcost(consp):
    fig_mcost = px.bar(
        consp,
        x=consp.index,
        y="Cost_in_\u20B9",
        orientation="v",
        title="<b>Monthly Bill</b>",
        color_discrete_sequence=["#0083B8"] * len(consp),
        template="plotly_white",
    )
    fig_mcost.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        bargap=0.1,  
        bargroupgap=0.1  
    )
    fig_mcost.update_xaxes(
        tickvals=consp.index,
        ticktext=[months_dict[month] for month in consp.index]
    )

    st.plotly_chart(fig_mcost)


## --------------------------------------5) Months Total Units and Cost Table
def days_table(table1, table3):
    left_column, right_column = st.columns(2, gap="large")
    with left_column:
        st.subheader("Monthly Units Table")
        st.dataframe(table1)
    with right_column:
        st.subheader("Monthly Cost Table")
        st.dataframe(table3)

#--------------------------------------------------------------Executing Functions

#----------------------------------------------------------------------------------------------------------Device 1



df1 = pd.read_csv('3.csv')
df2 = pd.read_csv('all_data.csv')
#load data
df = load_data(df1=df1, df2=df2)

# -------------SIDEBAR 

st.sidebar.header("Please select :")

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

df_selection = df.query(
    "Months == @Months & year == @year"
)

#st.dataframe(df_selection)


# ---- Page Heading----
st.title(":bar_chart: Monthly Meter")
with st.container():
    image = Image.open('Images/BlackBanner.png')
    st.image(image, caption ="", use_column_width = True)

st.markdown("##")
st.subheader("Device 1 : T-Bulb")
st.markdown("""---""")


# Recent Highlights variables
consp1, consp2, consp3 = to_group_and_select(df_selection)

#-----Recent Highlights
highlight_column(df)

#-----------------------------------Visualize start 
# Units by Month chart [BAR CHART]
visualize_chart1_monthlybar(consp2)

# Units by Month [PIE CHART]
visualize_chart2_monthlypie(consp2)

# Costs by Month [BAR CHART]
visualize_chart3_mcost(consp3)


st.markdown("""---""")
###---------------------------Visualize end

## Months Total Units and Cost Tables
days_table(consp2, consp3)




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)