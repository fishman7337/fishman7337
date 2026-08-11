# Security Policy

This profile repository publishes generated portfolio assets and supporting
scripts; it is not a production service. The main risks are accidental
credential exposure, unsafe generated content, and unreviewed dependencies.

## Supported Versions

Security fixes apply to the current default branch.

## Reporting

Report concerns privately to the repository maintainer where possible. Include
the affected file, a short impact description, and steps to reproduce. Do not
open a public issue containing secrets, personal data, or an exploit.

## Handling Secrets

- Keep tokens and local values outside the repository.
- Never commit API keys, cloud credentials, session cookies, or private data.
- Rotate any secret that was committed or exposed in generated output.

## Generated-asset safety

Review generator inputs, outbound links, and resulting SVG/HTML content before
publication. Dependency and workflow updates must pass the repository quality
gate before merge.
