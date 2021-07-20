import httpx
from benedict import benedict

from models import Library

LIBRARY_CACHE_TIMEOUT = 60 * 10
LIBRARY_TOML_FILE_NAME = "libraries.toml"


async def get_libraries(cache, github_username: str, github_personal_access_token: str):
    libraries = await cache.get("libraries")

    if libraries:
        return libraries

    parsed_libraries = benedict(LIBRARY_TOML_FILE_NAME, format="toml")
    libraries = []

    for value in parsed_libraries.values():
        libraries.append(Library(**value))

    async def set_data(url, obj, **attributes):
        """
        Sets data on the model object.

        Params:
            attributes: kwargs with attribute name as the key and target spec as the value.
        """
        async with httpx.AsyncClient() as client:
            res = await client.get(
                url, auth=(github_username, github_personal_access_token)
            )

            try:
                res.raise_for_status()
                data = res.json()

                # If the JSON was a list, just grab the first result because that's all we ever care about
                if isinstance(data, list):
                    data = data[0]

                data = benedict(data)

                for attribute_name, key_path in attributes.items():
                    value = data[key_path]
                    setattr(obj, attribute_name, value)
            except Exception as e:
                print(e)

    for library in libraries:
        if library.repo_name and library.is_github_repo:
            commit_url = f"https://api.github.com/repos/{library.repo_name}/commits?page=1&per_page=1"
            await set_data(commit_url, library, last_commit="commit.committer.date")

            repo_url = f"https://api.github.com/repos/{library.repo_name}"
            await set_data(
                repo_url,
                library,
                description="description",
                homepage_url="homepage",
                stars="stargazers_count",
                watchers="subscribers_count",
                forks="forks",
                open_issues="open_issues",
            )

            releases_url = f"https://api.github.com/repos/{library.repo_name}/releases?page=1&per_page=1"
            await set_data(
                releases_url, library, latest_version="name", latest_tag="tag_name"
            )

    libraries = sorted(libraries, key=lambda l: l.last_commit, reverse=True)

    # Put libraries in cache
    await cache.set("libraries", libraries, ttl=LIBRARY_CACHE_TIMEOUT)

    return libraries
