---
disable-model-invocation: true
name: skripsi-bab
description: Nyekripsi chapter-by-chapter drafting (Bab I - Bab V, classical & IT/SE variants, custom campus TOC)
model: sonnet
---

First invoke the Skill tool with `skill: "academic-research-skills:academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in chapter drafting mode for Indonesian undergraduate theses. Drafts or revises a designated chapter (Bab 1 through Bab 5) with full subsection depth and faculty alignment:
- Bab 1 (Pendahuluan): Dialectical problem statement `terdapat...`, Objek Material & Formal, 3 RQs, 3-tier benefits.
- Bab 2 (Kajian Pustaka): 3-level theory hierarchy (Grand, Middle, Applied), prior research matrix, Mermaid Kerangka Berpikir.
- Bab 3:
  * Klasik (Metodologi): Desain, instrumen, populasi/sampel atau subjek/informan, 3-stage data analysis.
  * IT / SE (Analisis & Desain Sistem): Kebutuhan fungsional/non-fungsional, Mermaid UML (use case, activity, sequence, class diagrams), arsitektur sistem.
- Bab 4:
  * Klasik (Hasil & Pembahasan): Penyajian data, uji hipotesis / temuan kualitatif, 3-way discussion (data vs teori vs studi terdahulu).
  * IT / SE (Implementasi & Pengujian): Lingkungan implementasi, antarmuka, pengujian black-box, UAT, System Usability Scale (SUS).
- Bab 5:
  * Klasik (Kesimpulan & Saran): Epistemic natijah, implikasi teoritis & praktis, saran operasional.
  * IT / SE (Penutup): Kesimpulan ketercapaian fitur sistem, keterbatasan sistem, saran pengembangan lanjutan.
- Custom TOC: Dynamic alignment when a university handbook outline is supplied via `--toc`.

Arguments & Configuration:
- `--bab <1|2|3|4|5>`: Target chapter number (mandatory).
- `--fakultas <preset>`: Faculty preset (`it-software`, `sosial-humaniora`, etc.).
- `--tipe <klasik|it-se|custom>`: Chapter structure variant.
- `--toc "<custom_toc.md>"`: Path to custom campus table of contents.
- `--draft "<existing_draft.md>"`: Optional existing chapter draft for revision.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § academic-paper.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/academic-paper/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
