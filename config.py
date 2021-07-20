from pydantic import BaseSettings


class Settings(BaseSettings):
    github_username: str
    github_personal_access_token: str

    class Config:
        env_file = ".env"
