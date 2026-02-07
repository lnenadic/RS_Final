from enum import Enum

from pydantic import BaseModel


class VoteCandidates(str, Enum):
    TEAM_A = "Tim A"
    TEAM_B = "Tim B"
    TEAM_C = "Tim C"


class VoteRequest(BaseModel):
    option: VoteCandidates
