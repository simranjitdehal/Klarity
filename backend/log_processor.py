import re

def extract_exception(raw_log: str):
    lines = raw_log.splitlines()

    pattern = re.compile(r"^\s*([A-Za-z_][\w\.]*(Error|Exception))(?::\s*(.*))?$")

    for line in reversed(lines):
        line = line.strip()

        match = pattern.match(line)   # 👈 use match instead of search
        if match:
            exception_type = match.group(1)
            exception_message = match.group(3) or ""
            return exception_type, exception_message

    return None, None

def extract_file_info(raw_log: str):
    lines = raw_log.splitlines()

    pattern = re.compile(r'File "(.+)", line (\d+), in (.+)')

    file_matches = []

    for line in lines:
        line = line.strip()
        match = pattern.match(line)

        if match:
            file_path = match.group(1)
            line_number = int(match.group(2))
            function_name = match.group(3)

            file_matches.append((file_path, line_number, function_name))

    if not file_matches:
        return None, None, None 

    IGNORE_PATTERNS = ["site-packages", "venv", "__pycache__", "/usr/", "lib/python"]

    relevant = [
        f for f in file_matches
        if not any(p in f[0] for p in IGNORE_PATTERNS)
    ]

    chosen = relevant[-1] if relevant else file_matches[-1]

    return chosen