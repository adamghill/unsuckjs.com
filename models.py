from datetime import datetime
from typing import List

from pydantic import BaseModel, HttpUrl


class Library(BaseModel):
    name: str
    repo_url: HttpUrl
    homepage_url: HttpUrl = None
    description: str = None
    size: str = None
    ie11_compatible: bool = False
    web_components: bool = False
    cdn_url: str = None
    latest_version: str = None
    latest_tag: str = None
    last_commit: datetime = None
    stars: int = None
    watchers: int = None
    forks: int = None
    open_issues: int = None
    categories: List[str] = []

    @property
    def is_github_repo(self):
        return "github.com" in self.repo_url.lower()

    @property
    def repo_name(self):
        if self.is_github_repo:
            github_repo_name = self.repo_url.strip()
            github_repo_name = github_repo_name.replace("https://github.com/", "")

            if github_repo_name.endswith("/"):
                github_repo_name = github_repo_name[:-1]

            return github_repo_name
