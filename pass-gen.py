#!/usr/bin/env python3
import argparse
import base64
import getpass
import hashlib
import hmac
import json
import math
import os
import secrets
import shutil
import string
import struct
import subprocess
import sys
import time
import urllib.request
import uuid
from datetime import datetime

# Enable ANSI escape codes on Windows
os.system("")

secure_rng = secrets.SystemRandom()

# --- Color & Style Palette (ANSI Escape Codes) ---
RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"

PURPLE_MID   = "\033[38;2;140;110;200m"
PURPLE_LIGHT = "\033[38;2;190;160;255m"
CYAN_SOFT    = "\033[38;2;130;220;255m"
ACCENT_PINK  = "\033[38;2;255;150;200m"
GREEN_SOFT   = "\033[38;2;140;240;180m"
YELLOW_SOFT  = "\033[38;2;255;220;130m"
WHITE        = "\033[38;2;240;240;255m"
GRAY         = "\033[38;2;110;110;140m"

SYMBOLS = "!@#$%^&*()-_=+[]{}<>?"
AMBIGUOUS = "l1IO0"
WATERMARK = f"{ACCENT_PINK}{BOLD}! moonlight <3{RESET}"
VAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".moonlight_vault.json")

WORD_LIST = [
    "nebula", "velvet", "cipher", "moonlight", "astral", "phantom", "quartz",
    "vortex", "eclipse", "shadow", "cobalt", "prism", "zenith", "aurora",
    "obsidian", "halcyon", "mirage", "solstice", "paradox", "valkyrie",
    "aether", "horizon", "pulse", "nova", "specter", "cosmos", "lynx",
    "onyx", "celeste", "drift", "echo", "frost", "glimmer", "haven",
    "ion", "jade", "krypton", "lumen", "matrix", "nexus", "orbit",
    "plasma", "quasar", "rune", "starlight", "titan", "umbra", "vector",
    "whisper", "xenon", "yonder", "zephyr", "arcane", "binary", "chrono",
    "delta", "ember", "flux", "galaxy", "helix", "indigo", "jolt", "karma",
    "lunar", "mythic", "nectar", "omega", "photon", "quantum", "radiant",
    "seraph", "tempest", "ultra", "vivid", "warden", "xylo", "zen"
]

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
           ╚═════╝  ╚══════╝ ╚═╝  ╚═══╝ ╚══════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝    ╚═╝     ╚═════╝  ╚═╝  ╚═╝

                                    {ACCENT_PINK}✦  made by: {WATERMARK} {ACCENT_PINK}✦{RESET}
"""

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
                                
          {ACCENT_PINK}✦  made by: {WATERMARK} {ACCENT_PINK}✦{RESET}"""


# ─── UI & Terminal Helpers ──────────────────────────────────────────────────

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def play_startup_sequence():
    clear_screen()
    print(STARTUP_LOGO)
    steps = [
        (PURPLE_LIGHT, "Initializing environment..."),
        (CYAN_SOFT,    "Mounting CSPRNG entropy pool & HIBP k-Anonymity engine..."),
        (ACCENT_PINK,  "Launching moonlight security suite...")
    ]
    for color, text in steps:
        print(f"        {color}✦ {text}{RESET}")
        time.sleep(0.3)


def print_main_screen():
    clear_screen()
    print(MAIN_LOGO)
    vault_count = len(load_vault_raw())
    vault_badge = f"{GREEN_SOFT}{vault_count} locked{RESET}" if vault_count else f"{GRAY}empty{RESET}"
    print(f" {GRAY}┌──────────────────────────────────────────────────────────────┐{RESET}")
    print(f" {GRAY}│{RESET}  {CYAN_SOFT}✦ SECURITY SUITE ✦{RESET}   |   Vault: {vault_badge}   |   {WATERMARK}  {GRAY}│{RESET}")
    print(f" {GRAY}└──────────────────────────────────────────────────────────────┘{RESET}\n")


def prompt_bool(message, default=True):
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        choice = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}{message} {GRAY}{hint}{RESET}: ").strip().upper()
        if not choice:
            return default
        if choice in ("Y", "YES"):
            return True
        if choice in ("N", "NO"):
            return False
        print(f"   {ACCENT_PINK}⚠ Please enter 'Y' or 'N'.{RESET}")


def prompt_int(message, min_val=1, max_val=999, default=None):
    hint = f" {GRAY}[default: {default}]{RESET}" if default is not None else ""
    while True:
        val = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}{message}{hint}: ").strip()
        if not val and default is not None:
            return default
        if val.isdigit() and min_val <= int(val) <= max_val:
            return int(val)
        print(f"   {ACCENT_PINK}⚠ Enter a number between {min_val} and {max_val}.{RESET}")


def colorize_password(pwd):
    out = []
    for ch in pwd:
        if ch.isdigit():
            out.append(f"{CYAN_SOFT}{ch}{RESET}")
        elif ch in SYMBOLS or ch in "-_":
            out.append(f"{ACCENT_PINK}{ch}{RESET}")
        else:
            out.append(f"{WHITE}{ch}{RESET}")
    return "".join(out)


def animate_decrypt_line(idx_str, pwd, padding):
    glyphs = "0123456789ABCDEF#$%&*@!?"
    length = len(pwd)
    steps = 8
    for step in range(steps):
        revealed = int((step / steps) * length)
        partial = colorize_password(pwd[:revealed])
        scrambled = "".join(secrets.choice(glyphs) for _ in range(length - revealed))
        sys.stdout.write(
            f"\r {GRAY}│{RESET}  {PURPLE_LIGHT}[{idx_str}]{RESET} {partial}{PURPLE_MID}{scrambled}{RESET}{padding}{GRAY}│{RESET}"
        )
        sys.stdout.flush()
        time.sleep(0.015)
    sys.stdout.write(
        f"\r {GRAY}│{RESET}  {PURPLE_LIGHT}[{idx_str}]{RESET} {colorize_password(pwd)}{padding}{GRAY}│{RESET}\n"
    )
    sys.stdout.flush()


def format_entropy_bar(bits):
    fill = min(20, max(1, int(round((bits / 128.0) * 20))))
    bar_str = "█" * fill + "░" * (20 - fill)

    if bits < 50:
        color, label, crack = ACCENT_PINK, "Weak", "Minutes to Hours"
    elif bits < 75:
        color, label, crack = YELLOW_SOFT, "Moderate", "Years to Centuries"
    elif bits < 100:
        color, label, crack = CYAN_SOFT, "Strong", "Millions of Years"
    else:
        color, label, crack = GREEN_SOFT, "Vault-Grade", "Heat Death of Universe"

    return (
        f"{color}[{bar_str}] {BOLD}{label}{RESET} {GRAY}({bits} bits){RESET}\n"
        f"  {GRAY}Est. Crack Time (Offline Fast Hash):{RESET} {WHITE}{crack}{RESET}"
    )


def _get_clipboard_cmds():
    if sys.platform == "win32":
        return [["clip"]]
    elif sys.platform == "darwin":
        return [["pbcopy"]]
    cmds = []
    if shutil.which("wl-copy"):
        cmds.append(["wl-copy"])
    if shutil.which("xclip"):
        cmds.append(["xclip", "-selection", "clipboard"])
    if shutil.which("xsel"):
        cmds.append(["xsel", "--clipboard", "--input"])
    return cmds


def copy_to_clipboard(text, auto_clear_sec=25):
    """Copies text and spawns a detached background process to wipe it after N seconds."""
    commands = _get_clipboard_cmds()
    copied_cmd = None
    for cmd in commands:
        try:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, close_fds=True)
            proc.communicate(input=text.encode("utf-8"))
            if proc.returncode == 0:
                copied_cmd = cmd
                break
        except Exception:
            continue

    if not copied_cmd:
        return False

    if auto_clear_sec > 0:
        try:
            wipe_code = (
                f"import time, subprocess; time.sleep({auto_clear_sec}); "
                f"p = subprocess.Popen({repr(copied_cmd)}, stdin=subprocess.PIPE); "
                f"p.communicate(input=b'')"
            )
            subprocess.Popen(
                [sys.executable, "-c", wipe_code],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                start_new_session=True,
            )
        except Exception:
            pass
    return True


# ─── Generators & Deterministic Key Derivation ──────────────────────────────

def generate_password(length, use_lower, use_upper, use_digits, use_symbols, no_ambiguous=False):
    active_sets = []
    if use_lower:
        active_sets.append(string.ascii_lowercase)
    if use_upper:
        active_sets.append(string.ascii_uppercase)
    if use_digits:
        active_sets.append(string.digits)
    if use_symbols:
        active_sets.append(SYMBOLS)

    if no_ambiguous:
        active_sets = ["".join(c for c in s if c not in AMBIGUOUS) for s in active_sets]
        active_sets = [s for s in active_sets if s]

    if not active_sets:
        raise ValueError("You must select at least one character type.")
    if length < len(active_sets):
        raise ValueError(f"Length must be at least {len(active_sets)} for chosen requirements.")

    pool = "".join(active_sets)
    password_chars = [secrets.choice(char_set) for char_set in active_sets]
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(pool) for _ in range(remaining))

    secure_rng.shuffle(password_chars)
    bits = round(length * math.log2(len(pool)), 1)
    return "".join(password_chars), bits


def generate_passphrase(num_words=4, separator="-"):
    words = [secrets.choice(WORD_LIST) for _ in range(num_words)]
    num_badge = str(secrets.randbelow(90) + 10)
    insert_pos = secrets.randbelow(num_words)
    words[insert_pos] = f"{words[insert_pos]}{separator}{num_badge}"

    phrase = separator.join(words)
    bits = round(num_words * math.log2(len(WORD_LIST)) + math.log2(90), 1)
    return phrase, bits


def generate_dev_token(token_type, master_phrase="", service_domain="", counter=1):
    alnum = string.ascii_letters + string.digits
    if token_type == 1:
        body = "".join(secrets.choice(alnum) for _ in range(32))
        return f"sk_live_{body}", round(32 * math.log2(62), 1)
    elif token_type == 2:
        body = "".join(secrets.choice(alnum) for _ in range(36))
        return f"ghp_{body}", round(36 * math.log2(62), 1)
    elif token_type == 3:
        return secrets.token_hex(32), 256.0
    elif token_type == 4:
        return str(uuid.UUID(bytes=secrets.token_bytes(16), version=4)), 122.0
    else:
        # Deterministic Site-Specific Key via PBKDF2-HMAC-SHA512
        salt = f"moonlight-deterministic:{service_domain.lower().strip()}:v{counter}".encode("utf-8")
        dk = hashlib.pbkdf2_hmac("sha512", master_phrase.encode("utf-8"), salt, 250_000, dklen=32)
        sets = [string.ascii_lowercase, string.ascii_uppercase, string.digits, SYMBOLS]
        pool = "".join(sets)
        chars = [sets[i][dk[i] % len(sets[i])] for i in range(4)]
        for b in dk[4:20]:
            chars.append(pool[b % len(pool)])
        # Deterministic shuffle using remaining bytes
        for i in range(len(chars) - 1, 0, -1):
            j = dk[20 + (i % 12)] % (i + 1)
            chars[i], chars[j] = chars[j], chars[i]
        return "".join(chars), round(20 * math.log2(len(pool)), 1)


# ─── HIBP Dark Web Breach Check & Password Auditor ──────────────────────────

def check_hibp_breach(pwd):
    """Queries HaveIBeenPwned API using k-Anonymity (only first 5 SHA-1 hex chars sent)."""
    sha1_hash = hashlib.sha1(pwd.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Moonlight-Security-Suite"})
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            body = resp.read().decode("utf-8")
        for line in body.splitlines():
            parts = line.split(":")
            if len(parts) == 2 and parts[0].strip() == suffix:
                return int(parts[1].strip())
        return 0
    except Exception:
        return None


def audit_password(pwd):
    if not pwd:
        return
    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_sym   = any(not c.isalnum() for c in pwd)

    pool = (26 if has_lower else 0) + (26 if has_upper else 0) + (10 if has_digit else 0) + (32 if has_sym else 0)
    raw_bits = len(pwd) * math.log2(max(pool, 1))

    unique_ratio = len(set(pwd)) / len(pwd)
    effective_bits = round(raw_bits * (0.5 + 0.5 * unique_ratio), 1)

    warnings = []
    if len(pwd) < 12:
        warnings.append("Length is under 12 characters.")
    if unique_ratio < 0.65:
        warnings.append("High character repetition detected.")
    for seq in ("123", "234", "345", "456", "789", "abc", "qwerty", "password", "admin"):
        if seq in pwd.lower():
            warnings.append(f"Contains predictable sequence '{seq}'.")
            effective_bits = max(10.0, round(effective_bits * 0.5, 1))
            break

    print(f"\n {PURPLE_LIGHT}✦ Querying k-Anonymity breach database...{RESET}")
    pwned_count = check_hibp_breach(pwd)
    if pwned_count and pwned_count > 0:
        effective_bits = min(effective_bits, 15.0)
        warnings.append(f"EXPOSED IN {pwned_count:,} KNOWN DATA BREACHES (Do not use!)")

    print(f"\n {GRAY}┌─ Security Audit & Breach Report ─────────────────────┐{RESET}")
    print(f" {GRAY}│{RESET}  {WHITE}Analyzed Key:{RESET}  {colorize_password(pwd)}")
    print(f" {GRAY}│{RESET}  {WHITE}Length:{RESET}        {CYAN_SOFT}{len(pwd)} chars{RESET} ({len(set(pwd))} unique)")
    print(f" {GRAY}│{RESET}  {WHITE}Composition:{RESET}   "
          f"{GREEN_SOFT if has_lower else GRAY}a-z{RESET}  "
          f"{GREEN_SOFT if has_upper else GRAY}A-Z{RESET}  "
          f"{GREEN_SOFT if has_digit else GRAY}0-9{RESET}  "
          f"{GREEN_SOFT if has_sym else GRAY}!@#{RESET}")
    if pwned_count is None:
        breach_str = f"{YELLOW_SOFT}Offline (Could not reach HIBP API){RESET}"
    elif pwned_count == 0:
        breach_str = f"{GREEN_SOFT}0 breaches found (Clean){RESET}"
    else:
        breach_str = f"{ACCENT_PINK}{BOLD}COMPROMISED ({pwned_count:,} leaks){RESET}"
    print(f" {GRAY}│{RESET}  {WHITE}Dark Web Check:{RESET} {breach_str}")
    print(f" {GRAY}└──────────────────────────────────────────────────────┘{RESET}")
    print(f"  {GRAY}Rating:{RESET}   {format_entropy_bar(effective_bits)}")

    if warnings:
        print(f"\n  {ACCENT_PINK}⚠ Vulnerabilities Found:{RESET}")
        for w in warnings:
            print(f"    {ACCENT_PINK}•{RESET} {WHITE}{w}{RESET}")
    else:
        print(f"\n  {GREEN_SOFT}✔ Zero structural weaknesses and zero known data breaches.{RESET}")


# ─── RFC 6238 Live TOTP 2FA Authenticator ───────────────────────────────────

def generate_totp(secret_b32, time_step=30, digits=6):
    clean = secret_b32.strip().replace(" ", "").upper()
    clean += "=" * ((8 - len(clean) % 8) % 8)
    key = base64.b32decode(clean, casefold=True)
    now = int(time.time())
    counter = now // time_step
    rem = time_step - (now % time_step)

    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code_int = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code_int).zfill(digits), rem


def run_totp_live():
    print(f"\n {GRAY}── Live 2FA / TOTP Authenticator (RFC 6238) ──{RESET}")
    secret = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Enter Base32 2FA Secret (or Enter for demo secret):{RESET} ").strip()
    if not secret:
        secret = "JBSWY3DPEHPK3PXP"
        print(f"   {GRAY}Using demo secret: {secret}{RESET}")

    try:
        generate_totp(secret)
    except Exception:
        print(f"\n {ACCENT_PINK}✖ Invalid Base32 secret string.{RESET}")
        input(f"\n {GRAY}Press Enter to return...{RESET}")
        return

    print(f"\n {CYAN_SOFT}✦ Live 2FA Token Stream (Press Ctrl+C to return to menu){RESET}\n")
    try:
        while True:
            code, rem = generate_totp(secret)
            bar_fill = int((rem / 30.0) * 15)
            bar = "█" * bar_fill + "░" * (15 - bar_fill)
            color = GREEN_SOFT if rem > 10 else (YELLOW_SOFT if rem > 5 else ACCENT_PINK)
            formatted_code = f"{code[:3]} {code[3:]}"
            sys.stdout.write(
                f"\r   {PURPLE_LIGHT}🔒 2FA Code:{RESET} {BOLD}{WHITE}{formatted_code}{RESET}   "
                f"{color}[{bar}] {rem:02d}s{RESET}   "
            )
            sys.stdout.flush()
            time.sleep(0.25)
    except KeyboardInterrupt:
        print(f"\n\n   {GRAY}Exited 2FA live view.{RESET}")
        time.sleep(0.5)


# ─── Encrypted Vault & Cryptographic File Locker ────────────────────────────

def _derive_keys(master_password, salt):
    dk = hashlib.pbkdf2_hmac("sha256", master_password.encode("utf-8"), salt, 200_000, dklen=64)
    return dk[:32], dk[32:]


def _keystream_xor(data_bytes, enc_key, nonce):
    out = bytearray(len(data_bytes))
    blocks = (len(data_bytes) + 31) // 32
    for counter in range(blocks):
        counter_bytes = counter.to_bytes(8, "big")
        keystream_block = hashlib.sha256(enc_key + nonce + counter_bytes).digest()
        start = counter * 32
        end = min(start + 32, len(data_bytes))
        for i in range(start, end):
            out[i] = data_bytes[i] ^ keystream_block[i - start]
    return bytes(out)


def encrypt_bytes(raw_bytes, master_password):
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(16)
    enc_key, mac_key = _derive_keys(master_password, salt)
    ciphertext = _keystream_xor(raw_bytes, enc_key, nonce)
    tag = hmac.new(mac_key, salt + nonce + ciphertext, hashlib.sha256).digest()
    return {
        "salt": base64.b64encode(salt).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
        "mac": base64.b64encode(tag).decode("ascii"),
    }


def decrypt_bytes(record, master_password):
    salt = base64.b64decode(record["salt"])
    nonce = base64.b64decode(record["nonce"])
    ciphertext = base64.b64decode(record["ciphertext"])
    expected_mac = base64.b64decode(record["mac"])

    enc_key, mac_key = _derive_keys(master_password, salt)
    actual_mac = hmac.new(mac_key, salt + nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(expected_mac, actual_mac):
        raise ValueError("Invalid Master Password or tampered ciphertext.")
    return _keystream_xor(ciphertext, enc_key, nonce)


def load_vault_raw():
    if not os.path.exists(VAULT_FILE):
        return []
    try:
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_to_vault(label, secret_key, master_password):
    vault = load_vault_raw()
    encrypted = encrypt_bytes(secret_key.encode("utf-8"), master_password)
    encrypted["label"] = label
    encrypted["created"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    vault.append(encrypted)
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(vault, f, indent=2)


def manage_vault_menu():
    vault = load_vault_raw()
    if not vault:
        print(f"\n {YELLOW_SOFT}⚠ Your encrypted vault is currently empty.{RESET}")
        print(f" {GRAY}Generate keys first and press [V] to lock a key into the vault.{RESET}")
        input(f"\n {GRAY}Press Enter to return...{RESET}")
        return

    print(f"\n {GRAY}── Encrypted Vault ({len(vault)} entries) ──{RESET}")
    for idx, item in enumerate(vault, start=1):
        print(f"  {PURPLE_LIGHT}[{idx:02d}]{RESET} {WHITE}{item['label']:<22}{RESET} {GRAY}({item['created']}){RESET}")

    print(f"\n  {PURPLE_LIGHT}[U]{RESET} Unlock & Decrypt   {PURPLE_LIGHT}[S]{RESET} Search Label   {PURPLE_LIGHT}[D]{RESET} Delete   {PURPLE_LIGHT}[Enter]{RESET} Back")
    cmd = input(f"\n {PURPLE_LIGHT}❯{RESET} {WHITE}Select vault action:{RESET} ").strip().upper()

    if cmd in ("U", "S"):
        query = ""
        if cmd == "S":
            query = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Filter by label:{RESET} ").strip().lower()
        master = getpass.getpass(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Enter Master Password:{RESET} ")
        print(f"\n {GRAY}┌─ Decrypted Vault Keys ────────────────────────────────┐{RESET}")
        unlocked_any = False
        for idx, item in enumerate(vault, start=1):
            if query and query not in item["label"].lower():
                continue
            try:
                plain = decrypt_bytes(item, master).decode("utf-8")
                unlocked_any = True
                print(f" {GRAY}│{RESET}  {PURPLE_LIGHT}[{idx:02d}]{RESET} {WHITE}{item['label']:<16}{RESET} ➔  {colorize_password(plain)}")
            except ValueError:
                print(f" {GRAY}│{RESET}  {PURPLE_LIGHT}[{idx:02d}]{RESET} {WHITE}{item['label']:<16}{RESET} ➔  {ACCENT_PINK}[🔒 Wrong Master Password]{RESET}")
        print(f" {GRAY}└───────────────────────────────────────────────────────┘{RESET}")
        if unlocked_any:
            copy_idx = input(f"\n {PURPLE_LIGHT}❯{RESET} {WHITE}Enter entry # to copy (or Enter to return):{RESET} ").strip()
            if copy_idx.isdigit() and 1 <= int(copy_idx) <= len(vault):
                try:
                    plain = decrypt_bytes(vault[int(copy_idx) - 1], master).decode("utf-8")
                    if copy_to_clipboard(plain):
                        print(f"   {GREEN_SOFT}✔ Copied to clipboard (Auto-wipes in 25s)!{RESET}")
                        time.sleep(0.9)
                except ValueError:
                    pass
        else:
            input(f"\n {GRAY}Press Enter to return...{RESET}")

    elif cmd == "D":
        del_idx = prompt_int("Enter entry # to delete", min_val=1, max_val=len(vault))
        removed = vault.pop(del_idx - 1)
        with open(VAULT_FILE, "w", encoding="utf-8") as f:
            json.dump(vault, f, indent=2)
        print(f"   {GREEN_SOFT}✔ Removed '{removed['label']}' from vault.{RESET}")
        time.sleep(0.8)


def file_locker_menu():
    print(f"\n {GRAY}── Cryptographic File Locker (PBKDF2-HMAC-SHA256) ──{RESET}")
    print(f"  {PURPLE_LIGHT}[1]{RESET} {WHITE}Encrypt a File{RESET}  {GRAY}(Creates a locked .moonlock file){RESET}")
    print(f"  {PURPLE_LIGHT}[2]{RESET} {WHITE}Decrypt a File{RESET}  {GRAY}(Restores a .moonlock file){RESET}")
    choice = prompt_int("Select action", 1, 2, default=1)
    filepath = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Enter file path:{RESET} ").strip().strip("'\"")

    if not os.path.isfile(filepath):
        print(f"   {ACCENT_PINK}✖ File not found: {filepath}{RESET}")
        input(f"\n {GRAY}Press Enter to return...{RESET}")
        return

    master = getpass.getpass(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Enter Master Password:{RESET} ")
    if not master:
        print(f"   {ACCENT_PINK}✖ Password cannot be empty.{RESET}")
        input(f"\n {GRAY}Press Enter to return...{RESET}")
        return

    try:
        if choice == 1:
            with open(filepath, "rb") as f:
                raw = f.read()
            payload = encrypt_bytes(raw, master)
            out_path = filepath + ".moonlock"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(payload, f)
            print(f"\n   {GREEN_SOFT}✔ File encrypted successfully ➔ {out_path}{RESET}")
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                payload = json.load(f)
            raw = decrypt_bytes(payload, master)
            out_path = filepath[:-9] if filepath.endswith(".moonlock") else filepath + ".decrypted"
            with open(out_path, "wb") as f:
                f.write(raw)
            print(f"\n   {GREEN_SOFT}✔ File verified & decrypted ➔ {out_path}{RESET}")
    except Exception as e:
        print(f"\n   {ACCENT_PINK}✖ Operation failed: {e}{RESET}")

    input(f"\n {GRAY}Press Enter to return...{RESET}")


# ─── Main Loop & CLI Entry ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Moonlight Security Suite")
    parser.add_argument("-q", "--quick", action="store_true", help="Generate a 24-char vault key and exit immediately")
    parser.add_argument("-l", "--length", type=int, default=24, help="Key length for quick mode (default: 24)")
    parser.add_argument("--no-splash", action="store_true", help="Skip startup splash screen")
    args = parser.parse_args()

    if args.quick:
        pwd, bits = generate_password(max(4, args.length), True, True, True, True, no_ambiguous=True)
        copied = copy_to_clipboard(pwd)
        copy_badge = f"{GREEN_SOFT}(Copied — auto-wipes in 25s){RESET}" if copied else ""
        print(f" {PURPLE_LIGHT}✦{RESET} {colorize_password(pwd)}  {GRAY}[{bits} bits]{RESET} {copy_badge}")
        return

    if not args.no_splash:
        play_startup_sequence()

    while True:
        print_main_screen()
        print(f" {GRAY}── Select Operation Mode ──{RESET}")
        print(f"  {PURPLE_LIGHT}[1]{RESET} {WHITE}Custom Cryptographic Key{RESET} {GRAY}(Configurable character sets){RESET}")
        print(f"  {PURPLE_LIGHT}[2]{RESET} {WHITE}Memorable Passphrase{RESET}     {GRAY}(e.g. nebula-42-velvet-cipher){RESET}")
        print(f"  {PURPLE_LIGHT}[3]{RESET} {WHITE}Developer & Site Keys{RESET}    {GRAY}(API tokens, Hex, Deterministic keys){RESET}")
        print(f"  {PURPLE_LIGHT}[4]{RESET} {WHITE}Breach & Strength Audit{RESET}  {GRAY}(HIBP Dark Web check + entropy report){RESET}")
        print(f"  {PURPLE_LIGHT}[5]{RESET} {WHITE}Live 2FA Authenticator{RESET}   {GRAY}(Real-time RFC 6238 TOTP generator){RESET}")
        print(f"  {PURPLE_LIGHT}[6]{RESET} {WHITE}Encrypted Key Vault{RESET}      {GRAY}(Unlock, search, or manage saved keys){RESET}")
        print(f"  {PURPLE_LIGHT}[7]{RESET} {WHITE}Cryptographic File Lock{RESET}  {GRAY}(Encrypt/decrypt local files){RESET}\n")

        mode = prompt_int("Select mode", min_val=1, max_val=7, default=1)

        if mode == 4:
            target = input(f"\n {PURPLE_LIGHT}❯{RESET} {WHITE}Enter password to audit:{RESET} ").strip()
            audit_password(target)
            input(f"\n {GRAY}Press Enter to return to menu...{RESET}")
            continue
        elif mode == 5:
            run_totp_live()
            continue
        elif mode == 6:
            manage_vault_menu()
            continue
        elif mode == 7:
            file_locker_menu()
            continue

        num_passwords = prompt_int("How many keys to generate?", min_val=1, max_val=50, default=3)

        try:
            if mode == 1:
                length = prompt_int("Key length", min_val=4, max_val=128, default=16)
                print(f"\n {GRAY}── Configuration Settings (Press Enter for defaults) ──{RESET}")
                use_lower    = prompt_bool("Include lowercase letters?", default=True)
                use_upper    = prompt_bool("Include uppercase letters?", default=True)
                use_digits   = prompt_bool("Include numbers?", default=True)
                use_symbols  = prompt_bool("Include special symbols?", default=True)
                no_ambiguous = prompt_bool("Exclude look-alike chars (l, 1, I, O, 0)?", default=False)

                results = [
                    generate_password(length, use_lower, use_upper, use_digits, use_symbols, no_ambiguous)
                    for _ in range(num_passwords)
                ]
            elif mode == 2:
                words_count = prompt_int("Number of words", min_val=3, max_val=10, default=4)
                results = [generate_passphrase(words_count) for _ in range(num_passwords)]
            elif mode == 3:
                print(f"\n {GRAY}── Select Key / Token Format ──{RESET}")
                print(f"  {PURPLE_LIGHT}[1]{RESET} {WHITE}Stripe-style Live Key{RESET}    {GRAY}(sk_live_...){RESET}")
                print(f"  {PURPLE_LIGHT}[2]{RESET} {WHITE}GitHub-style PAT{RESET}         {GRAY}(ghp_...){RESET}")
                print(f"  {PURPLE_LIGHT}[3]{RESET} {WHITE}256-Bit Hex Secret{RESET}       {GRAY}(64 hex chars){RESET}")
                print(f"  {PURPLE_LIGHT}[4]{RESET} {WHITE}UUID v4 Identifier{RESET}       {GRAY}(xxxxxxxx-xxxx-4xxx-...){RESET}")
                print(f"  {PURPLE_LIGHT}[5]{RESET} {WHITE}Deterministic Site Key{RESET}   {GRAY}(Derived from Master Phrase + Domain){RESET}")
                t_type = prompt_int("Format", min_val=1, max_val=5, default=1)
                if t_type == 5:
                    domain = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Service/Domain (e.g. github.com):{RESET} ").strip() or "default"
                    m_phrase = getpass.getpass(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Master Phrase:{RESET} ")
                    results = [generate_dev_token(5, m_phrase, domain, i + 1) for i in range(num_passwords)]
                else:
                    results = [generate_dev_token(t_type) for _ in range(num_passwords)]

            passwords = [r[0] for r in results]
            entropy_bits = results[0][1]

        except ValueError as e:
            print(f"\n {ACCENT_PINK}✖ Error: {e}{RESET}")
            input(f"\n {GRAY}Press Enter to try again...{RESET}")
            continue

        max_pwd_len = max(len(p) for p in passwords)
        box_width = max(56, max_pwd_len + 10)
        header_title = "─ Generated Keys "
        top_border = f"┌{header_title}{'─' * (box_width - len(header_title))}┐"
        bottom_border = f"└{'─' * box_width}┘"

        print(f"\n {GRAY}{top_border}{RESET}")
        for idx, pwd in enumerate(passwords, start=1):
            padded_idx = str(idx).zfill(2)
            padding = " " * (box_width - len(pwd) - 8)
            animate_decrypt_line(padded_idx, pwd, padding)
        print(f" {GRAY}{bottom_border}{RESET}")

        print(f"  {GRAY}Legend:{RESET}   {WHITE}Letters{RESET}  |  {CYAN_SOFT}Numbers{RESET}  |  {ACCENT_PINK}Symbols{RESET}")
        print(f"  {GRAY}Security:{RESET} {format_entropy_bar(entropy_bits)}")
        print(f"\n                   {WATERMARK}\n")

        while True:
            action = input(
                f" {PURPLE_LIGHT}❯{RESET} {WHITE}Action:{RESET} "
                f"{PURPLE_LIGHT}[Enter]{RESET} Menu  "
                f"{PURPLE_LIGHT}[C]{RESET} Copy (25s wipe)  "
                f"{PURPLE_LIGHT}[V]{RESET} Lock in Vault  "
                f"{PURPLE_LIGHT}[Q]{RESET} Quit: "
            ).strip().upper()

            if action == "":
                break
            elif action == "C":
                idx_to_copy = 1
                if len(passwords) > 1:
                    idx_to_copy = prompt_int(f"Which key # to copy (1-{len(passwords)})?", 1, len(passwords), default=1)
                if copy_to_clipboard(passwords[idx_to_copy - 1]):
                    print(f"   {GREEN_SOFT}✔ Key [{idx_to_copy:02d}] copied (Clipboard auto-scrubs in 25s)!{RESET}")
                else:
                    print(f"   {ACCENT_PINK}⚠ Clipboard tool not found (install wl-copy or xclip on Linux).{RESET}")
            elif action == "V":
                idx_to_save = 1
                if len(passwords) > 1:
                    idx_to_save = prompt_int(f"Which key # to lock in vault (1-{len(passwords)})?", 1, len(passwords), default=1)
                label = input(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Label for this key (e.g. GitHub, Discord):{RESET} ").strip() or "Untitled"
                master = getpass.getpass(f" {PURPLE_LIGHT}❯{RESET} {WHITE}Set/Enter Master Password to encrypt:{RESET} ")
                if not master:
                    print(f"   {ACCENT_PINK}⚠ Master password cannot be empty.{RESET}")
                else:
                    save_to_vault(label, passwords[idx_to_save - 1], master)
                    print(f"   {GREEN_SOFT}✔ Key [{idx_to_save:02d}] encrypted & locked under '{label}'!{RESET}")
            elif action in ("Q", "N", "NO"):
                print(f"\n {CYAN_SOFT}Exiting vault. See you soon! {WATERMARK}\n")
                return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n {ACCENT_PINK}✦ Session aborted. Exiting vault... {WATERMARK}\n")
        sys.exit(0)