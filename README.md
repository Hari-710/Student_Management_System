# 🎓 Student Admission Analytics Dashboard

This project is a **Streamlit + MySQL + Plotly/Matplotlib** based dashboard for analyzing student admissions across departments. It provides administrators with interactive visualizations for student demographics, academic performance, and department-wise analytics.

---

## 🚀 Features

* 🔑 **Admin Login** (MySQL authentication)
* 📊 **Interactive Dashboard** built with Streamlit
* 🏫 **Department & Year Filters** for dynamic insights
* 📈 **Key Metrics**:

  * % of Hostellers vs Day Scholars
  * Average 10th & 12th Marks
  * Top 3 Departments by Admissions
* 📅 **Year-wise Admission Trends**
* ⚡ **Real-time Data** fetched directly from MySQL
* 🔒 **Secure Credentials** – original `db.py` is excluded from Git, `db_example.py` provided for reference

---

## 🗂️ Project Structure

```
student_admission_dashboard/
│── app.py              # Main Streamlit app
│── db.py               # Your local database connection (ignored in Git)
│── db_example.py       # Template with example DB credentials for users
│── dashboard.py        # Dashboard plots & KPIs
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
```

> **Note:** Rename `db_example.py` to `db.py` and update your MySQL credentials before running the app.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/student-admission-dashboard.git
cd student-admission-dashboard
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac

pip install -r requirements.txt
```

### 3. Configure Database Credentials

1. Open `db_example.py`.
2. Update `user`, `password`, `host`, and `database` with your own MySQL credentials.
3. Save the file as `db.py` in the same directory.

```python
# db.py (example)
user = 'root'
password = 'yourpassword'
host = 'localhost'
database = 'studentdb'
```

> ⚠️ **Do not commit** `db.py` to Git. It contains sensitive credentials.

### 4. Set Up Database & Tables

```sql
-- Create Database
CREATE DATABASE IF NOT EXISTS 'Your DB Name';

USE 'Your DB Name';

-- Create Admin Table
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name varchar(20),
    email varchar(50) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Create Students Table
CREATE TABLE students (
    Student_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_Name VARCHAR(100),
    Gender Varchar(7),
    Student_Admitted_Date DATE,
    dob date,
    Department_Name VARCHAR(100),
    Grade_10_Mark DECIMAL(5,2),
    Grade_12_Mark DECIMAL(5,2),
    Phone_Number varchar(10),
    Native_Place VARCHAR(100),
    counselling_or_management varchar(20),
    Hosteller_or_Not VARCHAR(10)
);

```

### 5. Run the Application

```bash
streamlit run app.py
```

---


## 🛠️ Tech Stack

* **Frontend/UI** → Streamlit
* **Database** → MySQL
* **Visualization** → Plotly, Matplotlib
* **Authentication** → MySQL user records
* **Deployment Ready** → Streamlit Cloud / Heroku

---

## 🔮 Future Improvements

* ✅ Role-based access (Admin, Staff)
* ✅ Advanced analytics (student performance prediction with ML)
* ✅ Power BI / Tableau integration
* ✅ Automated daily refresh

---

## 👨‍💻 Author

**Harish J**
📌 Data Analyst Aspirant | Final Year Data Science Student

---

✨ With this project, administrators can **monitor admissions in real-time, identify trends, and make data-driven decisions**.
