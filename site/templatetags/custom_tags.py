import logging

import emoji_data_python
import iso8601
from api.github import add_metadata_from_graphql
from django import template

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter(name="humanize_int")
def humanize_int(value: int) -> str:
    try:
        if value:
            return f"{value:,}"
    except Exception:
        pass

    return str(value)


@register.filter(name="humanize_datetime")
def humanize_datetime(value: str) -> str:
    if value:
        return iso8601.parse_date(value).strftime("%Y-%m-%d")


@register.simple_tag
def hydrate_metadata(libraries: list[dict]) -> list[dict]:
    sort_key = "last_commit"

    try:
        libraries = add_metadata_from_graphql(libraries)

        return sorted(
            libraries, key=lambda l: l.get(sort_key) or "", reverse=True
        )
    except AssertionError as e:
        logger.exception(e)


@register.filter(name="emojize")
def emojize(value: str) -> str:
    if value:
        return emoji_data_python.replace_colons(value)

    return value
