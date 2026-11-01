"""Comprehensive Pure Python Unit Test Suite for Milestone 1 (M1) Core Assets.

This test suite verifies all 14 files created for Milestone 1:
1. academic-paper/references/objek_material_formal_guide.md
2. academic-paper/references/teori_tiga_level_guide.md
3. academic-paper/references/skripsi_citation_standards.md
4. academic-paper/references/eyd_v_pedoman.md
5. shared/output_language_pair.md (id-en registration)
6. deep-research/templates/matriks_penelitian_terdahulu_13_kolom_template.md
7. academic-paper/templates/skripsi_bab1_template.md
8. academic-paper/templates/skripsi_bab2_template.md
9. academic-paper/templates/skripsi_bab3_template.md
10. academic-paper/templates/skripsi_bab4_template.md
11. academic-paper/templates/skripsi_bab5_template.md
12. academic-paper/templates/skripsi_proposal_template.md
13. academic-paper/templates/skripsi_bilingual_abstract_template.md
14. tests/test_skripsi_m1_core.py

Strictly pure Python stdlib (unittest, re, pathlib).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestObjekMaterialFormalGuide(unittest.TestCase):
    """Verifies the Objek Material vs Objek Formal reference guide."""

    def setUp(self) -> None:
        self.guide_path = ROOT / "academic-paper/references/objek_material_formal_guide.md"
        self.assertTrue(self.guide_path.is_file(), f"Missing {self.guide_path}")
        self.content = self.guide_path.read_text(encoding="utf-8")

    def test_epistemological_definitions(self) -> None:
        self.assertIn("Objek Material", self.content)
        self.assertIn("Objek Formal", self.content)
        self.assertIn("pisau analisis", self.content.lower())
        self.assertIn("matter of inquiry", self.content.lower())
        self.assertIn("perspective of inquiry", self.content.lower())

    def test_title_formula_enforcement(self) -> None:
        # Title Formula: Objek Material + Objek Formal + Konteks + Metode
        self.assertRegex(
            self.content,
            r"Objek[\\ \t\[\]*]*Material.*Objek[\\ \t\[\]*]*Formal.*Konteks.*Metode",
        )
        # Verifies 4 syntax patterns
        self.assertIn("Pola 1", self.content)
        self.assertIn("Pola 2", self.content)
        self.assertIn("Pola 3", self.content)
        self.assertIn("Pola 4", self.content)

    def test_multidisciplinary_exemplars(self) -> None:
        # Must cover social sciences, economics/business, informatics/SE, linguistics
        self.assertIn("SMA Negeri 1 Kota Bandung", self.content)
        self.assertIn("Pasar Beringharjo Yogyakarta", self.content)
        self.assertIn("PT Bio Sejahtera Indonesia", self.content)
        self.assertIn("LRT Jabodebek", self.content)

    def test_disciplinary_corridor_principles(self) -> None:
        self.assertIn("Prinsip Homologi Epistemik", self.content)
        self.assertIn("Prinsip Dualitas Terkendali", self.content)

    def test_anti_patterns_present(self) -> None:
        for code in ("AP-01", "AP-02", "AP-03", "AP-04", "AP-05"):
            self.assertIn(code, self.content)

    def test_self_check_rubric(self) -> None:
        self.assertIn("Kejelasan Objek Material", self.content)
        self.assertIn("Ketajaman Objek Formal", self.content)
        self.assertIn("Presisi Konteks", self.content)
        self.assertIn("Kesesuaian Metode", self.content)
        self.assertIn("Sintaks Judul & EYD V", self.content)
        self.assertIn("75", self.content)


class TestTeoriTigaLevelGuide(unittest.TestCase):
    """Verifies the 3-Tier Theory Hierarchy guide."""

    def setUp(self) -> None:
        self.guide_path = ROOT / "academic-paper/references/teori_tiga_level_guide.md"
        self.assertTrue(self.guide_path.is_file(), f"Missing {self.guide_path}")
        self.content = self.guide_path.read_text(encoding="utf-8")

    def test_three_levels_present(self) -> None:
        self.assertIn("Grand Theory", self.content)
        self.assertIn("Middle-Range Theory", self.content)
        self.assertIn("Applied / Operational Theory", self.content)
        self.assertIn("Pisau Analisis", self.content)

    def test_genealogical_tracing_protocol(self) -> None:
        self.assertIn("Akar Klasik", self.content)
        self.assertIn("Lintasan Evolusi", self.content)
        self.assertIn("Pemanfaatan Mutakhir", self.content)

    def test_dimension_reduction_protocol(self) -> None:
        self.assertIn("Reduksi Dimensi", self.content)
        self.assertIn("Depth Over Breadth", self.content)

    def test_traceability_matrix(self) -> None:
        self.assertIn("Traceability Matrix", self.content)
        self.assertIn("Indikator Empiris", self.content)

    def test_three_directional_discussion(self) -> None:
        self.assertIn("Arah 1: Mengonfirmasi", self.content)
        self.assertIn("Arah 2: Memperluas", self.content)
        self.assertIn("Arah 3: Membantah", self.content)

    def test_examiner_defense_questions(self) -> None:
        self.assertIn("Sidang Munaqasyah", self.content)
        # Should have at least 7 questions
        matches = re.findall(r"\d+\.\s+\*\"", self.content)
        self.assertGreaterEqual(len(matches), 7)


class TestSkripsiCitationStandardsGuide(unittest.TestCase):
    """Verifies citation standards, recency ratio, and anti-phantom rules."""

    def setUp(self) -> None:
        self.guide_path = ROOT / "academic-paper/references/skripsi_citation_standards.md"
        self.assertTrue(self.guide_path.is_file(), f"Missing {self.guide_path}")
        self.content = self.guide_path.read_text(encoding="utf-8")

    def test_apa_comparison_matrix(self) -> None:
        self.assertIn("APA 6th Edition", self.content)
        self.assertIn("APA 7th Edition", self.content)
        self.assertIn("Sentence case", self.content)

    def test_eighty_percent_journal_ratio(self) -> None:
        self.assertIn("80%", self.content)
        self.assertIn("Peer-Reviewed", self.content)

    def test_recency_rule(self) -> None:
        self.assertIn("3 (tiga) tahun terakhir", self.content)
        self.assertIn("5 tahun", self.content.lower())

    def test_bi_directional_anti_phantom_audit(self) -> None:
        self.assertIn("Forward Audit", self.content)
        self.assertIn("Reverse Audit", self.content)
        self.assertIn("Sitasi Phantom", self.content)
        self.assertIn("Ghost Entry", self.content)

    def test_indexing_bodies(self) -> None:
        for indexer in ("SINTA", "GARUDA", "Neliti", "Moraref", "Scopus", "Web of Science", "DOAJ"):
            self.assertIn(indexer, self.content)

    def test_reference_manager_integration(self) -> None:
        self.assertIn("Zotero", self.content)
        self.assertIn("Mendeley", self.content)
        self.assertIn("BibTeX", self.content)


class TestEydVPedoman(unittest.TestCase):
    """Verifies EYD V grammar, morpho-syntax, and anti-cliché standards."""

    def setUp(self) -> None:
        self.guide_path = ROOT / "academic-paper/references/eyd_v_pedoman.md"
        self.assertTrue(self.guide_path.is_file(), f"Missing {self.guide_path}")
        self.content = self.guide_path.read_text(encoding="utf-8")

    def test_regulatory_reference(self) -> None:
        self.assertIn("EYD Edisi Kelima", self.content)
        self.assertIn("Kepmendikbudristek No. 342/M/2022", self.content)

    def test_spok_and_sentence_fragments(self) -> None:
        self.assertIn("Kaidah SPOK", self.content)
        self.assertIn("Sentence Fragments", self.content)

    def test_di_morpho_syntactic_rule(self) -> None:
        self.assertIn("AWALAN KATA KERJA PASIF (DI- / KE-)", self.content)
        self.assertIn("KATA DEPAN PENUNJUK TEMPAT/WAKTU (DI / KE)", self.content)
        self.assertIn("dilakukan", self.content)
        self.assertIn("di laboratorium", self.content)

    def test_anti_cliche_rule_without_penting(self) -> None:
        self.assertIn("Evidence of Consequences", self.content)
        self.assertIn("DILARANG KERAS", self.content)
        self.assertIn("penting", self.content.lower())

    def test_banned_pseudo_conjunctions(self) -> None:
        self.assertIn("di mana", self.content.lower())
        self.assertIn("yang mana", self.content.lower())

    def test_standard_vocabulary_wordlist(self) -> None:
        pairs = [
            ("analisis", "analisa"),
            ("kuesioner", "kusioner"),
            ("kuasi-eksperimen", "quasy experiment"),
            ("hipotesis", "hipotesa"),
            ("sintesis", "sintesa"),
            ("metode", "metoda"),
            ("variabel", "variable"),
            ("orisinalitas", "orisinilitas"),
            ("simpulan", "kesimpulan"),
        ]
        for baku, non_baku in pairs:
            self.assertIn(baku, self.content)
            self.assertIn(non_baku, self.content)


class TestMatriks13KolomTemplate(unittest.TestCase):
    """Verifies the 13-column comparative prior research matrix template."""

    def setUp(self) -> None:
        self.template_path = ROOT / "deep-research/templates/matriks_penelitian_terdahulu_13_kolom_template.md"
        self.assertTrue(self.template_path.is_file(), f"Missing {self.template_path}")
        self.content = self.template_path.read_text(encoding="utf-8")

    def test_thirteen_column_headers(self) -> None:
        expected_columns = [
            "Nama Penulis",
            "Judul Penelitian",
            "Objek Material",
            "Objek Formal",
            "Konteks",
            "Metode",
            "Hasil",
            "Pembahasan Singkat",
            "Simpulan",
            "Keterbatasan Penelitian",
            "Rekomendasi",
            "Penerbit",
            "Tahun Terbit",
        ]
        for col in expected_columns:
            self.assertIn(col, self.content)

        # Check markdown table row has exactly No + 13 columns = 14 columns
        header_match = re.search(r"\|\s*No\s*\|.*Tahun Terbit\s*\|", self.content)
        self.assertIsNotNone(header_match)
        header_line = header_match.group(0)
        cells = [c.strip() for c in header_line.split("|")[1:-1]]
        self.assertEqual(len(cells), 14)  # No + 13 substantive columns
        self.assertEqual(cells[0], "No")
        self.assertEqual(cells[1:], expected_columns)

    def test_synthesis_protocol_steps(self) -> None:
        self.assertIn("Pemetaan Irisan", self.content)
        self.assertIn("Research Gap Taxonomy", self.content)
        self.assertIn("State-of-the-Art", self.content)
        self.assertIn("Research Positioning", self.content)
        self.assertIn("Novelty Proposition", self.content)
        self.assertIn("Non-Duplication Defense Assertion", self.content)

    def test_benchmark_example_present(self) -> None:
        self.assertIn("Astro di DKI Jakarta", self.content)
        self.assertIn("Technology Acceptance Model (TAM)", self.content)
        self.assertIn("Stimulus-Organism-Response (S-O-R)", self.content)


class TestSkripsiBabTemplates(unittest.TestCase):
    """Verifies all Chapter templates (Bab I - Bab V and Proposal)."""

    def test_bab1_template(self) -> None:
        path = ROOT / "academic-paper/templates/skripsi_bab1_template.md"
        self.assertTrue(path.is_file(), f"Missing {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("# BAB I: PENDAHULUAN", text)
        self.assertIn("## 1.1 Latar Belakang Masalah", text)
        self.assertIn("## 1.2 Rumusan Masalah", text)
        self.assertIn("## 1.3 Tujuan Penelitian", text)
        self.assertIn("## 1.4 Manfaat Penelitian", text)
        self.assertIn("## 1.5 Batasan Penelitian", text)
        self.assertIn("## 1.6 Sistematika Penulisan", text)
        # Check rule "Terdapat..."
        self.assertIn("Terdapat", text)
        # Check 3 RQs
        self.assertIn("RQ1", text)
        self.assertIn("RQ2", text)
        self.assertIn("RQ3", text)
        # Check Tujuan formula
        self.assertIn("Penelitian ini bertujuan untuk:", text)
        # Check 3 target practical benefits
        self.assertIn("Pengguna Bidang Keilmuan Internal", text)
        self.assertIn("Kalangan Akademisi dan Praktisi Umum", text)
        self.assertIn("Masyarakat Luas", text)

    def test_bab2_template(self) -> None:
        path = ROOT / "academic-paper/templates/skripsi_bab2_template.md"
        self.assertTrue(path.is_file(), f"Missing {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("# BAB II: KAJIAN PUSTAKA DAN KERANGKA BERPIKIR", text)
        self.assertIn("## 2.1 Penelitian Terdahulu", text)
        self.assertIn("## 2.2 Landasan Teori", text)
        self.assertIn("## 2.3 Kerangka Berpikir", text)
        self.assertIn("## 2.4 Hipotesis Penelitian / Proposisi Penelitian", text)
        # Check 13 columns table
        self.assertIn("Nama Penulis", text)
        self.assertIn("Tahun Terbit", text)
        # Check 3-level theory
        self.assertIn("Grand Theory", text)
        self.assertIn("Middle-Range Theory", text)
        self.assertIn("Applied / Operational Theory", text)
        self.assertIn("Reduksi Dimensi Teori", text)
        # Check 5 paragraphs in Kerangka Berpikir
        self.assertIn("Paragraf 1 (Jawaban Sementara RQ1", text)
        self.assertIn("Paragraf 2 (Jawaban Sementara RQ2", text)
        self.assertIn("Paragraf 3 (Jawaban Sementara RQ3", text)

    def test_bab3_template(self) -> None:
        path = ROOT / "academic-paper/templates/skripsi_bab3_template.md"
        self.assertTrue(path.is_file(), f"Missing {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("# BAB III: METODOLOGI PENELITIAN", text)
        self.assertIn("## 3.1 Pendekatan dan Jenis Penelitian", text)
        self.assertIn("## 3.2 Objek Material dan Objek Formal Penelitian", text)
        self.assertIn("## 3.3 Tempat dan Waktu Penelitian", text)
        self.assertIn("## 3.4 Teknik Pengumpulan Data dan Kisi-Kisi Instrumen", text)
        self.assertIn("## 3.5 Uji Validitas, Reliabilitas, dan Keabsahan Data", text)
        self.assertIn("## 3.6 Prosedur Analisis Data", text)
        # Check 3 sequential stages
        self.assertIn("Tahap 1: Inventarisasi Data", text)
        self.assertIn("Tahap 2: Klasifikasi Data", text)
        self.assertIn("Tahap 3: Penafsiran Data dengan Pisau Analisis", text)

    def test_bab4_template(self) -> None:
        path = ROOT / "academic-paper/templates/skripsi_bab4_template.md"
        self.assertTrue(path.is_file(), f"Missing {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("# BAB IV: HASIL PENELITIAN DAN PEMBAHASAN", text)
        self.assertIn("## 4.1 Deskripsi Objek Penelitian", text)
        self.assertIn("## 4.2 Hasil Penelitian", text)
        self.assertIn("## 4.3 Pembahasan (Diskusi Dialektis)", text)
        # Check RQ findings
        self.assertIn("Temuan Penelitian Pertanyaan 1 (RQ1)", text)
        self.assertIn("Temuan Penelitian Pertanyaan 2 (RQ2)", text)
        self.assertIn("Temuan Penelitian Pertanyaan 3 (RQ3)", text)
        # Check 3 theoretical directions in discussion
        self.assertIn("Arah 1: Mengonfirmasi", text)
        self.assertIn("Arah 2: Memperluas", text)
        self.assertIn("Arah 3: Membantah", text)
        # Check Novelty Proposition
        self.assertIn("Novelty Proposition", text)

    def test_bab5_template(self) -> None:
        path = ROOT / "academic-paper/templates/skripsi_bab5_template.md"
        self.assertTrue(path.is_file(), f"Missing {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("# BAB V: KESIMPULAN DAN SARAN", text)
        self.assertIn("## 5.1 Kesimpulan (Natijah Epistemis)", text)
        self.assertIn("## 5.2 Keterbatasan Penelitian", text)
        self.assertIn("## 5.3 Peluang Penelitian Masa Depan", text)
        self.assertIn("## 5.4 Saran dan Rekomendasi Terarah", text)
        # Check natijah rule and prohibition against raw numbers dump
        self.assertIn("natijah", text.lower())
        self.assertIn("LARANGAN MENYALIN ANGKA MENTAH", text)
        # Check 1-to-1 mapping to 3 target groups
        self.assertIn("Rekomendasi bagi Pengguna Bidang Keilmuan Internal", text)
        self.assertIn("Rekomendasi bagi Kalangan Akademisi dan Praktisi Umum", text)
        self.assertIn("Rekomendasi bagi Masyarakat Luas", text)

    def test_proposal_template(self) -> None:
        path = ROOT / "academic-paper/templates/skripsi_proposal_template.md"
        self.assertTrue(path.is_file(), f"Missing {path}")
        text = path.read_text(encoding="utf-8")
        self.assertIn("# PROPOSAL PENELITIAN SKRIPSI", text)
        self.assertIn("HALAMAN JUDUL PROPOSAL", text)
        self.assertIn("HALAMAN PERSETUJUAN SEMINAR PROPOSAL", text)
        self.assertIn("BAGIAN I: PENDAHULUAN", text)
        self.assertIn("BAGIAN II: KAJIAN PUSTAKA DAN KERANGKA BERPIKIR", text)
        self.assertIn("BAGIAN III: METODOLOGI PENELITIAN", text)
        self.assertIn("BAGIAN IV: RENCANA JADWAL DAN MATRIKS KERJA", text)
        self.assertIn("Gantt Chart", text)
        self.assertIn("BAGIAN V: RANCANGAN DAFTAR PUSTAKA", text)
        self.assertIn("80%", text)


class TestBilingualAbstractTemplate(unittest.TestCase):
    """Verifies the 5-sentence bilingual abstract template and examples."""

    def setUp(self) -> None:
        self.path = ROOT / "academic-paper/templates/skripsi_bilingual_abstract_template.md"
        self.assertTrue(self.path.is_file(), f"Missing {self.path}")
        self.content = self.path.read_text(encoding="utf-8")

    def test_structural_formula_present(self) -> None:
        self.assertIn("Kalimat 1 (S1)", self.content)
        self.assertIn("Kalimat 2 (S2)", self.content)
        self.assertIn("Kalimat 3 (S3)", self.content)
        self.assertIn("Kalimat 4 (S4)", self.content)
        self.assertIn("Kalimat 5 (S5)", self.content)

    def test_exact_sentence_opening_formulas(self) -> None:
        self.assertIn("Penelitian ini bertujuan untuk", self.content)
        self.assertIn("This study aims to", self.content)

    def test_keywords_rules(self) -> None:
        self.assertIn("Minimal 3 (tiga) dan maksimal 5 (lima) kata kunci", self.content)
        self.assertIn("alfabetis dari a ke z", self.content.lower())
        self.assertIn("titik koma", self.content.lower())

    def _count_sentences(self, text: str) -> int:
        """Counts sentences by scanning periods followed by space/capital letter."""
        cleaned = text.strip()
        # Remove parenthetical abbreviations and math expressions before counting
        cleaned = re.sub(r"\([^)]*\)", "", cleaned)
        sentences = [s.strip() for s in re.split(r"\.\s+", cleaned) if s.strip()]
        return len(sentences)

    def test_multidisciplinary_concrete_exemplars(self) -> None:
        # Check quantitative, qualitative, and IT/SE sections exist
        self.assertIn("5.1 Paradigma Kuantitatif", self.content)
        self.assertIn("5.2 Paradigma Kualitatif", self.content)
        self.assertIn("5.3 Paradigma IT & Software Engineering", self.content)

        # Check keywords in exemplars are strictly sorted alphabetically A-Z
        kw_sections = re.findall(r"\*\*(?:Kata Kunci|Keywords):\*\*\s*([^\n]+)", self.content)
        self.assertGreaterEqual(len(kw_sections), 6)  # 3 paradigms x 2 languages
        for kw_line in kw_sections:
            raw_keywords = [k.strip().rstrip(".") for k in kw_line.split(";") if k.strip()]
            self.assertGreaterEqual(len(raw_keywords), 3, f"Too few keywords: {kw_line}")
            self.assertLessEqual(len(raw_keywords), 5, f"Too many keywords: {kw_line}")
            sorted_keywords = sorted(raw_keywords, key=lambda s: s.lower())
            self.assertEqual(
                [k.lower() for k in raw_keywords],
                [k.lower() for k in sorted_keywords],
                f"Keywords not alphabetically sorted: {raw_keywords}",
            )


class TestOutputLanguagePairRegistration(unittest.TestCase):
    """Verifies that id-en is properly registered in shared/output_language_pair.md."""

    def setUp(self) -> None:
        self.path = ROOT / "shared/output_language_pair.md"
        self.assertTrue(self.path.is_file(), f"Missing {self.path}")
        self.content = self.path.read_text(encoding="utf-8")

    def test_id_en_registered_with_supported_status(self) -> None:
        self.assertIn("`id-en`", self.content)
        self.assertIn("Indonesian (`id`)", self.content)
        self.assertIn("supported", self.content)

    def test_legacy_default_preserved(self) -> None:
        self.assertIn("`zh-tw-en`", self.content)
        self.assertIn("default", self.content)

    def test_csc_parser_succeeds_on_real_file(self) -> None:
        from scripts import check_spec_consistency as csc
        registry = csc.parse_output_language_pair_registry(self.content)
        self.assertIn("zh-tw-en", registry)
        self.assertEqual(registry["zh-tw-en"]["status"], "default")
        self.assertIn("id-en", registry)
        self.assertEqual(registry["id-en"]["status"], "supported")
        self.assertEqual(registry["id-en"]["l1_language"], "Indonesian (`id`)")
        self.assertEqual(registry["id-en"]["l2_language"], "English (`en`)")


class TestUserRefinements(unittest.TestCase):
    """Verifies the 4 user requirement refinements incorporated into Milestone 1."""

    def test_campus_guideline_flexibility(self) -> None:
        # Check Bab 3 supports both classical and IT/SE structure
        bab3 = (ROOT / "academic-paper/templates/skripsi_bab3_template.md").read_text(encoding="utf-8")
        self.assertIn("BAB III: METODOLOGI PENELITIAN / ANALISIS DAN PERANCANGAN SISTEM", bab3)
        self.assertIn("ANALISIS DAN PERANCANGAN SISTEM", bab3)

        # Check Bab 4 supports both classical and IT/SE structure
        bab4 = (ROOT / "academic-paper/templates/skripsi_bab4_template.md").read_text(encoding="utf-8")
        self.assertIn("BAB IV: HASIL PENELITIAN DAN PEMBAHASAN / IMPLEMENTASI DAN PENGUJIAN SISTEM", bab4)
        self.assertIn("IMPLEMENTASI DAN PENGUJIAN SISTEM", bab4)

        # Check Bab 5 supports both classical (Kesimpulan dan Saran) and IT/SE (Penutup)
        bab5 = (ROOT / "academic-paper/templates/skripsi_bab5_template.md").read_text(encoding="utf-8")
        self.assertIn("BAB V: KESIMPULAN DAN SARAN / PENUTUP", bab5)
        self.assertIn("BAB V: PENUTUP", bab5)

    def test_mermaid_syntax_diagrams(self) -> None:
        # Check Kerangka Berpikir in Bab 2 uses valid Mermaid flowchart
        bab2 = (ROOT / "academic-paper/templates/skripsi_bab2_template.md").read_text(encoding="utf-8")
        self.assertIn("```mermaid", bab2)
        self.assertIn("graph TD", bab2)

        # Check Bab 3 has Mermaid flowchart, sequenceDiagram, and classDiagram
        bab3 = (ROOT / "academic-paper/templates/skripsi_bab3_template.md").read_text(encoding="utf-8")
        self.assertIn("flowchart TD", bab3)
        self.assertIn("sequenceDiagram", bab3)
        self.assertIn("classDiagram", bab3)

        # Check Bab 4 has Mermaid flowchart
        bab4 = (ROOT / "academic-paper/templates/skripsi_bab4_template.md").read_text(encoding="utf-8")
        self.assertIn("flowchart LR", bab4)

    def test_configurable_prior_research_count(self) -> None:
        matrix = (ROOT / "deep-research/templates/matriks_penelitian_terdahulu_13_kolom_template.md").read_text(encoding="utf-8")
        self.assertIn("Konfigurasi Jumlah Studi Terdahulu", matrix)
        self.assertIn("5 Studi", matrix)
        self.assertIn("10 Studi", matrix)
        self.assertIn("15 Studi", matrix)
        self.assertIn("20+ Studi", matrix)

    def test_multi_citation_styles_support(self) -> None:
        citations = (ROOT / "academic-paper/references/skripsi_citation_standards.md").read_text(encoding="utf-8")
        self.assertIn("IEEE Style", citations)
        self.assertIn("Harvard Style", citations)
        self.assertIn("Chicago Manual of Style", citations)
        # Check IEEE numeric format [1], [2]
        self.assertIn("[1]", citations)
        self.assertIn("[2]", citations)
        self.assertIn("numerik", citations.lower())


if __name__ == "__main__":
    unittest.main()

