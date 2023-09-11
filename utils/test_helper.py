import helper
import pytest

class TestParseConfig:
    def test_simple_case(self):
        model_fixture = {"name": "testmodel", "url": "grpc://localhost:50051"}
        config_fixture = {"models": [model_fixture]}
        
        c = helper.parse_configs(config_fixture)
        assert c.models["testmodel"] == model_fixture
    