- [General Info](#general-info)
  - [Workflows](#workflows)
  - [Version Bump and Changelog Generation](#version-bump-and-changelog-generation)
    - [Inputs](#inputs)
    - [Outputs](#outputs)
    - [Branching strategy](#branching-strategy)
      - [Naming strategy](#naming-strategy)
  - [Build](#build)
    - [Inputs](#inputs-1)
    - [Build artifact](#build-artifact)
  - [GitHub Release](#github-release)
    - [Inputs](#inputs-2)
    - [Outputs](#outputs-1)
  - [PyPI Release](#pypi-release)
    - [Inputs](#inputs-3)
  - [Post Slack Notification](#post-slack-notification)
    - [Inputs](#inputs-4)

# General Info  

This page contains general info about reusable workflows;

## Workflows

- [Version Bump and Changelog Generation](.github/workflows/release-prep.yml)
- [Build](.github/workflows/build.yml)
- [GitHub Release](.github/workflows/github-release.yml)
- [PyPI Release](.github/workflows/pypi-release.yml)
- [Post Slack Notification](.github/workflows/slack-post-notification.yml)

## Version Bump and Changelog Generation

Perform the version bump, generate the changelog and run tests.

### Inputs

| name                    | description                                                |
| ----------------------- | ---------------------------------------------------------- |
| `sha`                   | The commit to attach to this release                       |
| `version_number`        | The release version number (i.e. 1.0.0b1, 1.2.3rc2, 1.0.0) |
| `target_branch`         | The branch that we will release from                       |
| `env_setup_script_path` | Path to the environment setup script                       |
| `test_run`              | Test run (The temp branch will be used for release)        |
| `nightly_release`       | Identifier that this is nightly release                    |

### Outputs

| name             | description                                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| `final_sha`      | The sha that will actually be released.  This can differ from the input sha if adding a version bump and/or changelog |
| `changelog_path` | Path to the changelog file (ex .changes/1.2.3-rc1.md)                                                                 |

### Branching strategy

- During execution workflow execution the temp branch will be generated;
- For normal runs the temp branch will be removed once changes were merged to target branch;
- For test runs we will keep temp branch and will use it for release;

#### Naming strategy

| case                 | example                                                                    |
| -------------------- | -------------------------------------------------------------------------- |
| For normal runs      | `prep-release/${{ inputs.version_number }}_$GITHUB_RUN_ID`                 |
| For test runs        | `prep-release/test-run/${{ inputs.version_number }}_$GITHUB_RUN_ID`        |
| For nightly releases | `prep-release/nightly-release/${{ inputs.version_number }}_$GITHUB_RUN_ID` |

## Build

Build release artifacts and store them to S3 bucket if they do not already exist.

### Inputs

Inputs:
| name                   | description                                                |
| ---------------------- | ---------------------------------------------------------- |
| `sha`                  | The commit to attach to this release                       |
| `version_number`       | The release version number (i.e. 1.0.0b1, 1.2.3rc2, 1.0.0) |
| `changelog_path`       | Path to the changelog file for release notes               |
| `build_script_path`    | Path to the build script                                   |
| `s3_bucket_name`       | AWS S3 bucket name                                         |
| `package_test_command` | Command to use to check package runs                       |
| `test_run`             | Test run (Bucket to upload the artifact)                   |
| `nightly_release`      | Identifier that this is nightly release                    |

### Build artifact

Expected build artifact layout:

```console
├── dist
│   ├── dbt-*.tar.gz
│   ├── dbt-*.whl
└── <release_notes>.md
```

Build artifacts get stored in S3 in a bucket with the following directory structure:

```console
"s3://<s3_bucket>/<org>/<repo>/<artifact_folder>/<version>/<commit>/"
```

`<artifact_folder>` - resolves based on `test_run` and `nightly_release` inputs:

- `nightly_release == true` will use "nightly-releases"
- `nightly_release == false` resolves based on `test_run` input
- `test_run == true`  will use "artifacts_testing"
- `test_run == false` will use "artifacts"

**Examples**:
| case                      | outcome                                                                                                                            |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `nightly_release == true` | `s3://core-team-artifacts/dbt-labs/dbt-core/nightly-releases/1.4.0a1.dev01112023+nightly/aaa410f17d300f1bde2cd67c03e48df135ab347b` |
| `test_run == true`        | `s3://core-team-artifacts/dbt-labs/dbt-core/artifacts_testing/1.2.3/ce98e6f067d9fa63a9b213bf99ebaf0c29d2b7eb/`                     |
| `test_run == false`       | `s3://core-team-artifacts/dbt-labs/dbt-core/artifacts/1.2.3/ce98e6f067d9fa63a9b213bf99ebaf0c29d2b7eb/`                             |

## GitHub Release

Create a new release on GitHub and include any artifacts in the `/dist` directory of the GitHub artifacts store.

### Inputs

| name             | description                                                |
| ---------------- | ---------------------------------------------------------- |
| `sha`            | The commit to attach to this release                       |
| `version_number` | The release version number (i.e. 1.0.0b1, 1.2.3rc2, 1.0.0) |
| `changelog_path` | Path to the changelog file for release notes               |
| `test_run`       | Test run (Publish release as draft)                        |

### Outputs

| name  | description                                |
| ----- | ------------------------------------------ |
| `tag` | The path to the changelog for this version |

## PyPI Release

After releasing to GitHub, release to PyPI

### Inputs

| name           | description                                                     |
| -------------- | --------------------------------------------------------------- |
| version_number | The release version number (i.e. 1.0.0b1, 1.2.3rc2, 1.0.0)      |
| test_run       | Test run (true - release to Test PyPI, false - release to PyPI) |

## Post Slack Notification

Post notification to Slack channel

### Inputs

| name                 | description                                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| `status`             | Workflow status (Expected values: success, failure, cancelled, warnings, skipped)                             |
| `notify_when`        | Specify on which status a slack notification is sent (By default: notification will be sent for all statuses) |
| `notification_title` | Specify on the notification message title (By default: Release Process Status)                                |
