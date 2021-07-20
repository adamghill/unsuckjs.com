import iso8601
from fastapi.templating import Jinja2Templates


def humanize_int(value: int) -> str:
    if value is not None:
        return "{:,}".format(value)


def humanize_datetime(value: str) -> str:
    if value:
        return iso8601.parse_date(value).strftime("%Y-%m-%d")


def get_templates():
    templates = Jinja2Templates(directory="templates")
    templates.env.filters["humanize_int"] = humanize_int
    templates.env.filters["humanize_datetime"] = humanize_datetime

    return templates
