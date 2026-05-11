Nonlinearity 

## **PAPER • OPEN ACCESS** 

## Self-consistent Coulomb interactions for machine learning interatomic potentials 

To cite this article: Jack Thomas et al 2025 Nonlinearity 38 095024 

View the article online for updates and enhancements. 

## You may also like 

- Introduction to machine learning potentials for atomistic simulations Fabian L Thiemann, Niamh O’Neill, Venkat Kapil et al. 

- Kernel charge equilibration: efficient and accurate prediction of molecular dipole moments with a machine-learning enhanced electron density model Carsten G Staacke, Simon Wengert, Christian Kunkel et al. 

- _(Invited)_ Training Accurate and Physically Meaningful Machine Learning Force Fields for Water 

Tristan Maxson and Tibor Szilvasi 

This content was downloaded from IP address 131.111.184.43 on 11/05/2026 at 12:11 

Nonlinearity 

Nonlinearity **38** (2025) 095024 (38pp) 

https://doi.org/10.1088/1361-6544/ae0402 

# **Self-consistent Coulomb interactions for machine learning interatomic potentials** 

**Jack Thomas**[1]  **, Will Baldwin**[2] **, Gabor Csanyi**[2] **and Christoph Ortner**[3][,] _**[∗]**_  

> 1 School of Mathematics, University of Minnesota Twin Cities, Minneapolis, MN 55455, United States of America 

> 2 Engineering Laboratory, University of Cambridge, Trumpington Street, Cambridge CB2 1PZ, United Kingdom 

> 3 Department of Mathematics, University of British Columbia, Vancouver, Canada 

E-mail: ortner@math.ubc.ca, thom9218@umn.edu, wjb48@cam.ac.uk and gc121@cam.ac.uk 

Received 18 June 2024; revised 7 August 2025 Accepted for publication 5 September 2025 Published 17 September 2025 

Recommended by Dr Helen Davis 

**==> picture [33 x 38] intentionally omitted <==**

## **Abstract** 

A ubiquitous approach to obtain transferable machine learning-based models of potential energy surfaces for atomistic systems is to decompose the total energy into a sum of local atom-centred contributions. However, in many systems non-negligible long-range electrostatic effects must be taken into account as well. We introduce a general mathematical framework to study how such long-range effects can be included in a way that (i) allows charge equilibration and (ii) retains the locality of the learnable atom-centred contributions to ensure transferability. Our results give partial explanations for the success of existing machine learned potentials that include equilibration and provide perspectives how to design such schemes in a systematic way. To complement the rigorous theoretical results, we describe a practical scheme for fitting the energy and electron density of water clusters. 

- _∗_ Author to whom any correspondence should be addressed. 

Original Content from this work may be used under the terms of the Creative Commons Attribution 4.0 licence. Any further distribution of this work must maintain attribution to the author(s) and the title of the work, journal citation and DOI. 

© 2025 The Author(s). Published by IOP Publishing Ltd and the London Mathematical Society. 

1 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

Keywords: Coulomb interactions, machine learning, electronic structure, tight binding, interatomic potentials, locality, body-order expansion 

Mathematics Subject Classification numbers: 65E05, 74E15, 81V45, 81V70 

## **1. Introduction** 

Electronic structure models are widely used to predict optical, magnetic, and mechanical properties of materials and molecules. Today, _ab initio_ methods, such as density functional theory (DFT) [20, 27, 30, 42], are too computationally expensive for large-scale simulations (but are still a popular choice for the simulation of systems up to a few hundred atoms, for example), whereas empirical force fields remain useful for large system sizes and long timescales. The introduction of machine-learning (ML) methodology into this field offers the prospect of bridging the gap between _ab initio_ and empirical models in order to derive models with _ab initio_ accuracy but at a fraction of the computational cost, enabling a systematic extension of the predictive first principles approach beyond the electronic structure length-scale to which it has been limited up until recently [6–8, 12, 17, 39]. 

This is often motivated by invoking the nearsightedness principle of electronic matter (NEM) [45]. NEM concerns an electron density which is the ground state of an external potential _v_ , given a fixed chemical potential. The statement is that if _v_ is changed in some region Ω, then the response of the electron density at point _x_ decays towards zero as _x_ moves away from Ω. NEM therefore suggests that local machine learning models are effective so long as a change in geometry does not induce changes in _potential_ at some distant point. This is not the case when, for instance, a reorientation of a polar molecule leads to a change in external potential even at distant points. In order to account for electrostatic effects, a long-range pairwise term can be added to the standard machine learning energy contribution that maps local geometry to energy [5]. However, changes in the chemical environment may induce changes in the charge distribution at long-range (even if the local geometry is unchanged). It is therefore important in many systems to include electronic information directly into the machine learning framework. In this paper, we derive a mathematically rigorous scheme for including enhanced electronic information into machine learned interatomic potentials. In doing so, we go some way to justifying the ML charge equilibration schemes which have been proposed in the literature, including the Fourth generation neural network potential [29], the Becke population neural network (BpopNN) [59] and the self consistent field neural network (SCFNN) [21]. 

To efficiently parameterise the complex many-body Born–Oppenheimer potential energy surface (PES) using ML methodology, one must decompose it into lower dimensional components. In previous works, we established two groups of results of this kind, both for simplified models that explicitly replaced Coulomb with an exponentially localised Yukawa interaction: The total potential energy can be decomposed into a sum of atom-centred site energy contributions that may be chosen (with controllable error) to _(i)_ depend only on atoms within a finite cut-off radius _r_ cut[41, 53], and ( _ii_ ) have finite _correlation order N_ [55]. The error committed in this approximation is exponentially small in both _r_ cut and _N_ . That is, for an atomic system _**r**_ = _{_ _**r** ℓ}[M] ℓ_ =1 _[⊂]_[R] _[d]_[, we may approximate the total energy] _[ E]_[(] _**[r]**_[) =][ �] _ℓ[E][ℓ]_[(] _**[r]**_[)][ by:] 

**==> picture [373 x 30] intentionally omitted <==**

2 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

where _**r** ℓk_ := _**r** k −_ _**r** ℓ_ , _rℓk_ := _|_ _**r** ℓk|_ , and _Vn_ ( _**r** ℓk_ 1 _,...,_ _**r** ℓkn_ ) is an ( _n_ + 1)- _body_ (or _n_ - _correlation_ ) _potential_ modelling the interaction of a central atom _ℓ_ and the _n_ neighbouring atoms _k_ 1 _,..., kn_ . 

Exponential convergence of (1.1) in terms of both cut-off radius and correlation order [41, 53, 55] lends theoretical support to the empirical success of body-ordered approximations in popular machine learning schemes [17, 50]. However, an underlying assumption in all of these results is the total screening of Coulomb interactions. While an appropriate simplification for a variety of systems, this assumption is a significant limitation of the results, and also considerably simplifies the mathematical analysis. 

In response, some machine learning schemes began to include an additional long-range electrostatic contribution to the total energy of the system. For example, in [2, 60], the authors incorporate long-range interactions by training additional neural networks to produce atomic charges that either predict the _ab initio_ point charges [2] directly, or do so by learning the dipole moments [60]. However, these methods learn the long-range electrostatics from machine learning schemes with local descriptors and therefore cannot be expected to correctly adapt to changes in the chemical environment that result in non-local charge equilibration. 

In a different direction, the long-distance equivariant (LODE) framework [24] builds on SOAP descriptors [4] by incorporating the electrostatic potential corresponding to proxy densities to provide enhanced electronic information directly into the descriptors. These additional non-local descriptors are fixed, and are again not equilibrated in a way resembling the underlying physics. 

An alternative perspective is to revisit the classical electronegativity equalisation method (EEM) [37, 38] (or, charge equilibration (QEq) [46, 47]), as well as improvements based on the same idea [15, 58]. One postulates an extended PES as a function of partial charges _qℓ_ := _Zℓ − pℓ_ where _Zℓ_ is the atomic species and _pℓ_ is an electron population on atom _ℓ_ . This extended PES is minimised with respect to the charges, together with constraints on the total charge in the system, to produce a charge-equilibrated PES: 

**==> picture [373 x 23] intentionally omitted <==**

The first term of _E_ ( _**r** , q_ ) is the intra-atomic energy resulting from a Taylor series expansion of the individual atomic energies of the constituent elements with _χ_ the electronegativity and _U_ the atomic hardness. These quantities may be written in terms of atomic ionisation potentials (IP) and electron affinities (EA), which traditionally were obtained from experimental data. The charges at different atomic positions interact through the Coulomb potential _J_ . Since _E_ ( _**r** , q_ ) is a quadratic function of _q_ , minimising with respect to the charges, leads to a linear system of equations which may be solved subject to a constraint on the total charge of the system. 

In reality, the parameters in (1.2) should be environment-dependent: _χℓ_ = _χℓ_ ( _**r**_ ) and _Uℓ_ = _Uℓ_ ( _**r**_ ). Exploiting the fact that the atomic electronegativities are local functions of the environment [22], a natural approach is to parameterise them using a machine learning framework, leading to the charge equilibration via neural network technique (CENT) [19, 22]. The basic idea in this method can be represented in the following schematic: 

**==> picture [313 x 12] intentionally omitted <==**

The first mapping in (1.3) is approximated through a neural network architecture, whereas the simple quadratic form of (1.2) means the mapping from electronegativities to energies _E_ and forces _∇E_ can be efficiently and cheaply evaluated through solving a linear system of equations and evaluating explicit functions. This approach therefore builds on the simplicity of QEq 

3 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

schemes with a machine learning approach, leading to improved accuracy and transferability. However, by its very nature, a quadratic-in- _q_ ansatz is too simple to fully model the underlying physics. For example, this scheme can only describe systems where the ground state electron density (and potential energy) is a smooth function of the geometry. This is not the case for systems which exhibit conical intersections—wherein the crossing in energies between two diabatic states leads to a discontinuous electron density as a function of geometry. Such conical intersections already occur in simple molecules [44, 57]. 

In the BpopNN [59], the electronegativity and atomic hardness are fixed, and an additional neural network correction is added to the total energy from (1.2) that depends on both the atomic positions and charges, 

**==> picture [313 x 23] intentionally omitted <==**

where _fZℓ_ is an atomic neural network for the atomic species _Zℓ_ . Then, in contrast to (1.2), the entire extended PES is approximated by targeting an _ab initio_ PES of the form minΨ _→q ⟨_ Ψ _|H|_ Ψ _⟩_ where Ψ is an admissible wavefunction in this minimisation problem if the corresponding electron density _ρ_ Ψ satisfies _qℓ_ = _Zℓ −_ ´ _ρ_ Ψ( _x_ ) _ω_ ( _x −_ _**r** ℓ_ )d _x_ for some chosen weight function _ω_ concentrated around the origin. In practice, this is done using constrained DFT implemented in Q-Chem [49]. Minimising the extended PES with respect to charges mimics the charge-equilibration in DFT models, and thus the electronic contributions are able to self-consistently adapt to the global environment. 

Thus, the overarching idea is to consider an extended PES as a function of the atomic configuration together with additional atom-centred features which provide a low-dimensional representation of the electron density (in BpopNN, the additional features are Becke populations). This model energy may then be minimised with respect to the additional features to provide a self-consistent PES. In this paper, we rigorously justify this approach by introducing atom-centred features � _v_ describing the effective potential: 

**==> picture [313 x 22] intentionally omitted <==**

and _E_ el is an explicit long-range function of the electron density. We then show that the quantities _Eℓ,ρℓ_ are local functions of the extended variables _{_ _**r** k,_ � _vk}k_ and can thus be approximated using a machine learning framework. In particular, we are able to approximate (1.5) with a body-ordered PES _EN_ ( _**r** ,_ � _v_ ) analogous to (1.1), and show that minimisers � _v[⋆]_ to (1.5) (and corresponding energies) may be approximated with minimisers � _v[⋆] N_[to] _[ E][N]_[(and the corresponding] approximate energies). The scheme is systematically improvable by choosing higher bodyordered approximations. 

While this approach is convenient to obtain theoretical results that partially justify the BpopNN approach [59], we also present numerical experiments for a closely related but computationally more practical fixed point scheme. We build a machine learning based surrogate model describing _Eℓ_ and _ρℓ_ as functions of the extended variables _{_ _**r** k,_ � _vk}k_ . Then, instead of minimising the approximate energy as in the theoretical results, in practice, it is more convenient to approach the critical points of the energy by iteratively solving the corresponding Euler–Lagrange equation directly. We show convergence plots for water clusters as the number of features on each atomic site is increased. 

The paper is organised as follows. In section 2, we discuss popular Kohn–Sham models (section 2.1) from which we derive corresponding tight-binding (section 2.2) and machine 

4 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

learning schemes (section 2.3). In section 3 we state that these resulting machine learning models can be decomposed as in (1.5). Numerical experiments are presented in section 4. Proofs of the main results are collected together in section 6. A brief summary of the main notation used throughout this paper is contained in appendix A. 

## **2. Electronic structure models** 

In this section, we consider a sequence of approximations starting with Kohn–Sham DFT and resulting in machine learning schemes that provide a convenient framework for the theoretical results of this paper. When discussing these electronic structure models, we follow the majority of numerical studies and consider the _canonical ensemble_ for the electrons; the number of particles in the system, the volume, and Fermi-temperature are all fixed. However, since the rigorous results of this paper are stated and proved in the _grand-canonical ensemble_ (where the chemical potential, volume, and Fermi-temperature are fixed), in remarks 3, 4 and 7 we explain how these models are adapted to this setting. In section 3 (remark 10) we explain how, in principle, one may extend the analysis of this paper to the canonical ensemble; a possible direction for future work. 

## _2.1. Kohn–Sham models_ 

For simplicity of notation, we shall consider spin unpolarised systems with an even number of electrons which allows us to omit the spin variable in the following. We consider a system of _M_ atoms at positions _**r**_ 1 _,...,_ _**r** M ∈_ R[3] with corresponding atomic charges _Z_ 1 _,..., ZM_ , and _N_ el electron pairs. The corresponding _one-particle density operator_ of this system is a selfadjoint projector _γ_ on _L_[2] (R[3] ) with Tr _γ_ = _N_ el. Since _γ_ is compact (as it is trace-class), _γ_ may be diagonalised in an orthonormal basis _φi_ = _|i⟩_ , leading to the following expressions for _γ_ and the corresponding electron density _ργ_ : 

**==> picture [165 x 30] intentionally omitted <==**

where _⟨i| ∈ L_[2] (R[3] ) _[⋆]_ with _⟨i|ϕ_ := ( _φi,ϕ_ ) _L_ 2(R3) and _⟨i|j⟩_ := ( _φi,φj_ ) _L_ 2(R3) = _δij_ . The density clearly satisfies _ργ_ ⩾ 0 and ´ _ργ_ = 2 _N_ el. The total energy of the system, in Kohn–Sham models, takes the form [1] 

**==> picture [313 x 25] intentionally omitted <==**

_Zi_ where _V_[nuc] ( _x_ ) := _−_[�] _i |x−_ _**r** i|_[is the potential generated by the nuclei and the kinetic energy is] given by 

**==> picture [176 x 30] intentionally omitted <==**

Therefore, if _γ_ has finite kinetic energy, then _[√] ργ ∈ H_[1] (R[3] ) and the Sobolev embedding [3] implies _ργ ∈ L_[1] _∩ L_[3] (R[3] ) _⊂ L_[6] _[/]_[5] (R[3] ). The latter fact also ensures the Coulomb energy ˜ _ργ_ ( _|xx−_ ) _ρyγ|_ ( _y_ ) d _x_ d _y_ is finite since ˜ _f_ ( _|xx_ ) _−g_ ( _yy|_ )[d] _[x]_[d] _[y]_[ ≲] _[∥][f][∥][L]_[6] _[/]_[5][(][R][3][)] _[∥][g][∥][L]_[6] _[/]_[5][(][R][3][)][ (which follows from the] Hardy–Littlewood–Sobolev inequality [3]). 

5 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**Remark 1 (smeared nuclei).** If we instead consider smeared nuclei (which is done implicitly in CENT [19, 22]) with distribution _ν_ ( _x_ ) =[�] _[M] k_ =1 _[Z][k][m][k]_[(] _[x][ −]_ _**[r]**[k]_[)][ where] _[ m]_[1] _[,...,][m][M]_[are smooth] _ν_ ( _y_ ) non-negative functions with ´ _mk_ = 1, then _V_[nuc] ( _x_ ) = _−_ ´ _|x−y|_[d] _[y]_[. Therefore, up to a constant] representing the nuclei-nuclei interaction, we have 

**==> picture [373 x 26] intentionally omitted <==**

The Coulomb term from [22] is _Jℓk_ = erf( _τℓkrℓk_ ) and results from the final term in (2.2) by assuming a Gaussian distribution for both the nuclei and the electron density. 

In theory, there is a universal exact exchange-correlation functional [27, 30]. However, this function is complicated and unknown. In practice, _E_ xc is replaced with an approximation: 

- _E_ xc = 0 : reduced Hartree–Fock (also known as the Hartree model [25]), 

- 2 

- _• E_ xc[ _γ_ ] = _−_[1] 2 ˜ _|γ|_ ( _xx−,yy_ ) _||_[d] _[x]_[d] _[y]_[ : Hartree–Fock. This model results from a variational formula-] tion restricted to the set of finite energy Slater determinants, 

- _E_ xc[ _γ_ ] = ´ _ε_ xc� _ργ_ ( _x_ )�d _x_ : local density approximation (LDA) [30]. In this formulation, _ρ[−]_[1] _ε_ xc( _ρ_ ) is the exchange-correlation density for a uniform electron gas with density _ρ_ . The 4 

- simplest such approximation is given by _ε_ xc( _ρ_ ) := _−c_ 0 _ρ_ 3 where _c_ 0 is a positive constant, 

- _• E_ xc[ _γ_ ] = ´ _ε_ xc� _ργ_ ( _x_ ) _, |∇_ � _ργ_ ( _x_ ) _|_[2][�] d _x_ : the generalised gradient approximation (GGA) is the next simplest functional form that allows for the inhomogeneity of the electron density. 

After choosing a level of theory, (2.1) is minimised over the space of finite energy (one particle) density operators as described above: 

**==> picture [313 x 14] intentionally omitted <==**

where _S_ � _L_[2] (R[3] )� is the space of self-adjoint operators on _L_[2] (R[3] ). In extended Kohn–Sham models, one minimises (2.1) over the convex hull of _PN_ el, denoted 

**==> picture [373 x 13] intentionally omitted <==**

allowing for fractional occupation numbers. The existence of a minimiser has been established for the various levels of theory: Hartree model [51], Hartree–Fock [34, 35], extended Hartree– Fock [33], LDA [11], and extended LDA and GGA [1]. 

We consider the minimisation problem (2.1) within the LDA theory (though conceptually at least our approach can be applied more generally). We first introduce mild assumptions on _ε_ xc that are satisfied for practical models: _ε_ xc : R+ _→_ R is twice differentiable with _ε_ xc _∼−ρ_[4] _[/]_[3] near zero and _−ρ_[1] _[/]_[3] ≲ _ε_ xc _[′]_[(] _[ρ]_[)][ ⩽][0 on][ (][0] _[,][∞]_[)][. Moreover, we define the Hamiltonian] 

**==> picture [313 x 21] intentionally omitted <==**

_f_ ( _y_ ) where _v_ C _f_ ( _x_ ) := ´ _|x−y|_[d] _[y]_[ denotes the Coulomb potential, and] _[ V]_[eff][[] _[ρ]_[]][ is the effective potential.] For a given _ρ_ , there exists an associated _Fermi level ε_ F satisfying Tr _χ_ ( _−∞,ε_ F]� _H_ [ _ρ_ ]� = _N_ el. We have the following existence result [1]: 

**Theorem 1.** _For neutral or positively charged systems, there exists a minimiser γ_[0] _of (_ 2.1 _) over KN_ el _. If there exists a Fermi level associated to ργ_ 0 _such that ε_ F _̸∈ σ_ � _H_ [ _ργ_ 0]� _, then_ 

**==> picture [313 x 13] intentionally omitted <==**

6 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**Remark 2 (finite Fermi-temperature).** The main results of this work also apply to the finite Fermi-temperature setting [36]. In this case, the total energy of the system is 

**==> picture [313 x 13] intentionally omitted <==**

where _S_ ( _x_ ) := _x_ log _x_ + (1 _− x_ ) log(1 _− x_ ) is the Fermi–Dirac entropy and _β_ = ( _k_ B _T_ ) _[−]_[1] is the _inverse Fermi-temperature_ where _k_ B is the Boltzmann constant and _T_ the absolute temperature. (The zero Fermi-temperature case (2.1) is naturally included with _E_ = _E∞_ ). Then, as in extended Kohn–Sham models, this finite Fermi-temperature energy is minimised over _KN_ el, yielding 

**==> picture [313 x 13] intentionally omitted <==**

where _Fµ,β_ ( _x_ ) := �1 + e _[β]_[(] _[x][−][µ]_[)][�] _[−]_[1] is the Fermi–Dirac distribution with chemical potential _µ_ and inverse Fermi-temperature _β_ . Using the notation _Fε_ F _,∞_ := lim[=] _[ χ]_[(] _[−∞][,ε]_[F][)][ +] 2[1] _[χ][{][ε]_[F] _[}]_[,] the Euler–Lagrange _β→∞[F][ε]_[F] _[,β]_ equation (2.8) is also valid at zero Fermi-temperature in the case that there is a spectral gap at the Fermi-level (2.6). 

The main results of this paper (see next section) are stated and proved both for insulators at zero temperature and in the case of finite Fermi-temperature. 

**Remark 3 (grand canonical ensemble).** For fixed chemical potential _µ ∈_ R, we also define the grand-canonical free energy: 

**==> picture [313 x 11] intentionally omitted <==**

which is minimised over the set of one-particle density operators without the constraint on the number of electrons in the system: _P_ :=[�] _N_ el⩾0 _[P][N]_ el[(for standard Kohn–Sham models at zero] Fermi-temperature) or _K_ :=[�] _N_ el⩾0 _[K][N]_ el[(for][extended][models][at][zero][Fermi-temperature,][or] at finite Fermi-temperature). In this way, the chemical potential represents the contribution to the free energy due to varying particle number. 

The main results of this paper are stated for the grand-canonical ensemble, and we comment further in remark 10 (below) regarding extending the analysis to the canonical ensemble. 

For the remainder of this paper, it will be convenient to consider the _(one-particle) density matrix_ , the integral kernel of the density operator: for _γ ∈PN_ el, it is common to abuse notation and also write _γ ∈ L_[2] (R[3] _×_ R[3] ) such that 

**==> picture [313 x 24] intentionally omitted <==**

## _2.2. Tight binding_ 

We expand the one-particle density operator _γ_ =[�] _i[f][i][ |][i][⟩⟨][i][| ∈K][N]_ el[in a local basis of atomic-] like orbitals (recall that, 0 ⩽ _fi_ ⩽ 1 with[�] _i[f][i]_[=] _[ N]_[el][).][That][is,][to][each][atomic][site] _[ℓ][∈] {_ 1 _,..., M}_ , we assign _N_ b = _N_ b( _Zℓ_ ) atomic-like orbitals _|ℓa⟩_ := _ϕℓa_ := _ϕZℓ,a_ ( _· −_ _**r** ℓ_ ) centred on _**r** ℓ_ and depending on the atomic species _Zℓ_ (for _a_ = 1 _,..., N_ b). Then, on expanding _|i⟩_ = � _ℓa[C] ℓ[i] a[|][ℓ][a][⟩]_[for some coefficients] _[ C][i][∈]_[(][R] _[N]_[b][)] _[M]_[, we have] 

**==> picture [313 x 24] intentionally omitted <==**

7 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

where _γ_ TB :=[�] _i[f][i][ C][i][⊗][C][i]_[. Throughout this paper, we will assume that the orbitals are expo-] nentially localised: there exists _cϕ,ηϕ >_ 0 such that 

**==> picture [313 x 14] intentionally omitted <==**

for all atomic species _Z_ , basis indices _a_ = 1 _,..., N_ b, and multi-indices _α ∈_ N[3] with _|α|_ 1 ⩽ _ν_ for some _ν_ ⩾ 2. (We require _ν_ = 2 for the main results, but will comment on possible extensions if _ν >_ 2.) 

For the remainder, we will simply write _γ_ = _ϕ_[T] _γ_ TB _ϕ_ both for the density matrix (2.11) as well as the corresponding density operator as defined by (2.10). Moreover, the electron density _ργ_ corresponding to _γ_ is given by _ργ_ ( _x_ ) := 2 _ϕ_ ( _x_ )[T] _γ_ TB _ϕ_ ( _x_ ). We suppose that _⟨ℓa|kb⟩_ = _δℓkδab_ that is, we assume an _othogonal_ tight binding model. This can be achieved in practice by considering a similarity transformation of the orbitals such as the Löwdin transform [9, 14]. A consequence of this is that _C[i] · C[j]_ = _δij_ . In the following, we also suppose that the number of orbitals per atom is constant. We do this without loss of generality [40, appendix B]. 

When _γ_ = _ϕ_[T] _γ_ TB _ϕ_ as in (2.11), and assuming an LDA exchange correlation functional, the _ab initio_ energy (2.1) reduces to 

**==> picture [313 x 23] intentionally omitted <==**

**==> picture [313 x 23] intentionally omitted <==**

Therefore, we also suppose that _{ϕℓa} ⊂ H_[1] (R[3] ). 

In particular, on making the tight-binding approximation, we are restricting the class of one-particle density operators to _PN_[TB] el[where] 

**==> picture [373 x 27] intentionally omitted <==**

We also define the projection of the Hamiltonian (2.5) onto the tight binding basis by 

**==> picture [313 x 24] intentionally omitted <==**

where _V_ eff[ _ρ_ ] is given by (2.5), and write _λ_ 1( _ρ_ ) ⩽ _···_ ⩽ _λM·N_ b( _ρ_ ) for the ordered eigenvalues of _H_[TB] [ _ρ_ ] counting multiplicities. 

The electronic structure problem in the tight binding framework then consists of minimising _E_ (2.13) over _PN_[TB] el[:] 

**Proposition 2.** _There exists γ_[0] = _ϕ_[T] _γ_ TB[0] _[ϕ][, a minimiser of][ E][over][ P] N_[TB] el _[. If there is a gap in the] spectrum (that is, λN_ el( _ργ_ 0) _< λN_ el+1( _ργ_ 0) _), then_ 

**==> picture [313 x 14] intentionally omitted <==**

_where the Fermi-level ε_ F _is any value satisfying λN_ el( _ργ_ 0) _< ε_ F _< λN_ el+1( _ργ_ 0) _._ 

8 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**Remark 4.** We may also consider minimising _Eβ_ (as defined in (2.7)) over 

**==> picture [353 x 27] intentionally omitted <==**

leading to minimisers satisfying _γ_[0] = _ϕ_[T] _Fβ,ε_ F� _H_[TB] [ _ργ_ 0]� _ϕ_ . Moreover, minimising _Gβ,µ_ (as defined in (2.7)) over _K_[TB] :=[�] _n_ ⩾0 _[K] n_[TB] leads to the Euler– Lagrange equation _γ_[0] = _ϕ[T] Fβ,µ_ � _H_[TB] [ _ργ_ 0]� _ϕ_ . 

## _2.3. Machine learning_ 

Starting from the _ab initio_ energy (2.1), we have considered a general LDA for the exchange correlation function. Then, restricting the class of admissible one particle density operators to a local basis of atomic-like orbitals, we obtain a tight binding approximation (2.13). In this way, the total energy of the system is now a function of the (finite dimensional) matrices _γ_ TB _∈_ (R _[N]_[b] _[×][N]_[b] ) _[M][×][M]_ . We now restrict the class of admissible density operators to _PN_[ML] el _[⊂P] N_[TB] el (or _KN_[ML] el _[⊂K] N_[TB] el[for finite Fermi-temperature models), a collection of density operators defined] in terms of atom-centred features. 

**Remark 5 (BpopNN).** In the BpopNN [59], the authors take the following approach: for _Becke populations p_ = _{p_ 1 _,..., pM} ∈_ R _[M]_ +[, a corresponding one-particle density operator] _[ γ]_[(] _[p]_[)] belongs to the set 

**==> picture [210 x 23] intentionally omitted <==**

where _ω_ is a smooth weight function concentrated about the origin. In this way, _γ_ ( _p_ ) is a one-particle density operator that minimises the energy subject to the constraint that the corresponding density reproduces the correct Becke populations which may be viewed as 0 _−_ order moment constraints with respect to the measures _ω_ ( _x −_ _**r** i_ )d _x_ for each atom _i_ . 

In this way, the density operator _γ_ ( _p_ ) is a function of the atom centred ‘features’ _{pi}_ , albeit a complicated and likely multi-valued function. 

Motivated by the BpopNN idea but to allow a rigorous analysis we define an explicit mapping from atom-centred features to an admissible density operator. To do this, we expand the effective potential _V_ eff in an atom centred basis and thus write the Hamiltonian of the system as _H_ 0 + _v_ as in (2.16). In this way, _v_ is a function of atom centred features representing the effective potential. This approach is similar to that of [23, 26]. 

Given an atom-centred feature vector � _v_ = _{_ � _vmc}_ where _m_ = 1 _,..., M_ is the atomic index and _c_ belongs to a finite set indexing the features, we write the effective potential as _V_ eff( _x_ ) = � _mc_[�] _[v][mc]_[Ξ] _[mc]_[(] _[x]_[)][ and thus the parameterised effective potential takes the form] 

**==> picture [313 x 26] intentionally omitted <==**

where Ξ = _{_ Ξ _mc_ := Ξ _c_ ( _· −_ _**r** m_ ) _}_ is a collection of atom-centred functions. We let _I_ := _{_ ( _m, c_ ) _}_ be the index set for the atom centred features and write � _vm_ := _{_ � _vmc}c_ for the feature vector on 

9 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

atom _m_ . Throughout this paper, we will assume that these atom-centred functions are exponentially localised: there exists _c_ Ξ _,η_ Ξ _>_ 0 such that 

**==> picture [313 x 14] intentionally omitted <==**

for all _c_ and multi-indices _α ∈_ N[3] with _|α|_ 1 ⩽ _ν_ for some _ν_ ⩾ 2. 

Then, as a function of the features, the tight binding Hamiltonian takes the form _H_ 0 + _v_ where _H_ 0 is given by (2.14) and _v_ is given by (2.19). We now write _λ_ 1( _v_ ) ⩽ _λ_ 2( _v_ ) ⩽ _···_ ⩽ _λM·N_ b( _v_ ) for the ordered eigenvalues of _H_ 0 + _v_ (counting multiplicities), and _C[i]_ ( _v_ ) corresponding normalised eigenvectors. Under this choice, we define 

**==> picture [373 x 52] intentionally omitted <==**

To simplify the presentation, we will consider _non-degenerate γ ∈PN_[ML] el[, where there is a] gap in the spectrum: if _γ_ ( _v_ ) = _ϕ_[T][��] _[N] i_ =[el] 1 _[C][i]_[(] _[v]_[)] _[ ⊗][C][i]_[(] _[v]_[)] � _ϕ_ , for some � _v ∈ ℓ[∞]_ ( _I_ ), we suppose that _λN_ el( _v_ ) _< λN_ el+1( _v_ ). In this case, we have 

**==> picture [353 x 40] intentionally omitted <==**

and the Fermi-level _ε_ F is any value satisfying _λN_ el( _v_ ) _< ε_ F _< λN_ el+1( _v_ ). In the following, we will denote by _Dχ_ ( _−∞,µ_ ) the Jacobian of the map (R _[N]_[b] _[×][N]_[b] ) _[M][×][M] →_ (R _[N]_[b] _[×][N]_[b] ) _[M][×][M]_ defined by _H �→ χ_ ( _−∞,µ_ )( _H_ ). Moreover, we write _V_ eff[ _ρ_ ] := _V_[nuc] + _v_ C _ρ_ + _ε_ xc _[′]_[(] _[ρ]_[)][and][[] _[∇][I][v]_[]] _[mc]_[:=] _∂_ � _v∂mc_ �� _m[′] c[′]_[ �] _[v][m][ ′][c][ ′]_[ ´] _ϕ ⊗ ϕ_ Ξ _m ′c ′_[�] = ´ _ϕ ⊗ ϕ_ Ξ _mc_ . The minimisation of (2.22) over _PN_[ML] el[is well-posed and yields an Euler–Lagrange equation:] **Lemma 3.** _There exists γ_[0] = _ϕ_[T][��] _[N] n_ =[el] 1 _[C][n]_[(] _[v]_[0][)] _[ ⊗][C][n]_[(] _[v]_[0][)] � _ϕ, a minimiser of E over PN_[ML] el _[.] Moreover, if λN_ el( _v_[0] ) _< ε_ F _< λN_ el+1( _v_[0] ) _, then we have_ 

**==> picture [313 x 25] intentionally omitted <==**

_In that case, we also have the following approximation result_ 

**==> picture [313 x 25] intentionally omitted <==**

10 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

_Therefore, if_ Ξ _is a complete basis, we have_ 

**==> picture [313 x 13] intentionally omitted <==**

_where H_[TB] _is given by (_ 2.16 _)._ 

**Sketch of the proof.** First, we note that _E_ is continuous and the space of possible _{C[i]_ ( _v_ ) _}[N] i_ =[el] 1 for � _v ∈ ℓ[∞]_ ( _I_ ) is compact. In particular, there exists a minimiser. Supposing there is a gap in the spectrum, we obtain (2.24) as an Euler–Lagrange equation. We finally obtain (2.25), (2.26) by noting that _Dχ_ ( _−∞,ε_ F)( _H_ 0 + _v_ ) is invertible. 

**Remark 6 (finite Fermi-temperature).** In the finite Fermi-temperature case, we minimise _Eβ_ as defined in (2.7) over the space of density operators of the form _γ_ = _ϕ[T] Fβ,ε_ F( _H_ 0 + _v_ ) _ϕ_ � where _v ∈ ℓ[∞]_ ( _I_ ) and _ε_ F is the unique solution to Tr _Fβ,ε_ F( _H_ 0 + _v_ ) = _N_ el. Minimisers _γ_[0] = _ϕ[T] Fβ,ε_ F( _H_ 0 + _v_[0] ) _ϕ_ satisfy the following Euler–Lagrange equation: 

**==> picture [313 x 25] intentionally omitted <==**

The full proof of this result is contained in the proof of lemma 3 in section 6. 

**Remark 7 (grand canonical ensemble).** For the grand canonical model, we minimise _Gβ,µ_ as defined in (2.9) over the space of density operators of the form _γ_ = _ϕ[T] Fβ,µ_ ( _H_ 0 + _v_ ) _ϕ_ where � _v ∈ ℓ[∞]_ ( _I_ ). Minimisers satisfy the Euler–Lagrange equation (2.27) but with _ε_ F = _µ_ . The proof of this result follows the exact same ideas as in the proof of lemma 3. 

## **3. Results** 

In the foregoing section, we reviewed a general framework for parameterising electronic structure models. In the present section we show how the ‘global many-body’ functionals arising in those models can be decomposed into low-dimensional and spatially localised components. Although our results can be formally applied in the general setting of the previous section, for the sake of simplicity of presentation, we give rigorous statements only for the grand-canonical ensemble setting. We will comment on how to incorporate the charge constraint into the analysis in remarks following the main results. 

We fix the chemical potential _µ_ and inverse Fermi-temperature _β ∈_ (0 _, ∞_ ] and consider the total free energy (2.9) but now written explicitly as a function of the atomic environment and additional atomic features � _v_ : 

**==> picture [313 x 61] intentionally omitted <==**

where _ρ_ ( _**r** ,_ � _v_ ; _x_ ) := 2 _ϕ_ ( _x_ ) _[T] Fβ,µ_ ( _H_ 0 + _v_ ) _ϕ_ ( _x_ ). 

11 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

To simplify the notation, we will from now on omit the parameters ( _β,µ_ ) in _G_ ( _**r** ,_ � _v_ ), and will similarly also write _F_ ( _x_ ) := _Fβ,µ_ ( _x_ ). Moreover, when � _v ∈ ℓ[∞]_ ( _I_ ) is fixed and it is clear from the context, we will write _H_ = _H_ 0 + _v_ , 

**==> picture [289 x 13] intentionally omitted <==**

The spectral gap will be written g := g _−_ + g+ ⩾ 0. 

## _3.1. Locality_ 

We first show that the total energy may be written as a sum of local energy contributions together with an explicit long-range electrostatic term: 

**Theorem 4.** _Fix_ _**r** and_ � _v ∈ ℓ[∞]_ ( _I_ ) _and suppose that either β < ∞ or that_ g _± >_ 0 _. Then, the total energy (_ 3.1 _) may be decomposed as follows:_ 

**==> picture [313 x 23] intentionally omitted <==**

**==> picture [373 x 76] intentionally omitted <==**

_The exponent satisfies η ∼ β[−]_[1] + min _{_ g _−,_ g+ _} as β[−]_[1] + g _→_ 0 _. If β_ = _∞, we have η ∼_ g _as_ g _→_ 0 _._ 

_Similar estimates hold for higher derivatives as long as ν as in (_ 2.12 _),(_ 2.20 _) is sufficiently large._ 

**Sketch of the proof.** First, we take a disjoint union[�][˙] _[M] ℓ_ =1 _[N][ℓ]_[=][ R][3][, and define] 

**==> picture [373 x 53] intentionally omitted <==**

where _G_ ( _x_ ) := _β[−]_[1] log �1 _− F_ ( _x_ )�. For _β < ∞_ , (3.5) is more convenient, while at _β_ = _∞_ , we consider (3.4) (after disregarding the entropy). Moreover, we define 

**==> picture [313 x 22] intentionally omitted <==**

To conclude, we can apply the main ideas of previous works [13, 14, 41, 53] to bound the derivatives of _H �→ F_ ( _H_ ) and _H �→ G_ ( _H_ ) evaluated at _H_ = _H_ 0 + _v_ . A full proof is given in section 6. 

12 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**Remark 8 (canonical ensemble).** The locality estimates break down in the canonical ensemble at finite temperature because the choice of Fermi-level introduces non-locality into the system [13]. 

## _3.2. Body-ordered approximation_ 

Now, approximating _F_ and _G_ as in (3.4) (for _β_ = _∞_ ), (3.5) (for _β < ∞_ ), and (3.6) by polynomials _FN_ and _GN_ of degree at most _N_ , we obtain the following approximate energy: 

**==> picture [373 x 23] intentionally omitted <==**

where 

**==> picture [329 x 65] intentionally omitted <==**

**Remark 9 (locality of the body–ordered approximations).** Following the same proof as theorem 4, one may show that the body-ordered approximations also satisfy the locality estimates (3.3). 

The decomposition (3.7) is a nonlinear body-order expansion: 

**Theorem 5.** _EN,ℓ_ ( _**r** ,_ � _v_ ) _and ρN,ℓ_ ( _**r** ,_ � _v_ ) _are functions of body-order at most_ 2 _N_ + 1 _. Specifically, with_ _**u** ℓ_ := ( _**r** ℓ, Zℓ,_ � _vℓ_ ) _there exist U_[(] _nN[α]_[)][(] _**[u]**[k]_ 1 _[,...,]_ _**[u]**[k] n_[)] _[ ∈]_[(][R] _[N]_[b] _[×][N]_[b][)] _[M][×][M][for][n]_[ =] 0 _,...,_ 2 _N −_ 1 _and α_ = 1 _,_ 2 _and a nonlinear function εℓ_ : (R _[N]_[b] _[×][N]_[b] ) _[M][×][M] →_ R _such that, on defining_ 

**==> picture [313 x 33] intentionally omitted <==**

_we obtain_ 

**==> picture [313 x 34] intentionally omitted <==**

_Moreover, one can write U_[(] _nN[α]_[)][(] _**[u]**[k]_ 1 _[,...,]_ _**[u]**[k] n_[)] _[ℓ][k]_[ =] _[U]_[�][(] _nN[α]_[)][(] _**[u]**[ℓ][k]_[;] _**[u]**[ℓ][k]_ 1 _[,...,]_ _**[u]**[ℓ][k] n_[)] _where_ _**u** ℓk_ := ( _**r** ℓk, Zℓ, Zk,_ � _vℓ,_ � _vk_ ) _._ 

**Sketch of the proof.** The Hamiltonian is 3-body and can thus be written as _Hℓk_ =[�] _p[H][ℓ][kp]_[,] which makes [ _H_[2] ] _ℓk_ =[�] _mpq[H][ℓ][mp][H][mkq]_[ 5-body, and][ [] _[H]_[3][]] _[ℓ][k]_[ =][ �] _pqr[H][ℓ][mp][H][mnq][H][nkr]_[ 7-body. In] general, for all polynomials _PN_ of degree at most _N_ , we have that _PN_ ( _H_ 0 + _v_ ) _ℓk_ are quantities of body-order at most 2 _N_ + 1. In particular, the quantities 

_ρN,ℓ_ ( _**r** ,_ � _v_ ) _,_ tr�( _H_ 0 _− µ_ ) _FN_ ( _H_ 0 + _v_ )� _ℓℓ[,]_ and tr� _GN_ ( _H_ 0 + _v_ ) _− vFN_ ( _H_ 0 + _v_ )� _ℓℓ_ 

have body-order at most 2 _N_ + 1. 

13 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**Remark 10 (canonical ensemble).** In the canonical ensemble, a possible choice for the bodyordered approximation to the Fermi-level, _ε_ F _,N_ , is a solution to the equation 

**==> picture [105 x 13] intentionally omitted <==**

where _FN,β,µ_ is a degree _N_ polynomial approximation to _Fβ,µ_ . Therefore, one must undergo an additional pre-computation step to find an approximate Fermi-level. In this way, the approximate Fermi-level is a nonlinear body-ordered function. That model can still be decomposed into parameterised components that are local and body-ordered components, but the operations performed on those components become more complex. 

## _3.3. Convergence of minimisers_ 

We first note that critical points of the approximate energy satisfy the following Euler– Lagrange equation: 

**Lemma 6.** _If β < ∞, then we approximate G with a polynomial G_ N _of degree at most N, and define FN_ := _GN[′][.][On][the][other][hand,][if][β]_[ =] _[ ∞][,][then][we][simply][approximate][F][with][a] polynomial F_ N _of degree at most N._ 

_Suppose_ � _v[⋆] minimises GN_ ( _**r** ,_ � _v_ ) _(at the fixed geometry_ _**r** ). Then,_ 

**==> picture [313 x 25] intentionally omitted <==**

**Sketch of the proof.** The proof is analogous to that of lemma 3. In section 6 we briefly outline the minor differences. 

We now consider stable critical points � _v[⋆]_ of _G_ : 

**==> picture [313 x 12] intentionally omitted <==**

We wish to approximate � _v[⋆]_ and (hence the corresponding electron density _ρ_ ( _**r** ,_ � _v[⋆]_ )) with solutions � _v[⋆] N_[to][the][approximate][energy] _[G][N]_[(and][the][corresponding][density] _[ρ][N]_[(] _**[r]**[,]_[�] _[v][⋆] N_[)][).][To][do] so, we require the following result about the convergence of the polynomial approximations _FN_ and _GN_ : 

**Lemma 7.** _Fix µ ∈_ R _, β ∈_ (0 _, ∞_ ] _, X_ := [ _σ, µ −_ g _−_ ] _∪_ [ _µ_ + g+ _, σ_ ] _⊂_ R _, and_ g := g _−_ + g+ _. Then, for N sufficiently large, there exists θ > 0 and polynomial approximations G_ N _and FN_ := _GN[′][such that]_ 

**==> picture [173 x 16] intentionally omitted <==**

_where θ ∼ β[−]_[1] + _[√]_ g _−_ ~~_√_~~ g+ _as β[−]_[1] + g _→_ 0 _. If β_ = _∞, we have θ ∼_ g _as_ g _→_ 0 _._ 

**Proof.** The proof uses logarithmic potential theory, see [48] for an overview of the general setting. For details of this theory applied to the particular functions _F_ and _G_ , see [55]. 

With this result at hand, we define the _GN_ as in (3.7) using _FN_ and _GN_ from lemma 7. Then, we may approximate � _v[⋆]_ with critical points of _GN_ . The following result is a direct consequence of regular perturbation theory. 

14 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**Theorem 8.** _Suppose_ � _v[⋆] is a stable critical point of G. Then, there exists C >_ 0 _such that for θN >_ 2log _M_ + _C, there exists a critical point_ � _v[⋆] N[of][ G][N][ such that]_ 

**==> picture [219 x 16] intentionally omitted <==**

_Moreover, we have_ 

**==> picture [133 x 14] intentionally omitted <==**

**Remark 11.** The dependence on system size _M_ is a weakness of our current results, preventing the analysis from being extended to the bulk limit. It is unclear to us whether this is a worst-case that is in principle attainable for some systems, or whether a stronger generally valid estimate can be proven. This is a possible direction for future study. 

## **4. Numerical experiments** 

We now present a preliminary numerical study to demonstrate that one can construct systematically improvable machine learning models for systems with long-range charge equilibration effects, based on the results of section 3. 

- (1) There exist functions _EN,ℓ_ ( _**r** ,_ � _v_ ) and _ρN,ℓ_ ( _**r** ,_ � _v_ ) which are local in the sense of theorem 4 and can be used to approximate the total free energy as in (3.2), 

- (2) By theorem 5, _EN,ℓ_ ( _**r** ,_ � _v_ ) and _ρN,ℓ_ ( _**r** ,_ � _v_ ) have body-order of at most 2 _N_ + 1 in the features _**u** k_ = ( _**rk** , Zk,_ � _vk_ ), 

- (3) Finally, the approximate free energy converges with increasing body-order, as stated rigorously in theorem 8. 

To demonstrate these statements in practice, one can extract the total energy, electron density and atomic features _**u** k_ from quantum mechanical calculations and fit the functions _EN,ℓ_ ( _**r** ,_ � _v_ ) and _ρN,ℓ_ ( _**r** ,_ � _v_ ) using machine learned, body-ordered functions. 

## _4.1. Implementation details_ 

First, we make the following design choices: 

- The local basis functions _ϕℓa_ , in which the electron density is expanded, are Gaussian-type orbitals and are the same for all chemical elements: 

**==> picture [259 x 22] intentionally omitted <==**

where ( _λ,µ_ ) is an angular momentum index tuple, _Rλµ_ is a real solid harmonic. 

- 

- _•_ The effective potential features _vℓ_ and the effective potential _V_ ( _x_ ) are connected via a projection: 

**==> picture [305 x 23] intentionally omitted <==**

where _ψnλµ_ is once again a Gaussian type orbital, but now with variable width _σn_ indexed by _n_ . As the range of _n_ and _λ_ grows, more information about the local effective potential is encoded in � _vℓ_ . 

15 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**Remark 12.** For the analysis, we needed _V_ to be a function of � _v_ so found it more convenient to work with the expansion, _V_ ( _x_ ) =[�] _ℓa_[�] _[v][ℓ][a]_[Ξ] _[ℓ][a]_[(] _[x]_[)][rather][than][the][projection][(][4.1][).][In] particular, the problem of solving (4.1) for _V_ is a complicated ill-posed inverse problem. However, both these approaches are equivalent if both sets of basis functions _{_ Ξ _ℓa}_ and _{ϕℓa}_ are orthogonal. 

- The effective potential _V_ = _V_ eff[ _ρ_ ] is evaluated using a smeared nuclei approximation, and by also neglecting the exchange correlation contribution: 

**==> picture [305 x 24] intentionally omitted <==**

## _4.2. Extracting ρ and_ � _v from DFT calculations_ 

A coarse-grained electron density was extracted by partitioning the total electron density of the DFT calculation, _ρ_[DFT] , onto atom centred functions with angular momentum indices ( _λ,µ_ ), giving atomic charges, dipoles and quadrupoles. Further details on this process are given in appendix C. Terms with _λ >_ 2 were not used. 

These atom centred quantities are then interpreted as the coefficients _ρ_[DFT] _ℓ,λµ_[in][a][coarse-] grained model of the system: 

**==> picture [313 x 24] intentionally omitted <==**

The task of predicting the charge density is then to predict the coefficients _ρ_[DFT] _ℓ,λµ_[.][From][this] surrogate charge distribution one can compute a coarse-grained potential at the solution of the DFT calculation through (4.2) and thus the features � _v_[DFT] _ℓ,λµ_[via (][4.1][).] 

## _4.3. Parameterisation of Eℓ and ρℓ_ 

_EN,ℓ_ and _ρN,ℓ_ are explicitly constructed as body-ordered functions of the features _**u** k_ = ( _**rk** , zk,_ � _vk_ ) of neighbouring atoms, through a flexible functional form which is fitted to a dataset. In particular, we used elements from the MACE equivariant message passing network architecture [7]. Full details are given in appendix B. 

## _4.4. Results clusters of water_ 

DFT calculations were performed on a dataset of 4800 small clusters of water molecules with the FHI-aims DFT code [10], using the PBE exchange correlation functional [43]. The total energy and electron density can be fitted with the above framework. 

The function _ρN,ℓ_ ( _**r** , v_ ) can be trained directly against _{_ _**u** k}k_ extracted from DFT. The function _Eℓ_ ( _**r** , v_ ) is instead fitted via the total energy of the water cluster and its gradients with respect to nuclear coordinates _{∂E_ tot _/∂_ _**r** ℓ}ℓ_ . These gradients are accessible from the DFT calculation as nuclear forces. As in the main result (3.2), the total energy also contains the Hartree energy, which can be computed from the coarse-grained density (4.3). 

16 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**==> picture [373 x 187] intentionally omitted <==**

**Figure 1.** Convergence of the fitted functions _EN,ℓ_ and _ρN,ℓ_ as a function of the number of electric potential features ˆ _v_ per atom and the body-order of the functions. Convergence of the PES is assessed by the accuracy of the nuclear forces. Convergence of the density is assessed by the error in the partitioned density coefficients in equation (4.3). These quantities are multipole moments and have units of charge _×_ length _[λ]_ . The number of electric potential features per atom is restricted by considering only _{ψnλµ}_ for _n_ ⩽ _n_ max, _λ_ ⩽ _λ_ max, and _−λ_ ⩽ _µ_ ⩽ _λ_ (so that the number of features is _n_ max( _λ_ max + 1)[2] ). For the plots, we take ( _n_ max _,λ_ max) = (0 _,_ 0), (1, 0), (2, 1), and (3, 2). 

Figure 1 shows the convergence of this scheme with respect to the number of electric potential features per atom (the range of _n_ and _λ_ in (4.1)), and the body-order of the functions _EN,ℓ_ and _ρN,ℓ_ . 

## **5. Conclusions** 

We rigorously demonstrated the possibility of decomposing a general electronic structure PES into local and body-ordered components, even in the presence of long-range charge equilibration effects. This was achieved by first discretising Kohn–Sham DFT in a basis of localised orbitals, resulting in a tight-binding-like formulation. The key idea then was to introduce an internal atom-centred variable (or, feature), resulting in an extended potential energy landscape representing the effective potential. By equilibrating the new internal variable (i.e. achieving self-consistency) our local model is capable of representing non-trivial long-range effects. Our formulation is closely related to extended variables in classical charge equilibration [46, 47], or the Becke populations in [59]. We construct body-ordered approximations to the selfconsistent solutions and prove an exponential rate of convergence as we increase the maximal body-order. 

## **6. Proofs** 

We recall here that _f_ ≲ _g_ means that _f_ ⩽ _Cg_ for some constant _C_ , independent of system size _M_ . When we wish to denote explicit dependencies, we use the notation _f_ ≲ _D g_ ; there exists a constant _CD_ depending on _D_ (but not on _M_ ) such that _f_ ⩽ _CDg_ . 

17 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

## _6.1. Preliminaries_ 

We first state an elementary result that we will use throughout: 

**Lemma 9.** _For_ 0 _< η_ 1 ⩽ _···_ ⩽ _ηn and {_ _**r** m}[M] m_ =1 _[⊂]_[R] _[d][ where M]_[ ⩾] _[n or M]_[ =] _[ ∞][, we have]_ 

**==> picture [313 x 57] intentionally omitted <==**

_where rij_ := _|_ _**r** j −_ _**r** i|._ 

**Proof.** We first show (6.1). We first note that[�] _[n] l_ =1 _[|][x][ −]_ _**[r]**[l][|]_[ ⩾] 2[1] � _r_ 12 + _r_ 23 + _···_ + _rn_ 1�. In particular, we have 

**==> picture [286 x 42] intentionally omitted <==**

We sketch the proof of (6.2); more details can be found in [54, appendix B.3]. After defining m := min _i_ = _j rij_ , we have _Bm_ := _Br_ 2 _m_ ( _**r**_ 2) _∩ B_ m _/_ 2( _**r** m_ ) are disjoint sets with _r_ 2 _m_ ⩾ _|x −_ _**r**_ 2 _|_ for all _x ∈Bm_ and _|Bm|_ ⩾ _cd_ m _[d]_ . In particular, we obtain 

**==> picture [359 x 71] intentionally omitted <==**

which concludes the proof. 

For the remainder, we will assume that min _i_ = _j rij_ ⩾ m _>_ 0, which allows us to apply lemma 9 with prefactors that only depend on the configuration via m. 

Next, we show that the tight binding Hamiltonian is exponentially localised: 

**Lemma 10.** _Fix_ _**r** and_ � _v ∈ ℓ[∞]_ ( _I_ ) _, and write H_ = _H_ 0 + _v. Then, there exists ηH >_ 0 _, such that_ 

**==> picture [373 x 25] intentionally omitted <==**

_where ηH depends on ηϕ,η_ Ξ _from (_ 2.12 _), (_ 2.20 _)._ 

**Proof.** Recall, _Hℓk,ab_ = ´ _∇ϕℓa · ∇ϕkb_ +[�] _mc_[�] _[v][mc]_ ´ _ϕℓaϕkb_ Ξ _mc_ . In particular, applying (2.12), (2.20) together with lemma 9, we obtain the first bound in (6.3) with the exponent 1 2[min] _[{][η][ϕ][,η]_[Ξ] _[ }]_[.] 

18 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

On defining _V_ ( _x_ ) :=[�] _mc_[�] _[v][mc]_[Ξ] _[mc]_[, we have] 

**==> picture [373 x 91] intentionally omitted <==**

**==> picture [373 x 61] intentionally omitted <==**

which concludes the proof. 

Next, we state properties of the Jacobian, _DFβ,µ_ , of _H �→ Fβ,µ_ ( _H_ ): 

**Lemma 11.** _Fix β ∈_ (0 _, ∞_ ] _, µ ∈_ R _, and a symmetric matrix H ∈_ (R _[N]_[b] _[×][N]_[b] ) _[M][×][M] . In the case β_ = _∞, we suppose µ ∈_ conv� _σ_ ( _H_ )� _\ σ_ ( _H_ ) _. Then, DFβ,µ_ ( _H_ ) _is negative definite with respect to the Frobenius inner product._ 

**Proof.** This elementary proof uses the same idea as in [32], and is included here for completeness. 

If _β_ = _∞_ , we suppose _C_ is a simple closed contour encircling _σ_ ( _H_ ) _∩_ ( _−∞,µ_ ) and avoiding the rest of the spectrum. On the other hand, if _β < ∞_ , we suppose _C_ is a simple closed contour encircling _σ_ ( _H_ ) and avoiding the poles of _Fβ,µ_ at _µ_ + _i πβ[−]_[1] (2Z + 1). Then, we have 

**==> picture [373 x 112] intentionally omitted <==**

with the convention that _Fβ,µ_ ( _x_ ) _x−−xFβ,µ_ ( _x_ ) := _Fβ,ε[′]_ F[(] _[x]_[)][and] _[σ]_[(] _[H]_[) =] _[ {][λ]_[1][ ⩽] _[···]_[ ⩽] _[λ][N]_ b _[·][M][}]_[.][In] particular, we have 

**==> picture [313 x 55] intentionally omitted <==**

which concludes the proof. 

19 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

If _β_ = _∞_ , then one obtains bounds on the spectrum of _−DF∞,µ_ ( _H_ ): 

**==> picture [198 x 25] intentionally omitted <==**

where _λN_ el _< µ < λN_ el+1. 

We recall the Combes–Thomas [16] resolvent estimate (the following particular form is taken from [53], while variants may be found in [13, 14, 41]): 

**Lemma 12 (Combes–Thomas resolvent estimate).** _Suppose that H ∈_ (R _[N]_[b] _[×][N]_[b] ) _[M][×][M] is symmetric with_ �� _Hℓk,ab_ �� ⩽ _cH_ e _−ηH rℓk (for some cH,ηH >_ 0 _) for all ℓ, k ∈{_ 1 _,..., M} and a, b ∈ {_ 1 _,..., N_ b _}. Then, if z ∈_ C _with_ d := dist� _z,σ_ ( _H_ )� _>_ 0 _, we have_ 

**==> picture [313 x 46] intentionally omitted <==**

_and c > 0 depends on_ min _ℓ_ = _k[r][ℓ][k][ and d.]_ 

Applying the polynomial approximation result (lemma 7), together with the Combes– Thomas estimate, we obtain the following result: 

**Lemma 13.** _Fix_ _**r** and_ � _v ∈ ℓ[∞]_ ( _I_ ) _, and write H_ = _H_ 0 + _v. Suppose that, if β_ = _∞, then_ g _± >_ 0 _. Then, for both O_ = _F and G, the polynomial approximations ON_ = _FN and G_ N _as in lemma_ 7 _satisfy the following: there exists θ,η_ ct _>_ 0 _such that_ 

**==> picture [313 x 37] intentionally omitted <==**

_for_ 0 ⩽ _j_ ⩽ _ν. Moreover, θ ∼ β[−]_[1] + _[√]_ g _−_ ~~_√_~~ g+ _and η_ ct _∼ β[−]_[1] + min _{_ g _−,_ g+ _} as β[−]_[1] + g _→_ 0 _. If β_ = _∞, we have θ,η ∼_ g _as_ g _→_ 0 _._ 

**Proof.** The Hamiltonian _H_ := _H_ 0 + _v_ satisfies the assumption of lemma 12 with _cH_ ≲ 1 + � _∥v∥ℓ∞_ and _ηH_ =[1] 2 _[η][ϕ]_[.] Moreover, a simple calculation reveals that, on defining _Rz_ := ( _z −H_ ) _[−]_[1] and thus 

**==> picture [326 x 39] intentionally omitted <==**

where [∆ _ℓkab_ ] _ℓ ′k ′,a ′b ′_ := _δℓℓ ′δkk ′δaa ′δbb ′_ , we have 

**==> picture [334 x 24] intentionally omitted <==**

where _C_ is a simple closed positively oriented contour encircling _σ_ ( _H_ ) and avoiding the singularities of _O_ . That is, for both _O_ = _F_ and _G_ , the contour must be contained in C _\ {µ_ + _ir_ : _r ∈_ R _, |r|_ ⩾ _πβ[−]_[1] _}_ . 

20 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

Therefore, applying (6.8), we obtain 

**==> picture [313 x 77] intentionally omitted <==**

where d _,η_ ct are the constants from lemma 12 applied to _H_ = _H_ 0 + _v_ , and _∥O∥C_ := len _C_ max _z∈C[|][O]_[(] _[z]_[)] _[|]_[.] 

Moreover, we similarly obtain the second inequality in (6.10) by noting that the polynomial approximation result of lemma 7 may be extended to obtain [55]: 

**==> picture [83 x 12] intentionally omitted <==**

In fact, one uses the Hermite integral formula [56] and the proof follows in the exact same way as lemma 7. 

As a direct corollary, we have the following result: 

**Corollary 14.** _Under the assumptions and notation from lemma_ 13 _, and for w_[(][1][)] _,..., w_[(] _[j]_[)] _with |w_[(] _ℓ[l] k_[)] _,ab[|]_[ ⩽] _[c][l]_[e] _[−][η][l]_[d] _[l]_[(] _**[r]**[ℓ][,]_ _**[r]**[k]_[)] _[for some c][l][,η][l][ >]_[ 0] _[, we have]_ 

**==> picture [276 x 35] intentionally omitted <==**

_where η_ = 2[1][min] _[{][η]_[ct] _[,η]_[1] _[,...,η][j][}][,][ η]_[ct] _[is the constant from lemma]_[ 13] _[, and]_[ d] _[l][is symmetric with] rℓk_ ⩽ d _l_ ( _**r** ℓ,_ _**r** k_ ) ⩽ _rℓm_ + d _l_ ( _**r** m,_ _**r** k_ ) _for all ℓ, k, m and l_ = 1 _,..., j._ 

_Moreover, in the case w_[(] _[l]_[)] :=[�] _mc[w]_[�] _mc_[(] _[l]_[)] ´ _ϕ ⊗ ϕ_ Ξ _mc for l_ = 1 _,..., j and_ 0 ⩽ _j_ ⩽ _ν, we have_ � _cl_ = _∥w_[(] _[l]_[)] _∥ℓ∞ and ηl_ =[1] 2 _[η][ϕ][.]_ 

**Remark 13.** In the main proofs, we will either apply corollary 14 with d( _**r** ℓ,_ _**r** k_ ) := _rℓk_ , d( _**r** ℓ,_ _**r** k_ ) := _rℓm_ + _rmk_ for fixed _m_ , or d( _**r** ℓ,_ _**r** k_ ) := _|_ _**r** ℓ − x|_ + _|x −_ _**r** k|_ for fixed _x_ . 

**Proof.** We directly apply lemma 13 to conclude 

**==> picture [373 x 101] intentionally omitted <==**

where d _ℓk_ := d( _**r** ℓ,_ _**r** k_ ). The summation in the square brackets in (6.12) is finite (independent of system size) by a repeated application of lemma 9. 

21 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**==> picture [373 x 67] intentionally omitted <==**

Here, we have applied lemma 9. 

## _6.2. Proofs of the main results_ 

**Proof of lemma 3.** We shall consider the finite and zero Fermi-temperature cases together by considering _Eβ_ as defined in (2.7) (allowing for the _β_ = _∞_ case). 

Firstly, we note that _Eβ_ is a continuous function of � _v_ : the mapping taking � _v_ to _H_ 0 + _v_ is affine, while the mapping from _H_ 0 + _v_ onto the ordered eigenpairs is continuous. Therefore � _v �→ γ_ TB _,ργ_ are both continuous, and thus the composition � _v �→ γ �→Eβ_ ( _γ_ ) is continuous. Moreover, the set of admissible density operators is compact and thus there exists a minimiser _γ_[0] . 

If _β_ = _∞_ then we assume there is a gap in the spectrum. Therefore, we have _γ_[0] = _ϕ[T] Fβ,ε_ F( _H_ 0 + _v_ ) _ϕ_ for some � _v ∈ ℓ[∞]_ ( _I_ ). In the zero Fermi-temperature case, _ε_ F is any value in the spectral gap, whereas for _β < ∞_ , the Fermi level _ε_ F is the unique solution to Tr _Fβ,ε_ F( _H_ 0 + _v_ ) = _N_ el. This equation has a unique solution since the mapping _τ �→_ Tr _Fβ,τ_ ( _H_ 0 + _v_ ) is strictly increasing with Tr _Fβ,τ_ ( _H_ 0 + _v_ ) _→_ 0 (resp. _M · N_ b) as _τ →−∞_ (resp. _τ →_ + _∞_ ). 

Rewriting the total energy, we have 

**==> picture [313 x 52] intentionally omitted <==**

where _σ_ ( _H_ 0 + _v_ ) = _{λi}_ . Moreover, we fix the numbering of the eigenvalues so that the functions � _v �→ λi_ are differentiable for each _i_ . 

In order to compute the derivatives of _Eβ_ , we require the derivatives of the eigenvalues: 

**==> picture [312 x 51] intentionally omitted <==**

The first term of (6.14) is zero due to the normalisation of the eigenvectors _∥C[i] ∥ℓ_ 2 = 1. 

Now, we note that at zero Fermi-temperature _ε_ F can be fixed constant in a neighbourhood of � _v_ . At finite Fermi-temperature, we differentiate the constraint Tr _Fβ,ε_ F( _H_ 0 + _v_ ) = _N_ el and apply (6.14), to obtain 

**==> picture [313 x 26] intentionally omitted <==**

We now may differentiate the first term of (6.13), 

22 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**==> picture [372 x 137] intentionally omitted <==**

Here, we have used the fact that _S[′]_ ( _x_ ) = log 1 _−x x_[, and thus] _[ S][′]_[�] _Fβ,ε_ F( _x_ )� = _−β_ ( _x − ε_ F). In the final line, we have applied (6.15). 

On the other hand, derivatives of the final term in (6.13) involve derivatives of the electron density: 

**==> picture [312 x 55] intentionally omitted <==**

In particular, combining (6.16), (6.17), we obtain 

**==> picture [373 x 58] intentionally omitted <==**

concluding the proof of (2.24). 

We move on to consider (2.25). To simplify notation, we write _g_ :=[�] _mc_[�] _[v][mc]_[Ξ] _[mc][ −][V]_[eff][[] _[ρ][γ]_[]][.] First, we note by lemma 11, that _−DFβ,ε_ F := _−DFβ,ε_ F( _H_ 0 + _v_ ) is positive definite and thus has a positive square root ( _−DFβ,ε_ F)[1] _[/]_[2] with inverse ( _−DFβ,ε_ F) _[−]_[1] _[/]_[2] . Then, by (6.18), we have 

**==> picture [372 x 112] intentionally omitted <==**

which concludes the proof of (2.25). 

23 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

The analogous results in the grand-canonical ensemble can be shown in the exact same way (but are simpler). 

**Proof of theorem 4.** We consider _Nℓ ⊂_ R[3] such that R[3] =[�] _[M] ℓ_ =1 _[N][ℓ]_[with][ (] _[N][ℓ]_[)] _[ℓ]_[pairwise dis-] joint and dist( _**r** m, Nℓ_ ) ⩾ 2[1] _[r][ℓ][m]_[ for all] _[ ℓ,][m]_[. Then, we may define] 

**==> picture [313 x 23] intentionally omitted <==**

**==> picture [373 x 25] intentionally omitted <==**

Therefore, we have (3.2) with _E_ el[ _ρ_ ] = ´ � _ρV_[nuc] +[1] 2 _[ρ][v]_[C] _[ρ]_ �. In the zero Fermi-temperature case, we may neglect the entropy contribution altogether, whereas, at finite Fermi-temperature, we have _xF_ ( _x_ ) + _β[−]_[1] _S_ ( _F_ ( _x_ )) = _µF_ ( _x_ ) + _β[−]_[1] log �1 _− F_ ( _x_ )�, and thus 

**==> picture [313 x 25] intentionally omitted <==**

where _G_ ( _x_ ) := _β[−]_[1] log �1 _− F_ ( _x_ )�. In the zero Fermi-temperature limit, one recovers (6.21). Therefore, in order to prove the locality estimates, we need to show that derivatives of the functions _x �→ F_ ( _x_ ) and _x �→ G_ ( _x_ ) evaluated at _H_ 0 + _v_ are exponentially localised. To do this, we simply apply lemma 13. In previous works [13, 14, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to13, 14, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to, 14, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to 14, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to 41, 53], the Combes–Thomas estimate (lemma 12) is applied to, 53], the Combes–Thomas estimate (lemma 12) is applied to 53], the Combes–Thomas estimate (lemma 12) is applied to], the Combes–Thomas estimate (lemma 12) is applied to 12) is applied to) is applied to obtain the exponential localisation of the local observables _O_ ( _H_ ) _ℓℓ_ where _x �→ �→ O_ ( _x_ ) is analytic is analytic in a neighbourhood of _σ_ ( _H_ ). Here, we extend the analysis to the off-diagonal entries. Here, we extend the analysis to the off-diagonal entries _O_ ( _H_ ) _ℓkk_ . _∂ ∂ ∂ T_ To simplify notation in the following, we write _∂_ ( _**r** m,_ � _vm_ )[:=] � _∂_ _**r** m[,] ∂_ � _vm_ � _._ Since, by lemma 10 we have ��� _∂∂_ ( _H_ _**r** mℓ,k_ � _v,mab_ ) ��� ≲ (1 + _∥_ � _v∥ℓ∞_ )e _−ηH_ d _ℓk_ where d _ℓk_ := _rℓm_ + _rmk_ , we apply corollary 14 to conclude 

In previous works [13, 14, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to13, 14, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to, 14, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to 14, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to, 41, 53], the Combes–Thomas estimate (lemma 12) is applied to 41, 53], the Combes–Thomas estimate (lemma 12) is applied to, 53], the Combes–Thomas estimate (lemma 12) is applied to 53], the Combes–Thomas estimate (lemma 12) is applied to], the Combes–Thomas estimate (lemma 12) is applied to 12) is applied to) is applied to obtain the exponential localisation of the local observables _O_ ( _H_ ) _ℓℓ_ where _x �→ �→ O_ ( _x_ ) is analytic is analytic in a neighbourhood of _σ_ ( _H_ ). Here, we extend the analysis to the off-diagonal entries. Here, we extend the analysis to the off-diagonal entries _O_ ( _H_ ) _ℓkk_ . 

**==> picture [363 x 31] intentionally omitted <==**

where _η_ ct is the constant from lemma 13. 

**==> picture [373 x 120] intentionally omitted <==**

24 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

Returning to the electron density (6.20), we therefore obtain 

**==> picture [313 x 81] intentionally omitted <==**

Therefore, derivatives of the site energies have analogous locality properties. In the _β_ = _∞_ case, we have 

**==> picture [312 x 59] intentionally omitted <==**

whereas, for _β < ∞_ , we have 

**==> picture [372 x 58] intentionally omitted <==**

In both cases, we therefore have 

**==> picture [313 x 45] intentionally omitted <==**

which concludes the proof. Here, we have used the assumption _|ε_ xc _[′]_[(] _[ρ]_[)] _[|]_[ ≲] _[|][ρ][|]_[1] _[/]_[3][and] _|ρ_ ( _**r** ,_ � _v_ ; _x_ ) _|_ ⩽ _N_[2] b _[c]_[2] _ϕ[c]_[1] � _ℓk_[e] _[−][η][ϕ]_[ [] _[|][x][−]_ _**[r]**[ℓ][|]_[+] _[|][x][−]_ _**[r]**[k][|]_[]][e] _[−][η]_[0] _[r][ℓ][k]_[≲][1.] 

**Remark 14.** As mentioned in remark 9, the body-ordered approximations as defined in (3.7) inherit the same locality properties as in theorem 4. To show this, one may follow the same proof with �� _ON_ ( _H_ ) _ℓk_ �� ⩽ _c_ 0e _−η_ 0 _rℓk_ and �� _∂∂O_ ( _N_ _**r** m_ ( _H,_ � _vm_ ) _ℓ_ ) _k_ �� ⩽ _c_ 1e _−η_ 1[ _rℓm_ + _rmk_ ] for _ON ∈{FN, GN}_ and some _c_ 0 _, c_ 1 _,η_ 0 _,η_ 1 _>_ 0 (which follows directly from lemma 13). 

**Proof of theorem 5.** Since _vℓk,ab_ =[�] _mc_[�] _[v][mc]_ ´ _ϕℓa_ Ξ _mc ϕkb_ , on writing _H_ := _H_ 0 + _v_ , we have 

**==> picture [373 x 55] intentionally omitted <==**

a quantity of body-order at most 3. In particular, we may write _Hℓk_ =[�] _m[H][ℓ][km]_[where] _[ H][ℓ][km]_ has body-order at most 3 (in the combined variables _{_ ( _**r** m,_ � _vm_ ) _}m_ ). Therefore, polynomials of 

25 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

the Hamiltonian also have finite body-order: 

**==> picture [353 x 30] intentionally omitted <==**

a quantity of body-order at most 2 _N_ + 1. That is, there exists _**U**_[(] _N_[1][)][as in (][3.8][) such that] _[ F][N]_[(] _[H]_[0][ +] _v_ ) = _**U**_[(] _N_[1][)][. See [][55][], for an explicit definition of the] _[ U]_[(] _nN_[1][)][. In particular, we have (][3.9][), and thus] the nonlinearity in (3.10) is given by 

**==> picture [148 x 25] intentionally omitted <==**

Since both _FN_ ( _H_ ) and _GN_ ( _H_ ) have body-order at most 2 _N_ + 1, the quantities 

**==> picture [313 x 25] intentionally omitted <==**

are both of body-order at most 2 _N_ + 1. 

**Proof of lemma 6.** The proof follows the exact same argument as in lemma 3, where, in the finite Fermi-temperature case, we require _GN[′]_[=] _[ F][N]_[.] 

**Proof of theorem 8.** _Preliminaries._ Define _TN_ : _ℓ[∞]_ ( _I_ ) _→ ℓ[∞]_ ( _I_ ) where the index set is defined as _I_ := _{_ ( _m, c_ ) _}_ by 

**==> picture [313 x 25] intentionally omitted <==**

where _v_ :=[�] _mc_[�] _[v][mc]_ ´ _ϕ ⊗ ϕ_ Ξ _mc_ and _ρN_ ( _x_ ) := _ϕ_ ( _x_ ) _[T] FN_ ( _H_ 0 + _v_ ) _ϕ_ ( _x_ ). Moreover, recall _V_ eff[ _ρ_ ] := _V_[nuc] + _v_ C _ρ_ + _ε_ xc _[′]_[(] _[ρ]_[)][.] 

We apply the inverse function theorem on _TN_ about _v_[�] _[⋆]_ : if there exist _δ, L,εN, c_ stab _,N >_ 0 such that 

(i) _TN_ : _ℓ[∞]_ ( _I_ ) _→ ℓ[∞]_ ( _I_ ) continuous, continuously differentiable on _Bδ_ ( _v_[�] _[⋆]_ ), 

(ii) Lipschitz: _∥DTN_ ( _v_ �1) _− DTN_ ( _v_ �2) _∥_ ⩽ _L∥v_ �1 _− v_ �2 _∥_ for all _v_ �1 _,_ � _v_ 2 _∈ Bδ_ ( _v_[�] _[⋆]_ ), 

(iii) Consistency: _∥TN_ ( _v[⋆]_ ) _∥_ ⩽ _εN_ , (iv) Stability: _DTN_ ( _v_[�] _[⋆]_ ) is non-singular with _∥DTN_ ( _v_[�] _[⋆]_ ) _[−]_[1] _∥_ ⩽ _c_ stab _,N_ , 

(v) Newton–Kantorovich condition: 2 _c_[2] stab _,N[ε][N][L][ <]_[ 1,] (vi) 2 _c_ stab _,NεN < δ_ , 

then the Newton iteration starting at _v_[�] _[⋆]_ is well-defined and converges quadratically to _v_[�] _[⋆] N_[, a] unique solution to _TN_ = 0 on _B∥·∥ℓ∞_ ( _v_[�] _[⋆]_ ; 2 _c_ stab _,NεN_ ) [28, 61]. Define _T_ : _ℓ[∞]_ ( _I_ ) _→ ℓ[∞]_ ( _I_ ) by 

**==> picture [313 x 25] intentionally omitted <==**

where _ρ_ ( _x_ ) := _ϕ_ ( _x_ ) _[T] F_ ( _H_ 0 + _v_ ) _ϕ_ ( _x_ ). In order to simplify the presentation, we will first show that _(i)–(vi)_ result from the following: there exist _c_ 0 _, c_ 1 _, c_ 2 _, c_ 3 _, c_ 4 _>_ 0 such that 

**==> picture [313 x 14] intentionally omitted <==**

26 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

and, for all � _v ∈ Bδ_ ( _v_[�] _[⋆]_ ), we have 

**==> picture [313 x 61] intentionally omitted <==**

The proof of (6.34)–(6.38) will follow the conclusion of the proof of theorem 8. 

(i) Since _FN_ is a polynomial, and � _v �→ H_ 0 + _v_ is smooth, _TN_ is smooth on _ℓ[∞]_ ( _I_ ). (ii) For fixed _v_ �0 _,_ � _v_ 1 _∈ B∥·∥ℓ∞_ ( _v_[�] _[⋆]_ ; _δ_ ), we define _v_ � _t_ := _tv_ �1 + (1 _− t_ ) _v_ �0, and use (6.36) to conclude 

**==> picture [300 x 41] intentionally omitted <==**

(iii) Consistency: by (6.37), we have _∥TN_ ( _v_[�] _[⋆]_ ) _∥ℓ∞_ = _∥_ ( _T − TN_ )( _v_[�] _[⋆]_ ) _∥ℓ∞_ ⩽ _c_ 3 _M_ e _[−][θ][N]_ =: _εN_ . 

(iv) Stability: We have _∥DT_ ( _v_[�] _[⋆]_ ) _[−]_[1] _∥_ ⩽ _c_ stab. Therefore, for _c_ 4 _M_ e _[−][θ][N]_ ⩽ 2 _c_ 1stab[,][we][apply] (6.38) to conclude 

**==> picture [298 x 22] intentionally omitted <==**

Therefore, for such _N_ , _DTN_ ( _v_[�] _[⋆]_ ) is invertible with 

**==> picture [257 x 13] intentionally omitted <==**

(v), (vi) With the choices of _δ, L,εN, c_ stab _,N >_ 0 as above, we require 

**==> picture [298 x 30] intentionally omitted <==**

_Conclusion:_ Therefore, there exists _C_ = _C_ ( _c_ stab _, c_ 0 _, c_ 1 _, c_ 2 _, c_ 3 _, c_ 4) _>_ 0 such that if 

**==> picture [73 x 10] intentionally omitted <==**

then there exists _v_[�] _[⋆] N_[such that] _[ T][N]_[(] _[v]_[ �] _[⋆] N_[) =][ 0 and] 

**==> picture [175 x 13] intentionally omitted <==**

_Density:_ We have _|ρN_ (� _v[⋆] N_[;] _[x]_[)] _[ −][ρ]_[(][�] _[v][⋆]_[;] _[x]_[)] _[|]_[ ≲][e] _[−][θ][N]_[ +] _[ |][ρ]_[(][�] _[v] N[⋆]_[;] _[x]_[)] _[ −][ρ]_[(][�] _[v][⋆]_[;] _[x]_[)] _[|]_[and,][using][the][same] argument as in lemma 13, we conclude 

27 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**==> picture [373 x 67] intentionally omitted <==**

where _η_ ct _,η_ ct _,N_ are the constants from lemma 12 when applied to _H_ 0 + _v[⋆]_ and _H_ 0 + _v[⋆] N_[, respect-] ively, and we have applied (6.47), below. _Energy:_ By applying lemma 13 and similar arguments as in (6.43), we have 

**==> picture [373 x 46] intentionally omitted <==**

where _η_ := 4[1][min] _[{][η]_[ct] _[,][N][,η]_[ct] _[,η][ϕ][}]_[. In particular, one may show that] 

**==> picture [313 x 50] intentionally omitted <==**

� where _ξ_ ( _x_ ) _∈_ � _ρN_ ( _v[⋆] N_[;] _[x]_[)] _[,ρ]_[(][�] _[v][⋆]_[;] _[x]_[)] � and, in the final line, we have applied (6.43). 

_6.3. Proof of (6.34)–(6.38)_ 

For � _v ∈ ℓ[∞]_ ( _I_ ), we define _V_ ( _x_ ) :=[�] _mc_[�] _[v][mc]_[Ξ] _[mc]_[(] _[x]_[)][ and] _[ v]_[ =] ´ _ϕ ⊗ ϕ V_ , _ρ_ ( _x_ ) := _ϕ_ ( _x_ ) _[T] F_ ( _H_ ) _ϕ_ ( _x_ ), and _ρN_ ( _x_ ) := _ϕ_ ( _x_ ) _[T] FN_ ( _H_ ) _ϕ_ ( _x_ ) where _H_ := _H_ 0 + _v_ . 

**Proof of (6.34).** We first note that 

**==> picture [373 x 64] intentionally omitted <==**

where 

**==> picture [222 x 29] intentionally omitted <==**

and 1 ⩽ _p, q,_ ⩽ _∞_ with[1] _p_[+][1] _q_[=][ 1.] 

Recall that g( _v_ ) := max � _σ_ ( _H_ 0 + _v_ ) _∩_ ( _−∞,µ_ ]� _−_ min � _σ_ ( _H_ 0 + _v_ ) _∩_ [ _µ, ∞_ )�. By (6.46), we have g( _v_ ) ⩾[1] 2[g][(] _[v][⋆]_[)][ for all][�] _[v][ ∈][B][∥·∥] ℓ[∞]_[(] _[v]_[ �] _[⋆]_[;] _[δ]_[)][ where] _[ δ]_[ :=] _[ c]_[0] _[M][−]_ 2[1] and _c_ 0 :=[g] 4[(] _C[v] ∞[⋆]_[)][. Therefore,] on _B∥·∥ℓ∞_ ( _v_[�] _[⋆]_ ; _δ_ ), the mapping � _v �→ F_ ( _H_ 0 + _v_ ) is smooth and thus � _v �→ T_ (� _v_ ) is smooth. 

In order to prove (6.35)–(6.38), we require the following basic facts: 

**==> picture [313 x 15] intentionally omitted <==**

28 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**Proof.** �� _vℓk,ab_ �� ⩽ � _mc[c]_[2] _ϕ[c]_[Ξ] _[ |]_[�] _[v][mc][|]_ ´ e _[−][η][ϕ]_[[] _[|][x][−]_ _**[r]**[ℓ][|]_[+] _[|][x][−]_ _**[r]**[k][|]_[]] _[−][η]_[Ξ] _[ |][x][−]_ _**[r]**[m][|]_ ≲ _∥_ � _v∥ℓ[∞]_ e _[−]_[1] 2 _[η][ϕ][ r][ℓ][k]_ . Here, the final inequality follows from lemma 9. 

For all _x ∈_ R[3] , and _η >_ 0, we have 

**==> picture [313 x 27] intentionally omitted <==**

**Proof.** For fixed _r >_ 0, the left hand side of (6.48) may be bounded above by 

**==> picture [284 x 56] intentionally omitted <==**

We conclude by choosing _r_ :=[1] 4[[] _[|]_ _**[r]**[ℓ][−][x][|]_[ +] _[ |][x][ −]_ _**[r]**[k][|]_[]][.] 

Finally, we have 

**==> picture [313 x 26] intentionally omitted <==**

**Proof.** First, we note that _|ρ_ ( _x_ ) _|_ ≲[�] _ℓk_[e] _[−][η][ϕ]_[ [] _[|][x][−]_ _**[r]**[ℓ][|]_[+] _[|][x][−]_ _**[r]**[k][|]_[]][e] _[−][η]_[ct] _[r][ℓ][k]_[≲][e] _[−][η][ϕ]_[min] _[ℓ][|][x][−]_ _**[r]**[ℓ][|]_[. Therefore,] applying (6.48), we have 

**==> picture [353 x 29] intentionally omitted <==**

The _V_[nuc] term in the effective potential also satisfies this bound. Moreover, we have �� _ε_ xc� _ρ_ ( _x_ )��� ≲ _|ρ_ ( _x_ ) _|_ 1 _/_ 3 ≲ 1. Therefore, we obtain the first bound in (6.49). The second follows in the same way by using lemma 13 and noting _|ρ_ ( _x_ ) _− ρN_ ( _x_ ) _|_ ≲ e _[−][θ][N]_ e _[−][η][ϕ]_[min] _[ℓ][|][x][−]_ _**[r]**[ℓ][|]_ . 

**Proof of (6.37).** From (6.32), (6.33), we have 

**==> picture [373 x 53] intentionally omitted <==**

We simply apply corollary 14, together with (6.47), (6.49), (6.48), to conclude 

**==> picture [373 x 64] intentionally omitted <==**

which concludes the proof of (6.37). 

29 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

Now we move on to consider the derivatives of _TN_ and _T_ : first note that 

**==> picture [312 x 25] intentionally omitted <==**

Therefore, taking derivatives of (6.32), we have 

**==> picture [373 x 81] intentionally omitted <==**

where _δV_ eff[ _ρ_ ] _f_ := _v_ C _f_ + _ε_ xc _[′′]_[(] _[ρ]_[)] _[f]_[.][A][similar][formula][for] _[DT][N]_[results][by][replacing] _[F]_[with] _[F][N]_ and _ρ_ with _ρN_ . 

**Proof of (6.35).** First, applying corollary 14, together with (2.12), we obtain 

**==> picture [312 x 69] intentionally omitted <==**

Similarly, we have �� _⟨DF_ ( _H_ ) _ϕ_ ( _x_ ) _⊗ ϕ_ ( _x_ ) _, w⟩_ �� ≲ _∥w_ � _∥ℓ∞_ e _−_[1] 4[min] _[{][η]_[ct] _[,η][ϕ][}]_ 1⩽min _ℓ_ ⩽ _M[|][x][−]_ _**[r]**[ℓ][|]_ . Therefore, again applying corollary 14, together with (6.47), (6.48), we obtain 

**==> picture [373 x 96] intentionally omitted <==**

which concludes the proof. 

**Proof of (6.38).** Simplifying the notation by omitting _H_ 0 + _v_ in the notation for _F_ and _FN_ , we have 

**==> picture [300 x 53] intentionally omitted <==**

30 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**==> picture [283 x 91] intentionally omitted <==**

In particular, by following the exact same arguments to that of the proof of (6.35), we obtain the desired estimate. More specifically, each term in (6.57) may be bounded above by similar terms from (6.54), but with additional factors of e _[−][θ][N]_ coming from the difference between _F_ and _FN_ (and their derivatives) and _ρ_ and _ρN_ . 

Moreover, we have 

**==> picture [373 x 146] intentionally omitted <==**

where _DF, D_[2] _F, D_[3] _F_ are all evaluated at _H_ 0 + _v_ and _δ_[2] _V_ eff[ _ρ_ ][ _f, g_ ] := _ε_ xc _[′′′]_[(] _[ρ]_[)] _[fg]_[. Similarly, we] have the same expression for _TN_ when _F_ is replaced with _FN_ and _ρ_ with _ρN_ . 

**Proof of (6.36).** Similarly to (6.55), we apply corollary 14 to obtain 

**==> picture [373 x 88] intentionally omitted <==**

Again, we apply corollary 14, together with (6.47)–(6.49) and (6.55), (6.59), (6.60), we obtain 

31 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

**==> picture [369 x 101] intentionally omitted <==**

which concludes the proof. 

## **Data availability statement** 

No new data were created or analysed in this study. 

## **Acknowledgments** 

JT is supported by EPSRC Grant EP/W522594/1. CO is supported by NSERC Discovery Grant GR019381 and NFRF Exploration Grant GR022937. WB thanks the AFRL for funding through grant FA8655-21-1-7010. This work utilised computational resources from the ARCHER2 UK National Supercomputing Service (http://www.archer2.ac.uk) which is funded by EPSRC the membership of the UK Car-Parrinello Consortium. We also utilised the Cambridge Service for Data Driven Discovery (CSD3). 

## **Appendix A. Notation** 

Here we summarise the key notation: 

- _**r**_ = _{_ _**r** ℓ}[M] ℓ_ =1 _[⊂]_[R] _[d]_[ : atomic positions,] 

- _**r** ℓk_ := _**r** k −_ _**r** ℓ_ and _rℓk_ := _|_ _**r** ℓk|_ : relative atomic positions, 

- _Z_ = _{Zℓ}[M] ℓ_ =1[: atomic species] 

- _δij_ : Kronecker delta ( _δij_ = 0 for _i ̸_ = _j_ and _δii_ = 1), 

- Id _n_ : _n × n_ identity matrix, 

- _| · |_ : absolute value on R _[d]_ or C, 

- _| · |_ : Frobenius matrix norm on R _[n][×][n]_ , 

- _a · b_ =[�] _i[a][i][ b][i]_[ : dot product of real vectors,] 

- _A_ : _B_ =[�] _ij[A][ij][B][ij]_[ : Frobenius inner product of real matrices,] 

- _A_[T] : transpose of the matrix _A_ , 

- Tr : trace of an operator, 

- _f ∼ g_ as _x → x_ 0 _∈_ R _∪{±∞}_ or C _∪{∞}_ : there exists an open neighbourhood _N_ of _x_ 0 and positive constants _c_ 1 _, c_ 2 _>_ 0 such that _c_ 1 _g_ ( _x_ ) ⩽ _f_ ( _x_ ) ⩽ _c_ 2 _g_ ( _x_ ) for all _x ∈ N_ , 

- _C_ : generic positive constant that may change from one line to the next, independent of system size _M_ , 

- _f_ ≲ _g_ : _f_ ⩽ _Cg_ for some generic positive constant, independent of system size _M_ , 

- N0 = _{_ 0 _,_ 1 _,_ 2 _,... }_ : Natural numbers including zero, 

- _δ_ : Dirac delta, distribution satisfying _⟨δ, f⟩_ = _f_ (0), 

32 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

- _∥f∥L∞_ ( _X_ ) := sup _x∈X |f_ ( _x_ ) _|_ : sup-norm of _f_ on _X_ , 

- dist( _z, A_ ) := inf _a∈A |z − a|_ : distance between _z ∈_ C and the set _A ⊂_ C, 

- _a_ + _bS_ := _{a_ + _bs_ : _s ∈ S}_ : Minkowski addition, 

- [�][˙] _i[A][i]_[ : union of pairwise disjoint sets] _[ A][i]_[,] 

- [ _ψ_ ] _ℓ_ : the _ℓ_[th] entry of the vector _ψ_ , 

- _∥ψ∥ℓ_ 2 := �� _k[|]_[[] _[ψ]_[]] _[k][|]_[2][�][1] _[/]_[2][ :] _[ ℓ]_[2][-norm of] _[ ψ]_[,] 

- tr _A_ :=[�] _ℓ[A][ℓℓ]_[: trace of matrix] _[ A]_[,] 

- _∥A∥_ max := max _ℓ,k |Aℓk|_ : max-norm of the matrix _A_ , 

- _σ_ ( _T_ ) : the spectrum of the operator _T_ , 

- _σ_ disc( _T_ ) _⊂ σ_ ( _T_ ) : isolated eigenvalues of finite multiplicity, 

- _σ_ ess( _T_ ) := _σ_ ( _T_ ) _\ σ_ disc( _T_ ) : essential spectrum, 

- _∥T∥X→Y_ := sup _x∈X,∥x∥X_ =1 _∥Tx∥Y_ : operator norm of _T_ : _X → Y_ , 

- _∇v_ : Jacobian of _v_ : R[Λ] _→_ R[Λ] , 

- [ _a, b_ ] := _{_ (1 _− t_ ) _a_ + _tb_ : _t ∈_ [0 _,_ 1] _}_ : closed interval between _a, b ∈_ R _[d]_ or _a, b ∈_ C, 

- _b_ 

- _•_ ´ _a_[:=] ´[ _a,b_ ][: integral over the interval][ [] _[a][,][b]_[]][ for] _[ a][,][b][ ∈]_[C][,] 

- len( _C_ ) : length of the simple closed contour _C_ , 

- supp _ν_ : support of the measure _ν_ , set of all _x_ for which every open neighbourhood of _x_ has non-zero measure, 

- conv _A_ := _{ta_ + (1 _− t_ ) _b_ : _a, b ∈ A, t ∈_ [0 _,_ 1] _}_ : convex hull of _A_ , 

- _Sn_ = _{σ_ : _{_ 1 _,..., n} →{_ 1 _,..., n}_ : _σ_ bijective _}_ : symmetric group of order _n_ . 

## **Appendix B. Machine learned parameterisation** _**Eℓ**_ **and** _**ρℓ**_ 

In this appendix, we describe the parameterisation of _EN,ℓ_ and _ρN,ℓ_ as body-ordered functions of _**u** k_ in more detail. The construction is a natural variation of the MACE architecture [7], and related to the equivariant ACE model [18]. An in-depth study of our proposed architecture and its generalisations goes beyond the scope of this work; our intention is only to demonstrate the significant potential of a self-consistent ML interatomic potential model. 

In the following, atoms are indexed by _i_ and _j_ , rather than _ℓ_ and _k_ to avoid clashes with standard notation in equivariant networks. 

## _B.1. Construction of body-ordered atom-centred features_ 

For atom _i_ , let the neighbourhood of atom _i_ , denoted _N_ ( _i_ ), be the set atoms which are within a fixed cutoff distance _r_ cut from atom _i_ . The environment around atom _i_ is encoded by constructing a set of learnable features _**h** i_ as functions of all neighbouring atoms. 

These features are denoted by _hi,kLM_ , where _k_ = 1 _,..., K_ indexes independent channels, and ( _L_ , _M_ ) is an angular momentum tuple. The features are equivariant with respect to rotations of the structure: if the underlying set of atomic positions _{_ _**r** i}_ is rotated according to _{_ _**r** i} →{R_ _**r** i}_ for some rotation _R_ , then the components of _**h** i_ transform according to the Wigner matrix corresponding to _R_ : 

**==> picture [107 x 24] intentionally omitted <==**

33 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

The features _hi,kLM_ are constructed as follows: firstly, the chemical element of each atom, _zi_ , is encoded by mapping each distinct element to a vector of length _K_ , via a set of weights _W_ : 

**==> picture [71 x 23] intentionally omitted <==**

The electric potential descriptors � _vi,nlm_ of atom _i_ are then introduced to create initial features. This is done by first linearly mixing the radial channels to create a vector of length _K_ , followed by multiplying with the species vector _ai,k_ : 

**==> picture [118 x 50] intentionally omitted <==**

Following this, we describe the identity and relative position of each neighbour _j_ of atom _i_ by calculating the _one-particle basis_ for the pair of atoms: 

**==> picture [211 x 24] intentionally omitted <==**

ˆ ˆ where _**r** ij_ := _**r** j −_ _**r** i_ = _rij_ _**r** ij_ with _|_ _**r** ij|_ = 1 and _rij_ ⩾ 0, _Y[m] l_[is a real spherical harmonic and each] _Rηl_ 1 _m_ 1 _l_ 2 _m_ 2( _r_ ) is a learnable function of the distance _r_ . This operation is inherited directly from the MACE MLIP framework, and combines the length and direction of the vector _**r** ij_ with equivariant features _h_[0] _j,kl_ 2 _m_ 2[on][the][neighbouring][atom,][while][preserving][the][equivariance][of] the output. The index _η_ appears since there may be more than one way to combine a given pair of vectors with angular momentum ( _l_ 1 _, l_ 2) to get an object with angular momentum _l_ 3. Further discussion can be found in [7, 18, 31]. 

The edge descriptors _ϕij,kηlm_ are then combined to form many body, atom centred descriptors. Firstly, atomic features are created by summing over the neighbours of each atom, and applying a linear map to mix between independent channels: 

**==> picture [197 x 25] intentionally omitted <==**

The initial features of atom _i_ are also added into _Ai,klm_ , since otherwise no information about atom _i_ ’s electric potential would be present in _Ai,klm_ . 

Secondly, products are taken between atomic features _Ai,klm_ and themselves to form many body descriptors. Specifically, products of up to _ν_ copies of _Ai,klm_ are formed, while controlling the behaviour of the output under rotations: 

**==> picture [128 x 30] intentionally omitted <==**

where _Cη[LM] ν_ _**lm**_[is the ‘generalised’ Clebsch–Gordan coefficient, which combines a set of] _[ ν]_[cop-] ies of _Ai,klm_ and generates an output which transforms in the same way as the _Y[M] L_[spherical] harmonic [7, 18]. The number of terms in the product is the number of neighbouring atoms which the features _B[ν]_ simultaneously depend on in a non-trivial way. Therefore, _ν_ controls the _body-order_ of the features, with _B[ν]_ having body-order _ν_ + 1, with the 1 coming from the central atom. 

34 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

The index _ην_ appears because for a given set of _{_ ( _lξ, mξ_ ) _}ξ_ , there can be multiple ways to form a product with a given behaviour under rotations. As with the one-particle basis, this many body product has been discussed and analysed previously [7, 31]. 

The final features describing the geometry around each atom are a linear mapping of these many body objects, summing over product order _ν_ : 

**==> picture [169 x 24] intentionally omitted <==**

where _W_ and _W_[˜] are again learnable weights. In a MACE model, the above process is repeated, with the features _hi,kLM_ replacing the chemical elements _ai,k_ , to iteratively construct a richer description of the geometry. In this study we do not iterate, which is equivalent to using a single ‘layer’ MACE model. The motivation for using only single layer is that when using multiple layers, the features on atom _i_ can depend on more distant atoms since each layer distributes information locally. In this case, we would rather that information about distant atoms is communicated only through the electric potential. 

## _B.2. Parameterising E_ 

Given features _hi,kLM_ , the energy _Ei_ is predicted by applying a on-layer multi-layer perceptron to the invariant parts of _hi,kLM_ . Explicitly: 

**==> picture [218 x 31] intentionally omitted <==**

Where _ψ_ is an activation function, which in this case was a sigmoid linear unit (SiLU): _ψ_ ( _x_ ) = 1+ _x_ e _[−][x]_[. If] _[ ν]_[is fixed during feature construction,] _[ E][i]_[ will have body-order] _[ ν]_[ +][ 1.] 

## _B.3. Parameterising ρ_ 

The electron density is expanded in an atom centred basis, and the model must predict the coefficients of this expansion. Specifically, let _ρi,lm_ ( _**r** , v_ ˆ) denote the ( _l_ , _m_ ) component of the density expansion on atom _i_ . This is parameterised as a linear map of the atomic features: 

**==> picture [102 x 22] intentionally omitted <==**

which has body-order _ν_ + 1. 

## _B.4. Hyperparameters_ 

For the demonstrations in this study, all models used an embedding size of _K_ = 128, a neighbourhood cutoff of 4 Å, and atomic features _hi,kLM_ were constructed for _L_ ⩽ 2. 

## **Appendix C. Charge density partitioning in FHI-aims** 

In FHI-aims, the electron density is partitioned onto atom centred contributions via partitioning functions _pℓ_ ( _**r**_ ) which satisfy[�] _ℓ[p][ℓ]_[(] _**[r]**_[) =][ 1. This allows one to coarse grain the electron density] 

35 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

_n_ ( _**r**_ ) into atomic multipole moments: 

**==> picture [220 x 25] intentionally omitted <==**

FHI-aims uses these atomic multipole moments to represent the contribution to the Hartree potential from atom _ℓ_ at points far from atom _ℓ_ . The functions _pℓ_ are determined by an atomcentred weight function _gℓ_ ( _**r**_ ) whereby _pℓ_ = _gℓ/_ ([�] _ℓ[g][ℓ]_[)][. In this work, the default weighting] function of FHI-aims was used which is described in [52]. 

## **ORCID iDs** 

Jack Thomas  0000-0001-8800-3406 Christoph Ortner  0000-0003-1498-8120 

## **References** 

- [1] Anantharaman A and Cancès E 2009 Existence of minimizers for Kohn–Sham models in quantum chemistry _Ann. Inst. Henri Poincare_ **26** 2425–55 

- [2] Artrith N, Morawietz T and Behler J 2011 High-dimensional neural-network potentials for multicomponent systems: applications to zinc oxide _Phys. Rev. B_ **83** 153101 

- [3] Aubin T 1982 _Nonlinear Analysis on Manifolds. Monge-Ampère Equations_ (Springer) 

- [4] Bartók A P, Kondor R and Csányi G 2013 On representing chemical environments _Phys. Rev. B_ **87** 184115 

- [5] Bartók A P, Payne M C, Kondor R and Csányi G 2010 Gaussian approximation potentials: the accuracy of quantum mechanics, without the electrons _Phys. Rev. Lett._ **104** 136403 

- [6] Bartók A P, De S, Poelking C, Bernstein N, Kermode J R, Csányi G and Ceriotti M 2017 Machine learning unifies the modeling of materials and molecules _Sci. Adv._ **3** e1701816 

- [7] Batatia I, Kovacs D P, Simm G, Ortner C and Csányi G 2022 MACE: higher order equivariant message passing neural networks for fast and accurate force fields _Advances in Neural Information Processing Systems_ vol 35 pp 11423–36 

- [8] Batzner S, Musaelian A, Sun L, Geiger M, Mailoa J P, Kornbluth M, Molinari N, Smidt T E and Kozinsky B 2022 E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials _Nat. Commun._ **13** 2453 

- [9] Benzi M, Boito P and Razouk N 2013 Decay properties of spectral projectors with applications to electronic structure _SIAM Rev._ **55** 3–64 

- [10] Blum V, Gehrke R, Hanke F, Havu P, Havu V, Ren X, Reuter K and Scheffler M 2009 Ab initio molecular simulations with numeric atom-centered orbitals _Comput. Phys. Commun._ **180** 2175–96 

- [11] Bris C L 1993 Quelques problèmes mathématiques en chimie quantique moleculaire _PhD Thesis_ Thèse de l’Ecole Polytechnique 

- [12] Butler K T, Davies D W, Cartwright H, Isayev O and Walsh A 2018 Machine learning for molecular and materials science _Nature_ **559** 547–55 

- [13] Chen H, Lu J and Ortner C 2018 Thermodynamic limit of crystal defects with finite temperature tight binding _Arch. Ration. Mech. Anal._ **230** 701–33 

- [14] Chen H and Ortner C 2016 QM/MM methods for crystalline defects. Part 1: locality of the tight binding model _Multiscale Model. Simul._ **14** 232–64 

- [15] Chen J and Martínez T J 2007 QTPIE: charge transfer with polarization current equalization. A fluctuating charge model with correct asymptotics _Chem. Phys. Lett._ **438** 315–20 

- [16] Combes J and Thomas L 1973 Asymptotic behavior of eigenfunctions for multiparticle Schrödinger operators _Commun. Math. Phys._ **34** 251–70 

- [17] Drautz R 2019 Atomic cluster expansion for accurate and transferable interatomic potentials _Phys. Rev. B_ **99** 014104 

36 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

- [18] Drautz R 2020 From electrons to interatomic potentials for materials simulations _Topology, Entanglement and Strong Correlations_ ed E Pavarini and E Koch (Forschungszentrum Jülich GmbH, Institute for Advanced Simulation) ch 3 

- [19] Faraji S, Ghasemi S A, Rostami S, Rasoulkhani R, Schaefer B, Goedecker S and Amsler M 2017 High accuracy and transferability of a neural network potential through charge equilibration for calcium fluoride _Phys. Rev. B_ **95** 104105 

- [20] Finnis M 2003 _Interatomic Forces in Condensed Matter_ (Oxford University Press) 

- [21] Gao A and Remsing R C 2022 Self-consistent determination of long-range electrostatics in neural network potentials _Nat. Commun._ **13** 1572 

- [22] Ghasemi S A, Hofstetter A, Saha S and Goedecker S 2015 Interatomic potentials for ionic systems with density functional accuracy based on charge densities obtained by a neural network _Phys. Rev. B_ **92** 045131 

- [23] Gonze X 1996 Towards a potential-based conjugate gradient algorithm for order-N self-consistent total energy calculations _Phys. Rev. B_ **54** 4383–6 

- [24] Grisafi A and Ceriotti M 2019 Incorporating long-range physics in atomic-scale machine learning _J. Chem. Phys._ **151** 204105 

- [25] Hartree D R 1928 The wave mechanics of an atom with a non-Coulomb central field. Part I. Theory and methods _Math. Proc. Camb. Phil. Soc._ **24** 89–110 

- [26] Herbst M F and Levitt A 2022 A robust and efficient line search for self-consistent field iterations _J. Comput. Phys._ **459** 111127 

- [27] Hohenberg P and Kohn W 1964 Inhomogeneous electron gas _Phys. Rev._ **136** B864–71 

- [28] Kantorovich L V 1948 On Newton’s method for functional equations _Dokl. Akad. Nauk SSSR_ **59** 1237–40 

- [29] Ko T W, Finkler J A, Goedecker S and Behler J 2021 A fourth-generation high-dimensional neural network potential with accurate electrostatics including non-local charge transfer _Nat. Commun._ **12** 398 

- [30] Kohn W and Sham L J 1965 Self-consistent equations including exchange and correlation effects _Phys. Rev._ **140** A1133–8 

- [31] Kovács D P, Batatia I, Arany E S and Csányi G 2023 Evaluation of the MACE force field architecture: from medicinal chemistry to materials science _J. Chem. Phys._ **159** 044118 

- [32] Levitt A 2020 Screening in the finite-temperature reduced Hartree–Fock model _Arch. Rat. Mech. Anal._ **238** 901–27 

- [33] Lieb E H 1981 Variational principle for many-fermion systems _Phys. Rev. Lett._ **46** 457–9 

- [34] Lieb E H and Simon B 1977 The Hartree–Fock theory for Coulomb systems _Commun. Math. Phys._ **53** 185–94 

- [35] Lions P 1987 Solutions of Hartree-Fock equations for Coulomb systems _Commun. Math. Phys._ **109** 33–97 

- [36] Mermin N D 1965 Thermal properties of the inhomogeneous electron gas _Phys. Rev._ **137** A1441–3 

- [37] Mortier W J, Genechten K V and Gasteiger J 1985 Electronegativity equalization: application and parametrization _J. Am. Chem. Soc._ **107** 829–35 

- [38] Mortier W J, Ghosh S K and Shankar S 1986 Electronegativity-equalization method for the calculation of atomic charges in molecules _J. Am. Chem. Soc._ **108** 4315–20 

- [39] Musil F, Grisafi A, Bartók A P, Ortner C, Csányi G and Ceriotti M 2021 Physics-inspired structural representations for molecules and materials _Chem. Rev._ **121** 9759–815 

- [40] Ortner C and Thomas J 2020 Point defects in tight binding models for insulators (arXiv:2004. 05356) 

- [41] Ortner C, Thomas J and Chen H 2020 Locality of interatomic forces in tight binding models for insulators _ESAIM Math. Model. Numer. Anal._ **54** 2295–318 

- [42] Parr R G and Weitao Y 1994 _Density-Functional Theory of Atoms and Molecules_ (Oxford University Press) 

- [43] Perdew J P, Burke K and Ernzerhof M 1996 Generalized gradient approximation made simple _Phys. Rev. Lett._ **77** 3865–8 

- [44] Perun S, Sobolewski A L and Domcke W 2006 Conical intersections in thymine _J. Phys. Chem. A_ **110** 13238–44 

- [45] Prodan E and Kohn W 2005 Nearsightedness of electronic matter _Proc. Natl Acad. Sci._ **102** 11635–8 

- [46] Rappe A K and Goddard W A 1991 Charge equilibration for molecular dynamics simulations _J. Phys. Chem._ **95** 3358–63 

37 

Nonlinearity **38** (2025) 095024 

J Thomas _et al_ 

- [47] Rick S W, Stuart S J and Berne B J 1994 Dynamical fluctuating charge force fields: application to liquid water _Chem. Phys._ **101** 6141–56 

- [48] Saff E B 2010 Logarithmic potential theory with applications to approximation theory _Surv. Approx. Theory_ **5** 165–200 

- [49] Shao Y _et al_ 2015 Advances in molecular quantum chemistry contained in the Q-Chem 4 program package _Mol. Phys._ **113** 184–215 

- [50] Shapeev A V 2016 Moment tensor potentials: a class of systematically improvable interatomic potentials _Multiscale Model. Simul._ **14** 1153–73 

- [51] Solovej J P 1991 Proof of the ionization conjecture in a reduced Hartree–Fock model _Invent. Math._ **104** 291–311 

- [52] Stratmann R, Scuseria G E and Frisch M J 1996 Achieving linear scaling in exchange-correlation density functional quadratures _Chem. Phys. Lett._ **257** 213–23 

- [53] Thomas J 2020 Locality of interatomic interactions in self-consistent tight binding models _J. Nonlinear Sci._ **30** 3293–319 

- [54] Thomas J 2021 Analysis of an _ab initio_ Potential Energy Landscape _PhD Thesis_ University of Warwick 

- [55] Thomas J, Chen H and Ortner C 2022 Body-ordered approximations of atomic properties _Arch. Rat. Mech. Anal._ **246** 1–60 

- [56] Trefethen L N 2019 _Approximation Theory and Approximation Practice Extended Edition_ 

- [57] Vieuxmaire O P J, Lan Z, Sobolewski A L and Domcke W 2008 Ab initio characterization of the conical intersections involved in the photochemistry of phenol _J. Chem. Phys._ **129** 224307 

- [58] Wilmer C E, Kim K C and Snurr R Q 2012 An extended charge equilibration method _J. Phys. Chem. Lett._ **3** 2506–11 

- [59] Xie X, Persson K A, Small D W and Small D W 2020 Incorporating electronic information into machine learning potential energy surfaces via approaching the ground-state electronic energy as a function of atom-based electronic populations _J. Chem. Theory Comput._ **16** 4256–70 

- [60] Yao K, Herr J E, Toth D W, Mckintyre R and Parkhill J 2018 The TensorMol-0.1 model chemistry: a neural network augmented with long-range physics _Chem. Sci._ **9** 2261–9 

- [61] Zhengda H 1993 A note on the Kantorovich theorem for Newton iteration _J. Comput. Appl. Math._ **47** 211–7 

38 

