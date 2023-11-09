from fastapi.testclient import TestClient
from main import app

import os

os.environ["LFAI_CONFIG_FILENAME"] = "test-config.yaml"
os.environ["LFAI_CONFIG_PATH"] = os.path.dirname(__file__) 


def test_config_load():
    with TestClient(app) as client:
        response = client.get("/models")
        assert response.status_code == 200
        assert response.json() == {"models":  {'whisper-1': {'backend': 'localhost:50052', 'name': 'whisper-1'}}}


def test_routes():
    expected_routes = {
        "/docs": ['GET', 'HEAD'],
        "/healthz": ['GET'],
        "/models": ['GET'],
        "/openai/v1/completions": ['POST'],
        "/openai/v1/chat/completions": ['POST'],
        "/openai/v1/models": ['GET'],
        "/openai/v1/embeddings": ['POST'],
        "/openai/v1/audio/transcriptions": ['POST'],
    }

    actual_routes = app.routes
    for route in actual_routes:
        if hasattr(route, "path") and route.path in expected_routes:
            assert route.methods == set(expected_routes[route.path])
            del expected_routes[route.path]

    assert len(expected_routes) == 0
