# Cross-Correlating HI 21-cm Intensity Mapping with the Unresolved Gamma-Ray Background for Dark Matter Indirect Detection

The angular cross-power spectrum between neutral hydrogen intensity maps and the unresolved gamma-ray background provides a powerful probe of particle dark matter annihilation, exploiting the fact that HI traces the linear density field while annihilation emission traces the density squared. This formalism, developed primarily by Fornengo & Regis (2014) and extended to the HI × UGRB case by Pinetti, Camera, Fornengo & Regis (2020), combines the Limber-projected angular power spectrum with a halo-model decomposition that naturally separates one-halo and two-halo clustering contributions for fields of different density weighting. The resulting cross-correlation signal depends on a single free parameter—the velocity-averaged annihilation cross section ⟨σv⟩ at fixed dark matter mass—making it an exceptionally clean test. SKA Phase 2 combined with next-generation gamma-ray telescopes can probe thermally produced dark matter up to TeV-scale masses.

---

## Part 1 — Angular power spectrum from spherical harmonic expansion through Limber projection

### Source intensity and spherical harmonic coefficients

The observable intensity of a tracer $i$ along a sky direction $\hat{\mathbf{n}}$ is a line-of-sight integral over comoving distance $\chi$ (Fornengo & Regis Eq. 1):

$$I_i(\hat{\mathbf{n}}) = \int \mathrm{d}\chi\;\tilde{W}_i(\chi)\,g_i(\chi,\hat{\mathbf{n}})$$

where $g_i(\chi,\hat{\mathbf{n}})$ is the three-dimensional source density field and $\tilde{W}_i(\chi)$ is a window function encoding the physics of emission and observation (distance dimming, spectral properties, absorption). A normalized window function is defined as $W_i(\chi) = \langle g_i \rangle \tilde{W}_i(\chi)$ so that the mean intensity is $\langle I_i \rangle = \int \mathrm{d}\chi\;W_i(\chi)$.

The intensity fluctuation $\delta I_i(\hat{\mathbf{n}}) \equiv I_i(\hat{\mathbf{n}}) - \langle I_i \rangle$ is expanded in spherical harmonics (Eq. 2):

$$\delta I_i(\hat{\mathbf{n}}) = \langle I_i \rangle \sum_{\ell m} a_{\ell m}^{(i)}\,Y_{\ell m}(\hat{\mathbf{n}})$$

where the expansion coefficients are $a_{\ell m}^{(i)} = \int \mathrm{d}\Omega\;\delta I_i(\hat{\mathbf{n}})\,Y_{\ell m}^*(\hat{\mathbf{n}})/\langle I_i \rangle$. These coefficients encode all the statistical information of the projected field on the celestial sphere.

### Rayleigh expansion and the exact double-integral expression

To connect the three-dimensional power spectrum to the angular coefficients, one Fourier-transforms the fluctuation field $f_{g_i}(\chi,\hat{\mathbf{n}}) = g_i/\langle g_i \rangle - 1$ and then uses the **Rayleigh expansion** of a plane wave into spherical Bessel functions and spherical harmonics:

$$e^{i\mathbf{k}\cdot\mathbf{x}} = 4\pi \sum_{\ell=0}^{\infty}\sum_{m=-\ell}^{\ell} i^\ell\,j_\ell(kr)\,Y_{\ell m}^*(\hat{\mathbf{k}})\,Y_{\ell m}(\hat{\mathbf{x}})$$

Inserting the Fourier representation of $f_{g_i}$ and applying this expansion yields (Fornengo & Regis Eq. 3):

$$a_{\ell m}^{(i)} = \int \mathrm{d}\chi\;\frac{W_i(\chi)}{\langle I_i \rangle}\int \frac{\mathrm{d}^3k}{(2\pi)^3}\;\tilde{f}_{g_i}(\mathbf{k},\chi)\;4\pi\,i^\ell\,j_\ell(k\chi)\,Y_{\ell m}^*(\hat{\mathbf{k}})$$

The orthogonality of spherical harmonics $\int \mathrm{d}\Omega\;Y_{\ell m}^*(\hat{\mathbf{n}})\,Y_{\ell' m'}(\hat{\mathbf{n}}) = \delta_{\ell\ell'}\delta_{mm'}$ collapses the angular integral over $\hat{\mathbf{n}}$, while the Rayleigh expansion handles the angular integral over $\hat{\mathbf{k}}$.

Forming the angular power spectrum $C_\ell^{(ij)} = \langle a_{\ell m}^{(i)} a_{\ell m}^{(j)*} \rangle$ and using the definition of the three-dimensional power spectrum $\langle \tilde{f}_{g_i}(\mathbf{k})\,\tilde{f}_{g_j}^*(\mathbf{k}')\rangle = (2\pi)^3\delta_D^3(\mathbf{k}-\mathbf{k}')\,P_{ij}(k)$, the exact (pre-Limber) expression becomes:

$$C_\ell^{(ij)} = \frac{2}{\pi}\int_0^\infty k^2\,\mathrm{d}k\;P_{ij}(k)\left[\int \mathrm{d}\chi\;\frac{W_i(\chi)}{\langle I_i \rangle}\,j_\ell(k\chi)\right]\left[\int \mathrm{d}\chi'\;\frac{W_j(\chi')}{\langle I_j \rangle}\,j_\ell(k\chi')\right]$$

This is a triple integral involving products of highly oscillatory spherical Bessel functions, making direct numerical evaluation expensive at large $\ell$.

### The Limber approximation

**Physical justification.** For $\ell \gg 1$, the spherical Bessel function $j_\ell(x)$ is sharply peaked around $x \approx \ell + 1/2$ and oscillates rapidly elsewhere. Consequently, the dominant contribution to the $k$-integral at angular multipole $\ell$ comes from the mode $k \approx (\ell + 1/2)/\chi$. Physically, this reflects the **thin-shell approximation**: at small angular scales ($\theta \sim \pi/\ell$), the dominant correlation signal arises from pairs of points at nearly the same radial distance, with transverse separation dominating over line-of-sight separation. The rapid oscillations of $j_\ell$ beyond its first peak cancel when integrated against smoothly varying window functions.

The mathematical identity underlying the Limber approximation is the closure relation for spherical Bessel functions:

$$\int_0^\infty k^2\,\mathrm{d}k\;j_\ell(k\chi)\,j_\ell(k\chi') = \frac{\pi}{2\chi^2}\,\delta_D(\chi-\chi')$$

Applying this to the double $\chi$-integral collapses it to a **single integral** (Fornengo & Regis Eq. 4, Pinetti et al. Eq. 2.2):

$$\boxed{C_\ell^{(ij)} = \int \frac{\mathrm{d}\chi}{\chi^2}\;\frac{W_i(\chi)\,W_j(\chi)}{\langle I_i \rangle\langle I_j \rangle}\;P_{ij}\!\left(k = \frac{\ell+\tfrac{1}{2}}{\chi},\,\chi\right)}$$

This is the master equation of the entire formalism. The three-dimensional power spectrum $P_{ij}$ is evaluated at $k = \nu/\chi$ where $\nu = \ell + 1/2$. As emphasized by LoVerde & Afshordi (2008), using $\nu = \ell + 1/2$ rather than simply $\ell$ improves accuracy from $\mathcal{O}(1/\ell)$ to $\mathcal{O}(1/\ell^2)$.

**Low-multipole corrections.** At $\ell \lesssim 20\text{--}50$, the Limber approximation introduces percent-level errors that grow at lower $\ell$. LoVerde & Afshordi developed a systematic expansion in powers of $1/\nu^2$:

$$C_\ell = C_\ell^{(0)} + C_\ell^{(2)} + C_\ell^{(4)} + \cdots$$

where $C_\ell^{(0)}$ is the standard Limber result and $C_\ell^{(2)} \propto 1/\nu^2$ involves second derivatives of the integrand with respect to $\chi$. For the multipole range $\ell = 10\text{--}2000$ relevant to the HI × UGRB cross-correlation, the zeroth-order Limber approximation is adequate for $\ell \gtrsim 50$, while the second-order correction suffices down to $\ell \sim 10$ with $\mathcal{O}(1/\ell^4)$ residual error. Modern implementations (e.g., FFTLog-based methods of Fang et al. 2020) can evaluate the exact double integral efficiently, but for the broad window functions entering the gamma-ray and HI signals, the Limber approximation is excellent throughout the range of interest.

---

## Part 2 — Halo model decomposition of the three-dimensional power spectrum

### Density field as a superposition of halo profiles

The foundational ansatz of the halo model, codified in the review by Cooray & Sheth (2002), is that **all dark matter resides in virialized halos**. The total density field is (Fornengo & Regis Eq. 5):

$$g(\mathbf{x}) = \sum_a g(\mathbf{x} - \mathbf{x}_a \,|\, m_a)$$

where $a$ labels individual halos at positions $\mathbf{x}_a$ with masses $m_a$, and $g(\mathbf{x}|m)$ is the density profile of a halo of mass $m$. The statistical properties of the halo population are encoded in the **halo mass function** $\mathrm{d}n/\mathrm{d}m$, giving the comoving number density of halos per unit mass.

### Two-point function decomposition

The two-point correlation function $\xi_{ij}^{(2)}(\mathbf{x},\mathbf{y}) = \langle f_{g_i}(\mathbf{x})\,f_{g_j}(\mathbf{y})\rangle$ naturally splits into contributions from point pairs within the same halo ($a = b$) and pairs in different halos ($a \neq b$) (Fornengo & Regis Eqs. 6–8). Fourier transforming to obtain the power spectrum yields the decomposition (Eq. 10):

$$P_{ij}(k) = P_{ij}^{\mathrm{1h}}(k) + P_{ij}^{\mathrm{2h}}(k)$$

For the different-halo contribution, the spatial correlation between halos of masses $m_1$ and $m_2$ is approximated via linear bias: $\xi_s^{(2)}(m_1, m_2, |\mathbf{x}_i - \mathbf{x}_j|) \approx b_i(m_1)\,b_j(m_2)\,\xi_{\mathrm{lin}}(|\mathbf{x}_i - \mathbf{x}_j|)$, where $b_h(m)$ is the halo bias and $\xi_{\mathrm{lin}}$ is the linear matter correlation function.

### One-halo and two-halo terms

The general expressions are (Fornengo & Regis Eqs. 11–12):

$$\boxed{P_{ij}^{\mathrm{1h}}(k) = \int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;\frac{\tilde{g}_i(k|m)}{\langle g_i \rangle}\;\frac{\tilde{g}_j(k|m)}{\langle g_j \rangle}}$$

$$\boxed{P_{ij}^{\mathrm{2h}}(k) = \left[\int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;b_h(m)\;\frac{\tilde{g}_i(k|m)}{\langle g_i \rangle}\right]\left[\int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;b_h(m)\;\frac{\tilde{g}_j(k|m)}{\langle g_j \rangle}\right]P_{\mathrm{lin}}(k)}$$

where $\tilde{g}(k|m)$ is the Fourier transform of the halo source profile $g(\mathbf{x}|m)$.

**Physical meaning.** The 1-halo term captures correlations between mass elements **within the same halo** and dominates on small scales ($k \gtrsim 1\;h\,\mathrm{Mpc}^{-1}$), where the signal reflects the internal density structure of individual halos. The 2-halo term captures correlations between mass in **different halos** and dominates on large scales ($k \lesssim 0.1\;h\,\mathrm{Mpc}^{-1}$), tracing the linear power spectrum modulated by halo bias. The **transition scale** at $k \sim 0.2\text{--}1\;h\,\mathrm{Mpc}^{-1}$ corresponds roughly to the virial radii of the most abundant massive halos ($M \sim 10^{13}\text{--}10^{14}\,M_\odot$) that dominate the correlation budget.

The mean source density, computed by integrating over all halos (Eq. 13), is $\langle g \rangle = \int \mathrm{d}m\;(\mathrm{d}n/\mathrm{d}m)\int \mathrm{d}^3x\;g(\mathbf{x}|m)$. The **consistency relations** $\int \mathrm{d}m\;(\mathrm{d}n/\mathrm{d}m)(m/\bar{\rho}) = 1$ and $\int \mathrm{d}m\;(\mathrm{d}n/\mathrm{d}m)(m/\bar{\rho})\,b_h(m) = 1$ ensure that $P^{\mathrm{2h}}(k) \to P_{\mathrm{lin}}(k)$ on large scales, recovering linear theory.

### Halo model ingredients

**Halo mass function.** Fornengo & Regis adopt the Sheth-Tormen (1999) / Sheth-Mo-Tormen (2001) mass function based on ellipsoidal collapse. The multiplicity function is:

$$\nu f(\nu) = A\left(1 + (q\nu)^{-p}\right)\sqrt{\frac{q\nu}{2\pi}}\,\exp\!\left(-\frac{q\nu}{2}\right)$$

with $q = 0.707$, $p = 0.3$, and $A \approx 0.3222$ fixed by normalization. Here $\nu = \delta_c^2/\sigma^2(M)$ is the peak height, $\delta_c \approx 1.686$ is the spherical collapse threshold, and $\sigma^2(M,z) = (2\pi^2)^{-1}\int k^2\,P_{\mathrm{lin}}(k,z)\,W^2(kR)\,\mathrm{d}k$ with $W$ the top-hat window at scale $R$ enclosing mass $M$. The parameter $q < 1$ relative to Press-Schechter ($q = 1$) captures the lower effective collapse barrier from triaxial dynamics. This mass function produces **fewer low-mass halos and more high-mass halos** than Press-Schechter, matching N-body simulations much better.

**Halo bias.** The Sheth-Tormen bias from the peak-background split is:

$$b(\nu) = 1 + \frac{q\nu - 1}{\delta_c} + \frac{2p}{\delta_c\left(1 + (q\nu)^p\right)}$$

This follows from recognizing that a long-wavelength perturbation $\epsilon$ modulates the local halo abundance: $\delta n/n = b_L\,\epsilon$, where the Lagrangian bias $b_L$ is obtained by differentiating $\ln[n(M)]$ with respect to $\delta_c$. The Eulerian bias is $b = 1 + b_L$, and the consistency relation $\int b(M)\,f(\nu)\,\mathrm{d}\nu = 1$ is automatically satisfied by construction.

**Density profile and its Fourier transform.** The NFW profile $\rho_{\mathrm{NFW}}(r) = \rho_s/[(r/r_s)(1+r/r_s)^2]$ is adopted, with scale radius $r_s = r_{\mathrm{vir}}/c$ and normalization $\rho_s = M/[4\pi r_s^3 f(c)]$ where $f(c) = \ln(1+c) - c/(1+c)$. The normalized Fourier transform truncated at $r_{\mathrm{vir}}$ admits an analytic expression in terms of sine and cosine integrals:

$$\tilde{u}(k|M) = \frac{1}{f(c)}\Big\{\sin(kr_s)\big[\mathrm{Si}((1{+}c)kr_s) - \mathrm{Si}(kr_s)\big] + \cos(kr_s)\big[\mathrm{Ci}((1{+}c)kr_s) - \mathrm{Ci}(kr_s)\big] - \frac{\sin(ckr_s)}{(1{+}c)kr_s}\Big\}$$

with $\tilde{u}(k\to 0|M) = 1$ by construction. This function drops from unity at low $k$, oscillates around zero at intermediate $k$, and decays at high $k$ with an envelope set by $r_s$.

**Concentration-mass relations.** The concentration parameter $c(M,z)$ is the single most consequential ingredient for dark matter annihilation predictions, since the annihilation luminosity of an NFW halo scales as $L \propto c^3/f(c)^2$. Fornengo & Regis use Muñoz-Cuartas et al. (2011)—a polynomial fit $\log_{10}c_{\mathrm{vir}} = a(z) + b(z)\,\log_{10}(M_h/h^{-1}M_\odot)$ valid for $10^{11}\text{--}10^{15}\;h^{-1}M_\odot$ at $z = 0\text{--}5$—extrapolated to smaller masses following the power-law behavior of Bullock et al. (2001), $c_{\mathrm{vir}} \propto (1+z)^{-1}(M/M_*)^{-0.13}$. The Correa et al. (2015) semi-analytic model, which links concentration to the halo mass accretion history and predicts a slope change at $\sim 10^{11}\,M_\odot$, provides an alternative that extends over a wider dynamic range.

---

## Part 3 — Density versus density-squared fields and their cross-correlation

### Why HI traces density linearly

Neutral hydrogen in the post-reionization universe resides in self-shielded regions within dark matter halos, predominantly in the mass range $\sim 10^8\text{--}10^{12}\,M_\odot$. The HI brightness temperature fluctuation is (Pinetti et al. Eq. 3.5):

$$\bar{T}_b(z) = 180\;\Omega_{\mathrm{HI}}(z)\;h\;\frac{(1+z)^2}{H(z)/H_0}\;\mathrm{mK}$$

On large scales, the HI overdensity is related to the matter overdensity by a **linear bias**: $\delta_{\mathrm{HI}}(\mathbf{x},z) = b_{\mathrm{HI}}(z)\,\delta_m(\mathbf{x},z)$. In the halo model, the HI source field within a halo of mass $M$ is:

$$f_{\mathrm{HI}}^h(k,z|M) = \frac{M_{\mathrm{HI}}(M,z)}{\bar{\rho}_{\mathrm{HI}}(z)}\;\tilde{u}(k|M)$$

where $M_{\mathrm{HI}}(M,z)$ is the HI mass hosted by a halo of total mass $M$, and $\tilde{u}(k|M)$ is the standard normalized NFW Fourier transform. The critical point is that **the HI field involves $\tilde{u}(k|M)$—the Fourier transform of density—weighted linearly by mass**. Consequently, HI power spectra involve only the profile $\tilde{u}$, and on large scales the HI auto-spectrum reduces to $P_{\mathrm{HI}}^{\mathrm{2h}}(k) \propto b_{\mathrm{HI}}^2\,P_{\mathrm{lin}}(k)$.

### Why dark matter annihilation traces density squared

The dark matter annihilation emissivity is proportional to the number density of annihilating pairs: $\varepsilon_{\mathrm{ann}} \propto n_\chi^2 \langle\sigma v\rangle \propto \rho_{\mathrm{DM}}^2$. This quadratic dependence fundamentally changes the halo model structure. The relevant Fourier-space profile becomes:

$$\tilde{v}(k|M) \propto \int \mathrm{d}^3x\;\rho_{\mathrm{NFW}}^2(\mathbf{x}|M)\;e^{i\mathbf{k}\cdot\mathbf{x}}$$

Since $\rho_{\mathrm{NFW}}^2 \propto r^{-2}(1+r/r_s)^{-4}$ is **much more centrally concentrated** than $\rho_{\mathrm{NFW}} \propto r^{-1}(1+r/r_s)^{-2}$, the function $\tilde{v}(k|M)$ falls off significantly more slowly with $k$ than $\tilde{u}(k|M)$. This means that **density-squared fields carry far more small-scale (high-$k$) power**, reflecting the enhanced contribution from the dense cores of halos.

### The three power spectrum types

Fornengo & Regis derive three distinct power spectrum classes that are central to the entire cross-correlation program:

**Auto-correlation $P_{\delta\delta}$ (density × density)** — relevant for lensing, decaying DM, and galaxy clustering (Eqs. 14–15):

$$P_{\delta\delta}^{\mathrm{1h}}(k) = \int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;\left(\frac{m}{\bar{\rho}}\right)^2[\tilde{u}(k|m)]^2 \qquad\qquad P_{\delta\delta}^{\mathrm{2h}}(k) = \left[\int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;b_h(m)\,\frac{m}{\bar{\rho}}\,\tilde{u}(k|m)\right]^2 P_{\mathrm{lin}}(k)$$

Here $\tilde{u}(k|m)$ is the normalised profile Fourier transform with $\tilde{u}(0|m) = 1$. Some references absorb the mass factor into $\tilde{u}$; we keep it explicit for clarity.

**Auto-correlation $P_{\delta^2\delta^2}$ (density² × density²)** — relevant for annihilating DM auto-correlation (Eqs. 21–22):

$$P_{\delta^2\delta^2}^{\mathrm{1h}}(k) = \int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;\frac{[\tilde{v}(k|m)]^2}{\langle\rho^2\rangle^2} \qquad\qquad P_{\delta^2\delta^2}^{\mathrm{2h}}(k) = \left[\int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;\frac{b_h(m)\,\tilde{v}(k|m)}{\langle\rho^2\rangle}\right]^2 P_{\mathrm{lin}}(k)$$

**Cross-correlation $P_{\delta\delta^2}$ (density × density²)** — relevant for gravitational tracer × annihilating DM (Eqs. 28–29):

$$\boxed{P_{\delta\delta^2}^{\mathrm{1h}}(k) = \int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;\frac{m}{\bar{\rho}}\,\tilde{u}(k|m)\;\frac{\tilde{v}(k|m)}{\langle\rho^2\rangle}}$$

$$\boxed{P_{\delta\delta^2}^{\mathrm{2h}}(k) = \left[\int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;b_h(m)\,\frac{m}{\bar{\rho}}\,\tilde{u}(k|m)\right]\left[\int \mathrm{d}m\;\frac{\mathrm{d}n}{\mathrm{d}m}\;\frac{b_h(m)\,\tilde{v}(k|m)}{\langle\rho^2\rangle}\right]P_{\mathrm{lin}}(k)}$$

Note that on the density side, the mass factor $m$ appears explicitly because $\tilde{u}$ is the normalised Fourier transform of the NFW profile ($\tilde{u}(0|m)=1$). On the density-squared side, $\tilde{v}(k|m) = \int \mathrm{d}^3x\;\rho^2(\mathbf{x}|m)\,e^{i\mathbf{k}\cdot\mathbf{x}}$ is the *unnormalised* Fourier transform (with $\tilde{v}(0|m) = \int \mathrm{d}^3x\;\rho^2$), so no additional factor is needed.

The cross-spectrum $P_{\delta\delta^2}$ is the key quantity for the HI × DM annihilation signal: one leg carries $\tilde{u}$ (the linear-density HI side) and the other carries $\tilde{v}$ (the density-squared annihilation side). Because $\tilde{v}$ extends to higher $k$ than $\tilde{u}$, **the 1-halo term of the cross-correlation is dominated by the $\tilde{u}$ cutoff**, giving intermediate small-scale behavior between $P_{\delta\delta}$ and $P_{\delta^2\delta^2}$.

### Mapping to the specific HI × DM and HI × astrophysical cross-correlations

Pinetti et al. (2020) construct the specific cross-correlation signals by specializing the general framework. For HI × DM annihilation (Eqs. 5.1–5.2):

$$C_\ell^{\mathrm{HI}\times\mathrm{DM}}(E) = \int \frac{\mathrm{d}\chi}{\chi^2}\;W_{\mathrm{HI}}(\chi)\;W_\gamma^{\mathrm{DM}}(E,\chi)\;P_{\mathrm{HI}\times\mathrm{DM}}\!\left(k = \frac{\ell+1/2}{\chi},\,\chi\right)$$

with the 3D cross-power decomposed as:

$$P_{\mathrm{HI}\times\mathrm{DM}}^{\mathrm{1h}}(k,z) = \int \mathrm{d}M\;\frac{\mathrm{d}n}{\mathrm{d}M}\;f_{\mathrm{HI}}^h(k|M)\;f_{\mathrm{DM}}^h(k|M)$$

$$P_{\mathrm{HI}\times\mathrm{DM}}^{\mathrm{2h}}(k,z) = \left[\int \mathrm{d}M\;\frac{\mathrm{d}n}{\mathrm{d}M}\;b_h(M)\;f_{\mathrm{HI}}^h(k|M)\right]\left[\int \mathrm{d}M'\;\frac{\mathrm{d}n}{\mathrm{d}M'}\;b_h(M')\;f_{\mathrm{DM}}^h(k|M')\right]P_{\mathrm{lin}}(k)$$

where $f_{\mathrm{HI}}^h \propto M_{\mathrm{HI}}(M)\,\tilde{u}(k|M)/\bar{\rho}_{\mathrm{HI}}$ (linear in the density profile) and $f_{\mathrm{DM}}^h \propto \mathcal{F}[\rho_h^2](k|M)/[\Delta^2(z)\,\bar{\rho}^2]$ (quadratic in the density profile). The 1-halo term probes the internal halo structure where HI gas and dark matter annihilation coexist, while the 2-halo term traces their large-scale cross-clustering.

For HI × astrophysical sources (Eqs. 5.3–5.4), the annihilation profile $f_{\mathrm{DM}}^h$ is replaced by the source profile $f_s^h(z|L) = L/\langle g_s \rangle$, leading to analogous expressions where the gamma-ray side is characterized by luminosity functions rather than density-squared profiles. The total cross-correlation signal is the sum: $C_\ell^{\mathrm{HI}\times\gamma} = C_\ell^{\mathrm{HI}\times\mathrm{DM}} + \sum_s C_\ell^{\mathrm{HI}\times s}$, where $s$ runs over BL Lacs, FSRQs, misaligned AGN, and star-forming galaxies.

---

## Part 4 — Clumping factor and substructure boost

### The clumping factor Δ²(z)

The clumping factor quantifies the enhancement of the mean annihilation rate due to the inhomogeneous dark matter distribution (Fornengo & Regis Eq. 37, Pinetti et al. Eq. 4.2):

$$\boxed{\Delta^2(z) \equiv \frac{\langle\rho^2(z)\rangle}{\bar{\rho}^2} = \frac{1}{\bar{\rho}^2}\int \mathrm{d}M\;\frac{\mathrm{d}n}{\mathrm{d}M}\int \mathrm{d}^3x\;\rho^2(\mathbf{x}|M,z)}$$

The integral over the squared NFW profile yields $\int_0^{r_{\mathrm{vir}}} 4\pi r^2\,\rho_{\mathrm{NFW}}^2(r)\,\mathrm{d}r = (4\pi/3)\,\rho_s^2\,r_s^3\,[1 - (1+c)^{-3}]$, which scales as $c^3$ at leading order. Since the mass integral is dominated by halos in the range $10^{10}\text{--}10^{14}\,M_\odot$ that are both abundant and concentrated enough to contribute substantially, the clumping factor grows dramatically with decreasing redshift as structure forms. Typical values span $\Delta^2(z=0) \sim 10^4\text{--}10^7$, with the enormous range reflecting uncertainty in the minimum halo mass and substructure treatment.

An equivalent expression using the nonlinear matter power spectrum (Serpico et al. 2012) is $\Delta^2(z) = 1 + (2\pi^2)^{-1}\int \mathrm{d}k\;k^2\,P_{\mathrm{NL}}(k,z)$, which offers a complementary perspective by integrating over all clustering scales without explicitly invoking the halo model.

### Substructure boost factor

Dark matter halos contain copious substructure from hierarchical accretion. Since annihilation scales as $\rho^2$, the clumpy internal mass distribution boosts the total halo luminosity. The **boost factor** $B(M,z)$ is defined as the ratio of subhalo annihilation luminosity to smooth-halo luminosity. Including substructure, the squared density profile is replaced by $[1 + B(\mathbf{x},M,z)]\,\rho^2(\mathbf{x}|M,z)$.

Fornengo & Regis employ the parameterization from Kamionkowski, Koushiappas & Kuhlen (2010), while the updated treatment by **Moliné et al. (2017)** provides a more detailed model calibrated on Via Lactea II and ELVIS simulations. The Moliné et al. prescription accounts for the position-dependent concentration of subhalos—subhalos closer to the host center are more concentrated due to tidal stripping—and yields boost factors **2–3× larger** than the earlier Sánchez-Conde & Prada (2014) estimates. The computation involves:

$$B(M,z) = \frac{1}{L_{\mathrm{smooth}}(M)}\int_{M_{\mathrm{min}}}^{M}\mathrm{d}m\;\frac{\mathrm{d}N_{\mathrm{sub}}}{\mathrm{d}m}\;L_{\mathrm{sub}}(m,x_{\mathrm{sub}})\;\big[1 + B(m)\big]$$

where $\mathrm{d}N_{\mathrm{sub}}/\mathrm{d}m \propto m^{-\alpha}$ ($\alpha \approx 1.9$) is the subhalo mass function, $L_{\mathrm{sub}} \propto m\,c_{\mathrm{sub}}^3/f(c_{\mathrm{sub}})^2$ is the subhalo annihilation luminosity, and the factor $[1 + B(m)]$ recursively includes sub-substructure.

### Theoretical uncertainty from simulations

Fornengo & Regis consider three benchmark scenarios that bracket the uncertainty:

**Scenario 1 (Optimistic):** $M_{\mathrm{min}} = 10^{-6}\,M_\odot$ (WIMP free-streaming mass) with **Via Lactea II** substructure boost — the most optimistic, producing the largest signal.

**Scenario 2 (Intermediate):** $M_{\mathrm{min}} = 10^{-6}\,M_\odot$ with **Aquarius/Virgo Consortium** substructure boost.

**Scenario 3 (Conservative):** $M_{\mathrm{min}} = 10^7\,M_\odot$ (dynamical minimum from resolved subhalos) without substructure — the most conservative.

The boost factor for Milky Way-mass halos ranges from $B \sim 1\text{--}10$ (conservative/Aquarius-based) to $B \sim 10\text{--}100$ (optimistic/Via Lactea-based) with $M_{\mathrm{min}} = 10^{-6}\,M_\odot$. This **up to two orders of magnitude spread** constitutes the single largest theoretical uncertainty in the dark matter annihilation signal prediction. The uncertainty is dominated by the extrapolation of the concentration-mass relation over **more than 12 orders of magnitude** below the resolution limit of current N-body simulations ($\sim 10^6\,M_\odot$), since $L \propto c^3$ makes the annihilation luminosity exquisitely sensitive to concentration.

---

## Part 5 — Window functions and their overlap

### HI intensity mapping window function

The HI window function for a tomographic redshift bin with selection function $\phi_i(z)$ is (Pinetti et al. Eqs. 3.15–3.16):

$$W_{\mathrm{HI}}(\chi) = \bar{T}_b(z)\;b_{\mathrm{HI}}(z)\;\phi_i(z)\;\frac{H(z)}{c}$$

where $\bar{T}_b(z)$ is the mean brightness temperature within a specific redshift bin defined by the radio band. The excellent frequency resolution of radio telescopes allows redshift tomography, and this is a powerful advantage for disentangling DM from astrophysical contributions (since their window functions peak at different redshifts, as shown in Figure 3 of Pinetti et al.).

### DM annihilation gamma-ray window function

The DM window function for an observed energy bin $[E_{\mathrm{min}}, E_{\mathrm{max}}]$ is (Pinetti et al. Eq. 4.1):

$$\boxed{W_\gamma^{\mathrm{DM}}(E,\chi) = \frac{(\Omega_{\mathrm{DM}}\rho_c)^2}{4\pi}\;\frac{\langle\sigma v\rangle}{2m_\chi^2}\;\frac{(1+z)^3}{H(z)}\;\Delta^2(z)\;\int_{E_{\mathrm{min}}}^{E_{\mathrm{max}}}\mathrm{d}E_0\;\frac{\mathrm{d}N_\gamma}{\mathrm{d}E'}\bigg|_{E'=E_0(1+z)}\;e^{-\tau(E_0(1+z),z)}}$$

Each factor has precise physical origin: $(\Omega_{\mathrm{DM}}\rho_c)^2$ is the square of the mean comoving dark matter density reflecting the pair-annihilation process; $(1+z)^3$ comes from the cosmological density scaling (since $\rho^2 \propto (1+z)^6$ but the comoving volume element contributes $(1+z)^{-3}$, a net $(1+z)^3$ remains); $\Delta^2(z)$ is the clumping factor from clustering and substructure; $\mathrm{d}N_\gamma/\mathrm{d}E'$ is the photon yield per annihilation at emitted energy $E' = E_0(1+z)$, computed from PYTHIA or tabulated in PPPC 4 DM ID; and $e^{-\tau(E',z)}$ accounts for pair-production absorption on the extragalactic background light.

This window function is strongly peaked at low redshift for DM because closer structures are brighter and the density-squared weighting favors nearby, well-resolved structures, in contrast to astrophysical sources whose window functions peak at $z \sim 0.5$–$1$.

### Astrophysical source window function

For unresolved gamma-ray sources of class $s$ (Pinetti et al. Eq. 4.3):

$$W_\gamma^{\mathrm{astro}}(E,z) = \frac{[d_L(z)]^2}{(1+z)^2}\int_0^{L_{\mathrm{thr}}(z)}\mathrm{d}L\;\Phi(L,z)\;\frac{\mathrm{d}F}{\mathrm{d}E}(E,L,z)$$

where $\Phi(L,z) = \mathrm{d}n/\mathrm{d}L$ is the gamma-ray luminosity function of the source class, $\mathrm{d}F/\mathrm{d}E$ is the spectral energy distribution (power-law with indices $\Gamma_{\mathrm{BL\,Lac}} = 2.11$, $\Gamma_{\mathrm{FSRQ}} = 2.44$, $\Gamma_{\mathrm{mAGN}} = 2.37$, $\Gamma_{\mathrm{SFG}} = 2.7$), and $L_{\mathrm{thr}}(z) = 4\pi d_L^2(z)\,S_{\mathrm{thr}}$ is the luminosity above which sources are individually resolved by Fermi-LAT and masked.

### Overlap and sensitivity

The HI window function peaks at $z \sim 0.2\text{--}0.5$ (for MeerKAT/SKA L-band), providing excellent overlap with the DM annihilation window which also peaks at low redshift. The distinct redshift dependence between DM (scaling as $(1+z)^3\Delta^2$) and astrophysical sources (scaling with their respective luminosity functions) enables **tomographic discrimination**—different redshift bins have different DM-to-astrophysical ratios, breaking the degeneracy. This is the physical basis for the key finding in Pinetti et al. that low-redshift radio bands (Band 2, corresponding to frequencies near the rest-frame 21-cm line) are most promising for DM searches.

---

## Part 6 — Error budget and signal-to-noise ratio

### Gaussian variance

Under Gaussian assumptions, the variance on the cross-correlation angular power spectrum is (Pinetti et al. Eq. 2.7):

$$\left(\Delta C_\ell^{\mathrm{HI},\gamma}\right)^2 = \frac{1}{(2\ell+1)\,\Delta\ell\,f_{\mathrm{sky}}}\left[\left(C_\ell^{\mathrm{HI},\gamma}\right)^2 + \left(C_\ell^{\mathrm{HI,HI}} + N_\ell^{\mathrm{HI}}\right)\left(C_\ell^{\gamma\gamma} + \frac{N_\ell^\gamma}{(B_\ell^\gamma)^2}\right)\right]$$

where $f_{\mathrm{sky}}$ is the observed sky fraction, $\Delta\ell$ is the multipole bin width, $N_\ell^{\mathrm{HI}}$ and $N_\ell^\gamma$ are instrumental noise power spectra, and $B_\ell^\gamma$ is the Fermi-LAT beam function in harmonic space (an energy-dependent Gaussian with $\sigma_b(E) \approx 1.2°\times (E/0.5\;\mathrm{GeV})^{-0.95} + 0.05°$).

The $C_\ell^{\mathrm{HI},\gamma}$ squared term represents cosmic variance of the cross-correlation signal itself and is typically negligible. The dominant term is the product of auto-correlations plus noise: even in the absence of a true cross-correlation, random chance alignments produce a spurious cross-correlation whose variance is set by the product of the two auto-spectra. At high $\ell$, $B_\ell^\gamma$ falls exponentially, so the ratio $N_\ell^\gamma/(B_\ell^\gamma)^2$ grows rapidly, making the effective gamma-ray noise very large. This means the cross-correlation becomes undetectable at multipoles above $\ell_{\mathrm{max}} \sim$ a few hundred (energy-dependent), creating a **sweet spot** in multipole space where the signal-to-noise is maximised.

In practice, since the cross-correlation signal is small and the gamma-ray auto-correlation is dominated by photon noise, the variance simplifies to:

$$\left(\Delta C_\ell^{\mathrm{HI},\gamma}\right)^2 \approx \frac{1}{(2\ell+1)\,\Delta\ell\,f_{\mathrm{sky}}}\;\frac{N_\ell^\gamma}{(B_\ell^\gamma)^2}\;\left(C_\ell^{\mathrm{HI,HI}} + N_\ell^{\mathrm{HI}}\right)$$

### Signal-to-noise ratio and Δχ² test

The cumulative signal-to-noise ratio is obtained by summing over multipoles and energy bins (Pinetti et al. Eq. 5.6):

$$\left(\frac{S}{N}\right)^2 = \sum_{E\text{-bins}}\sum_\ell \frac{\left[C_\ell^{\mathrm{HI}\times\gamma}(E)\right]^2}{\left[\Delta C_\ell^{\mathrm{HI}\times\gamma}(E)\right]^2}$$

To constrain dark matter parameters, Pinetti et al. employ a $\Delta\chi^2$ test (Eq. 5.7):

$$\Delta\chi^2 = \sum_{\ell,E}\frac{\left[C_\ell^{\mathrm{HI}\times\gamma,\mathrm{tot}}(E) - C_\ell^{\mathrm{HI}\times\gamma,\mathrm{astro}}(E)\right]^2}{\left[\Delta C_\ell^{\mathrm{HI}\times\gamma}(E)\right]^2}$$

Since the DM contribution is additive, $C_\ell^{\mathrm{tot}} = C_\ell^{\mathrm{astro}} + C_\ell^{\mathrm{DM}}(\langle\sigma v\rangle)$, and $C_\ell^{\mathrm{DM}}$ is strictly proportional to $\langle\sigma v\rangle$ at fixed $m_\chi$ and annihilation channel, **this reduces to a 1-parameter test**. The dark matter mass $m_\chi$ determines the spectral shape $\mathrm{d}N_\gamma/\mathrm{d}E$ and therefore the energy-bin weights, while the annihilation channel (e.g., $b\bar{b}$) is fixed by hypothesis. The $2\sigma$ (95.45% CL) upper limit on $\langle\sigma v\rangle$ is obtained from $\Delta\chi^2 = 4$ for one degree of freedom (note: $\Delta\chi^2 = 3.84$ gives the exact 95% CL; the approximation $\Delta\chi^2 = 4$ is standard practice in the particle physics literature). A Fisher matrix approach with nuisance parameters for the astrophysical normalization amplitudes confirms that the DM bound is robust against marginalization over astrophysical model uncertainties.

Key projected sensitivities from Pinetti et al.: **MeerKAT × Fermi-LAT** achieves S/N $\sim 3.7$ for astrophysical sources; **SKA1 × Fermi-LAT** reaches $\sim 5.7$; **SKA2 × Fermi-LAT** reaches $\sim 8.2$. For dark matter, SKA2 combined with a hypothetical next-generation gamma-ray telescope ("Fermissimo," with $2\times$ exposure and $5\times$ better angular resolution) can probe the **thermal relic cross section** $\langle\sigma v\rangle = 3 \times 10^{-26}\;\mathrm{cm}^3\,\mathrm{s}^{-1}$ up to $m_\chi \sim \mathcal{O}(\mathrm{TeV})$.

---

## Part 7 — Practical considerations for real-world implementation

### Pseudo-$C_\ell$ estimation under partial sky coverage

Real observations cover only a fraction $f_{\mathrm{sky}}$ of the sky (after masking the Galactic plane and resolved sources). The measured harmonic coefficients $\tilde{a}_{\ell m}$ of the masked field are related to the true coefficients through mode-coupling induced by the mask. The pseudo-$C_\ell$ estimator (Hivon et al. 2002) gives:

$$\langle\tilde{C}_\ell\rangle = \sum_{\ell'} M_{\ell\ell'}\,C_{\ell'}$$

where the **mode-coupling matrix** is:

$$M_{\ell\ell'} = \frac{2\ell'+1}{4\pi}\sum_{\ell''}(2\ell''+1)\,W_{\ell''}\begin{pmatrix}\ell & \ell' & \ell'' \\ 0 & 0 & 0\end{pmatrix}^2$$

Here $W_\ell$ is the angular power spectrum of the mask window, and the parenthesized term is the Wigner 3-$j$ symbol enforcing the triangle inequality $|\ell - \ell'| \leq \ell'' \leq \ell + \ell'$. The true power spectrum is recovered by matrix inversion: $\hat{C}_\ell = \sum_{\ell'} M_{\ell\ell'}^{-1}\,\tilde{C}_{\ell'}$. A key advantage of the cross-correlation approach is that **noise bias vanishes** because instrumental noise on the radio and gamma-ray sides is uncorrelated—unlike auto-correlation analyses where noise bias must be carefully subtracted.

### Foreground contamination

**Radio side.** Galactic synchrotron emission ($\sim 700$ K at 408 MHz, spectral index $\beta \approx -2.5$ to $-2.7$) dominates the HI signal ($\sim$hundreds of $\mu$K) by **six orders of magnitude**. Free-free emission and extragalactic point sources contribute at lower levels. The saving grace is that these foregrounds are spectrally smooth, while the 21-cm signal fluctuates with frequency. Polynomial fitting, principal component analysis, or independent component analysis along the frequency axis can remove foregrounds to the required level, though at the cost of removing some large-scale line-of-sight modes. This signal loss is quantified by a **transfer function** $T(k_\parallel)$ that must be calibrated through mock signal injection.

**Gamma-ray side.** Diffuse Galactic emission from cosmic-ray interactions (pion decay, inverse Compton, bremsstrahlung) dominates. Masking the Galactic plane ($|b| < 20°\text{--}30°$) and applying Galactic diffuse emission templates (from the Fermi Science Tools) mitigate this contamination. Resolved point sources from the 4FGL/5FGL catalog are masked. Residual cosmic-ray contamination in Fermi-LAT data is addressed through stringent event selection (ULTRACLEANVETO class).

**Cross-correlation advantage.** Since radio and gamma-ray foregrounds arise from independent physical processes and different regions of the electromagnetic spectrum, they are **uncorrelated** with each other. Their contribution to the cross-correlation is therefore zero in expectation, entering only through increased noise in the auto-spectra within the Gaussian variance. This makes the cross-correlation inherently more robust against systematics than either auto-correlation alone.

### Non-Gaussian contributions to the covariance

The Gaussian variance is a lower bound on the true uncertainty. The full covariance includes the **connected non-Gaussian (cNG) term**, arising from the angular trispectrum projected from the 3D matter trispectrum (dominated by the 1-halo trispectrum), and the **super-sample covariance (SSC)**, where density fluctuations on scales larger than the survey volume modulate the local power spectrum, coupling different multipoles. The SSC contribution scales as $\mathrm{Cov}_{\ell\ell'}^{\mathrm{SSC}} \propto (\partial C_\ell/\partial\delta_b)(\partial C_{\ell'}/\partial\delta_b)\,\sigma_b^2$.

For precision analyses, neglecting non-Gaussian contributions can **underestimate confidence regions by up to $\sim 70\%$** (as demonstrated for cosmic shear). For the HI × UGRB cross-correlation with current Fermi-LAT data, the error budget is dominated by gamma-ray photon noise, and non-Gaussian corrections are subdominant. However, for future experiments with substantially improved gamma-ray sensitivity, proper treatment of the non-Gaussian covariance will become essential.

---

## Conclusion

The theoretical formalism for cross-correlating HI 21-cm intensity mapping with the unresolved gamma-ray background is built on a chain of well-understood but interrelated components. The Limber-projected angular power spectrum converts three-dimensional clustering information into observable two-dimensional correlations with the identification $k = (\ell + 1/2)/\chi$. The halo model provides a physically transparent decomposition into 1-halo (intra-halo structure) and 2-halo (inter-halo clustering) contributions, with the crucial distinction between density fields ($\tilde{u}$) and density-squared fields ($\tilde{v}$) naturally encoding the difference between gravitational tracers like HI and annihilation signals.

The method's power lies in three features that standard single-tracer analyses lack. First, the cross-correlation isolates the physical connection between the matter distribution (traced by HI) and its squared analog (traced by annihilation), filtering out uncorrelated foregrounds from both sides. Second, the joint spectral–tomographic analysis (multiple energy bins × multiple redshift bins) exploits the distinct scaling of the DM signal—$(1+z)^3\Delta^2(z)\,\mathrm{d}N_\gamma/\mathrm{d}E\,e^{-\tau}$—versus astrophysical backgrounds to break degeneracies. Third, the sensitivity depends on the overlap integral of the window functions, and the fortunate coincidence that both HI intensity and DM annihilation signals peak at $z \lesssim 0.5$ maximizes this overlap.

The dominant theoretical uncertainty remains the substructure boost, spanning two orders of magnitude from conservative (no substructure, $M_{\mathrm{min}} = 10^7\,M_\odot$) to optimistic (Via Lactea extrapolation to $M_{\mathrm{min}} = 10^{-6}\,M_\odot$) prescriptions. This uncertainty propagates directly into the clumping factor $\Delta^2(z)$ and the 1-halo DM profile $\tilde{v}(k|M)$, making it the primary bottleneck for translating an observed cross-correlation signal into a definitive dark matter detection or exclusion. Progress will require both improved N-body resolution at the low-mass frontier and independent calibration through complementary probes of small-scale dark matter clustering.
