# Privacy Policy — Train Horn SPL Calculator

This plugin predicts a train horn sound pressure level from numeric inputs you provide in Dify. It performs no network requests, no file operations, and no external calls of any kind.

## Data collected

**None.** This plugin collects, stores, logs, or transmits no user data.

## What happens to your data

Everything runs inside your Dify runtime as a pure numerical calculation:

- The reference SPL, distances, and optional attenuation coefficient are processed in memory for the duration of a single tool invocation.
- The plugin sends no data to any external service, because it makes no network requests.
- The plugin does not persist anything to disk, a database, or any storage backend. Storage permission is not enabled in `manifest.yaml`.

## Third-party processing

None. The plugin does not transmit data to any third party. It has no API endpoints, no credentials, no telemetry, and no runtime dependencies beyond the Dify plugin SDK.

## Credential handling

The plugin requires **no credentials**. The provider's `_validate_credentials` method is a no-op, and no secret-input fields are declared.

## Contact

For privacy questions about this plugin, email info@hornguns.com or open an issue at https://github.com/bosshorncom-cmd/dify-plugin-train-horn-spl.
