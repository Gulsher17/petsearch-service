from pymongo import MongoClient
from app.core.config import settings

def get_mongo_client():
    return MongoClient(settings.MONGO_URI)

def assert_read_only(method_name: str):
    raise PermissionError(f"Write operation '{method_name}' not allowed in read-only mode.")

def enforce_read_only(collection):
    for method in ["insert_one", "insert_many", "update_one", "delete_one", "replace_one"]:
        setattr(collection, method, lambda *a, **kw: assert_read_only(method))
    return collection

def pets_collection():
    col = get_mongo_client()[settings.MONGO_DB][settings.COLLECTION]
    return enforce_read_only(col)
