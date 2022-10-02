from dataclasses import dataclass
from typing import Optional


@dataclass
class EntryResult:
    resourceName: str
    description: str
    status: Optional[str] = None
    location: Optional[str] = None

@dataclass
class BundleResult:
    statusCode:int
    entries: list[EntryResult]