---
disable-model-invocation: true
name: skripsi-citation
description: Nyekripsi citation & bibliography audit — APA 6/7, IEEE, Harvard, Chicago, 80% recency ratio & anti-phantom check
---

First invoke the Skill tool with `skill: "academic-research-skills:academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `citation-check` mode tailored for Indonesian undergraduate academic requirements. Audits in-text citations and Daftar Pustaka per `academic-paper/references/skripsi_citation_standards.md`.

Executes four rigorous integrity gates:
1. Bi-directional 100% Matching (Anti-Phantom & Anti-Orphan):
   - Every in-text citation must resolve to an entry in Daftar Pustaka.
   - Every Daftar Pustaka entry must have at least one anchored in-text citation.
   - Zero tolerance for hallucinated/phantom references.
2. Kemutakhiran Pustaka (Recency Verification):
   - At least 80% of cited literature must be peer-reviewed journal articles.
   - Publication year must be within the last 3-5 years (configurable; default: 5 years).
   - Textbooks and classic references permitted only for foundational Grand Theory.
3. Multi-Style Verification:
   - APA 7th edition (author-date) standard.
   - APA 6th edition.
   - IEEE numeric style (`[1]`, `[2]`) for IT and software engineering papers.
   - Harvard & Chicago author-date styles.
4. Bibliographic Surface Form:
   - Sentence case for article titles.
   - Title case and italics for journal/conference names.
   - Validation of DOIs and permanent URLs.

Arguments & Configuration:
- `--style <apa7|apa6|ieee|harvard|chicago>`: Citation style (default: `apa7`).
- `--recency-years <3|5>`: Maximum age for empirical journal references (default: 5).
- `--min-journal-ratio <80>`: Minimum percentage of peer-reviewed journal sources (default: 80).
- `--file "<path_to_draft.md>"`: Markdown draft containing in-text citations and Daftar Pustaka.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § academic-paper.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/academic-paper/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
