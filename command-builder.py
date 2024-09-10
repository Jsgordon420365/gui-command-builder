# ver 20240910145000.0
import sqlite3
import json

def get_command_data(command_name):
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM commands WHERE name = ?', (command_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        name, short_description, synopsis, description, options, is_zsh = result
        return {
            'name': name,
            'short_description': short_description,
            'synopsis': synopsis,
            'description': description,
            'options': json.loads(options),
            'is_zsh': bool(is_zsh)
        }
    return None

def display_command_info(command_data):
    print(f"\nCommand: {command_data['name']}")
    print(f"Description: {command_data['short_description']}")
    print(f"\nSynopsis: {command_data['synopsis']}")
    print("\nOptions:")
    for option in command_data['options']:
        print(f"  {option['flag']} {option['long_flag']}: {option['description']}")

def build_command(command_data):
    command = [command_data['name']]
    while True:
        print("\nCurrent command:", ' '.join(command))
        choice = input("Enter an option flag to add (or 'done' to finish): ").strip()
        if choice.lower() == 'done':
            break
        for option in command_data['options']:
            if choice in [option['flag'], option['long_flag']]:
                command.append(choice)
                if option['flag'] != '-' and not option['flag'].endswith('='):
                    value = input(f"Enter value for {choice} (press enter for no value): ").strip()
                    if value:
                        command.append(value)
                break
        else:
            print("Invalid option. Please try again.")
    
    return ' '.join(command)

def main():
    while True:
        command_name = input("\nEnter a command name (or 'quit' to exit): ").strip()
        if command_name.lower() == 'quit':
            break
        
        command_data = get_command_data(command_name)
        if command_data:
            display_command_info(command_data)
            built_command = build_command(command_data)
            print("\nFinal command:", built_command)
        else:
            print(f"Command '{command_name}' not found in the database.")

if __name__ == "__main__":
    main()

# Version History
# 20240910145000.0 - Initial version of the basic command builder
