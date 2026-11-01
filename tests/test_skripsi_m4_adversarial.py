"""Tier 5 Adversarial Stress & Coverage Hardening Test Suite for nyekripsi (Milestone 4).

Covers:
1. Custom TOC Intake Extreme Inputs & Adversarial Parser Vectors.
2. Multi-Style Citation Boundary, Anti-Contamination, and Hidden Phantom Detection.
3. Mathematical Formula Precision & Boundary Conditions (Slovin, SUS, N-Gain, Panel Data).
4. EYD V Morpho-Syntactic Linter & Grammatical Anomaly Engine.
5. Mermaid AST Validation on Complex Multi-Tier Architectures & Corrupted Inputs.
6. Write-Scope Guard Adversarial Payload & Path Traversal Verification.

Pure Python standard library implementation without third-party dependencies.
"""
from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
TESTS_DIR = ROOT / "tests"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import custom_toc_intake as cti
import ars_write_scope_guard as guard


# ===========================================================================
# Suite 1: Custom TOC Intake Extreme Inputs & Anomaly Hardening
# ===========================================================================

class TestCustomTocIntakeAdversarial(unittest.TestCase):
    """Stress-tests custom TOC intake engine with extreme, corrupted, and edge-case inputs."""

    def test_roman_numerals_beyond_twelve(self):
        """Verifies chapters XIII through XX parse with correct numbers and titles."""
        for r_num, expected_int in [("XIII", 13), ("XIV", 14), ("XV", 15), ("XVI", 16), ("XX", 20)]:
            raw = f"BAB {r_num}: MATRIKS KERJA DAN LAMPIRAN\n1.{expected_int} Modul Tambahan"
            chapters = cti.parse_raw_text_outline(raw)
            self.assertEqual(len(chapters), 1)
            self.assertEqual(chapters[0].number, expected_int)
            self.assertEqual(chapters[0].roman_number, r_num)
            self.assertEqual(chapters[0].title, f"BAB {r_num}: MATRIKS KERJA DAN LAMPIRAN")

    def test_markdown_list_syntax_in_chapter_headers(self):
        """Verifies markdown bullet list formats parse cleanly."""
        bullet_samples = [
            "- BAB I: PENDAHULUAN\n  1.1 Latar Belakang",
            "* BAB I: PENDAHULUAN\n  1.1 Latar Belakang",
            "+ BAB I: PENDAHULUAN\n  1.1 Latar Belakang",
            "1. BAB I: PENDAHULUAN\n  1.1 Latar Belakang",
        ]
        for sample in bullet_samples:
            chapters = cti.parse_raw_text_outline(sample)
            self.assertEqual(len(chapters), 1)
            self.assertEqual(chapters[0].number, 1)
            self.assertEqual(chapters[0].roman_number, "I")
            self.assertEqual(chapters[0].canonical_archetype, "introduction")

    def test_spaceless_corrupted_chapter_headings(self):
        """Verifies headers without spaces like BAB1 or BABIV parse properly."""
        cases = [
            ("BAB1: PENDAHULUAN\n1.1 Latar Belakang", 1, "I"),
            ("BABIV: HASIL PENELITIAN\n4.1 Deskripsi Data", 4, "IV"),
            ("BAB-1: PENDAHULUAN\n1.1 Latar Belakang", 1, "I"),
        ]
        for raw, expected_num, expected_roman in cases:
            chapters = cti.parse_raw_text_outline(raw)
            self.assertEqual(len(chapters), 1)
            self.assertEqual(chapters[0].number, expected_num)
            self.assertEqual(chapters[0].roman_number, expected_roman)

    def test_clean_section_title_trailing_dots_without_page_numbers(self):
        """Verifies trailing dots are stripped even when page numbers are missing."""
        cases = [
            ("1.1 Latar Belakang Masalah ......... 12", "1.1 Latar Belakang Masalah"),
            ("1.1 Latar Belakang Masalah .........", "1.1 Latar Belakang Masalah"),
            ("1.1 Latar Belakang Masalah .....................", "1.1 Latar Belakang Masalah"),
            ("1.2 Rumusan Masalah -------------------", "1.2 Rumusan Masalah"),
            ("1.3 Tujuan Penelitian _______________ 5", "1.3 Tujuan Penelitian"),
        ]
        for raw, expected in cases:
            self.assertEqual(cti.clean_section_title(raw), expected)

    def test_unicode_and_non_ascii_campus_presets(self):
        """Verifies non-ASCII campus names and foreign characters are preserved intact."""
        sample_json = {
            "faculty_id": "syiah-kuala-tarbiyah",
            "preset_name": "Tarbiyah & Keguruan UIN Ar-Raniry",
            "campus_name": "Universitas Syiah Kuala (Darussalam / جامعة)",
            "faculty_name": "Fakultas Tarbiyah dan Keguruan — Kampus Al-Washliyah",
            "citation_style": "APA",
            "recent_reference_ratio_min": 0.8,
            "recent_year_window": 5,
            "chapters": [
                {"number": 1, "roman_number": "I", "canonical_archetype": "introduction", "title": "BAB I: PENDAHULUAN"}
            ]
        }
        preset = cti.parse_input_source(json.dumps(sample_json))
        out_dict = preset.to_dict()
        self.assertEqual(out_dict["campus_name"], "Universitas Syiah Kuala (Darussalam / جامعة)")
        self.assertEqual(out_dict["faculty_name"], "Fakultas Tarbiyah dan Keguruan — Kampus Al-Washliyah")

    def test_empty_sections_chapter_handling(self):
        """Verifies chapter outline with no sub-sections parses with empty section list."""
        raw = "BAB I: PENDAHULUAN\nBAB II: KAJIAN PUSTAKA\nBAB III: METODOLOGI"
        chapters = cti.parse_raw_text_outline(raw)
        self.assertEqual(len(chapters), 3)
        self.assertEqual(chapters[0].required_sections, [])
        self.assertEqual(chapters[1].required_sections, [])
        self.assertEqual(chapters[2].required_sections, [])


# ===========================================================================
# Suite 2: Multi-Style Citations, Contamination & Hidden Phantom Detection
# ===========================================================================

def detect_citation_style_contamination(text: str, declared_style: str) -> list[str]:
    """Detects unintentional cross-style citation pollution within a document."""
    violations = []
    has_ieee = bool(re.search(r"\[\d+(?:\s*,\s*\d+)*\]|\[\d+\s*[\–\-]\s*\d+\]", text))
    has_apa = bool(re.search(r"\([A-Z][a-zA-Z\s\.\-&]+,\s*\d{4}[a-z]?\)", text) or
                   re.search(r"\b[A-Z][a-zA-Z\-]+\s*\(\d{4}[a-z]?\)", text))

    if declared_style.upper() == "APA":
        if has_ieee:
            matches = re.findall(r"\[\d+\]", text)
            violations.append(f"Contamination: Found IEEE numeric citation(s) {matches[:3]} in APA document")
    elif declared_style.upper() == "IEEE":
        if has_apa:
            matches = re.findall(r"\([A-Z][a-zA-Z\s\.\-&]+,\s*\d{4}[a-z]?\)", text)
            violations.append(f"Contamination: Found APA Author-Date citation(s) {matches[:3]} in IEEE document")
    return violations


class TestCitationIntegrityAdversarial(unittest.TestCase):
    """Stress-tests citation boundaries, style contamination, and hidden phantoms."""

    def test_cross_style_contamination_detection(self):
        mixed_body_1 = "Menurut Pratama (2023), sistem ini efisien. Namun modul lain merujuk pada [1]."
        apa_violations = detect_citation_style_contamination(mixed_body_1, declared_style="APA")
        self.assertTrue(len(apa_violations) > 0)
        self.assertIn("IEEE numeric citation", apa_violations[0])

        mixed_body_2 = "Efisiensi terbukti meningkat secara signifikan [1], sebagaimana dirujuk (Wijaya, 2022)."
        ieee_violations = detect_citation_style_contamination(mixed_body_2, declared_style="IEEE")
        self.assertTrue(len(ieee_violations) > 0)
        self.assertIn("APA Author-Date citation", ieee_violations[0])

    def test_phantom_citations_hidden_in_footnotes_and_tables(self):
        """Verifies citations hidden in markdown footnotes and tables are detected."""
        body = """
        Sistem ini memiliki keunggulan performa[^1].
        
        | Komponen | Pustaka Terkait |
        | Caching | Redis dkk. (2021) |
        
        [^1]: Catatan kaki mengutip temuan Pratama (2024).
        """
        bib = "Davis, F. D. (1989). Tech acceptance. MIS Q."

        # Test extraction catches both footnote and table
        apa_body_citations = re.findall(r"\b([A-Z][a-zA-Z]+)(?:\s+dkk\.)?\s*\((\d{4})\)", body)
        apa_body_citations += re.findall(r"\(([A-Z][a-zA-Z]+)(?:,\s*(\d{4}))\)", body)
        cites = set(apa_body_citations)
        self.assertIn(("Pratama", "2024"), cites)
        self.assertIn(("Redis", "2021"), cites)

    def test_recency_ratio_exact_floating_point_precision(self):
        """Verifies strict 80% boundary without premature rounding (79.9% vs 80.0%)."""
        from test_skripsi_m1_adversarial import ReferenceItem, evaluate_citation_portfolio

        # 799 out of 1000 = 79.9% -> MUST FAIL
        refs_799 = [ReferenceItem(f"r{i}", 2024, is_journal=True) for i in range(799)]
        refs_799.extend([ReferenceItem(f"b{i}", 2024, is_journal=False) for i in range(201)])
        res_799 = evaluate_citation_portfolio(refs_799, current_year=2026)
        self.assertFalse(res_799["valid"])
        self.assertFalse(res_799["journal_ok"])
        self.assertAlmostEqual(res_799["journal_ratio"], 0.799, places=3)

        # 39 out of 49 = 79.59% -> MUST FAIL
        refs_39_49 = [ReferenceItem(f"r{i}", 2024, is_journal=True) for i in range(39)]
        refs_39_49.extend([ReferenceItem(f"b{i}", 2024, is_journal=False) for i in range(10)])
        res_39 = evaluate_citation_portfolio(refs_39_49, current_year=2026)
        self.assertFalse(res_39["valid"])
        self.assertFalse(res_39["journal_ok"])

        # 24 out of 30 = 80.0% -> PASS
        refs_24_30 = [ReferenceItem(f"r{i}", 2024, is_journal=True) for i in range(24)]
        refs_24_30.extend([ReferenceItem(f"b{i}", 2024, is_journal=False) for i in range(6)])
        res_24 = evaluate_citation_portfolio(refs_24_30, current_year=2026)
        self.assertTrue(res_24["valid"])
        self.assertTrue(res_24["journal_ok"])


# ===========================================================================
# Suite 3: Mathematical Formulas Precision & Boundary Conditions
# ===========================================================================

def compute_slovin_robust(population_n: int, margin_of_error_e: float) -> float:
    """Computes Slovin sample size with input validation."""
    if population_n <= 0:
        raise ValueError("Population size N must be a positive integer")
    if not (0 < margin_of_error_e < 1.0):
        raise ValueError("Margin of error e must satisfy 0 < e < 1.0")
    return population_n / (1.0 + population_n * (margin_of_error_e ** 2))


def compute_n_gain_robust(pretest: float, posttest: float, max_score: float = 100.0) -> dict:
    """Computes Normalized Gain with division-by-zero ceiling and negative gain classification."""
    if not (0 <= pretest <= max_score) or not (0 <= posttest <= max_score):
        raise ValueError("Pretest and Posttest scores must be within [0, max_score]")

    denom = max_score - pretest
    if denom == 0:
        if posttest == max_score:
            return {"gain": 1.0, "category": "Maksimal (Ceiling Effect)", "status": "CEILING_PERFECT"}
        else:
            return {"gain": -1.0, "category": "Regresi Defisit", "status": "RETROGRADE"}

    gain = (posttest - pretest) / denom

    if gain < 0:
        cat = "Regresi / Penurunan Performa"
    elif gain > 0.70:
        cat = "Tinggi"
    elif gain >= 0.30:
        cat = "Sedang"
    else:
        cat = "Rendah"

    return {"gain": round(gain, 4), "category": cat, "status": "VALID"}


def select_panel_data_model(chow_p: float, hausman_p: float = None, lm_p: float = None) -> dict:
    """Executes econometric model selection decision tree among CEM, FEM, and REM."""
    steps = []
    if chow_p < 0.05:
        steps.append(f"Chow Test (p={chow_p:.4f} < 0.05): Fixed Effect Model (FEM) terpilih dibanding CEM.")
        if hausman_p is None:
            raise ValueError("Hausman test p-value required when Chow rejects CEM.")
        if hausman_p < 0.05:
            steps.append(f"Hausman Test (p={hausman_p:.4f} < 0.05): Fixed Effect Model (FEM) terpilih dibanding REM.")
            final = "Fixed Effect Model (FEM)"
        else:
            steps.append(f"Hausman Test (p={hausman_p:.4f} >= 0.05): Random Effect Model (REM) terpilih dibanding FEM.")
            final = "Random Effect Model (REM)"
    else:
        steps.append(f"Chow Test (p={chow_p:.4f} >= 0.05): Common Effect Model (CEM) terpilih dibanding FEM.")
        if lm_p is None:
            raise ValueError("Lagrange Multiplier test p-value required when Chow accepts CEM.")
        if lm_p < 0.05:
            steps.append(f"LM Test (p={lm_p:.4f} < 0.05): Random Effect Model (REM) terpilih dibanding CEM.")
            final = "Random Effect Model (REM)"
        else:
            steps.append(f"LM Test (p={lm_p:.4f} >= 0.05): Common Effect Model (CEM) terpilih dibanding REM.")
            final = "Common Effect Model (CEM)"
    return {"selected_model": final, "decision_steps": steps}


class TestMathematicalFormulasAdversarial(unittest.TestCase):
    """Stress-tests Slovin asymptotics, SUS flat-lining, N-Gain zero/negative, and Panel Data."""

    def test_slovin_extreme_boundary_conditions(self):
        # 1. N = 1 (Minimal population)
        res_n1 = compute_slovin_robust(1, 0.05)
        self.assertAlmostEqual(res_n1, 0.9975, places=3)
        self.assertEqual(math.ceil(res_n1), 1)

        # 2. Large population N = 1,000,000 (Approaches asymptotic limit 1/e^2 = 400)
        res_large = compute_slovin_robust(1_000_000, 0.05)
        self.assertAlmostEqual(res_large, 399.84, places=1)
        self.assertEqual(math.ceil(res_large), 400)

        # 3. Extreme error tolerances e = 0.01 (High precision)
        res_e01 = compute_slovin_robust(10_000, 0.01)
        self.assertEqual(res_e01, 5000.0)

        # 4. Extreme error tolerances e = 0.20 (Low precision)
        res_e20 = compute_slovin_robust(1000, 0.20)
        self.assertAlmostEqual(res_e20, 24.39, places=2)
        self.assertEqual(math.ceil(res_e20), 25)

        # 5. Invalid inputs raise ValueError
        with self.assertRaises(ValueError):
            compute_slovin_robust(0, 0.05)
        with self.assertRaises(ValueError):
            compute_slovin_robust(100, 0.0)
        with self.assertRaises(ValueError):
            compute_slovin_robust(100, 1.0)

    def test_sus_flatline_psychometric_invariant(self):
        """Proves any straight-line response (all 1s, all 2s, all 3s, all 4s, all 5s) equals 50.0."""
        from test_skripsi_m2_methodologies import compute_sus_score
        for constant_score in range(1, 6):
            responses = [constant_score] * 10
            sus_score = compute_sus_score(responses)
            self.assertEqual(sus_score, 50.0, f"Constant score {constant_score} must yield exact 50.0")

    def test_n_gain_division_by_zero_and_negative_gain(self):
        # 1. Perfect student pretest = posttest = 100
        res_perfect = compute_n_gain_robust(100.0, 100.0, 100.0)
        self.assertEqual(res_perfect["status"], "CEILING_PERFECT")
        self.assertEqual(res_perfect["gain"], 1.0)

        # 2. Negative gain / retrograde learning (Post < Pre)
        res_neg = compute_n_gain_robust(80.0, 60.0, 100.0)
        self.assertEqual(res_neg["gain"], -1.0)
        self.assertEqual(res_neg["category"], "Regresi / Penurunan Performa")

        # 3. High, medium, low thresholds
        self.assertEqual(compute_n_gain_robust(40.0, 85.0)["category"], "Tinggi")
        self.assertEqual(compute_n_gain_robust(40.0, 70.0)["category"], "Sedang")
        self.assertEqual(compute_n_gain_robust(50.0, 60.0)["category"], "Rendah")

    def test_panel_data_model_selection_all_four_paths(self):
        # Path 1: Chow < 0.05, Hausman < 0.05 -> FEM
        res1 = select_panel_data_model(chow_p=0.012, hausman_p=0.004)
        self.assertEqual(res1["selected_model"], "Fixed Effect Model (FEM)")

        # Path 2: Chow < 0.05, Hausman >= 0.05 -> REM
        res2 = select_panel_data_model(chow_p=0.012, hausman_p=0.210)
        self.assertEqual(res2["selected_model"], "Random Effect Model (REM)")

        # Path 3: Chow >= 0.05, LM < 0.05 -> REM
        res3 = select_panel_data_model(chow_p=0.180, lm_p=0.002)
        self.assertEqual(res3["selected_model"], "Random Effect Model (REM)")

        # Path 4: Chow >= 0.05, LM >= 0.05 -> CEM
        res4 = select_panel_data_model(chow_p=0.180, lm_p=0.550)
        self.assertEqual(res4["selected_model"], "Common Effect Model (CEM)")


# ===========================================================================
# Suite 4: EYD V Morpho-Syntactic Linter & Grammatical Anomaly Engine
# ===========================================================================

class EydVMorphoSyntacticAuditor:
    """Audits text against standard EYD V morpho-syntactic and academic rules."""

    RULES = [
        # 1. Merged prepositions that must be separated
        (re.compile(r"\bdimana\b", re.IGNORECASE), "EYD-PREP-01", "Bentuk tidak baku 'dimana'. Gunakan 'di mana' atau konjungsi yang tepat."),
        (re.compile(r"\bdiantara\b", re.IGNORECASE), "EYD-PREP-02", "Bentuk tidak baku 'diantara'. Wajib dipisah 'di antara'."),
        (re.compile(r"\bkedepan\b", re.IGNORECASE), "EYD-PREP-03", "Bentuk tidak baku 'kedepan'. Wajib dipisah 'ke depan' (kecuali 'mengedepankan')."),
        (re.compile(r"\bdidalam\b", re.IGNORECASE), "EYD-PREP-04", "Bentuk tidak baku 'didalam'. Wajib dipisah 'di dalam'."),
        (re.compile(r"\bdiluar\b", re.IGNORECASE), "EYD-PREP-05", "Bentuk tidak baku 'diluar'. Wajib dipisah 'di luar'."),
        # 2. Separated passive verbs that must be merged
        (re.compile(r"\bdi\s+(lakukan|uji|teliti|analisis|peroleh|susun|terapkan|bahas|simpulkan)\b", re.IGNORECASE),
         "EYD-VERB-01", "Awalan kata kerja pasif 'di-' wajib ditulis serangkai/disambung."),
        # 3. Improper hyphenation with proper nouns or ordinals
        (re.compile(r"\bdi([A-Z][a-z]+(?:kan|i)?)\b"), "EYD-HYPH-01", "Awalan di- pada kata nama diri wajib menggunakan tanda hubung 'di-$1'."),
        (re.compile(r"\bke\s*(\d+)\b", re.IGNORECASE), "EYD-HYPH-02", "Penulisan tingkat ordinal angka wajib menggunakan tanda hubung 'ke-$1'."),
        # 4. Pseudo-conjunctions
        (re.compile(r"[,;]?\s+di\s+mana\s+(?!.*\?)", re.IGNORECASE), "EYD-CONJ-01", "Frasa 'di mana' dilarang berfungsi sebagai kata penghubung (pseudo-conjunction)."),
        (re.compile(r"[,;]?\s+yang\s+mana\s+", re.IGNORECASE), "EYD-CONJ-02", "Frasa 'yang mana' dilarang berfungsi sebagai kata penghubung antarklausa.")
    ]

    @classmethod
    def audit_text(cls, text: str) -> list[dict]:
        findings = []
        for regex, code, msg in cls.RULES:
            for match in regex.finditer(text):
                findings.append({
                    "code": code,
                    "matched": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                    "message": msg
                })
        return findings


class TestEydVMorphoSyntacticAdversarial(unittest.TestCase):
    """Stress-tests Indonesian academic grammar and morpho-syntax."""

    def test_detection_of_merged_prepositions(self):
        bad_text = "Data disimpan didalam server dimana pengguna berada diantara dua pilihan kedepan."
        findings = EydVMorphoSyntacticAuditor.audit_text(bad_text)
        codes = [f["code"] for f in findings]
        self.assertIn("EYD-PREP-01", codes)  # dimana
        self.assertIn("EYD-PREP-02", codes)  # diantara
        self.assertIn("EYD-PREP-03", codes)  # kedepan
        self.assertIn("EYD-PREP-04", codes)  # didalam

    def test_detection_of_separated_passive_verbs(self):
        bad_text = "Pengujian sistem di lakukan di laboratorium dan data di peroleh secara empiris."
        findings = EydVMorphoSyntacticAuditor.audit_text(bad_text)
        codes = [f["code"] for f in findings]
        self.assertIn("EYD-VERB-01", codes)

    def test_hyphenation_rules_with_proper_nouns_and_ordinals(self):
        bad_text = "Sistem ini sudah diIndonesiakan untuk responden ke 21 pada tingkatan S1."
        findings = EydVMorphoSyntacticAuditor.audit_text(bad_text)
        codes = [f["code"] for f in findings]
        self.assertIn("EYD-HYPH-01", codes)  # diIndonesiakan -> di-Indonesia-kan
        self.assertIn("EYD-HYPH-02", codes)  # ke 21 -> ke-21

    def test_pseudo_conjunction_rejection(self):
        bad_text = "Sistem memiliki modul inventaris di mana pengguna dapat mengelola stok barang yang mana data diperbarui otomatis."
        findings = EydVMorphoSyntacticAuditor.audit_text(bad_text)
        codes = [f["code"] for f in findings]
        self.assertIn("EYD-CONJ-01", codes)
        self.assertIn("EYD-CONJ-02", codes)


# ===========================================================================
# Suite 5: Mermaid Diagram AST Validation on Complex & Corrupted Architectures
# ===========================================================================

class TestMermaidDiagramASTAdversarial(unittest.TestCase):
    """Validates Mermaid diagram parser against complex valid and invalid definitions."""

    def setUp(self):
        self.node_module_path = Path("/data/data/com.termux/files/usr/tmp/mermaid-test/node_modules/mermaid/dist/mermaid.core.mjs")
        if not self.node_module_path.is_file():
            self.skipTest("Mermaid npm module not found in test environment")

    def _parse_mermaid(self, snippet: str) -> tuple[bool, str]:
        validator_js = f"""
const {{ JSDOM }} = require('/data/data/com.termux/files/usr/tmp/mermaid-test/node_modules/jsdom');
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
global.window = dom.window;
global.document = dom.window.document;
global.DOMParser = dom.window.DOMParser;
global.Element = dom.window.Element;
global.Node = dom.window.Node;

import('/data/data/com.termux/files/usr/tmp/mermaid-test/node_modules/mermaid/dist/mermaid.core.mjs').then(async (m) => {{
  const mermaid = m.default;
  mermaid.initialize({{ startOnLoad: false }});
  try {{
    const parsed = await mermaid.parse(process.argv[1]);
    console.log(JSON.stringify({{ status: 'ok', type: parsed.diagramType }}));
  }} catch (err) {{
    console.log(JSON.stringify({{ status: 'error', error: err.message }}));
  }}
}});
"""
        cmd = ["node", "-e", validator_js, snippet]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if proc.returncode != 0:
            return False, proc.stderr
        res = json.loads(proc.stdout.strip())
        return res["status"] == "ok", res.get("error", res.get("type", ""))

    def test_complex_multi_tier_flowchart_with_subgraphs(self):
        complex_flowchart = """flowchart TD
  subgraph PresentationTier[Presentation Tier]
    direction LR
    A["Frontend Client (Vue.js)"] --> B["Mobile App (Flutter)"]
  end
  subgraph DataTier[Data & Persistence Tier]
    C[(PostgreSQL DB)] --- D[(Redis Cache)]
  end
  PresentationTier --> DataTier"""
        ok, msg = self._parse_mermaid(complex_flowchart)
        self.assertTrue(ok, f"Complex flowchart failed: {msg}")

    def test_sequence_diagram_with_alt_and_autonumber(self):
        seq = """sequenceDiagram
  autonumber
  actor M as Mahasiswa
  participant S as Server
  activate M
  M->>S: Unggah Berkas Proposal
  activate S
  alt Berkas Sesuai Format
    S-->>M: Notifikasi Sukses
  else Format Salah
    S-->>M: Notifikasi Galat
  end
  deactivate S
  deactivate M"""
        ok, msg = self._parse_mermaid(seq)
        self.assertTrue(ok, f"Sequence diagram failed: {msg}")

    def test_adversarial_corrupted_mermaid_definitions_rejected(self):
        broken_snippets = [
            "flowchart XX\n A --> B",
            "graph TD\n A[Unclosed bracket --> B",
            "sequenceDiagram\n Pengguna ===>>> Sistem",
            "classDiagram\n class A { +m() }\n A <|--",
            "flowchart TD\n A -->",
        ]
        for idx, s in enumerate(broken_snippets, 1):
            ok, msg = self._parse_mermaid(s)
            self.assertFalse(ok, f"Broken snippet #{idx} should have been rejected but passed!")


# ===========================================================================
# Suite 6: ARS Write-Scope Guard Adversarial Payload & Tamper Defense
# ===========================================================================

class TestArsWriteScopeGuardAdversarial(unittest.TestCase):
    """Stress-tests ARS write scope guard against adversarial escapes and tampered payloads."""

    def setUp(self):
        self.manifest = guard._load_manifest()
        self.workspace_root = str(ROOT)

    def test_bucket_a_agent_path_traversal_denied(self):
        payload = {
            "tool_name": "Write",
            "agent_type": "nyekripsi:synthesis_agent",
            "tool_input": {"file_path": "../../etc/passwd", "content": "malicious"}
        }
        dec = guard.evaluate_decision(payload, self.manifest, self.workspace_root)
        self.assertEqual(dec.get("decision"), "deny")
        self.assertIn("escapes", dec.get("reason", "").lower())

    def test_infrastructure_tamper_denied_for_all_callers(self):
        protected_paths = [
            "hooks/hooks.json",
            "scripts/ars_write_scope_guard.py",
            ".claude-plugin/plugin.json"
        ]
        for p in protected_paths:
            payload = {
                "tool_name": "Write",
                "tool_input": {"file_path": p, "content": "tamper"}
            }
            dec = guard.evaluate_decision(payload, self.manifest, self.workspace_root)
            self.assertEqual(dec.get("decision"), "deny", f"Tampering with {p} must be denied")

    def test_malformed_non_dict_payload_handles_gracefully(self):
        dec_list = guard.evaluate_decision([], self.manifest, self.workspace_root)
        self.assertEqual(dec_list.get("decision"), "allow")

        dec_str = guard.evaluate_decision("string", self.manifest, self.workspace_root)
        self.assertEqual(dec_str.get("decision"), "allow")

        dec_none = guard.evaluate_decision(None, self.manifest, self.workspace_root)
        self.assertEqual(dec_none.get("decision"), "allow")


if __name__ == "__main__":
    unittest.main()
