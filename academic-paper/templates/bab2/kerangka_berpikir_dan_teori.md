# PANDUAN KERANGKA BERPIKIR & TEORI 3 LEVEL (BAB II)

---

## 1. Hierarki Teori 3 Level
Jangan menumpuk teori tanpa korelasi fungsional. Strukturkan teori Anda ke dalam 3 tingkatan:

```mermaid
graph TD
    GT["1. GRAND THEORY<br/>(Teori Payung / Fundamental)<br/>Contoh: Resource-Based View / TAM / SWEBOK"]
    --> MT["2. MIDDLE-RANGE THEORY<br/>(Teori Penghubung / Konstruk Spesifik)<br/>Contoh: Perceived Ease of Use / Agility Framework"]
    --> AT["3. APPLIED / OPERATIONAL THEORY<br/>(Pisau Analisis Langsung / Indikator Operasional)<br/>Contoh: Kuisioner Skala Likert / Uji Black-Box Equivalence Partitioning"]
```

---

## 2. Scaffold Diagram Kerangka Berpikir (Mermaid)

Gunakan template diagram Mermaid berikut untuk Sub-Bab 2.3:

```mermaid
flowchart TD
    subgraph MasalahEmpiris ["Problematika Empiris (Objek Material)"]
        M1["Kondisi Nyata Lapangan (Das Sein)"]
        M2["Anomali / Friksi / Hambatan Sistem"]
    end

    subgraph LandasanTeori ["Pisau Analisis & Landasan Teori (Objek Formal)"]
        T1["Grand Theory: [Nama Teori]"]
        T2["Middle Theory: [Nama Teori]"]
        T3["Applied Theory: [Nama Teori / Algoritma]"]
    end

    subgraph SolusiIntervensi ["Intervensi Metodologis"]
        S1["Pengujian Empiris / Perancangan Sistem"]
        S2["Analisis Kausalitas / Implementasi Modul"]
    end

    subgraph LuaranHasil ["Luaran & Kontribusi (Bab 4 & 5)"]
        H1["Temuan Teruji / Sistem Tervalidasi"]
        H2["Rekomendasi Kebijakan / Peningkatan Performa"]
    end

    MasalahEmpiris --> LandasanTeori
    LandasanTeori --> SolusiIntervensi
    SolusiIntervensi --> LuaranHasil
```
