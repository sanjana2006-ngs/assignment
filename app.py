import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Visualization App", layout="wide")

st.title("📊 Data Visualization App")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Dataset")
    st.dataframe(df.head())

    # Select visualization type
    vis_type = st.selectbox(
        "Choose a visualization type",
        ["Scatter Plot", "Line Plot", "Bar Plot", "Histogram", "Box Plot", "Heatmap", "Pairplot"]
    )

    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    all_columns = df.columns.tolist()

    if vis_type == "Scatter Plot":
        x = st.selectbox("X-Axis", options=numeric_columns)
        y = st.selectbox("Y-Axis", options=numeric_columns)
        color = st.selectbox("Color (Optional)", options=[None] + all_columns)
        fig = px.scatter(df, x=x, y=y, color=color)
        st.plotly_chart(fig, use_container_width=True)

    elif vis_type == "Line Plot":
        x = st.selectbox("X-Axis", options=all_columns)
        y = st.selectbox("Y-Axis", options=numeric_columns)
        fig = px.line(df, x=x, y=y)
        st.plotly_chart(fig, use_container_width=True)

    elif vis_type == "Bar Plot":
        x = st.selectbox("X-Axis", options=all_columns)
        y = st.selectbox("Y-Axis", options=numeric_columns)
        fig = px.bar(df, x=x, y=y)
        st.plotly_chart(fig, use_container_width=True)

    elif vis_type == "Histogram":
        col = st.selectbox("Select Column", options=numeric_columns)
        fig = px.histogram(df, x=col)
        st.plotly_chart(fig, use_container_width=True)

    elif vis_type == "Box Plot":
        x = st.selectbox("X-Axis (Optional)", options=[None] + all_columns)
        y = st.selectbox("Y-Axis", options=numeric_columns)
        fig = px.box(df, x=x, y=y)
        st.plotly_chart(fig, use_container_width=True)

    elif vis_type == "Heatmap":
        st.subheader("Correlation Heatmap")
        corr = df.corr(numeric_only=True)
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    elif vis_type == "Pairplot":
        st.subheader("Seaborn Pairplot")
        selected_cols = st.multiselect("Select columns", options=numeric_columns, default=numeric_columns[:3])
        if len(selected_cols) >= 2:
            fig = sns.pairplot(df[selected_cols])
            st.pyplot(fig)
        else:
            st.warning("Please select at least two numeric columns.")
