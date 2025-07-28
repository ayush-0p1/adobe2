from __future__ import annotations
from dataclasses import dataclass
from typing import List
import yaml

@dataclass
class Persona:
    id: str
    role: str
    expertise: List[str]
    job: str
    keywords: List[str]
    def prompt(self) -> str:
        kws = ", ".join(self.keywords)
        exp = ", ".join(self.expertise)
        return f"Role: {self.role}. Expertise: {exp}. Job: {self.job}. Keywords: {kws}."

def load_personas(path: str) -> List[Persona]:
    data = yaml.safe_load(open(path, "r", encoding="utf-8"))
    res = []
    for p in data.get("personas", []):
        res.append(Persona(
            id=p["id"], role=p["role"], expertise=p.get("expertise", []),
            job=p["job"], keywords=p.get("keywords", [])
        ))
    return res
