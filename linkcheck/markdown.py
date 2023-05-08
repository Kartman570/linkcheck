import re


def content(text):
    return re.sub(r"```[^\n]*\n.*?```|~~~[^\n]*\n.*?~~~", "", text, flags=re.S)


def links(text):
    cleaned = content(text)
    return [(match.start(), match.group(1).strip("<>")) for match in re.finditer(
        r'!?\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+"[^"\n]*")?\)', cleaned)]


def reference_links(text):
    cleaned = content(text)
    definitions = {m.group(1).strip().lower(): m.group(2).strip("<>")
                   for m in re.finditer(r"(?m)^\s*\[([^\]]+)\]:\s*(\S+)", cleaned)}
    found = []
    for match in re.finditer(r"\[([^\]]+)\]\[([^\]]*)\]", cleaned):
        label = (match.group(2) or match.group(1)).strip().lower()
        found.append((match.start(), definitions.get(label, "missing-reference:" + label)))
    return found
