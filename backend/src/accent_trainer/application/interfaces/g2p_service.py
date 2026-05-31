from __future__ import annotations

from abc import ABC, abstractmethod


class G2PService(ABC):
    @abstractmethod
    def to_phonemes(self, word: str) -> list[str]:
        """Return ARPAbet phonemes for one word, without stress markers."""