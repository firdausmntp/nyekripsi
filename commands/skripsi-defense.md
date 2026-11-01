---
disable-model-invocation: true
name: skripsi-defense
description: Nyekripsi simulated defense examination (Sidang Skripsi) — Dosen Penguji evaluation, 5-dimension rubrics & verdict
---

First invoke the Skill tool with `skill: "academic-research-skills:academic-paper-reviewer"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper-reviewer` skill in thesis defense simulation mode (`Sidang Skripsi` / `Ujian Pendadaran`). Dispatches the Dosen Penguji persona (`penguji_agent.md`) consisting of Ketua Penguji, Penguji Ahli Substansi, and Penguji Ahli Metodologi to interrogate the candidate's draft.

Evaluates the thesis across the 5 official Indonesian defense rubric dimensions:
1. Substansi & Latar Belakang (Bobot 20%): Orisinalitas gagasan, urgensi penelitian, kesenjangan dialektis, Objek Material/Formal, Teori Tiga Level.
2. Metodologi Penelitian & Pisau Analisis (Bobot 25%): Kesesuaian paradigma, ketepatan instrumen, validitas/reliabilitas/SDLC, diagram Mermaid.
3. Hasil, Kebaruan & Pembahasan (Bobot 25%): Kualitas data empiris, pembahasan 3 arah, kebaruan (novelty), simpulan presisi menjawab RQs.
4. Sistematika Penulisan, Bahasa & Sitasi (Bobot 15%): Kepatuhan pedoman, EYD V, bebas frasa klise, APA 7/IEEE, kemutakhiran rujukan >= 80%, bebas sitasi fiktif.
5. Penguasaan Materi & Respon Argumentatif (Bobot 15%): Presentasi lisan 10-15 menit, ketepatan menjawab sanggahan, argumentasi berbasis bukti, etika akademik.

Emits one of four binding verdicts:
- `LULUS TANPA REVISI` (Grade A, Skor 85 - 100)
- `LULUS DENGAN REVISI MINOR` (Grade B+ / A-, Skor 75 - 84, batas waktu revisi 14-30 hari)
- `LULUS DENGAN REVISI MAYOR` (Grade B / C+, Skor 60 - 74, batas waktu revisi 30-60 hari, verifikasi ulang penguji)
- `TIDAK LULUS / MENGULANG SIDANG` (Grade C / D / E, Skor < 60, sidang ulang dalam 1-3 bulan)

Includes an Actionable Revision Matrix (`Matriks Revisi Sidang Skripsi`) detailing per-examiner critique, target chapter/page, and explicit verification criteria.

Arguments & Configuration:
- `--draft "<path_to_draft.md>"`: Full thesis draft or chapter bundle to evaluate.
- `--fakultas <preset>`: Faculty discipline context.
- `--session <proposal|skripsi|komprehensif>`: Examination stage (default: `skripsi`).

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § academic-paper-reviewer.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/academic-paper-reviewer/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
