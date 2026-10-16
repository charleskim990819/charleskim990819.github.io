# STK RevM20 evidence index

The released PCB is bound to SHA-256 `f2e3c2a2f3499b0fdad05f8f8aaffb69c3773540706764b1e55289f653d65690`. The [review summary](review-summary.json) extracts existing audit results and ignored check classes. [Selected implementation excerpts](implementation-excerpts.json) retain actual component pin nets and source lines for feedback gain, global isolation and configuration behavior. Source-reviewed implementation, manufacturer specifications, calculations and future physical tests remain distinct. Full CAD/firmware is not part of this documentation publication.

| ID        | Source and scope                                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| REL       | Released design manifest: `MANIFEST.json`; SHA-256 `c3c080b57788203a0d1d1e0c46e68fea45692b630b7890a2898d2d1708f5c3a3`                                                     |
| NET       | Released schematic connectivity: `verification/SCHEMATIC_NETLIST.xml`; SHA-256 `0eb789de739bfbf4f6ab0ecaf17356a15fcdcbd9fc091e97adf41fe482555008`                         |
| BOM       | Released fitted BOM: `STK_4WE_RevM20_USB_C_BOM.csv`; SHA-256 `aded882e773934cb038e9b1e7784018e93dbd65b56a9d3c249849e61f3f302d6`                                           |
| BRIDGE    | Factory PH link audit: `verification/FINAL_BRIDGES.json`; SHA-256 `9c986ea71996d4e9e6ea9146802f1d58d5ab7e4ac1f57410231c607c19475605`                                      |
| DRC       | Final DRC and ignored checks: `verification/FINAL_DRC.json`; SHA-256 `724768297e5f181eb3162618a18cb6d08062eac49452c4173adffdf447222c86`                                   |
| ERC       | Final ERC and ignored checks: `verification/FINAL_ERC.json`; SHA-256 `4a891d2840bac333cbce5800dd54e2b5c4a8995c11798de19a5d63340f4e154e`                                   |
| PARITY    | Schematic to physical pad parity: `verification/PCB_SCHEMATIC_NET_PARITY.json`; SHA-256 `273811e1f6fee47a1252bcfc1d8e336342f1c804d77a6aad7603cad97b28a819`                |
| CSV       | BOM and placement parity: `verification/FINAL_CSV_PART_PARITY.json`; SHA-256 `42f93fa0a6c792dc101267155d340462f22ffe32755ee5f1a9e578516316d7c8`                           |
| CAM       | Nominal Gerber geometry checks: `verification/FINAL_CAM.json`; SHA-256 `2642a704df2a5c91114f6bcb9b85490ca5b07a6fc45d5bff3950fcf9d30cd8d0`                                 |
| GEOM      | Native board dimensions: `verification/RELEASE_NATIVE_INSPECTION.json`; SHA-256 `84809482bf85410064530eaaf185b6a9f9208c3cd857b34e50762e624bf2cd46`                        |
| USB       | USB geometry and reference audit: `verification/USB_CONTROLLED_PAIR_REVIEW.json`; SHA-256 `86fce5d20ebc781757f77c08494d37c337c4987d79ff6b89421989b9b937deaf`              |
| FW        | FW18 acquisition and calibration source: `firmware/app/main/main.c`; SHA-256 `9be690803e2dce803c0e65ec6bc4948f5388a79e18685c64405594ecf20054f0`                           |
| DACDOC    | WE command calibration procedure: `firmware/app/DAC_CALIBRATION.txt`; SHA-256 `b6cef2babc4a26466371d7eafb5bc8e80a1e6780b75c1abea3aeb27496fe9dbe`                          |
| EISDOC    | Actual-voltage EIS calibration procedure: `firmware/app/ACTUAL_EIS_CALIBRATION.txt`; SHA-256 `699cdd0cc7dad600d738beb5e59b3fc8f454e15b6d3cd03c15c84c645634b184`           |
| ADG       | [ADI ADG704 RevA pp2-3](https://www.analog.com/media/en/technical-documentation/data-sheets/ADG704.pdf)                                                                   |
| OPA       | [TI OPA2320 RevF electrical table](https://www.ti.com/lit/ds/symlink/opa320.pdf)                                                                                          |
| ADS       | [TI ADS131M04 RevD](https://www.ti.com/lit/ds/symlink/ads131m04.pdf)                                                                                                      |
| DAC       | [TI DAC80508 RevD](https://www.ti.com/lit/ds/symlink/dac80508.pdf)                                                                                                        |
| TMUX      | [TI TMUX111x RevC 5V electrical table](https://www.ti.com/lit/ds/symlink/tmux1111.pdf)                                                                                    |
| PH        | [TI OPA391 RevE](https://www.ti.com/lit/ds/symlink/opa391.pdf)                                                                                                            |
| BQ        | [TI BQ25180](https://www.ti.com/lit/ds/symlink/bq25180.pdf)                                                                                                               |
| PNAS      | [Chae etal PNAS2023](https://doi.org/10.1073/pnas.2219231120)                                                                                                             |
| SUPPORT22 | board.c: `firmware/app/main/board.c`; SHA-256 `910f0d1c28568f9e4df300e05dceb390ec744c640133f09ffeefbd1904d455d2`                                                          |
| SUPPORT23 | precision.c: `firmware/precision.c`; SHA-256 `616b7186038e292c22e31bc9fd5c81a7ec51fcf6147c366864effcd7dfe51af4`                                                           |
| SUPPORT24 | ADG704_SUBSTITUTION_DESIGN_REVIEW.json: `verification/ADG704_SUBSTITUTION_DESIGN_REVIEW.json`; SHA-256 `175bdd9d54b3b2d563447c41cffc971ccd2af0a7a5dd20e71a9bc340c0325387` |
| SUPPORT25 | GROUND_REFERENCE_REVIEW.json: `verification/GROUND_REFERENCE_REVIEW.json`; SHA-256 `2536aac9c36cc515387595ec62b67f435660fc18091f6986a486de40ff113330`                     |
| SUPPORT26 | USB_CONTROLLED_PAIR_REVIEW.json: `verification/USB_CONTROLLED_PAIR_REVIEW.json`; SHA-256 `86fce5d20ebc781757f77c08494d37c337c4987d79ff6b89421989b9b937deaf`               |

Manufacturer limits apply only under each datasheet condition. The PNAS result supports a chemical-crosstalk mechanism and a specific flow experiment; it is not a performance measurement of this board.
