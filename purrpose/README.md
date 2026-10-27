# Purrpose application

Run commands from the repository root, not from this package directory.

- [Product and features](../README.md)
- [Dependencies and connection setup](../docs/SETUP.md)
- [Architecture and actual tool roles](../docs/ARCHITECTURE.md)
- [Demo walkthrough](../docs/DEMO.md)
- [Validation and known limits](../docs/VALIDATION.md)

`python -m purrpose.server --port 8767` starts a local no-model/no-cloud-config interface. To reproduce the integrated demo, configure H-MEM, remote Zetaris JDBC and optional NVIDIA as described in Setup. Do not infer live integration from the interface loading successfully.
