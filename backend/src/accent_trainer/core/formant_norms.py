"""Normative vowel formant frequencies (Hz) for General American English.

Values approximate adult male/neutral speaker. Sources: Hillenbrand et al. 1995.
For female speakers F1/F2 are roughly +15-20%, but MVP uses neutral baseline.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class FormantNorm:
    f1: float
    f2: float


ENGLISH_VOWEL_NORMS: dict[str, FormantNorm] = {
    "IY": FormantNorm(f1=270,  f2=2290),   # beat
    "IH": FormantNorm(f1=390,  f2=1990),   # bit
    "EH": FormantNorm(f1=530,  f2=1840),   # bet
    "AE": FormantNorm(f1=660,  f2=1720),   # bat
    "AA": FormantNorm(f1=730,  f2=1090),   # father
    "AO": FormantNorm(f1=570,  f2=840),    # bought
    "UH": FormantNorm(f1=440,  f2=1020),   # put
    "UW": FormantNorm(f1=300,  f2=870),    # boot
    "AH": FormantNorm(f1=640,  f2=1190),   # but
    "ER": FormantNorm(f1=490,  f2=1350),   # bird
    # Diphthongs: approximate to nucleus
    "EY": FormantNorm(f1=480,  f2=2000),   # bait
    "AY": FormantNorm(f1=700,  f2=1300),   # bite
    "OY": FormantNorm(f1=550,  f2=900),    # boy
    "AW": FormantNorm(f1=680,  f2=1100),   # bout
    "OW": FormantNorm(f1=500,  f2=900),    # boat
}


def get_norm(phoneme: str) -> FormantNorm | None:
    return ENGLISH_VOWEL_NORMS.get(phoneme.upper())