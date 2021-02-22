from typing import Optional

from card import Card


class Category:
    def __init__(self, name: str, api_suffix: Optional[str] = None):
        self.name = name
        self.api_suffix = '| ' + api_suffix if api_suffix else None

    def create_card(self) -> Card:
        return Card(name=self.name, suffix=self.api_suffix)
