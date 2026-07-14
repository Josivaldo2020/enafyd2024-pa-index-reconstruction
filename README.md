# ENAFyD 2024 Physical Activity Index — Scoring Reconstruction and Validity Evaluation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21361704.svg)](https://doi.org/10.5281/zenodo.21361704)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)]()

Companion software for the manuscript:

> **Undocumented scoring rules in national physical activity surveillance of children and adolescents: a full algorithmic reconstruction of the Chilean ENAFyD 2024 index.**

---

## Overview

This repository contains the complete reproducible code used to reconstruct, verify and validate the official physical activity index algorithm implemented in Chile's **National Survey of Physical Activity and Sport (ENAFyD 2024)**.

The repository allows researchers to:

- reconstruct the complete child and adolescent scoring algorithm (5–17 years);
- reconstruct the adult scoring algorithm (18+ years);
- quantify the impact of undocumented scoring rules;
- reproduce all analyses presented in the accompanying manuscript.

---

## Repository structure

```
.
├── ENAFyD_2024_scoring_reconstruction.ipynb
├── ENAFyD_2024_scoring_reconstruction.py
├── CITATION.cff
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Main features

✔ Complete reconstruction of the official ENAFyD 2024 algorithm

✔ Case-by-case validation

✔ Independent reconstruction of adult and child modules

✔ Full reproducibility

✔ Open-source implementation

---

## Key reconstructed rules

(Deja exactamente tu texto actual aquí. Está excelente.)

---

## Data availability

(Deja exactamente tu texto.)

---

## Installation

Clone the repository

```bash
git clone https://github.com/Josivaldo2020/enafyd2024-pa-index-reconstruction.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install pandas numpy scipy pyreadstat
```

---

## Running the analyses

After obtaining the ENAFyD 2024 microdata through Chile's Transparency Portal:

1. Download the datasets.

2. Open

```
ENAFyD_2024_scoring_reconstruction.ipynb
```

3. Modify

```
PATH_NNA
PATH_ADULTS
```

4. Run all cells.

---

## Requirements

- Python 3.x

Libraries

- pandas
- numpy
- scipy
- pyreadstat

Additional analyses reported in the manuscript used:

- lavaan (R)
- semTools (R)
- survey (R)

---

## Notes on weighting

(Aquí deja exactamente tu texto.)

---

## Citation

If you use this repository, please cite:

> de Souza-Lima J, et al.

> ENAFyD 2024 Physical Activity Index — Scoring Reconstruction and Validity Evaluation.

Zenodo

https://doi.org/10.5281/zenodo.21361704

---

## Authors

- Josivaldo de Souza-Lima
- Rodrigo Yáñez-Sepúlveda
- Maribel Parra-Saldías
- Daniel Duclos-Bastías
- Andrés Godoy-Cumillaf
- Eugenio Merellano-Navarro
- Claudio Farías-Valenzuela
- Pedro Valdivia-Moral

---

## Related publication

The accompanying manuscript is currently under peer review.

The citation will be updated once published.

---

## License

MIT License

See LICENSE.
