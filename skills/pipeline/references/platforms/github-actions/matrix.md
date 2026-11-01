# GitHub Actions: Matrix Strategies
## Basic Matrix
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
    os: [ubuntu-latest, macos-latest]
  fail-fast: true
  max-parallel: 4
```
## Dynamic Matrix
Generate matrix at runtime:
```yaml
jobs:
  generate:
    outputs:
      matrix: ${{ steps.set.outputs.matrix }}
    steps:
      - id: set
        run: echo "matrix=$(cat matrix.json)" >> $GITHUB_OUTPUT
  test:
    needs: generate
    strategy:
      matrix: ${{ fromJson(needs.generate.outputs.matrix) }}
```
## Include/Exclude
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    include:
      - os: ubuntu-latest
        extra-flag: --fast
    exclude:
      - os: windows-latest
```
## Test Sharding

This POSIX-runner example assumes Playwright is already a reviewed project
dev dependency pinned in the committed lockfile, and that the project's reviewed
lockfile installation step has completed before this test step. Run the local
project binary so a missing dependency fails instead of fetching a replacement.
For another runner shell, use the project's reviewed, platform-appropriate local
test script. See [npm exec's package-resolution behavior](https://docs.npmjs.com/cli/v11/commands/npm-exec/).

```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: ./node_modules/.bin/playwright test --shard=${{ matrix.shard }}/4
```
