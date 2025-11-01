import re

ALLERGENS_KR = [
    "eggs", "milk", "buckwheat", "peanuts", "soybeans", "wheat",
    "mackerel", "crab", "shrimp", "pork", "peach", "tomato",
    "sulfurous acid", "walnuts", "chicken", "beef", "squid",
    "clams", "oyster", "abalone", "mussels", "pine nut"
]

def parse_ingredients(text: str):
    """
    Extracts clean ingredient list from translated text.
    Removes country names, addresses, and irrelevant sections.
    """
    text = text.lower()

    # Detect "ingredients" or "raw material" section
    match = re.search(
        r"(ingredients|raw material|raw materials|raw material name|raw material name and content)[:\s]*(.*)",
        text, re.DOTALL)
    if match:
        text = match.group(2)

    # Stop at irrelevant section markers
    text = re.split(
        r"(expiration|manufacturer|storage|return|exchange|packaging|report|nutritional|nutrition|contains)",
        text
    )[0]

    # Normalize separators
    text = re.sub(r'[\n\r]+', ', ', text)
    parts = re.split(r'[.,;:/()•·\-\n]+', text)

    # Words to filter out
    blocked_words = [
        "usa", "america", "australia", "canada", "china", "japan", "france",
        "imported", "origin", "country", "etc", "jinmi", "food", "co", "ltd",
        "report", "exchange", "storage", "address", "ml", "g", "pe", "company"
    ]

    cleaned = [
        p.strip() for p in parts
        if p.strip()
        and len(p.strip()) > 2
        and not any(b in p for b in blocked_words)
    ]

    # Merge specific multi-word ingredients
    merged = []
    skip_next = False
    for i, word in enumerate(cleaned):
        if skip_next:
            skip_next = False
            continue
        if i + 1 < len(cleaned) and (cleaned[i] == "enzyme" and "stevia" in cleaned[i + 1]):
            merged.append("enzyme-treated stevia")
            skip_next = True
        else:
            merged.append(word)

    # Remove duplicates while keeping order
    seen, final = set(), []
    for p in merged:
        if p not in seen:
            seen.add(p)
            final.append(p)

    return final


def detect_allergens(text: str):
    """
    Detect allergens manually based on the official South Korean list.
    Matches in the translated English text.
    """
    found = []
    text = text.lower()
    for a in ALLERGENS_KR:
        if a in text:
            found.append(a)
    return sorted(set(found))