# GitHub Workflows for releasing dbt packages

A set of GitHub [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows) for automating releasing `dbt-core` and database adapter plugins.

## Workflows

- [Version Bump and Changelog Generation](.github/workflows/release-prep.yml)
- [Build](.github/workflows/build.yml)
- [GitHub Release](.github/workflows/github-release.yml)
- [PyPI Release](.github/workflows/pypi-release.yml)
- [Post Slack Notification](.github/workflows/slack-post-notification.yml)

## References to workflows

To use workflows inside other workflows, you can use the `main` branch or specific commit SHA as a workflow tag.

**Snippet**:

```yaml
  build-test-package:
    name: Build, Test, Package
    if: ${{ !failure() && !cancelled() }}
    needs: [bump-version-generate-changelog]

    uses: dbt-labs/dbt-release/.github/workflows/build.yml@main

    with:
      sha: ${{ needs.bump-version-generate-changelog.outputs.final_sha }}
      version_number: ${{ inputs.version_number }}
      changelog_path: ${{ needs.bump-version-generate-changelog.outputs.changelog_path }}
      build_script_path: ${{ inputs.build_script_path }}
      s3_bucket_name: ${{ inputs.s3_bucket_name }}
      package_test_command: ${{ inputs.package_test_command }}
      test_run: ${{ inputs.test_run }}
      nightly_release: ${{ inputs.nightly_release }}

    secrets:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**Example**: <https://github.com/dbt-labs/dbt-core/blob/main/.github/workflows/release.yml>

## Development

- Install pre-commit ([docs](https://pre-commit.com/#installation));
- Use the following [guidelines](https://github.com/dbt-labs/dbt-core/blob/main/.github/_README.md) during development;
- Each workflow should be self-documented;
- It is recommended to use the [act](https://github.com/nektos/act) for testing locally where possible.
