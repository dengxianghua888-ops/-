# Source Corrupt

`source.md` for this corpus entry is not valid readable text. The body contains
replacement characters and NUL bytes, so running Phase 1 would produce a
garbage dissection rather than a usable analysis.

- slug: `ancient_bird_cage`
- filename: `《不再是你的笼中雀》.txt`
- detected_at: `2026-05-22`
- status: blocked until the original text file is restored

Replace `source.md` with a readable UTF-8 copy of the original story, then run:

```bash
python3 scripts/storyforge.py run --story corpus/ancient_bird_cage --from-phase 1 --to-phase 1 --runner agent
python3 scripts/update-corpus-index.py
```
