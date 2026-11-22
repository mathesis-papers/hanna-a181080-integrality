# Hanna's conjecture in OEIS A181080, COMMENTS, first line

**Integrality and binomial-power companions** — Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore). Revision 2, 8 November 2026.

## Build

Build `note.tex` with **Tectonic 0.17.0**:

```sh
tectonic note.tex
```

Alternatively, run `pdflatex note.tex` twice. The bibliography is embedded; BibTeX is unnecessary. Required standard packages are `geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `fontenc`, `lmodern` and `hyperref`.

## Results and sources

The note proves the integrality conjecture at [OEIS A181080, NAME and first COMMENTS](https://oeis.org/A181080). Corollaries 6 and 7 prove seven companion integrality assertions and a three-range linear-exponent extension. The eight exponential/logarithmic pairs are:

| Exponential | Logarithmic coefficients |
| --- | --- |
| A181080 | A181081 |
| A181070 | A181071 |
| A166894 | A166895 |
| A181082 | A181083 |
| A181084 | A181085 |
| A181074 | A181075 |
| A181076 | A181077 |
| A181078 | A181079 |

For every pair, the logarithmic sequence is `c(m) = m [x^m] log A(x)`; its terms are integers satisfying the Dold congruences. The A181079 FORMULA sentence naming A181076 has the replacement A181078: their logarithmic coefficients at degree four are respectively 59 and 95. The lower-exponent comparison series specified in the COMMENTS of A181080, A181070 and A181074 are nonintegral, as those entries state; their first nonintegral coefficients occur at degree six and equal `327/2`, `45/2` and `1481/2`.

The coverage table in Section 5 distinguishes the source's conjectures and assertions from consequences not posed there. A166895's separate 2024 asymptotic formula is outside the integrality results. A181072 and A181073, despite variant links, describe unrelated random walks and permutations. All scientific references and their locators appear in the note.

## Written proofs, Lean declarations and finite checks

The all-degree proofs are in the note. At revision `abb48f723fe221da235c625800ba0d2ca1755296`, the common Lean namespace prefix is `D5.S1.Recurrence.Algebraic.`:

- [HannaA181080Integrality.lean](https://github.com/the-omega-institute/trureturing/blob/abb48f723fe221da235c625800ba0d2ca1755296/D5/S1/Recurrence/Algebraic/HannaA181080Integrality.lean): `HannaA181080Integrality.result` proves integrality of the literal A181080 formal exponential in every degree.
- [HannaA181070Integrality.lean](https://github.com/the-omega-institute/trureturing/blob/abb48f723fe221da235c625800ba0d2ca1755296/D5/S1/Recurrence/Algebraic/HannaA181070Integrality.lean): `HannaA181070Integrality.result` proves A181070 integrality. Its `integralGeneric` declaration proves integrality for nonnegative arrays satisfying the two stated divisibility/congruence hypotheses, with a diagonal logarithm; `literalBounded` and `literalUnbounded` identify the coefficient formulas.
- [HannaA181074Integrality.lean](https://github.com/the-omega-institute/trureturing/blob/abb48f723fe221da235c625800ba0d2ca1755296/D5/S1/Recurrence/Algebraic/HannaA181074Integrality.lean): `HannaA181074Integrality.result` proves A181074 integrality for its literal negative-binomial logarithm.

The remaining five exponentials, the eight logarithmic conclusions, the linear-exponent families and the source corrections have the written proofs in Sections 2–5. The scope of the three named `result` declarations is exactly the three entries above.

Python 3.10 or later, without third-party modules, reproduces the finite calculations:

```sh
python3 verify.py > checks-rebuilt.json
cmp checks.json checks-rebuilt.json
```

The default degree is 48; `--degree` accepts 8–96. The supplied output records:

- Differential-recurrence/Euler-product agreement through degree 48 for all eight exponentials, plus direct-exponential agreement through degree 16.
- Eight exact logarithmic-formula comparisons through degree 48, and the fixed OEIS prefixes at indices 0–8.
- 28,800 prime-scaling parameter triples: eight arrays, rows 1–24, columns 0–24, primes 2, 3, 5, 7, 11, 13. The divisibility condition is also tested on these triples.
- 496 Dold congruences with scaled index at most 48, and the three degree-six nonintegrality witnesses.
- 4,914 prime-scaling checks of the linear-exponent extension on `1+t+t^2`, `1+2t+t^3` and `1/(1-t)`, and 21 recurrence/direct-exponential/Euler-product comparisons through degree 12.

Full coefficient vectors and Euler exponents are represented by SHA256 digests of compact JSON lists of exact rational strings. These finite checks are distinct from the all-degree proofs. `manifest.json` gives the SHA256 and size of each other source member.

## License

Copyright 2026 Haobo Ma and Wenlin Zhang. The note, metadata and original accompanying code are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) (`cc-by-4.0`).
