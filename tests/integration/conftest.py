import pytest
from fastapi.testclient import TestClient

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.main import app
from app.infrastructure.db.database import get_db
from app.adapters.utils.debug import var_dump_die

class FakeMongoSession:
    def __init__(self):
        self._data = {}
        self.collections = {}

    def insert_one(self, data):
        _id = str(len(self._data) + 1)
        self._data[_id] = {**data, "_id": _id}
        
        return {"inserted_id": _id}

    def find_one(self, query):
        for item in self._data.values():
            if all(item.get(k) == v for k, v in query.items()):
                return item
        
        return None

    def find(self):
        return list(self._data.values())

    def update_one(self, query, update):
        item = self.find_one(query)
        
        if not item:
            return {"matched_count": 0}
        item.update(update["$set"])
        
        return {"matched_count": 1}

    def delete_one(self, query):
        to_delete = None
        
        for k, item in self._data.items():
            if all(item.get(f) == v for f, v in query.items()):
                to_delete = k
                break
        
        if to_delete:
            del self._data[to_delete]
            return {"deleted_count": 1}
        
        return {"deleted_count": 0}
    
    def __getitem__(self, name):
        if name not in self.collections:
            self.collections[name] = FakeMongoCollection()
            
        return self.collections[name]

class FakeMongoCollection:
    def __init__(self):
        self.items = []
        self._data = {}

    def insert_one(self, item):
        self.items.append(item)
        return {"inserted_id": len(self.items)}

    def find_one(self, query):
        return next((i for i in self.items if all(i[k] == v for k, v in query.items())), None)
    
    def get_collection(self, name):
        return FakeMongoCollection()
    
    def find(self, query=None):
        if not query:
            return list(self._data.values())
        
        return [
            doc for doc in self._data.values()
            if all(doc.get(k) == v for k, v in query.items())
        ]
    
    def update_one(self, query, update):
        for doc_id, doc in self._data.items():
            if all(doc.get(k) == v for k, v in query.items()):
                if "$set" in update:
                    self._data[doc_id].update(update["$set"])
                else:
                    self._data[doc_id].update(update)
                
                return {"matched_count": 1, "modified_count": 1}
        
        return {"matched_count": 0, "modified_count": 0}
    
    def delete_one(self, query):
        for doc_id in list(self._data.keys()):
            doc = self._data[doc_id]
            match = True
            
            # Comparação robusta entre query e documento
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break

            if match:
                var_dump_die('oi')
                del self._data[doc_id]
                return {"deleted_count": 1}

        return {"deleted_count": 0}
    
@pytest.fixture
def fake_db():
    return FakeMongoSession()

@pytest.fixture
def client(fake_db):
    def override_get_db():
        return fake_db
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()
