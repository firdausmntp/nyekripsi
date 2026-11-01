---
disable-model-invocation: true
name: skripsi-matriks
description: Nyekripsi 13-column prior literature comparative matrix (Matriks Penelitian Terdahulu) & state-of-the-art gap synthesis
model: sonnet
---

First invoke the Skill tool with `skill: "academic-research-skills:deep-research"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `deep-research` skill to compile the standardized Indonesian undergraduate 13-column prior literature comparative matrix (`Matriks Penelitian Terdahulu`). Enforces the strict 13-column schema:
1. `Nama Penulis`
2. `Judul Penelitian`
3. `Objek Material`
4. `Objek Formal`
5. `Konteks`
6. `Metode`
7. `Hasil`
8. `Pembahasan Singkat`
9. `Simpulan`
10. `Keterbatasan Penelitian`
11. `Rekomendasi`
12. `Penerbit`
13. `Tahun Terbit`

Supports configurable paper counts (5, 10, 15, 20+ studies) as specified by academic advisors. Produces a comprehensive cross-study state-of-the-art synthesis:
- Persamaan & Perbedaan (Commonalities & Methodological Divergence).
- Posisi Penelitian (Current Study Positioning vs Prior Literature).
- Research Gap & Originalitas (Kebaruan Penelitian yang membuktikan signifikansi skripsi).

Arguments & Configuration:
- `--count <5|10|15|20>`: Number of prior studies to analyze (default: 10).
- `--topic "<topic>"`: Core topic / research problem.
- `--objek-material "<phenomenon>"`: Empirical phenomenon focus.
- `--objek-formal "<lens>"`: Theoretical lens focus.
- `--years <3|5>`: Recency window in years (default: 5 years).

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § deep-research.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/deep-research/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
