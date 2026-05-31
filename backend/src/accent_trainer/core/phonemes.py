ENGLISH_VOWELS: frozenset[str] = frozenset({
    "AA", "AE", "AH", "AO", "AW", "AY",
    "EH", "ER", "EY",
    "IH", "IY",
    "OW", "OY",
    "UH", "UW",
})


def is_vowel(phoneme: str) -> bool:
    return phoneme.upper() in ENGLISH_VOWELS