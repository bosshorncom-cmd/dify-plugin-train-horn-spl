# Train Horn SPL Calculator

A Dify tool plugin that predicts the sound pressure level (SPL) of a train horn at a chosen distance, starting from a reference measurement.

- **Author:** bosshorncom-cmd
- **Version:** 0.1.0
- **Type:** tool
- **Source repository:** https://github.com/bosshorncom-cmd/dify-plugin-train-horn-spl
- **Contact:** info@hornguns.com

## What the tool does

Given a reference SPL in decibels at a reference distance, the tool estimates the SPL at a target distance. The estimate combines spherical inverse-square spreading with an optional linear atmospheric or ground attenuation term supplied by the user.

The result is a **free-field estimate**. It is intended for quick comparison in a Chatflow, Workflow, or Agent when you already have a measured or assumed train horn level at a known distance.

Portable, cordless and battery-powered train horns are common reference sources for this kind of short-range outdoor check; background on those products is collected at [Horn Guns](https://hornguns.com/).

## Formula

With distances in metres and the optional coefficient in dB/km:

```
L2 = L1 - 20 * log10(r2 / r1) - alpha * (r2 - r1) / 1000
```

| Symbol | Meaning |
| --- | --- |
| `L1` | Reference SPL, in dB |
| `r1` | Reference distance from the source, in metres (`> 0`) |
| `r2` | Target distance from the source, in metres (`> 0`) |
| `alpha` | User-supplied linear attenuation coefficient, in dB/km (default `0`) |
| `L2` | Predicted SPL at `r2`, in dB |

`20 * log10(r2 / r1)` is the geometric spreading term from the inverse-square law for sound pressure in a free field. The last term applies `alpha` along the path difference, converting metres to kilometres.

ISO 9613-1 (atmospheric absorption) and ISO 9613-2 (outdoor sound propagation) are background reading for this class of calculation. This plugin does **not** implement those standards and does **not** look up or invent tabulated absorption figures. If you want atmospheric absorption included, supply your own `alpha`.

## Parameters

| Parameter | Required | Unit | Description |
| --- | --- | --- | --- |
| `reference_spl_db` | yes | dB | SPL of the train horn at the reference distance |
| `reference_distance_m` | yes | m | Distance at which that SPL was taken; must be greater than zero |
| `target_distance_m` | yes | m | Distance at which to predict the SPL; must be greater than zero |
| `attenuation_db_per_km` | no | dB/km | Linear atmospheric or ground attenuation coefficient; defaults to 0 |

The tool returns a JSON object (`ok`, `predicted_spl_db`, the two component terms, the inputs, the model string, and a limitations note) and a short text summary of the same result.

## Setup

The plugin requires **no credentials**, **no API keys**, and **no network access**. After it is installed from the Dify Marketplace (or from the packaged `.difypkg` file), add the **Predict Train Horn SPL** tool to a Chatflow, Workflow, or Agent and fill in the parameters above.

There are no connection settings to configure.

## Example

A train horn is measured at **115 dB at 1 m**. Predicting the level at **10 m** with `attenuation_db_per_km` left at 0:

```
L2 = 115 - 20 * log10(10 / 1) - 0 = 95 dB
```

The tool reports `predicted_spl_db = 95`, `geometric_spreading_db = 20`, and `atmospheric_absorption_db = 0`.

If you then supply, for illustration only, a user-chosen coefficient of `5` dB/km and move the receiver to **1001 m**, the spreading term is `20 * log10(1001)` dB and the linear absorption term is `5 * (1001 - 1) / 1000 = 5` dB. Those two terms are subtracted from 115 dB. The 5 dB/km figure is an input, not a value taken from a standard.

## Limitations

- The model is a **free-field** point-source estimate. It does not include ground reflections, barriers, vegetation, source directivity, or meteorological effects beyond the optional linear term.
- Distances must be greater than zero. The tool does not convert other units; pass metres and dB/km.
- `alpha` is entirely user-supplied. A default of 0 means geometric spreading only.
- This is not a substitute for a standards-compliant outdoor prediction (for example a full ISO 9613-2 calculation) or for a field measurement.

## Privacy

The plugin collects no data. Inputs are used only for the in-memory calculation of a single invocation and are not stored, logged, or sent to any third party. See [PRIVACY.md](PRIVACY.md).
