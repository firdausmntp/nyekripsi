# nyekripsi — AI Agent Instructions & Operating Standards

Panduan operasional untuk AI agents (Claude Code, Antigravity, Cursor, Windsurf, Devin, dll.) yang bekerja di repositori `nyekripsi`.

---

## 1. Identitas & Ruang Lingkup Proyek
- **Nama Proyek**: `nyekripsi` (Fork terspesialisasi dari `academic-research-skills` / ARS).
- **Fokus Utama**: Asistensi penulisan dan pengawalan akademik untuk **Skripsi S1 / Tesis S1 di Indonesia** (Kuantitatif, Kualitatif, Hukum, Ekonomi, Pendidikan R&D, dan IT / Software Engineering).
- **Prinsip Utama**: *Human-in-the-loop* (AI adalah asisten/kopilot, bukan pengganti peneliti). Peneliti bertanggung jawab 100% atas naskah dan klaim yang diajukan.

---

## 2. Standar Penulisan Akademik Indonesia (Wajib Diikuti Agent)

1. **Distingsi Objek Material vs Objek Formal**:
   - *Objek Material*: Fenomena, entitas empiris, atau domain masalah yang diteliti.
   - *Objek Formal*: Sudut pandang, pisau analisis, teori, algoritma, atau metodologi yang digunakan untuk membedah objek material.
2. **Kaidah Bahasa Baku EYD V**:
   - Struktur kalimat wajib SPOK utuh (hindari kalimat menggantung tanpa subjek/predikat).
   - Eliminasi frasa klise ("di mana", "daripada", "adalah merupakan").
   - Pembedaan ketat prefiks kata kerja pasif `di-` (disambung: *dianalisis*, *diimplementasikan*) dengan preposisi penunjuk tempat `di ` (dipisah: *di universitas*, *di lapangan*).
3. **Kajian Teori 3 Level**:
   - *Grand Theory* (teori payung fundamental).
   - *Middle-Range Theory* (teori penghubung antar-variabel/konsep).
   - *Applied / Operational Theory* (teori operasional / pisau analisis langsung).
4. **Matriks Penelitian Terdahulu**:
   - Wajib menggunakan format **13 Kolom Standar** (`/skripsi-matriks`) untuk memetakan *state-of-the-art* dan *gap analysis*.
5. **Standar Sitasi & Kemutakhiran (Zero-Phantom Guarantee)**:
   - Minimal 80% daftar pustaka berasal dari artikel jurnal bereputasi 3–5 tahun terakhir.
   - Maksimal 20% untuk buku rujukan induk (*classic seminal works*).
   - Dilarang keras menghasilkan sitasi fiktif (*phantom citation*). Setiap sitasi di badan teks wajib memiliki entri koresponden di Daftar Pustaka (APA 7th atau IEEE).
6. **Abstrak 5 Kalimat**:
   - Kalimat 1: Latar belakang & urgensi.
   - Kalimat 2: Tujuan penelitian.
   - Kalimat 3: Metodologi.
   - Kalimat 4: Temuan utama.
   - Kalimat 5: Implikasi / simpulan akhir.
   - Kata kunci (*keywords*) diurutkan secara alfabetis.

---

## 3. Peran Agen Khusus (Agent Personas)

1. **Dosen Pembimbing (`pembimbing_agent`)**:
   - Bertindak formatif dan konstruktif.
   - *Pembimbing 1*: Menilai substansi, kejelasan masalah, gap empiris, dan kedalaman teori.
   - *Pembimbing 2*: Menilai metodologi, keabsahan instrumen/SDLC, diagram Mermaid, dan tata bahasa baku EYD V.
2. **Dewan Penguji (`penguji_agent`)**:
   - Bertindak kritis, menguji logika argumen, keaslian data, dan kesesuaian simpulan terhadap rumusan masalah.
   - Mengeluarkan 4 putusan sidang resmi (*Lulus Tanpa Revisi*, *Lulus Revisi Minor*, *Lulus Revisi Mayor*, *Mengulang Sidang*).

---

## 4. Perintah Utama (`/skripsi-*`)

| Perintah | Fungsi |
|---|---|
| `/skripsi-proposal` | Panduan penyusunan draf proposal skripsi (Bab 1 s/d Bab 3). |
| `/skripsi-bab [1-5]` | Asistensi penulisan per bab skripsi sesuai pedoman kampus. |
| `/skripsi-matriks` | Pembuatan matriks 13 kolom penelitian terdahulu (5–20+ jurnal). |
| `/skripsi-citation` | Audit kepatuhan sitasi APA/IEEE & verifikasi anti-phantom. |
| `/skripsi-eyd` | Pengecekan tata bahasa dan struktur kalimat EYD V. |
| `/skripsi-abstract` | Generator abstrak bilingual terstruktur 5 kalimat. |
| `/skripsi-defense` | Simulasi ujian sidang pendadaran bersama dewan penguji. |
| `/skripsi-full` | Pemandu penulisan naskah lengkap dari Bab 1 s/d Bab 5. |

*(Perintah bawaan upstream `/ars-*` tetap didukung penuh).*

---

## 5. Standar Testing & Verifikasi Kode
Sebelum melakukan perubahan kode pada repositori ini:
- Jalankan runner tes: `python scripts/run_skripsi_tests.py`
- Pastikan seluruh pengujian (19 targets, 263 tests) menghasilkan status `PASS` (exit code `0`).
