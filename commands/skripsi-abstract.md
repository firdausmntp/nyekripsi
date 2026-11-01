---
disable-model-invocation: true
name: skripsi-abstract
description: Nyekripsi 5-sentence bilingual abstract (Bahasa Indonesia & English) + alphabetical keywords
model: sonnet
---

First invoke the Skill tool with `skill: "academic-research-skills:academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `abstract-only` mode using language pair `id-en` (Bahasa Indonesia L1 + English L2) registered in `shared/output_language_pair.md`. Generates a strictly compliant undergraduate thesis abstract adhering to `academic-paper/templates/skripsi_bilingual_abstract_template.md`.

Enforces the canonical 5-sentence abstract formula:
- Kalimat 1 (Latar Belakang / Fenomena Empiris): Menjelaskan Objek Material dan permasalahan empiris utama.
- Kalimat 2 (Tujuan Penelitian / Pertanyaan): Menjelaskan Objek Formal dan tujuan utama penelitian.
- Kalimat 3 (Metodologi / Pendekatan): Menjelaskan paradigma/desain, subjek/populasi/sumber data, dan teknik analisis.
- Kalimat 4 (Temuan Kunci / Hasil): Menyajikan hasil analisis utama dan temuan empiris konkret.
- Kalimat 5 (Natijah / Implikasi Epistemik): Menegaskan kontribusi keilmuan, implikasi praktis, dan rekomendasi utama.

Formatting and Keyword Discipline:
- Word Count: 150 - 250 kata per blok bahasa, 1 paragraf tunggal, spasi 1.
- Kata Kunci / Keywords: 3 - 5 kata kunci, disusun **secara alfabetis** (A-Z) pada kedua bahasa.

Arguments & Configuration:
- `--pair id-en`: Language pair (default: `id-en`).
- `--draft "<path_to_draft.md>"`: Source draft or completed thesis chapters.
- `--keywords-count <3-5>`: Number of alphabetical keywords (default: 5).

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § academic-paper.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/academic-paper/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
