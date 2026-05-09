import streamlit as st
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
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.main {
    background-color: #fffafc;
}

h1, h2, h3 {
    color: #d63384;
    font-family: 'Poppins', sans-serif;
}

.stButton>button {
    background-color: #ff4da6;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #ff1a8c;
    transform: scale(1.03);
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

.stNumberInput>div>div>input {
    border-radius: 10px;
}

textarea {
    border-radius: 10px !important;
}

div[data-testid="stMetric"] {
    background-color: #ffe6f2;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #ffb3d9;
}

section[data-testid="stSidebar"] {
    background-color: #fff0f6;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOGIN ADMIN
# =====================================

admin_login = False

username = st.sidebar.text_input("Admin Username")
password = st.sidebar.text_input("Admin Password", type="password")

if username == "admin" and password == "123":
    admin_login = True

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

if "reviews" not in st.session_state:

    st.session_state.reviews = [
        {
            "nama": "Alya",
            "rating": 5,
            "komentar": "Bunganya cantik dan segar 🌸"
        },
        {
            "nama": "Rina",
            "rating": 4,
            "komentar": "Pengiriman cepat dan admin ramah"
        }
    ]

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
    },

    {
        "nama": "Tulip",
        "harga": 50000,
        "stok": 30,
        "gambar": "https://images.unsplash.com/photo-1520763185298-1b434c919102"
    },

    {
        "nama": "Sunflower",
        "harga": 30000,
        "stok": 12,
        "gambar": "https://images.unsplash.com/photo-1470509037663-253afd7f0f51"
    },

    {
        "nama": "Baby Breath",
        "harga": 40000,
        "stok": 18,
        "gambar": "https://images.unsplash.com/photo-1468327768560-75b778cbb551"
    },

    {
        "nama": "Anggrek",
        "harga": 75000,
        "stok": 8,
        "gambar": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6"
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

    st.markdown("""
    <h1 style='text-align:center; color:#ff4da6;'>
    🌸 SHIFA FLORIST 🌸
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center; font-size:18px;'>
    Bouquet aesthetic • Fresh flowers • Special moments 💐
    </p>
    """, unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1526045478516-99145907023c",
        use_container_width=True
    )

    st.info("""
📞 WhatsApp : 08123456789
📸 Instagram : @shifaflorist
🎵 TikTok : @shifaflorist
""")

    st.divider()

    st.header("📚 Katalog Bunga")

    cols = st.columns(3)

    for i, flower in enumerate(flowers):

        with cols[i % 3]:

            st.image(flower["gambar"], use_container_width=True)

            st.markdown(f"""
            <div style="
            background-color:white;
            padding:10px;
            border-radius:15px;
            box-shadow:0 4px 10px rgba(0,0,0,0.1);
            text-align:center;
            margin-bottom:10px;
            ">
            <h3 style='color:#ff4da6;'>{flower['nama']}</h3>
            </div>
            """, unsafe_allow_html=True)

            st.write(f"💰 Harga : Rp {flower['harga']:,}")
            st.write(f"📦 Stok : {flower['stok']}")

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
    # CUSTOM BOUQUET
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

        st.markdown(f"## 💵 Total : Rp {total:,}")

        catatan = st.text_area("Catatan Pembelian")

        st.subheader("🚚 Pengiriman")

        nama_penerima = st.text_input("Nama Penerima")

        alamat = st.text_area("Alamat Pengiriman")

        no_hp = st.text_input("Nomor HP Penerima")

        pengiriman = st.selectbox(
            "Metode Pengiriman",
            ["Ambil di Toko", "Kurir Toko", "GoSend", "GrabExpress"]
        )

        st.subheader("🎀 Request Customer")

        request_bunga = st.multiselect(
            "Bunga ingin diapakan?",
            [
                "Dibuat bouquet aesthetic",
                "Tambah pita",
                "Tambah lampu LED",
                "Packing premium",
                "Tambah boneka",
                "Warna dominan pink",
                "Warna dominan putih",
                "Buket wisuda",
                "Buket ulang tahun",
                "Buket anniversary"
            ]
        )

        kartu_ucapan = st.text_area(
            "Isi Kartu Ucapan"
        )

        permintaan_tambahan = st.text_area(
            "Permintaan Tambahan"
        )

        pembayaran = st.number_input(
            "Uang Masuk",
            min_value=0
        )

        if pembayaran >= total:

            kembalian = pembayaran - total

            st.success("Pembayaran Berhasil")

            st.write(f"💰 Kembalian : Rp {kembalian:,}")

            st.subheader("📱 QRIS Pembayaran")

            qris_text = f"""
            SHIFA FLORIST
            Total Bayar Rp {total}
            """

            qr = qrcode.make(qris_text)

            qr.save("qris.png")

            st.image("qris.png", width=250)

            st.subheader("🧾 Struk Pembelian")

            struk = f"""
=========================
     SHIFA FLORIST
=========================

Tanggal :
{datetime.now().strftime("%d-%m-%Y %H:%M")}

"""

            for item in st.session_state.cart:

                struk += f"""
{item['Produk']}
{item['Qty']} x Rp {item['Harga']:,}
= Rp {item['Subtotal']:,}
"""

            struk += f"""

-------------------------
TOTAL : Rp {total:,}
BAYAR : Rp {pembayaran:,}
KEMBALI : Rp {kembalian:,}

Terima Kasih 🌸
"""

            st.text(struk)

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
    # REVIEW
    # =====================================

    st.divider()

    st.header("⭐ Review Pelanggan")

    nama_review = st.text_input("Nama Anda")

    rating = st.slider(
        "Rating",
        min_value=1,
        max_value=5,
        value=5
    )

    komentar = st.text_area("Komentar Review")

    if st.button("Kirim Review"):

        st.session_state.reviews.append({
            "nama": nama_review,
            "rating": rating,
            "komentar": komentar
        })

        st.success("Review berhasil ditambahkan")

    for review in st.session_state.reviews:

        st.markdown("---")

        st.subheader(f"👤 {review['nama']}")

        st.write("⭐" * review["rating"])

        st.write(review["komentar"])

# =====================================
# HALAMAN KEUANGAN
# =====================================

elif menu == "Keuangan":

    if not admin_login:

        st.warning("Menu keuangan khusus admin")
        st.stop()

    st.title("📊 Dashboard Keuangan")

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

        st.subheader("📋 Data Transaksi")

        st.dataframe(filtered, use_container_width=True)

        st.subheader("📈 Grafik Penjualan")

        grafik = filtered.groupby("Produk")["Subtotal"].sum()

        st.bar_chart(grafik)

    else:
        st.warning("Belum ada transaksi")

# =====================================
# FOOTER
# =====================================

st.markdown("""
<hr>
<center>
<p style='color:gray;'>
🌸 SHIFA FLORIST © 2026 <br>
Made with Streamlit 💖
</p>
</center>
""", unsafe_allow_html=True)
