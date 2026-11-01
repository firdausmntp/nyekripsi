#!/usr/bin/env python3
"""Custom Table of Contents (TOC) Intake Engine for nyekripsi.

Parses university thesis handbook outlines (plain text, markdown, JSON, YAML)
and generates validated faculty preset configurations conforming to the
faculty-preset-v1 schema with automatic semantic archetype classification
and academic rigor rules attachment.

Pure Python standard library implementation without third-party dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

SCHEMA_URL = "https://nyekripsi.org/schemas/faculty-preset-v1.json"

def roman_to_int(roman_str: str) -> Optional[int]:
    """Converts a Roman numeral string (1 to 3999) to an integer. Returns None if invalid."""
    if not isinstance(roman_str, str):
        return None
    roman_str = roman_str.upper().strip()
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if not re.match(r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$", roman_str):
        return None
    res = 0
    i = 0
    while i < len(roman_str):
        val1 = roman_map.get(roman_str[i], 0)
        if i + 1 < len(roman_str):
            val2 = roman_map.get(roman_str[i + 1], 0)
            if val1 >= val2:
                res += val1
                i += 1
            else:
                res += val2 - val1
                i += 2
        else:
            res += val1
            i += 1
    return res if res > 0 else None


def int_to_roman(num: int) -> str:
    """Converts an integer (1 to 3999) to its standard Roman numeral string."""
    if not isinstance(num, int) or num <= 0 or num > 3999:
        return str(num)
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ""
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num


# Retain dictionary mappings for backwards compatibility up to 50
ROMAN_TO_INT = {int_to_roman(i): i for i in range(1, 51)}
INT_TO_ROMAN = {i: int_to_roman(i) for i in range(1, 51)}


# Indonesian word number to integer mapping (cardinals & ordinals)
WORD_TO_INT: Dict[str, int] = {
    "SATU": 1, "PERTAMA": 1, "KESATU": 1,
    "DUA": 2, "KEDUA": 2,
    "TIGA": 3, "KETIGA": 3,
    "EMPAT": 4, "KEEMPAT": 4,
    "LIMA": 5, "KELIMA": 5,
    "ENAM": 6, "KEENAM": 6,
    "TUJUH": 7, "KETUJUH": 7,
    "DELAPAN": 8, "KEDELAPAN": 8,
    "SEMBILAN": 9, "KESEMBILAN": 9,
    "SEPULUH": 10, "KESEPULUH": 10,
    "SEBELAS": 11, "KESEBELAS": 11,
    "DUA BELAS": 12, "KEDUA BELAS": 12,
}

# Semantic archetype keywords for classification
ARCHETYPE_KEYWORDS: Dict[str, List[str]] = {
    "introduction": [
        "pendahuluan", "latar belakang", "rumusan masalah", "tujuan penelitian",
        "identifikasi masalah", "batasan masalah", "fokus penelitian", "introduction"
    ],
    "literature_review": [
        "tinjauan pustaka", "kajian pustaka", "landasan teori", "kerangka pemikiran",
        "kerangka berpikir", "penelitian terdahulu", "studi literatur", "telaah pustaka",
        "kajian teoritis", "literature review"
    ],
    "system_design": [
        "analisis dan perancangan", "perancangan sistem", "analisis kebutuhan",
        "desain sistem", "arsitektur sistem", "perancangan perangkat lunak",
        "analisis sistem", "system analysis", "system design"
    ],
    "methodology": [
        "metode penelitian", "metodologi", "metode pengembangan", "prosedur penelitian",
        "populasi dan sampel", "bahan hukum", "desain penelitian", "metode kerja",
        "research methodology", "metode"
    ],
    "implementation_testing": [
        "implementasi dan pengujian", "implementasi sistem", "pengujian sistem",
        "evaluasi sistem", "hasil pengujian", "implementasi dan evaluasi",
        "pengujian black box", "testing", "implementation"
    ],
    "results_discussion": [
        "hasil dan pembahasan", "hasil penelitian", "analisis data", "pembahasan",
        "temuan dan analisis", "hasil studi", "results and discussion"
    ],
    "conclusion": [
        "penutup", "kesimpulan", "kesimpulan dan saran", "simpulan",
        "penutup dan saran", "conclusion"
    ]
}

# Default rigor rules attached per archetype
DEFAULT_ARCHETYPE_RULES: Dict[str, Dict[str, Any]] = {
    "introduction": {
        "problem_statement_starter": "terdapat",
        "min_research_questions": 3,
        "objek_material_formal_required": True
    },
    "literature_review": {
        "min_prior_studies": 10,
        "comparative_matrix_13_columns": True,
        "theory_hierarchy_levels": ["Grand Theory", "Middle-Range Theory", "Applied Theory"],
        "required_diagrams": ["Mermaid Flowchart Kerangka Berpikir"]
    },
    "system_design": {
        "required_diagrams": ["Mermaid Architecture Diagram", "Mermaid Class Diagram"]
    },
    "methodology": {
        "triangulation_or_sampling_protocol_required": True
    },
    "implementation_testing": {
        "min_blackbox_cases": 10,
        "sus_evaluation_required": True
    },
    "results_discussion": {
        "three_way_discussion_triangulation": True
    },
    "conclusion": {
        "natijah_epistemic_conclusion": True
    },
    "custom_specialized": {}
}


@dataclass
class ChapterConfig:
    number: int
    roman_number: str
    canonical_archetype: str
    title: str
    required_sections: List[str] = field(default_factory=list)
    rules: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FacultyPreset:
    faculty_id: str
    preset_name: str
    campus_name: str
    faculty_name: str
    citation_style: str
    recent_reference_ratio_min: float
    recent_year_window: int
    chapters: List[ChapterConfig]
    schema: str = SCHEMA_URL

    def to_dict(self) -> Dict[str, Any]:
        return {
            "$schema": self.schema,
            "faculty_id": self.faculty_id,
            "preset_name": self.preset_name,
            "campus_name": self.campus_name,
            "faculty_name": self.faculty_name,
            "citation_style": self.citation_style,
            "recent_reference_ratio_min": self.recent_reference_ratio_min,
            "recent_year_window": self.recent_year_window,
            "chapters": [asdict(c) for c in self.chapters]
        }


def classify_archetype(title: str, sections: Optional[List[str]] = None) -> str:
    """Classifies chapter title and its subsections into a canonical archetype."""
    combined = title.lower()
    if sections:
        combined += " " + " ".join(s.lower() for s in sections)

    scores: Dict[str, int] = {}
    for arch, keywords in ARCHETYPE_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in combined:
                score += (3 if kw in title.lower() else 1)
        if score > 0:
            scores[arch] = score

    if not scores:
        return "custom_specialized"

    # Prioritize system_design / implementation_testing over general methodology / results if matched
    if "system_design" in scores and "methodology" in scores:
        if any(k in title.lower() for k in ["perancangan", "analisis dan perancangan", "desain sistem"]):
            return "system_design"
    if "implementation_testing" in scores and "results_discussion" in scores:
        if any(k in title.lower() for k in ["implementasi", "pengujian", "evaluasi sistem"]):
            return "implementation_testing"

    best_match = max(scores.items(), key=lambda item: item[1])
    return best_match[0]


def clean_section_title(text: str) -> str:
    """Strips trailing page dots and page numbers often copied from PDF TOCs."""
    # e.g., "1.1 Latar Belakang Masalah ......... 12" -> "1.1 Latar Belakang Masalah"
    cleaned = re.sub(r"[\s\.\-_]{3,}\s*\d*\s*$", "", text.strip())
    cleaned = re.sub(r"\s+\d+\s*$", "", cleaned.strip())
    # Strip markdown list bullets if present
    cleaned = re.sub(r"^\s*[-*+]\s+", "", cleaned)
    return cleaned.strip()


def parse_raw_text_outline(raw_text: str) -> List[ChapterConfig]:
    """Parses raw text or markdown outline into chapter and section configurations."""
    if "\\n" in raw_text:
        raw_text = raw_text.replace("\\n", "\n")
    lines = raw_text.strip().splitlines()
    chapters: List[ChapterConfig] = []
    current_chapter: Optional[Dict[str, Any]] = None

    _word_keys = sorted(WORD_TO_INT.keys(), key=lambda w: (-len(w), w))
    _word_pattern = "|".join(r"\s+".join(re.escape(part) for part in k.split()) for k in _word_keys)
    _bullet_prefix = r"(?:(?:[-*+]|\d+[\.)])\s+)?"
    chapter_pattern = re.compile(
        rf"^\s*(?:###?\s+)?{_bullet_prefix}(?:BAB|CHAPTER)[\s\-]*([0-9IVXLCDM]+|{_word_pattern})(?:[\s:.-]+(.*))?$",
        re.IGNORECASE
    )
    standalone_chapter_pattern = re.compile(
        r"^\s*(?:###?\s+)?(?:[-*+]\s+)?([0-9IVXLCDM]+)\.[\s\t]+([A-Z\s]{4,})$"
    )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        chap_match = chapter_pattern.match(stripped) or standalone_chapter_pattern.match(stripped)
        if chap_match:
            num_raw = re.sub(r"\s+", " ", chap_match.group(1).strip().upper())
            title_rest = chap_match.group(2) or ""
            title_rest = clean_section_title(title_rest)

            # Determine integer and roman representations
            r_val = roman_to_int(num_raw)
            if r_val is not None:
                int_num = r_val
                roman_num = num_raw
            elif num_raw.isdigit():
                int_num = int(num_raw)
                roman_num = int_to_roman(int_num)
            elif num_raw in WORD_TO_INT:
                int_num = WORD_TO_INT[num_raw]
                roman_num = int_to_roman(int_num)
            else:
                int_num = len(chapters) + 1
                roman_num = int_to_roman(int_num)


            full_title = f"BAB {roman_num}: {title_rest}" if title_rest else f"BAB {roman_num}"

            if current_chapter:
                arch = classify_archetype(current_chapter["title"], current_chapter["sections"])
                rules = dict(DEFAULT_ARCHETYPE_RULES.get(arch, {}))
                chapters.append(ChapterConfig(
                    number=current_chapter["number"],
                    roman_number=current_chapter["roman_number"],
                    canonical_archetype=arch,
                    title=current_chapter["title"],
                    required_sections=current_chapter["sections"],
                    rules=rules
                ))

            current_chapter = {
                "number": int_num,
                "roman_number": roman_num,
                "title": full_title,
                "sections": []
            }
            continue

        if current_chapter is not None:
            # Section detection: "1.1 ...", "A. ...", "- 1.1 ...", "- Latar Belakang"
            cleaned_sec = clean_section_title(stripped)
            if cleaned_sec:
                # Exclude lines that look like page footnotes or unrelated text
                if not re.match(r"^(?:halaman|hal\.|page)\s+\d+$", cleaned_sec, re.IGNORECASE):
                    current_chapter["sections"].append(cleaned_sec)

    if current_chapter:
        arch = classify_archetype(current_chapter["title"], current_chapter["sections"])
        rules = dict(DEFAULT_ARCHETYPE_RULES.get(arch, {}))
        chapters.append(ChapterConfig(
            number=current_chapter["number"],
            roman_number=current_chapter["roman_number"],
            canonical_archetype=arch,
            title=current_chapter["title"],
            required_sections=current_chapter["sections"],
            rules=rules
        ))

    if not chapters:
        raise ValueError("No recognizable chapters found in raw outline text. Ensure lines begin with 'BAB <number>' or 'BAB <roman>'.")

    return chapters


def _simple_yaml_parse(text: str) -> Dict[str, Any]:
    """Lightweight pure-stdlib parser for basic YAML dictionaries and lists."""
    result: Dict[str, Any] = {}
    current_key = None
    in_list = False
    list_items = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.strip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip())
        stripped = line.strip()

        if stripped.startswith("- "):
            val = stripped[2:].strip().strip("\"'")
            if in_list:
                list_items.append(val)
            continue

        if ":" in stripped:
            if in_list and current_key:
                result[current_key] = list_items
                in_list = False
                list_items = []

            k, v = stripped.split(":", 1)
            key = k.strip()
            val = v.strip().strip("\"'")
            if not val:
                current_key = key
                in_list = True
                list_items = []
            else:
                if val.lower() == "true":
                    val_conv = True
                elif val.lower() == "false":
                    val_conv = False
                elif val.isdigit():
                    val_conv = int(val)
                else:
                    try:
                        val_conv = float(val)
                    except ValueError:
                        val_conv = val
                result[key] = val_conv

    if in_list and current_key:
        result[current_key] = list_items

    return result


def parse_input_source(content: str) -> FacultyPreset:
    """Parses JSON, YAML, or raw text outline into a FacultyPreset object."""
    stripped = content.strip()

    # Try JSON
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            data = json.loads(stripped)
            if isinstance(data, dict) and "chapters" in data and isinstance(data["chapters"], list):
                chapters = []
                for c in data.get("chapters", []):
                    arch = c.get("canonical_archetype") or classify_archetype(c.get("title", ""), c.get("required_sections", []))
                    rules = c.get("rules") or dict(DEFAULT_ARCHETYPE_RULES.get(arch, {}))
                    chap_num = c.get("number", len(chapters) + 1)
                    chapters.append(ChapterConfig(
                        number=chap_num,
                        roman_number=c.get("roman_number", int_to_roman(chap_num)),
                        canonical_archetype=arch,
                        title=c.get("title", f"BAB {chap_num}"),
                        required_sections=c.get("required_sections", []),
                        rules=rules
                    ))
                return FacultyPreset(
                    faculty_id=data.get("faculty_id", "custom"),
                    preset_name=data.get("preset_name", "Custom Campus Preset"),
                    campus_name=data.get("campus_name", "Custom Campus"),
                    faculty_name=data.get("faculty_name", "Custom Faculty"),
                    citation_style=data.get("citation_style", "APA"),
                    recent_reference_ratio_min=float(data.get("recent_reference_ratio_min", 0.8)),
                    recent_year_window=int(data.get("recent_year_window", 5)),
                    chapters=chapters
                )
        except json.JSONDecodeError:
            pass

    # Try YAML if it has top-level keys like chapters: or faculty_id:
    if "chapters:" in stripped and ("faculty_id:" in stripped or "preset_name:" in stripped):
        try:
            import yaml  # type: ignore
            data = yaml.safe_load(stripped)
        except Exception:
            data = _simple_yaml_parse(stripped)

        if isinstance(data, dict) and "chapters" in data:
            chapters = []
            for c in data.get("chapters", []):
                arch = c.get("canonical_archetype") or classify_archetype(c.get("title", ""), c.get("required_sections", []))
                rules = c.get("rules") or dict(DEFAULT_ARCHETYPE_RULES.get(arch, {}))
                chap_num = c.get("number", len(chapters) + 1)
                chapters.append(ChapterConfig(
                    number=chap_num,
                    roman_number=c.get("roman_number", int_to_roman(chap_num)),
                    canonical_archetype=arch,
                    title=c.get("title", f"BAB {chap_num}"),
                    required_sections=c.get("required_sections", []),
                    rules=rules
                ))
            return FacultyPreset(
                faculty_id=data.get("faculty_id", "custom"),
                preset_name=data.get("preset_name", "Custom Campus Preset"),
                campus_name=data.get("campus_name", "Custom Campus"),
                faculty_name=data.get("faculty_name", "Custom Faculty"),
                citation_style=data.get("citation_style", "APA"),
                recent_reference_ratio_min=float(data.get("recent_reference_ratio_min", 0.8)),
                recent_year_window=int(data.get("recent_year_window", 5)),
                chapters=chapters
            )

    # Fallback: Parse as raw outline text
    chapters = parse_raw_text_outline(stripped)
    return FacultyPreset(
        faculty_id="custom",
        preset_name="Custom Campus Preset",
        campus_name="Universitas",
        faculty_name="Fakultas",
        citation_style="APA",
        recent_reference_ratio_min=0.8,
        recent_year_window=5,
        chapters=chapters
    )


def validate_preset_dict(data: Dict[str, Any]) -> List[str]:
    """Validates preset dictionary against faculty-preset-v1 schema constraints."""
    errors = []
    required_top = ["faculty_id", "preset_name", "chapters"]
    for req in required_top:
        if req not in data:
            errors.append(f"Missing required top-level property: '{req}'")

    chapters = data.get("chapters")
    if not isinstance(chapters, list) or len(chapters) == 0:
        errors.append("Property 'chapters' must be a non-empty list")
    else:
        for i, chap in enumerate(chapters):
            if not isinstance(chap, dict):
                errors.append(f"Chapter index {i} must be an object")
                continue
            if "number" not in chap:
                errors.append(f"Chapter index {i} missing 'number'")
            if "title" not in chap:
                errors.append(f"Chapter index {i} missing 'title'")
            if "canonical_archetype" in chap:
                valid_archs = list(ARCHETYPE_KEYWORDS.keys()) + ["custom_specialized"]
                if chap["canonical_archetype"] not in valid_archs:
                    errors.append(f"Chapter index {i} has invalid canonical_archetype '{chap['canonical_archetype']}'")

    if errors:
        raise ValueError("Schema validation errors:\n- " + "\n- ".join(errors))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ingest, parse, and validate university thesis Table of Contents into nyekripsi faculty presets."
    )
    parser.add_argument("--input", "-i", type=str, help="Path to input outline file (text, markdown, JSON, or YAML)")
    parser.add_argument("--text", "-t", type=str, help="Raw outline text directly from CLI")
    parser.add_argument("--output", "-o", type=str, help="Destination path for generated custom_preset.json")
    parser.add_argument("--preset-name", type=str, default="Custom Campus Preset", help="Descriptive preset name")
    parser.add_argument("--campus-name", type=str, default="Universitas", help="University name")
    parser.add_argument("--faculty-name", type=str, default="Fakultas", help="Faculty name")
    parser.add_argument("--citation-style", type=str, default="APA", choices=["APA", "IEEE", "Harvard", "Chicago"], help="Primary citation style")
    parser.add_argument("--validate", action="store_true", help="Validate input JSON file against preset schema")

    args = parser.parse_args()

    if not args.input and not args.text:
        parser.print_help()
        return 0

    try:
        if args.input:
            content = Path(args.input).read_text(encoding="utf-8")
        else:
            content = args.text
            if content and "\\n" in content:
                content = content.replace("\\n", "\n")

        if args.validate:
            data = json.loads(content)
            validate_preset_dict(data)
            print(f"[OK] Validation passed: {len(data.get('chapters', []))} chapters conform to faculty-preset-v1 schema.")
            return 0

        preset = parse_input_source(content)

        # Apply CLI overrides if provided and not defaulted
        if args.preset_name != "Custom Campus Preset" or preset.preset_name == "Custom Campus Preset":
            preset.preset_name = args.preset_name
        if args.campus_name != "Universitas" or preset.campus_name == "Universitas":
            preset.campus_name = args.campus_name
        if args.faculty_name != "Fakultas" or preset.faculty_name == "Fakultas":
            preset.faculty_name = args.faculty_name
        if args.citation_style != "APA" or preset.citation_style == "APA":
            preset.citation_style = args.citation_style

        output_dict = preset.to_dict()
        formatted_json = json.dumps(output_dict, indent=2, ensure_ascii=False)

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(formatted_json, encoding="utf-8")
            print(f"[OK] Saved faculty preset to {out_path} ({len(preset.chapters)} chapters).")
        else:
            print(formatted_json)

        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
