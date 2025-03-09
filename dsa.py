#!pip install streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("/content/university_student_dashboard_data.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
selected_term = st.sidebar.selectbox("Select Term", ['All'] + sorted(df['Term'].unique()))

if selected_term != 'All':
    df = df[df['Term'] == selected_term]

# KPIs
st.title("📊 University Student Analytics Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", f"{df['Applications'].sum():,}")
col2.metric("Total Admissions", f"{df['Admitted'].sum():,}")
col3.metric("Total Enrollments", f"{df['Enrolled'].sum():,}")

# Enrollment Breakdown by Department
st.subheader("📌 Enrollment Breakdown by Department")
department_enrollment = df[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].sum()

fig, ax = plt.subplots()
department_enrollment.plot(kind='bar', ax=ax, color=['blue', 'green', 'red', 'purple'])
ax.set_ylabel("Total Enrollments")
ax.set_title("Enrollment by Department")
st.pyplot(fig)

# Retention Rate Over Time
st.subheader("📈 Retention Rate Over Time")
fig, ax = plt.subplots()
df.groupby('Year')['Retention Rate (%)'].mean().plot(ax=ax, marker='o', linestyle='-', color='blue')
ax.set_ylabel("Retention Rate (%)")
ax.set_title("Retention Rate Over the Years")
st.pyplot(fig)

# Student Satisfaction Over Years
st.subheader("😊 Student Satisfaction Scores Over Years")
fig, ax = plt.subplots()
df.groupby('Year')['Student Satisfaction (%)'].mean().plot(ax=ax, marker='s', linestyle='-', color='orange')
ax.set_ylabel("Satisfaction Score (%)")
ax.set_title("Student Satisfaction Trend")
st.pyplot(fig)

# Comparison of Spring vs Fall Enrollment
st.subheader("🌱📚 Comparison: Spring vs Fall Enrollment")
seasonal_enrollment = df.groupby('Term')['Enrolled'].sum()

fig, ax = plt.subplots()
seasonal_enrollment.plot(kind='bar', ax=ax, color=['skyblue', 'salmon'])
ax.set_ylabel("Total Enrolled Students")
ax.set_title("Spring vs. Fall Enrollment")
st.pyplot(fig)

# Department Trends Over Time
st.subheader("📊 Trends Across Departments Over Time")
department_trends = df.pivot_table(index="Year", values=['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled'], aggfunc="sum")

fig, ax = plt.subplots()
department_trends.plot(ax=ax, marker='o')
ax.set_ylabel("Number of Enrollments")
ax.set_title("Department Enrollment Trends Over Time")
st.pyplot(fig)

# Display Data Table
st.subheader("📋 Student Enrollment Data")
st.dataframe(df)
