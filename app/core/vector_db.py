from qdrant_client import QdrantClient
from qdrant_client.http import models as qm
from app.core.config import settings
import uuid


def client():
    """Return a Qdrant client connected to configured host/port."""
    return QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)


def ensure_collection(dim: int = 768):
    """Ensure the Qdrant collection exists; create if missing."""
    c = client()
    existing = {col.name for col in c.get_collections().collections}
    if settings.QDRANT_COLLECTION not in existing:
        c.recreate_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=qm.VectorParams(size=dim, distance=qm.Distance.COSINE),
        )
        print(f"✅ Created Qdrant collection '{settings.QDRANT_COLLECTION}'")
    else:
        print(f"✅ Qdrant collection '{settings.QDRANT_COLLECTION}' already exists.")


def upsert_points(vectors, payloads):
    """
    Upsert points into Qdrant.
    Generates UUIDs for each record but keeps Mongo ID in payload.
    """
    ids = []
    for p in payloads:
        if "mongo_id" not in p:
            raise ValueError("Payload missing 'mongo_id'")
        ids.append(str(uuid.uuid4()))  # ✅ Generate valid UUIDs for Qdrant

    c = client()
    ensure_collection(len(vectors[0]))

    c.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=qm.Batch(
            ids=ids,
            vectors=vectors,
            payloads=payloads,
        ),
    )
    print(f"🟢 Upserted {len(vectors)} vectors into Qdrant.")


def search_vector(query_vec, limit=10, filters=None):
    """
    Search for similar vectors in Qdrant and return a simplified list of dicts.
    """
    c = client()
    flt = None
    if filters:
        must = [
            qm.FieldCondition(key=k, match=qm.MatchValue(value=v))
            for k, v in filters.items()
        ]
        flt = qm.Filter(must=must)

    hits = c.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=query_vec,
        limit=limit,
        query_filter=flt,
    )

    # Normalize to plain dicts
    return [
        {"id": h.id, "score": h.score, "payload": h.payload or {}}
        for h in hits
    ]
