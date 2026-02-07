from collections import Counter
from typing import List

from database import get_all_votes, save_vote_to_db
from fastapi import APIRouter, HTTPException
from models import VoteCandidates, VoteRequest

router = APIRouter()


@router.get("/candidates", response_model=List[str])
async def get_voting_candidates():
    """Vraća listu kandidata za koje je moguće glasati."""
    return [candidate.value for candidate in VoteCandidates]


@router.post("/vote")
async def vote(vote: VoteRequest):
    """Zaprima novi glas."""
    try:
        result = save_vote_to_db(vote.option.value)
        return {
            "message": "Glas uspješno zaprimljen!",
            "option": vote.option,
            "data": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
async def get_results():
    """Dohvaća sve glasove po kandidatu."""
    try:
        raw_votes = get_all_votes()

        vote_options = [v["option"] for v in raw_votes]

        results = Counter(vote_options)

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/votes")
async def get_raw_votes():
    """Vraća raw podatke (za admina)."""
    try:
        votes = get_all_votes()
        return {"count": len(votes), "votes": votes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
