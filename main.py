import datetime
import lib
import yaml
from pathlib import Path
import os

from rich.console import Console

console = Console()

with open('config.yml', 'r', encoding='utf-8') as f:
    s = f.read()
    config = yaml.safe_load(s)

csv_file = Path(config['csv_file'])
if not csv_file.exists():
    print(f"CSV file {csv_file} does not exist.")
    exit(1)

password = config['password']


def string_contains_list_any(string, lst) -> bool:
    for s in lst:
        low = s.lower()
        if low in string.lower():
            return True
    return False


def write_file():
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        plaintext = f.read()

    lines = plaintext.split('\n')
    new_lines = []
    for line in lines:
        sline = line.strip()
        if string_contains_list_any(sline, config['private']):
            console.print(f"Skipping private line: {sline}")
            continue
        new_lines.append(sline)

    plaintext = '\n'.join(new_lines)

    encrypted = lib.encrypt_string(plaintext, password)
    with open('./static/data.js', 'w', encoding='utf-8') as g:
        g.write(f"window.data = '{encrypted}';")

    console.print(f"Encrypted data written to {csv_file}.")


def push_to_cloud():
    ask = console.input("Push to cloud? (Y/n) ")
    if ask.lower() != 'y':
        return

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.system("git add static/data.js")
    os.system(f"git commit -m 'Update data.js at {now}'")
    os.system("git push origin master")
    console.print("[bold green]Pushed to cloud.")


if __name__ == "__main__":
    write_file()
    push_to_cloud()
