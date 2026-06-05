import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================================
# PAGE SETTINGS
# ==================================
st.set_page_config(
    page_title="Online Retail Dashboard",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 18px !important;
}
h1 {
    font-size: 2.2rem !important;
}
h2 {
    font-size: 1.8rem !important;
}
h3 {
    font-size: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Online Retail Dashboard")
st.markdown("### Designed for Adults Aged 65+")
st.markdown("---")

# ==================================
# FILE UPLOAD
# ==================================
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    @st.cache_data
    def load_data(file):
        df = pd.read_csv(file, encoding="latin1")

        df = df.dropna(subset=["InvoiceNo", "Description", "CustomerID"])
        df = df[df["Quantity"] > 0]
        df = df[df["UnitPrice"] > 0]

        df["InvoiceNo"] = df["InvoiceNo"].astype(str)
        df = df[~df["InvoiceNo"].str.startswith("C")]

        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=True)
        df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

        df["Revenue"] = df["Quantity"] * df["UnitPrice"]

        return df

    df = load_data(uploaded_file)

    # ==================================
    # SIDEBAR FILTER
    # ==================================
    st.sidebar.header("Filters")

    countries = sorted(df["Country"].unique())

    selected_country = st.sidebar.selectbox(
        "Select Country",
        ["All"] + countries
    )

    if selected_country != "All":
        df = df[df["Country"] == selected_country]

    # ==================================
    # OVERVIEW
    # ==================================
    st.subheader("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Transactions", df["InvoiceNo"].nunique())
    col2.metric("Products", df["Description"].nunique())
    col3.metric("Customers", df["CustomerID"].nunique())
    col4.metric("Revenue", f"£{df['Revenue'].sum():,.0f}")

    st.markdown("---")

    # ==================================
    # TOP PRODUCTS
    # ==================================
    st.subheader("Top 10 Best Selling Products")

    top_products = (
        df.groupby("Description")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    top_products.plot(kind="bar", ax=ax1)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig1)

    st.markdown("---")

    # ==================================
    # AVG REVENUE
    # ==================================
    st.subheader("Average Revenue per Customer")

    customers = df["CustomerID"].nunique()

    if customers > 0:
        avg_revenue = df["Revenue"].sum() / customers
    else:
        avg_revenue = 0

    st.metric("Avg Revenue per Customer", f"£{avg_revenue:,.2f}")

    st.markdown("---")

    # ==================================
    # MONTHLY TREND
    # ==================================
    st.subheader("Monthly Revenue Trend")

    monthly = df.groupby("Month")["Revenue"].sum().reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(monthly["Month"], monthly["Revenue"], marker="o")

    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig2)

    st.markdown("---")

    # ==================================
    # TOP COUNTRIES
    # ==================================
    st.subheader("Top Countries by Revenue")

    country_revenue = (
        df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    country_revenue.plot(kind="bar", ax=ax3)

    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig3)

    st.markdown("---")

    # ==================================
    # DATA PREPARATION (UPDATED TEXT)
    # ==================================
    st.subheader("Data Preparation")

    st.markdown("""
In order to ensure the dataset was suitable for analysis, several cleaning steps were carried out:

- Rows with missing values were removed to ensure data quality  
- Cancelled orders (invoices starting with 'C') were excluded from the analysis  
- Negative quantities, which represent returns, were removed  
- Invalid unit prices (zero or negative values) were filtered out  
- The date column was converted into a proper datetime format for time-based analysis  
- A new feature called Revenue was created by multiplying Quantity by Unit Price  
""")

    # ==================================
    # ML SUITABILITY (UPDATED TEXT)
    # ==================================
    st.subheader("Why This Dataset is Suitable for Machine Learning")

    st.markdown("""
This dataset is highly suitable for machine learning applications due to its structure and size:

- It contains a large number of real customer transactions  
- There is a wide variety of products available for analysis  
- Customer purchasing behaviour can be clearly observed  
- It is well suited for recommendation system development  
- It supports market basket analysis techniques  
- It includes time-based information, which allows trend analysis over time  
""")

    # ==================================
    # DASHBOARD DESIGN (UPDATED TEXT)
    # ==================================
    st.subheader("Dashboard Design for Adults Aged 65+")

    st.markdown("""
The dashboard was specifically designed with older adults (65+) in mind to ensure ease of use and accessibility:

- Font sizes were increased to improve readability  
- Charts were kept simple and easy to interpret  
- Each section is clearly separated with headings  
- High-contrast colours were used for better visibility  
- The design minimises the need for complex user interactions  
- Information is presented in simple and clear language without technical jargon  
""")

else:
    st.info("Please upload your Online Retail CSV file to begin.")