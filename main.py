import student as s
import shutil

def heading():
    """Display application heading with ASCII art"""
    terminal_width = shutil.get_terminal_size().columns
    width = max(84 + 4, terminal_width)
    sage_green = "\033[38;2;143;188;143m"
    reset = "\033[0m"
    print()
    print()
    print()
    print()
    print(sage_green + "═" * width + reset)
    print(sage_green + "-" * width + reset)
    print()
    print()
    banner = [
        "  _   _      _                     _ _           ",
        " | | | |    (_)                   (_) |          ",
        "| | | |_ __  ___   _____ _ __ ___ _| |_ _   _   ",
        "| | | | '_ \\| \\ \\ / / _ \\ '__/ __| | __| | | |  ",
        "| |_| | | | | |\\ V /  __/ |  \\__ \\ | |_| |_| |  ",
        " \\___/|_| |_|_| \\_/ \\___|_|  |___/_|\\__|\\__, |  ",
        "                                          __/ |  ",
        "                                         |___/   ",
        "",
        "     ____  _                             ",
        "    |  _ \\| | __ _ _ __  _ __   ___ _ __ ",
        "    | |_) | |/ _` | '_ \\| '_ \\ / _ \\ '__|",
        "    |  __/| | (_| | | | | | | |  __/ |   ",
        "    |_|   |_|\\__,_|_| |_|_| |_|\\___|_|   "
    ]
    terminal_width = shutil.get_terminal_size().columns
    for line in banner:
        print(sage_green + line.center(terminal_width) + reset)
    print()
    print()
    print(sage_green + "-" * width + reset)
    print(sage_green + "═" * width + reset)
    print()
    print()
    print()
    print()

# Display heading
heading()

# Main menu loop
while True:
    print("1. Student Portal")
    print("2. Exit")
    choice = input("Enter your choice: ")  
    if choice == "1":
        s.client_main()
    elif choice == "2":
        print("\n\033[92m Thank you for using University Planner! Goodbye! 📚\033[0m\n")
        break
    else:
        s.print_warning("Invalid choice. Enter 1, 2, or 3.")