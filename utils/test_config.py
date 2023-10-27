import utils.config as config


class TestParseConfig:
    def test_simple_case(self):
        model_fixture = {"name": "testmodel", "url": "grpc://localhost:50051"}
        config_fixture = {"models": [model_fixture]}

        c = config.Config()
        c.parse_models(config_fixture)
        assert c.models["testmodel"] == model_fixture


class TestConfig:
    def test_existing_model_backend(self):
        c = config.Config(
            {
                "test": config.Model(
                    name="test", backend="grpc://localhost:50051", capabilities=None
                )
            }
        )
        assert c.get_model_backend("test") == "grpc://localhost:50051"
