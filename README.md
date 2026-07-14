# ENAFyD 2024 physical activity index — scoring reconstruction and validity evaluation

Companion code for:

> Undocumented scoring rules in national physical activity surveillance of
> children and adolescents: a full algorithmic reconstruction of the Chilean
> ENAFyD 2024 index.

This repository contains the code used to (1) reconstruct and verify, case by
case, the official scoring algorithm of the physical activity index of Chile's
National Survey of Physical Activity and Sport (ENAFyD 2024) for children and
adolescents (5–17 years); (2) quantify the classification impact of the
undocumented scoring rules; and (3) evaluate validity evidence based on
relations to other variables. It also contains the case-level reconstruction of
the **adult module (18+)** reported in Supplementary File S1, which is used for
the cross-module comparison in the paper.

## Contents

- `ENAFyD_2024_scoring_reconstruction.ipynb` — consolidated notebook
  (children/adolescents Blocks 1–8 and the adult-module S1 reconstruction).
- `ENAFyD_2024_scoring_reconstruction.py` — the same code as a plain script.
- `LICENSE` — MIT License.
- `CITATION.cff` — citation metadata.

## Key reconstructed rules

**Children and adolescents (5–17).** Each context (school, leisure, domestic,
transport) is classified from reported frequency (days/week), a ≥60 min/day
threshold, and an intensity gate whereby a self-rating of "light" or "not
applicable" overrides reported volume and classifies the context as Inactive.
The **general index accumulates valid MVPA days across the four contexts** and
applies the 7-day / 3–6-day cut-offs to the sum (100% concordance in complete
cases; 99.85% overall). Missing data follow a dual rule: a structural skip (not
attending school) contributes zero days, whereas genuine item nonresponse
invalidates the general index.

**Adults (18+, Supplementary File S1).** Each context is classified from
days > 0 **and** minutes > 0 **and** intensity moderate/vigorous, with weekly-
volume WHO thresholds. The **general index accumulates weekly volume across
contexts** (total moderate ≥ 150 min **or** total vigorous ≥ 75 min → Active;
100% concordance). This differs from the day-accumulation rule of the child
module — the central cross-module contrast of the paper.

## Data availability

The analyses use anonymised microdata from the *Encuesta Nacional de Actividad Física y Deporte 2024 (ENAFyD 2024)*, Ministerio del Deporte, Gobierno de Chile, obtained through a formal request under Chile's Transparency Law (Law No. 20.285).

The microdata are **not redistributed** in this repository because redistribution is not permitted. Researchers wishing to reproduce the analyses may obtain access by submitting an equivalent request through Chile's Transparency Portal:

https://www.portaltransparencia.cl

After obtaining the datasets, update the `PATH_NNA` and `PATH_ADULTS` variables at the beginning of the notebook or Python script.

The official ENAFyD 2024 executive report is available at:

https://www.mindep.cl/secciones/211

## Requirements

Python 3 with: `pandas`, `numpy`, `scipy`, `pyreadstat`.

```
pip install pandas numpy scipy pyreadstat
```

Confirmatory steps described in the manuscript (CFA-type sensitivity checks)
additionally used R (`lavaan`, `semTools`, `survey`); the reconstruction and the
quantities reported in Results are computed in pure Python.

## Notes on weighting

All prevalence estimates use the official expansion factor (`pond`). Direct
inspection shows the delivered weight takes 16 unique values, constant within
region, in both the child and adult public-use files; consequently association
measures are reported unweighted and design-adjusted variance estimation is not
possible from the public data. See the manuscript for details.

## License

MIT — see `LICENSE`.
