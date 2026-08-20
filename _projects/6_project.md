---
layout: page
title: Multimodal Bioelectronics
description: Combined EC + EMG + neurostim front-end roadmap
img: assets/img/proj_multimodal.png
importance: 2
category: engineering
related_publications: false
---

## Vision

A **single wearable platform that fuses electrochemical sensing, electromyography, and programmable neurostimulation** — using a shared MCU, shared BLE link, and a shared liquid-metal interconnect fabric.

## Building blocks

| Function | Chip | Notes |
|---|---|---|
| Electrochemistry (CV / CA / EIS / OCP) | AD5941 | LPTIA bypass via LTC6078 |
| EEG / EMG (24-bit, 8-ch) | ADS131M08 | Simultaneous-sampling ΔΣ ADC |
| Neurostimulation (16-ch) | Intan RHS2116 | Programmable biphasic current pulses |
| Iontophoresis | Custom current source | For transdermal delivery experiments |
| MCU + BLE | Apollo510 / DA14531 / nRF52832 | Selected per power / footprint budget |

## Form-factor strategy

Phase-staged miniaturization from a 5×5 cm dev-kit PCB through FPCB-on-PI to a final **3×3 cm wearable tattoo sticker** with PDA-LM interconnects replacing connectors and antenna routing wherever possible.

## Reference inspirations

Wei Gao, Ali Javey, and Dae-Hyeong Kim groups' integrated wearable platforms — adapted to LM-printed substrates rather than rigid-flex assemblies.
