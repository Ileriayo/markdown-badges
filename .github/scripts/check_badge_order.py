
import sys
import re

README_FILE_PATH = '../../README.md'

def find_badge_sections():
    with open(README_FILE_PATH, encoding='utf-8') as f:
        lines = f.readlines()

    # Find the line number of the main badges section
    badge_header_idx = None
    for idx, line in enumerate(lines):
        if line.strip().lower() == '# badges':
            badge_header_idx = idx
            break
    if badge_header_idx is None:
        print('No "# Badges" section found in README.md')
        sys.exit(1)

    # Find all ### section headers after # Badges
    section_indices = []
    for idx in range(badge_header_idx + 1, len(lines)):
        if lines[idx].startswith('### '):
            section_indices.append(idx)

    # Add an artificial end index for the last section
    section_indices.append(len(lines))

    # For each section, collect badge lines (table rows)
    badge_sections = []
    for i in range(len(section_indices) - 1):
        section_start = section_indices[i]
        section_end = section_indices[i + 1]
        section_title = lines[section_start].strip()
        badge_lines = []
        in_table = False
        for line in lines[section_start + 1:section_end]:
            if line.strip().startswith('|'):
                # Only consider table rows that are not header or separator
                if not in_table:
                    in_table = True
                    continue  # skip header
                if set(line.strip()) == {'|', '-', ' '}:
                    continue  # skip separator
                badge_lines.append(line.strip())
            elif in_table and not line.strip():
                break  # End of table
        if badge_lines:
            badge_sections.append((section_title, badge_lines))
    return badge_sections

def main():
    badge_sections = find_badge_sections()
    if not badge_sections:
        print('No badge tables found under any ### section after # Badges.')
        sys.exit(1)
    failed = False
    import difflib
    for section_title, badge_lines in badge_sections:
        # Sort by the first column (badge name)
        def get_name(row):
            cols = [c.strip() for c in row.strip('|').split('|')]
            return cols[0].lower() if cols else ''
        sorted_lines = sorted(badge_lines, key=get_name)
        if badge_lines != sorted_lines:
            failed = True
            print(f'❌ Badge table in section "{section_title}" is not in alphabetical order!')
            print('Please sort the badge table rows by badge name.')
            diff = difflib.unified_diff(
                badge_lines, sorted_lines,
                fromfile='Current', tofile='Expected',
                lineterm=''
            )
            for line in diff:
                if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
                    print(f'\033[36m{line}\033[0m')  # Cyan for diff headers
                elif line.startswith('-'):
                    print(f'\033[31m{line}\033[0m')  # Red for removals
                elif line.startswith('+'):
                    print(f'\033[32m{line}\033[0m')  # Green for additions
                else:
                    print(line)
    if failed:
        sys.exit(1)
    print('✅ All badge tables are in alphabetical order.')

if __name__ == '__main__':
    main()
