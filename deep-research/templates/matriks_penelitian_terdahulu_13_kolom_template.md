# Template Matriks Penelitian Terdahulu 13 Kolom (Sintesis Hasil Penelitian Terdahulu)

**Status:** Kanonikal / Standar Baku `nyekripsi`  
**Sasaran Pengguna:** Penulis Skripsi, Peneliti Literatur, Dosen Pembimbing, dan Dosen Penguji  
**Rujukan Metodologis:** Gambar Pedoman Skripsi (`IMG_20261101_025204_754.jpg`)  
**Penempatan Naskah:** Bab II (Sub-bab 2.1 Penelitian Terdahulu / Kajian Riset Sebelumnya)  

---

## 1. Panduan dan Filosofi Matriks Komparatif

Dalam penulisan tugas akhir sarjana (*Skripsi S1 Indonesia*), tinjauan penelitian terdahulu tidak boleh disajikan sekadar sebagai ringkasan paragraf terisolasi tanpa benang merah komparatif. Matriks 13 Kolom ini dirancang untuk:
1. **Memetakan Irisan:** Menemukan irisan Objek Material dan Objek Formal antara penelitian saat ini dengan riset sebelumnya.
2. **Menentukan Posisi Riset (*Research Positioning*):** Menempatkan usulan penelitian secara visual dan objektif dalam peta lanskap keilmuan yang telah ada.
3. **Membuktikan Anti-Duplikasi:** Menegaskan secara jujur dan transparan bahwa penelitian saat ini bukan merupakan plagiasi atau duplikasi dari riset terdahulu.
4. **Mengekstraksi Celah Pengetahuan (*Research Gap*):** Menemukan celah empiris, teoretis, kontekstual, dan metodologis dari kolom keterbatasan dan rekomendasi penelitian terdahulu.
5. **Merumuskan *State-of-the-Art* dan Penawaran Gagasan (*Novelty Proposition*):** Menyusun argumen kebaruan yang akan diuji sepanjang penelitian.

---

## 2. Struktur Baku Tabel Matriks 13 Kolom

Matriks wajib memuat kolom penomoran (`No`) dan tepat 13 kolom substantif sebagai berikut:

```markdown
| No | Nama Penulis | Judul Penelitian | Objek Material | Objek Formal | Konteks | Metode | Hasil | Pembahasan Singkat | Simpulan | Keterbatasan Penelitian | Rekomendasi | Penerbit | Tahun Terbit |
|:--:|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:--:|
| 1 | [Nama Penulis] | [Judul Artikel Rujukan] | [Objek Material] | [Objek Formal] | [Konteks Penelitian] | [Metode Penelitian] | [Temuan Hasil Utama] | [Pembahasan Singkat] | [Simpulan / Natijah] | [Keterbatasan Penelitian] | [Rekomendasi Peneliti Terdahulu] | [Nama Jurnal / Penerbit] | [Tahun Terbit] |
```

### 2.1 Konfigurasi Jumlah Studi Terdahulu (*Configurable Paper Count*)
Jumlah baris penelitian terdahulu dalam matriks ini bersifat fleksibel dan dapat dikonfigurasikan sesuai ketentuan dosen pembimbing atau pedoman selingkung perguruan tinggi:
- **Preset Minimal (5 Studi):** Standar ambang batas dasar untuk seminar proposal skripsi S1 program studi tertentu.
- **Preset Rekomendasi (10 Studi - Default):** Standar baku `nyekripsi` untuk memastikan pemetaan *state-of-the-art* yang kokoh dan representatif.
- **Preset Lanjutan (15 Studi):** Disarankan untuk skripsi yang menargetkan publikasi artikel pada jurnal nasional terakreditasi SINTA 1–2.
- **Preset Komprehensif (20+ Studi):** Diwajibkan untuk riset skripsi interdisipliner yang menggabungkan dua domain atau skripsi jalur riset unggulan.

Baris matriks dapat ditambah atau dikurangi secara dinamis ($N = 5, 10, 15, 20+$) dengan tetap mempertahankan keutuhan 13 kolom substantif dan baris penutup *USULAN* peneliti saat ini.

---

## 3. Spesifikasi Kolom dan Batasan Anti-Halusinasi

Setiap kolom memiliki aturan pengisian yang ketat guna mencegah distorsi atau halusinasi informasi:

| # | Nama Kolom | Deskripsi Substantif | Format Baku & Sintaks Valid | Batasan Integritas (*Anti-Hallucination Rules*) |
|---|---|---|---|---|
| **0** | `No` | Nomor urut artikel rujukan | Integer terurut: `1, 2, 3, ...` | Wajib berurutan; minimal 5–10 artikel jurnal mutakhir untuk skripsi S1. |
| **1** | `Nama Penulis` | Nama penulis artikel ilmiah rujukan | Format sitasi formal APA: `NamaBelakang, Inisial.` atau `NamaBelakang, Inisial. & NamaBelakang, Inisial.` | Dilarang menyingkat nama penulis pertama secara sembarangan; sesuaikan persis dengan naskah asli. |
| **2** | `Judul Penelitian` | Judul lengkap artikel atau karya ilmiah | *Sentence case* persis seperti naskah sumber, diapit tanda kutip ganda: `"..."` | Dilarang memparafrasa judul artikel rujukan. |
| **3** | `Objek Material` | Fenomena empiris spesifik yang diselidiki dalam artikel rujukan | Frasa nominal spesifik: misal `Perilaku konsumtif generasi Z di e-commerce` | Wajib mengekstrak fenomena faktual yang benar-benar diteliti, bukan opini umum. |
| **4** | `Objek Formal` | Teori, model analitis, atau pisau analisis yang digunakan | Frasa teoretis baku: misal `Technology Acceptance Model (TAM)` | Wajib menyebut nama teori atau kerangka kerja yang dirujuk penulisnya. |
| **5** | `Konteks` | Locus, setting instansional, populasi, dan rentang waktu riset rujukan | Lokus & subjek: misal `Mahasiswa pengguna mobile banking di Kota Yogyakarta` | Wajib mencerminkan populasi dan wilayah naskah asli. |
| **6** | `Metode` | Pendekatan, desain riset, instrumen, dan teknik analisis data | Ringkas & padat: misal `Kuantitatif survei (N=220), SEM-PLS` | Wajib menyebut ukuran sampel ($N$) atau jumlah informan jika tercantum di artikel. |
| **7** | `Hasil` | Temuan data dan nilai statistik utama | Faktual: misal `Perceived Ease of Use berpengaruh signifikan terhadap niat beli (β=0,38; p<0,01)` | Dilarang mengarang angka statistik. Jika kualitatif, sajikan tema temuan utamanya. |
| **8** | `Pembahasan Singkat` | Intisari perbandingan hasil studi tersebut dengan teori rujukan | Sintesis perbandingan: misal `Temuan mengonfirmasi teori TAM pada layanan belanja instan` | Tunjukkan posisi temuan artikel tersebut terhadap teori yang mereka gunakan. |
| **9** | `Simpulan` | *Natijah* / nilai pengetahuan inti yang dihasilkan artikel rujukan | 1–2 kalimat deklaratif: misal `Kenyamanan navigasi menjadi penentu utama loyalitas pengguna` | Intisari kesimpulan akhir penulis asli. |
| **10** | `Keterbatasan Penelitian` | Kelemahan metodologis, batas populasi, atau kendala lapangan | Kutipan batasan: misal `Sampel homogen di satu wilayah perkotaan; tidak menguji aspek biaya` | Jika artikel asli tidak menyebutkan secara eksplisit, tulis: `[Tersirat: ...]`. Dilarang mengarang bebas. |
| **11** | `Rekomendasi` | Arahan riset masa depan yang disarankan oleh penulis artikel | Arahan lanjutan: misal `Disarankan memperluas sampel ke kota tier-2 dan menambah variabel kepercayaan` | Menjadi pijakan utama perumusan *research gap* skripsi pengusul. |
| **12** | `Penerbit` | Nama jurnal ilmiah bereputasi, prosiding, atau penerbit resmi | Nama jurnal lengkap + Akreditasi (SINTA/Scopus) + DOI | Wajib jurnal peer-reviewed terindeks. Dilarang blog pribadi atau artikel tanpa reputasi. |
| **13** | `Tahun Terbit` | Tahun resmi publikasi naskah | Angka tahun 4 digit: `YYYY` (misal: `2023`, `2024`) | Wajib dominan ($\ge 80\%$) diterbitkan dalam kurun waktu 3 (tiga) tahun terakhir. |

---

## 4. Protokol Sintesis: Mengubah Matriks Menjadi Narasi Bab 2.1

Tabel matriks adalah alat komparasi, bukan teks akhir naskah. Penulis wajib mengekstrak tabel menjadi narasi ilmiah Bab 2.1 melalui 6 langkah metodologis berikut:

### Langkah 1: Pemetaan Irisan (*Intersection Mapping*)
Identifikasi keterkaitan antara skripsi saat ini dengan literatur yang dipetakan:
- *Irisan Objek Material:* Artikel mana yang meneliti fenomena empiris serupa tetapi dengan sudut pandang (Objek Formal) berbeda?
- *Irisan Objek Formal:* Artikel mana yang menggunakan teori serupa tetapi diterapkan pada konteks atau objek material berbeda?

### Langkah 2: Taksonomi Celah Penelitian (*Research Gap Taxonomy*)
Berdasarkan Kolom 10 (*Keterbatasan Penelitian*) dan Kolom 11 (*Rekomendasi*), sintesiskan 4 jenis celah pengetahuan:
1. **Empirical Gap:** Fenomena atau kasus empiris baru di lapangan yang belum pernah diamati atau diuji oleh peneliti terdahulu.
2. **Theoretical Gap:** Ruang pembaruan atau ekspansi dari model teoretis yang digunakan dalam literatur sebelumnya (misal: penambahan variabel moderasi/mediasi baru).
3. **Contextual Gap:** Perbedaan dinamika sosial, budaya, geografis, regulasi, atau karakteristik pengguna antara lokus riset terdahulu dengan lokus penelitian saat ini.
4. **Methodological Gap:** Keterbatasan metodologi riset terdahulu (misal: hanya menggunakan data *cross-sectional*, sampel terbatas, ketiadaan triangulasi) yang diperbaiki dalam metodologi skripsi saat ini.

### Langkah 3: Formulasi *State-of-the-Art*
Susun kalimat penegasan batas pencapaian literatur ilmiah mutakhir:
> *"Perkembangan literatur mutakhir mengenai [Objek Material] sebagian besar baru berfokus pada [temuan umum riset terdahulu] dengan menggunakan perspektif [Objek Formal terdahulu], sebagaimana ditunjukkan dalam kajian Pratama (2023) dan Wibowo (2024). Namun demikian, sejauh penelusuran pustaka dilakukan, belum ditemukan kajian yang secara mendalam membedah dinamika [masalah spesifik] pada konteks [Konteks saat ini]."*

### Langkah 4: Pernyataan Posisi Berdiri Peneliti (*Research Positioning*)
Tegaskan posisi berdiri penelitian di antara literatur yang ada:
> *"Berdasarkan peta komparatif tersebut, penelitian ini memposisikan diri untuk mengisi celah kontekstual dan metodologis yang ditinggalkan oleh peneliti sebelumnya dengan menerapkan [Objek Formal saat ini] untuk membedah [Objek Material saat ini] pada [Konteks saat ini]."*

### Langkah 5: Penawaran Gagasan & Orisinalitas (*Novelty Proposition*)
Rumuskan penawaran gagasan orisinal:
> *"Dengan demikian, penelitian ini mengajukan penawaran gagasan berupa [model integratif / proposisi konseptual / solusi sistemik baru] yang secara signifikan berbeda dari riset terdahulu karena menggabungkan [aspek pembeda spesifik]."*

### Langkah 6: Pernyataan Bebas Duplikasi (*Non-Duplication Defense Assertion*)
Pernyataan deklarasi resmi untuk mempertahankan proposal di depan Dosen Penguji dalam sidang:
> *"Berdasarkan penelusuran komparatif terhadap 10 penelitian terdahulu yang paling relevan pada matriks di atas, ditegaskan secara jujur dan objektif bahwa judul dan fokus penelitian ini bukan merupakan duplikasi. Perbedaan fundamental terletak pada kombinasi Objek Formal [sebutkan] dan Objek Material [sebutkan] pada Konteks [sebutkan] yang memiliki karakteristik unik dan belum pernah diselidiki sebelumnya."*

---

## 5. Contoh Nyata Matriks 13 Kolom (Domain: Adopsi Quick Commerce)

Tabel di bawah ini merupakan contoh matriks terisi lengkap berstandar tinggi:

| No | Nama Penulis | Judul Penelitian | Objek Material | Objek Formal | Konteks | Metode | Hasil | Pembahasan Singkat | Simpulan | Keterbatasan Penelitian | Rekomendasi | Penerbit | Tahun Terbit |
|:--:|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:--:|
| 1 | Wibowo, A. & Lestari, S. | "Faktor Pendorong Niat Beli Konsumen pada Layanan Quick Commerce di Kota Metropolitan" | Perilaku belanja instan kebutuhan harian | *Technology Acceptance Model (TAM)* | Konsumen aplikasi Astro di DKI Jakarta (N=210) | Kuantitatif survei, regresi linear berganda | Perceived Usefulness berpengaruh positif signifikan terhadap niat beli (β=0,38; p<0,01) | Temuan mengonfirmasi model TAM pada konteks pengiriman instan | Efisiensi waktu merupakan determinan utama konsumen mengadopsi quick commerce | Sampel homogen kelas menengah perkotaan; tidak menguji faktor biaya kirim | Menyarankan pengujian faktor sensitivitas harga dan perluasan ke kota tier-2 | *Jurnal Distribusi dan Logistik Indonesia*, Vol. 8, No. 2, DOI: 10.22146/jdli.2023.82 | 2023 |
| 2 | Kurniawan, D. | "Analisis Hambatan Logistik Rantai Pasok Mikro pada Layanan Belanja Cepat" | Operasional kurir pengiriman instan belanja harian | *Theory of Planned Behavior (TPB)* | Mitra pengemudi dan hub gudang di Surabaya (N=15 informan) | Kualitatif deskriptif, wawancara mendalam | Keterbatasan stok di dark store lokal sering memicu pembatalan pesanan konsumen | Hambatan kontrol perilaku menurunkan kepuasan mitra logistik | Integrasi data inventaris dark store lebih krusial dibanding kecepatan armada | Penelitian kualitatif tanpa uji signifikansi statistik | Disarankan mengembangkan model integrasi inventaris berbasis peramalan permintaan | *Jurnal Sistem Informasi Bisnis (SINTA 2)*, DOI: 10.21456/jsib.2024.11 | 2024 |
| 3 | Chen, H. & Zhang, Y. | "Impulse Buying and Perceived Urgency in On-Demand Grocery Delivery Platforms" | Pembelian impulsif pada aplikasi e-grocery | *Stimulus-Organism-Response (S-O-R) Framework* | Pengguna platform Dingdong Fresh di Shanghai (N=340) | Kuantitatif, Structural Equation Modeling (PLS-SEM) | Promo kilat (stimulus) memicu perceived urgency (organisme) yang mendorong pembelian impulsif (β=0,45; p<0,001) | Mengonfirmasi S-O-R framework dalam antarmuka digital real-time | Desain antarmuka hitung mundur waktu efektif merangsang transaksi spontan | Tidak memotret budaya belanja kolektif khas masyarakat Asia Tenggara | Perlu studi komparasi lintas budaya pada masyarakat berkembang | *Journal of Retailing and Consumer Services (Scopus Q1)*, DOI: 10.1016/j.jretconser.2024.103 | 2024 |
| *USULAN* | **Peneliti Saat Ini** | **"Pengaruh Stimulus Flash Sale terhadap Keputusan Pembelian Impulsif melalui Pendekatan S-O-R pada Konsumen Quick Commerce di Kota Bandung"** | **Keputusan pembelian impulsif kebutuhan harian** | **Stimulus-Organism-Response (S-O-R) Framework dengan Variabel Moderasi Literasi Finansial** | **Konsumen aplikasi belanja instan di Kota Bandung (N=250)** | **Kuantitatif eksplanatori, SEM-PLS dengan uji efek moderasi multigroup** | *(Akan dibuktikan pada Bab IV)* | *(Akan dibahas secara dialektis pada Bab IV)* | *(Natijah yang ditargetkan)* | *(Mengatasi keterbatasan homogenitas lokasi dan memasukkan literasi finansial)* | *(Memberikan rekomendasi perlindungan konsumen dan strategi platform)* | **Skripsi S1 Universitas X** | **2024** |
