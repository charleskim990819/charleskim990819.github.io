---
layout: page
title: STK RevM20 sensor front end
description: Simultaneous electrochemical sensing on a compact four-layer flex PCB
permalink: /projects/stk-revm20/
img: assets/projects/stk-revm20/architecture.svg
importance: 0
category: engineering
related_publications: false
---

**Prototype · 3 current channels + pH · 4-layer FPC · 41.8 × 42.5 mm**

## Key design decisions

- **Acquisition and coupling.** Continuous TIAs and simultaneous ADC sampling preserve channel timing. Shared RE/CE saves connections, with electrical and chemical crosstalk left for measurement.
- **Precision and sourcing.** The ADG704 substitution was checked for pin/control compatibility. Leakage, on-resistance, resistor tolerance and reference errors drive the per-range calibration plan.
- **Layout and assembly.** GND/power continuity, high-impedance inputs and USB routing were reviewed. Double-sided FPC assembly requires fixture, reflow and USB mechanical-support review.

<img src="/assets/projects/stk-revm20/architecture.svg" alt="STK RevM20: continuous TIAs and pH buffer, simultaneous ADC, DAC setpoints and ESP32-S3 USB acquisition" class="img-fluid rounded">

## Verification and next step

**CAD evidence:** 0 DRC/ERC violations and 0 unconnected items under the configured checks; BOM/placement matching for 196 fitted parts. [Audit scope and exclusions](https://github.com/charleskim990819/charleskim990819.github.io/tree/main/docs/projects/stk-revm20/evidence).

**Next:** factory review → USB-only bring-up → dummy-cell accuracy, noise and crosstalk tests. Reset/startup and selected-channel EIS still need physical validation. No measured accuracy is claimed.

[Requirements](https://github.com/charleskim990819/charleskim990819.github.io/tree/main/docs/projects/stk-revm20/requirements.md) · [Error budget](https://github.com/charleskim990819/charleskim990819.github.io/tree/main/docs/projects/stk-revm20/error-budget.md) · [Validation plan](https://github.com/charleskim990819/charleskim990819.github.io/tree/main/docs/projects/stk-revm20/validation.md) · [한국어](https://github.com/charleskim990819/charleskim990819.github.io/tree/main/docs/projects/stk-revm20/README.ko.md)

<small>RevM20 / FW18 · Design baseline: 15 October 2026 · <a href="/projects/5_project/">Earlier AD5941 toolkit</a></small>
