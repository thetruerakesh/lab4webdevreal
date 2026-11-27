import streamlit as st

# Title of App
st.title("ProstheticsMatch")

# Assignment Data
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 53, Web Development - Section A")
st.subheader("Ashutosh Barde, Ansh Mithani")

# TODO (optional): Add a group photo to the images folder and show it here, for example:
# st.image("images/group_photo.jpg")


# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description

st.write("""
Welcome to ProstheticMatch! You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Data Page**: Lets you filter FDA-classified prosthetic device categories by medical specialty or keyword, view regulatory class breakdowns, and inspect registered GUDID products by manufacturer.
2. **Chatbot**: A biomedical engineering assistant that answers general questions about prosthetic technologies—such as mechanical, body-powered, myoelectric, and microprocessor-controlled prosthetics—without looking up external data.
3. **Agent**: An AI assistant that looks up real prosthetic device and classification data from external sources to answer specific questions.
""")
