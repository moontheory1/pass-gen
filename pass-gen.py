import os
import random
import string
import time

# --- Color & Style Palette (ANSI Escape Codes) ---
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Moonlight color tones
PURPLE_MID   = "\033[38;2;140;110;200m"
PURPLE_LIGHT = "\033[38;2;190;160;255m"
CYAN_SOFT    = "\033[38;2;130;220;255m"
ACCENT_PINK  = "\033[38;2;255;150;200m"
WHITE        = "\033[38;2;240;240;255m"
GRAY         = "\033[38;2;110;110;140m"

WATERMARK = f"{ACCENT_PINK}{BOLD}! moonlight <3{RESET}"

# 1. STARTUP LOGO (Plays on initial launch)
STARTUP_LOGO = rf"""{PURPLE_LIGHT}
   ┌──┐
   │  │         ██████╗   █████╗  ███████╗ ███████╗ ██╗    ██╗  ██████╗  ██████╗  ██████╗
 ┌─┴──┴─┐       ██╔══██╗ ██╔══██╗ ██╔════╝ ██╔════╝ ██║    ██║ ██╔═══██╗ ██╔══██╗ ██╔══██╗
 │ ✦  ✦ │       ██████╔╝ ███████║ ███████╗ ███████╗ ██║ █╗ ██║ ██║   ██║ ██████╔╝ ██║  ██║
 │  ▼   │       ██╔═══╝  ██╔══██║ ╚════██║ ╚════██║ ██║███╗██║ ██║   ██║ ██╔══██╗ ██║  ██║         ██╗
 └──────┘       ██║      ██║  ██║ ███████║ ███████║ ╚███╔███╔╝ ╚██████╔╝ ██║  ██║ ██████╔╝         ██║       ██╗██████╗
                ╚═╝      ╚═╝  ╚═╝ ╚══════╝ ╚══════╝  ╚══╝╚══╝   ╚═════╝  ╚═╝  ╚═╝ ╚═════╝          ██║      ██╔╝╚════██╗
                                                                                                   ██║    ██╔╝  █████╔╝
           ██████╗  ███████╗ ███╗   ██╗ ███████╗ ██████╗   █████╗  ████████╗  ██████╗  ██████╗     ██║     ╚██╗  ╚═══██╗
          ██╔════╝  ██╔════╝ ████╗  ██║ ██╔════╝ ██╔══██╗ ██╔══██╗ ╚══██╔══╝ ██╔═══██╗ ██╔══██╗    ╚═╝      ╚██╗██████╔╝
          ██║  ███╗ █████╗   ██╔██╗ ██║ █████╗   ██████╔╝ ███████║    ██║    ██║   ██║ ██████╔╝    ██╗       ╚═╝╚═════╝ 
          ██║   ██║ ██╔══╝   ██║╚██╗██║ ██╔══╝   ██╔══██╗ ██╔══██║    ██║    ██║   ██║ ██╔══██╗    ╚═╝
          ╚██████╔╝ ███████╗ ██║ ╚████║ ███████╗ ██║  ██║ ██║  ██║    ██║    ╚██████╔╝ ██║  ██║
           ╚═════╝  ╚══════╝ ╚═╝  ╚═══╝ ╚══════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝    ╚═╝     ╚═════╝  ╚═╝  ╚═╝{ACCENT_PINK}

                                    ✦  made by: {WATERMARK}  ✦
{RESET}
"""

# 2. MAIN LOGO (Persistent dashboard banner while running)
MAIN_LOGO = rf"""{PURPLE_MID}

                      ┌──┐
                      │  │    
                    ┌─┴──┴─┐  
                    │ ✦  ✦ │  
                    │  ▼   │  
                    └──────┘  
                                ___       __    __ 
   ____ ___  ____  ____  ____  / (_)___ _/ /_  / /_
  / __ `__ \/ __ \/ __ \/ __ \/ / / __ `/ __ \/ __/
 / / / / / / /_/ / /_/ / / / / / / /_/ / / / / /_  
/_/ /_/ /_/\____/\____/_/ /_/_/_/\__, /_/ /_/\__/  
                                /____/             
                                
          {ACCENT_PINK}✦  made by: {WATERMARK}  ✦
{RESET}"""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def play_startup_sequence():
    clear_screen()
    print(STARTUP_LOGO)
    print(f"\n        {PURPLE_LIGHT}✦ Initializing environment...{RESET}")
    time.sleep(1.2)
    print(f"        {CYAN_SOFT}✦ Loading cryptographic vault...{RESET}")
    time.sleep(0.9)
    print(f"        {ACCENT_PINK}✦ Launching...{RESET}")
    time.sleep(0.6)

def print_main_screen():
    clear_screen()
    print(MAIN_LOGO)
    print(f"{GRAY}┌──────────────────────────────────────────────┐{RESET}")
    print(f"  {CYAN_SOFT}✦ KEY VAULT & GENERATOR ✦{RESET}  |  {WATERMARK}")
    print(f"{GRAY}└──────────────────────────────────────────────┘{RESET}\n")

def prompt_bool(message):
    while True:
        choice = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}{message} {GRAY}[Y/N]{RESET}: ").strip().upper()
        if choice in ("Y", "YES"):
            return True
        if choice in ("N", "NO"):
            return False
        print(f"   {ACCENT_PINK}⚠ Please enter 'Y' or 'N'.{RESET}")

def prompt_int(message, min_val=1):
    while True:
        val = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}{message}{RESET}: ").strip()
        if val.isdigit() and int(val) >= min_val:
            return int(val)
        print(f"   {ACCENT_PINK}⚠ Enter a valid number ({min_val}+).{RESET}")

def generate_password(length, use_lower, use_upper, use_digits, use_symbols):
    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%^&*()-_=+[]{}<>?"

    if not pool:
        raise ValueError("You must select at least one character type.")

    required_chars = []
    if use_lower:
        required_chars.append(random.choice(string.ascii_lowercase))
    if use_upper:
        required_chars.append(random.choice(string.ascii_uppercase))
    if use_digits:
        required_chars.append(random.choice(string.digits))
    if use_symbols:
        required_chars.append(random.choice("!@#$%^&*()-_=+[]{}<>?"))

    if length < len(required_chars):
        raise ValueError(f"Length must be at least {len(required_chars)} for chosen requirements.")

    remaining = length - len(required_chars)
    password_chars = required_chars + [random.choice(pool) for _ in range(remaining)]
    random.shuffle(password_chars)
    return "".join(password_chars)

def main():
    # Show the initial startup splash
    play_startup_sequence()

    while True:
        # Show the main operational screen
        print_main_screen()

        num_passwords = prompt_int("How many keys to generate?", min_val=1)
        length = prompt_int("Key length", min_val=4)

        print(f"\n {GRAY}── Configuration Settings ──{RESET}")
        use_lower = prompt_bool("Include lowercase letters?")
        use_upper = prompt_bool("Include uppercase letters?")
        use_digits = prompt_bool("Include numbers?")
        use_symbols = prompt_bool("Include special symbols?")

        try:
            passwords = [
                generate_password(length, use_lower, use_upper, use_digits, use_symbols)
                for _ in range(num_passwords)
            ]
        except ValueError as e:
            print(f"\n {ACCENT_PINK}✖ Error: {e}{RESET}\n")
            input(f"\n {GRAY}Press Enter to try again...{RESET}")
            continue

        print(f"\n {PURPLE_LIGHT}Generating cryptographic keys...{RESET}")
        time.sleep(0.4)

        print(f"\n {GRAY}┌─ Generated Keys ─────────────────────────────────────┐{RESET}")
        for idx, pwd in enumerate(passwords, start=1):
            padded_idx = str(idx).zfill(2)
            print(f" {GRAY}│{RESET}  {PURPLE_LIGHT}[{padded_idx}]{RESET} {CYAN_SOFT}{pwd}{RESET}")
        print(f" {GRAY}└──────────────────────────────────────────────────────┘{RESET}")
        print(f"\n                   {WATERMARK}\n")

        again = prompt_bool("Generate more keys?")
        if not again:
            print(f"\n {CYAN_SOFT}Exiting vault. See you soon! {WATERMARK}\n")
            break

if __name__ == "__main__":
    main()
