import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(f"{Path.cwd().parent}/.env")


class Settings:

    @classmethod
    def DB_NAME(cls) -> str:
        return os.getenv("DATABASE_NAME")
    
    
    @classmethod
    def DB_PASSWORD(cls) -> str:
        return os.getenv("DATABASE_PASSWORD")
    

    @classmethod
    def HOST(cls) -> str:
        return os.getenv("HOST")
    

    @classmethod
    def USER(cls) -> str:
        return os.getenv("USER")
    

    @classmethod
    def PORT(cls) -> str:
        return os.getenv("PORT")
    

    @classmethod
    def MODE(cls) -> str:
        return os.getenv("MODE")
    

    @classmethod
    def BASE_DIR(cls) -> Path:
        if cls.MODE() == "TEST":
            return Path.cwd()
        
        return Path.cwd().parent


    @classmethod
    def SAVES_DIR(cls) -> Path:
        return f"{cls.BASE_DIR()}/static/saves"
