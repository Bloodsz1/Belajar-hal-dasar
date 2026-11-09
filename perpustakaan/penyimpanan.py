"""penyimpanan.py - Membaca dan menulis file JSON dengan aman.

Menulis dilakukan ke file sementara dulu, lalu diganti (os.replace). Dengan begitu
file asli tidak pernah setengah tertulis kalau program mati di tengah jalan.
"""

import json
import os

from models import DataRusakError


def simpan_json(nama_file, data):
    sementara = f"{nama_file}.tmp"
    with open(sementara, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    os.replace(sementara, nama_file)


def muat_json(nama_file, bawaan):
    """Isi file JSON. Kalau file belum ada, kembalikan `bawaan`.

    Kalau isinya bukan JSON yang valid, muncul DataRusakError.
    """
    if not os.path.exists(nama_file):
        return bawaan
    try:
        with open(nama_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as error:
        nama = os.path.basename(str(nama_file))
        raise DataRusakError(f"File '{nama}' bukan JSON yang valid: {error}") from error
