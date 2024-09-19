from PIL import Image
import pandas as pd
import streamlit as st



st.set_page_config(
    page_title = 'Welcome Power Savers',
    page_icon = "",

)
with st.container():

    # CSS styling for the logout button
    logout_button_style = """
    <style>
    .logout-button {
    background-color: black; /* Coral color */
    color: black; /* White text color */
    border: none;
    padding: 5px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 15px;
    font-weight: bold;
    display: inline-block;
    transition: background-color 0.3s ease;
    }

    .logout-button:hover {
    background-color: white; /* Darker coral color on hover */
    }
    </style>
    """

    # Add CSS styling to the app
    st.markdown(logout_button_style, unsafe_allow_html=True)

    logout_link = """
    <a href="http://localhost:8081/login" class="logout-button">Logout</a>
    """
    col1,col2,col3, col4,col5 = st.columns(5)
    with col1:
        st.empty()
    with col2:
        st.empty()
    with col3:
        st.empty()
    with col4:
        st.empty()
    with col5:
        st.markdown(logout_link, unsafe_allow_html=True)

st.title('Electricity Consumption Monitoring System ')



with st.container():
    st.write("At Electricity Monitoring, we believe in the power of knowledge to drive positive change. Our mission is simple: to empower individuals and businesses to conserve energy, resources, and money through real-time monitoring of device power consumption.")

    st.write("In an era where energy conservation and sustainability have become paramount concerns, the need for effective monitoring and management of power consumption in domestic settings has never been greater. Domestic power consumption not only impacts household budgets but also plays a significant role in the overall energy footprint of a region. "  )
    
    image = Image.open('Images/mainpage.jpg')
    st.image(image, caption ="", use_column_width = True)

    st.write("To address this, modern technology has given rise to innovative solutions in the form of applications designed to monitor and optimize power consumption within homes.") 

   

st.write("Our Solution : " )
st.write("Our cutting-edge monitoring system provides you with the tools you need to take control of your energy usage. With intuitive dashboards and detailed analytics, you can track power consumption down to the device level, identify trends, and set targets for improvement. Whether you're a homeowner, a business owner, or a facility manager, our solution is tailored to meet your needs.")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

