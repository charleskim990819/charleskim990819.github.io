---
layout: page
title: Wearable BCI
description: Non-invasive ear-EEG brain-computer interface with PDA-LM microneedle contacts
img: assets/img/proj_wearable_bci.png
importance: 3
category: research
related_publications: false
---

## Goal

A **non-invasive, ear-mounted EEG platform** (cEEGrid form factor) using PDA-LM microneedle contacts to lower skin-electrode impedance without piercing the stratum corneum mechanically. Targets motor-imagery, SSVEP, and auditory paradigms.

## Architecture

- **Analog front-end:** ADS131M08 (24-bit, 8-ch simultaneous-sampling ΔΣ ADC)
- **MCU:** Apollo510 (Cortex-M55 with embedded ML acceleration)
- **Comparison baseline:** BioAmp EXG Pill (open hardware), Yonsei in-house cEEGrid

## Why PDA-LM contacts?

Conventional Ag/AgCl gel electrodes dry out within hours. Dry electrodes have high impedance and motion artifacts. PDA-LM offers a middle path: **soft, conformal liquid metal** with PDA's catechol chemistry providing wet-like coupling to skin without gel maintenance.

## Status

Hardware development ongoing; migrating from dev-kit prototype to a custom sPCB co-designed with the AD5941 EC channels.
