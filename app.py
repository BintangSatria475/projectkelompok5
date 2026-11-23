import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="SmartJajan - Teman Jajan Pintar",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Daftar contoh menu kantin. Silakan ubah nama dan harga sesuai kantin sekolah.
DEFAULT_MENU = [
    {"nama": "Nasi Goreng", "kategori": "Makanan", "harga": 10000, "emoji": "🍛"},
    {"nama": "Mie Goreng", "kategori": "Makanan", "harga": 8000, "emoji": "🍜"},
    {"nama": "Ayam Geprek", "kategori": "Makanan", "harga": 12000, "emoji": "🍗"},
    {"nama": "Roti Cokelat", "kategori": "Camilan", "harga": 5000, "emoji": "🍞"},
    {"nama": "Kentang Goreng", "kategori": "Camilan", "harga": 7000, "emoji": "🍟"},
    {"nama": "Es Teh", "kategori": "Minuman", "harga": 3000, "emoji": "🧋"},
    {"nama": "Air Mineral", "kategori": "Minuman", "harga": 4000, "emoji": "💧"},
    {"nama": "Jus Jeruk", "kategori": "Minuman", "harga": 6000, "emoji": "🍊"},
]

DATA_FILE = Path(__file__).with_name("menu_kantin.json")

def load_menu():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list) and data:
                return data
        except Exception:
            pass
    return DEFAULT_MENU.copy()

def save_menu():
    DATA_FILE.write_text(
        json.dumps(st.session_state.menu, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

if "menu" not in st.session_state:
    st.session_state.menu = load_menu()
if "keranjang" not in st.session_state:
    st.session_state.keranjang = {}

def rupiah(value):
    return "Rp" + f"{int(value):,}".replace(",", ".")

def total_belanja():
    return sum(
        next((m["harga"] for m in st.session_state.menu if m["nama"] == nama), 0) * jumlah
        for nama, jumlah in st.session_state.keranjang.items()
    )

st.markdown("""
<div class="hero">
  <div class="hero-badge">🌈 TEMAN JAJAN PINTAR</div>
  <h1>Uang jajanku cukup nggak, ya?</h1>
  <p>Atur uang saku, pilih makanan favorit, dan cek apakah uangmu cukup sebelum jajan.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🍱 SmartJajan")
    st.caption("Asisten kecil untuk mengatur uang jajan.")
    halaman = st.radio(
        "Pilih halaman",
        ["🏠 Cek Uang Jajan", "📋 Daftar Menu", "🛠️ Atur Menu Kantin"],
        label_visibility="collapsed"
    )
    st.divider()
    st.markdown("**💡 Tips hemat**")
    st.info("Sisihkan sedikit uang untuk ditabung. Tidak harus menghabiskan semua uang saku!")

if halaman == "🏠 Cek Uang Jajan":
    st.subheader("💰 Berapa uang saku kamu hari ini?")
    col1, col2 = st.columns([1.1, 1])
    with col1:
        uang_saku = st.number_input(
            "Masukkan uang yang kamu bawa (rupiah)",
            min_value=0, max_value=1000000, value=15000, step=1000,
            help="Contoh: 15000 berarti Rp15.000"
        )
    with col2:
        target_tabung = st.number_input(
            "Mau ditabung berapa? (opsional)",
            min_value=0, max_value=1000000, value=0, step=1000
        )
    uang_boleh_dipakai = max(0, int(uang_saku) - int(target_tabung))
    st.markdown(
        f'<div class="budget-strip"><span>Uang yang boleh dipakai jajan</span>'
        f'<strong>{rupiah(uang_boleh_dipakai)}</strong></div>',
        unsafe_allow_html=True
    )

    st.divider()
    st.subheader("🛒 Pilih jajanan yang kamu mau")
    if not st.session_state.menu:
        st.warning("Belum ada menu. Tambahkan menu di halaman Atur Menu Kantin.")
    else:
        names = [m["nama"] for m in st.session_state.menu]
        selected = st.selectbox(
            "Pilih menu kantin",
            names,
            format_func=lambda n: f"{next(m['emoji'] for m in st.session_state.menu if m['nama'] == n)}  {n} — {rupiah(next(m['harga'] for m in st.session_state.menu if m['nama'] == n))}"
        )
        chosen = next(m for m in st.session_state.menu if m["nama"] == selected)
        add_col, qty_col = st.columns([2, 1])
        with qty_col:
            jumlah = st.number_input("Jumlah", min_value=1, max_value=20, value=1, step=1)
        with add_col:
            st.write("")
            st.write("")
            if st.button("➕ Tambahkan ke keranjang", use_container_width=True, type="primary"):
                st.session_state.keranjang[selected] = st.session_state.keranjang.get(selected, 0) + int(jumlah)
                st.rerun()

    st.subheader("🧺 Keranjang jajanmu")
    if st.session_state.keranjang:
        for nama in list(st.session_state.keranjang.keys()):
            menu_item = next((m for m in st.session_state.menu if m["nama"] == nama), None)
            if menu_item is None:
                del st.session_state.keranjang[nama]
                continue
            c1, c2, c3, c4 = st.columns([3, 1, 2, 1])
            with c1:
                st.write(f"{menu_item['emoji']} **{nama}**")
                st.caption(rupiah(menu_item["harga"]) + " / item")
            with c2:
                st.write(f"x {st.session_state.keranjang[nama]}")
            with c3:
                st.write(f"**{rupiah(menu_item['harga'] * st.session_state.keranjang[nama])}**")
            with c4:
                if st.button("🗑️", key=f"hapus_{nama}", help=f"Hapus {nama}"):
                    del st.session_state.keranjang[nama]
                    st.rerun()
        total = total_belanja()
        sisa = uang_boleh_dipakai - total
        st.divider()
        a, b = st.columns(2)
        a.metric("Total belanja", rupiah(total))
        b.metric("Sisa uang", rupiah(sisa) if sisa >= 0 else rupiah(abs(sisa)) + " kurang")
        if sisa >= 0:
            st.success(f"🎉 Yeay! Uangmu cukup. Setelah jajan, kamu masih punya {rupiah(sisa)}.")
            if target_tabung > 0:
                st.caption(f"Target tabungan {rupiah(target_tabung)} sudah disisihkan dari awal.")
        else:
            st.error(f"Ups! Uangmu kurang {rupiah(abs(sisa))}. Coba kurangi satu menu atau pilih yang lebih murah.")
        if st.button("Kosongkan keranjang", use_container_width=False):
            st.session_state.keranjang = {}
            st.rerun()
    else:
        st.info("Keranjangmu masih kosong. Pilih menu di atas untuk mulai menghitung.")

    st.divider()
    st.subheader("✨ Rekomendasi sesuai uangmu")
    if uang_boleh_dipakai > 0:
        affordable = [m for m in st.session_state.menu if m["harga"] <= uang_boleh_dipakai]
        affordable.sort(key=lambda x: x["harga"])
        if affordable:
            st.caption("Menu yang harganya masih sesuai dengan uang jajan yang boleh kamu pakai:")
            rec_cols = st.columns(min(3, len(affordable)))
            for i, item in enumerate(affordable[:9]):
                with rec_cols[i % len(rec_cols)]:
                    st.markdown(
                        f'<div class="menu-card"><div class="food-emoji">{item["emoji"]}</div>'
                        f'<b>{item["nama"]}</b><div class="price">{rupiah(item["harga"])}</div>'
                        f'<small>{item["kategori"]}</small></div>',
                        unsafe_allow_html=True
                    )
        else:
            st.warning("Belum ada menu yang sesuai. Coba sisihkan tabungan lebih sedikit atau pilih menu yang lebih murah.")
    else:
        st.info("Masukkan uang jajan terlebih dahulu untuk melihat rekomendasi.")

elif halaman == "📋 Daftar Menu":
    st.subheader("📋 Daftar harga kantin")
    st.write("Lihat harga sebelum membeli supaya kamu bisa merencanakan uang jajan.")
    categories = ["Semua"] + sorted(set(m["kategori"] for m in st.session_state.menu))
    category = st.selectbox("Filter kategori", categories)
    filtered = st.session_state.menu if category == "Semua" else [m for m in st.session_state.menu if m["kategori"] == category]
    cols = st.columns(3)
    for i, item in enumerate(filtered):
        with cols[i % 3]:
            st.markdown(
                f'<div class="menu-card"><div class="food-emoji">{item["emoji"]}</div>'
                f'<b>{item["nama"]}</b><div class="price">{rupiah(item["harga"])}</div>'
                f'<small>{item["kategori"]}</small></div>',
                unsafe_allow_html=True
            )

elif halaman == "🛠️ Atur Menu Kantin":
    st.subheader("🛠️ Atur daftar menu dan harga")
    st.caption("Halaman ini untuk pengelola/guru/orang yang memperbarui daftar harga kantin.")
    with st.form("form_menu", clear_on_submit=True):
        nama = st.text_input("Nama menu")
        kategori = st.selectbox("Kategori", ["Makanan", "Camilan", "Minuman"])
        harga = st.number_input("Harga (rupiah)", min_value=500, max_value=100000, value=5000, step=500)
        emoji = st.selectbox("Ikon menu", ["🍛", "🍜", "🍗", "🍞", "🍟", "🧋", "💧", "🍊", "🍰", "🥪"])
        submitted = st.form_submit_button("Simpan menu", type="primary")
        if submitted:
            if not nama.strip():
                st.error("Nama menu belum diisi.")
            elif any(m["nama"].lower() == nama.strip().lower() for m in st.session_state.menu):
                st.error("Nama menu tersebut sudah ada.")
            else:
                st.session_state.menu.append({
                    "nama": nama.strip(), "kategori": kategori,
                    "harga": int(harga), "emoji": emoji
                })
                save_menu()
                st.success(f"Menu {nama} berhasil ditambahkan!")
                st.rerun()

    st.divider()
    st.markdown("**Menu yang tersedia saat ini**")
    for i, item in enumerate(list(st.session_state.menu)):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        c1.write(f"{item['emoji']} **{item['nama']}**")
        c2.write(item["kategori"])
        c3.write(rupiah(item["harga"]))
        if c4.button("Hapus", key=f"delmenu_{i}"):
            st.session_state.menu = [m for m in st.session_state.menu if m["nama"] != item["nama"]]
            st.session_state.keranjang.pop(item["nama"], None)
            save_menu()
            st.rerun()

st.markdown('<div class="footer">Dibuat untuk membantu anak-anak jajan dengan bijak 💚</div>', unsafe_allow_html=True)
