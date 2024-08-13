import enum


class ProfileType(enum.StrEnum):
    client = "client"
    contractor = "contractor"


class ContractStatus(enum.StrEnum):
    new = "new"
    in_progress = "in_progress"
    terminated = "terminated"
