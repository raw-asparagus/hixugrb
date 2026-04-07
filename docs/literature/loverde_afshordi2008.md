# LoVerde & Afshordi (2008) — Extended Limber Approximation

**Authors:** M. LoVerde, N. Afshordi
**Journal:** JCAP 2008(08), 005
**arXiv:** [0809.5112](https://arxiv.org/abs/0809.5112)

## Abstract

Develops a systematic series expansion for the Limber approximation to the angular cross-power spectrum of two random fields, in powers of $(\ell + 1/2)^{-1}$. Shows that the standard (0th-order) Limber approximation has error $\mathcal{O}(\ell^{-2})$, and provides a closed-form 2nd-order correction that improves accuracy to $\mathcal{O}(\ell^{-4})$.

## Key Results

### Improved $k$-substitution

The paper demonstrates that the correct replacement in the Limber integral is

$$k = \frac{\ell + 1/2}{\chi}$$

rather than the naive $k = \ell/\chi$ commonly used in the literature. Using $\ell$ instead of $\ell + 1/2$ degrades the approximation error from $\mathcal{O}(\ell^{-2})$ to $\mathcal{O}(\ell^{-1})$ — a significant loss of accuracy at low multipoles.

### 2nd-order correction (Eq. 13)

$$C_{AB}(\ell) = \int \frac{dk}{k}\, P_{AB}(k)\, f_A(r)\, f_B(r) \left\{1 + \frac{\nu^{-2}}{2}\left[\frac{d\ln f_A}{d\ln r}\frac{d\ln f_B}{d\ln r} \cdot s(k) - p(k)\right] + \mathcal{O}(\nu^{-4})\right\}$$

where $\nu = \ell + 1/2$ and $s(k)$, $p(k)$ encode the spectral slope and curvature of the power spectrum.

### Practical accuracy guideline

For a projection kernel of width $\sigma_r$ centered at comoving distance $r_0$, the 0th-order Limber formula is accurate to $\sim 1\%$ when $\ell \gtrsim 5\, r_0 / \sigma_r$.

## Repository Use

Used by the repository as the justification for the improved Limber $k$-substitution $k = (\ell + 1/2)/\chi$ in `angular_power.py`, documented as deliberate deviation D8 from the thesis (which uses $k = \ell/\chi$). Effect is $\sim 5\%$ at $\ell = 10$, negligible at $\ell > 100$.
