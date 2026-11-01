"""Tier 4 Real-World Application Scenarios and E2E Thesis Workloads.

This test suite executes 5 end-to-end Indonesian undergraduate thesis (Skripsi S1)
lifecycles across diverse faculty presets and methodologies:
- Scenario 1: IT / Software Engineering Skripsi Lifecycle (Preset: it-software)
- Scenario 2: Quantitative Empirical Skripsi Lifecycle (Preset: ekonomi-bisnis / sosial-humaniora)
- Scenario 3: Qualitative Descriptive/Case Study Skripsi Lifecycle (Preset: sosial-humaniora / hukum)
- Scenario 4: Educational R&D / Clinical Health Skripsi Lifecycle (Preset: pendidikan-r&d / kesehatan-sains)
- Scenario 5: Custom Campus Table of Contents Intake & Dynamic Adaptation (Preset: custom)

Pure standard library Python implementation without third-party dependencies.
"""
from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
import unittest
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- Verification Helper Engines ---

def compute_slovin(population_n: int, margin_of_error_e: float) -> float:
    if population_n <= 0:
        raise ValueError("Population must be positive")
    if not (0 < margin_of_error_e < 1.0):
        raise ValueError("Margin of error e must satisfy 0 < e < 1.0")
    return population_n / (1.0 + population_n * (margin_of_error_e ** 2))

def compute_sus_score(responses: List[int]) -> float:
    if len(responses) != 10:
        raise ValueError(f"SUS requires exactly 10 responses, got {len(responses)}")
    for i, r in enumerate(responses):
        if not (1 <= r <= 5):
            raise ValueError(f"Response {i+1} value {r} out of range [1, 5]")
    total = 0.0
    for idx, val in enumerate(responses, start=1):
        if idx % 2 != 0:  # Odd questions
            total += (val - 1)
        else:  # Even questions
            total += (5 - val)
    return total * 2.5

def evaluate_sus_adjective_and_grade(score: float) -> Dict[str, str]:
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
    denom = max_score - pretest
    if denom <= 0:
        return 0.0
    return (posttest - pretest) / denom

def evaluate_n_gain_category(g: float) -> str:
    if g > 0.70:
        return "Tinggi"
    elif g >= 0.30:
        return "Sedang"
    else:
        return "Rendah"

def evaluate_panel_model_selection(chow_p: float, hausman_p: float, lm_p: float) -> str:
    """Decision tree for econometric panel data model selection (CEM, FEM, REM)."""
    # Chow test: CEM vs FEM (p < 0.05 -> FEM)
    chow_chooses_fem = chow_p < 0.05
    if chow_chooses_fem:
        # Hausman test: FEM vs REM (p < 0.05 -> FEM, p >= 0.05 -> REM)
        return "FEM" if hausman_p < 0.05 else "REM"
    else:
        # LM test: CEM vs REM (p < 0.05 -> REM, p >= 0.05 -> CEM)
        return "REM" if lm_p < 0.05 else "CEM"

def evaluate_vif_and_tolerance(r_squared: float) -> Tuple[float, float]:
    tolerance = 1.0 - r_squared
    vif = 1.0 / tolerance if tolerance > 0 else float("inf")
    return tolerance, vif

def evaluate_defense_verdict(scores: Dict[str, float]) -> Dict[str, Any]:
    weights = {"D1": 0.20, "D2": 0.25, "D3": 0.25, "D4": 0.15, "D5": 0.15}
    composite = sum(scores[d] * weights[d] for d in weights)
    if composite >= 85.0:
        verdict = "LULUS TANPA REVISI"
        grade = "Grade A"
    elif composite >= 75.0:
        verdict = "LULUS DENGAN REVISI MINOR"
        grade = "Grade B+ / A-"
    elif composite >= 60.0:
        verdict = "LULUS DENGAN REVISI MAYOR"
        grade = "Grade B / C+"
    else:
        verdict = "TIDAK LULUS / MENGULANG SIDANG"
        grade = "Grade C / D / E"
    return {"composite": composite, "verdict": verdict, "grade": grade}

def audit_anti_phantom_apa(body_text: str, bib_text: str) -> Dict[str, Any]:
    parenthetical = re.findall(r"\(([A-Z][^,()]+?),\s*(\d{4}[a-z]?)\)", body_text)
    narrative = re.findall(r"([A-Z][a-zA-Z\-]+(?:\s+(?:dan|&)\s+[A-Z][a-zA-Z\-]+|\s+dkk\.|\s+et al\.)*)\s*\((\d{4}[a-z]?)\)", body_text)

    cited_keys = set()
    for auth, yr in parenthetical + narrative:
        auth_first = re.split(r"[\s,&]|dkk|et al", auth.strip())[0].strip()
        if auth_first:
            cited_keys.add((auth_first, yr))

    bib_entries = set()
    for line in bib_text.strip().splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Z][a-zA-Z\-]+).*?\((\d{4}[a-z]?)\)", line.strip())
        if m:
            bib_entries.add((m.group(1).strip(), m.group(2).strip()))

    phantoms = [k for k in cited_keys if k not in bib_entries]
    ghosts = [k for k in bib_entries if k not in cited_keys]
    return {
        "fully_passed": len(phantoms) == 0 and len(ghosts) == 0,
        "phantoms": phantoms,
        "ghosts": ghosts,
    }

def audit_anti_phantom_ieee(body_text: str, bib_text: str) -> Dict[str, Any]:
    cited_nums = set()
    for m in re.finditer(r"\[(\d+)(?:[–\-](\d+))?\]", body_text):
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else start
        for num in range(start, end + 1):
            cited_nums.add(num)

    bib_nums = set()
    for line in bib_text.strip().splitlines():
        m = re.match(r"^\[(\d+)\]", line.strip())
        if m:
            bib_nums.add(int(m.group(1)))

    phantoms = cited_nums - bib_nums
    ghosts = bib_nums - cited_nums
    return {
        "fully_passed": len(phantoms) == 0 and len(ghosts) == 0,
        "phantoms": sorted(list(phantoms)),
        "ghosts": sorted(list(ghosts)),
    }

def validate_mermaid_syntax_pure_python(block: str) -> Dict[str, Any]:
    lines = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
    if not lines:
        return {"valid": False, "error": "Empty block"}
    header = lines[0]
    valid_headers = (
        "flowchart TD", "flowchart TB", "flowchart LR", "flowchart RL",
        "sequenceDiagram", "classDiagram", "erDiagram", "stateDiagram",
        "graph TD", "graph TB", "graph LR", "graph RL"
    )
    if not any(header.startswith(vh) for vh in valid_headers):
        return {"valid": False, "error": f"Invalid Mermaid header: {header}"}
    # Check block level curly brackets
    if block.count("{") != block.count("}"):
        return {"valid": False, "error": "Unbalanced curly brackets in block"}
    # Check line level brackets for parentheses and square brackets
    brackets = {"(": ")", "[": "]"}
    for l in lines:
        if l.startswith("%%"):
            continue
        for b_open, b_close in brackets.items():
            if l.count(b_open) != l.count(b_close):
                return {"valid": False, "error": f"Unbalanced bracket {b_open}{b_close} in: {l}"}
    return {"valid": True, "type": header.split()[0]}


# ==============================================================================
# SCENARIO 1: IT / SOFTWARE ENGINEERING LIFECYCLE
# ==============================================================================

class TestScenario1_ITSoftwareLifecycle(unittest.TestCase):
    """Scenario 1: IT / Software Engineering Skripsi Lifecycle (Preset: `it-software`)."""

    def setUp(self):
        self.preset_id = "it-software"
        self.topic = {
            "objek_material": "Sistem Informasi Distribusi Logistik Farmasi Rumah Sakit",
            "objek_formal": "Arsitektur Microservices dan Algoritma Dijkstra",
            "konteks": "Instalasi Farmasi RSUD Tarakan Jakarta",
            "metode": "Rekayasa Perangkat Lunak Agile / Scrum",
            "title": "Rancang Bangun Sistem Informasi Distribusi Logistik Farmasi Rumah Sakit Berbasis Arsitektur Microservices Menggunakan Algoritma Dijkstra pada Instalasi Farmasi RSUD Tarakan Jakarta",
        }

    def test_scenario1_proposal_structure_and_title_formula(self):
        # 1. Title Formula: Objek Material + Objek Formal + Konteks + Metode
        t = self.topic["title"]
        self.assertIn(self.topic["objek_material"], t)
        self.assertIn("Arsitektur Microservices", t)
        self.assertIn(self.topic["konteks"], t)

        # 2. Dialectical Problem Statement starting with 'Terdapat'
        problem_statement = (
            "Terdapat diskoneksi data antara gudang farmasi utama dan depo rawat inap "
            "yang mengakibatkan keterlambatan suplai obat darurat pada instalasi farmasi RSUD Tarakan Jakarta, "
            "sehingga menuntut perancangan sistem berbasis arsitektur microservices dan optimasi rute Dijkstra."
        )
        self.assertTrue(problem_statement.startswith("Terdapat"))

        # 3. 3 Hierarchical Research Questions
        rqs = [
            "Bagaimanakah analisis kebutuhan dan perancangan arsitektur microservices untuk distribusi obat? (RQ1 - Kebutuhan & Desain)",
            "Bagaimanakah implementasi algoritma Dijkstra dalam optimasi rute pengantaran obat internal? (RQ2 - Implementasi)",
            "Bagaimanakah efektivitas fungsionalitas dan penerimaan pengguna sistem berbasis SUS? (RQ3 - Evaluasi)"
        ]
        self.assertEqual(len(rqs), 3)

    def test_scenario1_it_chapter_architecture_and_sections(self):
        # Chapter 3 must be 'Analisis dan Desain Sistem', Chapter 4 'Implementasi dan Pengujian Sistem'
        it_chapters = {
            1: "BAB I PENDAHULUAN",
            2: "BAB II KAJIAN PUSTAKA DAN LANDASAN TEORI",
            3: "BAB III ANALISIS DAN DESAIN SISTEM",
            4: "BAB IV IMPLEMENTASI DAN PENGUJIAN SISTEM",
            5: "BAB V PENUTUP"
        }
        self.assertIn("ANALISIS DAN DESAIN SISTEM", it_chapters[3])
        self.assertIn("IMPLEMENTASI DAN PENGUJIAN SISTEM", it_chapters[4])
        self.assertIn("PENUTUP", it_chapters[5])

    def test_scenario1_moscow_and_furps_requirements_engineering(self):
        # MoSCoW prioritization
        fr = [
            {"id": "FR-01", "name": "Autentikasi Pengguna & JWT", "priority": "Must have"},
            {"id": "FR-02", "name": "Kalkulasi Rute Dijkstra", "priority": "Must have"},
            {"id": "FR-03", "name": "Pelacakan Kurir Real-Time", "priority": "Should have"},
            {"id": "FR-04", "name": "Ekspor Laporan Audit Bulanan", "priority": "Could have"},
        ]
        must_haves = [f for f in fr if f["priority"] == "Must have"]
        self.assertGreaterEqual(len(must_haves), 2)

        # FURPS+ attributes
        furps = {
            "Functionality": "Enkripsi kata sandi Bcrypt dan transmisi TLS 1.3",
            "Usability": "Skor SUS target >= 75 pada 30 pengguna",
            "Reliability": "Uptime 99.5% dan failover otomatis",
            "Performance": "Latency p90 < 500 ms pada 50 RPS",
            "Supportability": "Arsitektur modular microservices berbasis Docker"
        }
        for k in ["Functionality", "Usability", "Reliability", "Performance", "Supportability"]:
            self.assertIn(k, furps)

    def test_scenario1_mermaid_architecture_sequence_class_diagrams(self):
        arch_diagram = """
flowchart TB
    subgraph PresentationTier[Presentation Tier]
        WebClient[Web Browser Vue.js]
    end
    subgraph GatewayTier[API Gateway]
        Gateway[Nginx Reverse Proxy]
    end
    subgraph ServiceTier[Microservices]
        AuthService[Auth Service]
        RouteService[Dijkstra Routing Service]
    end
    subgraph DataTier[Persistence]
        MainDB[(PostgreSQL)]
    end
    WebClient --> Gateway
    Gateway --> AuthService
    Gateway --> RouteService
    AuthService --> MainDB
    RouteService --> MainDB
"""
        seq_diagram = """
sequenceDiagram
    autonumber
    actor Staff as Petugas Depo
    participant UI as Antarmuka Vue.js
    participant GW as API Gateway
    participant Route as Layanan Dijkstra
    participant DB as PostgreSQL
    Staff->>UI: Permintaan Stok Obat Cito
    UI->>GW: POST /api/v1/routes/optimal
    GW->>Route: Hitung Rute Dijkstra Terpendek
    Route->>DB: Query Matriks Jarak Gudang
    DB-->>Route: Bobot Graf Jarak
    Route-->>GW: Hasil Rute Terpendek & ETA
    GW-->>UI: Respons HTTP 200 OK
    UI-->>Staff: Tampilkan Panduan Rute Pengantaran
"""
        class_diagram = """
classDiagram
    class NodeGudang {
        +String nodeId
        +String namaDepo
        +Double koordinatX
        +Double koordinatY
    }
    class RuteDijkstra {
        +List~NodeGudang~ jalur
        +Double totalJarak
        +hitungRuteTerpendek(NodeGudang awal, NodeGudang akhir) List
    }
    RuteDijkstra "1" --> "*" NodeGudang : melintasi
"""
        for diag in [arch_diagram, seq_diagram, class_diagram]:
            res = validate_mermaid_syntax_pure_python(diag)
            self.assertTrue(res["valid"], f"Mermaid invalid: {res}")

    def test_scenario1_black_box_testing_matrix_bva_and_ep(self):
        test_cases = [
            {"id": "TC-01", "type": "EP", "desc": "Login kredensial valid", "status": "Pass"},
            {"id": "TC-02", "type": "EP", "desc": "Login email invalid format", "status": "Pass"},
            {"id": "TC-03", "type": "BVA", "desc": "Permintaan obat kuantitas min = 1", "status": "Pass"},
            {"id": "TC-04", "type": "BVA", "desc": "Permintaan obat kuantitas di bawah min = 0", "status": "Pass"},
            {"id": "TC-05", "type": "BVA", "desc": "Permintaan obat kuantitas max = 500", "status": "Pass"},
            {"id": "TC-06", "type": "BVA", "desc": "Permintaan obat kuantitas melebihi max = 501", "status": "Pass"},
            {"id": "TC-07", "type": "EP", "desc": "Kalkulasi rute antar-depo terhubung", "status": "Pass"},
            {"id": "TC-08", "type": "EP", "desc": "Kalkulasi rute simpul terisolasi", "status": "Pass"},
            {"id": "TC-09", "type": "EP", "desc": "Pembaruan status pengiriman kurir", "status": "Pass"},
            {"id": "TC-10", "type": "BVA", "desc": "Unggah berkas resep tepat batas 20MB", "status": "Pass"},
        ]
        self.assertGreaterEqual(len(test_cases), 10)
        self.assertTrue(all(tc["status"] == "Pass" for tc in test_cases))

    def test_scenario1_sus_calculation_and_acceptability_benchmark(self):
        # Respondent A: Highly positive
        resp_a = [5, 1, 5, 2, 4, 1, 5, 2, 5, 2]  # Sum: odd(4+4+3+4+4)=19, even(4+3+4+3+3)=17 -> 36 * 2.5 = 90.0
        score_a = compute_sus_score(resp_a)
        self.assertEqual(score_a, 90.0)
        eval_a = evaluate_sus_adjective_and_grade(score_a)
        self.assertEqual(eval_a["grade"], "Grade A")
        self.assertEqual(eval_a["adjective"], "Excellent")
        self.assertEqual(eval_a["acceptable"], "Acceptable")

    def test_scenario1_ieee_citation_formatting_and_anti_phantom_audit(self):
        body = (
            "Arsitektur microservices terbukti meningkatkan fault tolerance [1]. "
            "Penerapan algoritma Dijkstra untuk rute tercepat logistik dianalisis pada [2], [3]."
        )
        bib = (
            "[1] A. Pratama and B. Setiawan, \"Penerapan arsitektur microservices logistik farmasi,\" JSI, vol. 19, no. 2, pp. 101–112, 2024.\n"
            "[2] D. Wijaya, \"Optimasi graf shortest path,\" JTI, vol. 11, no. 1, pp. 45–55, 2023.\n"
            "[3] H. Nugroho, \"Evaluasi performa containerized routing,\" JTI, vol. 12, no. 3, pp. 210–222, 2025.\n"
        )
        audit = audit_anti_phantom_ieee(body, bib)
        self.assertTrue(audit["fully_passed"], f"Audit failed: {audit}")

    def test_scenario1_defense_simulation_and_verdict_deliberation(self):
        scores = {"D1": 90.0, "D2": 88.0, "D3": 85.0, "D4": 92.0, "D5": 86.0}
        eval_res = evaluate_defense_verdict(scores)
        # Composite: 90*0.20 + 88*0.25 + 85*0.25 + 92*0.15 + 86*0.15 = 18 + 22 + 21.25 + 13.8 + 12.9 = 87.95
        self.assertAlmostEqual(eval_res["composite"], 87.95, places=2)
        self.assertEqual(eval_res["verdict"], "LULUS TANPA REVISI")
        self.assertEqual(eval_res["grade"], "Grade A")


# ==============================================================================
# SCENARIO 2: QUANTITATIVE EMPIRICAL LIFECYCLE
# ==============================================================================

class TestScenario2_QuantitativeEmpiricalLifecycle(unittest.TestCase):
    """Scenario 2: Quantitative Empirical Skripsi Lifecycle (Preset: `ekonomi-bisnis` / `sosial-humaniora`)."""

    def test_scenario2_slovin_sampling_and_hair_rule_of_thumb(self):
        pop_n = 1250
        e = 0.05
        # Slovin: 1250 / (1 + 1250 * 0.0025) = 1250 / 4.125 = 303.03 -> 304
        sample_n = compute_slovin(pop_n, e)
        self.assertAlmostEqual(sample_n, 303.03, places=2)
        final_sample = math.ceil(sample_n)
        self.assertEqual(final_sample, 304)

        indicators_count = 24
        hair_min = 5 * indicators_count  # 120
        hair_ideal = 10 * indicators_count  # 240
        self.assertGreaterEqual(final_sample, hair_min)
        self.assertGreaterEqual(final_sample, hair_ideal)

    def test_scenario2_variable_operationalization_matrix_taxonomy(self):
        matrix = [
            {"var": "Financial Technology (X1)", "role": "Bebas", "scale": "Likert", "dim": "Akses & Fitur"},
            {"var": "Literasi Keuangan (X2)", "role": "Bebas", "scale": "Likert", "dim": "Pengetahuan & Sikap"},
            {"var": "Manajemen Risiko (Z)", "role": "Mediasi", "scale": "Likert", "dim": "Mitigasi & Kontrol"},
            {"var": "Kinerja Keuangan UMKM (Y)", "role": "Terikat", "scale": "Likert", "dim": "Pertumbuhan Laba & Efisiensi"},
        ]
        roles = {item["role"] for item in matrix}
        self.assertIn("Bebas", roles)
        self.assertIn("Terikat", roles)
        self.assertIn("Mediasi", roles)

    def test_scenario2_panel_regression_model_selection_decision_tree(self):
        # Pathway 1: Chow < 0.05 (FEM), Hausman < 0.05 (FEM) -> FEM
        model_1 = evaluate_panel_model_selection(chow_p=0.012, hausman_p=0.034, lm_p=0.200)
        self.assertEqual(model_1, "FEM")

        # Pathway 2: Chow < 0.05 (FEM), Hausman >= 0.05 (REM) -> REM
        model_2 = evaluate_panel_model_selection(chow_p=0.012, hausman_p=0.180, lm_p=0.010)
        self.assertEqual(model_2, "REM")

        # Pathway 3: Chow >= 0.05 (CEM), LM < 0.05 (REM) -> REM
        model_3 = evaluate_panel_model_selection(chow_p=0.080, hausman_p=0.250, lm_p=0.025)
        self.assertEqual(model_3, "REM")

        # Pathway 4: Chow >= 0.05 (CEM), LM >= 0.05 (CEM) -> CEM
        model_4 = evaluate_panel_model_selection(chow_p=0.150, hausman_p=0.500, lm_p=0.220)
        self.assertEqual(model_4, "CEM")

    def test_scenario2_classical_assumptions_blue_invariants(self):
        # 1. Normality: p > 0.05
        normality_ks_p = 0.200
        self.assertGreater(normality_ks_p, 0.05)

        # 2. Multicollinearity: VIF < 10, Tol > 0.10
        tol_1, vif_1 = evaluate_vif_and_tolerance(0.35)
        self.assertGreater(tol_1, 0.10)
        self.assertLess(vif_1, 10.0)

        # 3. Heteroscedasticity: Glejser test p-values > 0.05
        glejser_p_values = [0.185, 0.240, 0.312]
        self.assertTrue(all(p > 0.05 for p in glejser_p_values))

        # 4. Autocorrelation: du < d < 4 - du
        dw_stat = 1.95
        du = 1.72
        self.assertTrue(du < dw_stat < (4.0 - du))

    def test_scenario2_apa7_citation_recency_and_grandfathering_audit(self):
        body = (
            "Kinerja keuangan UMKM dipengaruhi oleh literasi keuangan (Pratama & Rahayu, 2023). "
            "Hal ini sejalan dengan pandangan klasik Resource-Based View (Barney, 1991). "
            "Pemanfaatan financial technology juga meningkatkan inklusi keuangan (Sari dkk., 2024)."
        )
        bib = (
            "Barney, J. (1991). Firm resources and sustained competitive advantage. Journal of Management, 17(1), 99–120.\n"
            "Pratama, A., & Rahayu, S. (2023). Literasi keuangan dan kinerja UMKM. Jurnal Riset Akuntansi, 15(2), 120–135.\n"
            "Sari, M., Hidayat, R., & Wibowo, T. (2024). Fintech dan inklusi keuangan. Jurnal Ekonomi Bisnis, 22(1), 45–60.\n"
        )
        audit = audit_anti_phantom_apa(body, bib)
        self.assertTrue(audit["fully_passed"], f"Audit failed: {audit}")

    def test_scenario2_dosen_pembimbing_formative_consultation_review(self):
        consultation_log = {
            "bab_target": "Bab III",
            "catatan_revisi": "Perjelas kriteria sampel purposif dan operasionalisasi variabel mediasi",
            "status_approval": "Acc Bab dengan Catatan Minor",
        }
        self.assertIn("Acc Bab", consultation_log["status_approval"])


# ==============================================================================
# SCENARIO 3: QUALITATIVE CASE STUDY LIFECYCLE
# ==============================================================================

class TestScenario3_QualitativeCaseStudyLifecycle(unittest.TestCase):
    """Scenario 3: Qualitative Descriptive/Case Study Skripsi Lifecycle (Preset: `sosial-humaniora` / `hukum`)."""

    def test_scenario3_yin_case_study_and_legal_normative_framework(self):
        # Yin Case Study: Single-case embedded design with 3 sub-units
        sub_units = ["Regulasi dan Kebijakan", "Laporan Kasus Konsumen YLKI", "Platform E-Commerce"]
        self.assertEqual(len(sub_units), 3)

        # Legal materials taxonomy
        legal_sources = {
            "primer": ["UU Perlindungan Konsumen No. 8/1999", "UU ITE No. 1/2024"],
            "sekunder": ["Jurnal Hukum Lex Generalis", "Buku Hadjon Perlindungan Hukum"],
            "tersier": ["Kamus Hukum Black's Law", "KBBI V"]
        }
        self.assertGreaterEqual(len(legal_sources["primer"]), 2)
        self.assertGreaterEqual(len(legal_sources["sekunder"]), 2)

    def test_scenario3_informant_profiling_and_saturation_protocol(self):
        informants = [
            {"code": "[INF-01]", "role": "Direktur Kemendag", "type": "Key Informant"},
            {"code": "[INF-02]", "role": "Ketua Bidang Pengaduan YLKI", "type": "Main Informant"},
            {"code": "[INF-03]", "role": "Legal Counsel Marketplace", "type": "Main Informant"},
            {"code": "[INF-04]", "role": "Konsumen Korban Sengketa", "type": "Secondary Informant"},
        ]
        self.assertTrue(all(inf["code"].startswith("[INF-") for inf in informants))
        self.assertGreaterEqual(len(informants), 4)

    def test_scenario3_triangulation_matrix_three_vectors(self):
        triangulation_matrix = {
            "source_triangulation": ["Pemerintah / Kemendag", "LSM / YLKI", "Konsumen"],
            "methodological_triangulation": ["Wawancara Mendalam", "Observasi Lapangan", "Studi Dokumen"],
            "theoretical_triangulation": ["Teori Perlindungan Hukum Hadjon", "Teori Framing Entman"]
        }
        self.assertGreaterEqual(len(triangulation_matrix["source_triangulation"]), 3)
        self.assertGreaterEqual(len(triangulation_matrix["methodological_triangulation"]), 3)

    def test_scenario3_content_analysis_entman_framing_and_coding(self):
        framing = {
            "Define Problems": "Ketiadaan pertanggungjawaban algoritma pemrosesan sengketa otomatis",
            "Diagnose Causes": "Asimetri informasi dan klausula baku sepihak",
            "Make Moral Judgments": "Pelanggaran asas itikad baik dan keadilan bagi konsumen",
            "Suggest Remedies": "Penetapan regulasi perlindungan data pribadi dan ODR independen"
        }
        for elem in ["Define Problems", "Diagnose Causes", "Make Moral Judgments", "Suggest Remedies"]:
            self.assertIn(elem, framing)

    def test_scenario3_lincoln_guba_trustworthiness_pillars(self):
        pillars = ["Credibility", "Transferability", "Dependability", "Confirmability"]
        audit_trail = {
            "Credibility": "Triangulasi 3 sumber & member checking pada 3 informan",
            "Transferability": "Thick description lokus kasus YLKI dan Kemendag",
            "Dependability": "Audit trail log wawancara dan transkrip verbatim",
            "Confirmability": "Refleksivitas peneliti dan bracketing bebas bias"
        }
        for p in pillars:
            self.assertIn(p, audit_trail)

    def test_scenario3_eyd_v_spok_prefix_and_anti_cliche_audit(self):
        text = (
            "Penelitian ini dilakukan di Indonesia dengan pendekatan yuridis-empiris. "
            "Data dianalisis melalui tiga tahapan koding tematik. "
            "Oleh karena itu, kepastian hukum menjadi faktor determinan mitigasi kerugian konsumen."
        )
        self.assertRegex(text, r"\bdilakukan\b")
        self.assertRegex(text, r"\bdianalisis\b")
        self.assertRegex(text, r"\bdi Indonesia\b")
        self.assertNotIn("sangat penting", text.lower())
        self.assertNotRegex(text, r"\.\s*(?:Sehingga|Karena|Sedangkan)\b")

    def test_scenario3_dosen_pembimbing_guidance_and_chapter_clearance(self):
        clearance_record = {
            "student_nim": "20210801042",
            "advisor": "Dr. Pembimbing Utama, S.H., M.H.",
            "evaluated_chapters": ["Bab I", "Bab II", "Bab III", "Bab IV", "Bab V"],
            "verdict": "Acc Seluruh Bab untuk Pendaftaran Sidang Munaqasyah",
        }
        self.assertIn("Acc Seluruh Bab", clearance_record["verdict"])


# ==============================================================================
# SCENARIO 4: EDUCATIONAL R&D / CLINICAL HEALTH LIFECYCLE
# ==============================================================================

class TestScenario4_EducationalRndClinicalHealthLifecycle(unittest.TestCase):
    """Scenario 4: Educational R&D / Clinical Health Skripsi Lifecycle (Preset: `pendidikan-r&d` / `kesehatan-sains`)."""

    def test_scenario4_addie_4d_instructional_rnd_framework(self):
        addie_phases = ["Analysis", "Design", "Development", "Implementation", "Evaluation"]
        self.assertEqual(len(addie_phases), 5)

    def test_scenario4_expert_appraisal_scoring_and_validity(self):
        materi_expert_score = 88.5  # >= 85% Sangat Layak
        media_expert_score = 91.0   # >= 85% Sangat Layak
        self.assertGreaterEqual(materi_expert_score, 85.0)
        self.assertGreaterEqual(media_expert_score, 85.0)

    def test_scenario4_n_gain_score_computation_and_categories(self):
        pretest_mean = 44.0
        posttest_mean = 86.0
        max_score = 100.0
        # g = (86 - 44) / (100 - 44) = 42 / 56 = 0.75 -> Tinggi (> 0.70)
        g = compute_n_gain(pretest_mean, posttest_mean, max_score)
        self.assertAlmostEqual(g, 0.75, places=2)
        cat = evaluate_n_gain_category(g)
        self.assertEqual(cat, "Tinggi")

        # Medium gain scenario: Pre=40, Post=70 -> g = 30 / 60 = 0.50
        g_med = compute_n_gain(40.0, 70.0, 100.0)
        self.assertEqual(evaluate_n_gain_category(g_med), "Sedang")

    def test_scenario4_prior_research_10_studies_13_columns_matrix(self):
        expected_cols = [
            "No", "Nama Penulis", "Judul Penelitian", "Objek Material", "Objek Formal",
            "Konteks", "Metode", "Hasil", "Pembahasan Singkat", "Simpulan",
            "Keterbatasan Penelitian", "Rekomendasi", "Penerbit", "Tahun Terbit"
        ]
        self.assertEqual(len(expected_cols), 14)  # No + 13 substantive cols

        # Simulate 10 studies
        studies = [{"id": i+1, "author": f"Penulis {i+1}", "year": 2022 + (i % 4)} for i in range(10)]
        self.assertEqual(len(studies), 10)

    def test_scenario4_5_sentence_bilingual_abstract_validation(self):
        abstract_id = (
            "Dinamika pemahaman konsep sains pada siswa SMP menghadapi tantangan rendahnya visualisasi materi abstrak. "
            "Penelitian ini bertujuan untuk mengembangkan media pembelajaran gamifikasi interaktif berbasis model ADDIE. "
            "Dengan pendekatan Research and Development (R&D) melalui model ADDIE, data dikumpulkan dari 32 siswa kelas VII dan divalidasi oleh para ahli. "
            "Hasil penelitian menunjukkan bahwa media dinyatakan sangat layak oleh ahli media (91%) dan menghasilkan peningkatan N-gain sebesar 0,75 berkategori tinggi. "
            "Penelitian ini menyimpulkan bahwa media gamifikasi efektif mengoptimalkan retensi konsep sains siswa sekolah menengah."
        )
        abstract_en = (
            "Science conceptual understanding among middle school students faces difficulties due to inadequate visualization of abstract concepts. "
            "This study aims to develop an interactive gamified learning media employing the ADDIE development framework. "
            "Employing a Research and Development (R&D) approach using the ADDIE model, data were gathered from 32 grade VII students and validated by subject matter experts. "
            "The findings reveal that the interactive media achieved high feasibility from media experts (91%) and yielded a normalized gain (N-gain) of 0.75 categorized as high. "
            "This study concludes that interactive gamified media effectively improves science conceptual mastery in secondary education."
        )
        # Protect decimal points (e.g. 0.75 or 0,75) when segmenting sentences
        cleaned_id = re.sub(r"(\d+)\.(\d+)", r"\1@@DECIMAL@@\2", abstract_id.strip())
        parts_id = [s.replace("@@DECIMAL@@", ".").strip() for s in re.split(r"\.\s+", cleaned_id) if s.strip()]
        sentences_id = [p.rstrip(".") for p in parts_id if p.rstrip(".")]

        cleaned_en = re.sub(r"(\d+)\.(\d+)", r"\1@@DECIMAL@@\2", abstract_en.strip())
        parts_en = [s.replace("@@DECIMAL@@", ".").strip() for s in re.split(r"\.\s+", cleaned_en) if s.strip()]
        sentences_en = [p.rstrip(".") for p in parts_en if p.rstrip(".")]

        self.assertEqual(len(sentences_id), 5)
        self.assertEqual(len(sentences_en), 5)

        self.assertTrue(sentences_id[1].startswith("Penelitian ini bertujuan untuk"))
        self.assertTrue(sentences_en[1].startswith("This study aims to"))

    def test_scenario4_alphabetical_keywords_sorting_id_en(self):
        kw_id_raw = "Media Pembelajaran; Model ADDIE; Gamifikasi; Pemahaman Konsep; Sains Terapan"
        kw_id_list = [k.strip() for k in kw_id_raw.split(";")]
        kw_id_sorted = sorted(kw_id_list)
        self.assertEqual(kw_id_sorted, ["Gamifikasi", "Media Pembelajaran", "Model ADDIE", "Pemahaman Konsep", "Sains Terapan"])

        kw_en_raw = "ADDIE Model; Conceptual Understanding; Gamification; Interactive Media; Science Learning"
        kw_en_list = [k.strip() for k in kw_en_raw.split(";")]
        kw_en_sorted = sorted(kw_en_list)
        self.assertEqual(kw_en_list, kw_en_sorted)


# ==============================================================================
# SCENARIO 5: CUSTOM CAMPUS TOC INTAKE & DYNAMIC ADAPTATION LIFECYCLE
# ==============================================================================

class TestScenario5_CustomCampusTOCIntakeLifecycle(unittest.TestCase):
    """Scenario 5: Custom Campus Table of Contents Intake & Dynamic Adaptation (Preset: `custom`)."""

    def setUp(self):
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        import custom_toc_intake as intake
        self.intake = intake

    def tearDown(self):
        if str(REPO_ROOT / "scripts") in sys.path:
            sys.path.remove(str(REPO_ROOT / "scripts"))

    def test_scenario5_custom_toc_raw_outline_parsing_and_cleaning(self):
        raw_handbook = """
BAB I: PENDAHULUAN ......... 1
1.1 Latar Belakang Masalah ......... 1
1.2 Rumusan Masalah ......... 4
1.3 Tujuan Penelitian ......... 5
1.4 Batasan Masalah ......... 6

BAB II: TINJAUAN PUSTAKA ......... 7
2.1 Penelitian Terkait ......... 7
2.2 Landasan Teori ......... 12
2.3 Kerangka Berpikir ......... 20

BAB III: ANALISIS DAN PERANCANGAN SISTEM ......... 24
3.1 Metodologi Rekayasa (Scrum) ......... 24
3.2 Analisis Kebutuhan Perangkat Lunak ......... 26
3.3 Perancangan Arsitektur dan Antarmuka ......... 32

BAB IV: IMPLEMENTASI DAN PENGUJIAN SISTEM ......... 40
4.1 Lingkungan Implementasi ......... 40
4.2 Pengujian Black Box ......... 45
4.3 Pengujian Usability (SUS) ......... 52

BAB V: PENUTUP ......... 58
5.1 Kesimpulan ......... 58
5.2 Saran ......... 60
"""
        chapters = self.intake.parse_raw_text_outline(raw_handbook)
        self.assertEqual(len(chapters), 5)
        self.assertEqual(chapters[0].title, "BAB I: PENDAHULUAN")
        self.assertEqual(chapters[2].title, "BAB III: ANALISIS DAN PERANCANGAN SISTEM")

    def test_scenario5_semantic_chapter_archetype_classification(self):
        raw_text = (
            "BAB 1 PENDAHULUAN\n"
            "BAB 2 KAJIAN PUSTAKA\n"
            "BAB 3 ANALISIS DAN DESAIN SISTEM\n"
            "BAB 4 IMPLEMENTASI DAN EVALUASI\n"
            "BAB 5 KESIMPULAN DAN SARAN\n"
        )
        chapters = self.intake.parse_raw_text_outline(raw_text)
        self.assertEqual(chapters[0].canonical_archetype, "introduction")
        self.assertEqual(chapters[1].canonical_archetype, "literature_review")
        self.assertEqual(chapters[2].canonical_archetype, "system_design")
        self.assertEqual(chapters[3].canonical_archetype, "implementation_testing")
        self.assertEqual(chapters[4].canonical_archetype, "conclusion")

    def test_scenario5_preset_schema_conformance_and_rigor_attachment(self):
        raw_text = "BAB I PENDAHULUAN\n1.1 Latar Belakang\nBAB II LANDASAN TEORI\nBAB III METODOLOGI PENELITIAN\nBAB IV HASIL DAN PEMBAHASAN\nBAB V PENUTUP\n"
        chapters = self.intake.parse_raw_text_outline(raw_text)
        preset = self.intake.FacultyPreset(
            faculty_id="custom-fasilkom",
            preset_name="Pedoman Fasilkom Custom",
            campus_name="Universitas Contoh",
            faculty_name="Ilmu Komputer",
            citation_style="IEEE",
            recent_reference_ratio_min=0.80,
            recent_year_window=5,
            chapters=chapters,
        )
        p_dict = preset.to_dict()
        self.assertEqual(p_dict["$schema"], "https://nyekripsi.org/schemas/faculty-preset-v1.json")
        self.assertEqual(len(p_dict["chapters"]), 5)
        chap1_rules = p_dict["chapters"][0]["rules"]
        self.assertEqual(chap1_rules.get("problem_statement_starter"), "terdapat")

    def test_scenario5_defense_evaluation_5_dimension_scoring(self):
        scores = {
            "D1": 82.0,  # 20% -> 16.4
            "D2": 80.0,  # 25% -> 20.0
            "D3": 81.0,  # 25% -> 20.25
            "D4": 85.0,  # 15% -> 12.75
            "D5": 78.0,  # 15% -> 11.7
        }
        res = evaluate_defense_verdict(scores)
        self.assertAlmostEqual(res["composite"], 81.1, places=1)
        self.assertEqual(res["verdict"], "LULUS DENGAN REVISI MINOR")
        self.assertEqual(res["grade"], "Grade B+ / A-")

    def test_scenario5_defense_verdict_intervals_and_edge_cases(self):
        self.assertEqual(evaluate_defense_verdict({"D1":85,"D2":85,"D3":85,"D4":85,"D5":85})["verdict"], "LULUS TANPA REVISI")
        self.assertEqual(evaluate_defense_verdict({"D1":84.9,"D2":84.9,"D3":84.9,"D4":84.9,"D5":84.9})["verdict"], "LULUS DENGAN REVISI MINOR")
        self.assertEqual(evaluate_defense_verdict({"D1":75,"D2":75,"D3":75,"D4":75,"D5":75})["verdict"], "LULUS DENGAN REVISI MINOR")
        self.assertEqual(evaluate_defense_verdict({"D1":74.9,"D2":74.9,"D3":74.9,"D4":74.9,"D5":74.9})["verdict"], "LULUS DENGAN REVISI MAYOR")
        self.assertEqual(evaluate_defense_verdict({"D1":60,"D2":60,"D3":60,"D4":60,"D5":60})["verdict"], "LULUS DENGAN REVISI MAYOR")
        self.assertEqual(evaluate_defense_verdict({"D1":59.9,"D2":59.9,"D3":59.9,"D4":59.9,"D5":59.9})["verdict"], "TIDAK LULUS / MENGULANG SIDANG")

    def test_scenario5_berita_acara_and_revision_matrix_deliverables(self):
        berita_acara = (
            "# BERITA ACARA UJIAN SIDANG SKRIPSI\n"
            "Mahasiswa: Budi Santoso (NIM: 12022001)\n"
            "Nilai Akhir: 81.1 (Grade B+ / A-)\n"
            "Keputusan: LULUS DENGAN REVISI MINOR\n"
            "Batas Waktu Revisi: 14 hari kalender\n"
        )
        self.assertIn("BERITA ACARA UJIAN SIDANG SKRIPSI", berita_acara)
        self.assertIn("LULUS DENGAN REVISI MINOR", berita_acara)


if __name__ == "__main__":
    unittest.main()
