import logging

import httpx
from benedict import benedict
from cache_memoize import cache_memoize
from django import template
from django.conf import settings

register = template.Library()
logger = logging.getLogger(__name__)


def get_repo_name(repo_url: str) -> str:
    github_repo_name = repo_url.strip()
    github_repo_name = github_repo_name.replace("https://github.com/", "")

    if github_repo_name.endswith("/"):
        github_repo_name = github_repo_name[:-1]

    return github_repo_name


def run_gql(repo_names):
    # TODO: Chunk up the list and run multiple queries when there are more than 100 libraries
    search_repos = " ".join([f"repo:{r}" for r in repo_names])

    gql = """
query repos($repo_names: String!) {
  search(
    type: REPOSITORY
    query: $repo_names
    first: 100
  ) {
    nodes {
      ... on Repository {
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 1) {
                edges {
                  node {
                    authoredDate
                  }
                }
              }
            }
          }
        }
        id
        description
        homepageUrl
        stargazers {
          totalCount
        }
        watchers {
          totalCount
        }
        forks {
          totalCount
        }
        nameWithOwner
        licenseInfo {
          url
          spdxId
        }
        issues(states: [OPEN]) {
          totalCount
        }
        releases(first: 1) {
          totalCount
          nodes {
            name
            tagName
          }
        }
      }
    }
  }
}
"""

    headers = {"Authorization": f"Bearer {settings.ENV['GITHUB_PERSONAL_ACCESS_TOKEN']}"}

    res = httpx.post("https://api.github.com/graphql",
        json={"query": gql, "variables": {"repo_names": search_repos}},
        headers=headers,
        timeout=30)

    return res.json()


@cache_memoize(60 * 60 * 24, prefix="20240731")
def add_metadata_from_graphql(libraries: list[dict]) -> list[dict]:
    repo_names = [get_repo_name(l["repo_url"]) for l in libraries]

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

    data = run_gql(repo_names)

    if "data" not in data:
        raise AssertionError("Missing data from GraphQL")

    graphql_search_nodes = data["data"]["search"]["nodes"]

    for library in libraries:
        library_metadata = metadata.copy()
        repo_name = get_repo_name(library["repo_url"])

        graphql_data = filter(lambda d: d["nameWithOwner"] == repo_name, graphql_search_nodes)

        try:
            graphql_data = next(iter(graphql_data))
        except StopIteration:
            continue

        graphql_data = benedict(graphql_data)

        library_metadata["description"] = graphql_data.description
        library_metadata["homepage_url"] = graphql_data.homepageUrl
        library_metadata["stars"] = graphql_data.stargazers.totalCount
        library_metadata["watchers"] = graphql_data.watchers.totalCount
        library_metadata["forks"] = graphql_data.forks.totalCount
        library_metadata["open_issues"] = graphql_data.issues.totalCount
        library_metadata["last_commit"] = graphql_data.defaultBranchRef.target.history.edges[0].node.authoredDate if graphql_data.defaultBranchRef.target.history.edges else None
        library_metadata["latest_version"] = graphql_data.releases.nodes[0].name if graphql_data.releases.nodes else None
        library_metadata["latest_tag"] = graphql_data.releases.nodes[0].tagName if graphql_data.releases.nodes else None
        library_metadata["licenseSpdxId"] = graphql_data.licenseInfo.spdxId if graphql_data.licenseInfo else None
        library_metadata["licenseUrl"] = graphql_data.licenseInfo.url if graphql_data.licenseInfo else None

        library.update(library_metadata)

    return libraries
