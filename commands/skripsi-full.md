---
disable-model-invocation: true
name: skripsi-full
description: Nyekripsi full undergraduate thesis pipeline — research → matriks → proposal → Bab I-V → citation/EYD audit → defense simulation → finalize
---

First invoke the Skill tool with `skill: "academic-research-skills:academic-pipeline"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-pipeline` orchestrator for the complete Indonesian undergraduate thesis workflow (Skripsi S1). Orchestrates the 8-stage thesis writing pipeline:
1. Inisiasi & Formulasi: Perumusan Objek Material, Objek Formal, Konteks, dan Metode. Pemilihan preset fakultas (`it-software`, `sosial-humaniora`, `hukum`, `ekonomi-bisnis`, `pendidikan-r&d`, `kesehatan-sains`, atau `custom`) atau intake custom TOC. Perumusan Dialectical Problem Statement, 3 Research Questions, dan 3 Manfaat Penelitian.
2. Kajian Pustaka Terdahulu: Eksekusi `deep-research` untuk menyusun Matriks Penelitian Terdahulu 13 Kolom (5, 10, 15, atau 20+ artikel jurnal terakreditasi/bereputasi) dan sintesis riset gap.
3. Kerangka Teori: Grand Theory, Middle-Range Theory, dan Applied Theory (pisau analisis) beserta diagram Kerangka Berpikir Mermaid.
4. Proposal & Bab I-III: Penyusunan Bab I (Pendahuluan), Bab II (Kajian Pustaka), dan Bab III (Metodologi Penelitian / Analisis & Desain Sistem). Formative review dengan Dosen Pembimbing.
5. Bab IV-V: Hasil Penelitian, Pembahasan 3 Arah (triangulasi data, teori, dan studi terdahulu), serta Kesimpulan & Natijah Epistemik.
6. Audit Kepatuhan: Audit sitasi APA 7 / IEEE ([1], [2]) dengan verifikasi kemutakhiran 80% (< 3-5 tahun), anti-phantom citation, dan audit bahasa EYD V.
7. Simulasi Sidang (Defense): Evaluasi komprehensif Dosen Penguji menggunakan 5 dimensi rubrik dan penerbitan 4 status putusan sidang.
8. Finalisasi: Matriks revisi, abstrak bilingual 5 kalimat (id-en), dan penyiapan berkas naskah lengkap.

Arguments & Configuration:
- `--fakultas <preset>`: Faculty preset (`it-software`, `sosial-humaniora`, `hukum`, `ekonomi-bisnis`, `pendidikan-r&d`, `kesehatan-sains`, `custom`).
- `--metode <kuantitatif|kualitatif|it-se>`: Research paradigm.
- `--judul "<proposed title>"`: Tentative research title.
- `--objek-material "<empirical phenomenon>"`: Empirical phenomenon / problem domain.
- `--objek-formal "<theoretical lens>"`: Theory / perspective used to analyze.
- `--toc "<custom_toc.md>"`: Optional university specific thesis guide outline.
- `--citation-style <apa7|ieee|harvard|chicago>`: Citation style (default: `apa7`, IT: `ieee`).

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § academic-pipeline.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/academic-pipeline/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
