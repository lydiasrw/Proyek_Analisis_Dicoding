import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import streamlit as st
from babel.numbers import format_currency
from PIL import GifImagePlugin, Image, ImageFile

sn.set(style="dark")


def create_month_order_df(df):
    month_order_df = df.resample(rule="M", on="order_purchase_timestamp").agg({
    "order_id" : "nunique",
    "price" : "sum"
    })
    month_order_df = month_order_df.reset_index()
    month_order_df.rename(columns={
        "order_id" : "count_id",
        "price" : "revenue"
        }, inplace=True)

    month_order_df= month_order_df.reset_index()

    return month_order_df

def create_sum_product_df(df):
    sum_product_df = df.groupby(by="product_category_name").agg({
        "freight_value" : "sum",
        "price" : "sum"
        })
    sum_product_df = sum_product_df.reset_index()
    sum_product_df.rename(columns={
            "freight_value" : "count",
            "price" : "income"
            }, inplace=True)

    return sum_product_df

def create_sum_seller_df(df):
    sum_seller_df = df.groupby(by="seller_city").price.sum().sort_values(ascending=False).reset_index()
   
    return sum_seller_df

def create_sum_customer_df(df):
    sum_customer_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()

    return sum_customer_df

# Load cleaned data

commerce_df = pd.read_csv("https://raw.githubusercontent.com/lydiasrw/Proyek_Analisis_Dicoding/main/dashboard/commerce_df.csv")

date_columns=["order_purchase_timestamp"]
commerce_df.sort_values(by="order_purchase_timestamp", inplace=True)
commerce_df.reset_index(inplace=True)

for columns in date_columns:
    commerce_df[columns] = pd.to_datetime(commerce_df[columns])

# Create widget for website

# Add widget to adorn website

# Filter data
min_date = commerce_df["order_purchase_timestamp"].min()
max_date = commerce_df["order_purchase_timestamp"].max()


with st.sidebar:

    # Add logo
    st.title("Welcome")
    st.image("https://github.com/lydiasrw/Proyek_Analisis_Dicoding/blob/main/dashboard/Dico.png")

    # Getting start date and end date from data input
    start_date, end_date = st.date_input(
    label = "Calendar", min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
    )

main_df = commerce_df[(commerce_df["order_purchase_timestamp"] >= str(start_date)) &
                    (commerce_df["order_purchase_timestamp"] <= str(end_date))]

# Prepare all DataFrame

month_order_df = create_month_order_df(main_df)
sum_product_df = create_sum_product_df(main_df)
sum_seller_df = create_sum_seller_df(main_df)
sum_customer_df = create_sum_customer_df(main_df)

# Add Element to streamlit

# Create Title

st.title("Hello Dicomers :sparkles:")


# Create a header

st.text("E-commerce Public Analysist in 2016-2018")

# Create Matrix for month order

st.write("""
# Month Order
Below month order of our product year by year.
""")

col1, col2 = st.columns(2)

with col1:
    total_orders = month_order_df.count_id.sum()
    st.metric("Total order", value=total_orders)

with col2:
    total_revenue = format_currency(month_order_df.revenue.sum(), "RUSD", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(
    month_order_df["order_purchase_timestamp"],
    month_order_df["count_id"],
    marker='o',
    linewidth=2,
    color="#818FB4"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

window = st.slider("Forecast Month")


# Create The Best Product in 2016-2017

st.subheader("The Best Dico Product")
st.text("Which one of The Most Selling Product in 2016-2018?")


color=["#776B5D", "#EBE3D5", "#EBE3D5", "#EBE3D5", "#EBE3D5"]
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45,40))
sn.barplot(x="count", 
           y="product_category_name", 
           data=sum_product_df.sort_values(by="count", ascending=False).head(5),
           palette=color,
           ax=ax[0])

ax[0].set_xlabel("Count", fontsize=40)
ax[0].set_ylabel("Product", fontsize=40)
ax[0].set_title("Number of Selling", fontsize=45)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30)

sn.barplot(x="income",
           y= "product_category_name",
           data=sum_product_df.sort_values(by="income", ascending=False).head(5),
           palette=color,
           ax=ax[1])

ax[1].set_xlabel("Income", fontsize=40)
ax[1].set_ylabel("Product", fontsize=40)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Total of Selling", fontsize=45)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30)


st.pyplot(fig)


# Create How much customer in the city

st.subheader("Top 5 Customer in The State")
st.text("Who The Best our customer in these State?")

fig, ax = plt.subplots(figsize=(10, 5))
color=["#94A684", "#E4E4D0", "#E4E4D0", "#E4E4D0", "#E4E4D0"]

sn.barplot(x="customer_state", 
           y="customer_id", 
           data=sum_customer_df.sort_values(by="customer_id", ascending=False).head(5), 
           palette=color,
           ax=ax)

ax.set_xlabel("State")
ax.set_ylabel("Customer Count")
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)


# Create how much seller in the city

st.subheader("Top 5 Sellers in The City")
st.text("Where the City that get much money?")

fig, ax = plt.subplots(figsize=(10, 5))
color=["#E9B824", "#F4BF96", "#F4BF96", "#F4BF96", "#F4BF96"]

sn.barplot(x="seller_city", 
           y="price", 
           data=sum_seller_df.head(5), 
           palette=color,
           ax=ax)

ax.set_xlabel("City")
ax.set_ylabel("Price")
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)




st.caption("Copyright @Dicomer 2023")


