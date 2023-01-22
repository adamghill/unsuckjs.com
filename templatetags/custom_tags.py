import logging
from typing import Dict, List, Union

import httpx
import iso8601
from benedict import benedict
from cache_memoize import cache_memoize
from django import template
from django.conf import settings

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter(name="humanize_int")
def humanize_int(value: int) -> str:
    if value is not None:
        return "{:,}".format(value)


@register.filter(name="humanize_datetime")
def humanize_datetime(value: str) -> str:
    if value:
        return iso8601.parse_date(value).strftime("%Y-%m-%d")


def _get_github_data(url: str) -> Dict:
    res = httpx.get(
        url, auth=(settings.GITHUB_USERNAME, settings.GITHUB_PERSONAL_ACCESS_TOKEN)
    )

    if res.is_error:
        logger.error(res.text)
    else:
        return res.json()


@cache_memoize(60 * 60 * 24)
def _get_github_metadata(repo_name: str) -> Dict:
    metadata = {
        "description": None,
        "homepage_url": None,
        "stars": None,
        "watchers": None,
        "forks": None,
        "open_issues": None,
        "last_commit": None,
        "latest_version": None,
        "latest_tag": None,
    }

    commit_url = f"https://api.github.com/repos/{repo_name}/commits?page=1&per_page=1"
    commits = _get_github_data(commit_url)

    if commits:
        # Just grab the first result because that's all we ever care about
        latest_commit = commits[0]

        latest_commit = benedict(latest_commit)
        metadata["last_commit"] = latest_commit["commit.committer.date"]

    repo_url = f"https://api.github.com/repos/{repo_name}"
    repo = _get_github_data(repo_url)

    if repo:
        metadata["description"] = repo.get("description")
        metadata["homepage_url"] = repo.get("homepage")
        metadata["stars"] = repo.get("stargazers_count")
        metadata["watchers"] = repo.get("subscribers_count")
        metadata["forks"] = repo.get("forks")
        metadata["open_issues"] = repo.get("open_issues")

    releases_url = (
        f"https://api.github.com/repos/{repo_name}/releases?page=1&per_page=1"
    )
    releases = _get_github_data(releases_url)

    if releases:
        latest_release = releases[0]
        metadata["latest_version"] = latest_release.get("name")
        metadata["latest_tag"] = latest_release.get("tag_name")

    return metadata


def _get_github_repo_name(repo_url: str) -> str:
    github_repo_name = repo_url.strip()
    github_repo_name = github_repo_name.replace("https://github.com/", "")

    if github_repo_name.endswith("/"):
        github_repo_name = github_repo_name[:-1]

    return github_repo_name


def _get_repo_name(library: Dict) -> str:
    if "github.com" in library.get("repo_url").lower():
        return _get_github_repo_name(library.get("repo_url"))


def _get_metadata_value(library: Dict, key: str) -> Union[int, str]:
    repo_name = _get_repo_name(library)

    if repo_name:
        metadata = _get_github_metadata(repo_name)

        return metadata[key]


@register.simple_tag
def repo(library: Dict) -> Dict:
    repo_name = _get_repo_name(library)

    if repo_name:
        return _get_github_metadata(repo_name)


@register.simple_tag
def sort_libraries_by_stars(libraries: List[Dict]) -> List[Dict]:
    return sorted(
        libraries, key=lambda l: _get_metadata_value(l, "last_commit"), reverse=True
    )
