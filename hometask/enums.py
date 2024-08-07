import enum


class ProfileType(enum.Enum):
    client = "client"
    contractor = "contractor"


class ContractStatus(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    terminated = "terminated"
