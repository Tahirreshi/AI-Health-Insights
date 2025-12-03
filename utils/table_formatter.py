import re

FLAG_PATTERN = re.compile(r'\b(h|l|high|low|↑|↓|\*|>|\<)\b', flags=re.IGNORECASE)

def extract_table(text):
    """
    Return cleaned lines likely to be lab rows.
    Keep only lines with letters + digits and skip obvious headers.
    """
    lines = text.splitlines()
    rows = []

    for line in lines:
        clean = re.sub(r'\s+', ' ', line).strip()
        if len(clean) < 4:
            continue

        # must contain at least one letter and one digit
        if not re.search(r'[A-Za-z]', clean) or not re.search(r'\d', clean):
            continue

        # skip common header words
        if clean.lower().startswith(("sample", "name", "age", "sex", "medical", "department", "ref", "report", "submitted")):
            continue

        rows.append(clean)

    return rows


def convert_to_table(rows):
    """
    Convert cleaned OCR lines into a structured table:
    [parameter, value, unit, ref_range, flag]
    """
    table = []

    for row in rows:
        parts = row.split()

        # detect first numeric token as "value"
        value_idx = None
        for i, tok in enumerate(parts):
            if re.search(r"\d", tok):
                value_idx = i
                break

        if value_idx is None:
            continue

        param = " ".join(parts[:value_idx]).replace(":", "").strip()
        value = parts[value_idx]
        unit = ""
        ref_range = ""
        flag = ""

        # possible unit next
        pos = value_idx + 1
        if pos < len(parts) and ("/" in parts[pos] or "%" in parts[pos] or re.search(r"[a-zA-Z]", parts[pos])):
            unit = parts[pos]
            pos += 1

        # possible ref range, must contain "-" or be two numbers
        ref_tokens = []
        while pos < len(parts):
            tok = parts[pos]

            # detect flag
            if FLAG_PATTERN.search(tok):
                flag = tok
                pos += 1
                continue

            if "-" in tok or re.search(r"\d", tok):
                ref_tokens.append(tok)
                pos += 1
            else:
                pos += 1
        
        if ref_tokens:
            ref_range = " ".join(ref_tokens)

        # add final row
        table.append([param, value, unit, ref_range, flag])

    return table



def filter_abnormal(table):
    """
    Universal abnormal detector:
    Return only rows that contain HIGH/LOW flags,
    without relying on predefined parameter names.
    """
    abnormal = []

    for row in table:
        param, value, unit, ref_range, flag = row

        # Row must contain alphabetic parameter name
        if not re.search(r"[A-Za-z]", param):
            continue
        
        # Must contain some numeric value
        if not re.search(r"\d", value):
            continue

        # Flag present anywhere in the row → abnormal
        row_text = " ".join(row).lower()
        if FLAG_PATTERN.search(row_text):
            abnormal.append(row)

    return abnormal

