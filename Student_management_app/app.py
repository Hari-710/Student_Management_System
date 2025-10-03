import pandas as pd
import streamlit as st
from datetime import date
import db
import datetime
import plotly.express as px

st.set_page_config("Student Management System", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.admin_mail = None
    st.session_state.admin_name = None

st.title("Welcome to Student Management App")

with st.sidebar:

    choice = st.sidebar.selectbox("Login Credentials",["Login","Register", "Logout"])

    if choice == "Login":
        email = st.text_input("E-Mail")
        password = st.text_input("Password", type="password")
        if st.button("Login", type="primary"):
            if db.login(email, password):
                st.session_state.logged_in = True
                st.session_state.admin_mail = email
                st.session_state.admin_name = db.fetch_adname(email)
                st.success(f"Welcome {st.session_state.admin_name}")
            else:
                st.warning("Invalid E-mail or Password")

    elif choice == "Register":
        name = st.text_input("Admin Name")
        email = st.text_input("E-Mail")
        password = st.text_input("Passord", type="password")

        if st.button("Register", type="primary"):
            if db.register(name, email, password):
                st.success("Registered Successfully! You can Login now..")
            else:
                st.error("Email already exists")
    
    elif choice == 'Logout':
        if st.button("Logout", type="primary"):
            st.session_state.logged_in = False
            st.session_state.admin_mail = None
            st.session_state.admin_name = None
            st.success("Logged out Successfully")
            st.rerun()


if st.session_state.logged_in:
    st.info(f"Logged in as {st.session_state.admin_name}")
    options = st.selectbox("Tasks",["Add Student", "View Student", "Edit/Delete Student", "View Analytics", "Select from Dropdown"],index=4)

    if options == "Add Student":
        st.write("Adding Student....")
        min_date = datetime.date(1900, 1, 1)
        max_date = datetime.date(2100, 12, 31)
        today = date.today()
        student_name = st.text_input("Student Name")
        gender = st.selectbox("Gender",["Male","Female"])
        admitted_date = st.date_input("Admitted Date", value=today)
        dob = st.date_input("DOB", min_value=min_date, max_value=max_date)
        dept_name = st.selectbox("Department", ["AI&DS","AI&ML","IT","Cyber","CSE","ECE","EEE","FT","BT","BME","Mech","Agri"])
        grade_10_mark = st.number_input("10th mark")
        grade_12_mark = st.number_input("12th mark")
        phone_number = st.text_input("Phone Number")
        native = st.text_input("Native Place")
        counselling_or_not = st.selectbox("Counselling/Management",["Counselling","Management"])
        hosteller_or_not = st.selectbox("Hostel/Not",["Yes","No"])
        if st.button("Add Student", type="primary"):
            if db.add_student(student_name, gender, admitted_date, dob, dept_name, grade_10_mark, grade_12_mark, phone_number, native, counselling_or_not, hosteller_or_not):
                st.success("Student added successfully")
            else:
                st.warning("Check Student Phone Number its already exists..")

    elif options == 'View Student':
        st.write("Viewing Students Details....")
        view = st.selectbox("Choose",['View one student','View all students'])
        if view == 'View one student':
            st.write("Search Student")
            res = db.view_student()
            if res:
                student_dict = {s['Student_Name']: s["Student_Id"] for s in res}
                selected_student = st.selectbox("Select a Student", list(student_dict.keys()))

                if st.button("View Student", type="primary"):
                    if selected_student:
                        student_id = student_dict[selected_student]

                        student_data = db.fetch_student(student_id)

                        if student_id:
                            df = pd.DataFrame([student_data], columns=['Student_ID','Student_Name', "Gender", 'Student_Admitted_Date', 'dob', 'Department_Name', 'Grade_10_Mark', 'Grade_12_Mark', 'Phone_Number', 'Native_Place', 'counselling_or_management', 'Hosteller_or_Not'])
                            st.dataframe(df)
                        else:
                            st.warning("No record found for this student")
            else:
                st.warning("No Students available")

        else:
            if st.button("View Students", type="primary"):
                res = db.view_students()
                if res:
                    df1 = pd.DataFrame(res, columns=['Student_ID','Student_Name', 'Gender', 'Student_Admitted_Date', 'dob', 'Department_Name', 'Grade_10_Mark', 'Grade_12_Mark', 'Phone_Number', 'Native_Place', 'counselling_or_management', 'Hosteller_or_Not'])
                    st.dataframe(df1)
                else:
                    st.info("No Students added yet....")

    elif options == 'Edit/Delete Student':
        st.write("Edit or Delete Student")

        stud = db.view_students()
        students = pd.DataFrame(stud, columns=['Student_ID','Student_Name', 'Gender', 'Student_Admitted_Date', 'dob', 'Department_Name', 'Grade_10_Mark', 'Grade_12_Mark', 'Phone_Number', 'Native_Place', 'counselling_or_management', 'Hosteller_or_Not'])
        if not students.empty:
            stud_names = students['Student_Name'].tolist()
            selected_name = st.selectbox("Select Student", stud_names)

            student_data = students[students['Student_Name'] == selected_name].iloc[0]

            with st.form("edit_student_form"):
                new_name = st.text_input("Name", value=student_data['Student_Name'])
                gender = st.selectbox("Gender",["Male","Female"],index=["Male","Female"].index(student_data['Gender']))
                admitted_date = st.date_input("Admitted Date", value=pd.to_datetime(student_data['Student_Admitted_Date']))
                dob = st.date_input("Date of Birth", value=pd.to_datetime(student_data['dob']))
                dept_options = ["AI&DS","AI&ML","IT","Cyber","CSE","ECE","EEE","FT","BT","BME","Mech","Agri"]
                dept_name = st.selectbox("Department", dept_options,
                                        index=dept_options.index(student_data['Department_Name']))
                grade_10 = st.number_input("10th Mark", value=int(student_data['Grade_10_Mark']))
                grade_12 = st.number_input("12th Mark", value=int(student_data['Grade_12_Mark']))
                phone_number = st.text_input("phone number", value=student_data['Phone_Number'])
                native = st.text_input("Native", value=student_data['Native_Place'])
                counselling_or_not = st.selectbox("Counselling/Not",["Counselling","Management"],index=["Counselling","Management"].index(student_data['counselling_or_management']))
                hostel = st.selectbox("Hostel", ["Yes","No"], index=0 if student_data['Hosteller_or_Not']=="Yes" else 1)

                update_btn = st.form_submit_button("Update Student")
                delete_btn = st.form_submit_button("Delete Student")

            if update_btn:
                db.update_student(student_data['Student_ID'],new_name, gender, admitted_date, dob, dept_name, grade_10, grade_12, phone_number, native, counselling_or_not, hostel)
                st.success(f"{new_name} updated Successfully")
            
            if delete_btn:
                st.error(f"Are you sure you want to delete {student_data['Student_Name']}?")
                confirm = st.button("Confirm Delete", type="primary")
                if confirm:
                    db.delete_student(student_data['Student_ID'])
                    st.success(f"{student_data['Student_Name']} deleted successfully!")
                    st.rerun()

        else:
            st.info("No students available to edit or delete")

    elif options == 'View Analytics':
        st.subheader("Analytics Dashboard")

        data = db.view_students()
        stud = pd.DataFrame(data, columns=['Student_ID','Student_Name', 'Gender', 'Student_Admitted_Date', 'dob', 'Department_Name', 'Grade_10_Mark', 'Grade_12_Mark', 'Phone_Number', 'Native_Place', 'counselling_or_management', 'Hosteller_or_Not'])

        if not stud.empty:
            dept_list = ["All"] + stud['Department_Name'].unique().tolist()
            selected_dept = st.multiselect("Filter by Department", stud['Department_Name'].unique(),default=stud['Department_Name'].unique())
            
            stud['Year'] = pd.to_datetime(stud['Student_Admitted_Date']).dt.year
            year_list = ["All"] + sorted(stud['Year'].unique().tolist())
            selected_year = st.selectbox("Filter by Year", year_list)


            if selected_dept != "All":
                stud = stud[stud["Department_Name"].isin(selected_dept)]

            if selected_year != "All":
                stud = stud[stud['Year'] == selected_year]

            total = len(stud)
            hostellers = (stud['Hosteller_or_Not'] == 'Yes').sum()
            scholars = total - hostellers
            avg10 = stud['Grade_10_Mark'].mean()
            avg12 = stud['Grade_12_Mark'].mean()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Students", total)
            col2.metric("Hostellers %", f"{(hostellers/total)*100:.1f}%")
            col3.metric("Avg 10th Mark", f"{avg10:.1f}" if total > 0 else "N/A")
            col4.metric("Avg 12th Mark", f"{avg12:.1f}" if total > 0 else "N/A")

            tab1, tab2, tab3, tab4 = st.tabs(["Admissions by Department", "Hostellers vs Day scholars", "Admission Trend Over Time", "Top 3 Departments"])

            with tab1:
                st.plotly_chart(px.bar(stud, x="Department_Name", title="Admissions by Department"), use_container_width=True)

            with tab2:
                st.plotly_chart(px.pie(stud, names="Hosteller_or_Not", title="Hostellers vs Day scholars"), use_container_width=True)

            with tab3:
                stud['Student_Admitted_Date'] = pd.to_datetime(stud['Student_Admitted_Date'])
                adm_trend = stud.groupby(stud['Student_Admitted_Date'].dt.to_period("M")).size().reset_index()
                adm_trend['Student_Admitted_Date'] = adm_trend['Student_Admitted_Date'].dt.to_timestamp()
                st.plotly_chart(px.line(adm_trend, x="Student_Admitted_Date", y=0, title="Admission Over Time"), use_container_width=True)

            with tab4:
                top_depts = stud['Department_Name'].value_counts().head(3).reset_index()
                st.table(top_depts.rename(columns={'index': 'Department', 'Department_Name': 'Admissions'}))
                
            with st.sidebar:
                st.divider()
                st.subheader("Click below to download report...")
                csv = stud.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV Report",
                    data=csv,
                    file_name=f"Students report of {st.session_state.admin_name}",
                    mime="text/csv",
                    type="primary"
                )
                
        else:
            st.info("No Student data available for analytics.")

