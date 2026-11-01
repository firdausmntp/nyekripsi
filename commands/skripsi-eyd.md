---
disable-model-invocation: true
name: skripsi-eyd
description: Nyekripsi EYD V academic Indonesian language audit — SPOK syntax, di-/ke- morphology, cliches, academic vocabulary
model: sonnet
---

First invoke the Skill tool with `skill: "academic-research-skills:academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in academic language audit mode per Pedoman Umum Ejaan Bahasa Indonesia Edisi V (EYD V) and `academic-paper/references/eyd_v_pedoman.md`.

Audits thesis prose across 5 linguistic and stylistic dimensions:
1. Struktur Kalimat Efektif & SPOK:
   - Memastikan kejelasan Subjek dan Predikat di setiap kalimat.
   - Mengeliminasi kalimat menggantung/anak kalimat tanpa induk (contoh: "Sehingga penelitian ini...", "Meskipun hal tersebut...").
2. Morfologi Prefiks vs Preposisi (`di-` dan `ke-`):
   - Prefiks kata kerja pasif wajib dirangkai (`dilakukan`, `dikembangkan`, `dianalisis`).
   - Preposisi penunjuk arah/tempat wajib dipisah (`di lapangan`, `di laboratorium`, `ke depan`).
3. Eliminasi Frasa Klise & Tidak Baku:
   - Melarang kata sambung tidak baku dalam posisi anak kalimat (penggunaan "...di mana...", "...yang mana...").
   - Menghapus amplifikasi subjektif tanpa bukti empiris ("sangat penting sekali", "amat luar biasa").
   - Memperbaiki pembuka kesimpulan klise ("Dapat disimpulkan bahwa...").
4. Kosakata Baku Akademik (KBBI V):
   - Koreksi otomatis kata serapan tidak baku: `analisis` (bukan analisa), `metode` (bukan metoda), `kualitas` (bukan kualitet), `hipotesis` (bukan hipotesa), `sistematis` (bukan sistimatis), `objektif` (bukan obyektif).
5. Tipografi & Pungtuasi Akademis:
   - Huruf miring (italic) untuk semua istilah asing/daerah yang belum diserap.
   - Huruf kapital untuk entitas formal skripsi (Bab I, Tabel 4.1, Gambar 2.2).
   - Ketepatan tanda koma sebelum konjungsi intrakalimat (`sedangkan`, `melainkan`, `yaitu`).

Arguments & Configuration:
- `--file "<path_to_draft.md>"`: Draft file to audit (mandatory).
- `--mode <audit|autofix>`: Report violations only, or produce corrected draft (default: `audit`).
- `--report "<output_path.md>"`: Destination path for EYD audit report.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § academic-paper.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/academic-paper/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
