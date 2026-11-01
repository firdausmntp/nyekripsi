# PANDUAN PENGISIAN BAB III & ARTIFAK METODOLOGI

---

## 1. Tabel Operasionalisasi Variabel (Kuantitatif)

Gunakan format tabel berikut pada Sub-Bab 3.3:

| Variabel | Konsep Teoretis | Dimensi | Indikator | Skala Pengukuran | No. Butir Kuesioner |
|---|---|---|---|---|---|
| Variabel X (Bebas) | [Definisi teoretis dari Grand/Middle Theory] | 1. Dimensi A<br/>2. Dimensi B | - Indikator 1<br/>- Indikator 2<br/>- Indikator 3 | Likert (1-5) | 1, 2, 3<br/>4, 5<br/>6, 7, 8 |
| Variabel Y (Terikat) | [Definisi teoretis dari Grand/Middle Theory] | 1. Dimensi C<br/>2. Dimensi D | - Indikator 4<br/>- Indikator 5 | Likert (1-5) | 9, 10, 11<br/>12, 13, 14 |

---

## 2. Template Kebutuhan Fungsional (FR) & Non-Fungsional (NFR) (IT / Software Engineering)

Gunakan format berikut pada Sub-Bab 3.2:

### Kebutuhan Fungsional (Functional Requirements)
| Kode FR | Deskripsi Kebutuhan Sistem | Aktor | Tingkat Prioritas |
|---|---|---|---|
| FR-01 | Pengguna dapat melakukan registrasi dan verifikasi akun via email/OTP. | Mahasiswa | High |
| FR-02 | Sistem mampu mengunggah dan memverifikasi daftar referensi sitasi. | Mahasiswa | High |
| FR-03 | Dosen dapat memberikan catatan revisi formatif per sub-bab. | Dosen Pembimbing | Medium |

### Kebutuhan Non-Fungsional (Non-Functional Requirements - FURPS+)
| Kategori | Parameter | Kriteria Sukses / Spesifikasi |
|---|---|---|
| **Performance** | Waktu respon server | $< 2$ detik untuk beban 100 pengguna simultan. |
| **Usability** | Skor kepuasan pengguna | Skor System Usability Scale (SUS) minimal 70 (Grade B). |
| **Reliability** | Ketersediaan sistem | Uptime minimal 99.5% selama masa pengujian. |
| **Security** | Enkripsi data sensitif | Hashing kata sandi menggunakan algoritma Argon2id / bcrypt. |
