"""Common source adapter interfaces."""
from __future__ import annotations

from abc import ABC, abstractmethod

from scraper.models import Article, Publisher


class BaseSourceAdapter(ABC):
    def __init__(self, publisher: Publisher, max_items: int = 30) -> None:
        self.publisher = publisher
        self.max_items = max_items

    @abstractmethod
    async def fetch(self) -> list[Article]:
        """Fetch source headlines without article bodies."""
