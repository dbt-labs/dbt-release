import json
import os
from typing import Union, Dict
from urllib.request import urlopen, Request

from .common import ReleaseFile, EnvironmentInformation


def make_post(release: ReleaseFile):
    GITHUB_API_TOKEN = os.getenv("DBT_GITHUB_API_TOKEN")
    data: Dict[str, Union[str, bool]] = {
        "tag_name": f"v{release.version}",
        "target_commitish": release.branch,
        "name": f"dbt {release.version}",
        "body": release.notes,
    }
    if release.is_prerelease:
        data["prerelease"] = True
    request = Request(
        url="https://api.github.com/repos/dbt-labs/dbt-core/releases",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"token {GITHUB_API_TOKEN}",
        },
        data=json.dumps(data).encode("utf-8"),
    )
    print(f"Creating release with data:\n{data}")
    try:
        with urlopen(request) as fp:
            resp_data = fp.read()
    except Exception as exc:
        raise ValueError(f"Could not create release {release.version}: {exc}") from exc
    print(f"Github response:\n{resp_data}")


def make_github_release(args=None):
    env = EnvironmentInformation()
    release = ReleaseFile.from_artifacts(env)
    make_post(release)


def add_github_parsers(subparsers):
    github_sub = subparsers.add_parser("github", help="Create the github release")
    github_subs = github_sub.add_subparsers(title="Available sub-commands")
    create_release = github_subs.add_parser("create-release")
    create_release.set_defaults(func=make_github_release)
