import logging
from typing import Dict, Optional

import httpx
from benedict import benedict
from cache_memoize import cache_memoize
from django import template
from django.conf import settings

register = template.Library()
logger = logging.getLogger(__name__)


def _get_data(url: str) -> Dict:
    res = httpx.get(
        url, auth=(settings.ENV["GITHUB_USERNAME"], settings.ENV["GITHUB_PERSONAL_ACCESS_TOKEN"]),
        follow_redirects=False,
    )

    if res.status_code in (301, 302):
        logger.error(f"Redirect detected for: {url}; redirecting to {res.next_request.url}")

        res = httpx.get(
            url, auth=(settings.ENV["GITHUB_USERNAME"], settings.ENV["GITHUB_PERSONAL_ACCESS_TOKEN"]),
            follow_redirects=True,
        )

    if res.is_error:
        logger.error(res.text)
    else:
        return res.json()


def get_repo_name(repo_url: str) -> str:
    github_repo_name = repo_url.strip()
    github_repo_name = github_repo_name.replace("https://github.com/", "")

    if github_repo_name.endswith("/"):
        github_repo_name = github_repo_name[:-1]

    return github_repo_name


def get_last_commit(repo_name: str) -> Optional[str]:
    commit_url = f"https://api.github.com/repos/{repo_name}/commits?page=1&per_page=1"
    commits = _get_data(commit_url)

    if commits and isinstance(commits, list):
        # Grab the first result because that's all we ever care about
        latest_commit = commits[0]

        latest_commit = benedict(latest_commit)

        return latest_commit["commit.committer.date"]


def get_license(repo: Dict) -> Optional[str]:
    license = repo.get("license") or {}

    if license and license.get("spdx_id"):
        if license.get("url"):
            return f'<a href="{license.get("url")}">{license.get("spdx_id")}</a>'
        elif license.get("url"):
            return license.get("spdx_id")


def get_repo(repo_name: str) -> Dict:
    repo_url = f"https://api.github.com/repos/{repo_name}"

    return _get_data(repo_url)


def get_latest_release(repo_name: str) -> Optional[Dict]:
    releases_url = (
        f"https://api.github.com/repos/{repo_name}/releases?page=1&per_page=1"
    )
    releases = _get_data(releases_url)

    if releases and isinstance(releases, list):
        return releases[0]


@cache_memoize(60 * 60 * 24, prefix="20230617")
def get_github_metadata(repo_name: str) -> Dict:
    metadata = {
        "description": None,
        "homepage_url": None,
        "stars": None,
        "watchers": None,
        "forks": None,
        "open_issues": None,
        "last_commit": None,
        "latest_version": "",
        "latest_tag": None,
        "license": None,
    }

    metadata["last_commit"] = get_last_commit(repo_name)

    latest_release = get_latest_release(repo_name)

    if latest_release:
        metadata["latest_version"] = latest_release.get("name")
        metadata["latest_tag"] = latest_release.get("tag_name")

    repo = get_repo(repo_name)

    if repo:
        metadata["full_name"] = repo.get("full_name")
        metadata["description"] = repo.get("description")
        metadata["homepage_url"] = repo.get("homepage")
        metadata["stars"] = repo.get("stargazers_count")
        metadata["watchers"] = repo.get("subscribers_count")
        metadata["forks"] = repo.get("forks")
        metadata["open_issues"] = repo.get("open_issues")

        metadata["license"] = get_license(repo)

    return metadata
