from dataclasses import dataclass, field
from Name import Name
from Phone import Phone


@dataclass
class NewRecord:
    name: Name
    phones: list[Phone] = field(default_factory=list)