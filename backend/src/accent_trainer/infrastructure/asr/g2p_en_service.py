from __future__ import annotations

import logging
import re
from functools import lru_cache

from g2p_en import G2p

from accent_trainer.application.interfaces.g2p_service import G2PService

logger = logging.getLogger(__name__)

_STRESS_DIGIT = re.compile(r"\d+$")


@lru_cache(maxsize=1)
def _get_g2p() -> G2p:
    return G2p()


class G2PEnService(G2PService):
    def to_phonemes(self, word: str) -> list[str]:
        word = word.strip().lower()
        if not word:
            return []
        g2p = _get_g2p()
        raw: list[str] = g2p(word)
        out: list[str] = []
        for tok in raw:
            tok = tok.strip()
            if not tok or not tok[0].isalpha():
                # skip punctuation/space tokens g2p_en emits
                continue
            # strip stress markers: "EH1" -> "EH"
            out.append(_STRESS_DIGIT.sub("", tok))
        return out