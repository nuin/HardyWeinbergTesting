"""Text and JSON output formatting for HW test results."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from hwtest.models import MultiAlleleResults, TestResult, TwoAlleleResults


def format_p_value(p: float | None) -> str:
    """Format p-value matching the original program's display logic."""
    if p is None:
        return "   -"
    if p >= 1e-4:
        return f" = {p:.4f}"
    if p >= 1e-5:
        return " < 10^-4"
    if p >= 1e-6:
        return " < 10^-5"
    return " < 10^-6"


def format_two_allele_text(results: TwoAlleleResults) -> str:
    """Format two-allele results as text, matching original output."""
    data = results.input_data
    d, h, r, n = data.d, data.h, data.r, data.n
    ef = results.expected_frequencies
    de0, he0, re0 = ef.no_correction
    de1, he1, re1 = ef.hogben_levene
    de2, he2, re2 = ef.cannings_edwards

    lines: list[str] = []
    lines.append("")
    lines.append("                       HARDY-WEINBERG TESTING")
    lines.append("")
    lines.append("                       Copyright 2006-2019 by")
    lines.append("      Fernando A. Bautzer Santos, Renan B. Lemes & Paulo A. Otto")
    lines.append("            Departamento de Genetica e Biologia Evolutiva")
    lines.append("                     Universidade de Sao Paulo")
    lines.append("                         Rua do Matao, 277")
    lines.append("                   05508-090 Sao Paulo SP, Brazil")
    lines.append("                            otto@usp.br")
    lines.append("")
    lines.append("                                        AA         Aa         aa          N")
    lines.append("---------------------------------------------------------------------------")
    lines.append(
        f"obs. abs. frequencies                 {d:4d}       {h:4d}       {r:4d}       {n:4d}"
    )
    lines.append(
        f"exp. abs. freq. (without correction)  {de0:8.3f}   {he0:8.3f}   {re0:8.3f}   {n:4d}"
    )
    lines.append(
        f"exp. abs. freq. (Hogben/Levene)       {de1:8.3f}   {he1:8.3f}   {re1:8.3f}   {n:4d}"
    )
    lines.append(
        f"exp. abs. freq. (Cannings & Edwards)  {de2:8.3f}   {he2:8.3f}   {re2:8.3f}   {n:4d}"
    )
    lines.append("---------------------------------------------------------------------------")
    lines.append(
        f"obs. rel. frequencies                 {d/n:8.3f}   {h/n:8.3f}   {r/n:8.3f}      -"
    )
    lines.append(
        f"exp. rel. freq. (without correction)  {de0/n:8.3f}   {he0/n:8.3f}   {re0/n:8.3f}      -"
    )
    lines.append(
        f"exp. rel. freq. (Hogben/Levene)       {de1/n:8.3f}   {he1/n:8.3f}   {re1/n:8.3f}      -"
    )
    lines.append(
        f"exp. rel. freq. (Cannings & Edwards)  {de2/n:8.3f}   {he2/n:8.3f}   {re2/n:8.3f}      -"
    )
    lines.append("---------------------------------------------------------------------------")
    lines.append("")
    lines.append(f"p = P(A) = {results.p_freq:8.4f}")
    lines.append(f"q = P(a) = {results.q_freq:8.4f}")
    lines.append(f"H0:{{d,h,r}}        s.e.(p) = s.e.(q) = {results.se_h0:8.4f}")
    lines.append(f"Ha:{{p^2,2pq,q^2}}  s.e.(p) = s.e.(q) = {results.se_h1:8.4f}")
    lines.append("")

    for tr in results.test_results:
        lines.append(f"P({tr.label}){format_p_value(tr.p_value)}")

    if results.bootstrap is not None:
        bs = results.bootstrap
        lines.append("")
        lines.append("'EXACT' BOOTSTRAP (1000 SIMULATIONS) ESTIMATES")
        lines.append("")
        lines.append(f"OBS. SAMPLE p = P(A)  = (2D+H)/2N        = {results.p_freq:.4f}")
        lines.append(f"BOOTSTRAP EST. p                         = {bs.mean_p:.4f}")
        lines.append("")
        lines.append(f"EXACT PROBABILITY (1000 SIMUL.)         {format_p_value(bs.exact_p_value)}")

    return "\n".join(lines)


def format_multi_allele_text(results: MultiAlleleResults) -> str:
    """Format multi-allele results as text."""
    data = results.input_data
    k = data.n_alleles
    n = data.n
    freqs = results.allele_freqs

    lines: list[str] = []
    lines.append("")
    lines.append("                       HARDY-WEINBERG TESTING")
    lines.append("")
    lines.append("----------------------------------------------------------------------------")
    lines.append("                     genotype                         genotype")
    lines.append("               absolute frequencies             relative frequencies")
    lines.append("----------------------------------------------------------------------------")
    lines.append("            observed       expected          observed       expected")
    lines.append("")

    allele_names = "ABCDEFGHIJKLMNO"
    for i in range(k):
        for j in range(i, k):
            label = allele_names[i] + allele_names[j]
            obs = data.genotypes[i][j]
            if i == j:
                exp_val = freqs[i] * freqs[j] * n
                exp_rel = freqs[i] * freqs[j]
            else:
                exp_val = 2 * freqs[i] * freqs[j] * n
                exp_rel = 2 * freqs[i] * freqs[j]
            lines.append(
                f"    {label}        {obs:4d}         {exp_val:8.3f}"
                f"            {obs/n:.3f}          {exp_rel:.3f}"
            )

    lines.append("")
    lines.append("----------------------------------------------------------------------------")
    lines.append(f"    N         {n:4d}")
    lines.append("")
    lines.append("----------------------------------------------------")
    lines.append("            allele     s.e.(pi)       s.e.(pi)    ")
    lines.append("          freq. (pi)  H0:{d,h,r}  H1:{p^2,2pq,q^2}")
    lines.append("")

    for i in range(k):
        lines.append(f"     {allele_names[i]}       {freqs[i]:.3f}")

    lines.append("----------------------------------------------------")
    lines.append("")

    for tr in results.test_results:
        lines.append(f"P({tr.label}){format_p_value(tr.p_value)}")

    return "\n".join(lines)


def results_to_json(results: TwoAlleleResults | MultiAlleleResults) -> str:
    """Convert results to JSON string."""

    def _serialize(obj: Any) -> Any:
        if hasattr(obj, "__dataclass_fields__"):
            return asdict(obj)
        if hasattr(obj, "value"):
            return obj.value
        return str(obj)

    return json.dumps(asdict(results), default=_serialize, indent=2)
