# Development

## Setup

```bash
git clone https://github.com/craigtrim/gngram-lookup.git
cd gngram-lookup
make install
```

## Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make test` | Run tests |
| `make lint` | Run linter |
| `make build-hash` | Build hash files from source parquet |
| `make package-release` | Create parquet-hash.tar.gz |
| `make release VERSION=v1.1.0` | Create GitHub release |

## Building Data

To rebuild the hash-bucketed parquet files from source:

```bash
make build-hash
```

This processes the raw ngram data and creates the 256 bucket files.

## Creating a Release

```bash
make package-release
make release VERSION=v1.2.0
```

This creates a tarball and uploads it as a GitHub release asset.
