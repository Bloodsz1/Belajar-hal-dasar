"""info_buku.py - Mencari info buku (penulis, tahun, subjek) dari judul.

Cara kerja (dua sumber, supaya hasilnya tidak mengarang):
  1. Open Library (data buku nyata, gratis, tanpa kunci) -> daftar kandidat buku.
  2. Gemini (LLM) -> memilih kandidat yang paling cocok, membetulkan judul yang typo,
     dan menentukan subjek Fiksi / Non-fiksi.
Penulis dan tahun SELALU diambil dari data Open Library, bukan dari tebakan LLM.
Gemini hanya menjawab sendiri kalau Open Library tidak menemukan apa-apa, dan hasilnya
diberi label "belum diverifikasi".

Tanpa kunci Gemini atau tanpa internet, fungsi tetap bekerja sebisanya (lihat cari_info_buku).
Modul ini tidak memakai tkinter, jadi mudah diuji. Hanya memakai library bawaan Python.
"""

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

from models import DAFTAR_SUBJEK

URL_OPEN_LIBRARY = "https://openlibrary.org/search.json"
URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
MODEL_BAWAAN = "gemini-3.8-flash"   # bisa diganti lewat variabel lingkungan GEMINI_MODEL
NAMA_FILE_KUNCI = "gemini_key.txt"
BATAS_WAKTU = 15                    # detik
USER_AGENT = "PustakaPerpustakaan/1.0 (belajar python)"


class InfoBukuError(Exception):
    """Gagal menghubungi layanan atau jawabannya tidak bisa dibaca."""


# --------------------------------------------------------------------------
# Kunci API
# --------------------------------------------------------------------------
def muat_kunci(folder):
    """Mengambil kunci Gemini: dari variabel lingkungan GEMINI_API_KEY, atau dari file
    gemini_key.txt di folder program. Mengembalikan None kalau tidak ada."""
    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if kunci:
        return kunci
    jalur = os.path.join(str(folder), NAMA_FILE_KUNCI)
    try:
        with open(jalur, encoding="utf-8") as f:
            kunci = f.read().strip()
    except OSError:
        return None
    return kunci or None


# --------------------------------------------------------------------------
# Permintaan HTTP
# --------------------------------------------------------------------------
def http_json(url, isi=None, header=None):
    """Mengirim permintaan (GET, atau POST kalau `isi` ada) lalu mengembalikan JSON-nya."""
    data = None
    kepala = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if header:
        kepala.update(header)
    if isi is not None:
        data = json.dumps(isi).encode("utf-8")
        kepala["Content-Type"] = "application/json"
    permintaan = urllib.request.Request(url, data=data, headers=kepala)
    try:
        with urllib.request.urlopen(permintaan, timeout=BATAS_WAKTU) as jawaban:
            return json.loads(jawaban.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise InfoBukuError(f"Server menjawab galat {e.code}.") from e
    except urllib.error.URLError as e:
        raise InfoBukuError("Tidak bisa terhubung ke internet.") from e
    except (TimeoutError, OSError) as e:
        raise InfoBukuError("Koneksi terlalu lama atau terputus.") from e
    except ValueError as e:
        raise InfoBukuError("Jawaban server tidak bisa dibaca.") from e


# --------------------------------------------------------------------------
# Sumber 1: Open Library
# --------------------------------------------------------------------------
def tahun_wajar(nilai):
    """Mengembalikan tahun (int) kalau masuk akal, kalau tidak None."""
    try:
        tahun = int(nilai)
    except (TypeError, ValueError):
        return None
    return tahun if 1000 <= tahun <= date.today().year + 1 else None


def tebak_subjek(daftar_subjek):
    """Tebakan kasar dari label subjek Open Library: 'Fiksi' atau None (belum tahu)."""
    kecil = [str(s).lower() for s in daftar_subjek or []]
    if any("non-fiction" in s or "nonfiction" in s for s in kecil):
        return "Non-fiksi"
    if any("fiction" in s or "novel" in s for s in kecil):
        return "Fiksi"
    return None


def cari_open_library(judul, ambil=http_json, jumlah=5):
    """Mengembalikan daftar kandidat: [{'judul','penulis','tahun','subjek'}, ...]."""
    query = urllib.parse.urlencode({
        "title": judul,
        "limit": jumlah,
        "fields": "title,author_name,first_publish_year,subject",
    })
    jawaban = ambil(f"{URL_OPEN_LIBRARY}?{query}")
    kandidat = []
    for d in jawaban.get("docs", []):
        if not d.get("title"):
            continue
        penulis = ", ".join((d.get("author_name") or [])[:2])
        kandidat.append({
            "judul": str(d["title"]).strip(),
            "penulis": penulis,
            "tahun": tahun_wajar(d.get("first_publish_year")),
            "subjek": tebak_subjek(d.get("subject")),
        })
    return kandidat


# --------------------------------------------------------------------------
# Sumber 2: Gemini
# --------------------------------------------------------------------------
def buat_perintah(judul, kandidat):
    daftar = json.dumps(
        [{"no": i, "judul": k["judul"], "penulis": k["penulis"], "tahun": k["tahun"]}
         for i, k in enumerate(kandidat)], ensure_ascii=False)
    return (
        "Kamu asisten perpustakaan. Pengguna mengetik judul buku (mungkin ada typo atau tidak "
        "lengkap):\n"
        f"JUDUL: {judul}\n\n"
        f"Kandidat dari database Open Library (nomor mulai 0):\n{daftar}\n\n"
        "Tugasmu:\n"
        "1. Pilih nomor kandidat yang paling cocok dengan buku yang dimaksud. Kalau tidak ada "
        "yang cocok atau daftar kosong, pilihan = null.\n"
        "2. 'judul' = judul buku yang benar (betulkan typo, huruf besar-kecil).\n"
        f"3. 'subjek' harus persis salah satu dari: {', '.join(DAFTAR_SUBJEK)}, atau null kalau ragu.\n"
        "4. Hanya kalau pilihan = null DAN kamu yakin buku itu nyata, isi 'penulis' dan 'tahun' "
        "(tahun terbit pertama, angka). Kalau tidak yakin, isi null. Jangan mengarang.\n"
        'Jawab HANYA JSON: {"pilihan": angka|null, "judul": teks|null, "subjek": teks|null, '
        '"penulis": teks|null, "tahun": angka|null}')


def _ambil_json(teks):
    teks = teks.strip()
    teks = re.sub(r"^```(?:json)?\s*|\s*```$", "", teks)
    return json.loads(teks)


def tanya_gemini(judul, kandidat, kunci, model=None, ambil=http_json):
    """Mengembalikan dict jawaban Gemini (kunci: pilihan, judul, subjek, penulis, tahun)."""
    model = model or os.environ.get("GEMINI_MODEL") or MODEL_BAWAAN
    isi = {
        "contents": [{"parts": [{"text": buat_perintah(judul, kandidat)}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }
    jawaban = ambil(URL_GEMINI.format(model=model), isi=isi, header={"x-goog-api-key": kunci})
    try:
        teks = jawaban["candidates"][0]["content"]["parts"][0]["text"]
        hasil = _ambil_json(teks)
    except (KeyError, IndexError, TypeError, ValueError) as e:
        raise InfoBukuError("Jawaban Gemini tidak sesuai format.") from e
    if not isinstance(hasil, dict):
        raise InfoBukuError("Jawaban Gemini tidak sesuai format.")
    return hasil


def _subjek_sah(teks):
    for s in DAFTAR_SUBJEK:
        if str(teks or "").strip().lower() == s.lower():
            return s
    return None


# --------------------------------------------------------------------------
# Fungsi utama
# --------------------------------------------------------------------------
def cari_info_buku(judul, kunci=None, ambil=http_json):
    """Mencari info buku dari judul.

    Mengembalikan (hasil, pesan):
      hasil = {'judul','penulis','tahun','subjek','sumber','terverifikasi'} atau None
      pesan = keterangan untuk pengguna (mis. sumber data atau alasan gagal)
    """
    judul = judul.strip()
    if len(judul) < 2:
        return None, "Ketik judul buku dulu (minimal 2 huruf)."

    peringatan = ""
    try:
        kandidat = cari_open_library(judul, ambil)
    except InfoBukuError as e:
        kandidat = []
        peringatan = f"Open Library: {e} "

    jawab = None
    if kunci:
        try:
            jawab = tanya_gemini(judul, kandidat, kunci, ambil=ambil)
        except InfoBukuError as e:
            peringatan += f"Gemini: {e} "
    else:
        peringatan += "Kunci Gemini belum diatur, hanya memakai Open Library. "

    hasil = _gabung(judul, kandidat, jawab)
    if hasil is None:
        return None, (peringatan + "Buku tidak ditemukan, isi manual saja.").strip()
    if hasil["terverifikasi"]:
        sumber = "Open Library + Gemini" if jawab else "Open Library"
        pesan = f"Terisi dari {sumber}. Periksa dulu sebelum menyimpan."
    else:
        pesan = "Dari tebakan Gemini, BELUM diverifikasi. Periksa penulis dan tahun dengan teliti."
    return hasil, (pesan + " " + peringatan).strip()


def _gabung(judul, kandidat, jawab):
    """Menentukan hasil akhir. Penulis & tahun hanya dari kandidat Open Library bila ada."""
    jawab = jawab or {}
    pilihan = jawab.get("pilihan")
    if isinstance(pilihan, int) and not isinstance(pilihan, bool) and 0 <= pilihan < len(kandidat):
        pilih = kandidat[pilihan]
    elif not jawab and kandidat:
        pilih = kandidat[0]  # tanpa Gemini: ambil hasil teratas Open Library
    else:
        pilih = None

    if pilih is not None:
        nama = str(jawab.get("judul") or "").strip() or pilih["judul"]
        return {
            "judul": nama,
            "penulis": pilih["penulis"],
            "tahun": pilih["tahun"],
            "subjek": _subjek_sah(jawab.get("subjek")) or pilih["subjek"],
            "sumber": "open_library",
            "terverifikasi": True,
        }

    penulis = str(jawab.get("penulis") or "").strip()
    tahun = tahun_wajar(jawab.get("tahun"))
    if penulis or tahun:  # Gemini yakin, tapi tanpa data pendukung
        return {
            "judul": str(jawab.get("judul") or "").strip() or judul,
            "penulis": penulis,
            "tahun": tahun,
            "subjek": _subjek_sah(jawab.get("subjek")),
            "sumber": "gemini",
            "terverifikasi": False,
        }
    return None
