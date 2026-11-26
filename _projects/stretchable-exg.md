---
layout: page
title: Stretchable EMG circuit
description: A stretchable electrode readout design and an EMG-controlled RC car demonstration.
permalink: /projects/stretchable-exg/
importance: 2
category: engineering
_styles: |
  footer.fixed-bottom { position: static; }
  body { padding-bottom: 0; }
  #rc-car-demo { scroll-margin-top: 5rem; }
  .rc-car-player {
    display: block;
    width: auto;
    height: auto;
    max-width: min(100%, 360px);
    max-height: 62vh;
    max-height: 62svh;
    margin-bottom: 1rem;
  }
---

I adapted the [BioAmp EXG Pill](https://github.com/upsidedownlabs/BioAmp-EXG-Pill) circuit for a stretchable substrate. After testing the original rigid board, I redrew the layout in AutoCAD, printed liquid-metal traces, and mounted the components on the new board.

## Controlling an RC car with muscle signals {#rc-car-demo}

The electrodes on the forearm record muscle activity as the hand closes. In this demonstration, that signal controls the RC car beside it.

<video aria-label="Forearm electrodes recording a hand contraction to control an RC car" class="rc-car-player rounded" width="360" height="640" controls playsinline preload="metadata" poster="{{ '/assets/projects/stretchable-exg/emg-rc-car-poster.jpg' | relative_url }}">
  <source src="{{ '/assets/projects/stretchable-exg/emg-rc-car.mp4' | relative_url }}" type="video/mp4">
</video>

[Open the full video (21 s)]({{ '/assets/projects/stretchable-exg/emg-rc-car.mp4' | relative_url }}) · [View the mask and circuit files](https://github.com/charleskim990819/Biopotential-EXG-sPCB/tree/master/hardware)
