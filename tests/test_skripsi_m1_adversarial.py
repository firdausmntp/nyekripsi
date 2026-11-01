"""Empirical Adversarial Test Suite for Milestone 1 (M1) Deliverables.

This suite stress-tests:
1. Citation & Recency Math Boundary Values (80% journal ratio, 3-5 year recency, grandfathering rule).
2. Anti-Phantom Forward & Reverse Audit Rules (synthetic corpora with phantoms & ghosts).
3. Multi-Style Citations (APA 6/7 Author-Date vs IEEE Numeric [1], [2]).
4. Mermaid Diagram Syntax Validation (Bab 2, 3, 4 templates via Mermaid engine & AST rules).
"""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Oracle & Verification Helpers for Citation & Recency Math
# ---------------------------------------------------------------------------


class ReferenceItem:
    def __init__(
        self,
        key: str,
        year: int,
        is_journal: bool,
        is_peer_reviewed: bool = True,
        is_seminal_classic: bool = False,
    ):
        self.key = key
        self.year = year
        self.is_journal = is_journal
        self.is_peer_reviewed = is_peer_reviewed
        self.is_seminal_classic = is_seminal_classic


def evaluate_citation_portfolio(
    references: list[ReferenceItem],
    current_year: int = 2026,
    strict_journal_ratio: float = 0.80,
    strict_recency_ratio: float = 0.80,
    max_recency_years: int = 5,
    max_classic_quota: float = 0.20,
) -> dict[str, any]:
    """Computes journal ratio and recency ratio adhering to Skripsi Citation Standards."""
    total = len(references)
    if total == 0:
        return {
            "valid": False,
            "error": "EMPTY_BIBLIOGRAPHY",
            "journal_ratio": 0.0,
            "recency_ratio": 0.0,
            "classic_ratio": 0.0,
        }

    peer_reviewed_journals = [
        r for r in references if r.is_journal and r.is_peer_reviewed
    ]
    journal_ratio = len(peer_reviewed_journals) / total

    # Recency window: within last max_recency_years
    min_recent_year = current_year - max_recency_years
    recent_sources = [r for r in references if r.year >= min_recent_year]
    recency_ratio = len(recent_sources) / total

    # Classic seminal papers (grandfathering rule)
    classic_sources = [
        r for r in references if r.is_seminal_classic and r.year < min_recent_year
    ]
    classic_ratio = len(classic_sources) / total

    # Grandfathering validation:
    # Classic seminal works must fit within the 20% non-journal / book quota
    non_recent_non_classic = [
        r for r in references if r.year < min_recent_year and not r.is_seminal_classic
    ]

    journal_ok = journal_ratio >= strict_journal_ratio
    recency_ok = recency_ratio >= strict_recency_ratio
    classic_ok = classic_ratio <= max_classic_quota and len(non_recent_non_classic) == 0

    valid = journal_ok and recency_ok and classic_ok

    return {
        "valid": valid,
        "total": total,
        "journal_count": len(peer_reviewed_journals),
        "journal_ratio": journal_ratio,
        "journal_ok": journal_ok,
        "recent_count": len(recent_sources),
        "recency_ratio": recency_ratio,
        "recency_ok": recency_ok,
        "classic_count": len(classic_sources),
        "classic_ratio": classic_ratio,
        "classic_ok": classic_ok,
        "non_recent_non_classic_count": len(non_recent_non_classic),
    }


# ---------------------------------------------------------------------------
# Oracle & Verification Helpers for Anti-Phantom & Multi-Style Audits
# ---------------------------------------------------------------------------

RE_APA_PARENTHETICAL_GROUP = re.compile(r"\(([^)]+)\)")
RE_APA_CHUNK = re.compile(
    r"^([A-Za-zÀ-ÖØ-öø-ÿ\s\.\-&]+(?:,\s*(?:dkk\.|et al\.))?),\s*(\d{4}[a-z]?)$"
)
RE_APA_NARRATIVE = re.compile(
    r"\b([A-Z][a-zA-ZÀ-ÖØ-öø-ÿ\-]+(?:\s+(?:dan|and|&)\s+[A-Z][a-zA-ZÀ-ÖØ-öø-ÿ\-]+|\s+(?:dkk\.|et al\.))?)\s*\((\d{4}[a-z]?)\)"
)
RE_IEEE_SINGLE = re.compile(r"\[(\d+)\]")
RE_IEEE_RANGE_BRACKETED = re.compile(r"\[(\d+)\]\s*[\–\-]\s*\[(\d+)\]")
RE_IEEE_RANGE_SINGLE_BRACKET = re.compile(r"\[(\d+)\s*[\–\-]\s*(\d+)\]")
RE_IEEE_MULTI = re.compile(r"\[(\d+(?:\s*,\s*\d+)+)\]")


def extract_apa_body_citations(body_text: str) -> set[tuple[str, str]]:
    """Extracts (PrimaryAuthor, Year) keys from body text in APA style."""
    citations = set()
    # 1. Parenthetical citations: (Author, Year) or (Author1, Year; Author2, Year)
    for group_match in RE_APA_PARENTHETICAL_GROUP.finditer(body_text):
        inner = group_match.group(1).strip()
        chunks = [c.strip() for c in inner.split(";")]
        for chunk in chunks:
            chunk_match = RE_APA_CHUNK.match(chunk)
            if chunk_match:
                author_part = chunk_match.group(1).strip()
                year = chunk_match.group(2).strip()
                first_author = (
                    author_part.split("&")[0]
                    .split(" dan ")[0]
                    .split(" and ")[0]
                    .split("dkk")[0]
                    .split("et al")[0]
                    .split(",")[0]
                    .strip()
                )
                citations.add((first_author, year))

    # 2. Narrative citations: Author (Year)
    for match in RE_APA_NARRATIVE.finditer(body_text):
        author_part = match.group(1).strip()
        year = match.group(2).strip()
        first_author = (
            author_part.split("&")[0]
            .split(" dan ")[0]
            .split(" and ")[0]
            .split("dkk")[0]
            .split("et al")[0]
            .strip()
        )
        citations.add((first_author, year))

    return citations


def extract_apa_bibliography_keys(bib_text: str) -> set[tuple[str, str]]:
    """Extracts (PrimaryAuthorLastName, Year) from APA reference list."""
    keys = set()
    pattern = re.compile(
        r"^([A-Z][a-zA-ZÀ-ÖØ-öø-ÿ\-]+),\s+[^(\n]+\((\d{4}[a-z]?)\)", re.MULTILINE
    )
    for match in pattern.finditer(bib_text):
        author = match.group(1).strip()
        year = match.group(2).strip()
        keys.add((author, year))
    return keys


def extract_ieee_body_citations(body_text: str) -> set[int]:
    """Extracts IEEE numeric citation indices [1], [2], [1]–[3], [1-3], [1, 2] from text."""
    indices = set()
    # 1. Range with individual brackets: [1]–[3] or [1]-[3]
    for match in RE_IEEE_RANGE_BRACKETED.finditer(body_text):
        start, end = int(match.group(1)), int(match.group(2))
        for i in range(start, end + 1):
            indices.add(i)

    # 2. Range inside single bracket: [1-3] or [1–3]
    for match in RE_IEEE_RANGE_SINGLE_BRACKET.finditer(body_text):
        start, end = int(match.group(1)), int(match.group(2))
        for i in range(start, end + 1):
            indices.add(i)

    # 3. Comma-separated inside single bracket: [1, 2, 3]
    for match in RE_IEEE_MULTI.finditer(body_text):
        for num in match.group(1).split(","):
            if num.strip().isdigit():
                indices.add(int(num.strip()))

    # 4. Single bracket: [1]
    for match in RE_IEEE_SINGLE.finditer(body_text):
        indices.add(int(match.group(1)))

    return indices


def extract_ieee_bibliography_indices(bib_text: str) -> set[int]:
    """Extracts IEEE reference list entry indices [1], [2], etc."""
    indices = set()
    pattern = re.compile(r"^\[(\d+)\]", re.MULTILINE)
    for match in pattern.finditer(bib_text):
        indices.add(int(match.group(1)))
    return indices


def audit_anti_phantom_apa(body_text: str, bib_text: str) -> dict[str, any]:
    """Performs forward & reverse audit for APA citations."""
    body_citations = extract_apa_body_citations(body_text)
    bib_keys = extract_apa_bibliography_keys(bib_text)

    # Normalize author names to lower-case for comparison
    bib_authors_by_year: dict[str, set[str]] = {}
    for author, year in bib_keys:
        bib_authors_by_year.setdefault(year, set()).add(author.lower())

    phantoms = []
    for author, year in body_citations:
        norm_author = author.lower()
        candidates = bib_authors_by_year.get(year, set())
        matched = any(norm_author in cand or cand in norm_author for cand in candidates)
        if not matched:
            phantoms.append((author, year))

    body_authors_by_year: dict[str, set[str]] = {}
    for author, year in body_citations:
        body_authors_by_year.setdefault(year, set()).add(author.lower())

    ghosts = []
    for author, year in bib_keys:
        norm_author = author.lower()
        candidates = body_authors_by_year.get(year, set())
        matched = any(norm_author in cand or cand in norm_author for cand in candidates)
        if not matched:
            ghosts.append((author, year))

    return {
        "phantoms": phantoms,
        "ghosts": ghosts,
        "forward_audit_passed": len(phantoms) == 0,
        "reverse_audit_passed": len(ghosts) == 0,
        "fully_passed": len(phantoms) == 0 and len(ghosts) == 0,
    }


def audit_anti_phantom_ieee(body_text: str, bib_text: str) -> dict[str, any]:
    """Performs forward & reverse audit for IEEE numeric citations."""
    body_indices = extract_ieee_body_citations(body_text)
    bib_indices = extract_ieee_bibliography_indices(bib_text)

    # Forward audit: body indices not in bib
    phantoms = sorted(list(body_indices - bib_indices))
    # Reverse audit: bib indices not in body
    ghosts = sorted(list(bib_indices - body_indices))

    return {
        "phantoms": phantoms,
        "ghosts": ghosts,
        "forward_audit_passed": len(phantoms) == 0,
        "reverse_audit_passed": len(ghosts) == 0,
        "fully_passed": len(phantoms) == 0 and len(ghosts) == 0,
    }


# ===========================================================================
# Test Cases
# ===========================================================================


class TestCitationRecencyMathStress(unittest.TestCase):
    """Adversarial stress-testing of citation ratios, boundary values, and grandfathering."""

    def test_exact_eighty_percent_boundary_values(self) -> None:
        # Case 1: 4 out of 5 = 80.0% -> PASS
        refs_4_of_5 = [ReferenceItem(f"r{i}", 2024, is_journal=True) for i in range(4)]
        refs_4_of_5.append(ReferenceItem("b1", 2024, is_journal=False))
        res = evaluate_citation_portfolio(refs_4_of_5, current_year=2026)
        self.assertTrue(res["valid"])
        self.assertEqual(res["journal_ratio"], 0.80)

        # Case 2: 3 out of 4 = 75.0% -> FAIL
        refs_3_of_4 = [ReferenceItem(f"r{i}", 2024, is_journal=True) for i in range(3)]
        refs_3_of_4.append(ReferenceItem("b1", 2024, is_journal=False))
        res = evaluate_citation_portfolio(refs_3_of_4, current_year=2026)
        self.assertFalse(res["valid"])
        self.assertFalse(res["journal_ok"])
        self.assertEqual(res["journal_ratio"], 0.75)

        # Case 3: 8 out of 10 = 80.0% -> PASS
        refs_8_of_10 = [ReferenceItem(f"r{i}", 2025, is_journal=True) for i in range(8)]
        refs_8_of_10.extend(
            [ReferenceItem(f"b{i}", 2025, is_journal=False) for i in range(2)]
        )
        res = evaluate_citation_portfolio(refs_8_of_10, current_year=2026)
        self.assertTrue(res["valid"])
        self.assertEqual(res["journal_ratio"], 0.80)

        # Case 4: 7 out of 10 = 70.0% -> FAIL
        refs_7_of_10 = [ReferenceItem(f"r{i}", 2025, is_journal=True) for i in range(7)]
        refs_7_of_10.extend(
            [ReferenceItem(f"b{i}", 2025, is_journal=False) for i in range(3)]
        )
        res = evaluate_citation_portfolio(refs_7_of_10, current_year=2026)
        self.assertFalse(res["valid"])
        self.assertFalse(res["journal_ok"])

        # Case 5: 79.9% Boundary test (799 out of 1000) -> Must NOT round up to 80%
        refs_799 = [ReferenceItem(f"r{i}", 2025, is_journal=True) for i in range(799)]
        refs_799.extend(
            [ReferenceItem(f"b{i}", 2025, is_journal=False) for i in range(201)]
        )
        res = evaluate_citation_portfolio(refs_799, current_year=2026)
        self.assertFalse(res["valid"])
        self.assertFalse(res["journal_ok"])
        self.assertAlmostEqual(res["journal_ratio"], 0.799, places=3)

        # Case 6: 80.0% Boundary test (800 out of 1000) -> PASS
        refs_800 = [ReferenceItem(f"r{i}", 2025, is_journal=True) for i in range(800)]
        refs_800.extend(
            [ReferenceItem(f"b{i}", 2025, is_journal=False) for i in range(200)]
        )
        res = evaluate_citation_portfolio(refs_800, current_year=2026)
        self.assertTrue(res["valid"])
        self.assertEqual(res["journal_ratio"], 0.80)

    def test_recency_window_boundary_values(self) -> None:
        # Base year: 2026. 5-year window: 2021..2026
        # Case 1: All published in 2021 (exactly 5 years old) -> RECENT
        refs_2021 = [ReferenceItem(f"r{i}", 2021, is_journal=True) for i in range(10)]
        res = evaluate_citation_portfolio(refs_2021, current_year=2026)
        self.assertTrue(res["valid"])
        self.assertEqual(res["recency_ratio"], 1.0)

        # Case 2: Published in 2020 (6 years old, not classic) -> OUTDATED
        refs_mixed = [ReferenceItem(f"r{i}", 2024, is_journal=True) for i in range(7)]
        refs_mixed.extend(
            [ReferenceItem(f"old{i}", 2020, is_journal=True) for i in range(3)]
        )
        res = evaluate_citation_portfolio(refs_mixed, current_year=2026)
        self.assertFalse(res["valid"])
        self.assertFalse(res["recency_ok"])
        self.assertEqual(res["recency_ratio"], 0.70)

    def test_classic_seminal_paper_grandfathering_rule(self) -> None:
        # Grandfathering Rule: Classical seminal works (Maslow 1943, Davis 1989) exempt from 5-year recency
        # but MUST fit within the max 20% non-journal / book quota.

        # Scenario A: 8 recent peer-reviewed journals (2024-2026) + 2 seminal classic books (1943, 1989)
        # Total = 10, Journals = 8 (80%), Recency = 8/10 (80%), Classic = 2/10 (20%) -> PASS!
        refs_scenario_a = [
            ReferenceItem(f"j{i}", 2025, is_journal=True) for i in range(8)
        ]
        refs_scenario_a.append(
            ReferenceItem("maslow1943", 1943, is_journal=False, is_seminal_classic=True)
        )
        refs_scenario_a.append(
            ReferenceItem("davis1989", 1989, is_journal=False, is_seminal_classic=True)
        )
        res_a = evaluate_citation_portfolio(refs_scenario_a, current_year=2026)
        self.assertTrue(res_a["valid"])
        self.assertTrue(res_a["journal_ok"])
        self.assertTrue(res_a["recency_ok"])
        self.assertTrue(res_a["classic_ok"])

        # Scenario B: 7 recent journals + 3 seminal classic papers
        # Total = 10, Journals = 7 (70% < 80%) -> FAIL on journal ratio and classic ratio > 20%!
        refs_scenario_b = [
            ReferenceItem(f"j{i}", 2025, is_journal=True) for i in range(7)
        ]
        refs_scenario_b.append(
            ReferenceItem("maslow1943", 1943, is_journal=False, is_seminal_classic=True)
        )
        refs_scenario_b.append(
            ReferenceItem("davis1989", 1989, is_journal=False, is_seminal_classic=True)
        )
        refs_scenario_b.append(
            ReferenceItem("ajzen1991", 1991, is_journal=False, is_seminal_classic=True)
        )
        res_b = evaluate_citation_portfolio(refs_scenario_b, current_year=2026)
        self.assertFalse(res_b["valid"])
        self.assertFalse(res_b["journal_ok"])
        self.assertFalse(res_b["recency_ok"])
        self.assertFalse(res_b["classic_ok"])

        # Scenario C: 8 recent journals + 1 seminal classic + 1 non-seminal outdated blog/book (2010)
        # Total = 10. Non-recent non-classic exists -> FAIL!
        refs_scenario_c = [
            ReferenceItem(f"j{i}", 2025, is_journal=True) for i in range(8)
        ]
        refs_scenario_c.append(
            ReferenceItem("maslow1943", 1943, is_journal=False, is_seminal_classic=True)
        )
        refs_scenario_c.append(
            ReferenceItem(
                "random_old_blog", 2010, is_journal=False, is_seminal_classic=False
            )
        )
        res_c = evaluate_citation_portfolio(refs_scenario_c, current_year=2026)
        self.assertFalse(res_c["valid"])
        self.assertFalse(res_c["classic_ok"])

    def test_empty_bibliography_guard(self) -> None:
        res = evaluate_citation_portfolio([], current_year=2026)
        self.assertFalse(res["valid"])
        self.assertEqual(res["error"], "EMPTY_BIBLIOGRAPHY")


class TestAntiPhantomForwardReverseAudit(unittest.TestCase):
    """Stress-tests forward audit (phantom detection) and reverse audit (ghost detection)."""

    def test_clean_apa_corpus(self) -> None:
        body = (
            "Menurut Pratama dan Setiawan (2022), arsitektur mikroservis meningkatkan ketahanan transaksi. "
            "Hal ini diperkuat oleh temuan empiris terdahulu (Wijaya dkk., 2023). "
            "Selain itu, model penerimaan teknologi terbukti andal (Davis, 1989)."
        )
        bib = (
            "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance. MIS Quarterly, 13(3), 319–340.\n"
            "Pratama, A., & Setiawan, B. (2022). Penerapan arsitektur mikroservis logistik. Jurnal Sistem Informasi, 18(1), 45–56.\n"
            "Wijaya, C., Setiawan, B., & Kusuma, D. (2023). Pengujian throughput sistem terdistribusi. Jurnal Teknologi, 12(2), 101–112.\n"
        )
        audit = audit_anti_phantom_apa(body, bib)
        self.assertTrue(audit["fully_passed"])
        self.assertEqual(len(audit["phantoms"]), 0)
        self.assertEqual(len(audit["ghosts"]), 0)

    def test_phantom_citation_detected_in_apa(self) -> None:
        # Body cites 'Kurniawan (2024)' which is MISSING from bibliography
        body = (
            "Penelitian ini merujuk pada temuan Kurniawan (2024) mengenai efisiensi database. "
            "Hal tersebut juga sesuai dengan Pratama dan Setiawan (2022)."
        )
        bib = "Pratama, A., & Setiawan, B. (2022). Penerapan arsitektur mikroservis logistik. Jurnal Sistem Informasi, 18(1), 45–56.\n"
        audit = audit_anti_phantom_apa(body, bib)
        self.assertFalse(audit["fully_passed"])
        self.assertFalse(audit["forward_audit_passed"])
        self.assertTrue(audit["reverse_audit_passed"])
        self.assertEqual(len(audit["phantoms"]), 1)
        self.assertEqual(audit["phantoms"][0][0], "Kurniawan")
        self.assertEqual(audit["phantoms"][0][1], "2024")

    def test_ghost_reference_detected_in_apa(self) -> None:
        # Bibliography has 'Hidayat (2023)' which is NEVER cited in body text
        body = "Pratama dan Setiawan (2022) mengemukakan pentingnya indexing pada relasional database."
        bib = (
            "Hidayat, R. (2023). Analisis performa caching Redis. Jurnal Komputasi, 15(2), 80–92.\n"
            "Pratama, A., & Setiawan, B. (2022). Penerapan arsitektur mikroservis logistik. Jurnal Sistem Informasi, 18(1), 45–56.\n"
        )
        audit = audit_anti_phantom_apa(body, bib)
        self.assertFalse(audit["fully_passed"])
        self.assertTrue(audit["forward_audit_passed"])
        self.assertFalse(audit["reverse_audit_passed"])
        self.assertEqual(len(audit["ghosts"]), 1)
        self.assertEqual(audit["ghosts"][0][0], "Hidayat")
        self.assertEqual(audit["ghosts"][0][1], "2023")

    def test_complex_apa_surface_forms(self) -> None:
        # Complex forms: Ampersand, dkk., hyphenated surname, semicolon multiple citations
        body = (
            "Penerapan model ini telah dikonfirmasi (Al-Jabri & Setiawan, 2022; Pratama dkk., 2021). "
            "Selanjutnya, Al-Jabri dan Setiawan (2022) mendemonstrasikan stabilitas jaringan."
        )
        bib = (
            "Al-Jabri, M., & Setiawan, B. (2022). Stabilitas jaringan sensor nirkabel. Jurnal Elektro, 10(1), 12–25.\n"
            "Pratama, A., Rahardjo, S., & Kusuma, D. (2021). Evaluasi throughput multi-hop. Jurnal Sistem Cerdas, 9(3), 50–65.\n"
        )
        audit = audit_anti_phantom_apa(body, bib)
        self.assertTrue(audit["fully_passed"], f"Audit failed: {audit}")

    def test_clean_ieee_numeric_corpus(self) -> None:
        body = (
            "Sebagaimana ditunjukkan pada [1], arsitektur RESTful mempermudah integrasi data. "
            "Efisiensi query basis data terbukti meningkat secara signifikan [2], [3]."
        )
        bib = (
            '[1] A. Pratama and B. Setiawan, "Penerapan algoritma Dijkstra," JSI, vol. 19, no. 2, pp. 145–158, 2023.\n'
            '[2] F. D. Davis, "Perceived usefulness," MIS Q., vol. 13, no. 3, pp. 319–340, 1989.\n'
            '[3] R. Hidayat, "Optimasi indexing PostgreSQL," JK, vol. 11, no. 1, pp. 12–20, 2024.\n'
        )
        audit = audit_anti_phantom_ieee(body, bib)
        self.assertTrue(audit["fully_passed"])
        self.assertEqual(len(audit["phantoms"]), 0)
        self.assertEqual(len(audit["ghosts"]), 0)

    def test_phantom_citation_detected_in_ieee(self) -> None:
        # Body cites [4] which does NOT exist in bibliography
        body = "Hasil eksperimen mengonfirmasi hipotesis awal [1], [2], dan modul pendukung [4]."
        bib = (
            '[1] A. Pratama and B. Setiawan, "Penerapan algoritma Dijkstra," JSI, 2023.\n'
            '[2] F. D. Davis, "Perceived usefulness," MIS Q., 1989.\n'
            '[3] R. Hidayat, "Optimasi indexing PostgreSQL," JK, 2024.\n'
        )
        audit = audit_anti_phantom_ieee(body, bib)
        self.assertFalse(audit["fully_passed"])
        self.assertFalse(audit["forward_audit_passed"])
        self.assertIn(4, audit["phantoms"])

    def test_ghost_reference_detected_in_ieee(self) -> None:
        # Bibliography defines [3] but body text only cites [1] and [2]
        body = "Sebagaimana dirumuskan oleh Pratama [1] dan dikembangkan pada [2], latensi menurun."
        bib = (
            '[1] A. Pratama, "Penerapan algoritma Dijkstra," JSI, 2023.\n'
            '[2] F. D. Davis, "Perceived usefulness," MIS Q., 1989.\n'
            '[3] R. Hidayat, "Entri hantu yang tidak pernah dikutip," JK, 2024.\n'
        )
        audit = audit_anti_phantom_ieee(body, bib)
        self.assertFalse(audit["fully_passed"])
        self.assertTrue(audit["forward_audit_passed"])
        self.assertFalse(audit["reverse_audit_passed"])
        self.assertIn(3, audit["ghosts"])

    def test_ieee_range_numeric_citations(self) -> None:
        # Body cites [1]–[3]
        body = "Berbagai studi terkait telah mendokumentasikan fenomena ini [1]–[3]."
        bib = (
            '[1] A. Pratama, "Studi 1," JSI, 2023.\n'
            '[2] B. Setiawan, "Studi 2," JSI, 2024.\n'
            '[3] C. Wijaya, "Studi 3," JSI, 2025.\n'
        )
        audit = audit_anti_phantom_ieee(body, bib)
        self.assertTrue(
            audit["fully_passed"], f"Failed to expand range citation: {audit}"
        )


class TestMermaidDiagramSyntaxEmpirical(unittest.TestCase):
    """Empirical validation of Mermaid diagrams in Chapter templates."""

    def test_all_template_diagrams_are_syntactically_valid(self) -> None:
        validator_script = Path(
            "/data/data/com.termux/files/usr/tmp/mermaid-test/validate.js"
        )
        if not validator_script.is_file():
            self.skipTest(
                f"Mermaid validator not available at {validator_script} (Termux-specific environment)"
            )
        proc = subprocess.run(
            ["node", str(validator_script)],
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(proc.returncode, 0, f"Validator failed: {proc.stderr}")
        results = json.loads(proc.stdout.strip())
        self.assertEqual(len(results), 5, f"Expected 5 diagrams, got {len(results)}")
        for item in results:
            self.assertEqual(
                item.get("status"),
                "ok",
                f"Mermaid syntax error in {item['file']} block #{item['block']}: {item.get('message')}",
            )

    def test_broken_mermaid_diagrams_fail_validation(self) -> None:
        validator_script = Path(
            "/data/data/com.termux/files/usr/tmp/mermaid-test/validate.js"
        )
        if not validator_script.is_file():
            self.skipTest(
                f"Mermaid validator environment not available at {validator_script}"
            )
        broken_test_script = """
const { JSDOM } = require('/data/data/com.termux/files/usr/tmp/mermaid-test/node_modules/jsdom');
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
global.window = dom.window;
global.document = dom.window.document;
global.DOMParser = dom.window.DOMParser;
global.Element = dom.window.Element;
global.Node = dom.window.Node;

import('/data/data/com.termux/files/usr/tmp/mermaid-test/node_modules/mermaid/dist/mermaid.core.mjs').then(async (m) => {
  const mermaid = m.default;
  mermaid.initialize({ startOnLoad: false });
  const brokenSnippets = [
    'flowchrt TD\\n A --> B',
    'graph TD\\n A[Unclosed bracket --> B',
    'sequenceDiagram\\n Pengguna ===>>> Frontend'
  ];
  let errorsCaught = 0;
  for (const s of brokenSnippets) {
    try {
      await mermaid.parse(s);
    } catch (e) {
      errorsCaught++;
    }
  }
  console.log(JSON.stringify({ total: brokenSnippets.length, errorsCaught }));
});
"""
        proc = subprocess.run(
            ["node", "-e", broken_test_script],
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(
            proc.returncode, 0, f"Broken snippet runner failed: {proc.stderr}"
        )
        res = json.loads(proc.stdout.strip())
        self.assertEqual(res["errorsCaught"], res["total"])


if __name__ == "__main__":
    unittest.main()
