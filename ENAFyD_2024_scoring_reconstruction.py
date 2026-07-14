# =====================================================================
# Reconstruction and validity evaluation of the ENAFyD 2024 physical
# activity index (children/adolescents 5-17 and adults 18+).
#
# Companion code for:
#   "Undocumented scoring rules in national physical activity
#    surveillance of children and adolescents: a full algorithmic
#    reconstruction of the Chilean ENAFyD 2024 index"
#
# Author: Josivaldo de Souza-Lima et al.
# License: MIT
#
# Data are NOT included. The ENAFyD 2024 microdata are administered by
# the Undersecretariat of Sport of Chile; access is subject to the data
# custodian's conditions. Place the .sav files where indicated below.
#
# Environment: Python 3 (pandas, numpy, scipy, pyreadstat). Confirmatory
# steps in the manuscript additionally used R (lavaan/semTools/survey);
# the reconstruction and quantification reported here are pure Python.
# =====================================================================

import pandas as pd
import numpy as np
import itertools
from scipy import stats

# ---- Paths (edit to your environment) -------------------------------
PATH_NNA    = "/content/BASE DE DATOS NNA.sav"
PATH_ADULTS = "/content/BASE DE DATOS ADULTOS.sav"

import pyreadstat


# =====================================================================
# PART A - CHILDREN AND ADOLESCENTS (5-17)
# =====================================================================

def load(path):
    return pyreadstat.read_sav(path, apply_value_formats=False)


# --- BLOCK 1: variable inventory ------------------------------------
def block1_inventory(df, meta):
    inv = pd.DataFrame({"variable": meta.column_names,
                        "etiqueta": [l if l else "" for l in meta.column_labels]})
    print(f"Dimensions: {df.shape[0]} cases x {df.shape[1]} variables")
    return inv


# --- BLOCKS 2-3: context-level reconstruction (NNA) -----------------
NNA_CTX = {"ESC":   ("p31_1", "p32_1", "p33_1", "indice_ESC"),
           "TLIBRE":("p31_2", "p32_2", "p33_2", "indice_TLIBRE"),
           "DOM":   ("p31_3", "p32_3", "p33_3", "indice_DOM"),
           "TRANSP":("p31_4", "p32_4", "p33_4", "ind_TRANSP")}
DIAS = {1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0}
ORD  = {"Inactivo": 0, "Parcialmente Activo": 1, "Activo": 2}


def nna_reconstruct_context(f, m, i, gate_int=True, min60=True):
    """Context classification: days (p31) + >=60 min (p32) + intensity gate (p33)."""
    d = f.map(DIAS)
    ok_min = (m >= 60) if min60 else pd.Series(True, index=f.index)
    ok_int = i.isin([2, 3]) if gate_int else pd.Series(True, index=f.index)
    out = pd.Series("Inactivo", index=f.index, dtype=object)
    out[(d >= 3) & (d <= 6) & ok_min & ok_int] = "Parcialmente Activo"
    out[(d == 7) & ok_min & ok_int] = "Activo"
    out[f.isna()] = np.nan
    return out


def block3_context_concordance(df):
    """Factorial test of context rules; the gate+min60 variant reaches 100%."""
    results = {}
    for name, (pf, pm, pi, pofi) in NNA_CTX.items():
        f, m, i = df[pf], pd.to_numeric(df[pm], errors="coerce"), df[pi]
        ofi = df[pofi]
        row = {}
        for gate, min60 in itertools.product([True, False], repeat=2):
            rec = nna_reconstruct_context(f, m, i, gate, min60)
            mask = ofi.notna() & rec.notna()
            row[f"gate={gate},min60={min60}"] = round((rec[mask] == ofi[mask]).mean() * 100, 2)
        results[name] = row
    return results


# --- BLOCKS 4-5: general index (day accumulation) + missing rule ----
def block4_general_index(df):
    """General index = day accumulation across contexts; requires complete contexts."""
    D = {}
    for n, (pf, pm, pi, _) in NNA_CTX.items():
        d = df[pf].map(DIAS).astype(float)
        ok = (pd.to_numeric(df[pm], errors="coerce") >= 60) & df[pi].isin([2, 3])
        dv = d.where(ok, 0.0)
        dv[df[pf].isna()] = np.nan
        D[n] = dv
    D = pd.DataFrame(D)

    def clasif(dt):
        out = pd.Series("Inactivo", index=dt.index, dtype=object)
        out[(dt >= 3) & (dt < 7)] = "Parcialmente Activo"
        out[dt >= 7] = "Activo"
        out[dt.isna()] = np.nan
        return out

    gen = df["indice_GEN"]
    rec_complete = clasif(D.dropna(how="any").sum(axis=1).reindex(df.index))
    mask = gen.notna() & rec_complete.notna()
    acc = (rec_complete[mask] == gen[mask]).mean() * 100
    return D, acc


def block6_impacts(df):
    """Key quantities reported in Results: accumulation impact, gate impact, inconsistencies."""
    niv = pd.DataFrame({n: df[c[3]].map(ORD) for n, c in NNA_CTX.items()})
    gen = df["indice_GEN"]
    w = df["pond"]

    act = gen.eq("Activo")
    act_sin_ctx = act & (niv.max(axis=1, skipna=True) < 2)
    pct_unw = 100 * act_sin_ctx.sum() / act.sum()
    pct_w = 100 * w[act_sin_ctx].sum() / w[act].sum()

    # hard inconsistencies (types a-c)
    hard = pd.Series(False, index=df.index)
    anyt = pd.Series(False, index=df.index)
    for n, (pf, pm, pi, _) in NNA_CTX.items():
        d = df[pf].map(DIAS); m = pd.to_numeric(df[pm], errors="coerce")
        a = (d > 0) & (m == 0)
        b = (d == 0) & (m > 0)
        c = (d > 0) & (m > 0) & df[pi].eq(4)
        e = (d == 0) & df[pi].isin([1, 2, 3])
        hard |= a | b | c
        anyt |= a | b | c | e
    return {"active_no_context_unweighted": round(pct_unw, 1),
            "active_no_context_weighted": round(pct_w, 1),
            "hard_inconsistency_pct": round(100 * hard.mean(), 1),
            "any_inconsistency_pct": round(100 * anyt.mean(), 1)}


def block7_known_groups(df):
    """Known-groups / convergent validity (Kendall tau-b, unweighted)."""
    gen_ord = df["indice_GEN"].map(ORD)

    def tau(x):
        mask = x.notna() & gen_ord.notna()
        t = stats.kendalltau(x[mask], gen_ord[mask])
        return round(t.statistic, 3), t.pvalue

    p58 = pd.to_numeric(df["p58"], errors="coerce")
    p23 = pd.to_numeric(df["p23"], errors="coerce")
    return {"p58_importance": tau(p58),
            "p23_org_binary": tau(p23.map({1: 1, 2: 0, 3: 0, 4: 0})),
            "p40_workshop_school": tau(pd.to_numeric(df["p40"], errors="coerce").map({2: 0, 1: 1})),
            "p43_workshop_out": tau(pd.to_numeric(df["p43"], errors="coerce").map({2: 0, 1: 1})),
            "p53_sleep_discriminant": tau(pd.to_numeric(df["p53"], errors="coerce").where(lambda s: s.between(1, 5)))}


# =====================================================================
# PART B - ADULTS (18+)  [Supplementary File S1]
# =====================================================================

ADULT_IDX = {"IndiceLAB": 1, "IndiceESC": 2, "IndiceTLibre": 3,
             "IndiceDOM": 4, "IndiceTRANS": 5}
DIAS_A = {1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0, 9: np.nan}


def _norm(s):
    return s.astype(str).str.strip().str.lower().replace({"nan": np.nan})


def adult_reconstruct_context(f, m, i):
    """Adult context rule: days>0 AND minutes>0 AND intensity moderate/vigorous;
    weekly-volume WHO thresholds (150 moderate / 75 vigorous)."""
    d = f.map(DIAS_A)
    vol = d * pd.to_numeric(m, errors="coerce")
    out = pd.Series("inactivo", index=f.index, dtype=object)
    practica = (d > 0) & (pd.to_numeric(m, errors="coerce") > 0) & i.isin([2, 3])
    out[practica] = "parcialmente activo"
    out[practica & i.eq(2) & (vol >= 150)] = "activo"
    out[practica & i.eq(3) & (vol >= 75)] = "activo"
    out[f.isna()] = np.nan
    out[f.eq(9)] = "inactivo"
    return out


def adult_general_index(df):
    """Adult general index = VOLUME accumulation across contexts with separate
    WHO thresholds (total moderate>=150 OR total vigorous>=75). Reaches 100%."""
    VM, VV, PR = {}, {}, {}
    for idx, k in ADULT_IDX.items():
        d = df[f"p26_{k}"].map(DIAS_A)
        mm = pd.to_numeric(df[f"p27_{k}"], errors="coerce")
        i = df[f"p28_{k}"]
        ok = (d > 0) & (mm > 0) & i.isin([2, 3])
        vol = (d * mm).where(ok, 0.0)
        vol[df[f"p26_{k}"].isna()] = np.nan
        VM[idx] = vol.where(i.eq(2), 0.0).where(~df[f"p26_{k}"].isna(), np.nan)
        VV[idx] = vol.where(i.eq(3), 0.0).where(~df[f"p26_{k}"].isna(), np.nan)
        PR[idx] = ok.astype(float).where(~df[f"p26_{k}"].isna(), np.nan)
    VM, VV, PR = pd.DataFrame(VM), pd.DataFrame(VV), pd.DataFrame(PR)
    tm, tv = VM.sum(axis=1, min_count=1), VV.sum(axis=1, min_count=1)
    alguno = PR.max(axis=1, skipna=True)

    out = pd.Series("inactivo", index=df.index, dtype=object)
    out[alguno.eq(1)] = "parcialmente activo"
    out[((tm >= 150) | (tv >= 75)) & alguno.eq(1)] = "activo"
    out[alguno.isna()] = np.nan

    gen = _norm(df["ÍndiceGEN"])
    mask = gen.notna() & out.notna()
    acc = (out[mask] == gen[mask]).mean() * 100
    return round(acc, 2)


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    # ---- Children/adolescents ----
    df, meta = load(PATH_NNA)
    block1_inventory(df, meta)
    print("\n[NNA] Context concordance (gate+min60 -> 100%):")
    for k, v in block3_context_concordance(df).items():
        print(f"  {k}: {v['gate=True,min60=True']}%")
    _, acc_gen = block4_general_index(df)
    print(f"[NNA] General index (day accumulation, complete cases): {acc_gen:.2f}%")
    print("[NNA] Impacts:", block6_impacts(df))
    print("[NNA] Known groups (tau-b):", block7_known_groups(df))

    # ---- Adults (Supplementary File S1) ----
    dfa, metaa = load(PATH_ADULTS)
    print(f"\n[ADULTS] {dfa.shape[0]} cases")
    acc_ctx = {}
    for idx, k in ADULT_IDX.items():
        rec = adult_reconstruct_context(dfa[f"p26_{k}"], dfa[f"p27_{k}"], dfa[f"p28_{k}"])
        ofi = _norm(dfa[idx])
        mask = ofi.notna() & rec.notna()
        acc_ctx[idx] = round((rec[mask] == ofi[mask]).mean() * 100, 2)
    print("[ADULTS] Context concordance:", acc_ctx)
    print(f"[ADULTS] General index (volume accumulation): {adult_general_index(dfa):.2f}%")
