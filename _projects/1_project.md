---
layout: page
title: PDA-LM Ink
description: Sintering-free, primer-free liquid-metal ink via catechol–Ga³⁺ chelation — a 10-minute deep dive
img: assets/img/12.jpg
importance: 1
category: research
related_publications: false
toc:
  sidebar: left
---

> **TL;DR** — Conventional liquid-metal (EGaIn) inks need mechanical sintering, organic solvents, or adhesion primers before they become useful conductors. We replaced all three crutches with a single chemistry: **catechol–Ga³⁺ coordination**. The result is a water-based ink that prints, sticks, and conducts in one step.

---

{% tabs pdalm-story %}

{% tab pdalm-story 🎯 The hook %}

### Why should you care?

Imagine you want to print a soft, stretchable circuit **directly onto human skin** — for a wearable biosensor, a transient bioelectronic, or even a temporary tattoo display.

Today's liquid metal (LM) inks force you to choose between:

- 🔥 **Sinter it** — mechanical pressure, laser, or stretch to break the oxide shell. Not gentle on skin.
- 🧴 **Primer it** — coat the substrate first with an adhesion promoter (often solvent-based, often toxic).
- 🌫️ **Solvent it** — disperse the LM particles in ethanol or worse. Slow drying, biocompatibility headaches.

We asked: *what if a single chemistry could do all three jobs — particle-to-particle conduction, substrate adhesion, and water dispersibility — at once?*

The answer turned out to be sitting in mussel biology.

{% endtab %}

{% tab pdalm-story 🔍 Where this came from %}

### The origin story

In late 2024 I was reading two literatures in parallel:

1. **Liquid metal printing papers** — Qi, Pyeon, Lee, Zheng, Pei, Müller, Tian, and others. All elegant chemistry, all stuck on the sintering / primer problem.
2. **Mussel-inspired adhesion (PDA / DOPA) papers** — Holten-Andersen's foundational work on catechol–metal coordination, originally explaining how mussels glue themselves to wet rocks.

I noticed something both communities had **stepped past without connecting:**

EGaIn particles spontaneously grow a **2–3 nm amorphous Ga₂O₃ shell** in air. That shell is what blocks conduction (so people grind it off) and what nobody bonds to (so people add primers).

But that shell is **hydroxyl-rich amorphous oxide**. And catechol's signature trick is binding hydroxyl-rich metal-oxide surfaces.

If polydopamine could grip Ga³⁺ the same way it grips Fe³⁺ on mussel adhesives, it might **simultaneously bridge particles and stick to substrates** — without ever needing to remove the oxide.

That was the hypothesis worth testing.

<details>
<summary><strong>Why dopamine·HCl specifically (and not just any catechol)?</strong></summary>

Most catechol-on-LM work uses tannic acid or DOPA polymerized in Tris buffer. Both have side reactions: tannic acid is a giant heterogeneous polyphenol, and Tris itself coordinates Ga³⁺. We use **dopamine hydrochloride** at controlled pH to get clean catechol–Ga³⁺ binding without buffer interference — the Holten-Andersen UV-Vis fingerprints (mono/bis/tris stoichiometries with pH 5/7.5/10 transitions) come out cleanly.

</details>

{% endtab %}

{% tab pdalm-story ⚠️ What everyone else tried %}

### The graveyard of partial solutions

Eight key LM-ink papers, three failure modes:

| Approach | Group / year | Solves conduction? | Solves adhesion? | Substrate-agnostic? |
|---|---|---|---|---|
| Mechanical sintering | Dickey et al. | ✅ (after sintering) | ❌ | ❌ |
| Laser sintering | Various | ✅ (after sintering) | ❌ | ❌ |
| Sub-µm milling + solvent ink | Qi 2022 | ✅ | ❌ | partial |
| Polymer primer underlayer | Pyeon 2023 | ✅ | ✅ (primer-dependent) | ❌ |
| Magnetic field percolation | Kim 2026 | ✅ (in-field) | ❌ | requires AMF |
| **PDA-LM (this work)** | **2026** | **✅ (instant)** | **✅ (catechol)** | **✅ (water-based)** |

The pattern: every prior approach **trades off one problem for another**. Nobody hit all three boxes with a single ink.

> The deeper reason: most groups treated the Ga₂O₃ shell as a *problem to remove*. We treated it as a *binding site to exploit*.

{% endtab %}

{% tab pdalm-story 💡 Our pivot %}

### The chemistry, in one paragraph

Polydopamine's catechol groups chelate the Ga³⁺ surface sites of the amorphous Ga₂O₃ shell. This achieves **two things simultaneously**:

1. **Particle–particle bridging** → PDA chains link adjacent EGaIn particles through shared Ga³⁺ coordination → conductive network forms *as the water evaporates*, no sintering needed.
2. **Particle–substrate adhesion** → PDA's residual catechols (and pyrogallol-like oxidation products) bind hydroxyl-rich surfaces (PDMS, PVA, paper, skin) through the same Holten-Andersen mechanism.

The pH controls coordination stoichiometry (mono / bis / tris), which we tune to balance conductivity vs. adhesion.

<details>
<summary><strong>Wait — does PDA itself short the conductive path?</strong></summary>

Good catch. PDA is a semiconductor (~10⁻⁵ S/cm). Bulk PDA between particles would kill conductivity. But the catechol–Ga³⁺ coordination is **interfacial**, not bulk — PDA wraps the particle surface in a monolayer-thin shell. Particle-to-particle electron transport goes through the **Ga-O-PDA-O-Ga bridge** directly, not through bulk PDA. Empirically, we measure sheet resistances comparable to sintered EGaIn films.

</details>

<details>
<summary><strong>How do we know it's coordination and not just physisorption?</strong></summary>

Three orthogonal evidence streams:

1. **UV-Vis titration** — pH-dependent absorption shifts matching Holten-Andersen's catechol–Ga³⁺ signatures (charge-transfer bands at ~395/495/600 nm depending on stoichiometry).
2. **ITC** — measurable binding enthalpy with stoichiometric breakpoint at the expected catechol:Ga³⁺ ratio.
3. **DFT (ORCA r2SCAN-3c, wB97X-D3/TZVP with BSSE)** — modeled catechol on -OH-terminated amorphous Ga₂O₃ slabs, binding energy ≫ physisorption baseline.

</details>

{% endtab %}

{% tab pdalm-story 🧪 What we built %}

### The ink, the film, the demo

#### The ink
- **Composition:** EGaIn microparticles + dopamine·HCl + water (with pH adjuster)
- **Storage:** stable for weeks at 4 °C
- **Patterning:** screen-print, brush, spray, hydroprint — your choice

#### The film
- Conductive **immediately after water evaporation** (no post-treatment)
- Sheet resistance comparable to sintered EGaIn films
- Bonds to PDMS, PVA, paper, glass, and skin without primer

#### The demonstrator
- **4-LED circuit water-transferred onto skin** (see [Water-Transfer Electronics](/projects/2_project/))
- Conductivity verified by lighting the LEDs immediately after transfer
- No sintering step, no primer step, no organic solvent

### The evidence stack (for the manuscript)

- 📊 **UV-Vis** — pH-stoichiometry titration matching Holten-Andersen framework
- 🌡️ **ITC** — binding enthalpy + stoichiometry breakpoint
- 🔬 **XPS** — Ga 3d / N 1s correlation on cured films
- 🧮 **DFT** — catechol–Ga₂O₃ surface binding energy from ORCA r2SCAN-3c (with BSSE)
- ⚡ **4-probe sheet resistance** — quantitative conductivity vs. PDA loading
- 🤲 **Pull-off / peel tests** — adhesion vs. substrate

{% endtab %}

{% tab pdalm-story ✨ Novelty %}

### What's new (in three claims)

We make three "first-time" claims, each backed by a different experiment:

> **Claim 1 — A liquid metal ink that requires no sintering, no primer, and no organic solvent.**
> Evidence: 4-probe sheet resistance immediately after water evaporation, compared to all eight competitor inks in the table above.

> **Claim 2 — The same single chemistry (catechol–Ga³⁺ coordination) provides both particle-bridging and substrate adhesion.**
> Evidence: removing dopamine eliminates both conductivity and adhesion (one-knob ablation); ITC + UV-Vis + DFT triangulate the coordination chemistry.

> **Claim 3 — The ink is biocompatible enough for direct on-skin printing.**
> Evidence: 4-LED demonstrator on human skin, no irritation observed; water-based formulation with biologically-derived dopamine (already a clinical molecule).

### Why this matters beyond our group

Anyone building **wearable bioelectronics, transient electronics, or printable functional materials** has been waiting for an LM ink that *just works* on soft, biological substrates. PDA-LM removes the sintering / primer / solvent overhead, making LM printing accessible to labs that don't have laser sintering rigs or chemistry hoods optimized for organic solvents.

{% endtab %}

{% tab pdalm-story 🚀 What's next %}

### Roadmap

- ✍️ **Manuscript in preparation** — targeting *Advanced Materials* (Figure 1 mechanism + 4 results figures + SI)
- 🤲 **[Water-transfer electronics platform](/projects/2_project/)** — Phase 2 integrating AD5941 + BLE for self-contained skin-mounted biosensing
- 🧬 **[Wearable BCI](/projects/3_project/)** — using PDA-LM microneedle contacts for ear-EEG
- 🔬 **Chemistry extensions** — substituting dopamine with other catechol-rich biomolecules (DHCA, gallic acid) to tune mechanical / optical / degradation properties

### Want to collaborate?

If you work on:

- Transient / bioresorbable bioelectronics
- Skin-mounted continuous monitoring
- Printed flexible energy storage

…the PDA-LM ink might fit your stack. [Get in touch](/).

{% endtab %}

{% endtabs %}

---

### Acknowledgments

This work is conducted in **Prof. Jeong-Mok Seo's lab** at Yonsei University, with computational support from the lab's ORCA / Slurm cluster. DFT methodology builds on the lab's prior amorphous Ga₂O₃ surface chemistry studies.
