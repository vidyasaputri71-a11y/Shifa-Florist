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
# HALAMAN KEUANGAN
# =====================================

if menu == "Keuangan":

    if admin_login:

        st.title("📊 Keuangan SHIFA FLORIST")

        df = pd.read_csv(FILE_NAME)

        if len(df) > 0:

            total_penjualan = df["Subtotal"].sum()

            total_transaksi = len(df)

            st.metric(
                "💰 Total Penjualan",
                f"Rp {total_penjualan:,}"
            )

            st.metric(
                "🧾 Jumlah Transaksi",
                total_transaksi
            )

            st.subheader("📋 Data Transaksi")

            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇ Download Laporan CSV",
                csv,
                "laporan_keuangan.csv",
                "text/csv"
            )

        else:

            st.warning("Belum ada transaksi")

    else:

        st.error("❌ Login admin terlebih dahulu")
# =====================================
# HALAMAN KASIR
# =====================================

elif menu == "Kasir":

    st.markdown("""
    <div style="
    background: linear-gradient(90deg, #ffd6e7, #fff0f6);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    ">

    <h1 style="
    color:#ff4da6;
    font-size:55px;
    margin-bottom:10px;
    ">
    🌸 🌷 SHIFA FLORIST 🌷 🌸
    </h1>

    <p style="
    font-size:20px;
    color:#cc0066;
    ">
    Fresh Flower • Bouquet Aesthetic • Special Moment 💐
    </p>

    <p style="
    font-size:16px;
    color:gray;
    ">
    ✨ Make Every Moment Bloom Beautifully ✨
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.info("""
📞 WhatsApp : 08123456789
📸 Instagram : @shifaflorist
🎵 TikTok : @shifaflorist
""")

    # =====================================
# KATALOG BUNGA
# =====================================

st.divider()

st.header("🌸 Katalog Bunga Premium")

cols = st.columns(3)

for i, flower in enumerate(flowers):

    with cols[i % 3]:

        st.markdown(f"""
        <div style="
        background: linear-gradient(180deg,#fff0f6,#ffffff);
        padding:20px;
        border-radius:25px;
        box-shadow:0 6px 18px rgba(255,105,180,0.15);
        text-align:center;
        margin-bottom:25px;
        border:1px solid #ffd6e7;
        ">

        <img src="{flower['gambar']}"
        style="
        width:100%;
        height:240px;
        object-fit:cover;
        border-radius:20px;
        margin-bottom:15px;
        ">

        <h2 style="
        color:#ff4da6;
        margin-bottom:10px;
        ">
        🌷 {flower['nama']}
        </h2>

        <p style="
        font-size:20px;
        color:#cc0066;
        font-weight:bold;
        ">
        Rp {flower['harga']:,}
        </p>

        <p style="
        color:gray;
        ">
        📦 Stok tersedia : {flower['stok']}
        </p>

        </div>
        """, unsafe_allow_html=True)

        qty = st.number_input(
            f"Qty {flower['nama']}",
            min_value=1,
            step=1,
            key=f"qty{i}"
        )

        if st.button(f"🛒 Tambah {flower['nama']}", key=f"btn{i}"):

            st.session_state.cart.append({
                "Produk": flower["nama"],
                "Qty": qty,
                "Harga": flower["harga"],
                "Subtotal": qty * flower["harga"]
            })

            st.success(f"{flower['nama']} berhasil ditambahkan 🌸")

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

    st.success("Custom bouquet ditambahkan 🌸")

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

    # =====================================
    # CATATAN
    # =====================================

    catatan = st.text_area("Catatan Pembelian")

    # =====================================
    # PENGIRIMAN
    # =====================================

    st.subheader("🚚 Pengiriman")

    nama_penerima = st.text_input("Nama Penerima")

    alamat = st.text_area("Alamat Pengiriman")

    no_hp = st.text_input("Nomor HP Penerima")

    pengiriman = st.selectbox(
        "Metode Pengiriman",
        ["Ambil di Toko", "Kurir Toko", "GoSend", "GrabExpress"]
    )

    # =====================================
    # REQUEST CUSTOMER
    # =====================================

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
        "Isi Kartu Ucapan",
        placeholder="Contoh : Happy Birthday 🌸"
    )

    permintaan_tambahan = st.text_area(
        "Permintaan Tambahan"
    )

    # =====================================
    # PEMBAYARAN
    # =====================================

    pembayaran = st.number_input(
        "Uang Masuk",
        min_value=0
    )

    if pembayaran >= total:

        kembalian = pembayaran - total

        st.success("Pembayaran Berhasil ✅")

        st.write(f"💰 Kembalian : Rp {kembalian:,}")

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
     SHIFA FLORIST
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

Penerima :
{nama_penerima}

Alamat :
{alamat}

No HP :
{no_hp}

Pengiriman :
{pengiriman}

Request :
{", ".join(request_bunga)}

Kartu Ucapan :
{kartu_ucapan}

Tambahan :
{permintaan_tambahan}

Terima Kasih 🌸
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

            st.success("Transaksi berhasil disimpan 🌸")

            st.session_state.cart = []

    else:
        st.error("Uang tidak cukup ❌")

else:
    st.info("Keranjang kosong")

# =====================================
# REVIEW PELANGGAN
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

    st.success("Review berhasil ditambahkan 🌸")

for review in st.session_state.reviews:

    st.markdown("---")

    st.subheader(f"👤 {review['nama']}")

    st.write("⭐" * review["rating"])

    st.write(review["komentar"])
