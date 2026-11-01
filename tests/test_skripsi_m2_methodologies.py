"""Comprehensive Pure Python Unit Test Suite for Milestone 2 (M2) Methodologies & Presets.

This test suite verifies the 4 Milestone 2 reference guides and their underlying
methodological, statistical, software engineering, and faculty configuration specifications:
1. academic-paper/references/metodologi_kuantitatif_guide.md
2. academic-paper/references/metodologi_kualitatif_guide.md
3. academic-paper/references/metodologi_it_se_guide.md
4. academic-paper/references/fakultas_presets_guide.md

Adheres strictly to pure Python stdlib (unittest, re, pathlib, json, math, subprocess).
"""

from __future__ import annotations

import json
import math
import re
import subprocess
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


# ===========================================================================
# 1. Test Suite: Metodologi Kuantitatif Guide
# ===========================================================================

class TestMetodologiKuantitatifGuide(unittest.TestCase):
    """Verifies the Quantitative Methodology reference guide."""

    def setUp(self) -> None:
        self.guide_path = ROOT / "academic-paper/references/metodologi_kuantitatif_guide.md"
        self.assertTrue(self.guide_path.is_file(), f"Missing file: {self.guide_path}")
        self.content = self.guide_path.read_text(encoding="utf-8")
        self.lines = self.content.splitlines()

    def test_substantive_length_and_structure(self) -> None:
        self.assertGreater(len(self.lines), 200, "Guide should be comprehensive (>200 lines)")
        self.assertIn("# Pedoman Metodologi Penelitian Kuantitatif", self.content)

    def test_paradigms_and_typologies(self) -> None:
        content_lower = self.content.lower()
        # Surveys
        self.assertIn("cross-sectional", content_lower)
        self.assertIn("longitudinal", content_lower)
        # Quasi-experimental
        self.assertIn("kuasi-eksperimen", content_lower)
        self.assertIn("non-equivalent control group", content_lower)
        # Regressions & Panel
        self.assertIn("regresi linear sederhana", content_lower)
        self.assertIn("regresi linear berganda", content_lower)
        self.assertIn("regresi data panel", content_lower)
        self.assertIn("common effect model", content_lower)
        self.assertIn("fixed effect model", content_lower)
        self.assertIn("random effect model", content_lower)
        self.assertIn("chow", content_lower)
        self.assertIn("hausman", content_lower)
        self.assertIn("lagrange multiplier", content_lower)
        # Correlation
        self.assertIn("pearson product-moment", content_lower)
        self.assertIn("spearman", content_lower)

    def test_operationalization_of_variables(self) -> None:
        # 4 taxonomy roles
        self.assertRegex(self.content, r"(?i)variabel\s+(bebas|eksogen)")
        self.assertRegex(self.content, r"(?i)variabel\s+(terikat|endogen)")
        self.assertRegex(self.content, r"(?i)variabel\s+(mediasi|intervening)")
        self.assertRegex(self.content, r"(?i)variabel\s+moderasi")
        # Traceability table
        self.assertIn("Matriks Operasionalisasi Variabel", self.content)
        self.assertIn("Indikator Empiris", self.content)
        self.assertIn("Skala Pengukuran", self.content)

    def test_population_and_sampling(self) -> None:
        content_lower = self.content.lower()
        # Probability & Non-probability
        self.assertIn("simple random sampling", content_lower)
        self.assertIn("stratified random sampling", content_lower)
        self.assertIn("cluster", content_lower)
        self.assertIn("purposive sampling", content_lower)
        self.assertIn("snowball sampling", content_lower)
        # Mathematical formulas
        self.assertIn("slovin", content_lower)
        self.assertRegex(self.content, r"1\s*\+\s*N\s*\(\s*e\^2\s*\)")
        self.assertIn("isaac", content_lower)
        self.assertIn("krejcie", content_lower)
        self.assertIn("morgan", content_lower)
        # Hair rule of thumb: 5-10 times indicators
        self.assertRegex(self.content, r"5\s*(\\times|[x×])\s*.*indikator.*10\s*(\\times|[x×])")

    def test_instruments_and_measurement(self) -> None:
        # Scales
        self.assertIn("Skala Likert", self.content)
        self.assertIn("Semantic Differential", self.content)
        self.assertIn("Skala Guttman", self.content)
        # Validity
        self.assertIn("Pearson Product-Moment", self.content)
        self.assertIn("r_{xy}", self.content)
        self.assertRegex(self.content, r"r_\{?\\text\{hitung\}\}?\s*>\s*r_\{?\\text\{tabel\}\}?")
        self.assertIn("CFA", self.content)
        self.assertIn("0,50", self.content)
        # Reliability
        self.assertIn("Cronbach's Alpha", self.content)
        self.assertRegex(self.content, r"\\alpha\s*\\ge\s*0,70")
        self.assertIn("Composite Reliability", self.content)

    def test_classical_assumption_tests(self) -> None:
        content_lower = self.content.lower()
        # Normality
        self.assertIn("kolmogorov-smirnov", content_lower)
        self.assertIn("shapiro-wilk", content_lower)
        # Linearity
        self.assertIn("linearitas", content_lower)
        # Multicollinearity
        self.assertIn("vif", content_lower)
        self.assertIn("tolerance", content_lower)
        self.assertIn("10", self.content)
        # Heteroskedasticity
        self.assertIn("heteroskedastisitas", content_lower)
        self.assertIn("glejser", content_lower)
        self.assertIn("scatterplot", content_lower)
        # Autocorrelation
        self.assertIn("autokorelasi", content_lower)
        self.assertIn("durbin-watson", content_lower)

    def test_three_stage_data_analysis(self) -> None:
        self.assertIn("Inventarisasi Data", self.content)
        self.assertIn("Klasifikasi Data", self.content)
        self.assertIn("Penafsiran Data dengan Pisau Analisis", self.content)
        # Must connect to RQs
        self.assertRegex(self.content, r"(?i)rumusan masalah|pertanyaan penelitian|rq")

    def test_hypothesis_testing(self) -> None:
        content_lower = self.content.lower()
        self.assertIn("uji t", content_lower)
        self.assertIn("uji f", content_lower)
        self.assertIn("koefisien determinasi", content_lower)
        self.assertIn("r^2", content_lower)
        self.assertIn("adjusted", content_lower)
        self.assertIn("sobel test", content_lower)


# ===========================================================================
# 2. Test Suite: Metodologi Kualitatif Guide
# ===========================================================================

class TestMetodologiKualitatifGuide(unittest.TestCase):
    """Verifies the Qualitative Methodology reference guide."""

    def setUp(self) -> None:
        self.guide_path = ROOT / "academic-paper/references/metodologi_kualitatif_guide.md"
        self.assertTrue(self.guide_path.is_file(), f"Missing file: {self.guide_path}")
        self.content = self.guide_path.read_text(encoding="utf-8")
        self.lines = self.content.splitlines()

    def test_substantive_length_and_structure(self) -> None:
        self.assertGreater(len(self.lines), 200, "Guide should be comprehensive (>200 lines)")
        self.assertIn("# Pedoman Metodologi Penelitian Kualitatif", self.content)

    def test_paradigms_and_typologies(self) -> None:
        content_lower = self.content.lower()
        # Case study Yin
        self.assertIn("yin", content_lower)
        self.assertIn("single-case holistic", content_lower)
        self.assertIn("single-case embedded", content_lower)
        self.assertIn("multiple-case", content_lower)
        # Descriptive-analytical
        self.assertIn("deskriptif-analitis", content_lower)
        self.assertIn("fenomenologi", content_lower)
        # Content & Framing analysis
        self.assertIn("krippendorff", content_lower)
        self.assertIn("robert n. entman", content_lower)
        self.assertIn("define problems", content_lower)
        self.assertIn("diagnose causes", content_lower)
        self.assertIn("make moral judgments", content_lower)
        self.assertIn("suggest remedies", content_lower)
        # Pan & Kosicki
        self.assertIn("zhongdang pan", content_lower)
        self.assertIn("sintaksis", content_lower)
        self.assertIn("skrip", content_lower)
        self.assertIn("tematik", content_lower)
        self.assertIn("retoris", content_lower)
        # CDA
        self.assertIn("fairclough", content_lower)
        self.assertIn("van dijk", content_lower)

    def test_empirical_reality_and_informants(self) -> None:
        content_lower = self.content.lower()
        self.assertIn("purposive sampling", content_lower)
        self.assertIn("saturasi data", content_lower)
        # Informant categories
        self.assertIn("informan kunci", content_lower)
        self.assertIn("informan utama", content_lower)
        self.assertIn("triangulasi", content_lower)
        # Profile table
        self.assertIn("Kode Informan", self.content)
        self.assertIn("[INF-01]", self.content)

    def test_data_collection_techniques(self) -> None:
        content_lower = self.content.lower()
        self.assertIn("wawancara mendalam", content_lower)
        self.assertIn("semi-terstruktur", content_lower)
        self.assertIn("probing", content_lower)
        self.assertIn("observasi partisipatif", content_lower)
        self.assertIn("catatan lapangan", content_lower)
        self.assertIn("studi dokumentasi", content_lower)
        self.assertIn("focus group discussion", content_lower)

    def test_data_trustworthiness_and_triangulation(self) -> None:
        content_lower = self.content.lower()
        # Lincoln & Guba 4 criteria
        self.assertIn("lincoln", content_lower)
        self.assertIn("guba", content_lower)
        self.assertIn("kredibilitas", content_lower)
        self.assertIn("transferabilitas", content_lower)
        self.assertIn("dependabilitas", content_lower)
        self.assertIn("konfirmabilitas", content_lower)
        # Triangulation 4 types
        self.assertIn("triangulasi sumber", content_lower)
        self.assertIn("triangulasi metode", content_lower)
        self.assertIn("triangulasi peneliti", content_lower)
        self.assertIn("triangulasi teori", content_lower)
        # Member checking & audit trail
        self.assertIn("member checking", content_lower)
        self.assertIn("audit trail", content_lower)

    def test_three_stage_data_analysis(self) -> None:
        self.assertIn("Tahap 1: Inventarisasi Data", self.content)
        self.assertIn("Tahap 2: Klasifikasi Data", self.content)
        self.assertIn("Tahap 3: Penafsiran Data dengan Pisau Analisis", self.content)
        # Coding methods
        content_lower = self.content.lower()
        self.assertIn("koding terbuka", content_lower)
        self.assertIn("koding aksial", content_lower)
        self.assertIn("koding selektif", content_lower)
        # Miles & Huberman
        self.assertIn("miles", content_lower)
        self.assertIn("huberman", content_lower)
        self.assertIn("reduksi", content_lower)
        self.assertIn("penyajian", content_lower)

    def test_reflexivity_and_objectivity(self) -> None:
        content_lower = self.content.lower()
        self.assertIn("refleksivitas", content_lower)
        self.assertIn("instrumen utama", content_lower)
        self.assertIn("epoche", content_lower)
        self.assertIn("positionality statement", content_lower)


# ===========================================================================
# 3. Test Suite: Metodologi IT / Software Engineering Guide
# ===========================================================================

class TestMetodologiITSEGuide(unittest.TestCase):
    """Verifies the IT & Software Engineering Methodology reference guide."""

    def setUp(self) -> None:
        self.guide_path = ROOT / "academic-paper/references/metodologi_it_se_guide.md"
        self.assertTrue(self.guide_path.is_file(), f"Missing file: {self.guide_path}")
        self.content = self.guide_path.read_text(encoding="utf-8")
        self.lines = self.content.splitlines()

    def test_substantive_length_and_structure(self) -> None:
        self.assertGreater(len(self.lines), 200, "Guide should be comprehensive (>200 lines)")
        self.assertIn("# Pedoman Metodologi Rekayasa Perangkat Lunak dan Teknologi Informasi", self.content)

    def test_software_engineering_paradigms(self) -> None:
        content_lower = self.content.lower()
        # Agile & Scrum
        self.assertIn("agile", content_lower)
        self.assertIn("scrum", content_lower)
        self.assertIn("product backlog", content_lower)
        self.assertIn("user story", content_lower)
        self.assertIn("sprint planning", content_lower)
        self.assertIn("daily standup", content_lower)
        self.assertIn("sprint review", content_lower)
        self.assertIn("sprint retrospective", content_lower)
        self.assertIn("burndown chart", content_lower)
        # Waterfall
        self.assertIn("waterfall", content_lower)
        # Prototyping
        self.assertIn("prototyping", content_lower)
        self.assertIn("evolutionary prototyping", content_lower)
        self.assertIn("throwaway", content_lower)
        # R&D models
        self.assertIn("addie", content_lower)
        self.assertIn("4d", content_lower)
        self.assertIn("thiagarajan", content_lower)
        self.assertIn("borg & gall", content_lower)
        self.assertIn("ptk", content_lower)

    def test_requirements_engineering(self) -> None:
        # FR with MoSCoW
        self.assertIn("Functional Requirements", self.content)
        self.assertIn("MoSCoW", self.content)
        self.assertIn("Must have", self.content)
        self.assertIn("Should have", self.content)
        self.assertIn("Could have", self.content)
        self.assertIn("Won't have", self.content)
        # NFR with FURPS+
        self.assertIn("FURPS", self.content)
        self.assertIn("Functionality", self.content)
        self.assertIn("Usability", self.content)
        self.assertIn("Reliability", self.content)
        self.assertIn("Performance", self.content)
        self.assertIn("Supportability", self.content)

    def test_mermaid_syntax_modeling(self) -> None:
        # Flowchart TD / LR
        self.assertIn("flowchart TD", self.content)
        # Sequence Diagram
        self.assertIn("sequenceDiagram", self.content)
        # Class Diagram
        self.assertIn("classDiagram", self.content)
        # Architecture Tier Diagram
        self.assertIn("PresentationTier", self.content)
        self.assertIn("DataTier", self.content)

    def test_verification_and_testing_strategies(self) -> None:
        content_lower = self.content.lower()
        # Black box
        self.assertIn("black-box testing", content_lower)
        self.assertIn("equivalence partitioning", content_lower)
        self.assertIn("boundary value analysis", content_lower)
        # SUS: 10 questions and formula
        self.assertIn("system usability scale", content_lower)
        self.assertIn("q1", content_lower)
        self.assertIn("q10", content_lower)
        self.assertRegex(self.content, r"2,5|2\.5")
        self.assertIn("80,3", self.content)
        self.assertIn("Excellent", self.content)
        # UAT & Stress Testing
        self.assertIn("user acceptance testing", content_lower)
        self.assertIn("throughput", content_lower)
        self.assertIn("latency", content_lower)


# ===========================================================================
# 4. Test Suite: Fakultas Presets Guide
# ===========================================================================

class TestFakultasPresetsGuide(unittest.TestCase):
    """Verifies the Universal Faculty Presets reference guide."""

    def setUp(self) -> None:
        self.guide_path = ROOT / "academic-paper/references/fakultas_presets_guide.md"
        self.assertTrue(self.guide_path.is_file(), f"Missing file: {self.guide_path}")
        self.content = self.guide_path.read_text(encoding="utf-8")
        self.lines = self.content.splitlines()

    def test_substantive_length_and_structure(self) -> None:
        self.assertGreater(len(self.lines), 200, "Guide should be comprehensive (>200 lines)")
        self.assertIn("# Pedoman Sistem Preset Fleksibilitas Fakultas Universal", self.content)

    def test_all_seven_presets_specified(self) -> None:
        presets = [
            "it-software",
            "sosial-humaniora",
            "hukum",
            "ekonomi-bisnis",
            "pendidikan-r&d",
            "kesehatan-sains",
            "custom",
        ]
        for p in presets:
            self.assertIn(f"`{p}`", self.content, f"Preset {p} must be defined")

    def test_it_software_preset(self) -> None:
        # Chapter 3 & 4 variations
        self.assertIn("Bab III: Analisis dan Desain Sistem", self.content)
        self.assertIn("Bab IV: Implementasi dan Pengujian Sistem", self.content)
        self.assertIn("Bab V: Penutup", self.content)
        self.assertIn("IEEE", self.content)

    def test_sosial_humaniora_preset(self) -> None:
        self.assertIn("Bab I: Pendahuluan", self.content)
        self.assertIn("Kajian Pustaka & Kerangka Teori", self.content)
        self.assertIn("Pembahasan Dialektis", self.content)
        self.assertIn("APA 7", self.content)

    def test_hukum_preset(self) -> None:
        content_lower = self.content.lower()
        self.assertIn("hukum normatif", content_lower)
        self.assertIn("hukum empiris", content_lower)
        # Legal materials
        self.assertIn("bahan hukum primer", content_lower)
        self.assertIn("bahan hukum sekunder", content_lower)
        self.assertIn("bahan hukum tersier", content_lower)
        # Approaches
        self.assertIn("statute approach", content_lower)
        self.assertIn("case approach", content_lower)
        self.assertIn("conceptual approach", content_lower)
        # Chicago footnotes
        self.assertIn("footnote", content_lower)

    def test_ekonomi_bisnis_preset(self) -> None:
        content_lower = self.content.lower()
        self.assertIn("ekonometrika", content_lower)
        self.assertIn("regresi data panel", content_lower)
        self.assertIn("chow", content_lower)
        self.assertIn("hausman", content_lower)
        self.assertIn("rasio", content_lower)
        self.assertIn("sem-pls", content_lower)

    def test_pendidikan_rnd_preset(self) -> None:
        content_lower = self.content.lower()
        self.assertIn("r&d", content_lower)
        self.assertIn("addie", content_lower)
        self.assertIn("4d", content_lower)
        self.assertIn("borg & gall", content_lower)
        self.assertIn("ahli materi", content_lower)
        self.assertIn("ahli media", content_lower)
        self.assertIn("n-gain score", content_lower)
        self.assertIn("ptk", content_lower)

    def test_kesehatan_sains_preset(self) -> None:
        content_lower = self.content.lower()
        self.assertIn("cross-sectional", content_lower)
        self.assertIn("case-control", content_lower)
        self.assertIn("kohort", content_lower)
        self.assertIn("ethical clearance", content_lower)
        self.assertIn("kepk", content_lower)
        self.assertIn("vancouver", content_lower)

    def test_custom_preset_and_json_schema(self) -> None:
        self.assertIn("https://nyekripsi.org/schemas/faculty-preset-v1.json", self.content)
        self.assertIn("custom_toc.json", self.content)
        self.assertIn("faculty_id", self.content)
        self.assertIn("preset_name", self.content)


# ===========================================================================
# 5. Algorithmic and Mathematical Formula Verification
# ===========================================================================

def compute_slovin(population_n: int, margin_of_error_e: float) -> float:
    """Computes sample size using Slovin's formula."""
    if population_n <= 0:
        raise ValueError("Population must be positive")
    return population_n / (1.0 + population_n * (margin_of_error_e ** 2))


def compute_sus_score(responses: list[int]) -> float:
    """Computes System Usability Scale (SUS) score from 10 Likert responses (1 to 5)."""
    if len(responses) != 10:
        raise ValueError(f"SUS requires exactly 10 responses, got {len(responses)}")
    for i, r in enumerate(responses):
        if not (1 <= r <= 5):
            raise ValueError(f"Response {i+1} value {r} out of range [1, 5]")

    total_contribution = 0.0
    for idx, val in enumerate(responses, start=1):
        if idx % 2 != 0:  # Odd questions (1, 3, 5, 7, 9)
            total_contribution += (val - 1)
        else:  # Even questions (2, 4, 6, 8, 10)
            total_contribution += (5 - val)

    return total_contribution * 2.5


def evaluate_sus_adjective_and_grade(score: float) -> dict[str, str]:
    """Evaluates SUS score to grade scale, adjective rating, and acceptability."""
    if score >= 80.3:
        return {"grade": "Grade A", "adjective": "Excellent", "acceptable": "Acceptable"}
    elif score >= 68.0:
        return {"grade": "Grade B", "adjective": "Good", "acceptable": "Acceptable"}
    elif score >= 51.0:
        return {"grade": "Grade C", "adjective": "OK", "acceptable": "Marginal"}
    elif score >= 38.0:
        return {"grade": "Grade D", "adjective": "Poor", "acceptable": "Not Acceptable"}
    else:
        return {"grade": "Grade F", "adjective": "Worst Imaginable", "acceptable": "Not Acceptable"}


def compute_n_gain(pretest: float, posttest: float, max_score: float = 100.0) -> float:
    """Computes Normalized Gain (N-Gain) score according to Hake (1998)."""
    denom = max_score - pretest
    if denom <= 0:
        return 0.0
    gain = (posttest - pretest) / denom
    return gain


def evaluate_n_gain_category(g: float) -> str:
    """Classifies N-Gain score into High, Medium, or Low effectiveness."""
    if g > 0.70:
        return "Tinggi"
    elif g >= 0.30:
        return "Sedang"
    else:
        return "Rendah"


class TestMethodologyMathematicalFormulasAndAlgorithms(unittest.TestCase):
    """Empirical mathematical tests verifying that formulas in the guides execute correctly."""

    def test_slovin_formula_computation(self) -> None:
        # Standard benchmark: N = 1000, e = 0.05
        # n = 1000 / (1 + 1000 * 0.0025) = 1000 / 3.5 = 285.714... -> 286
        result = compute_slovin(1000, 0.05)
        self.assertAlmostEqual(result, 285.714, places=2)
        self.assertEqual(math.ceil(result), 286)

        # N = 500, e = 0.05 -> 500 / (1 + 500 * 0.0025) = 500 / 2.25 = 222.22 -> 223
        res500 = compute_slovin(500, 0.05)
        self.assertAlmostEqual(res500, 222.22, places=1)
        self.assertEqual(math.ceil(res500), 223)

    def test_sus_calculation_algorithm(self) -> None:
        # Perfect score: all 5 on odd, all 1 on even -> 4 contribution each * 10 = 40 * 2.5 = 100.0
        perfect_responses = [5, 1, 5, 1, 5, 1, 5, 1, 5, 1]
        score_100 = compute_sus_score(perfect_responses)
        self.assertEqual(score_100, 100.0)
        eval_100 = evaluate_sus_adjective_and_grade(score_100)
        self.assertEqual(eval_100["grade"], "Grade A")
        self.assertEqual(eval_100["adjective"], "Excellent")
        self.assertEqual(eval_100["acceptable"], "Acceptable")

        # Neutral score: all 3s -> odd contributes (3-1)=2, even contributes (5-3)=2 -> 2*10 = 20 * 2.5 = 50.0
        neutral_responses = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        score_50 = compute_sus_score(neutral_responses)
        self.assertEqual(score_50, 50.0)
        eval_50 = evaluate_sus_adjective_and_grade(score_50)
        self.assertEqual(eval_50["grade"], "Grade D")
        self.assertEqual(eval_50["acceptable"], "Not Acceptable")

        # Worst score: all 1 on odd, all 5 on even -> 0 contribution each -> 0 * 2.5 = 0.0
        worst_responses = [1, 5, 1, 5, 1, 5, 1, 5, 1, 5]
        score_0 = compute_sus_score(worst_responses)
        self.assertEqual(score_0, 0.0)
        eval_0 = evaluate_sus_adjective_and_grade(score_0)
        self.assertEqual(eval_0["grade"], "Grade F")

        # Industry benchmark score (~68.0, Grade B Good)
        # E.g. [4, 2, 4, 2, 4, 2, 4, 2, 3, 2]:
        # Odd: Q1=4->3, Q3=4->3, Q5=4->3, Q7=4->3, Q9=3->2 (sum odd = 14)
        # Even: Q2=2->3, Q4=2->3, Q6=2->3, Q8=2->3, Q10=2->3 (sum even = 15)
        # Total = 29 * 2.5 = 72.5 -> Grade B Good
        good_responses = [4, 2, 4, 2, 4, 2, 4, 2, 3, 2]
        score_good = compute_sus_score(good_responses)
        self.assertEqual(score_good, 72.5)
        eval_good = evaluate_sus_adjective_and_grade(score_good)
        self.assertEqual(eval_good["grade"], "Grade B")
        self.assertEqual(eval_good["adjective"], "Good")

    def test_n_gain_score_computation(self) -> None:
        # High gain: Pre = 40, Post = 85, Max = 100
        # g = (85 - 40) / (100 - 40) = 45 / 60 = 0.75 -> Tinggi
        g_high = compute_n_gain(40.0, 85.0, 100.0)
        self.assertEqual(g_high, 0.75)
        self.assertEqual(evaluate_n_gain_category(g_high), "Tinggi")

        # Medium gain: Pre = 40, Post = 70, Max = 100
        # g = (70 - 40) / (100 - 40) = 30 / 60 = 0.50 -> Sedang
        g_med = compute_n_gain(40.0, 70.0, 100.0)
        self.assertEqual(g_med, 0.50)
        self.assertEqual(evaluate_n_gain_category(g_med), "Sedang")

        # Low gain: Pre = 50, Post = 60, Max = 100
        # g = (60 - 50) / (100 - 50) = 10 / 50 = 0.20 -> Rendah
        g_low = compute_n_gain(50.0, 60.0, 100.0)
        self.assertEqual(g_low, 0.20)
        self.assertEqual(evaluate_n_gain_category(g_low), "Rendah")

    def test_vif_and_tolerance_relationship(self) -> None:
        # Tolerance = 0.25 -> VIF = 1 / 0.25 = 4.0 (Safe, < 10)
        tolerance = 0.25
        vif = 1.0 / tolerance
        self.assertEqual(vif, 4.0)
        self.assertLess(vif, 10.0)

        # Danger zone: Tolerance = 0.05 -> VIF = 20.0 (Multicollinearity present)
        tol_low = 0.05
        vif_high = 1.0 / tol_low
        self.assertEqual(vif_high, 20.0)
        self.assertGreater(vif_high, 10.0)


# ===========================================================================
# 6. Empirical Mermaid Diagram Syntax Validation for M2 Guides
# ===========================================================================

class TestMermaidDiagramSyntaxInM2Guides(unittest.TestCase):
    """Validates every Mermaid diagram block across all 4 Milestone 2 guides."""

    def setUp(self) -> None:
        self.target_files = [
            ROOT / "academic-paper/references/metodologi_kuantitatif_guide.md",
            ROOT / "academic-paper/references/metodologi_kualitatif_guide.md",
            ROOT / "academic-paper/references/metodologi_it_se_guide.md",
            ROOT / "academic-paper/references/fakultas_presets_guide.md",
        ]
        self.mermaid_regex = re.compile(r"```mermaid\s*\n([\s\S]*?)```")

    def test_each_guide_contains_at_least_one_valid_mermaid_diagram(self) -> None:
        for fpath in self.target_files:
            content = fpath.read_text(encoding="utf-8")
            matches = self.mermaid_regex.findall(content)
            self.assertGreater(
                len(matches),
                0,
                f"Guide {fpath.name} must contain at least 1 Mermaid diagram block",
            )
            for idx, diagram in enumerate(matches, start=1):
                diagram_clean = diagram.strip()
                # Check valid starter diagram keyword
                valid_starters = (
                    "flowchart TD",
                    "flowchart LR",
                    "flowchart TB",
                    "sequenceDiagram",
                    "classDiagram",
                    "graph TD",
                    "graph LR",
                    "stateDiagram",
                )
                starts_valid = any(diagram_clean.startswith(s) for s in valid_starters)
                self.assertTrue(
                    starts_valid,
                    f"Diagram #{idx} in {fpath.name} starts with invalid token:\n{diagram_clean[:40]}",
                )

    def test_empirical_nodejs_mermaid_ast_parse_if_available(self) -> None:
        """If node & mermaid library are available on the host, perform actual headless AST parsing."""
        node_module_path = Path("/data/data/com.termux/files/usr/tmp/mermaid-test/node_modules/mermaid/dist/mermaid.core.mjs")
        if not node_module_path.is_file():
            self.skipTest("Mermaid npm module not found in test environment, skipping headless AST validation")

        validator_js = """
const { JSDOM } = require('/data/data/com.termux/files/usr/tmp/mermaid-test/node_modules/jsdom');
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
global.window = dom.window;
global.document = dom.window.document;
global.DOMParser = dom.window.DOMParser;
global.Element = dom.window.Element;
global.Node = dom.window.Node;

const fs = require('fs');

import('/data/data/com.termux/files/usr/tmp/mermaid-test/node_modules/mermaid/dist/mermaid.core.mjs').then(async (m) => {
  const mermaid = m.default;
  mermaid.initialize({ startOnLoad: false });

  const files = process.argv.slice(2);
  const results = [];
  const regex = /```mermaid\\n([\\s\\S]*?)```/g;

  for (const file of files) {
    const text = fs.readFileSync(file, 'utf8');
    let match;
    let block = 1;
    while ((match = regex.exec(text)) !== null) {
      const code = match[1].trim();
      try {
        const parsed = await mermaid.parse(code);
        results.push({ file, block, status: 'ok', diagramType: parsed.diagramType });
      } catch (err) {
        results.push({ file, block, status: 'error', error: err.message });
      }
      block++;
    }
  }
  console.log(JSON.stringify(results));
});
"""
        cmd = ["node", "-e", validator_js, "--"] + [str(p) for p in self.target_files]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        self.assertEqual(proc.returncode, 0, f"Mermaid node validator error: {proc.stderr}")
        results = json.loads(proc.stdout.strip())
        self.assertGreater(len(results), 0, "Expected parsed Mermaid diagrams")
        for res in results:
            self.assertEqual(
                res.get("status"),
                "ok",
                f"Mermaid syntax error in {res.get('file')} block #{res.get('block')}: {res.get('error')}",
            )


if __name__ == "__main__":
    unittest.main()
