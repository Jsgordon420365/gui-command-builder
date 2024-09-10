# ver 20240910143500.1
import sqlite3
import json

def verify_parsed_data():
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()

    # Get all command names
    cursor.execute('SELECT name FROM commands')
    all_commands = [row[0] for row in cursor.fetchall()]

    print(f"Total commands in database: {len(all_commands)}")

    # Count ZSH commands
    cursor.execute('SELECT COUNT(*) FROM commands WHERE is_zsh = 1')
    zsh_count = cursor.fetchone()[0]
    print(f"Total ZSH commands: {zsh_count}")

    # Sample commands to verify (including some potential ZSH commands)
    sample_commands = ['ls', 'grep', 'find', 'zsh', 'setopt', 'alias']

    for command in sample_commands:
        cursor.execute('SELECT * FROM commands WHERE name = ?', (command,))
        result = cursor.fetchone()

        if result:
            name, short_description, synopsis, description, options, is_zsh = result
            print(f"\nCommand: {name}")
            print(f"Short Description: {short_description}")
            print(f"Synopsis: {synopsis[:100]}..." if synopsis else "Synopsis: Not available")
            print(f"Description: {description[:100]}..." if description else "Description: Not available")
            print("Options:")
            try:
                parsed_options = json.loads(options)
                for option in parsed_options[:3]:  # First 3 options
                    print(f"  {option['flag']} {option['long_flag']}: {option['description'][:50]}...")
                print(f"  ... and {len(parsed_options) - 3} more options")
            except json.JSONDecodeError:
                print("  No options or invalid options data")
            print(f"Is ZSH: {'Yes' if is_zsh else 'No'}")
        else:
            print(f"\nCommand '{command}' not found in the database.")

    # List first 10 ZSH commands
    cursor.execute('SELECT name FROM commands WHERE is_zsh = 1 LIMIT 10')
    zsh_commands = [row[0] for row in cursor.fetchall()]
    print("\nFirst 10 ZSH commands:", ", ".join(zsh_commands))

    conn.close()

if __name__ == "__main__":
    verify_parsed_data()

# Version History
# 20240910143000.0 - Initial version of the parser verification script
# 20240910143500.1 - Updated to provide more detailed output and check for ZSH commands
