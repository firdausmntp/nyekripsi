"""Unit and Integration Tests for nyekripsi Milestone 3.

Covers:
1. 8 `/skripsi-*` commands (existence, frontmatter, skill dispatch, release discipline).
2. Dosen Pembimbing & Penguji personas and byte-identical plugin mirroring.
3. Custom Table of Contents (TOC) intake engine and semantic classification.
4. Custom TOC mapper guide documentation and schema compliance.
5. Repository rebranding, write guard dual namespaces, and release invariants.

Pure standard library Python implementation without third-party dependencies.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SKRIPSI_COMMANDS = [
    "skripsi-full",
    "skripsi-proposal",
    "skripsi-matriks",
    "skripsi-bab",
    "skripsi-defense",
    "skripsi-citation",
    "skripsi-abstract",
    "skripsi-eyd",
]

EXPECTED_SKILL_TARGETS = {
    "skripsi-full": "academic-pipeline",
    "skripsi-proposal": "academic-paper",
    "skripsi-matriks": "deep-research",
    "skripsi-bab": "academic-paper",
    "skripsi-defense": "academic-paper-reviewer",
    "skripsi-citation": "academic-paper",
    "skripsi-abstract": "academic-paper",
    "skripsi-eyd": "academic-paper",
}


class TestSkripsiCommandsDiscoveryAndFrontmatter(unittest.TestCase):
    """Suite 1: Validates that all 8 skripsi commands exist and satisfy frontmatter invariants."""

    def test_all_8_skripsi_commands_exist(self):
        for name in SKRIPSI_COMMANDS:
            cmd_path = REPO_ROOT / "commands" / f"{name}.md"
            self.assertTrue(
                cmd_path.is_file(), f"Command file {cmd_path} does not exist"
            )

    def test_skripsi_commands_frontmatter_invariants(self):
        for name in SKRIPSI_COMMANDS:
            cmd_path = REPO_ROOT / "commands" / f"{name}.md"
            text = cmd_path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), f"{name}.md must start with ---")
            self.assertGreaterEqual(
                text.count("---"), 2, f"{name}.md frontmatter must terminate with ---"
            )

            frontmatter = text.split("---", 2)[1]
            # Exact name: <stem>
            name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
            self.assertIsNotNone(name_match, f"{name}.md missing name: in frontmatter")
            self.assertEqual(
                name_match.group(1).strip(),
                name,
                f"{name}.md frontmatter name must equal filename stem",
            )

            # disable-model-invocation: true
            vis_match = re.search(
                r"^disable-model-invocation:\s*(.+)$", frontmatter, re.MULTILINE
            )
            self.assertIsNotNone(
                vis_match, f"{name}.md missing disable-model-invocation"
            )
            self.assertEqual(
                vis_match.group(1).strip(),
                "true",
                f"{name}.md disable-model-invocation must be true",
            )

            # description present
            desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
            self.assertIsNotNone(desc_match, f"{name}.md missing description")
            self.assertTrue(
                len(desc_match.group(1).strip()) > 10,
                f"{name}.md description too short",
            )

    def test_skripsi_commands_skill_dispatch(self):
        for name, expected_target in EXPECTED_SKILL_TARGETS.items():
            cmd_path = REPO_ROOT / "commands" / f"{name}.md"
            text = cmd_path.read_text(encoding="utf-8")

            expected_call = f'First invoke the Skill tool with `skill: "academic-research-skills:{expected_target}"`.'
            self.assertIn(
                expected_call,
                text,
                f"{name}.md missing explicit Skill call for {expected_target}",
            )

            mode_ref = f"Mode reference: `${{CLAUDE_PLUGIN_ROOT}}/MODE_REGISTRY.md`"
            self.assertIn(mode_ref, text, f"{name}.md missing rooted mode reference")

            skill_ref = (
                f"Skill entry: `${{CLAUDE_PLUGIN_ROOT}}/{expected_target}/SKILL.md`."
            )
            self.assertIn(skill_ref, text, f"{name}.md missing rooted skill entry")

            stop_clause = (
                "do not substitute this command summary for the mode instructions."
            )
            self.assertIn(stop_clause, text, f"{name}.md missing fallback stop clause")

    def test_backward_compatibility_ars_commands_intact(self):
        ars_commands = [
            "ars-3w",
            "ars-abstract",
            "ars-cache-invalidate",
            "ars-citation-check",
            "ars-disclosure",
            "ars-format-convert",
            "ars-full",
            "ars-lit-review",
            "ars-mark-read",
            "ars-outline",
            "ars-plan",
            "ars-rebuttal-audit",
            "ars-reviewer",
            "ars-revision-coach",
            "ars-revision",
            "ars-unmark-read",
        ]
        for name in ars_commands:
            cmd_path = REPO_ROOT / "commands" / f"{name}.md"
            self.assertTrue(
                cmd_path.is_file(), f"Original command {cmd_path} must remain intact"
            )

        total_commands = list((REPO_ROOT / "commands").glob("*.md"))
        self.assertEqual(
            len(total_commands),
            24,
            f"Expected 24 commands total (16 ars + 8 skripsi), got {len(total_commands)}",
        )

    def test_command_invariants_lint_execution(self):
        res = subprocess.run(
            [
                sys.executable,
                "tools/release-discipline/scripts/check_command_invariants.py",
                "--manifest",
                ".command-invariants.toml",
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            res.returncode,
            0,
            f"check_command_invariants.py failed:\n{res.stdout}\n{res.stderr}",
        )
        self.assertIn("26 pass, 0 fail, 0 skip", res.stdout)


class TestSkripsiAgentPersonasAndMirroring(unittest.TestCase):
    """Suite 2: Validates Pembimbing & Penguji personas, content rubrics, and byte-identical mirroring."""

    def test_pembimbing_agent_file_and_mirror_sync(self):
        src = REPO_ROOT / "academic-paper" / "agents" / "pembimbing_agent.md"
        dst = REPO_ROOT / "agents" / "pembimbing_agent.md"
        self.assertTrue(src.is_file(), f"Canonical source {src} does not exist")
        self.assertTrue(dst.is_file(), f"Plugin mirror {dst} does not exist")
        self.assertFalse(
            dst.is_symlink(),
            f"Mirror {dst} must be a regular file, not a symlink (#413)",
        )
        self.assertEqual(
            src.read_bytes(),
            dst.read_bytes(),
            f"Mirror {dst} must be byte-identical to {src}",
        )

    def test_penguji_agent_file_and_mirror_sync(self):
        src = REPO_ROOT / "academic-paper-reviewer" / "agents" / "penguji_agent.md"
        dst = REPO_ROOT / "agents" / "penguji_agent.md"
        self.assertTrue(src.is_file(), f"Canonical source {src} does not exist")
        self.assertTrue(dst.is_file(), f"Plugin mirror {dst} does not exist")
        self.assertFalse(
            dst.is_symlink(),
            f"Mirror {dst} must be a regular file, not a symlink (#413)",
        )
        self.assertEqual(
            src.read_bytes(),
            dst.read_bytes(),
            f"Mirror {dst} must be byte-identical to {src}",
        )

    def test_agents_mirror_sync_script_passes(self):
        res = subprocess.run(
            [sys.executable, "scripts/check_agents_mirror_sync.py"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            res.returncode,
            0,
            f"check_agents_mirror_sync.py failed:\n{res.stdout}\n{res.stderr}",
        )

    def test_pembimbing_agent_content_and_rubrics(self):
        src = REPO_ROOT / "academic-paper" / "agents" / "pembimbing_agent.md"
        text = src.read_text(encoding="utf-8")

        # Dual identity
        self.assertIn("Pembimbing 1", text)
        self.assertIn("Pembimbing 2", text)

        # Core concepts
        self.assertIn("Objek Material", text)
        self.assertIn("Objek Formal", text)
        self.assertIn("terdapat", text)
        self.assertIn("Grand Theory", text)
        self.assertIn("Middle-Range Theory", text)
        self.assertIn("Applied Theory", text)
        self.assertIn("Matriks Penelitian Terdahulu", text)
        self.assertIn("13 Kolom", text)
        self.assertIn("Mermaid", text)
        self.assertIn("80%", text)
        self.assertIn("anti-phantom", text.lower())
        self.assertIn("EYD V", text)

        # Formative deliverable
        self.assertIn("LEMBAR CATATAN KONSULTASI BIMBINGAN SKRIPSI", text)
        self.assertIn("Revisi Total", text)
        self.assertIn("Revisi Minor", text)
        self.assertIn("Acc Bab", text)

    def test_penguji_agent_content_and_defense_verdicts(self):
        src = REPO_ROOT / "academic-paper-reviewer" / "agents" / "penguji_agent.md"
        text = src.read_text(encoding="utf-8")

        # Board composition
        self.assertIn("Ketua", text)
        self.assertIn("Anggota Penguji", text)

        # 5-dimension rubrics
        self.assertIn("D1: Substansi", text)
        self.assertIn("D2: Metodologi", text)
        self.assertIn("D3: Hasil, Kebaruan", text)
        self.assertIn("D4: Sistematika", text)
        self.assertIn("D5: Penguasaan Materi", text)

        # 4 official Indonesian verdicts
        self.assertIn("LULUS TANPA REVISI", text)
        self.assertIn("LULUS DENGAN REVISI MINOR", text)
        self.assertIn("LULUS DENGAN REVISI MAYOR", text)
        self.assertTrue("TIDAK LULUS" in text or "MENGULANG SIDANG" in text)

        # Deliverable template
        self.assertIn("BERITA ACARA UJIAN SIDANG SKRIPSI", text)

    def test_personas_canonical_boundary_and_bucket_c(self):
        for path in [
            REPO_ROOT / "academic-paper" / "agents" / "pembimbing_agent.md",
            REPO_ROOT / "academic-paper-reviewer" / "agents" / "penguji_agent.md",
        ]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("<!-- canonical:instruction-data-boundary -->", text)
            self.assertIn("<!-- /canonical:instruction-data-boundary -->", text)
            # Must NOT contain single-phase fence because they are Bucket C
            self.assertNotIn("## Phase Boundary (v3.9.2)", text)
            self.assertNotIn("## Phase Boundary (v3.9.4)", text)

    def test_skripsi_defense_command_synchronization_with_penguji_agent(self):
        cmd_file = REPO_ROOT / "commands" / "skripsi-defense.md"
        agent_file = (
            REPO_ROOT / "academic-paper-reviewer" / "agents" / "penguji_agent.md"
        )
        cmd_text = cmd_file.read_text(encoding="utf-8")
        agent_text = agent_file.read_text(encoding="utf-8")

        # Rubric weights in command summary must match canonical agent exactly: 20%, 25%, 25%, 15%, 15%
        cmd_weights = [int(w) for w in re.findall(r"Bobot\s+(\d+)%", cmd_text)]
        agent_weights = [
            int(m)
            for m in re.findall(
                r"\|\s*\*\*D\d+:[^*]+\*\*\s*\|\s*(\d+)%\s*\|", agent_text
            )
        ]
        self.assertEqual(
            cmd_weights, [20, 25, 25, 15, 15], f"Command weights: {cmd_weights}"
        )
        self.assertEqual(
            agent_weights, [20, 25, 25, 15, 15], f"Agent weights: {agent_weights}"
        )
        self.assertEqual(
            cmd_weights,
            agent_weights,
            "Command weights must synchronize with penguji_agent.md",
        )

        # Official Indonesian verdict intervals and passing threshold
        self.assertIn("LULUS TANPA REVISI` (Grade A, Skor 85 - 100)", cmd_text)
        self.assertIn(
            "LULUS DENGAN REVISI MINOR` (Grade B+ / A-, Skor 75 - 84", cmd_text
        )
        self.assertIn(
            "LULUS DENGAN REVISI MAYOR` (Grade B / C+, Skor 60 - 74", cmd_text
        )
        self.assertIn(
            "TIDAK LULUS / MENGULANG SIDANG` (Grade C / D / E, Skor < 60", cmd_text
        )

        # Regress against old flawed threshold (< 65)
        self.assertNotIn(
            "Skor < 65",
            cmd_text,
            "Failing threshold in skripsi-defense.md must be < 60, not < 65",
        )


class TestCustomTocIntakeEngine(unittest.TestCase):
    """Suite 3: Tests custom TOC CLI, parser, format handling, and semantic classification."""

    def setUp(self):
        # Import intake module dynamically
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        import custom_toc_intake as intake

        self.intake = intake

    def tearDown(self):
        if str(REPO_ROOT / "scripts") in sys.path:
            sys.path.remove(str(REPO_ROOT / "scripts"))

    def test_clean_section_title_removes_page_numbers(self):
        cases = [
            ("1.1 Latar Belakang Masalah ......... 12", "1.1 Latar Belakang Masalah"),
            ("1.2 Rumusan Masalah --------------- 15", "1.2 Rumusan Masalah"),
            ("- 1.3 Tujuan Penelitian   20", "1.3 Tujuan Penelitian"),
            ("* 2.1 Tinjauan Pustaka", "2.1 Tinjauan Pustaka"),
        ]
        for inp, expected in cases:
            self.assertEqual(self.intake.clean_section_title(inp), expected)

    def test_archetype_semantic_classification(self):
        classify = self.intake.classify_archetype
        self.assertEqual(classify("BAB I: PENDAHULUAN"), "introduction")
        self.assertEqual(
            classify("BAB II: TINJAUAN PUSTAKA DAN LANDASAN TEORI"), "literature_review"
        )
        self.assertEqual(
            classify("BAB III: ANALISIS DAN PERANCANGAN SISTEM"), "system_design"
        )
        self.assertEqual(classify("BAB III: METODE PENELITIAN"), "methodology")
        self.assertEqual(
            classify("BAB IV: IMPLEMENTASI DAN PENGUJIAN SISTEM"),
            "implementation_testing",
        )
        self.assertEqual(
            classify("BAB IV: HASIL PENELITIAN DAN PEMBAHASAN"), "results_discussion"
        )
        self.assertEqual(classify("BAB V: KESIMPULAN DAN SARAN"), "conclusion")

    def test_parse_raw_text_outline_roman_numerals(self):
        raw = """
        BAB I PENDAHULUAN
        1.1 Latar Belakang Masalah ...... 1
        1.2 Rumusan Masalah ...... 4
        1.3 Tujuan Penelitian ...... 5
        BAB II TINJAUAN PUSTAKA
        2.1 Penelitian Terdahulu ...... 7
        2.2 Landasan Teori ...... 12
        BAB III METODOLOGI PENELITIAN
        3.1 Desain Penelitian ...... 20
        3.2 Populasi dan Sampel ...... 22
        BAB IV HASIL DAN PEMBAHASAN
        4.1 Deskripsi Data ...... 30
        4.2 Pembahasan ...... 45
        BAB V PENUTUP
        5.1 Kesimpulan ...... 60
        5.2 Saran ...... 62
        """
        chapters = self.intake.parse_raw_text_outline(raw)
        self.assertEqual(len(chapters), 5)
        self.assertEqual(chapters[0].canonical_archetype, "introduction")
        self.assertEqual(chapters[0].number, 1)
        self.assertEqual(chapters[0].roman_number, "I")
        self.assertEqual(len(chapters[0].required_sections), 3)

        self.assertEqual(chapters[1].canonical_archetype, "literature_review")
        self.assertEqual(chapters[2].canonical_archetype, "methodology")
        self.assertEqual(chapters[3].canonical_archetype, "results_discussion")
        self.assertEqual(chapters[4].canonical_archetype, "conclusion")

    def test_parse_raw_text_outline_arabic_numerals(self):
        raw = """
        BAB 1 PENDAHULUAN
        1.1 Latar Belakang
        1.2 Rumusan Masalah
        BAB 2 LANDASAN TEORI
        2.1 Teori Terkait
        BAB 3 ANALISIS DAN DESAIN SISTEM
        3.1 Analisis Kebutuhan
        3.2 Desain Arsitektur
        BAB 4 IMPLEMENTASI DAN EVALUASI
        4.1 Implementasi Fitur
        4.2 Pengujian Black Box
        BAB 5 PENUTUP
        5.1 Simpulan
        """
        chapters = self.intake.parse_raw_text_outline(raw)
        self.assertEqual(len(chapters), 5)
        self.assertEqual(chapters[2].canonical_archetype, "system_design")
        self.assertEqual(chapters[3].canonical_archetype, "implementation_testing")

    def test_automatic_rule_attachment(self):
        raw = """
        BAB I PENDAHULUAN
        1.1 Latar Belakang
        BAB II KAJIAN PUSTAKA
        2.1 Penelitian Terkait
        BAB III ANALISIS DAN PERANCANGAN SISTEM
        3.1 Desain Sistem
        BAB IV IMPLEMENTASI DAN PENGUJIAN
        4.1 Pengujian
        BAB V PENUTUP
        5.1 Simpulan
        """
        preset = self.intake.parse_input_source(raw)
        chaps = {c.number: c for c in preset.chapters}

        # Intro rules
        self.assertEqual(chaps[1].rules.get("problem_statement_starter"), "terdapat")
        self.assertEqual(chaps[1].rules.get("min_research_questions"), 3)

        # Lit review rules
        self.assertEqual(chaps[2].rules.get("min_prior_studies"), 10)
        self.assertTrue(chaps[2].rules.get("comparative_matrix_13_columns"))

        # Implementation rules
        self.assertEqual(chaps[4].rules.get("min_blackbox_cases"), 10)
        self.assertTrue(chaps[4].rules.get("sus_evaluation_required"))

        # Conclusion rules
        self.assertTrue(chaps[5].rules.get("natijah_epistemic_conclusion"))

    def test_parse_valid_json_input(self):
        sample_json = {
            "$schema": "https://nyekripsi.org/schemas/faculty-preset-v1.json",
            "faculty_id": "test-faculty",
            "preset_name": "Test Faculty Preset",
            "campus_name": "Universitas Uji Coba",
            "faculty_name": "Fakultas Uji Coba",
            "citation_style": "IEEE",
            "recent_reference_ratio_min": 0.85,
            "recent_year_window": 3,
            "chapters": [
                {
                    "number": 1,
                    "roman_number": "I",
                    "canonical_archetype": "introduction",
                    "title": "BAB I: PENDAHULUAN",
                    "required_sections": ["1.1 Latar Belakang", "1.2 Rumusan Masalah"],
                }
            ],
        }
        preset = self.intake.parse_input_source(json.dumps(sample_json))
        self.assertEqual(preset.faculty_id, "test-faculty")
        self.assertEqual(preset.citation_style, "IEEE")
        self.assertEqual(preset.recent_reference_ratio_min, 0.85)
        self.assertEqual(len(preset.chapters), 1)

    def test_error_handling_invalid_input(self):
        with self.assertRaises(ValueError):
            self.intake.parse_raw_text_outline(
                "Just some random text with no chapters at all"
            )

    def test_cli_execution_help_and_validate(self):
        res = subprocess.run(
            [sys.executable, "scripts/custom_toc_intake.py", "--help"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("custom_toc_intake.py", res.stdout)

    def test_parse_raw_text_outline_indonesian_word_numbers(self):
        raw = """
        BAB SATU: PENDAHULUAN
        1.1 Latar Belakang
        1.2 Rumusan Masalah
        BAB DUA: TINJAUAN PUSTAKA
        2.1 Landasan Teori
        2.2 Penelitian Terdahulu
        BAB TIGA: METODE PENELITIAN
        3.1 Desain Penelitian
        BAB EMPAT: HASIL DAN PEMBAHASAN
        4.1 Deskripsi Data
        4.2 Pembahasan
        BAB LIMA: PENUTUP
        5.1 Simpulan
        5.2 Saran
        """
        chapters = self.intake.parse_raw_text_outline(raw)
        self.assertEqual(len(chapters), 5)
        self.assertEqual([c.number for c in chapters], [1, 2, 3, 4, 5])
        self.assertEqual(
            [c.roman_number for c in chapters], ["I", "II", "III", "IV", "V"]
        )
        self.assertEqual(chapters[0].canonical_archetype, "introduction")
        self.assertEqual(chapters[1].canonical_archetype, "literature_review")
        self.assertEqual(chapters[2].canonical_archetype, "methodology")
        self.assertEqual(chapters[3].canonical_archetype, "results_discussion")
        self.assertEqual(chapters[4].canonical_archetype, "conclusion")

        # Test ordinals and higher numbers up to 12
        raw_ordinals = """
        BAB PERTAMA PENDAHULUAN
        1.1 Latar Belakang
        BAB KEDUA KAJIAN PUSTAKA
        2.1 Teori
        BAB KESEPULUH PENGUJIAN
        10.1 Uji Beban
        BAB SEBELAS PEMBAHASAN
        11.1 Diskusi
        BAB DUA BELAS PENUTUP
        12.1 Simpulan
        """
        chapters_ord = self.intake.parse_raw_text_outline(raw_ordinals)
        self.assertEqual(len(chapters_ord), 5)
        self.assertEqual([c.number for c in chapters_ord], [1, 2, 10, 11, 12])
        self.assertEqual(
            [c.roman_number for c in chapters_ord], ["I", "II", "X", "XI", "XII"]
        )

    def test_parse_literal_newline_in_text_input(self):
        raw_escaped = "BAB I PENDAHULUAN\\n1.1 Latar Belakang\\n1.2 Rumusan Masalah\\nBAB II LANDASAN TEORI\\n2.1 Landasan Teori"
        chapters = self.intake.parse_raw_text_outline(raw_escaped)
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0].roman_number, "I")
        self.assertEqual(len(chapters[0].required_sections), 2)
        self.assertEqual(chapters[1].roman_number, "II")
        self.assertEqual(len(chapters[1].required_sections), 1)

        # Also verify via CLI subprocess execution with --text
        res = subprocess.run(
            [sys.executable, "scripts/custom_toc_intake.py", "--text", raw_escaped],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        parsed = json.loads(res.stdout)
        self.assertEqual(len(parsed["chapters"]), 2)
        self.assertEqual(parsed["chapters"][0]["title"], "BAB I: PENDAHULUAN")
        self.assertEqual(parsed["chapters"][1]["title"], "BAB II: LANDASAN TEORI")

    def test_parse_input_source_omitted_chapter_numbers(self):
        json_data = {
            "faculty_id": "test-faculty",
            "preset_name": "Test Faculty Preset",
            "chapters": [
                {"title": "BAB I: PENDAHULUAN", "canonical_archetype": "introduction"},
                {
                    "title": "BAB II: TINJAUAN PUSTAKA",
                    "canonical_archetype": "literature_review",
                },
                {"canonical_archetype": "methodology"},
                {"canonical_archetype": "results_discussion"},
                {"title": "PENUTUP", "canonical_archetype": "conclusion"},
            ],
        }
        preset = self.intake.parse_input_source(json.dumps(json_data))
        self.assertEqual(len(preset.chapters), 5)
        # Numbers should be sequentially assigned: 1 to 5
        self.assertEqual([c.number for c in preset.chapters], [1, 2, 3, 4, 5])
        # Roman numerals should match chapter numbers: I to V, not hardcoded to "I"
        self.assertEqual(
            [c.roman_number for c in preset.chapters], ["I", "II", "III", "IV", "V"]
        )
        # Title fallback should reflect dynamic chapter number
        self.assertEqual(preset.chapters[2].title, "BAB 3")
        self.assertEqual(preset.chapters[3].title, "BAB 4")
        self.assertNotEqual(preset.chapters[1].roman_number, "I")


class TestCustomTocMapperGuide(unittest.TestCase):
    """Suite 4: Validates mapper documentation and campus exemplars."""

    def test_mapper_guide_exists_and_comprehensive(self):
        guide = REPO_ROOT / "academic-paper" / "intake" / "custom_toc_mapper.md"
        self.assertTrue(guide.is_file(), f"{guide} does not exist")
        lines = guide.read_text(encoding="utf-8").splitlines()
        self.assertGreater(
            len(lines), 150, "custom_toc_mapper.md must be comprehensive (>150 lines)"
        )

    def test_mapper_guide_specifies_archetypes_and_prompts(self):
        guide = REPO_ROOT / "academic-paper" / "intake" / "custom_toc_mapper.md"
        text = guide.read_text(encoding="utf-8")
        for arch in [
            "introduction",
            "literature_review",
            "system_design",
            "methodology",
            "implementation_testing",
            "results_discussion",
            "conclusion",
        ]:
            self.assertIn(
                arch, text, f"Archetype {arch} must be documented in mapper guide"
            )
        self.assertIn("/skripsi-bab", text)
        self.assertIn("/skripsi-proposal", text)
        self.assertIn("/skripsi-defense", text)

    def test_mapper_guide_contains_campus_exemplars(self):
        guide = REPO_ROOT / "academic-paper" / "intake" / "custom_toc_mapper.md"
        text = guide.read_text(encoding="utf-8")
        self.assertIn("Informatika", text)
        self.assertIn("Hukum", text)
        self.assertIn("Kependidikan", text)


class TestRebrandingAndReleaseInvariants(unittest.TestCase):
    """Suite 5: Validates package rebranding, announcement synchronization, and guard namespaces."""

    def test_package_json_rebranding(self):
        pkg_path = REPO_ROOT / "package.json"
        data = json.loads(pkg_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "nyekripsi")
        keywords = data.get("keywords", [])
        self.assertIn("nyekripsi", keywords)
        self.assertIn("skripsi", keywords)

    def test_plugin_json_agent_counts_and_version(self):
        plugin_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
        data = json.loads(plugin_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("version"), "3.24.0")
        desc = data.get("description", "")
        self.assertIn("45 prompt roles", desc)
        self.assertIn("6 plugin-exposed agents", desc)

    def test_announce_script_lists_all_24_commands(self):
        script_path = REPO_ROOT / "scripts" / "announce-ars-loaded.sh"
        text = script_path.read_text(encoding="utf-8")
        self.assertIn("Slash commands (24):", text)
        for cmd in SKRIPSI_COMMANDS:
            self.assertIn(f"/{cmd}", text)
        self.assertIn("pembimbing_agent", text)
        self.assertIn("penguji_agent", text)

    def test_write_scope_guard_dual_namespace_support(self):
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        import ars_write_scope_guard as guard

        try:
            self.assertEqual(
                guard._manifest_key("academic-research-skills:synthesis_agent"),
                "synthesis_agent",
            )
            self.assertEqual(
                guard._manifest_key("nyekripsi:synthesis_agent"), "synthesis_agent"
            )
            self.assertEqual(
                guard._manifest_key("other-plugin:synthesis_agent"),
                "other-plugin:synthesis_agent",
            )
        finally:
            if str(REPO_ROOT / "scripts") in sys.path:
                sys.path.remove(str(REPO_ROOT / "scripts"))

    def test_readme_dual_branding_and_badges(self):
        readme_path = REPO_ROOT / "README.md"
        text = readme_path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# nyekripsi"))
        self.assertIn("badge/version-v3.24.0-blue", text)
        self.assertIn("/skripsi-proposal", text)
        self.assertIn("/skripsi-full", text)


if __name__ == "__main__":
    unittest.main()
