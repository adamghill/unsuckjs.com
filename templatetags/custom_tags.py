import logging
from typing import Dict, List, Union

import iso8601
from django import template

from api.github import get_github_metadata, get_repo_name

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


def _get_repo_name(library: Dict) -> str:
    if "github.com" in library.get("repo_url").lower():
        return get_repo_name(library.get("repo_url"))


def _get_metadata_value(library: Dict, key: str) -> Union[int, str]:
    repo_name = _get_repo_name(library)

    if repo_name:
        metadata = get_github_metadata(repo_name)

        return metadata[key]


@register.simple_tag
def repo(library: Dict) -> Dict:
    repo_name = _get_repo_name(library)

    if repo_name:
        return get_github_metadata(repo_name)


@register.simple_tag
def sort_libraries(libraries: List[Dict], key: str) -> List[Dict]:
    return sorted(
        libraries, key=lambda l: _get_metadata_value(l, key) or "", reverse=True
    )
