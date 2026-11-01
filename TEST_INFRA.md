# Test Infrastructure Architecture — nyekripsi

## 1. Executive Summary & Philosophy
`nyekripsi` employs a dual-track, zero-dependency testing architecture designed to enforce Indonesian academic standards, university guideline flexibility, and mathematical rigors across the entire research writing pipeline.

### Core Architecture Principles:
1. **Zero External Runtime Dependencies**: All test runners, linters, and verification suites execute entirely on the Python Standard Library (`unittest`, `subprocess`, `re`, `json`, `argparse`, `math`, `pathlib`). This guarantees immediate execution on Linux, Termux / Android, macOS, and standard minimal CI environments.
2. **Multi-Tier Verification Pyramid**: Verification is organized into 5 progressive tiers:
   - **Tier 1: Static Linters & Repository Invariants** (Fast, deterministic contract enforcement, schema & manifest synchronization).
   - **Tier 2: Algorithmic Unit Tests** (Domain-specific mathematical checks, operational definitions, regex AST parsing).
   - **Tier 3 & Tier 4: Real-World E2E Thesis Workloads** (Multi-phase undergraduate thesis lifecycle simulations).
   - **Tier 5: Adversarial Stress Testing & Coverage Hardening** (Extreme boundary math, malformed inputs, edge-case citation strings).
3. **Strict Bi-directional Traceability**: Every feature (F1–F17) defined in `PROJECT.md` is explicitly covered by deterministic test assertions.

---

## 2. The 5-Tier Verification Pyramid

```
                      / \
                     /   \
                    /  5  \    Tier 5: Adversarial Stress Testing
                   /-------\
                  /    4    \   Tier 4: Real-World Thesis Workloads
                 /-----------\
                /      3      \  Tier 3: Multi-Stage Integration Harness
               /---------------\
              /        2        \ Tier 2: Algorithmic Unit Tests (124 tests)
             /-------------------\
            /          1          \ Tier 1: Static Linters & Invariants (13 targets)
           /-----------------------\
```

### Tier 1: Static Linters & Repository Invariants
Tier 1 ensures that the repository remains stable, manifests stay synchronized, commands obey Claude plugin invariants, and agent write boundaries are enforced deterministically:
1. `scripts/check_command_frontmatter_name.py`: Verifies all 24 slash commands have valid YAML frontmatter matching filename stem (#633).
2. `scripts/check_command_skill_dispatch.py`: Verifies all 21 mode commands invoke skills with rooted references `${CLAUDE_PLUGIN_ROOT}` (#857).
3. `tools/release-discipline/scripts/check_command_invariants.py`: Enforces token synchronization across `.command-invariants.toml` and announce scripts.
4. `scripts/check_agents_mirror_sync.py`: Asserts byte-identical mirroring between source agent definitions and plugin-exposed `agents/` (#413).
5. `scripts/check_v3_10_134_write_scope.py`: Verifies Bucket A agent write rosters and Bucket B/C/D exemptions.
6. `scripts/check_v3_9_2_phase_boundary.py`: Verifies phase boundary instruction tags on Bucket A agents.
7. `scripts/check_model_tiering.py`: Enforces classification of 45 agents into 31 judgment and 14 execution tiers.
8. `scripts/check_distribution_surface_claims.py`: Asserts distribution surface claims stay strictly within evidence records.
9. `scripts/check_version_consistency.py`: Enforces version synchronization across `package.json`, `plugin.json`, and documentation.
10. `scripts/check_spec_consistency.py`: Validates cross-links and document consistency.
11. `scripts/check_ci_pytest_manifest.py`: Validates CI manifest integrity (183 targets).
12. `scripts/check_preprint_venues_consistency.py`: Synchronizes preprint venue lists across bibliography agents.
13. `scripts/test_ars_write_scope_guard.py`: 71 unit tests validating deterministic PreToolUse write interception and dual namespace support (`nyekripsi:`).

### Tier 2: Algorithmic Unit Tests
Tier 2 validates domain-specific logic, operational structures, and mathematical formulas:
1. `tests/test_skripsi_m1_core.py` (44 tests):
   - Epistemological definitions of Objek Material vs Objek Formal and title formula (F1).
   - Standard 5-chapter templates (Bab 1–5), IT/SE templates (Bab 3–4), dialectical problem statements, 3 RQs, 3-tier benefits, 3-stage data analysis, 3-way discussion, and epistemic natijah (F2).
   - Three-level theory hierarchy (Grand, Middle-Range, Applied/Operational Theory) (F3).
   - 13-column comparative literature matrix template (F4).
   - 5-sentence structured bilingual abstract with alphabetical keywords (F5).
   - Multi-style citation guidelines (APA 6/7, IEEE, Harvard, Chicago) (F6).
   - EYD V academic Indonesian language rules (SPOK, prefix `di-` vs `di `, banned clichés) (F7).
2. `tests/test_skripsi_m1_adversarial.py` (14 tests):
   - Citation & recency math boundary values (80% journal ratio, 3–5 year recency) (F6).
   - Anti-phantom forward and reverse audit algorithms (F6).
   - Multi-style citation boundary testing (APA vs IEEE) (F6).
   - Mermaid diagram AST validation in Markdown templates (F15).
3. `tests/test_skripsi_m2_methodologies.py` (35 tests):
   - Quantitative sampling formulas (Slovin, Isaac-Michael) and classical assumption tests (F8).
   - Qualitative Yin case study protocols, triangulation matrices, and coding stages (F9).
   - IT & Software Engineering SDLC models, MoSCoW, FURPS+, UML Mermaid, and SUS calculation (F10, F15).
   - Universal Faculty Presets schema, 7 presets, and chapter mappings (F16).
4. `tests/test_skripsi_m3_commands_agents.py` (31 tests):
   - 8 `/skripsi-*` commands registration, frontmatter, and skill dispatch (F11).
   - Dosen Pembimbing and Dosen Penguji personas, 5-dimension defense rubrics, and 4 verdicts (F12).
   - Package rebranding and dual namespace compatibility (F13).
   - Custom TOC intake engine CLI and archetype mapping (F17).

### Tier 3 & Tier 4: Real-World E2E Thesis Workload Scenarios
`tests/test_skripsi_e2e_workloads.py` simulates 5 complete end-to-end undergraduate thesis lifecycles:
1. **Scenario 1: IT / Software Engineering Skripsi Lifecycle** (`it-software`): Proposal -> Bab 1–5 (IT variant: Bab 3 Analisis & Desain, Bab 4 Implementasi & Pengujian) -> Mermaid Architecture & Sequence Diagrams -> MoSCoW & FURPS+ -> Black Box & SUS calculation -> IEEE citation formatting -> Defense simulation.
2. **Scenario 2: Quantitative Empirical Skripsi Lifecycle** (`ekonomi-bisnis` / `sosial-humaniora`): Slovin sample calculation -> Panel Regression (CEM/FEM/REM) -> Classical Assumptions (BLUE) -> APA 7 citation recency ratio (>= 80% < 5 yrs) -> Dosen Pembimbing review.
3. **Scenario 3: Qualitative Descriptive/Case Study Skripsi Lifecycle** (`sosial-humaniora` / `hukum`): Yin Case Study / Legal Normatif -> Triangulation matrix -> Informant profiling -> Content analysis / framing -> EYD V compliance audit -> Dosen Pembimbing guidance.
4. **Scenario 4: Educational R&D / Clinical Health Skripsi Lifecycle** (`pendidikan-r&d` / `kesehatan-sains`): ADDIE/4D model -> N-Gain calculation -> 13-column prior research matrix (10 studies) -> 5-sentence bilingual abstract generation with alphabetical keywords.
5. **Scenario 5: Custom Campus Table of Contents Intake & Dynamic Adaptation** (`custom`): Non-standard university guideline intake via `scripts/custom_toc_intake.py` -> Semantic chapter archetype mapping -> Verification against schema -> Dosen Penguji defense evaluation with 5-dimension weighted scoring and binding verdict.

### Tier 5: Adversarial Stress Testing & Coverage Hardening
`tests/test_skripsi_m4_adversarial.py` tests edge cases and stress vectors:
- Custom TOC intake edge cases (Roman numerals beyond XII, markdown bullet chapters, spaceless headings, dot trails without page numbers).
- Slovin formula extreme populations ($N=1$, $N=1,000,000$) and tolerances ($e=0.01$, $e=0.20$).
- SUS score computation with boundary scores (all 1s, all 5s, all 3s = 50.0).
- N-Gain handling of division by zero ($Post = Pre = 100$) and negative gains.
- APA 7 vs IEEE numeric citation cross-style contamination and hidden phantoms in footnotes/tables.
- EYD V morpho-syntactic rules (merged prepositions `dimana`, separated verbs `di lakukan`, proper noun hyphenation `di-Indonesia-kan`, `ke-21`).
- Mermaid AST validation for complex multi-tier architectures and corruption rejection.

---

## 3. Unified Test Runner (`scripts/run_skripsi_tests.py`)

### Usage:
```bash
# Run all tiers (Tier 1 through Tier 5)
python3 scripts/run_skripsi_tests.py

# Run specific tier
python3 scripts/run_skripsi_tests.py --tier 1  # Static linters
python3 scripts/run_skripsi_tests.py --tier 2  # Unit tests
python3 scripts/run_skripsi_tests.py --tier 3  # E2E workloads
python3 scripts/run_skripsi_tests.py --tier 5  # Adversarial stress

# Run with verbose output and generate JSON report
python3 scripts/run_skripsi_tests.py -v --json-report test_report.json

# Fail fast on first error
python3 scripts/run_skripsi_tests.py -x
```

### Exit Codes:
- `0`: 100% of executed targets and tests passed cleanly.
- `1`: One or more tests, linters, or invariant checks failed.
- `2`: Invalid CLI arguments.

---

## 4. Feature Traceability Matrix (F1–F17)

| Feature ID | Feature Name | Primary Test Suite | Key Test Methods / Classes |
|---|---|---|---|
| **F1** | Objek Material & Objek Formal | `tests/test_skripsi_m1_core.py` | `TestObjekMaterialFormalGuide.test_epistemological_definitions`, `test_title_formula_enforcement` |
| **F2** | Flexible Indonesian Chapter Structures | `tests/test_skripsi_m1_core.py` | `TestSkripsiBabTemplates.test_classical_five_chapters_exist`, `test_it_se_variant_chapters_exist`, `test_dialectical_problem_statement` |
| **F3** | Three-Level Theory Hierarchy | `tests/test_skripsi_m1_core.py` | `TestTeoriTigaLevelGuide.test_theory_hierarchy_levels`, `test_dimension_reduction_matrix` |
| **F4** | Configurable 13-Column Prior Matrix | `tests/test_skripsi_m1_core.py`, `test_skripsi_m1_adversarial.py` | `TestMatriksPenelitianTerdahuluTemplate.test_thirteen_columns_present`, `TestMatrixConfigurableScalability.test_paper_count_scaling` |
| **F5** | 5-Sentence Bilingual Abstract & Keywords | `tests/test_skripsi_m1_core.py` | `TestSkripsiBilingualAbstractTemplate.test_five_sentence_structure`, `test_alphabetical_keywords` |
| **F6** | Multi-Style Citation & Recency Standards | `tests/test_skripsi_m1_core.py`, `test_skripsi_m1_adversarial.py` | `TestSkripsiCitationStandardsGuide.test_apa_and_ieee_specifications`, `TestCitationRecencyMathBoundaries.test_eighty_percent_ratio`, `TestAntiPhantomCitationAudit` |
| **F7** | EYD V Academic Language Standards | `tests/test_skripsi_m1_core.py` | `TestEydVPedomanGuide.test_spok_structure`, `test_prefix_vs_preposition_di`, `test_prohibited_cliches` |
| **F8** | Quantitative Methodology Module | `tests/test_skripsi_m2_methodologies.py` | `TestMetodologiKuantitatifGuide.test_paradigms_and_typologies`, `test_slovin_and_sample_formulas`, `test_classical_assumptions_blue` |
| **F9** | Qualitative Methodology Module | `tests/test_skripsi_m2_methodologies.py` | `TestMetodologiKualitatifGuide.test_yin_case_study_protocol`, `test_triangulation_matrix_structure`, `test_coding_stages` |
| **F10** | IT & Software Engineering Module | `tests/test_skripsi_m2_methodologies.py` | `TestMetodologiItSeGuide.test_sdlc_models`, `test_moscow_and_furps`, `test_sus_scoring_formula` |
| **F11** | Skripsi Commands (`/skripsi-*`) | `tests/test_skripsi_m3_commands_agents.py` | `TestSkripsiCommandsDiscoveryAndFrontmatter.test_all_8_skripsi_commands_exist`, `test_skripsi_commands_frontmatter_invariants` |
| **F12** | Academic Personas (Pembimbing & Penguji) | `tests/test_skripsi_m3_commands_agents.py` | `TestSkripsiAgentPersonasAndMirroring.test_agent_files_exist_and_mirrored`, `test_penguji_rubric_dimensions_and_weights` |
| **F13** | Rebranding & Package Configuration | `tests/test_skripsi_m3_commands_agents.py` | `TestRebrandingAndReleaseInvariants.test_package_json_rebranding`, `test_announce_script_lists_all_24_commands` |
| **F14** | Comprehensive E2E Test Suite | `scripts/run_skripsi_tests.py`, `tests/test_skripsi_e2e_workloads.py` | Multi-tier runner execution, Scenario 1–5 test classes |
| **F15** | Mermaid Diagram Standardization | `tests/test_skripsi_m1_adversarial.py`, `tests/test_skripsi_m2_methodologies.py` | `TestMermaidDiagramSyntaxInTemplates.test_valid_mermaid_syntax_blocks`, `TestMetodologiItSeGuide.test_uml_mermaid_diagrams` |
| **F16** | Universal Faculty Presets | `tests/test_skripsi_m2_methodologies.py` | `TestFakultasPresetsGuide.test_all_seven_faculty_presets_defined`, `test_faculty_specific_chapter_mappings` |
| **F17** | Custom Chapter Configuration Intake | `tests/test_skripsi_m3_commands_agents.py` | `TestCustomTocIntakeEngine.test_clean_section_title`, `test_classify_archetype_semantic`, `test_parse_raw_text_outline_indonesian_word_numbers` |

---

## 5. CI/CD Integration

To run E2E verification in GitHub Actions without third-party pip dependencies:

```yaml
name: nyekripsi E2E Verification
on: [push, pull_request]

jobs:
  e2e-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run Unified Skripsi Test Suite
        run: python3 scripts/run_skripsi_tests.py --verbose --json-report test_report.json
      - name: Archive Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-test-report
          path: test_report.json
```
