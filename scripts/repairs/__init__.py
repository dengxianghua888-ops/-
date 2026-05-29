"""StoryForge auto-repair package.

Each repair_*.py exposes ``run(story: Path, mode: str) -> dict`` and never
raises on missing inputs (it returns a status payload with ``skipped`` instead).
"""
