"""util.py - Fungsi kecil untuk memformat tampilan (tanggal, rupiah, id, subjek)."""

from models import DAFTAR_SUBJEK

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def format_tanggal(tgl):
    """date(2026, 11, 8) -> '08 Nov 2026'. None -> '-'."""
    if tgl is None:
        return "-"
    return f"{tgl.day:02d} {BULAN[tgl.month - 1]} {tgl.year}"


def format_rupiah(angka):
    """15000 -> 'Rp15.000'."""
    return "Rp" + f"{int(angka):,}".replace(",", ".")


def format_id(nilai):
    """1 -> '#0001'."""
    try:
        return f"#{int(nilai):04d}"
    except (TypeError, ValueError):
        return str(nilai)


def samakan_subjek(teks):
    """Mencocokkan subjek tanpa peduli huruf besar-kecil: 'fiksi' -> 'Fiksi'."""
    bersih = str(teks).strip()
    for pilihan in DAFTAR_SUBJEK:
        if pilihan.lower() == bersih.lower():
            return pilihan
    return bersih
