from pathlib import Path
import os


class ApplicationConfig:

    @classmethod
    def BASE_URL(cls) -> str:
        if cls.MODE() == "TEST":
            return "http://127.0.0.1:8000"
        else:
            return "https://api.localhost/"


    @classmethod
    def BASE_DIR(cls) -> Path:
        return Path(os.path.dirname(os.path.abspath(__file__))).parent


    @classmethod
    def STATIC_DIR(cls) -> Path: 
        return Path(f"{cls.BASE_DIR()}/static")
    

    @classmethod
    def TOKENS_JSON_PATH(cls) -> Path:
        if cls.MODE() == "TEST":
            return Path(f"{cls.BASE_DIR()}/test/test_tokens.json")
        else:
            return Path(f"{cls.STATIC_DIR()}/tokens.json")
    

    @classmethod
    def SEARCH_VALUES_JSON_PATH(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/search_values.json")


    @classmethod
    def SAVES_DIR(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/saves")
    

    @classmethod
    def MODE(cls) -> str:
        return os.getenv("MODE")


    @classmethod
    def WELDER_REGISTRY_PATH(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/welder_registry.xlsx")
