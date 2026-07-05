from dataclasses import dataclass, field


@dataclass
class Pokemon:
    name: str
    name_fr: str | None = None
    level: float | None = None
    ivs: float | None = None
    ability: str | None = None
    nature: str | None = None
    held_item: str | None = None
    moves: list[str] = field(default_factory=list)


@dataclass
class Trainer:
    trainer_class: str
    trainer_name: str
    location: str
    team: list[Pokemon] = field(default_factory=list)
