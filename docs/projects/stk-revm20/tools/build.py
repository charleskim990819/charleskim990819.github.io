#!/usr/bin/env python3
"""Generate the RevM20 portfolio from a versioned design baseline.

Only standard-library Python is needed. Datasheet limits, calculations and
physical results have separate fields; no missing measurement becomes zero.
"""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT.parents[2]
SHA = "f2e3c2a2f3499b0fdad05f8f8aaffb69c3773540706764b1e55289f653d65690"
DATE = "2026-10-15"
REPO = "https://github.com/charleskim990819/charleskim990819.github.io"
DOC_URL = REPO + "/tree/main/docs/projects/stk-revm20"
ASSET = "/assets/projects/stk-revm20"


def clean_text(s):
    s = re.sub(r'\b(The|As of|nominal|default|Default|at|At|max|min|approximately|permanent|specified|example|Example|above|below|to|from|of|with|for|all|permits|outline|and|typ|uses|Each|spans|produce|equal|internal|Internal|datasheet|measured|plus|step|half-step|absolute|assumes|hypothetical|sum|gives|qualify|about|records|interval|window|Output|planned)(?=[0-9])', r'\1 ', s)
    s = re.sub(r'(?<![A-Za-z0-9])(-?[0-9]+(?:\.[0-9]+)?)C\b', r'\1 °C', s)
    s = re.sub(r'(?<=[0-9])(?=(?:pA|nA|uA|mA|uV|mV|kV|V|kSPS|SPS|MHz|kHz|Hz|LSB|kohm|Mohm|ohm|mm|ms|s|K)\b)', ' ', s)
    return s.replace('allI,', 'all I,').replace('victimWE-RE', 'victim WE-RE').replace('all25', 'all 25').replace('other22physical','other 22 physical')


def clean_values(value):
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, list):
        return [clean_values(v) for v in value]
    if isinstance(value, dict):
        return {k:clean_values(v) for k,v in value.items()}
    return value


def parallel(a, b):
    return a * b / (a + b)


def calculations():
    rows = []
    for r, cf, stop in zip([1e3, 1e4, 1e5, 1e6], [68e-9, 22e-9, 6.8e-9, 2.2e-9], [1e-3, 1e-4, 1e-5, 1e-6]):
        rf = parallel(r + 3, 1e7)
        # DC model only. 3 ohms is the firmware approximation, not a part limit.
        rf_min = parallel(r * .999 + 3, 1e7 * .99)
        rf_max = parallel(r * 1.001 + 3, 1e7 * 1.01)
        ron_min = parallel(r, 1e7)
        ron_max = parallel(r + 4, 1e7)
        rows.append(dict(selected_R_ohm=r, selected_C_F=cf, firmware_stop_A=stop,
                         model_Rf_ohm=rf,
                         passive_gain_min_pct=(rf_min / rf - 1) * 100,
                         passive_gain_max_pct=(rf_max / rf - 1) * 100,
                         ron_only_min_pct=(ron_min / rf - 1) * 100,
                         ron_only_max_pct=(ron_max / rf - 1) * 100,
                         adc_code_pA_at_PGA1=1.2 / (2**23 * .5 * rf) * 1e12,
                         feedback_thermal_pA_sqrtHz_25C=math.sqrt(4 * 1.380649e-23 * 298.15 / rf) * 1e12,
                         divider_zero_example_nA=500e-6 / (.5 * rf) * 1e9,
                         tia_offset_direct_example_pA=150e-6 / rf * 1e12))
    return dict(ranges=rows, DAC_LSB_uV=5 / 2**16 * 1e6,
                DAC_nearest_rounding_uV=5 / 2**17 * 1e6,
                divider_alpha_min=.9998 / (1.0002 + .9998),
                divider_alpha_max=1.0002 / (.9998 + 1.0002),
                reference_fraction=5e-3 / 2.5,
                reference_error_mV_at_1V2=1.2 * (5e-3 / 2.5) * 1000,
                CE_R_drop_example_V=3e-3 * 100,
                required_error_pA_example=1e-9 * .01 * 1e12)


def requirement(i, topic, baseline, status, source, tests, acceptance):
    return dict(id=f"R{i:02}", topic=topic, baseline=baseline, evidence_status=status,
                sources=source.split(), validation_ids=tests.split(), acceptance=acceptance)


def requirements():
    C, F, M, U = "CAD_CONFIRMED", "FW_CONFIRMED", "CALCULATED", "UNSPECIFIED"
    return [
        requirement(1, "Default topology", "3 current channels + pH; one shared RE and CE; not separate galvanically isolated cells.", C, "NET BRIDGE", "V01 V02 V13 V16", "Confirm physical links, polarity and actual WE-RE control before connecting enzyme electrodes."),
        requirement(2, "Four-current mode", "4CA requires all physical CH4 selectors in WE mode with power removed and MODE WE acknowledgment.", F, "BRIDGE FW", "V02 V13", "No mixed jumper state; firmware declaration must match inspected copper links."),
        requirement(3, "Continuous current paths", "Four OPA2320 TIA channels; U21-U24 select feedback gain, not the sampled WE.", C, "NET BOM FW", "V09 V13 V14", "Validate simultaneous streams, settling and cross-channel response with a dummy cell."),
        requirement(4, "WE-RE command", "Firmware command envelope +/-1.2 V, nominal VSET=2.5 V+E; actual compliance is load dependent.", F, "FW DACDOC", "V08 V09 V13", "Numerical maximum actual potential error is TBD; command range is not an accuracy specification."),
        requirement(5, "Current ranges", "Selected R: 1k/10k/100k/1M ohm with permanent 10M ohm feedback; model includes 3 ohm switch approximation.", C, "NET FW", "V10 V11 V12", "Calibrate each board/channel/range/PGA profile; characterize independent points."),
        requirement(6, "Current stop limits", "Firmware limits: +/-1mA, +/-100uA, +/-10uA, +/-1uA. ADC/PGA and TIA headroom can limit earlier.", F, "FW", "V10 V19", "Exercise clipping and stop logic with a protected dummy cell; do not interpret limits as validated ranges."),
        requirement(7, "ADC conversion", "ADS131M04, four simultaneous 24-bit conversion channels. CA: nominal 976.5625 SPS/channel at 8MHz/2/4096.", M, "FW ADS", "V07 V14", "Measure rate, channel alignment, gaps and clock error. 24-bit coding is not effective resolution."),
        requirement(8, "Filtering and output", "CA default ENBW 1Hz, output 20 rows/s; configurable ENBW 0.1-10Hz and output 10-100 rows/s.", F, "FW", "V07 V11", "Measure actual noise and step response at the recorded filter configuration."),
        requirement(9, "DAC command generation", "DAC80508 16-bit; nominal 0-5V span on four active outputs with software simultaneous update.", F, "FW DAC", "V08 V09", "Validate voltage and update timing; DC calibration does not establish dynamic phase accuracy."),
        requirement(10, "pH input", "OPA391 input buffer and driven guard; CH4 voltage limit +/-600mV, PGA1/2; PH2/PH3 calibration interface.", C, "NET FW", "V15 V16 V23", "Actual pH error, input impedance and drift targets are TBD; calibrate the fitted electrode."),
        requirement(11, "Sample temperature", "Manual TEMP input 0-60C; no implemented automatic sample-temperature measurement. Battery NTC serves another purpose.", F, "FW", "V15 V23", "Define actual sample temperature range and uncertainty; 0-60C is a software input envelope."),
        requirement(12, "EIS operating envelope", "Selected channel only: 1-100Hz default, 0.1Hz with EISLOW; amplitude >0 to 20mV peak; |bias|+amplitude <=1.2V.", F, "FW EISDOC", "V17 V18", "Physical magnitude/phase accuracy and usable impedance range remain TBD."),
        requirement(13, "EIS range restrictions", "1k/10k: up to100Hz; 100k: up to10Hz; 1M: CA only. Current and voltage ADCs have separate conversion timing.", F, "FW EISDOC", "V17 V18", "Characterize exact frequency/profile; DRDY timestamps are not ADC aperture timestamps."),
        requirement(14, "Live channel independence", "Sampling accepts STOP only. Range/bias changes require global stop. U10 SEL pins share CELL_EN; no per-WE disconnect.", F, "NET FW", "V19", "This is an implemented limitation, not a performance target awaiting measurement."),
        requirement(15, "USB interface", "USB-C, USB2 Full Speed 12Mbps, USB Serial/JTAG, separate CC Rd resistors. No PD, BLE or Wi-Fi feature in current firmware.", C, "NET USB FW", "V05 V06", "Check both orientations, enumeration and data integrity. Whole-interface 90ohm compliance is unverified."),
        requirement(16, "Power architecture", "USB/BQ25180 SYS path, MCU 3.3V and analog boost/LDO rails. FW 5VA coarse validity window: 4.85-5.15V.", C, "NET FW", "V03 V04 V05", "Measure all rails, ripple, transients and input current; monitor thresholds are not regulator accuracy claims."),
        requirement(17, "Cell startup and faults", "CELL_EN defaults low; firmware gates START on valid monitors and setup. Power task nominal polling interval200ms.", F, "FW", "V03 V19 V20", "Measure actual electrode state and fault latency, including MCU reset and stalled firmware."),
        requirement(18, "Battery and charging", "External protected 1S LiPo path. FW disables charging after boot; BQ25180 reset state permits charging before FW initialization.", C, "NET FW BQ", "V03 V21", "Battery capacity/NTC/charge profile TBD. First bring-up uses USB with battery and sensor disconnected."),
        requirement(19, "PCB form factor", "4 copper layers, nominal0.20mm FPC; outline41.8x42.5mm; no permanent stiffener; populated areas need flat support and USB retention.", C, "REL GEOM", "V22 V24 V25", "Bend radius/cycles, connector load and operating temperature are TBD. Flexibility does not establish stretchability."),
        requirement(20, "CAD checks", "Released DRC0 errors/0 warnings/0 unconnected; ERC0;202 references and687 physical pads checked for schematic parity.", C, "DRC ERC PARITY", "V01 V02", "Read together with recorded ignored check classes. No electrical performance follows from CAD pass."),
        requirement(21, "Fabrication and assembly", "196 assembled parts,54 BOM SKUs; TOP101/BOTTOM95; BOM/CPL parity checked; nominal coverlay and paste checks recorded.", C, "REL CSV CAM", "V01 V22", "Factory CAM, placement orientation/origin and FPC reflow/fixture acceptance pending."),
        requirement(22, "Absolute current accuracy", "No accepted numeric error function or minimum quantitative current is established.", U, "REL", "V10 V11 V12 V23", "Define DeltaI_allow(I,T,B), minimum signal, calibration interval and instrument uncertainty before sign-off."),
        requirement(23, "WE-RE accuracy and cell limits", "Maximum allowed potential error, electrode Cdl/Rct/Rs and common CE current envelope are not fixed.", U, "REL NET", "V08 V09 V13", "Define DeltaE_allow and cell parameter range before claiming regulation performance."),
        requirement(24, "Crosstalk acceptance", "Allowable electrical and chemical cross responses are not yet specified; shared-cell EIS may perturb other channels.", U, "NET PNAS", "V13 V14 V16 V18", "Define absolute error per victim channel and normalized coupling for each aggressor/victim pair."),
        requirement(25, "Power and lifetime", "Current consumption, efficiency, worst-case power, thermal rise and battery runtime are unmeasured; battery capacity is not selected.", U, "REL", "V04 V21 V24", "Set duty cycle, load states, capacity and derating assumptions before calculating runtime."),
        requirement(26, "Scope of implemented features", "CA, pH and experimental selected-channel EIS. No implemented CV/DPV, wireless telemetry, automatic charging policy or quantitative EIS qualification.", F, "FW EISDOC", "V07 V17", "Describe RevM20 separately from the earlier AD5941 project and its historical results."),
    ]


def budget_rows(c):
    def b(i, topic, value, basis, conversion, treatment, refs, tests):
        return dict(id=f"B{i:02}", topic=topic, value=value, evidence_status=basis,
                    conversion=conversion, treatment=treatment, sources=refs.split(), validation_ids=tests.split(), measured_value=None)
    return [
        b(1,"Effective TIA gain", "Rf=(Rselected+3ohm) parallel10Mohm; detailed range table below.","CALCULATED", "Vcode=raw*1.2V/2^23; I=-Vcode/(0.5*PGA*Rf) before calibration.","3ohm is a firmware approximation; calibrate actual fitted path.","NET FW","V10"),
        b(2,"Feedback resistor tolerance", "Selected R +/-0.1%; permanent10M +/-1%. Highest-gain combined DC term approximately +/-0.182%.","CALCULATED", "Evaluate both parallel resistors at tolerance corners; hold Ron=3ohm for this term.","Uncalibrated multiplicative error; resistor TCR/self-heating and calibration uncertainty remain separate.","NET BOM","V10 V23"),
        b(3,"Gain-switch Ron model", "ADG704 typ2.5ohm/max4ohm at25C; max4.5ohm to85C. FW uses3ohm.","DATASHEET", "At25C use conservative0<=Ron<=4ohm, other components nominal; range table gives model residual.","Do not add the entire Ron again after calibrating fitted gain. No whole-temperature gain bound claimed.","ADG FW","V10 V12 V23"),
        b(4,"ADG704 leakage", "On/off leakage magnitude max100pA at25C;300pA over-40..85C at specified5V-table test conditions.","DATASHEET", "Each specification is a terminal/test-condition limit, not a complete-board total. Off branches require topology-aware accounting.","Measure zero versus bias/time/temperature. Constant offset calibration does not bound drift.","ADG NET","V11 V12 V23"),
        b(5,"WE isolation-switch leakage", "TMUX1112 at5V/25C: on leakage max25pA at2.5V;100pA at1.5/4.5V test points.","DATASHEET", "Electrode-side current can include switch leakage; source buffers and humid surfaces also load that node.","Keep terminal conditions with each value; include the actual active/inactive topology.","TMUX NET","V11 V12 V23"),
        b(6,"TIA input bias current", "OPA2320: max0.9pA at25C, specified common-mode and supply conditions.","DATASHEET", "Direct current offset term; the installed TIAs are OPA2320, not OPA2391.","Review source-buffer leakage separately and measure fitted-board temperature dependence.","OPA NET BOM","V11 V23"),
        b(7,"TIA offset voltage", "OPA2320 Vos max150uV at25C; drift max5uV/C under specified temperature test.","DATASHEET", "Direct current-equivalent term Vos/Rf; also changes actual WE bias and electrode reaction current.","A simple Vos/Rf conversion does not include the chemistry-dependent response to potential error.","OPA","V08 V10 V23"),
        b(8,"Input-divider mismatch", "Each1k resistor +/-0.02%; ideal unloaded alpha spans0.4999..0.5001. P/N mismatch at2.5V can produce500uV ADC differential offset.","CALCULATED", "Equivalent current=500uV/(0.5*Rf);1.1nA at the highest-gain model. Example at equal2.5V inputs.","Use bias-dependent zero calibration. ADC input loading, resistor TCR and correlation are not included in this example.","NET BOM FW","V10 V12 V23"),
        b(9,"ADC reference, gain and offset", "ADS131M04 internal1.2V model. Actual gain/offset/drift at selected PGA, OSR and source impedance await characterization.","BENCH_PENDING", "For already input-referred ADC voltage uncertainty, DeltaI=DeltaV_ADC_input/(0.5*Rf). Account for PGA gain uncertainty separately.","Do not insert datasheet4kSPS noise as the measured976.5625SPS plus1Hz-filter result; avoid counting included reference errors twice.","ADS FW","V10 V11 V23"),
        b(10,"ADC code step", "24-bit bipolar conversion: LSB=1.2V/(2^23*PGA); PGA1 current code steps listed below.","CALCULATED", "I_LSB=1.2/(2^23*PGA*0.5*Rf).", "Code step is neither noise floor nor current accuracy; ideal quantization RMS requires a suitable statistical model.","ADS FW","V11"),
        b(11,"Feedback Johnson noise", "At25C and1Hz ENBW, resistor-only input noise approximately4.052..0.135pA RMS across the four modeled ranges.","CALCULATED", "sqrt(4*kB*T*B/Rf), assuming an ideal DC feedback resistance and white noise.","Partial model only: op-amp voltage/current noise, noise gain, dividers, ADC,1/f and cell are excluded.","NET","V11"),
        b(12,"DAC quantization and INL", f"Nominal DAC code step{c['DAC_LSB_uV']:.5f}uV; nearest rounding half-step{c['DAC_nearest_rounding_uV']:.5f}uV; DAC80508 INL max1LSB under stated code/load conditions.","CALCULATED", "5V/65536. Envelope endpoints can be moved inward one code by firmware.","Keep rounding, INL, DAC gain/offset and fitted calibration residual as distinct terms.","DAC FW","V08 V09"),
        b(13,"Shared DAC reference", "Internal2.5V initial accuracy max+/-5mV; reference-only scale example+/-0.2% of E.","CALCULATED", "Ideal shared-reference relation E=(2*code/65536-1)*Vref; at1.2V the term is+/-2.4mV, with first-order cancellation atE=0.","This correlation excludes DAC gain/offset, buffer offsets and load effects; do not add two independent absolute2.5V-reference errors.","DAC NET","V08 V23"),
        b(14,"WE switch and solution drop", "DeltaE includes I_WE*Ron_WE and a cell-geometry-dependent solution transfer resistance. Example10uA*1kohm=10mV.","CALCULATED", "Actual electrode-side WE-RE measurement is required. The example is not measured patch resistance.","Static near-zero-load DAC calibration does not remove arbitrary load-dependent voltage drop.","NET DACDOC","V08 V13"),
        b(15,"Common CE headroom", "R4=100ohm; same-polarity sum3mA gives0.30V resistor drop before switch/cell polarization.","CALCULATED", "I_CE is the signed sum of all WE currents. This example does not qualify3mA operation.","Sweep summed load and cell capacitance; CE_MON reads the driver before R4, not the electrode surface.","NET FW","V09 V13"),
        b(16,"pH voltage and temperature", "Input-buffer leakage*electrode source resistance, differential buffer offsets, reference drift and temperature remain separate terms.","BENCH_PENDING", "Delta pH=DeltaV/|fitted electrode slope|. Ideal25C Nernst slope is about59.16mV/pH; use measured electrode slope.","Sample-temperature measurement and pH accuracy targets are TBD. Battery NTC is not a sample sensor.","PH FW","V15 V16 V23"),
        b(17,"EIS phase and magnitude", "Different current/voltage ADC filters, clocks, ISR delays, TIA transfer and DAC updates contribute to complex-ratio error.","BENCH_PENDING", "Compare conventional Z=-V/I to characterized R/RC at the exact channel/frequency/range/PGA/filter/calibration profile.","Keep EIS_ACTUAL_UNVERIFIED. A fitted DC coefficient or modeled delay does not qualify phase.","EISDOC FW","V17 V18"),
        b(18,"Board and chemistry residuals", "Supply coupling, FPC/connector humidity leakage, temperature drift, electrode selectivity and H2O2 transport have no measured bound.","BENCH_PENDING", "Electrical aggressor/victim tests and single-analyte enzyme controls must be evaluated separately.","No total worst-case accuracy or LOD can be calculated while these terms and numerical requirements are unresolved.","REL PNAS","V11 V13 V14 V16 V23 V24"),
    ]


def validations():
    # Existing audit review is not a fresh physical test execution.
    rows = []
    def add(i, title, method, accept, sources, reqs, evidence=False, result=None):
        rows.append(dict(id=f"V{i:02}", title=title, method=method, acceptance=accept,
                         execution_status="AUDIT_REVIEWED" if evidence else "NOT_RUN",
                         evidence_status="CAD_CONFIRMED" if evidence else "BENCH_PENDING",
                         result=result, sources=sources.split(), requirement_ids=reqs.split(),
                         measurement_file=None, instrument_uncertainty=None))
    add(1,"Released CAD and manufacturing files", "Review hash-bound DRC/ERC, BOM/CPL, coverlay/paste and schematic-pad parity records.", "No recorded violation in enabled checks; identify all excluded checks; manufacturer approval remains separate.","REL DRC ERC PARITY CSV CAM", "R19 R20 R21",True,"Existing release audits:DRC0/ERC0/unconnected0;202 references/687 pads;54 BOM SKUs/196 fitted parts. Reviewed, not rerun here.")
    add(2,"Selector and pin mapping", "Read J1/U10/U21-24/U14/U25 net connections and final PH link audit; inspect physical links after assembly.", "Default3CA+pH, matching declaration; no unintentional TIA connection to pH. Physical inspection still pending.","NET BRIDGE", "R01 R02 R20",True,"Logical connections and nominal PH link copper confirmed from released CAD; no assembled board inspected.")
    add(3,"First power-up and reset", "USB only, sensor/battery disconnected; current-limited supply, scope CELL_EN/rails/reset and repeat cold/MCU resets.", "No unintended electrode connection; rail sequence consistent with component limits. Repeat count and reset waveform envelope recorded.","FW BQ", "R16 R17 R18",result=None)
    add(4,"Rail quality and power", "Measure3V3_D/3V3_A/5V_A/DAC_AVDD at rest/acquisition/USB traffic and defined dummy loads; record ripple bandwidth and current.", "5VA coarse FW window4.85..5.15V; other rail, ripple, transient and power budgets must be fixed before qualification.","NET FW", "R16 R25")
    add(5,"USB power and plug orientations", "Enumerate in both USB-C orientations; record inrush, SYS/rail startup, disconnect and brownout behavior.", "Both orientations work without rail excursions beyond device limits; defined test count and fault behavior reported.","NET USB", "R15 R16")
    add(6,"USB signal and data integrity", "Exercise console/programming and sustained timestamped data; scope interface only with suitable probes.", "No unexplained loss/reset in a declared duration and host/cable matrix. USB impedance/compliance is a separate claim.","USB FW", "R15")
    add(7,"Acquisition rate and data flags", "Log raw four-channel frames and sequence/DRDY timing at each required OSR/PGA/filter setting.", "Rate compared with nominal976.5625SPS; observed clock tolerance, gaps and clipping flags reported. Output20rows/s is not ADC sample rate.","FW ADS", "R07 R08 R26")
    add(8,"Actual WE-RE DC accuracy", "Use calibrated high-input-impedance DMM, defined dummy cell and independent interior/endpoint points before and after DACCAL.", "Max/RMS residual plus instrument uncertainty <=DeltaE_allow, presently TBD. Sweep current as well as command.","DACDOC FW", "R04 R09 R23")
    add(9,"Loop stability and compliance", "Scope electrode-side WE-RE and CE during safe steps across R_s/R_ct/C_dl and same-polarity total loads, all required gains.", "No sustained oscillation; settling/overshoot, allowed cell range and voltage error limits TBD before qualification.","NET", "R03 R04 R09 R23")
    add(10,"Current transfer and calibration", "Floating/isolated calibrated current or characterized dummy cell; zero and signed points per channel/range/PGA; independent validation points.", "Report error versus current, linearity and combined uncertainty againstDeltaI_allow(I,T,B), currently TBD. Respect tighter ADC/headroom limits.","FW", "R05 R06 R22")
    add(11,"Zero, noise and usable minimum current", "Document input termination, warm-up, raw/filtered PSD and RMS, duration, ENBW, bias, temperature and EMI conditions.", "Report measured input noise and drift; establish minimum quantitative current from agreed signal/error criterion, not ADC code step.","FW ADS", "R08 R22")
    add(12,"Bias-dependent and switch leakage", "Record zero versus WE bias/range, temperature and time; separate dry-board, connector and fixture leakage controls.", "Residual after offset/gain/bias fit stays within the assigned leakage budget, which must first be defined.","NET ADG TMUX", "R05 R22")
    add(13,"Shared-cell electrical coupling", "Without enzymes, step one channel load using an isolated dummy network; record allI, victimWE-RE and CE. Repeat each aggressor/victim pair.", "Report both absoluteDeltaI_victim andDeltaI_victim/DeltaI_aggressor with voltage disturbance; thresholds TBD. Preserve real shared impedances.","NET", "R01 R03 R04 R23 R24")
    add(14,"ADC, supply and digital coupling", "Keep analog loads fixed; apply activity to other channels, USB and SPI; compare raw/filteredI and supply spectra.", "Assign an absolute error/noise budget before judging pass; distinguish ADC coupling from shared-cell effects.","FW ADS", "R03 R07 R24")
    add(15,"pH calibration and loading", "Use certified buffers at measured sample temperature; PH2/PH3 fit then independent buffers; characterize electrode source impedance/loading.", "Residual pH, drift and temperature uncertainty <=agreedpH tolerance, currently TBD.","FW PH", "R10 R11")
    add(16,"Chemical coupling and pH disturbance", "Add glucose alone, then lactate/other target alone while recording all channels; include enzyme-free PB control and actual PAH/flow geometry.", "Report concentration-equivalent cross responses andpH shifts at defined analyte, flow and oxygen conditions; acceptance TBD.","PNAS", "R01 R10 R24")
    add(17,"EIS complex-ratio calibration", "Use characterized passiveR/RC with traceable complexZ; validate independent loads at each exact frequency/profile and quantifyV/I timing.", "Magnitude/phase tolerances and usableZ range TBD; preserve raw traces and unverified flag until qualified.","EISDOC", "R12 R13 R26")
    add(18,"EIS effect on other channels", "Run selected-channel EIS in the shared dummy/chemical cell and compare all other current/pH channels with CA-only baseline.", "Quantify disturbance; do not label other channels independent concentration measurements without a suitable criterion.","NET EISDOC", "R12 R13 R24")
    add(19,"Limits and global stop", "Induce protected overrange, ADC clipping, stale/invalid monitor and allowed communication faults; scope actual cell isolation.", "Verify global stop and record physical latency. No claim of independent per-WE stop;200ms is a polling setting, not guaranteed fault latency.","FW NET", "R06 R14 R17")
    add(20,"Calibration persistence and invalidation", "Change range/PGA/DAC fit and restart; inspect valid masks, CRC rejection, profile binding and safe-start behavior.", "Stale/corrupt coefficients cannot silently qualify a different profile; actual fits remain linked to board serial and instrument record.","FW DACDOC EISDOC", "R05 R17")
    add(21,"Battery qualification", "After choosing capacity/protection/NTC/profile, validate charger registers, power path, cold reset, USB removal and discharge at defined loads.", "Battery-specific current/voltage/temperature limits and runtime target TBD; firmware-after-boot charging-off does not qualify pre-boot behavior.","BQ FW", "R18 R25")
    add(22,"Manufacturer CAM and assembly", "Obtain factory review of stackup, vias/slots, panel rails, fixture, bottom module reflow and actual component origins/orientations.", "Explicit CAM/placement/reflow disposition with customer confirmation; a quote or browser preview is not approval.","REL CSV CAM", "R19 R21")
    rows[-1]['execution_status']='AWAITING_REVIEW'
    rows[-1]['evidence_status']='MANUFACTURER_PENDING'
    add(23,"Temperature and humidity", "Repeat zero/gain/pH/coupling under defined temperature/RH and wet-connector conditions with sample temperature measured separately.", "Environmental range, leakage and drift budgets TBD; keep drying/recovery data and calibration age.","ADG PH", "R10 R11 R22")
    add(24,"Mechanical and thermal behavior", "Record flat-supported baseline, connector retention and defined bend/strain cycles; repeat electrical checks and measure self-heating.", "Bend radius, cycle count, fixture/load and strain requirement TBD. FPC bendability does not demonstrate stretchable electronics.","GEOM", "R19 R25")
    add(25,"Board-to-board repeatability", "Assign serial numbers to the planned5boards; repeat accepted functional/calibration tests and record assembly or calibration failures.", "Report n, exclusions, distribution and worst board. A5-board pilot does not establish production yield or long-term reliability.","REL", "R19 R22 R25")
    return rows


SOURCES = {
    "REL": ("Released design manifest", "MANIFEST.json"),
    "NET": ("Released schematic connectivity", "verification/SCHEMATIC_NETLIST.xml"),
    "BOM": ("Released fitted BOM", "STK_4WE_RevM20_USB_C_BOM.csv"),
    "BRIDGE": ("Factory PH link audit", "verification/FINAL_BRIDGES.json"),
    "DRC": ("Final DRC and ignored checks", "verification/FINAL_DRC.json"),
    "ERC": ("Final ERC and ignored checks", "verification/FINAL_ERC.json"),
    "PARITY": ("Schematic to physical pad parity", "verification/PCB_SCHEMATIC_NET_PARITY.json"),
    "CSV": ("BOM and placement parity", "verification/FINAL_CSV_PART_PARITY.json"),
    "CAM": ("Nominal Gerber geometry checks", "verification/FINAL_CAM.json"),
    "GEOM": ("Native board dimensions", "verification/RELEASE_NATIVE_INSPECTION.json"),
    "USB": ("USB geometry and reference audit", "verification/USB_CONTROLLED_PAIR_REVIEW.json"),
    "FW": ("FW18 acquisition and calibration source", "firmware/app/main/main.c"),
    "DACDOC": ("WE command calibration procedure", "firmware/app/DAC_CALIBRATION.txt"),
    "EISDOC": ("Actual-voltage EIS calibration procedure", "firmware/app/ACTUAL_EIS_CALIBRATION.txt"),
    "ADG": ("ADI ADG704 RevA pp2-3", "https://www.analog.com/media/en/technical-documentation/data-sheets/ADG704.pdf"),
    "OPA": ("TI OPA2320 RevF electrical table", "https://www.ti.com/lit/ds/symlink/opa320.pdf"),
    "ADS": ("TI ADS131M04 RevD", "https://www.ti.com/lit/ds/symlink/ads131m04.pdf"),
    "DAC": ("TI DAC80508 RevD", "https://www.ti.com/lit/ds/symlink/dac80508.pdf"),
    "TMUX": ("TI TMUX111x RevC 5V electrical table", "https://www.ti.com/lit/ds/symlink/tmux1111.pdf"),
    "PH": ("TI OPA391 RevE", "https://www.ti.com/lit/ds/symlink/opa391.pdf"),
    "BQ": ("TI BQ25180", "https://www.ti.com/lit/ds/symlink/bq25180.pdf"),
    "PNAS": ("Chae etal PNAS2023", "https://doi.org/10.1073/pnas.2219231120"),
}


def md_table(headers, rows):
    def esc(v):
        return str(v).replace('*','×').replace("|", "\\|").replace("\n", " ")
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] + ["| " + " | ".join(esc(v) for v in row) + " |" for row in rows]) + "\n"


LEGEND = """CAD_CONFIRMED = confirmed in released CAD/audit records; FW_CONFIRMED = source-reviewed behavior; CALCULATED = stated analytical model; DATASHEET = manufacturer specification under its conditions; BENCH_PENDING = physical evidence required; MANUFACTURER_PENDING = factory disposition required; UNSPECIFIED = numerical requirement not yet set. These labels do not imply factory approval or measured product performance."""


def write_docs(d):
    (ROOT / "data").mkdir(parents=True, exist_ok=True)
    (ROOT / "data/baseline.json").write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    req = md_table(["ID / topic", "Current baseline and conditions", "Evidence", "Acceptance or remaining work", "Tests"], [
        [r['id'] + " " + r['topic'], r['baseline'], r['evidence_status'] + "; " + ",".join(r['sources']), r['acceptance'], ",".join(r['validation_ids'])] for r in d['requirements']])
    budget = md_table(["ID / source", "Value / condition", "Basis", "Propagation", "Treatment and limitation", "Tests"], [
        [r['id'] + " " + r['topic'], r['value'], r['evidence_status'] + "; " + ",".join(r['sources']), r['conversion'], r['treatment'], ",".join(r['validation_ids'])] for r in d['error_budget']])
    val = md_table(["ID / test", "Method", "Acceptance", "Execution / current result", "Requirements"], [
        [r['id'] + " " + r['title'], r['method'], r['acceptance'], r['execution_status'] + ": " + (r['result'] or ("Factory review not received." if r['execution_status']=='AWAITING_REVIEW' else "Physical test not run; no measured value.")), ",".join(r['requirement_ids'])] for r in d['validation']])
    ranges = md_table(["Selected R", "Model Rf (ohm)", "Passive R gain bounds (%)", "Ron-only model bounds (%) at25C", "PGA1 current code step", "Feedback-only noise density"], [
        [f"{r['selected_R_ohm']:g} ohm",f"{r['model_Rf_ohm']:.6f}",f"{r['passive_gain_min_pct']:.5f} to {r['passive_gain_max_pct']:.5f}",f"{r['ron_only_min_pct']:.5f} to {r['ron_only_max_pct']:.5f}",f"{r['adc_code_pA_at_PGA1']:.6f} pA",f"{r['feedback_thermal_pA_sqrtHz_25C']:.6f} pA/√Hz"] for r in d['calculations']['ranges']])
    for name, title, intro, text in [
        ('requirements.md','STK RevM20 requirements and design baseline', 'This is a baseline reconstructed from the current implementation, not a claim that all original product requirements were fixed before design. Accuracy, environmental limits and lifetime remain open requirements.',req),
        ('error-budget.md','STK RevM20 preliminary error budget', 'This is a component-level pre-calibration budget and a plan for residual characterization. There is no justified total product accuracy yet. Keep bounded bias terms, typical noise densities, correlated reference terms and unknown residuals separate. Do not RSS maximum limits as if they were independent standard deviations.',budget + '\n## Range calculations\n\n' + ranges + '\nThe passive-resistor and Ron rows vary different inputs separately. They are not independent measured uncertainties and are not a combined corner bound. Noise uses298.15K and ideal DC feedback resistance. Quantization steps do not establish effective resolution.\n\n## Requirement feasibility example\n\nA hypothetical1nA signal with1% error permits10pA total error. This is an illustration, not an adopted requirement. The ADG704 specified100pA terminal leakage limit alone prevents inferring that target from part selection. Actual bias-dependent leakage, temperature drift and post-calibration residual must be characterized.\n\n## Budget closure\n\nDefine DeltaI_allow(I,T,B), DeltaE_allow, pH tolerance and EIS magnitude/phase tolerances. Assign budgets to the relevant mechanisms and add instrument/fixture uncertainty. Preserve uncalibrated and independently validated post-calibration results; unresolved contributors remain null rather than zero.\n'),
        ('validation.md','STK RevM20 validation matrix', 'V01-V02 review existing digital design audits. V22 awaits manufacturer review. The other22physical test groups have not been run. An unset numerical acceptance criterion blocks performance qualification even after a measurement exists.',val + '\n## Measurement record\n\nFor every run retain board serial, PCB/FW hashes, channel, selector state, range/PGA/OSR/filter/output rate, calibration fingerprint, supply, actual sample temperature/RH, cell/fixture model, instrument identity/calibration/uncertainty, raw data, processing script version, acceptance criterion and outcome. Use independent validation points after fitting.\n\n## Test sequence\n\n1. Factory review and physical assembly/link inspection.\n2. USB-only rails/reset/programming, battery and sensor disconnected.\n3. Dummy-cell acquisition, DC voltage/current and loop stability.\n4. Noise/leakage and electrical cross responses.\n5. pH and single-analyte chemical controls, then mixed samples.\n6. EIS, environment, mechanical and board-to-board characterization as applicable.\n')]:
        (ROOT / name).write_text(f"# {title}\n\nAs of{DATE}; hardware RevM20, firmware FW18.\n\n{intro}\n\n{LEGEND}\n\n{text}\nSources: [evidence index](evidence/README.md). [Project overview](README.md).\n")
    return req, budget, val, ranges


def snapshot_evidence(release):
    out = ROOT / 'evidence'
    out.mkdir(exist_ok=True)
    def read(name):
        return json.loads((release / name).read_text())
    manifest, drc, erc = read('MANIFEST.json'), read('verification/FINAL_DRC.json'), read('verification/FINAL_ERC.json')
    parity = read('verification/PCB_SCHEMATIC_NET_PARITY.json')
    summary = dict(review_date=DATE, scope='Extracted released CAD/code audit facts; no physical test results.',
                   pcb_sha256=SHA, release_status=manifest['status'],
                   board={k:v for k,v in manifest['PCB'].items() if k!='USB_case_retention_confirmed'},
                   mechanical_support_assumption='Flat support under populated areas and case retention of the USB shell; no physical fit or strength test performed.',
                   checks=manifest['checks'], limitations=manifest['limitations'],
                   DRC_ignored_checks=drc['ignored_checks'], ERC_ignored_checks=erc['ignored_checks'],
                   parity={k:parity[k] for k in ['status','PCB_component_count','physical_PCB_pad_count','expected_connected_named_pin_count','expected_NC_named_pin_count','issues']})
    (out/'review-summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    netlist=ET.parse(release/'verification/SCHEMATIC_NETLIST.xml').getroot()
    selected={'J1','U2','U3','U4','U10','U14','U21','U22','U23','U24','U25','R3','R4','C2'}
    components={c.get('ref'):{'value':c.findtext('value'),'pins':{}} for c in netlist.find('components') if c.get('ref') in selected}
    for net in netlist.find('nets'):
        for node in net.findall('node'):
            if node.get('ref') in components:
                components[node.get('ref')]['pins'][node.get('pin')]=net.get('name')
    excerpts=[]
    for path,needle,count in [('firmware/app/main/board.c','double board_effective_feedback',6),
                              ('firmware/app/main/board.c','esp_err_t board_configure',21),
                              ('firmware/app/main/main.c','Console accepts only STOP',6)]:
        lines=(release/path).read_text().splitlines()
        start=next(i for i,s in enumerate(lines) if needle in s)
        excerpts.append(dict(source=path,first_line=start+1,lines=lines[start:start+count],
                             sha256=hashlib.sha256((release/path).read_bytes()).hexdigest()))
    (out/'implementation-excerpts.json').write_text(json.dumps(dict(scope='Selected connectivity and source text; no physical measurement.',
        pcb_sha256=SHA,components=components,firmware_excerpts=excerpts),indent=2,ensure_ascii=False)+'\n')
    entries=[]
    for k,(title,path) in SOURCES.items():
        item=dict(id=k,title=title,source=path)
        if not path.startswith('https://'):
            item['sha256']=hashlib.sha256((release/path).read_bytes()).hexdigest()
            item['availability']='Release file identified by basename/relative path and hash; full source is not republished by this documentation update.'
        entries.append(item)
    for path in ['firmware/app/main/board.c','firmware/precision.c','verification/ADG704_SUBSTITUTION_DESIGN_REVIEW.json','verification/GROUND_REFERENCE_REVIEW.json','verification/USB_CONTROLLED_PAIR_REVIEW.json']:
        entries.append(dict(id='SUPPORT'+str(len(entries)),title=Path(path).name,source=path,sha256=hashlib.sha256((release/path).read_bytes()).hexdigest()))
    (out/'source-inventory.json').write_text(json.dumps(entries,indent=2,ensure_ascii=False)+'\n')
    source_table=md_table(['ID','Source and scope'],[[x['id'],f"[{x['title']}]({x['source']})" if x['source'].startswith('https://') else f"{x['title']}: `{x['source']}`; SHA-256 `{x['sha256']}`"] for x in entries])
    (out/'README.md').write_text('# STK RevM20 evidence index\n\nThe released PCB is bound to SHA-256 `' + SHA + '`. The [review summary](review-summary.json) extracts existing audit results and ignored check classes. [Selected implementation excerpts](implementation-excerpts.json) retain actual component pin nets and source lines for feedback gain, global isolation and configuration behavior. Source-reviewed implementation, manufacturer specifications, calculations and future physical tests remain distinct. Full CAD/firmware is not part of this documentation publication.\n\n'+source_table+'\nManufacturer limits apply only under each datasheet condition. The PNAS result supports a chemical-crosstalk mechanism and a specific flow experiment; it is not a performance measurement of this board.\n')


def write_overview(d):
    (ROOT/'README.md').write_text('''# STK RevM20 electrochemical hardware design

RevM20 is a compact four-layer FPC instrument design for simultaneous three-channel chronoamperometry and pH sensing in a shared electrochemical cell. It uses discrete continuous TIAs, a simultaneous current ADC and a separate selected-channel voltage path for experimental EIS.

**Stage:** CAD and source review completed; manufacturer CAM/placement acceptance and physical characterization pending. No RevM20 measured current accuracy, noise floor, EIS phase accuracy or battery lifetime is claimed.

## Engineering records

- [Requirements and implementation baseline](requirements.md)
- [Preliminary error budget and reproducible calculations](error-budget.md)
- [Validation matrix and measurement record requirements](validation.md)
- [Design evidence and release hashes](evidence/README.md)
- [한국어 요약](README.ko.md)

The website case study and these tables share the same generated dataset. Accuracy targets marked TBD require an explicit requirement before a physical result can receive a qualification pass.

## System architecture

```mermaid
flowchart LR
  CELL[Shared electrolyte: WE1..3, pH, RE, CE]
  CELL --> SW[Global cell isolation]
  SW --> TIA[OPA2320 continuous TIAs]
  MUX[ADG704 feedback range per TIA] --- TIA
  TIA --> DIV[0.5 differential conditioning]
  CELL --> PH[OPA391 pH buffer]
  PH --> DIV
  DIV --> ADC[ADS131M04 simultaneous ADC]
  ADC --> MCU[ESP32-S3 / USB Serial]
  MCU --> DAC[DAC80508 setpoints]
  DAC --> TIA
  CELL --> RE[OPA391 reference buffer]
  RE --> CE[Shared OPA2320 CE loop]
  CE --> CELL
  CELL --> VB[Buffered electrode voltages]
  VB --> VADC[ADS124S06 selected voltage: EIS only in FW18]
  VADC --> MCU
```

## Design decisions and their consequences

**Continuous paths and shared electrodes.** Separate TIAs and a simultaneous ADC support same-time current acquisition. A shared RE/CE reduces electrode connections, while retaining common-cell electrical and chemical coupling. Global CELL_EN also means independent live per-WE disconnect is outside this revision's scope. The validation matrix separates these limitations from measurable transfer/noise performance.

**A procurement-driven switch substitution.** U21-U24 use ADG704BRMZ-REEL7 in place of unavailable TMUX1104DGSR. Pin mapping, truth table, logic thresholds and control-rail behavior were reviewed. On-resistance, leakage, capacitance and charge injection change the precision and settling problem; per-range calibration and physical residual characterization remain required.

**Compact flex with manufacturing constraints.** The nominal41.8x42.5mm,0.20mm four-layer board has196 fitted parts on both faces. Connected GND/power routing, coverlay/paste geometry and BOM/CPL alignment were audited. Assembly fixtures, reflow sequence, placement acceptance, USB retention and populated-area support remain manufacturing/mechanical work. A flexible board does not establish stretchable-system performance.

## Current evidence boundary

The release records0 DRC errors,0 warnings and0 unconnected items under its enabled rules,0 ERC violations and matching202 component references/687 physical pads. Ignored check classes are retained in the evidence summary. These are CAD outcomes. The physical tests in the matrix are NOT_RUN, and quantities without measurements use null values.

Default operation is3CA+pH. Four-current operation requires unpowered physical selector changes. The implemented firmware does not provide CV/DPV, wireless telemetry, automatic battery charging policy or qualified EIS accuracy. Historical AD5941 results on the personal site belong to the earlier architecture.

## Reproduce the documentation

The portable calculations require only Python3:

```bash
python3 docs/projects/stk-revm20/tools/build.py --check
```

To regenerate the hash-bound source index and pages from the matching private release, use `--release /path/to/release`. The script refuses a mismatched PCB hash. Website and Markdown tables are generated from one baseline. The full board source and procurement/account information are outside this publication.
''')
    (ROOT/'README.ko.md').write_text('''# STK RevM20 하드웨어 포트폴리오

현재 설계는 공통 RE/CE에서3개 전류 채널과pH를 동시에 기록하는4층 FPC 시제품이다. RevM20의 실측 정확도·잡음·검출한계·EIS 위상·배터리 수명은 아직 측정하지 않았다.

## 세 가지 표

- [요구사양표](requirements.md): 현재 구현 기준과 미정 성능 목표를 구분한다. 펌웨어 명령 범위와 보호 제한은 실제 달성 범위·정확도 보증이 아니다.
- [오차 예산표](error-budget.md): 저항 허용오차, 스위치 누설·온저항, TIA 오프셋, 분압 불일치, ADC/DAC, 공통 기준전압, 용액 저항을 분리한다. 미확정 항목은0으로 합산하지 않는다.
- [검증 항목표](validation.md): 기존 CAD 감사 검토와 앞으로 수행할 물리 시험을 구분한다. 요구사양 ID와 시험 ID가 서로 연결된다.

## 상태 표기

CAD_CONFIRMED는 CAD/감사 자료에서 확인, FW_CONFIRMED는 코드 검토로 확인, CALCULATED는 명시된 모델의 계산, DATASHEET는 제조사 지정 조건의 부품 사양이다. BENCH_PENDING은 실측 대기, MANUFACTURER_PENDING은 제조사 검토 대기, UNSPECIFIED는 수치 기준 미정이다. 제조사 승인이나 실물 성능을 대신하지 않는다.

## 강조할 설계 판단

연속 TIA와 동시 ADC, 공통 RE/CE의 결합과 개별 차단 제약, 재고 부족에 따른 ADG704 교체의 정밀도 영향, 양면 FPC의 전원·GND·제조 제약을 설명한다. 다음 단계에서는 수치화된 최소 전류·허용 오차·환경 조건을 정하고, 효소 없는 부하 시험과 단일 분석물 첨가 시험을 분리해 검증한다.

프로젝트 기여 범위는 실제 담당한 요구사항 정의·회로 판단·CAD·펌웨어·시험 작업에 맞춰 설명한다. 자동화/AI를 사용한 검토와 본인이 직접 수행한 계측·판단을 구분하며, 아직 수행하지 않은 시험을 완료했다고 기재하지 않는다.
''')


def write_site(d, tables):
    req,budget,val,ranges=tables
    asset=SITE/'assets/projects/stk-revm20'
    asset.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'data/baseline.json',asset/'baseline.json')
    for name in ['requirements.md','error-budget.md','validation.md']:
        shutil.copy2(ROOT/name,asset/name)
    def wrap(text):
        return '<div class="table-responsive" markdown="1">\n\n'+text+'\n</div>\n'
    page='''---
layout: page
title: STK RevM20 electrochemical hardware
description: Simultaneous 3CA and pH on a four-layer FPC, with a traceable requirements baseline, preliminary error budget and validation plan
permalink: /projects/stk-revm20/
img: assets/projects/stk-revm20/architecture.svg
importance: 0
category: engineering
related_publications: false
toc:
  sidebar: left
---

**RevM20 / FW18 · Design baseline as of 15 October 2026**

This instrument design records three electrochemical current channels and pH simultaneously in a shared cell. Its continuous TIAs and simultaneous ADC support same-time acquisition; a common RE/CE retains electrical and chemical coupling that must be characterized.

> **Current stage:** CAD/source review and manufacturing-file preparation. Factory CAM/placement acceptance and physical characterization are pending. Current accuracy, noise floor, EIS phase accuracy and battery lifetime are not measured results.

<p><a class="btn btn-sm btn-outline-primary" href="DOC_URL">GitHub engineering records</a> <a class="btn btn-sm btn-outline-primary" href="ASSET/baseline.json">Download data</a> <a class="btn btn-sm btn-outline-primary" href="DOC_URL/README.ko.md">한국어 요약</a></p>

## Architecture and design choices

<img src="ASSET/architecture.svg" alt="RevM20 architecture: shared RE and CE, continuous TIAs, simultaneous current ADC and selected-channel EIS voltage ADC" class="img-fluid rounded" loading="lazy">

The default physical links implement **3CA+pH**. Four-current mode requires selector changes with power removed. The41.8×42.5mm board uses four copper layers and nominal0.20mm FPC with196 fitted components on both sides.

**Acquisition architecture.** Each current channel has an OPA2320 TIA. ADG704 switches select feedback ranges within each TIA; they do not multiplex a single current amplifier between electrodes. The ADS131M04 samples four conversion channels simultaneously. The ADS124S06 voltage path serves a selected EIS channel in current firmware.

**Procurement and precision.** Replacing the unavailable TMUX1104 with ADG704 preserved the reviewed pin mapping and control truth table. Leakage, on-resistance, charge injection and capacitance remain explicit error/settling contributors. Per-range calibration is an interface ready for physical characterization, not an already achieved accuracy result.

**Shared-cell limits.** One RE/CE pair and global CELL_EN keep the topology compact. One channel's reaction can still affect others through solution impedance or transported products. Live per-channel disconnect and live range/bias changes are outside FW18's implemented behavior.

**Manufacturing and mechanics.** Hash-bound CAD audits cover connectivity, enabled design rules, coverlay/paste geometry and BOM/placement parity. Factory approval, FPC fixtures/reflow, USB shell retention and populated-area support remain separate gates. FPC bendability does not demonstrate stretchability.

## Evidence labels

LEGEND

**Validation status:** 22 physical test groups have not been run; one manufacturer review gate awaits disposition. Two rows below review existing CAD audits. No numerical pass is assigned while its acceptance threshold is TBD.

## Requirements and implementation baseline

The table records the current implementation. Minimum quantitative current, absolute accuracy, environmental limits and lifetime still need numerical requirements.

REQ

## Preliminary error budget

Separate bounded offsets, multiplicative gain errors, typical noise and correlated reference terms. Unknown post-calibration residuals remain unknown; there is no justified total accuracy or detection limit yet.

BUDGET

### Reproducible range calculations

The DC model is the parallel combination of(Rselected+3ohm) and10Mohm. Passive-resistor and Ron bounds vary different inputs separately. The resistor-noise estimate assumes25C and an ideal DC feedback resistance; ADC code steps are not measured resolution.

RANGES

A hypothetical1nA signal at1% error permits10pA total error. That is an illustrative requirement, not this board's achieved specification. The ADG704 specified100pA terminal leakage limit makes actual leakage and calibration residual characterization essential for such a target.

## Validation matrix

Begin with assembly/link inspection and USB-only power-up. Proceed through dummy-cell transfer/stability, noise and electrical coupling before enzyme controls. Each measurement must retain board/FW identity, configuration, calibration fingerprint, environment, instruments, uncertainty and raw data.

VAL

## Engineering records and next measurements

The release records0 DRC errors,0 warnings,0 unconnected items and0 ERC violations under its configured checks, with202 references and687 pads checked for schematic parity. The [evidence summary](DOC_URL/evidence) retains ignored rule classes and source hashes. These are CAD outcomes.

The next quantitative milestone is an independently validated DC current/voltage transfer and noise/crosstalk characterization across the declared operating conditions. EIS remains labeled EIS_ACTUAL_UNVERIFIED. Sample temperature is manual input; battery NTC is not sample-temperature measurement.

The [earlier AD5941 toolkit](/projects/5_project/) uses a different front end and MCU. Its historical mode/status claims do not establish RevM20 performance.

Full tables: [requirements](ASSET/requirements.md), [error budget](ASSET/error-budget.md), [validation](ASSET/validation.md). The [GitHub source index](DOC_URL/evidence/README.md) links manufacturer datasheets and identifies the matching release artifacts.
'''
    page=page.replace('DOC_URL',DOC_URL).replace('ASSET',ASSET).replace('LEGEND',LEGEND).replace('REQ\n',wrap(req)).replace('BUDGET\n',wrap(budget)).replace('RANGES\n',wrap(ranges)).replace('VAL\n',wrap(val))
    (SITE/'_projects/stk-revm20.md').write_text(page)


def check(d):
    ids={r['id'] for r in d['requirements']};vids={r['id'] for r in d['validation']}
    assert len(ids)==len(d['requirements']) and len(vids)==len(d['validation'])
    for row in d['requirements']+d['error_budget']:
        assert set(row['validation_ids'])<=vids
        assert set(row['sources'])<=set(SOURCES)
    for row in d['validation']:
        assert set(row['requirement_ids'])<=ids
        if row['evidence_status']=='BENCH_PENDING':
            assert row['execution_status']=='NOT_RUN' and row['result'] is None
        assert row['measurement_file'] is None and row['instrument_uncertainty'] is None
    c=d['calculations'];assert math.isclose(c['DAC_LSB_uV'],76.2939453125)
    assert math.isclose(c['ranges'][-1]['model_Rf_ohm'],909093.3884290758,rel_tol=1e-9)
    assert math.isclose(c['ranges'][-1]['divider_zero_example_nA'],1.099997000009,rel_tol=1e-8)
    assert math.isclose(c['required_error_pA_example'],10)
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix in ['.json','.md']:
            assert not re.search(r'/(?:Users|home)/[^/\s]+/',p.read_text()),f'Private absolute path in {p.name}'
    print(json.dumps(dict(requirements=len(ids),error_budget_terms=len(d['error_budget']),validation_groups=len(vids),
                          audit_reviews=sum(r['execution_status']=='AUDIT_REVIEWED' for r in d['validation']),
                          physical_tests_run=0,physical_groups_not_run=sum(r['execution_status']=='NOT_RUN' for r in d['validation']),
                          arithmetic_and_links='pass',pcb_sha256=d['pcb_sha256'])))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--release',type=Path);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    if args.release:
        actual=hashlib.sha256((args.release/'hardware/STK_4WE_RevM20_USB_C_4L_FPC.kicad_pcb').read_bytes()).hexdigest()
        if actual!=SHA:raise SystemExit('Release PCB hash mismatch; refuse baseline generation.')
        snapshot_evidence(args.release)
    d=clean_values(dict(schema_version=1,as_of=DATE,hardware='RevM20',firmware='FW18',pcb_sha256=SHA,
           physical_measurements_available=False,requirements=requirements(),error_budget=budget_rows(calculations()),
           calculations=calculations(),validation=validations()))
    if args.check and not args.release:
        stored=json.loads((ROOT/'data/baseline.json').read_text())
        assert stored==d,'Generated baseline differs from stored data; regenerate intentionally.'
        check(stored);return
    tables=write_docs(d);write_overview(d);write_site(d,tables)
    for p in list(ROOT.glob('*.md')) + list((SITE/'assets/projects/stk-revm20').glob('*.md')) + [SITE/'_projects/stk-revm20.md']:
        p.write_text(clean_text(p.read_text()))
    check(d)


if __name__=='__main__':
    main()
