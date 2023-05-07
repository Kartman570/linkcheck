import re


def content(text):
    return re.sub(r"```[^\n]*\n.*?```|~~~[^\n]*\n.*?~~~", "", text, flags=re.S)


def links(text):
    cleaned = content(text)
    return [(match.start(), match.group(1).strip("<>")) for match in re.finditer(
        r'!?\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+"[^"\n]*")?\)', cleaned)]
