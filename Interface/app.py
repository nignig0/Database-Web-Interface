import streamlit as st
import mysql.connector as sql
from queries import *
import pandas as pd

db_connection = sql.connect(host='127.0.0.1', database='projectdb', username='root', password= 'password', port = 3307)
db_cursor = db_connection.cursor()
live_table = None
live_table_title = ''

st.write("Health System Database Interface")

col1, col2, col3, col4 = st.columns(4)
if 'show_livetable' not in st.session_state:
    st.session_state.show_livetable = False

if 'live_table_title' not in st.session_state:
    st.session_state.live_table_title = ''

if 'hp_form' not in st.session_state:
    st.session_state.hp_form = False

if 'date_form' not in st.session_state:
    st.session_state.date_form = False

if 'student_form' not in st.session_state:
    st.session_state.student_form = False


with col1:
    with st.expander("Students"):
        df  = pd.DataFrame(getAllStudents(db_cursor))
        df.columns = ["StudentID", "FirstName", "LastName", "Email", "Phone Number"]
        st.dataframe(df)

with col2:
    with st.expander("Health Personnel"):
        df = pd.DataFrame(getAllHealthPersonnel(db_cursor))
        df.columns = ["Health Personnel ID", "FirstName", "LastName", "Email", "PhoneNumber"]
        st.dataframe(df)

with col3:
    with st.expander("Approved By"):
        df = pd.DataFrame(getApprovedBy(db_cursor))
        df.columns = ["RequestID", "Health Personnel ID", "Approved Time"]
        st.dataframe(df)

with col4:
    with st.expander("Health Requests"):
        df = pd.DataFrame(getAllRequests(db_cursor))
        df.columns = ["RequestID", "Symptoms", "Created at"]
        st.dataframe(df)


c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

with c1:
    if st.button("Get Requests from the last 30 days"):
        live_table = pd.DataFrame(getLast30DaysQueries(db_cursor))
        live_table_title = "Requsts from the last 30 days"
        live_table.columns = [
             "RequestID", "Status Name", "Symptoms", "Created at",
             "First Name", "Last Name", "Days Ago"
         ]
        st.session_state.show_livetable = True

with c2:
    if st.button("Students with multiple health requests"):
        live_table = pd.DataFrame(findStudentsMultipleHealthRequests(db_cursor))
        live_table.columns = [
            "First Name", "Last Name", "Email", "Phone Number",
            "Request ID", "Status" 
        ]
        live_table_title = "Students with multiple health requests"
        st.session_state.show_livetable = True

with c3:
    if st.button("Get Students with no requests"):
        live_table = pd.DataFrame(getStudentsNoRequests(db_cursor))
        live_table.columns = ["StudentID", "First Name", "Last Name", "Email"]
        live_table_title = "Students with no health requests"
        st.session_state.show_livetable = True

with c4:
    if st.button("Get Health Request and Student for each status"):
        live_table = pd.DataFrame(getHealthRequestAndStudentForEachStatus(db_cursor))
        live_table.columns = ['Status', 'First Name', 'Last Name', 'Student ID', 'Request Count']
        label_table_title = 'Health Reques and Student for each status'
        st.session_state.show_livetable = True

with c5: 
    if st.button("Number of Requests Approved by Health Personnel"):
        st.session_state.show_livetable = False
        st.session_state.hp_form = True

with c6: 
    if st.button("Number of Requests in a day"):
        st.session_state.show_livetable = False
        st.session_state.date_form = True

with c7: 
    if st.button("Get All Requests from a student"):
        st.session_state.show_livetable = False
        st.session_state.student_form = True


if st.session_state.student_form:
    with st.form(key='_student_form'):
        st.write("Enter the student first name")
        firstname = st.text_input('first name')
        lastname = st.text_input('last name')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            live_table = pd.DataFrame(getRequestFromStudent(db_cursor, firstname, lastname))
            live_table.columns = ['Name', "RequestID", 'Request Detail', 'Request Date']
            live_table_title = f'All Requests by {firstname} {lastname}'
            st.session_state.show_livetable = True
            st.session_state.student_form = False


if st.session_state.hp_form:
    with st.form(key='_hp_form'):
        st.write("Health Peronnel ID:")
        text_input = st.text_input('ID')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            
            live_table = pd.DataFrame(getNumberOfRequestsApprovedByHP(db_cursor, text_input))
            live_table.columns = ['Health Personnel', "Name", 'Approved Requests']
            live_table_title = f'Number of Requests Approved by {text_input}'
            st.session_state.show_livetable = True
            st.session_state.hp_form = False

if st.session_state.date_form:
    with st.form(key='_date_form'):
        st.write("Enter the date in the format yyyy-mm-dd")
        date_input = st.text_input('yyyy-mm-dd')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            
            live_table = pd.DataFrame(countRequestsInADay(db_cursor, date_input))
            live_table.columns = ['Request Date', "Request Count"]
            live_table_title = f'Number of Requests on {date_input}'
            st.session_state.show_livetable = True
            st.session_state.date_form = False

if st.session_state.show_livetable:
    st.write(live_table_title)
    st.dataframe(live_table)




