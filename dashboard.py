import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from babel.numbers import format_currency

sns.set(style="dark")


def bulanan_df(df):
    # Resampling and Aggregation the dataFrame based on order_date ('D' indicates day)
    monthly_orders_df = df.resample(rule="D", on="order_purchase_date").agg(
        {
            "order_id": "nunique",  # Count the number of unique order IDs per day
            "payment_value": "sum",  # Sum the total price of orders per day
        }
    )
    # resetting index
    monthly_orders_df = monthly_orders_df.reset_index()
    # rename the column
    monthly_orders_df.rename(
        columns={
            "order_id": "order_count",
            "payment_value": "sales",
        },
        inplace=True,
    )

    return monthly_orders_df


path = os.path.dirname(os.path.abspath(__file__))
data_source = path + "/all_data.csv"
all_data = pd.read_csv(data_source)


def intro():
    import streamlit as st

    st.write("# Brazilian E-Commerce Public Analysis! 🔎")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        ### About dataset
        Dataset ini berisi informasi tentang 100.000 pesanan dari tahun 2016 hingga 2018 yang dilakukan di beberapa pasar di Brasil.
        untuk kali ini hanya 5 data yang akan digunakan. 
        - customers_dataset.csv ✔️  
        - order_items_dataset.csv ✔️ 
        - orders_dataset.csv ✔️ 
        - product_category_name_translation.csv ✔️ 
        - products_dataset.csv ✔️  
        ### Task 
        untuk project ini saya akan menampilkan :
        1. Apa jenis produk yang paling diminati atau sering dibeli?
        2. Bagaimana kinerja penjualan dan pendapatan perusahaan dalam beberapa bulan terakhir? Apakah ada tren penjualan yang signifikan atau perubahan pendapatan yang mencolok dalam rentang waktu tersebut?
        """
    )


def pertanyaan_2():
    print("pertanyaan 2 mulai\n")

    st.markdown(f"# {list(page_connector_with_funcs.keys())[2]}")
    st.title("Brazilian E-Commerce Public :sparkles:")
    st.header("", divider="rainbow")
    st.subheader("Data penjualan bulanan dari tahun 2017-2018")

    waktu = [
        "order_purchase_timestamp",
        "order_purchase_date",
        "order_estimated_delivery_date",
        "order_delivered_date",
    ]
    all_data.sort_values(by="order_purchase_date", inplace=True)
    all_data.reset_index(inplace=True)
    for count in waktu:
        all_data[count] = pd.to_datetime(all_data[count])

    data_minimal = all_data["order_purchase_date"].min()
    data_maksimal = all_data["order_purchase_date"].max()

    group_columns = ["order_date_year", "order_date_month", "month-year"]
    pendapatan_tahunan_bulanan = (
        all_data.groupby(group_columns)["order_id"].nunique().reset_index()
    )

    pendapatan__2017_tahunan_bulanan = pendapatan_tahunan_bulanan[
        pendapatan_tahunan_bulanan["order_date_year"] == 2017
    ]
    pendapatan_2018_tahunan_bulanan = pendapatan_tahunan_bulanan[
        pendapatan_tahunan_bulanan["order_date_year"] == 2018
    ]

    pendapatan__2017_tahunan_bulanan.rename(
        columns={
            "order_id": "total_order",
            "order_date_month": "month",
        },
        inplace=True,
    )

    pendapatan_2018_tahunan_bulanan.rename(
        columns={
            "order_id": "total_order",
            "order_date_month": "month",
        },
        inplace=True,
    )

    with st.sidebar:
        start_date, end_date = st.date_input(
            label="Date Range",
            min_value=data_minimal,
            max_value=data_maksimal,
            value=[data_minimal, data_maksimal],
        )

    main_df = all_data[
        (all_data["order_purchase_date"] >= str(start_date))
        & (all_data["order_purchase_date"] <= str(end_date))
    ]

    monthly_orders_df = bulanan_df(main_df)

    col1_left, col2_right = st.columns(2)

    with col1_left:
        total_orders = monthly_orders_df.order_count.sum()
        st.metric("Total Penjualan", value=total_orders)

    st.markdown("")
    col1_line_chart, col2_line_chart = st.columns(2)

    with col1_line_chart:
        colors = ["#D3D3D3"]
        st.write("##### Total Penjualan di 2017")
        st.line_chart(
            pendapatan__2017_tahunan_bulanan, x="month", y="total_order", color=colors
        )

    with col2_line_chart:
        colors = ["#90CAF9"]
        st.write("##### Total Penjualan di 2018")
        st.line_chart(
            pendapatan_2018_tahunan_bulanan, x="month", y="total_order", color=colors
        )
    st.markdown("Analysis summary:")
    st.markdown(
        "- berdasarkan data serta chart yang terlihat, jumlah total pesanan pada tahun 2018 mengalami penurunan yang cukup signifikan namun masih tetap ada kenaikan yang signifikan juga di penghujung tahun.Total pesanan terendah terjadi pada bulan Juni dan kenaikan tertinggi terjadi pada bulan januari. Untuk jumlah total pesanan pada tahun 2017 mengalami meningkatan walaupun sempat mengalami penurunan namun peningkatannya tetap konsisten dan signifikan.Total pesanan terendah terjadi pada bulan Januari dan kenaikan tertinggi terjadi pada bulan november."
    )
    st.markdown("")


def pertanyaan_1():
    print("pertanyaan 1 mulai\n")

    st.markdown(f"# {list(page_connector_with_funcs.keys())[1]}")
    st.title("Brazilian E-Commerce Public :sparkles:")
    st.header("", divider="rainbow")
    st.subheader("Top 7 kategori Produk")

    # product_join_item = products_df.merge(items_df, on='product_id', how='inner')

    top_kategori = all_data["product_category_name"].value_counts().head(7)
    kategori = all_data.sort_values("product_category_name").head(7)

    st.markdown("")

    col1_bar_chart, col2_line_chart = st.columns(2)

    colors = ["#D3D3D3"]
    st.bar_chart(top_kategori)

    st.markdown("Analysis summary:")
    st.markdown(
        "- 7 kategori produk paling sering di beli adalah cama_mesa_banho lalu kedua yaitu beleza_saude, ketiga yaitu esporte_lazer, selanjutnya yaitu moveis_decoracao, serta informatica_acessorios, utilidades_domesticas, dan terakhir relogios_presentes."
    )
    st.markdown("")


page_connector_with_funcs = {
    "awalan": intro,
    "pertanyaan 1": pertanyaan_1,
    "pertanyaan 2": pertanyaan_2,
}
demo_name = st.sidebar.selectbox("silahkan pilih", page_connector_with_funcs.keys())
page_connector_with_funcs[demo_name]()


st.caption("Copyright (c) - Created by mfajarjati - 2023")
