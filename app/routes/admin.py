from fastapi import APIRouter, Depends, HTTPException
from app.core.auth_jwt import verify_jwt
from app.core.db_client import pets_collection
from app.core.vector_db import ensure_collection, upsert_points
from app.utils.embeddings import embed_text, make_search_doc

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/reindex")
async def reindex(limit: int = 200, user=Depends(verify_jwt)):
    col = pets_collection()
    cursor = col.find({}, {
        "name": 1, "breed": 1, "tags": 1,
        "description": 1, "temperament": 1,
        "location": 1, "energyLevel": 1
    }).limit(limit)

    vectors, payloads = [], []
    count = 0

    for pet in cursor:
        sd = make_search_doc(pet)
        vec = embed_text(sd)
        vectors.append(vec)

        payloads.append({
            "mongo_id": str(pet["_id"]),
            "breed": pet.get("breed"),
            "location": pet.get("location"),
            "tags": pet.get("tags"),
            "energyLevel": pet.get("energyLevel"),
        })
        count += 1

    if not vectors:
        raise HTTPException(status_code=404, detail="No pets to index")

    ensure_collection(len(vectors[0]))
    upsert_points(vectors, payloads)

    return {"indexed": count}
