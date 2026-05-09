import streamlit as st
# LOGIN ADMIN
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username != "admin" or password != "123":
    st.warning("Login dulu")
    st.stop()
import pandas as pd
from datetime import datetime, timedelta
import os
import qrcode
from PIL import Image

# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="SHIFA FLORIST",
    layout="wide"
)

# =====================================
# FILE CSV
# =====================================
FILE_NAME = "transaksi.csv"

if not os.path.exists(FILE_NAME):
    df_init = pd.DataFrame(columns=[
        "Tanggal",
        "Produk",
        "Qty",
        "Harga",
        "Subtotal",
        "Catatan",
        "Pembayaran",
        "Kembalian"
    ])
    df_init.to_csv(FILE_NAME, index=False)

# =====================================
# SESSION STATE
# =====================================
if "cart" not in st.session_state:
    st.session_state.cart = []

# =====================================
# DATA BUNGA
# =====================================
flowers = [
    {
        "nama": "Mawar",
        "harga": 10000,
        "stok": 20,
        "gambar": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7"
    },

    {
        "nama": "Lily",
        "harga": 100000,
        "stok": 15,
        "gambar": "https://images.unsplash.com/photo-1490750967868-88aa4486c946"
    }
]

# =====================================
# MENU
# =====================================
menu = st.sidebar.radio(
    "Menu",
    ["Kasir", "Keuangan"]
)

# =====================================
# HALAMAN KASIR
# =====================================
if menu == "Kasir":

    st.title("🌸 SHIFA FLORIST")

    st.subheader("Daftar Bunga")

    cols = st.columns(4)

    for i, flower in enumerate(flowers):

        with cols[i]:

            st.image(flower["gambar"], use_container_width=True)

            st.markdown(f"### {flower['nama']}")
            st.write(f"Harga : Rp {flower['harga']:,}")
            st.write(f"Stok : {flower['stok']}")

            qty = st.number_input(
                f"Qty {flower['nama']}",
                min_value=1,
                step=1,
                key=f"qty{i}"
            )

            if st.button(f"Tambah {flower['nama']}", key=f"btn{i}"):

                st.session_state.cart.append({
                    "Produk": flower["nama"],
                    "Qty": qty,
                    "Harga": flower["harga"],
                    "Subtotal": qty * flower["harga"]
                })

                st.success("Berhasil ditambahkan")

    # =====================================
    # CUSTOM BUNGA
    # =====================================
    st.divider()

    st.subheader("💐 Custom Bouquet")

    custom_nama = st.text_input("Nama Bouquet")

    custom_harga = st.number_input(
        "Harga Bouquet",
        min_value=0
    )

    custom_qty = st.number_input(
        "Jumlah Bouquet",
        min_value=1,
        step=1
    )

    if st.button("Tambah Custom Bouquet"):

        st.session_state.cart.append({
            "Produk": custom_nama,
            "Qty": custom_qty,
            "Harga": custom_harga,
            "Subtotal": custom_qty * custom_harga
        })

        st.success("Custom bouquet ditambahkan")

    # =====================================
    # KERANJANG
    # =====================================
    st.divider()

    st.subheader("🛒 Keranjang")

    if len(st.session_state.cart) > 0:

        df_cart = pd.DataFrame(st.session_state.cart)

        st.dataframe(df_cart, use_container_width=True)

        total = df_cart["Subtotal"].sum()

        st.markdown(f"## Total : Rp {total:,}")

        # =====================================
        # CATATAN
        # =====================================
        catatan = st.text_area("Catatan Pembelian")

        # =====================================
        # PEMBAYARAN
        # =====================================
        pembayaran = st.number_input(
            "Uang Masuk",
            min_value=0
        )

        if pembayaran >= total:

            kembalian = pembayaran - total

            st.success("Pembayaran Berhasil")

            st.write(f"Kembalian : Rp {kembalian:,}")

                      # =====================================
            # QRIS PEMBAYARAN
            # =====================================

            st.subheader("📱 QRIS Pembayaran")

            qris_text = f"""
            SHIFA FLORIST
            Total Bayar Rp {total}
            """

            qr = qrcode.make(qris_text)

            qr.save("qris.png")

            st.image("qris.png", width=250)

            # =====================================
            # CETAK STRUK
            # =====================================

            st.subheader("🧾 Struk Pembelian")

            struk = f'''
=========================
     FLORIST SHOP
=========================

Tanggal :
{datetime.now().strftime("%d-%m-%Y %H:%M")}
'''

            for item in st.session_state.cart:

                struk += f'''
{item['Produk']}
{item['Qty']} x Rp {item['Harga']:,}
= Rp {item['Subtotal']:,}
'''

            struk += f'''

-------------------------
TOTAL : Rp {total:,}
BAYAR : Rp {pembayaran:,}
KEMBALI : Rp {kembalian:,}

Catatan :
{catatan}

Terima Kasih
'''

            st.text(struk)

            # =====================================
            # SIMPAN TRANSAKSI
            # =====================================
            if st.button("Simpan Transaksi"):

                data_baru = []

                for item in st.session_state.cart:

                    data_baru.append({
                        "Tanggal": datetime.now(),
                        "Produk": item["Produk"],
                        "Qty": item["Qty"],
                        "Harga": item["Harga"],
                        "Subtotal": item["Subtotal"],
                        "Catatan": catatan,
                        "Pembayaran": pembayaran,
                        "Kembalian": kembalian
                    })

                df_baru = pd.DataFrame(data_baru)

                df_lama = pd.read_csv(FILE_NAME)

                df_gabung = pd.concat(
                    [df_lama, df_baru],
                    ignore_index=True
                )

                df_gabung.to_csv(FILE_NAME, index=False)

                st.success("Transaksi berhasil disimpan")

                st.session_state.cart = []

        else:
            st.error("Uang tidak cukup")

    else:
        st.info("Keranjang kosong")

# =====================================
# HALAMAN KEUANGAN
# =====================================
elif menu == "Keuangan":

    st.title("📊 KEUANGAN")
    st.subheader("Dashboard Keuangan")

    df = pd.read_csv(FILE_NAME)

    if len(df) > 0:

        df["Tanggal"] = pd.to_datetime(df["Tanggal"])

        pilihan = st.selectbox(
            "Pilih Periode",
            [
                "Hari Ini",
                "7 Hari",
                "30 Hari",
                "Custom"
            ]
        )

        today = datetime.now()

        if pilihan == "Hari Ini":

            filtered = df[
                df["Tanggal"].dt.date == today.date()
            ]

        elif pilihan == "7 Hari":

            filtered = df[
                df["Tanggal"] >= today - timedelta(days=7)
            ]

        elif pilihan == "30 Hari":

            filtered = df[
                df["Tanggal"] >= today - timedelta(days=30)
            ]

        else:

            start = st.date_input("Dari")

            end = st.date_input("Sampai")

            filtered = df[
                (df["Tanggal"].dt.date >= start) &
                (df["Tanggal"].dt.date <= end)
            ]

        # =====================================
        # RINGKASAN
        # =====================================
        pemasukan = filtered["Subtotal"].sum()

        pengeluaran = 0

        laba_bersih = pemasukan - pengeluaran

        transaksi = len(filtered)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Pemasukan", f"Rp {pemasukan:,}")
        col2.metric("Pengeluaran", f"Rp {pengeluaran:,}")
        col3.metric("Laba Bersih", f"Rp {laba_bersih:,}")
        col4.metric("Jumlah Transaksi", transaksi)

        st.divider()

        st.subheader("Data Transaksi")

        st.dataframe(filtered, use_container_width=True)
        st.subheader("📈 Grafik Penjualan")

grafik = filtered.groupby("Produk")["Subtotal"].sum()

st.bar_chart(grafik)

    else:
        st.warning("Belum ada transaksi")
