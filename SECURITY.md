# Security policy

## Reporting a vulnerability

Please do not open a public issue for a vulnerability that could expose credentials, private memory records, or bypass an approval boundary.

Use GitHub's private vulnerability reporting for this repository. Include the affected file or schema, a minimal reproduction, the expected boundary, the observed behavior, and any known mitigation.

## Supported versions

Until v1, only the latest tagged release is supported.

## Scope

Security-relevant areas include:

- authority or approval bypasses;
- unsafe path handling or destructive initialization;
- memory privacy or provenance failures;
- schema ambiguity that changes effect classification;
- examples or fixtures that contain real secrets or personal data.

The project does not execute models or store credentials. Harness adapters must keep raw secrets outside model-visible project state.
