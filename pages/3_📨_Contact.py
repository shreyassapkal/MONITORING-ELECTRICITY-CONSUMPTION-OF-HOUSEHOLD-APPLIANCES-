import streamlit as st

st.title("📧 Contact Us")

with st.container():
    st.write('---')
    st.write("Please feel free to reach out to us using the contact form below.")
    st.write("##")

    contact_form = """
    <form action="b168846ea6881f1c63c26c42799b03e1" method="POST">
    <input type = "hidden", name ="_captcha", value="false">
        <input type="text" name="name", placeholder="Your name" required>
        <input type="email" name="email", placeholder="Your email" required>
        <textarea name = "message", placeholder="Your message"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")