import os
import ssl
import sys

from pymongo import MongoClient
from pymongo.errors import PyMongoError

try:
    import certifi
except ImportError:
    certifi = None

DEBUG_FALLBACK_MONGODB_URI = ""

DEFAULT_DB_NAME = "lanchonete_pagamento_database"

def _redact_mongodb_uri(uri: str) -> str:
    """Redact credentials from MongoDB URI for safe logging."""
    if not uri:
        return ""
    if "@" in uri:
        return uri.split("@", 1)[0].split("://")[0] + "://***@" + uri.split("@", 1)[1].split("/")[0]
    return "<redacted-uri>"


def get_db():
    """Return a MongoDB database handle with connectivity diagnostics."""

    mongodb_uri = os.getenv("MONGODB_URI") or DEBUG_FALLBACK_MONGODB_URI
    db_name = os.getenv("MONGODB_DB_NAME", DEFAULT_DB_NAME)

    if not mongodb_uri:
        raise RuntimeError("MongoDB URI not configured")

    py_ver = sys.version.split()[0]
    openssl_ver = getattr(ssl, "OPENSSL_VERSION", "unknown")

    print(
        f"[MongoDB] Connecting... uri={_redact_mongodb_uri(mongodb_uri)} db={db_name} "
        f"python={py_ver} openssl={openssl_ver}"
    )

    try:
        client_kwargs = dict(
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=10000,
        )

        # Explicit CA bundle fixes TLS issues on macOS / corporate networks
        if certifi is not None:
            client_kwargs["tlsCAFile"] = certifi.where()

        client = MongoClient(mongodb_uri, **client_kwargs)

        # Force handshake + auth
        client.admin.command("ping")
        print("[MongoDB] Ping OK")

        return client[db_name]

    except PyMongoError as e:
        raise RuntimeError(f"MongoDB connection failed: {type(e).__name__}: {e}") from e


if __name__ == "__main__":
    db = get_db()
    print(f"Connected to MongoDB database: {db.name}")