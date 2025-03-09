!pip install streamlit plotly

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px  # For interactive charts

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("/content/university_student_dashboard_data.csv")
    return df

df = load_data()

# Sidebar Filters with Sliders
st.sidebar.header("🎛️ Filters")
year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), 
                               (int(df['Year'].min()), int(df['Year'].max())))

selected_term = st.sidebar.selectbox("Select Term", ['All'] + sorted(df['Term'].unique()))

# Apply Filters
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

if selected_term != 'All':
    filtered_df = filtered_df[filtered_df['Term'] == selected_term]

# KPIs with Vibrant Colors
st.title("🚀 University Student Analytics Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("📌 Total Applications", f"{filtered_df['Applications'].sum():,}", delta=None)
col2.metric("🎓 Total Admissions", f"{filtered_df['Admitted'].sum():,}", delta=None)
col3.metric("📝 Total Enrollments", f"{filtered_df['Enrolled'].sum():,}", delta=None)

# Enrollment Breakdown by Department (Interactive)
st.subheader("📌 Enrollment Breakdown by Department")
department_enrollment = filtered_df[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].sum()
fig_dept = px.bar(department_enrollment, 
             x=department_enrollment.index, 
             y=department_enrollment.values, 
             labels={'x': "Department", 'y': "Total Enrollments"},
             color=department_enrollment.index,
             title="Enrollment by Department",
             text_auto=True)
st.plotly_chart(fig_dept)

# Retention Rate Over Time (Interactive)
st.subheader("📈 Retention Rate Over Time")
fig_retention = px.line(filtered_df.groupby('Year')['Retention Rate (%)'].mean().reset_index(), 
              x="Year", 
              y="Retention Rate (%)",
              markers=True,
              title="Retention Rate Over the Years",
              hover_name="Year")
st.plotly_chart(fig_retention)

# Student Satisfaction Over Years (Interactive)
st.subheader("😊 Student Satisfaction Scores Over Years")
fig_satisfaction = px.line(filtered_df.groupby('Year')['Student Satisfaction (%)'].mean().reset_index(), 
              x="Year", 
              y="Student Satisfaction (%)",
              markers=True,
              title="Student Satisfaction Trend",
              hover_name="Year",
              color_discrete_sequence=["orange"])
st.plotly_chart(fig_satisfaction)

# Comparison of Spring vs Fall Enrollment (Interactive)
st.subheader("🌱📚 Comparison: Spring vs Fall Enrollment")
seasonal_enrollment = filtered_df.groupby('Term')['Enrolled'].sum().reset_index()
fig_season = px.bar(seasonal_enrollment, 
             x='Term', 
             y='Enrolled', 
             title="Spring vs. Fall Enrollment",
             color='Term', 
             text_auto=True)
st.plotly_chart(fig_season)

# Department Trends Over Time (Interactive)
st.subheader("📊 Trends Across Departments Over Time")
department_trends = filtered_df.pivot_table(index="Year", 
                                            values=['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled'], 
                                            aggfunc="sum").reset_index()
fig_dept_trend = px.line(department_trends, 
              x="Year", 
              y=['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled'],
              title="Department Enrollment Trends Over Time",
              markers=True)
st.plotly_chart(fig_dept_trend)

# Display Filtered Data Table
st.subheader("📋 Student Enrollment Data")
st.dataframe(filtered_df)
