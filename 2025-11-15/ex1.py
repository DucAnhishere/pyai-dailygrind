def clean_text(text: str) -> str:
    if text is None:
        return text
    lowercased = text.lower().strip()
    removed_punctuation = ''.join(char for char in lowercased if char.isalnum() or char.isspace())
    replaced_spaces = ' '.join(removed_punctuation.split())
    return replaced_spaces

def extract_fields(doc: dict, fields: list[str]) -> dict:
    result = {}
    for field in fields:
        value = doc.get(field, None)
        if isinstance(value, str):
            result[field] = value
        else:
            result[field] = value
    return result

def merge_docs(a: dict, b: dict) -> dict:
    keys = a.keys() | b.keys()
    merged = {}
    for key in keys:
        if key in a:
            merged[key] = a[key]
        else:
            merged[key] = b[key]
    return merged
