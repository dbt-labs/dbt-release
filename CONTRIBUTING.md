# Contributing to `dbt-release`

`dbt-release` is a set of GitHub [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows) for automating releasing `dbt-core` and adapter plugins.


1. [About this document](#about-this-document)
2. [Getting the code](#getting-the-code)
3. [Setting up an environment](#setting-up-an-environment)
4. [Running in development](#running-dbt-release-in-development)
5. [Testing](#testing)
6. [Debugging](#debugging)
7. [Adding or modifying a changelog entry](#adding-or-modifying-a-changelog-entry)
8. [Submitting a Pull Request](#submitting-a-pull-request)
9. [Troubleshooting Tips](#troubleshooting-tips)

## About this document

There are many ways to contribute to the ongoing development of `dbt-release`, such as by participating in discussions and issues. We encourage you to first read our higher-level document: ["Expectations for Open Source Contributors"](https://docs.getdbt.com/docs/contributing/oss-expectations).

The rest of this document serves as a more granular guide for contributing code changes to `dbt-release` (this repository). It is not intended as a guide for using `dbt-release`, and some pieces assume a level of familiarity with GitHub workflow development. Specific code snippets in this guide assume you are using macOS or Linux and are comfortable with the command line.

### Notes

- **CLA:** Please note that anyone contributing code to `dbt-release` must sign the [Contributor License Agreement](https://docs.getdbt.com/docs/contributor-license-agreements). If you are unable to sign the CLA, the `dbt-release` maintainers will unfortunately be unable to merge any of your Pull Requests. We welcome you to participate in discussions, open issues, and comment on existing ones.
- **Branches:** All pull requests from community contributors should target the `main` branch (default).
- **Releases**: This repository is never released.

## Getting the code

### Installing git

You will need `git` in order to download and modify the source code.

### External contributors

If you are not a member of the `dbt-labs` GitHub organization, you can contribute to `dbt-release` by forking the `dbt-release` repository. For a detailed overview on forking, check out the [GitHub docs on forking](https://help.github.com/en/articles/fork-a-repo). In short, you will need to:

1. Fork the `dbt-release` repository
2. Clone your fork locally
3. Check out a new branch for your proposed changes
4. Push changes to your fork
5. Open a pull request against `dbt-labs/dbt-release` from your forked repository

### dbt Labs contributors

If you are a member of the `dbt-labs` GitHub organization, you will have push access to the `dbt-release` repo. Rather than forking `dbt-release` to make your changes, just clone the repository, check out a new branch, and push directly to that branch.

## Setting up an environment

There are some tools that will be helpful to you in developing locally. While this is the list relevant for `dbt-release` development, many of these tools are used commonly across open-source python projects.

### Tools

These are the tools used in `dbt-release` development and testing:

- [`flake8`](https://flake8.pycqa.org/en/latest/) for code linting
- [`black`](https://github.com/psf/black) for code formatting
- [`pre-commit`](https://pre-commit.com) to easily run those checks

A deep understanding of these tools in not required to effectively contribute to `dbt-release`, but we recommend checking out the attached documentation if you're interested in learning more about each one.

## Running `dbt-release` in development

- Install pre-commit ([docs](https://pre-commit.com/#installation))
- Use the following [guidelines](https://github.com/dbt-labs/dbt-core/blob/main/.github/_README.md) during development
- Each workflow should be self-documented


### Running `dbt-release`

Workflows in this repository are all triggered with a `workflow_call` so to test your changes you will need to set up a workflow in another repository to trigger your the modified workflow on your branch or fork.  [release.yml](https://github.com/dbt-labs/dbt-core/blob/main/.github/workflows/release.yml) is what we use to trigger all the workflows in this repository and is a good example of how to trigger them.


## Testing

There are no automated tests for this repository.

Workflows can be triggered with a `test_run`` flag set to `true``.  This publishes releases as Drafts in Github and also pushes release to pypi-test instead of production.

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

## Debugging

You can enable debug logging for GHA by setting secret values for your repository. See [docs](https://docs.github.com/en/github-ae@latest/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging) for more info.

- Set `ACTIONS_RUNNER_DEBUG` to `true` to enable runner diagnostic logging.
- Set `ACTIONS_STEP_DEBUG` to `true` to enable run step debug logging.

### Assorted development tips
* Sometimes flake8 complains about lines that are actually fine, in which case you can put a comment on the line such as: # noqa or # noqa: ANNN, where ANNN is the error code that flake8 issues.

## Submitting a Pull Request

Code can be merged into the current development branch `main` by opening a pull request. A `dbt-release` maintainer will review your PR. They may suggest code revision for style or clarity, or request that you add unit or integration test(s). These are good things! We believe that, with a little bit of help, anyone can contribute high-quality code.

Automated tests run via GitHub Actions. If you're a first-time contributor, all tests (including code checks and unit tests) will require a maintainer to approve. Changes in the `dbt-release` repository trigger integration tests against Postgres. dbt Labs also provides CI environments in which to test changes to other adapters, triggered by PRs in those adapters' repositories, as well as periodic maintenance checks of each adapter in concert with the latest `dbt-release` code changes.

Once all tests are passing and your PR has been approved, a `dbt-release` maintainer will merge your changes into the active development branch. And that's it! Happy developing :tada:

## Troubleshooting Tips
- Sometimes, the content license agreement auto-check bot doesn't find a user's entry in its roster. If you need to force a rerun, add `@cla-bot check` in a comment on the pull request.
