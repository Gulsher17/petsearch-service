from fastapi import APIRouter, Depends, Query, HTTPException
from bson import ObjectId
from app.core.auth_jwt import verify_jwt
from app.core.db_client import pets_collection
from app.core.vector_db import search_vector
from app.utils.embeddings import embed_text

router = APIRouter(prefix="/search", tags=["search"])


def intent_boost(pet: dict, q: str) -> float:
    q = q.lower()
    boost = 0.0

    # Behavioral intent matching
    energy = pet.get("energyLevel", "").lower()
    if "active" in q and energy == "high":
        boost += 0.12
    if "calm" in q and energy == "low":
        boost += 0.12

    # Keyword boosting for tags + temperament
    words = q.split()
    tags = [t.lower() for t in (pet.get("tags") or [])]
    temp = [t.lower() for t in (pet.get("temperament") or [])]
    for w in words:
        if w in tags or w in temp:
            boost += 0.05

    return min(boost, 0.25)


@router.get("")
async def search(
    q: str = Query(...),
    breed: str | None = None,
    location: str | None = None,
    energy: str | None = None,
    top_k: int = 12,
    user=Depends(verify_jwt),
):
    q_vec = embed_text(q)
    hits = search_vector(q_vec, limit=top_k * 3)

    col = pets_collection()
    results = []

    for h in hits:
        payload = h.get("payload", {})
        mongo_id = payload.get("mongo_id")
        if not mongo_id:
            continue

        pet = col.find_one({"_id": ObjectId(mongo_id)})
        if not pet:
            continue

        # Optional UI filters
        if breed and pet.get("breed", "").lower() != breed.lower():
            continue
        if location and pet.get("location", "").lower() != location.lower():
            continue
        if energy and pet.get("energyLevel", "").lower() != energy.lower():
            continue

        vec_score = float(h.get("score", 0))
        b = intent_boost(pet, q)
        final_score = 0.85 * vec_score + 0.15 * b

        pet["_id"] = str(pet["_id"])
        pet["_score"] = round(final_score, 4)
        results.append(pet)

    results.sort(key=lambda x: x["_score"], reverse=True)
    return {"results": results[:top_k], "count": len(results)}
