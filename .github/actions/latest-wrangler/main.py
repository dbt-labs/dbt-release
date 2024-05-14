import os
import sys
from typing import List, Optional

from packaging.version import Version, parse
import requests


def main():
    package_name: str = os.environ["INPUT_PACKAGE_NAME"]
    new_version: Version = parse(os.environ["INPUT_NEW_VERSION"])
    github_token: str = os.environ["INPUT_GITHUB_TOKEN"]

    response = _package_metadata(package_name, github_token)
    published_versions = _published_versions(response)
    new_version_tags = _new_version_tags(new_version, published_versions)
    _register_tags(new_version_tags, package_name)


def _package_metadata(package_name: str, github_token: str) -> requests.Response:
    url = f"https://api.github.com/orgs/dbt-labs/packages/container/{package_name}/versions"
    return requests.get(url, auth=("", github_token))


def _published_versions(response: requests.Response) -> List[Optional[Version]]:
    package_metadata = response.json()
    return [
        parse(tag)
        for version in package_metadata
        for tag in version["metadata"]["container"]["tags"]
        if "latest" not in tag
    ]


def _new_version_tags(new_version: Version, published_versions: List[Optional[Version]]) -> List[str]:
    latest = "latest"
    latest_minor = f"{new_version.major}.{new_version.minor}.latest"
    pinned = str(new_version)

    published_patches = [
        patch
        for patch in published_versions
        if patch.major == new_version.major and patch.minor == new_version.minor
    ]

    # pre-releases don't get tagged with `latest` tags
    if new_version.is_prerelease:
        tags = [pinned]

    # first releases are automatically the latest
    elif not published_versions:
        tags = [pinned, latest_minor, latest]

    # the overall latest release is also the latest minor release
    elif new_version > max(published_versions):
        tags = [pinned, latest_minor, latest]

    # first minor releases are automatically the latest minor release
    elif not published_patches:
        tags = [pinned, latest_minor]

    # this is a patch release that was released chronologically
    elif new_version > max(published_patches):
        tags = [pinned, latest_minor]

    # this is a patch release that was released off-cycle
    else:
        tags = [pinned]

    return tags


def _register_tags(tags: List[str], package_name: str) -> None:
    fully_qualified_tags = ",".join([f"ghcr.io/dbt-labs/{package_name}:{tag}" for tag in tags])
    github_output = os.environ.get("GITHUB_OUTPUT")
    with open(github_output, "at", encoding="utf-8") as gh_output:
        gh_output.write(f"fully_qualified_tags={fully_qualified_tags}")


def _validate_response(response: requests.Response) -> None:
    message = response["message"]
    if response.status_code != 200:
        print(f"Call to GitHub API failed: {response.status_code} - {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
