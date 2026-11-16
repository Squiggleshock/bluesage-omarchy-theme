#!/usr/bin/env python3
"""Render BlueSage's native theme assets from its single source palette."""
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r"\{\{\s*(\w+)\s*\}\}")

def render_assets():
    palette = tomllib.loads((ROOT / "colors.toml").read_text())
    outputs = []
    for source in sorted((ROOT / "templates").glob("*.tpl")):
        def resolve(match):
            key = match.group(1)
            if key not in palette:
                raise ValueError(f"Missing palette field: {key}")
            value = palette[key]
            if not isinstance(value, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
                raise ValueError(f"Invalid color for {key}: {value!r}")
            return value
        rendered = TOKEN.sub(resolve, source.read_text())
        if "{{" in rendered:
            raise ValueError(f"Unresolved token in {source.name}")
        outputs.append((ROOT / source.name.removesuffix(".tpl"), rendered))
    for target, rendered in outputs:
        target.write_text(rendered)
        print(target.name)

if __name__ == "__main__":
    render_assets()
