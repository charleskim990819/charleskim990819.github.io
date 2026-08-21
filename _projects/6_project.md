---
layout: page
title: Multimodal Bioelectronics
description: A design concept — one wearable front end for electrochemistry, EMG and stimulation
img: assets/img/proj_multimodal.png
importance: 2
category: interests
related_publications: false
---

<div class="ll-role is-interest">
<div class="ll-role-k">Status</div>
<div><p>A design concept. Nothing here has been fabricated or measured &mdash; the chip selection below is a paper exercise in what a combined front end would have to contain, not a description of a board that exists.</p></div>
</div>

## The idea

Wearable studies usually measure one thing. A sweat sensor measures chemistry, an EMG band measures muscle activity, a stimulator delivers current — each with its own electrodes, its own enclosure, its own clock. When results from different modalities are compared afterwards, a good part of the disagreement is just that the measurements were never made on the same patch of skin at the same moment.

A single front end that runs all three on a shared electrode fabric would remove that ambiguity. That is the thing I find interesting about it.

## What such a front end would need

| Function | Candidate part | Why |
|---|---|---|
| Electrochemistry (CV / CA / EIS / OCP) | AD5941 | The part I already know from the toolkit build |
| EMG / EEG (24-bit, 8-ch) | ADS131M08 | Simultaneous sampling matters when channels are compared |
| Stimulation (16-ch) | Intan RHS2116 | Programmable biphasic current |
| MCU + BLE | DA14531 / nRF52 class | Chosen against power and footprint budget |

## The parts I do not know yet

Listing chips is the easy half. The questions that would decide whether this is worth building:

- **Crosstalk.** A stimulator putting current into tissue and a potentiostat holding a working electrode at a few hundred millivolts are not obviously compatible on a shared substrate. What isolation is actually needed?
- **Grounding.** Three subsystems with different reference conventions sharing one liquid-metal interconnect fabric — where does the return current go?
- **Whether it earns its complexity.** Three separate devices already work. A combined one has to answer a question that separate ones cannot.

I have not resolved any of these. Until I have, this stays a concept.
