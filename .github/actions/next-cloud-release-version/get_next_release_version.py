import argparse
import re

from semantic_version import Version
from typing import List


def increment_latest_version(released_versions: List[str], target_version: str) -> Version:
    """Retrieve the latest version matching the major.minor and release stage
       semantic version if it exists. Ignores the patch version.

    Args:
        released_versions (List[str]): List of semantic versions (1.0.0.0rc, 2.3.5) to match against
        target_version (str): semantic version (1.0.0.0rc, 2.3.5) to match against

    Returns:
        Version: The latest version.
    """
    target_version = Version.coerce(target_version)
    latest_version = target_version
    latest_version.prerelease = ("post0",)

    # Function to extract the numeric part from prerelease tags, even malformed ones
    # like 'post01' or 'post2' if they end up in the archive
    def get_post_number(version: Version) -> int:
        prerelease = version.prerelease[0]
        match = re.match(r'(\D*)(\d+)', prerelease)  # Capture any non-digit prefix and the numeric part
        return int(match.group(2)) if match else 0

    for version in released_versions:
        version = Version.coerce(version)

        # semantic_version does not handle build metadata, so we need to move it to the prerelease field
        if not version.prerelease and version.build:
            version.prerelease = version.build
            version.build = []
        if (
                version.major == latest_version.major
                and version.minor == latest_version.minor
                and version.patch == latest_version.patch
                and get_post_number(version) > get_post_number(latest_version)
        ):
            latest_version = version

    next_pre = re.sub(r"\d+", lambda x: str(int(x.group()) + 1), latest_version.prerelease[0])
    latest_version.prerelease = (next_pre,)
    latest_version.build = []

    return latest_version


def main():
    parser = argparse.ArgumentParser(description="Get the next release version")
    parser.add_argument("--released_versions", type=str, help="comma delimited list of released versions")
    parser.add_argument("--target_version", help="Target version to compare against")
    args = parser.parse_args()
    released_versions = list(filter(None, args.released_versions.split(","))) if args.released_versions else []
    target_version = args.target_version
    latest_version = increment_latest_version(released_versions, target_version)
    print(f"{latest_version.major}.{latest_version.minor}.{latest_version.patch}{latest_version.prerelease[0]}")


if __name__ == "__main__":
    main()
