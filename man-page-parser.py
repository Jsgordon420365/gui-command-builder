# ver 20240910170000.2
import os
import re
import sqlite3
import json

def parse_command_file(command):
    try:
        with open(os.path.expanduser(f"~/commands/{command}.txt"), 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"No documentation file found for command: {command}")
        return None

    sections = {}
    current_section = None
    for line in content.split('\n'):
        if line.isupper() and line.strip():
            current_section = line.strip()
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)

    options = []
    if 'OPTIONS' in sections:
        option_pattern = r'(-\w+,?\s+)?(--[\w-]+)?\s*(.+)'
        for line in sections['OPTIONS']:
            match = re.match(option_pattern, line.strip())
            if match:
                short_flag, long_flag, description = match.groups()
                option_type = infer_option_type(description)
                valid_values = extract_valid_values(description) if option_type == 'selection' else None
                options.append({
                    'flag': short_flag.strip() if short_flag else '',
                    'long_flag': long_flag.strip() if long_flag else '',
                    'description': description.strip(),
                    'type': option_type,
                    'valid_values': valid_values
                })

    return {
        'name': command,
        'synopsis': ' '.join(sections.get('SYNOPSIS', [])).strip(),
        'description': ' '.join(sections.get('DESCRIPTION', [])).strip(),
        'options': options
    }

def infer_option_type(description):
    if re.search(r'\bfile\b|\bpath\b|\bdirectory\b', description, re.IGNORECASE):
        return 'file'
    elif re.search(r'\bselect\b|\bchoose\b|\boptions are\b', description, re.IGNORECASE):
        return 'selection'
    else:
        return 'text'

def extract_valid_values(description):
    values_match = re.search(r'(?:options are|can be):?\s*((?:[\w-]+(?:,\s*|$))+)', description, re.IGNORECASE)
    if values_match:
        return [value.strip() for value in values_match.group(1).split(',')]
    return None

def store_command_data(command_data):
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS commands (
        name TEXT PRIMARY KEY,
        synopsis TEXT,
        description TEXT,
        options TEXT
    )
    ''')

    cursor.execute('''
    INSERT OR REPLACE INTO commands (name, synopsis, description, options)
    VALUES (?, ?, ?, ?)
    ''', (
        command_data['name'],
        command_data['synopsis'],
        command_data['description'],
        json.dumps(command_data['options'])
    ))

    conn.commit()
    conn.close()

def main():
    with open(os.path.expanduser('~/commands/commands01.txt'), 'r') as f:
        commands = [line.strip() for line in f if line.strip()]

    for command in commands:
        command_data = parse_command_file(command)
        if command_data:
            store_command_data(command_data)
            print(f"Parsed and stored data for command: {command}")

if __name__ == "__main__":
    main()

# Version History
# 20240910142000.0 - Initial version of the man page parser
# 20240910160500.1 - Improved option extraction and handling of complex syntax patterns
# 20240910170000.2 - Expanded database schema to include option types and valid values
