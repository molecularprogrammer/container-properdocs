# ProperDocs Container

ProperDocs can render markdown into a publishable documentation static site.

This container contains ProperDocs, MaterialX, and useful extensions.

See the following for more details:

- [Official ProperDocs documentation](https://properdocs.org/)
- [Official MaterialX theme documentation](https://github.com/jaywhj/mkdocs-materialx)

## Build

Run `build.sh` to build locally.

## Publish

Push changes to the `main` branch. The CI pipeline will handle publishing to the container registry.

## Example

The `example` demonstrates the use of some configurations and extensions. Use `./example/build.sh`
to generate the static site. The output will be in `example/site`.
