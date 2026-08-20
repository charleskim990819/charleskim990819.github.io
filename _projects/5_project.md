---
layout: page
title: AD5941 EC Sensor Toolkit
description: Portable 4-channel electrochemical sensor based on AD5941 + ESP32-C6
img: assets/img/proj_ec_toolkit.png
importance: 1
category: engineering
related_publications: false
---

## What

A **palm-sized, BLE-enabled, 4-channel electrochemical sensor toolkit (STK)** built around the Analog Devices **AD5941** analog front-end and the **ESP32-C6** MCU. Supports cyclic voltammetry (CV), chronoamperometry (CA), electrochemical impedance spectroscopy (EIS), and open-circuit potentiometry (OCP).

## Hardware highlights

- **AD5941** analog front-end with internal TIA, DAC, and 16-bit ADC
- **ESP32-C6** for BLE + Wi-Fi telemetry
- **External LTC6078 bypass** to AIN3 — a workaround for the AD5941 internal LPTIA latch-up failure mode observed after ~30 s of sustained current (software mitigation alone is insufficient)
- Custom KiCad layout, optimized BOM, and reduced-footprint stretchable PCB variant in development

## Firmware status

| Mode | Status |
|---|---|
| Cyclic voltammetry | Phase 1 complete (clean duck-shape on standard ferrocyanide, dEp limited by carbon electrode) |
| Amperometry | In progress (current focus, May 2026) |
| OCP / ISE (Na⁺) | Next milestone |
| EIS | Validated against benchtop potentiostat |

## DIY screen-printed electrodes

A parallel track produces in-house SPEs from SEBS substrates with Dycotec DM-CAP-2100S carbon ink — a low-cost alternative to commercial DRP-110 chips, with the same standard 3-electrode geometry (WE / RE / CE).
