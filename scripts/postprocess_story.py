#!/usr/bin/env python3
"""Post-process a story draft: split long lines (quote-aware) and report stats."""
import re
import sys
from pathlib import Path

def split_lines_quote_aware(text: str, max_nonspace: int = 35) -> str:
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            new_lines.append(line)
            continue
        ns_len = len(re.sub(r'\s+', '', stripped))
        if ns_len <= max_nonspace:
            new_lines.append(line)
            continue
        # Check if line is inside quotes (starts with " and doesn't close)
        # Split at sentence boundaries, but respect quote integrity
        segments = []
        current = ''
        in_quote = False
        for char in stripped:
            current += char
            if char in '“「':  # opening quotes
                in_quote = True
            elif char in '”」':  # closing quotes
                in_quote = False
            elif char in '。？！' and not in_quote:
                cur_ns = len(re.sub(r'\s+', '', current))
                if cur_ns >= 12:
                    segments.append(current)
                    current = ''
        if current:
            if segments:
                segments[-1] += current
            else:
                segments.append(current)
        if len(segments) > 1:
            merged = []
            buf = ''
            for seg in segments:
                combined_ns = len(re.sub(r'\s+', '', buf + seg))
                if combined_ns <= max_nonspace:
                    buf += seg
                else:
                    if buf:
                        merged.append(buf)
                    buf = seg
            if buf:
                merged.append(buf)
            new_lines.extend(merged)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: postprocess_story.py <file.md>")
        sys.exit(1)
    path = Path(sys.argv[1])
    text = path.read_text(encoding='utf-8')
    orig_ns = len(re.sub(r'\s+', '', text))

    result = split_lines_quote_aware(text)
    new_ns = len(re.sub(r'\s+', '', result))

    assert orig_ns == new_ns, f"Nonspace changed: {orig_ns} -> {new_ns}"

    path.write_text(result, encoding='utf-8')

    content_lines = [l for l in result.split('\n') if l.strip() and not l.strip().startswith('#')]
    avg = sum(len(l) for l in content_lines) / len(content_lines) if content_lines else 0
    qmarks = result.count('？') + result.count('?')

    print(f"nonspace: {new_ns}")
    print(f"lines: {len(content_lines)}")
    print(f"avg_line_chars: {avg:.1f}")
    print(f"question_marks: {qmarks} ({qmarks/new_ns*1000:.2f}/k)")

if __name__ == '__main__':
    main()
