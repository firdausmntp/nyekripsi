---
disable-model-invocation: true
name: skripsi-proposal
description: Nyekripsi proposal drafting — Bab I (Pendahuluan), Bab II (Kajian Pustaka), Bab III (Metodologi) with Kerangka Berpikir & Matriks
model: sonnet
---

First invoke the Skill tool with `skill: "academic-research-skills:academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `proposal` mode tailored for Indonesian Skripsi Proposal (Seminar Proposal / Sempro). Produces a complete proposal draft encompassing:
- Bab I (Pendahuluan): Latar Belakang Masalah dengan pemisahan tegas Objek Material dan Objek Formal, Identifikasi & Batasan Masalah, Rumusan Masalah (3 RQs berjenjang), Tujuan Penelitian, Manfaat Penelitian (Teoretis, Praktis, Kebijakan).
- Bab II (Kajian Pustaka): Kajian Teori 3 Level (Grand, Middle, Applied), Tinjauan Penelitian Terdahulu (matriks komparatif 13 kolom), Kerangka Berpikir konseptual berbasis diagram Mermaid, Hipotesis Penelitian (Kuantitatif) atau Fokus Eksplanasi (Kualitatif/IT).
- Bab III (Metodologi Penelitian): Desain & Paradigma Penelitian, Populasi & Sampel / Subjek & Informan / Analisis Kebutuhan Sistem, Teknik Pengumpulan Data, Instrumen & Uji Validitas-Reliabilitas, Teknik Analisis Data 3 Tahap.
- Daftar Pustaka Awal: Minimal 80% jurnal bereputasi kemutakhiran 3-5 tahun terakhir format APA 7 atau IEEE.

Supports preset structuring (`it-software`, `sosial-humaniora`, dll.) and formative feedback from Dosen Pembimbing persona (`pembimbing_agent.md`).

Arguments & Configuration:
- `--fakultas <preset>`: Faculty preset selection.
- `--metode <kuantitatif|kualitatif|it-se>`: Methodological paradigm.
- `--judul "<title>"`: Research title.
- `--toc "<custom_toc.md>"`: Optional custom campus outline for proposal.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § academic-paper.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/academic-paper/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
