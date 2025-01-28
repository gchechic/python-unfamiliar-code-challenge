from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

class Items(BaseModel):
    items: Dict[str, int]

@app.post("/foo")
def foo(items: Items):
    return items.items

client = TestClient(app)

def test_additional_properties_post():
    response = client.post("/foo", json={"items": {"foo": 1, "bar": 2}})
    assert response.status_code == 200, response.text
    assert response.json() == {"foo": 1, "bar": 2}

def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert schema["openapi"] == "3.0.2"
    assert schema["info"]["title"] == "FastAPI"
    assert schema["info"]["version"] == "0.1.0"
    assert "/foo" in schema["paths"]
    assert "post" in schema["paths"]["/foo"]
    assert "responses" in schema["paths"]["/foo"]["post"]
    assert "200" in schema["paths"]["/foo"]["post"]["responses"]
    assert "description" in schema["paths"]["/foo"]["post"]["responses"]["200"]
    assert schema["paths"]["/foo"]["post"]["responses"]["200"]["description"] == "Successful Response"
    assert "content" in schema["paths"]["/foo"]["post"]["responses"]["200"]
    assert "application/json" in schema["paths"]["/foo"]["post"]["responses"]["200"]["content"]
    assert "schema" in schema["paths"]["/foo"]["post"]["responses"]["200"]["content"]["application/json"]
    assert schema["paths"]["/foo"]["post"]["responses"]["200"]["content"]["application/json"]["schema"] == {}

def test_additional_properties_false():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    assert "components" in schema
    assert "schemas" in schema["components"]
    assert "Items" in schema["components"]["schemas"]
    assert "additionalProperties" in schema["components"]["schemas"]["Items"]
    assert schema["components"]["schemas"]["Items"]["additionalProperties"] is False