PHYSICAL REVIEW E **111** , 045308 (2025) 

## 

Namu Kroupa,[1][,][2][,][3][,][*] Gábor Csányi © ,[3] and Will Handley © 2,4 

> 1 _Astrophysics Group, Cavendish Laboratory, J.J. Thomson Avenue, Cambridge CB3 0HE, United Kingdom_ 

> 2 _Kavli Institute for Cosmology, Madingley Road, Cambridge CB3 0HA, United Kingdom_ 

> 3 _Engineering Laboratory, University of Cambridge, Cambridge CB2 1PZ, United Kingdom_ 

> 4 _Institute of Astronomy, University of Cambridge, Madingley Road CB3 0HA, United Kingdom_ 

(Received 27 December 2024; accepted 7 April 2025; published 22 April 2025) 

In high dimensions, reflective Hamiltonian Monte Carlo with inexact reflections exhibits slow mixing when the particle ensemble is initialized from a Dirac _δ_ distribution and the uniform distribution is targeted. By quantifying the instantaneous nonuniformity of the distribution with the Sinkhorn divergence, we elucidate the principal mechanisms underlying the mixing problems. In spheres and cubes, we show that the collective motion transitions between fluidlike and discretization-dominated behavior, with the critical step size scaling as a power law in the dimension. In both regimes, the particles can spontaneously unmix, leading to resonances in the particle density and the aforementioned problems. Additionally, low-dimensional toy models of the dynamics are constructed which reproduce the dominant features of the high-dimensional problem. Finally, the dynamics is contrasted with the exact Hamiltonian particle flow and tuning practices are discussed. 

DOI: 10.1103/PhysRevE.111.045308 

## **I. INTRODUCTION** 

Reflective Hamiltonian Monte Carlo with inexact reflections (RHMC) is an algorithm used to sample from uniform distributions in R _[n]_ . Originally introduced to perform slice sampling [1], it was later adopted within the nested sampling algorithm [2] to calculate the normalizing constant of a probability distribution, for which it is used in the physical sciences, such as in Bayesian inference and materials science [3–7]. Inexact reflections are necessary when the boundary of the uniform distribution is not known _a priori_ and solving numerically for the intersection of a particle trajectory with the boundary to perform exact reflections is computationally prohibitive. Several variations of the algorithm have been proposed [1,8,9], differing in the way the reflection is performed and the time at which the momentum of a particle is randomized. 

However, in the context of nested sampling, it is observed that RHMC introduces a negative systematic error in the normalizing constant which increases in magnitude with the dimensionality of the distribution [10,11]. The algorithm therefore does not seem to scale beyond _O_ (10) dimensions in practice, which has been attributed to poor mixing [10] and the curse of dimensionality [11]. It has been observed that the addition of Gaussian noise to the particle momentum leads to a decrease in the error [10], thus rendering the dy- 

*Contact author: nk544@cam.ac.uk 

_Published by the American Physical Society under the terms of the Creative Commons Attribution 4.0 International license. Further distribution of this work must maintain attribution to the author(s) and the published article’s title, journal citation, and DOI._ 

namics diffusive and lowering the degree of coherence in a Markov chain. However, it has remained elusive why coherence induces the observed problems in the first place. While existing algorithms not using gradient information, notably hit-and-run slice sampling [12], do not exhibit such an error [13], the overall increase in availability of gradient information due to automatic differentiation frameworks [14,15] paired with an inflation in parameter space dimensionality [16] has increased interest in algorithms which utilize gradients in an effective manner. This is particularly the case within computational materials science, wherein forces are already necessary for molecular dynamics simulations [17] and reaching the thermodynamic limit is a primary aim. While the suboptimal performance of RHMC has prompted changes in how the reflective update is conducted [9], the precise cause has remained unidentified and consequently unaddressed to date. 

The problem is exacerbated by the fact that, in contrast to the usual setting of Markov chain Monte Carlo, in which a chain is run until the burn-in time is reached and correlations between subsequent samples are removed by appropriate subsampling [18], the application in nested sampling falls into the many-short-chains regime, in which multiple chains are run in parallel until a single sufficiently decorrelated sample per chain is obtained. More specifically, the chains are initialized from a mixture of Dirac distributions centered at a prepared set of points inside a volume, called live points, from which current state-of-the-art implementations initialize chains in parallel. Typically the number of live points is set proportional to _n_ and number of chains is chosen to be greater than or equal to the number of live points. To isolate the mixing problems, we initialize a large number of chains from a single point, corresponding to a setting with a single live point and many parallel processors. A setting with multiple live points thus 

2470-0045/2025/111(4)/045308(17) 

045308-1 

Published by the American Physical Society 

KROUPA, CSÁNYI, AND HANDLEY 

PHYSICAL REVIEW E **111** , 045308 (2025) 

amounts to an equally weighted superposition of the particle densities observed in our setting. However, even when the number of live points scales linearly with _n_ , an exponential proliferation of minima in realistic energy landscapes [19–22] causes the live point population to drop below a single live point per basin on average. Since basins become ergodically separated during a nested sampling run, our setting of a single isolated live point becomes typical. Hence, even in a practical setting, the question of convergence therefore reduces to the short time-scale mixing of an ensemble of particles. 

In this respect, guarantees for asymptotic convergence, as provided by ergodic theorems, are uninformative. Instead, we require tight bounds on the mixing time of RHMC, which do not exist for the setting under consideration. Typically, an upper bound on the mixing time is dependent on the warmness of the initial distribution [23], which quantifies a notion of the difference from the stationary distribution. For a Dirac _δ_ initialization, the warmness is infinite. Application of the results in Refs. [24–27], which provide an upper bound in terms of the warmness, therefore give a vacuous upper bound on the mixing time. Instead, the particle distribution after one step of the algorithm may be used, which renders the warmness finite. However, the bounds also depend on the conductance of the Markov chain, for which there are currently no results available to the authors’ knowledge. 

We therefore measure the mixing of the Markov chain computationally. For this, we use the Sinkhorn divergence (SD) to quantify the distance of the density of an ensemble of particles to the uniform distribution and track the SD as a function of time. We focus on an instance of RHMC known as Galilean Monte Carlo (GMC) [8] as it is most prevalently used in practice [5,28]. The alternative variant known as reflective slice sampling [1], which rerandomizes the momentum upon rejection of a step, follows the same dynamics as GMC in the sphere as the dynamics is rejection-free. We investigate mixing in the sphere and cube in _n_ dimensions, which pose tractable cases due to their high symmetry. We study the dynamics in the sphere as it is relevant to the case of isotropic probability distributions in nested sampling and slice sampling. Moreover, linear statistical models with Gaussian errors on the data have Gaussian likelihoods in parameter space. For nonlinear models, the Laplace approximation around the maximum likelihood estimator yields a Gaussian. In the context of Boltzmann sampling in computational materials science, a harmonic approximation of a minimum in the potential energy surface leads to the Gaussian case as well. Since current state-of-the-art nested sampling codes map nonisotropic Gaussian distributions to an isotropic one via a coordinate transformation [13], the sphere is an archetypal case to be investigated. The investigation is extended to the cube as its faces are flat. In applications, flat boundaries occur in polytope volume calculations [29,30], Hamiltonian Monte Carlo on discontinuous distributions [31], when nested sampling is used for distributions with discrete parameters [32,33] and in toy problem likelihoods with plateaus [34]. 

The paper is structured as follows. Section II introduces GMC and SD. In Secs. III and IV, the dynamics of GMC in the sphere and cube is analysed, respectively, and discussed in Sec. VI. The paper concludes with Sec. VII. Appendices A– C provide derivations, Appendix D shows additional results 

**==> picture [216 x 114] intentionally omitted <==**

FIG. 1. Possible moves of the GMC Markov chain. A particle starting at **q** ( _t_ ) with momentum **p** ( _t_ ) inside a volume _U_ attempts to move forward (1), reflect (2), or reverse its direction (3). Since the motion is discretized, the particle will overstep the boundary of _U_ so that the normal vector **ˆn** ( **q** ) on the outside is used for reflections. This necessitates the definition of **ˆn** ( **q** ) as a vector field outside _U_ , which we define by considering scaled copies of the boundary (dotted line). 

for the sphere and the scaling of the mean chord length with dimension is calculated in Appendix E. 

## **II. BACKGROUND** 

In this section, we introduce GMC and Sinkhorn divergences. We will subsequently use Sinkhorn divergences to measure the convergence of the GMC algorithm. 

## **A. Galilean Monte Carlo** 

Starting from an initial position and momentum inside the volume _U_ , GMC [8] either moves forward, reflects using the normal vector **ˆn** or reverses the initial momentum (Fig. 1). It tries these moves in this order and only tries the next move if the proposed point lies outside the volume. This defines a step in the GMC algorithm. More precisely, given an initial position **q** ( _t_ ), a momentum **p** ( _t_ ), a time step _τ_ , and a scalar mass _m_ , the position and momentum at time _t_ + 1 are calculated as follows: 

(1) Let **q** 1 = **q** ( _t_ ) + _m[τ]_ **[p]**[(] _[t]_[).][If] **[q]**[1][is][inside,][then][proceed] with **q** ( _t_ + 1) = **q** 1 and **p** ( _t_ + 1) = **p** ( _t_ ). 

(2) Otherwise, let **ˆn** 1 = **ˆn** ( **q** 1), **p** 1 = **p** ( _t_ ) − 2( **p** ( _t_ )[⊤] **ˆn** 1) **ˆn** 1 and **q** 2 = **q** 1 + _m[τ]_ **[p]**[1][.][If] **[q]**[2][is][inside,][then][proceed][with] **[q]**[(] _[t]_[+] 1) = **q** 2 and **p** ( _t_ + 1) = **p** 1. (3) Otherwise, proceed with **q** ( _t_ + 1) = **q** ( _t_ ) and **p** ( _t_ + 1) = − **p** ( _t_ ). 

We call the second and third branches the reflection and rejection branches, respectively. Note that GMC reflects inexactly as it uses a normal vector strictly outside the volume, as opposed to dynamical billiards which uses the normal vector at the boundary. 

We define a trajectory as a sequence of _L_ steps, mapping the particle state from time _t_ to _t_ + _L_ . The GMC algorithm proceeds by sampling a momentum from the Gaussian distribution _N_ ( **0** _, σp_[2] **[1]**[),][where] **[0]**[and] **[1]**[are][the][zero][vector][and][the] identity matrix of appropriate sizes, respectively, and _σp_ is the momentum standard deviation, followed by a trajectory and repeating this by sampling a new momentum, i.e., rerandomizing the momentum. By the term GMC dynamics, we refer to the deterministic evolution of a particle in a trajectory. In 

045308-2 

PHYSICAL REVIEW E **111** , 045308 (2025) 

RESONANCES IN REFLECTIVE HAMILTONIAN … 

the Supplemental Material [35] (see also Refs. [1,9,18,36,37] therein), we prove that any variety of RHMC has the uniform distribution as its stationary distribution and show that this also holds for GMC as a special case. Finally, we note that momentum rerandomizations are required for ergodicity although we do not prove this here. 

GMC requires us to define a vector field **ˆn** ( **q** ) which matches the boundary normal vector at the boundary. While many choices are possible, for convex boundaries we can imagine moving each point on the boundary at constant speed along its instantaneous normal vector. This constructs a family of boundaries, indexed by time. The union of the normal vector fields of such boundaries defines our normal vector field **ˆn** ( **q** ) (Fig. 1). For the sphere and cube, we give the explicit form thereof in Secs. III and IV, respectively. In the application within the nested sampling algorithm, **ˆn** ( **q** ) is naturally defined by the gradient of the likelihood [2], ∇ _L_ ( **q** ), and the volume _U_ corresponds to a level set of the likelihood function, { **q** | _L_ ( **q** ) _< L⋆_ }, for some fixed value of the likelihood _L⋆_ . In the application within slice sampling [1], the volume and **ˆn** ( **q** ) are similarly defined by level sets of the probability distribution to be sampled. 

Since _τ_ only appears in the combination _m[τ]_ **[p]**[,][a][scaling][of] _τ_ is equivalent to an appropriate change in _σp_ so that we set _τ_ = 1 without loss of generality. Similarly, we take _m_ = 1 so that momentum, velocity and position have the same units. The absolute scale is set by the volume under consideration. In the literature, _σp_ is commonly referred to as the step size of the algorithm. Time _t_ is measured in units of Monte Carlo steps (MCS). Finally, we use the notation **ˆx** to denote the normalization of the vector **x** throughout. In summary, GMC has three parameters, _σp_ , _L_ and the number of trajectories, which must be jointly tuned in practice. 

In comparison with dynamical billiards, which is the Hamiltonian flow of a particle in a potential constant inside and infinite outside the boundary, there are two fundamental differences. First, GMC dynamics introduces additional discontinuities into the billiards flow map. To see this, consider a particle moving close to a flat boundary, in parallel. Considering the effective momentum of a particle, **p** eff = **q** ( _t_ + 1) − **q** ( _t_ ), it is clear that **p** eff = **p** ( _t_ ). However, if the momentum of the particle has a small angle towards the boundary such that it crosses the boundary in the next time step, then we approximately have | **p** eff | ≈ 2| **p** ( _t_ )| since the particle evolves under the reflection branch and hence takes two position updates in a single step. Generalizing to an ensemble of particles coexisting in a small neighborhood in phase space, these discontinuities split the ensemble into spatially separated subpopulations, traveling at two different effective speeds. In the sphere and cube, we show this splitting explicitly. 

Second, by the definition of dynamical billiards, the reflection is fixed in space and neighboring particles reflect with a time delay determined by the momentum normal to the boundary [38]. However, in GMC dynamics, two particles sufficiently close in phase space reflect at the same time. In the sphere and cube, this simultaneous reflection is accompanied with bunching of the particle density, i.e., the formation of a local overdensity of particles. Specifically, in the sphere, first note that a reflection preserves the radial position of a 

particle, i.e., | **q** ( _t_ + 1)| = | **q** ( _t_ )|. For example, Fig. 12 shows this. As we will show in Sec. III B, for a typical initialization, most particles will reflect in the next time step, assuming intermediate _σp_ . Now, if we have an ensemble of particles initialized at the same position, then this implies that most particles will still have the same radius at the next time step. The dimensionality of the support of the particle distribution is therefore _n_ − 1 since all particles are squashed onto the same radius. As we will show, a significant fraction of the particles continue to remain at the initial position in subsequent time steps. This illustrates the previously mentioned bunching of a particle distribution. In contrast, for the same initialization in dynamical billiards, all particles immediately obtain different radial positions, regardless of the value of _σp_ . The particle distribution will continue to gradually spread in the full dimensionality _n_ of the space. In the cube, we will show that a dispersing wave packet will be focused by a reflection in Sec. IV C and Fig. 9, which is again not the case for billiards. The described instances of bunching manifest as oscillations in the SD because the SD measures the nonuniformity of the particle distribution. This will become clear in the following sections. We call the general phenomenon associated with bunching a resonance. 

Finally, we note that there is no Hamiltonian generating a continuous-time dynamics whose restriction to discrete times is GMC dynamics. Alternatively formulated, we cannot extend GMC to continuous time even if we change the potential. Any modification on the potential must be outside the boundary since particles travel in straight lines inside. In one dimension, for a particle in a box of length 2 _ℓ_ , [− _ℓ, ℓ_ ], suppose that the particle is traveling in the positive **q** -direction with momentum **p** . Assuming that the GMC Markov chain is ergodic, the particle will be located at position **q** = _ℓ_ − **p** + _ε_ at some time _t_ , where we choose 0 _< ε <_ **[p]** 2[.][The][positivity] condition on _ε_ ensures that the particle is mapped to **q** at time _t_ + 1 again because it reflects. However, a continuous dynamics will take at least a time interval of 2 **[p]**[−] **p** _[ε] >_ 1 for the particle to return to position **q** , so that the particle does not make it back in time to the same position **q** . While the above argument holds in one dimension, we conjecture that GMC cannot be extended to continuous time dynamics in higher dimensions, as well. In fact, if there were such an extension, then we could take the radial dynamics in the ( _n_ − 1)-sphere as a one-dimensional continuous extension of GMC, which we have shown is not possible. The implication of the above is that our subsequent analysis must be based solely on the dynamical equations of GMC. 

## **B. Sinkhorn divergences** 

In this section, we define the main tool to analyze the mixing of GMC. As a preliminary definition, we introduce the entropy-regularized optimal transport cost [39,40], which 

**==> picture [244 x 23] intentionally omitted <==**

**==> picture [13 x 9] intentionally omitted <==**

045308-3 

KROUPA, CSÁNYI, AND HANDLEY 

PHYSICAL REVIEW E **111** , 045308 (2025) 

for any _ε >_ 0 and probability distributions _α_ and _β_ on R _[n]_ , where _c_ is a positive symmetric cost function and 

**==> picture [221 x 25] intentionally omitted <==**

is the Kullback-Leibler divergence between _π_ and the product distribution _α_ ⊗ _β_ . The minimization in Eq. (1) is performed over all _π_ in the set _�_ ( _α, β_ ) of joint distributions on the support of _α_ and _β_ with _α_ and _β_ as marginal distributions. In the following, we always choose _c_ ( _x, y_ ) =[�] _[n] i_ =1[|] _[x][i]_[ −] _[y][i]_[|][.] For _ε_ → 0, we recover the optimal transport cost between the distributions _α_ and _β_ . For _ε >_ 0, the entropic regularization through the Kullback-Leibler divergence renders the minimization problem convex and it can be solved efficiently on a GPU for empirical distributions defined through samples. 

The problem with OT _ε_ is that OT _ε_ ( _α, α_ ) ̸= 0. As a remedy, the SD was introduced [41], 

**==> picture [237 x 13] intentionally omitted <==**

which does not have this bias. 

Importantly, we have SD( _α, β_ ) ⩾ 0, SD( _α, β_ ) = 0 if and only if _α_ = _β_ and SD( _α, β_ ) → 0 if _α_ converges to _β_ in law [42]. If we have access to _N_ samples from each of the two distributions, then we can measure the divergence between the empirical distributions defined by the samples. The accuracy of the divergence between the empirical distributions when compared to the divergence between the underlying distributions is termed the sample efficiency, which scales as _N_[−][1] _[/]_[2] with a constant dependent on _ε_ and _n_ [43]. 

In the following, we always choose _β_ to be the empirical distribution of _N_ independent and identically distributed samples drawn from the uniform distribution on the particular volume under consideration. While it is possible to sample exactly from the sphere and cube, other volumes can generally be sampled from by rejection sampling. The samples defining _α_ will evolve in time under the GMC Markov chain, initialized from the same position but with momenta drawn independently from the Gaussian _N_ ( **0** _, σp_[2] **[1]**[). The initialization] in configuration space is therefore a Dirac _δ_ distribution and the decrease in SD measures the mixing of the Markov chain in time, while an increase indicates that _α_ is becoming less uniform, or equivalently that the underlying particles exhibit bunching. For _t_ →∞, we expect that SD( _α, β_ ) → 0 due to the convergence of the Markov chain. 

In the following, we use the implementation of Eq. (3) in the OTT library [44]. We choose _ε_ = 4, such that SD ≈ 0 for two sets of uniformly distributed samples in the sphere and cube for 2 × 10[3] samples in _n_ = 100 dimensions. Increasing _ε_ smooths variations in the SD when measured as a function of time, but does not change the timescales of the variations and the frequency content, which we mainly use in the following. 

## **III. DYNAMICS IN A UNIT SPHERE** 

In this section, we consider the volume bounded by the unit sphere, _S[n]_[−][1] = { **q** ∈ R _[n]_ |[�] _i[q] i_[2][=][ 1][}][.][Since][GMC][requires] gradients outside the sphere, we define a unit vector field pointing towards the origin, **ˆn** ( **q** ) = − **ˆq** . In nested sampling, this corresponds to the case of an isotropic distribution such as a Gaussian with isotropic covariance. 

## **A. Empirical mixing results** 

The left subfigure of Fig. 2 shows the SD against time for an ensemble of chains of GMC, initialized at the same position drawn uniformly from the unit ball with momenta sampled from _N_ ( **0** _, σp_[2] **[1]**[)][in] _[n]_[ =][ 100][dimensions.][At][time] _[t]_[=][ 0,][all] particles are localized at the same position, resulting in a large SD. In high dimensions, the radius of the initial position is almost at the boundary. As the particles spread out, the SD decreases rapidly. In high dimensions, the radial distribution of the Gaussian momentum distribution is concentrated at | **p** | = _σp_ √ _n_ with standard deviation ~~√~~ _σp_ 2[[][45][].][The][particle] distribution therefore spreads like a narrow shock wave which reflects at the boundaries. The momentum standard deviation _σp_ = 2 × 10[−][3] is sufficiently small that the discretization is negligible and the particle density behaves fluidlike. The SD reaches a minimum before the particles reassemble into a _δ_ peak at approximately − **q** (0). Since the radial distribution has a finite standard deviation, this _δ_ peak is smeared out so that the SD does not rise to the value at _t_ = 0. This process continues, resembling a fluid which oscillates back and forth between **q** (0) and − **q** (0). Rerandomizing the momenta of all particles every _L_ = 400 MCS introduces a kink in the evolution of the SD against time. As expected, the SD decreases to lower values at every rerandomization since the algorithm is only ergodic due to the momentum rerandomizations. Moreover, we observe roughly the same pattern in the SD against time at every rerandomization, in accordance with the notion that the algorithm restarts for each particle. 

When the momentum standard deviation is increased to _σp_ = 8 × 10[−][3] , the frequency of the oscillations increases. We observe that the SD reaches a finite plateau, indicating that the particle distribution has converged to a subspace of the unit ball. In particular, at this point the particle distribution exhibits an under-density at the center of the sphere, forming a hole. Meanwhile, the angular distribution is approximately uniform. The convergence speed to the subspace increases with _σp_ as this is driven by diffusive spreading of particles which is induced by the finite width of the radial momentum distribution, _σp_[Larger] _[σ][p]_[therefore][causes][faster][conver-] ~~√~~ 2[.] gence. Subsequent rerandomization of the particle momenta moves each particle onto a new contour in phase space, allowing the particles to explore a larger subspace, leading to an almost discontinuous drop in the SD. This pattern repeats until the particle distribution converges to the uniform distribution with the SD converging to zero, as expected, since this is the stationary distribution of the Markov chain. Increasing _σp_ further to 24 × 10[−][3] agrees with the picture developed above. 

Note that the value of the SD being approximately zero, as in Fig. 2, does not imply a uniform particle distribution as decreasing the regularization parameter _ε_ shifts the curves to larger absolute values. In fact, especially the radial distribution function exhibits little mixing at this point. We provide a detailed description of this in the following section. 

## **B. Lossless two-dimensional representation** 

We now focus on an ensemble of deterministic trajectories of GMC, i.e., an ensemble of particles initialized at the same position with momenta drawn from _N_ ( **0** _, σp_[2] **[1]**[)][but][without] 

045308-4 

PHYSICAL REVIEW E **111** , 045308 (2025) 

RESONANCES IN REFLECTIVE HAMILTONIAN … 

**==> picture [503 x 146] intentionally omitted <==**

FIG. 2. Sinkhorn divergence (SD) of an ensemble of GMC Markov chains in the sphere (left) and the cube (right) in _n_ = 100 dimensions, measured with respect to the uniform distribution. Time is measured in Monte Carlo steps (MCS). Initialized from a randomly chosen point, 10[3] particles are evolved under GMC dynamics with momenta drawn independently from a multivariate Gaussian _N_ with standard deviation _σp_ , commonly known as the step size of the algorithm. Every _L_ = 400 MCS, the momenta are rerandomized. Within a single trajectory, i.e., up to the momentum rerandomization, the particle ensemble converges to a subspace of the full volume so that the SD stagnates on a timescale given by the dispersion the particle distribution. The observed oscillations are caused by temporary bunching (resonances) of the particles, both due to the inexact reflections present in the GMC dynamics and concentration phenomena in high dimensions. Momentum rerandomization effectively restarts the algorithm, leading to an approximately repeating pattern in the SD, which converges to zero on longer timescales since the stationary distribution of the Markov chain is uniform in the volume. 

subsequent momentum rerandomizations. This corresponds to the behavior of the SD in Fig. 2 up to the first rerandomization time. 

By considering the geometry of a reflection, it can be seen that a single particle is reflected onto a position of the same radius. In particular, this implies that the Markov chain is rejection free, i.e., the rejection branch is never invoked. Moreover, the motion is confined to a two-dimensional disk. This is seen by noting that the initial position vector, measured from the center of the sphere, the momentum vector and the normal vector lie in the same plane. Hence, any subsequent positions and momenta defined by the GMC dynamics can be expressed as linear combinations of the initial conditions so that they remain confined in this plane. 

Consequently, we can map all trajectories onto a single two-dimensional disk while preserving radial distribution functions as follows (Fig. 3). First, assume that the initial position is aligned with the **q** 1 axis. Otherwise we can perform a global rotation to achieve this. For each particle _i_ , there is now a rotation matrix **R** _i_ , constructed explicitly in Appendix A, and projection matrix **P** _i_ = ( **1** 2×2 **0** 2×( _n_ −2)), where **1** 2×2 is the two-dimensional identity matrix and **0** 2×( _n_ −2) is a matrix of zeros of size 2 × ( _n_ − 2), which map the _n_ -dimensional position vector **q** _i_ ( _t_ ) to a two-dimensional vector, 

**==> picture [160 x 10] intentionally omitted <==**

by first rotating the two-dimensional disk around the axis spanned by the sphere center and the initial position, giving **R** _i_ **q** _i_ ( _t_ ) = (( ˜ _qi_ )1( _t_ ) _,_ ( ˜ _qi_ )2( _t_ ) _,_ 0 _, . . . ,_ 0)[⊤] , and subsequently discarding the dimensions zeroed by **R** _i_ . To preserve the symmetry of isotropic distributions, we choose to rotate either clockwise or anti-clockwise such that half of the particles end up on the upper or lower half of the two-dimensional disk. We use the same transformation on the momenta, thus giving two-dimensional momenta **˜p** _i_ ( _t_ ) = **P** _i_ **R** _i_ **p** _i_ ( _t_ ). The radial distribution of **˜p** _i_ is identical to that of **p** _i_ as lengths are 

preserved under application of **P** _i_ **R** _i_ . While the distribution of **ˆp** _i_ = **p** _i/_ | **p** _i_ | is uniform, the distribution of **˜p[ˆ]** _i_ = **˜p** _i/_ | **˜p** _i_ | is proportional to | sin _φ_ | _[n]_[−][2] (Appendix B), where _φ_ is the angle between **q** _i_ and **p** _i_ . The effective angular distribution hence concentrates around _φ_ = ± _[π]_ 2[.][The][standard][deviation] of _φ_ decreases as ( _n_ − 2)[−][1] _[/]_[2] with increasing dimensionality _n_ , obtained by a Laplace approximation. Intuitively, the overlap of the isotropically distributed momentum vector with the ( _n_ − 1)-dimensional tangent space at the initial position is significantly larger than the overlap with the one-dimensional radial vector. Hence, in high dimensions, a particle is most likely to initially move orthogonally to its initial position. We stress that the map in Eq. (4) is an effectively lossless compression of the high-dimensional particle positions onto two dimensions, enabled by the symmetries of the sphere. 

The two-dimensional positions { **˜q** _i_ ( _t_ )} _[N] i_ =1[can][be][directly] visualized. To avoid numerical instabilities, we do not apply Eq. (4) to high-dimensional particles. Instead, we use the analytically derived two-dimensional distributions to directly prepare the particles in two dimensions. To initialize the particle positions, we sample **q** _i_ (0) from the _n_ -dimensional unit ball and set **˜q** _i_ (0) = (| **q** _i_ (0)| _,_ 0 _, . . . ,_ 0). To initialize the momenta, we sample { **p** _i_ (0)} _[N] i_ =1[from][the] _[n]_[-dimensional] normal distribution, giving **˜p** _i_ (0) in polar coordinates as | **˜p** _i_ (0)| = | **p** _i_ (0)| and angle _θ_ = sgn(( **p** _i_ )2(0)) cos[−][1] ( **p** _i_ )1(0) [Eq. (A4)]. 

To show the dynamics of the particle density more clearly, we increase concentration effects by increasing the dimensionality to _n_ = 2 × 10[3] . We scale the three values of _σp_ shown in Fig. 2 to _σp_ = _σ_ ˜ _p_ ~~�~~ 100 _n_[,][where] _σ_ ˜ _p_ ∈{2 × 10[−][3] _,_ 8 × 10[−][3] _,_ 24 × 10[−][3] }. This ensures that the radius of the momentum shell remains the same. Figure 4 shows the particle density of the angle _θ_ and radius | **q** | as it evolves in time. The density is a Dirac _δ_ function at _θ_ = 0 at 

045308-5 

KROUPA, CSÁNYI, AND HANDLEY 

PHYSICAL REVIEW E **111** , 045308 (2025) 

**==> picture [183 x 352] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a)<br>(b)<br>**----- End of picture text -----**<br>


FIG. 3. (a) Action of the rotation map **R** _i_ [Eq. (4)]. In the sphere _S[n]_[−][1] , a trajectory lies in a two-dimensional disk spanned by the initial position **q** _i_ (0) and momentum **p** _i_ (0). All particles have different momenta but are initialized from the same point and hence share the axis **q** _i_ (0). Their individual discs can therefore be rotated onto the **q** 1- **q** 2-plane. This maps the angle _ψ_ to zero but preserves _θ_ . (b) Image of the rotation map. The radial and angular distributions of the initial momentum concentrate around _σp_ √ _n_ ± ~~√~~ _σp_ 2[and][±] _[π]_ 2[±][ (] _[n]_[ −][2)][−][1] _[/]_[2][,] respectively. To first order in _n_[1][,][the][distance][of][the][initial][position] is 1 −[2] _n_[from][the][origin.][The][dominant][motion][in][high][dimensions] therefore approximately follows a path close to the boundary, converging at an antipodal point. 

initialization. At _t_ = 1 MCS, the particle distributions propagate as Gaussian wave packets, as expected. The mean angle increases linearly with time, except for _σ_ ˜ _p_ = 24 × 10[−][3] . This wave packet is aliased, i.e., its effective (visible) momentum is slower than its true momentum due to the discretized motion. In addition, the angular wave packets visibly disperse and eventually spread over all angles. This diffusive component of the motion is induced by the finite radial width of the momentum distribution. 

The radial distributions display a Dirac _δ_ peak at the initial radius, as expected. The fraction of particles stuck at this radius increases as _σ_ ˜ _p_ is increased. For _σ_ ˜ _p_ = 24 × 10[−][3] , all particles are stuck at the same radius. Additionally, the remaining particles are confined to a narrow shell near the 

**==> picture [241 x 399] intentionally omitted <==**

FIG. 4. Angular and radial particle density for different times _t_ in the sphere for _n_ = 2 × 10[3] and _σp_ = _σ_ ˜ _p_ � 100 _n_[. The angle] _[ θ]_[is defined] through the rotation map [Eq. (4)]. The dispersion and the splitting of the particle distribution is visible for _σ_ ˜ _p_ = 8 × 10[−][3] at _t_ = 10 MCS, with the faster particles traveling at the supersonic velocity defined in Eq. (8) and the slower particles in a smaller wave packet behind them. At _t_ = 20 MCS, the wave packet merges at _θ_ = _π_ with the one traveling in the opposite direction. For _σ_ ˜ _p_ = 24 × 10[−][3] , the wave packet travels faster, however this motion appears slower due to aliasing. The radial distribution is effectively fixed at the initial radius, which is expected from the concentration of the angular distribution _p_ ( _φ_ ) ∝| sin _φ_ | _[n]_[−][2] . The arrow denotes a _δ_ function and the percentage is the fraction of particles at the _δ_ function. For comparison, the dotted straight line is the radial distribution _p_ ( _r_ ) = _nr[n]_[−][1] of the uniform distribution in the sphere on a log-log axis. There are no particles deeper inside the sphere than shown. This creates an under-density compared to the uniform distribution or, equivalently, an overdensity near the boundary. 

boundary. A comparison with the radial density, _p_ ( _r_ ) = _nr[n]_[−][1] , of the uniform distribution inside the sphere shows that there is an overdensity near the boundary and a lack of particles deeper inside the sphere. 

045308-6 

PHYSICAL REVIEW E **111** , 045308 (2025) 

RESONANCES IN REFLECTIVE HAMILTONIAN … 

With the radius approximately fixed, all particles travel simultaneously to the antipodal point, until they meet at − **q** (0). At this point, the angle _θ_ wraps around and we observe particles with angle larger than _π_ in the range [0 _, π_ ]. The merging of the two particle distributions traveling in opposite angular directions is visible for _σ_ ˜ _p_ = 8 × 10[−][3] at _t_ = 20 MCS. Overall, the dynamics of the particle density supports the picture of the oscillating fluidlike motion developed in Sec. III A. 

In addition to the dominant mode of the angular particle density, there is a second mode of particles moving at a slower effective angular velocity. This is especially visible for _σ_ ˜ _p_ = 8 × 10[−][3] at _t_ = 10 MCS. We analyze the components of this motion in the following section. 

## **C. Frequency spectrum** 

We model the SD as a function of time (left subfigure of Fig. 2) for a single trajectory as 

**==> picture [201 x 32] intentionally omitted <==**

where { _fi_ } _[N] i_ =[freq] 1[is][the][frequency][spectrum][of][density][oscilla-] tions and _τ_ broad is the timescale of decay corresponding to the decay from diffusive broadening of the wave front. The functional form of e[−] _[t][/τ]_[broad] matches the observed exponential decay when the momentum standard deviation _σp_ is sufficiently large. For smaller _σp_ , the decay takes a Gaussian form, e[−] _[t]_[2] _[/]_[2] _[τ]_[ 2] . However, for the purpose of describing the dominant timescales of the dynamics, the precise functional form matters less since both functional forms lead to the same scale of broadening in frequency space, which is why we continue with the exponential decay. The power spectral density, PSD( _f_ ) ∝| _F_ [SD]( _f_ )|[2] , restricted to positive frequencies is 

**==> picture [230 x 35] intentionally omitted <==**

where _F_ is the Fourier transform, _⋆_ denotes a convolution and _f_ broad = _τ_ broad[−][1][.] We now discuss the frequency content { _fi_ } _[N] i_ =[freq] 1[.][In][suf-] ficiently high dimensions, the momentum distribution is concentrated in a thin spherical shell of radius _σp_ √ _n_ . We therefore expect density oscillations to originate from the propagation of the wavefront as it is reflected in the unit ball. This includes a density wave reflecting back and forth between antipodal points of the unit sphere, leading to radial oscillations of frequency 

**==> picture [160 x 23] intentionally omitted <==**

where _R_ = 1 is the radius of the sphere. As Fig. 5 shows, _f_ diag provides a lower bound to the spectrum instead of constituting the dominant frequency component. In particular, the mean frequency deviates nonlinearly in _σp_ from _f_ diag. In fact, as previously shown, since the effective angular distribution concentrates around ± _[π]_[we][expect][most][particles][to] 2[,] follow trajectories along the disk boundary. Computing the frequency _f_ super along such trajectories gives approximately 

FIG. 5. Power spectral density PSD( _f_ ) of the Sinkhorn divergence against the standard deviation _σp_ of the momentum distribution in the sphere in _n_ = 100 dimensions. Increasing _σp_ increases the average momentum magnitude of the particles, leading to higher-frequency oscillations in the particle density up to the Nyquist frequency _f_ N = 0 _._ 5 MCS[−][1] when _σp_ √ _n_ ∼ 1. The dominant frequency _f_ super _> f_ diag indicates that most particles travel with larger effective momentum close to the boundary. Dispersion of the particle wave front leads to broadening of the PSD on a scale of _f_ broad. 

(Appendix C), 

**==> picture [239 x 43] intentionally omitted <==**

which we term the supersonic frequency since the particles move faster than particles moving in a straight line and in particular reach the antipodal point earlier despite taking a longer path along the disk boundary. Intuitively, the fact that particles have a higher effective momentum when colliding with a boundary, as explained in Sec. II A, overcompensates for the longer path. 

The decay of the SD induces a broadening of the spectrum. As the wave front has a width of approximately ~~√~~ _[σ][p]_ 2[in momen-] tum space, the timescale over which a wavefront disperses is given by _τ_ broad ∼ ~~√~~ _σp_ 2[so][that] _[f]_[broad][=] _[ τ]_ broad[ −][1][∼] ~~√~~ _[σ][p]_ 2[,][omitting][a] dimensional prefactor of unity. 

We compute the power spectral density as a function of _σp_ in Fig. 5. As expected, the frequency of oscillations increases with _σp_ . At _σp_ ∼ _n_[−][1] _[/]_[2] , the Nyquist frequency _f_ N = 2[1][MCS][−][1] is reached and we observe an aliased frequency spectrum for _f > f_ N. This is approximately the value of _σp_ at which the particles traverse the ball in approximately a single step, _σp_ ~~√~~ _n_ ∼ 1. For _σp_ ≲ 0 _._ 25, we see that the dominant frequency is less than _f_ diag. These are particles traveling at the ordinary nonsupersonic speed, which reach the antipodal point at a later time than particles traveling diagonally through the sphere due to the longer path length. For _σp_ ≳ 0 _._ 25, this mode disappears and the dominant frequency becomes _f_ super, in agreement with the previously described two-dimensional representation. Additionally, see that the dominant frequencies are broadened. In particular, the zero-frequency component and _f_ super exhibit 

045308-7 

KROUPA, CSÁNYI, AND HANDLEY 

PHYSICAL REVIEW E **111** , 045308 (2025) 

broadening on roughly the expected scale of _f_ broad. A larger range of _σp_ values is shown in Appendix D. 

## **IV. DYNAMICS IN A CUBE** 

In this section, we consider the _n_ -dimensional cube, _U_ = [−1 _,_ 1] _[n]_ , which we extend by a unit vector field **ˆn** _i_ ( **q** ) = − _δi j_ where _j_ = arg max _i_ | **q** _i_ |. In nested sampling, this setup arises as the normalized gradient field of a pyramid. 

**==> picture [223 x 66] intentionally omitted <==**

**----- Start of picture text -----**<br>
a 0.4<br>n 5<br>1S)<br>2 0.3<br>+> rs — 10<br>a 0.2<br>)<br>(<br>ln (PSD)<br>**----- End of picture text -----**<br>


## **A. Empirical mixing results** 

The right subfigure of Fig. 2 shows the SD as a function of time. For all _σp_ , there is initially a monotonic decay of the SD. This corresponds to the particle distribution spreading out and mixing. The SD subsequently reaches a minimum and increases in time, corresponding to the particles unmixing. The time at which the minimum is reached corresponds to the particles hitting the boundary of the cube along their trajectory and either being reflected or reversing their momentum. Naturally, a larger _σp_ decreases this time. Moreover, the fraction of particles evolving according to the rejective branch generally increases as _σp_ is increased. The reason is that a larger step size causes larger overstepping of the boundary and therefore lowers the probability of a particle reflecting back inside the boundary. Consequently, the minimum in the SD becomes sharper as _σp_ is increased. That is, for a sufficiently large value of _σp_ , almost all particles reverse their momentum upon hitting the boundary instead of reflecting and mixing further, causing the SD to increase almost immediately. 

As the particle distribution evolves further, the SD reaches a steady-state value and fluctuations around this value are visible. The steady-state value is larger than the minimum SD attained previously. As we will show in Sec. IV C, the particle distribution does not continue to relax to the uniform distribution after hitting a boundary. Instead, the distribution oscillates between more spread-out and bunched states. As a measure of the nonuniformity of the particle distribution, the SD shows this oscillation around an average nonuniform state. 

Furthermore, it is visible that the steady-state value of the SD increases as _σp_ is increased. Two factors influence this value. First, more particles are stuck at their initial position due to the increase in momentum reversals. This causes the steady-state value to increase. Additionally, more particles are trapped along one-dimensional subspaces due to momentum reversal at both ends of the subspace. We test this in Sec. IV B. For _σp_ = 24 × 10[−][3] , the initial minimum is of the same magnitude as the fluctuations, showing that the particles effectively do not explore the cube beyond one-dimensional subspaces. 

Overall, the support of the particle distribution therefore shrinks as _σp_ is increased, leading to a larger value of the steady-state SD. As _σp_ is increased significantly (not shown), all particles are trapped at their initial position and the SD remains constant in time. 

Subsequent rerandomizations of the particle momenta decrease the SD further, as expected. It is visible that the effect of a rerandomization decreases as _σp_ is increased. Specifically, the steady-state SD decreases more strongly for _σp_ = 2 × 10[−][3] than for the other values of _σp_ . This occurs because 

FIG. 6. Transition between fluidlike ( _σp_ ≲ 4 × 10[−][3] ) and quasiperiodic ( _σp_ ≳ 4 × 10[−][3] ) dynamics. The plot shows the power spectral density PSD( _f_ ) of the Sinkhorn divergence against the standard deviation _σp_ of the momentum distribution in the cube in _n_ = 100 dimensions. At low _σp_ , the particle distribution diffuses throughout the cube. Increasing _σp_ increases the rejection probability, leading to particles trapped along effectively one-dimensional trajectories, causing a discrete spectrum of resonant frequencies. At even larger _σp_ , the spectral line at _σp_ = 4[1][MCS][−][1] dominates and other frequencies vanish. 

the subspace of the cube explored by a particles decreases with _σp_ , as discussed above, so that the gain in exploration from a randomization of the momentum becomes smaller for larger _σp_ . 

## **B. Frequency spectrum** 

The dynamics of a single particle in an _n_ -dimensional cube, [−1 _,_ 1] _[n]_ , is either quasiperiodic or periodic, depending on the relative magnitude of the components of its momentum along the coordinate axes. Moreover, as the GMC dynamics simply reverses the momentum component along a coordinate on a reflection, the particle will retrace its positions along that coordinate. Hence, in the case of quasiperiodic motion, the dynamics is ergodic on a discrete lattice with spacings given by the momentum vector components. Similarly to the dynamics of billiards, it does not mix as the dynamics is integrable. 

Figure 6 shows the frequency spectrum of the SD in _n_ = 100 dimensions. The power spectral density is averaged over multiple random initializations to ensure independence from the trajectory initial conditions. For _σp_ ≲ 4 × 10[−][3] , we observe almost continuous mixing of the particle distribution, leading to a dominant zero-frequency component broadened by the decay of the SD. For _σp_ ≳ 4 × 10[−][3] , discrete frequency peaks appear. As expected from quasiperiodic motion, the spectrum of an observable contains frequencies at all integer linear combinations of the fundamental frequencies [46]. At _σp_ ≳ 10[−][2] , the dominant frequency _σp_ = 4[1][MCS][−][1][emerges] and, for _σp_ ≳ 8 × 10[−][2] , all frequencies vanish except for this frequency. For even larger _σp_ ( _σp_ ≳ 0 _._ 3), all particles are stuck at their initial position and _f_ = 0 MCS[−][1] is the only 

045308-8 

PHYSICAL REVIEW E **111** , 045308 (2025) 

RESONANCES IN REFLECTIVE HAMILTONIAN … 

uniformly from the volume, which is the cube here. From a ~~TE ,~~ a Monte Carlo estimate (Appendix E), we obtain a power-law ic)a. 107-1 ~~Poe ey~~ 3 fas}8© scaling, ⟨ _ℓ_ ⟩∝ _n_[−][0] _[.]_[486][±][0] _[.]_[002] . Since the momentum of each par- ~~_~~ ~ ticle is approximately _σp_ ~~√~~ _n_ , the critical momentum standard 8 deviation scales roughly as ( _σp_ )crit ∝⟨ _ℓ_ ⟩ _/_[√] - _n_ ∝ _n_[−][0] _[.]_[986][±][0] _[.]_[002] , ~~25~~ =I a ~~5~~ ) which is shown in Fig. 7 and aligns with the observed boundo GH ary. 

## **C. Low-dimensional representation** 

FIG. 7. The transition boundary between fluidlike and quasiperiodic dynamics follows a power law in the dimension _n_ , ( _σp_ )crit ∝ _n_[−][0] _[.]_[986(2)] . The plot shows the entropy of the Fouriertransformed Sinkhorn divergence against the standard deviation _σp_ of the momentum distribution and the dimensionality _n_ . A larger value of the entropy indicates the occurrence of multiple resonances. A value of zero corresponds to the presence of a single frequency, in which case all particles are stuck due to rejections. The line indicates the critical _σp_ above which particles are rejected, where the power-law exponent is determined by an estimate of the mean chord length ⟨ _ℓ_ ⟩. 

frequency present, which corresponds to a Sinkhorn divergence constant in time. 

In contrast to the dynamics in the sphere, the rejection branch of GMC is invoked. This happens particularly around the corners of the cube where a reflection may not suffice to bring the particle back inside. Consequently, in high dimensions, in which most of the volume of a cube is in its corners [47], the fraction of rejected particles increases. 

We measure the critical momentum standard deviation ( _σp_ )crit above which all particles evolve under the rejection branch, and are hence fixed at the initial position for all times, by calculating the entropy of the Fourier transform of the SD, _H_ = − _k[I]_[ˆ] _[k]_[ log] _[I]_[ˆ] _[k]_[,][where] _[I]_[ˆ] _[k]_[is][obtained][by][normalizing][the] power spectral density of the SD as a function of time and the sum runs over over the frequency spectrum obtained from the discrete Fourier transform. Since _H_ measures the effective support size of a probability distribution [48], a large value of _H_ indicates the presence of many frequencies, whereas _H_ = 0 indicates that the SD does not vary with time and hence that all particles are stuck at their initial position. The boundary between _H_ = 0 and _H >_ 0 is the critical momentum standard deviation ( _σp_ )crit. 

Figure 7 shows the entropy _H_ as a function of _σp_ and _n_ . For any given value of _n_ , starting from _σp_ ≈ 0, increasing _σp_ increases _H_ until _H_ reaches a maximum value. This is expected, since we transition from the regime dominated by the zero frequency component to the regime in which multiple discrete frequencies start to appear. Increasing _σp_ further then decreases _H_ as the diversity of the frequency spectrum decreases and only the frequency at _σp_ = 4[1][MCS][−][1][remains.] 

Additionally, it can be seen that ( _σp_ )crit decreases monotonically with _n_ . We estimate scaling with dimension by considering the average chord length ⟨ _ℓ_ ⟩, which we define as the length of the intersection of a line with direction sampled uniformly from the sphere starting from at a point sampled 

Since the momentum distribution is concentrated, immediately after initialization the particle density is concentrated in a thin spherical shell which expands isotropically, akin to the propagation of a spherical shock wave. For sufficiently small _σp_ , the wave front is reflected at the boundaries and simultaneously disperses, leading to a decay of the SD with time as the particle distribution spreads out uniformly. As _σp_ is increased, an increasingly larger fraction of the particle distribution evolves according to the rejection branch. Therefore, a fraction of particles remain stuck at the initial position. The particle density is therefore a superposition of a Dirac _δ_ distribution at the initial position and a thin nonspherical wave front. As _σp_ increases further, an increasing fraction of the freely propagating particles are rejected when they reach the boundary and are therefore confined to move back and forth along a line. As the radial momentum of the wave front is approximately Gaussian with mean _σp_ ~~√~~ _n_ and standard deviation _σp_[the][coarse-grained][picture][of][the][dynamics][is] ~~√~~ 2[,] that of a Gaussian wave packet moving along such a line. 

Figure 8 shows the dynamics of a wave packet with a momentum distribution set to the radial distribution of a Gaussian in _n_ = 100 dimensions. As the dynamics is scale-invariant in one dimension, i.e., scaling all positions **q** → _λ_ **q** and momenta **p** → _λ_ **p** by the same factor _λ_ , the spacings of the lattice traced out by each particle also scale by _λ_ , the observed density can only depend on the ratio **q[p]**[,][where] **[q]**[and] **[p]**[are] scalars here. We choose a one-dimensional model system on the one-dimensional cube, [−1 _,_ 1], having mean chord length ⟨ _ℓ_ ⟩1d = 2. Since we observe a cross-over to the fully rejective regime at ( _σp_ )crit ≈ 8 × 10[−][2] and the mean chord length in the 100-dimensional cube is ⟨ _ℓ_ ⟩≈ 0 _._ 5, the appropriately scaled momentum distribution takes standard deviation ( _σp_ )1d = ⟨ _ℓ_ ⟩1d _σp/_ ⟨ _ℓ_ ⟩= 3 _._ 2 × 10[−][1] . As we aim to observe resonances, which occur at smaller ( _σp_ )1d, we decrease this value by one order of magnitude to ( _σp_ )1d = 3 _._ 2 × 10[−][2] . The evolving particle density is plotted in Fig. 8, which shows periodically recurring resonances in the particle density, i.e., the particle density increases locally at certain times instead of the particles spreading out uniformly over time. 

The resonances are a consequence of the inexact reflections (Fig. 9). Tracking a pair of particles _i_ and _j_ impinging normally onto a flat boundary, the GMC dynamics preserves the order of the particles, i.e., **q** _i_ ( _t_ 1) _<_ **q** _j_ ( _t_ 1) _< b_ implies **q** _i_ ( _t_ 2) _<_ **q** _j_ ( _t_ 2) _< b_ if a reflection occurs at time _t_ 1 at a boundary located at _b_ . This is not the case in dynamical billiards, in which the order is reversed after a reflection. As the momenta of the particles are reversed after a reflection, the particles will converge for times _t > t_ 2 if they were diverging at _t < t_ 1. Applying this picture to a dispersing Gaussian wave packet, in which particles are sorted by momentum, **p** _i_ ( _t_ ) _<_ **p** _j_ ( _t_ ) 

045308-9 

KROUPA, CSÁNYI, AND HANDLEY 

PHYSICAL REVIEW E **111** , 045308 (2025) 

**==> picture [58 x 11] intentionally omitted <==**

**----- Start of picture text -----**<br>
Timet (  MCS )<br>**----- End of picture text -----**<br>


FIG. 8. Particle density of a wave packet reflecting in a one-dimensional cube, [−1 _,_ 1], under GMC dynamics. The density shows periodic unmixing of the particle density caused by the inexact reflections. Additionally, the wave packet splits into two distinct wave packets visible at the same time. The particles constituting the wave packet are initialized at position **x** (0) = −0 _._ 9 and have their momentum distribution set to the radial distribution of a 100-dimensional Gaussian with _σp_ = 3 _._ 2 × 10[−][2] , emulating the propagation of a wave front confined to a one-dimensional line. The density is computed with a kernel density estimate from the particle distribution and clipped to 2 (indicated by the triangle on the color bar) to discern fluctuations in the lower density regions. The time axis takes discrete values _t_ = 0 _,_ 1 _, . . ._ but the particle density is plotted in the full intervals [0 _,_ 1] _,_ [1 _,_ 2] _, . . ._ . 

if **q** _i_ ( _t_ ) _<_ **q** _j_ ( _t_ ) for all particle pairs _i_ and _j_ at all times _t_ before a reflection, the wave packet becomes anti-dispersing after a reflection and is focused to a point. This causes the observed resonances in the particle density so that the Markov chain defined by GMC temporarily unmixes. This does not contradict the convergence of the Markov chain to the uniform distribution as the Markov chain is only ergodic under repeated rerandomizations of the momentum, whereas we are discussing only a single deterministic trajectory. 

The dominant frequency _f_ = 4[1][MCS][−][1][appears][here][by] considering a wave packet with a sufficiently large average momentum such that it just reaches the other end of the boundary, reflects, returns to its initial position and reflects at the other end of the boundary. Hence, after four steps, the wave packet returns to its initial position in phase space, i.e., initial position in configuration space with all particles having their initial momenta. This amounts to a period of 4 MCS and the observed dominant frequency. 

Finally, we note that the wave packet is cut into multiple wave packets since each reflection induces a time delay by 

1 MCS in which a particle remains at its current position. This explains why two wave packets are simultaneously present after a single reflection, as seen in Fig. 8. Both wave packets are anti-dispersing and hence cause resonances, albeit delayed in time. In general, the number of wave packets appearing after a reflection depends on the width of the wave packet immediately before the reflection and the momentum distribution of the wave packet so that a reflection may produce multiple wave packets. 

## **V. DAMPING RESONANCES** 

Resonances can be damped by adding noise to the momentum vector at every step, see for example Algorithm 5 in Ref. [10]. Here, we implement the following Markov chain. It is initialized by drawing **p** ∼ _N_ ( **0** _, σp_[2] **[1]**[), as before. It then] proceeds by repeatedly alternating between a GMC step and updating the momentum to **p** + _δ_ **p** , where _δ_ **p** ∼ _N_ ( **0** _, σδ_[2] _p_ **[1]**[).] Therefore, the tuning parameter _L_ is replaced by the noise strength _σδ p_ . 

We note that, while this algorithm is reminiscent of underdamped Langevin dynamics, it is missing a friction term in the momentum update. As we are increasing the kinetic energy of the particle ensemble at every step, the momentum distribution does not converge to a stationary distribution. For a system of free particles, the standard deviation of the instantaneous momentum distribution diverges with time since the particles perform a random walk in momentum space. However, as we are investigating the particle dynamics of existing implementations [10], we choose to focus on this algorithm. 

FIG. 9. Inexact reflections are a cause of resonances. In high dimensions, particles move in wave packets and hence are sorted in momentum when approaching the boundary at position _b_ . Particles _i_ and _j_ overstep the boundary at time _t_ 1. GMC dynamics preserves the order of particles and flips the momenta. Subsequently, the particles will converge if they were initially diverging. In dynamical billiards, the order reverses and the particles continue to diverge. 

Now, if _σδ p_ is too small, then the effect of the noise is negligible and the Markov chain reduces to a single long trajectory of GMC. However, if _σδ p_ is comparable to _σp_ or too large, then the Markov chain effectively reduces to GMC with _L_ = 1 and exhibits diffusive behavior. To provide a comparison with Fig. 2, we equate the cumulative effect of noising the momentum over _L_ steps with the full rerandomization. In particular, the average change in the momentum magnitude 

045308-10 

PHYSICAL REVIEW E **111** , 045308 (2025) 

RESONANCES IN REFLECTIVE HAMILTONIAN … 

**==> picture [272 x 10] intentionally omitted <==**

**----- Start of picture text -----**<br>
( ) ( )<br>**----- End of picture text -----**<br>


FIG. 10. Adding noise to the particle momentum at every step causes resonances to decay with time. Here, the Markov chain is initialized with a momentum **p** ∼ _N_ ( **0** _, σp_[2] **[1]**[) and subsequently alternates between a GMC step and the addition of] _[ δ]_ **[p]**[ ∼] _[N]_[ (] **[0]** _[, σ] δ_[ 2] _p_ **[1]**[) to the momentum] vector. We show all combinations of the values ( _σp_ )− = 2 × 10[−][3] , ( _σp_ )+ = 8 × 10[−][3] , ( _σδ p_ )− = ~~√~~ _[σ][p] L_[and][(] _[σ][δ][p]_[)][+][=][ 10(] _[σ][δ][p]_[)][−][, where] _[ L]_[=][ 400.] The SD is calculated for 10[3] independent and identically distributed Markov chains initialized at the same position. In the sphere, the resonances (Fig. 2) are still present, although increasingly damped over time. In the cube, the SD decreases approximately linearly over longer timescales instead of plateauing. The continuous decrease stands in contrast to the discontinuities induced by full momentum rerandomizations in Fig. 2. 

over _L_ steps is approximately √ _Lσδ p_ . This is only strictly true if we did not have reflections, which introduce correlations between particle momenta. However, we aim for only roughly similar behavior so that we set _σδ p_ = ~~√~~ _[σ][p] L_[.] Figure 10 shows the SD against time for this Markov chain for _σp_ ∈{2 × 10[−][3] _,_ 8 × 10[−][3] } and the noise strengths _σδ p_ ∈ { ~~√~~ _[σ][p] L[,]_[ 10] ~~√~~ _[σ][p] L_[}][,][where] _[L]_[=][ 400][is][taken][from][Fig.][2][.][We][show] the SD up to 800 MCS as the trend in the variation of the SD continues thereafter. While the total decrease in SD over 1200 MCS is slightly larger than for GMC, we caution from concluding that the noisy Markov chain mixes faster since we do not compute error bars on the SD to assess statistical significance and we may further optimize the GMC parameter _L_ in Fig. 2. Therefore, we conclude at this point that the overall decrease in the SD over 1200 MCS for _σδ p_ = ~~√~~ _[σ][p] L_[is][similar][to][that][in] Fig. 2, as expected from the choice of _σδ p_ . 

In the sphere, Fig. 10 shows that the oscillations in the SD are damped over time and the SD averaged over an oscillation continuously decreases, as expected. The average SD initially decreases rapidly as in Fig. 2 and shows an approximately linear drift at later times. Increasing _σδ p_ increases the decay rate. Moreover, larger _σδ p_ increases the frequency of oscillations. This can be understood by noting that adding _δ_ **p** broadens the wave front of the particle ensemble so that the particle ensemble reaches the antipodal point of the sphere at an earlier time. 

In the cube, the initial rapid decay of the SD is similar to Fig. 2 as well. Instead of unmixing and plateauing, the SD also exhibits an approximately linear decrease on longer timescales. That is, the resonances are dominated by the effect of the noise, as expected, since they are subdominant compared to the plateauing to begin with and less pronounced than in the sphere. 

In contrast to the sphere, increasing _σδ p_ causes the Markov chain to mix more slowly. This may be understood by noting that the mixing of GMC is bottlenecked by high rejection rates and the entailed trapping in one-dimensional subspaces. 

The comparison above with Langevin dynamics suggests that the average particle momentum increases, which therefore increases the average speed of the particles and hence the rejection rate. This increases the probability of trapping in such a subspace, leading to a slower decay rate. The dynamics in the sphere, in contrast, is rejection free and hence any increase in momentum increases the decay rate, consistent with the discussion in Sec. III A. Overall, this suggests that the optimal value of _σδ p_ depends on the dynamics in the subspace trapping the particles. 

Indeed, the slower mixing with increasing _σδ p_ appears contradictory with Fig. 2. Specifically, suppose that we decrease _L_ to _L_ = 50 MCS for _σp_ = 8 × 10[−][3] in Fig. 2. This would rerandomize the momentum almost exactly when the SD converges to a plateau and hence decrease the SD more rapidly. Decreasing _L_ corresponds to increasing _σδ p_ = ~~√~~ _[σ][p] L_[in Fig.][ 10][.] However, as discussed above, this slows mixing down. The contradiction is resolved by noting that the average momentum increases, as discussed, whereas GMC fully rerandomizes the momentum. Indeed, we observe in Fig. 10 that the SD decreases more rapidly for _σδ p_ = 10 ~~√~~ _[σ][p] L_[than for] _[ σ][δ][p]_[=] ~~√~~ _[σ][p] L_[at] earlier times and only decreases more slowly at later times when the average momentum becomes significantly larger than _σp_ . Reintroducing the parameter _L_ to rerandomize the momentum may prevent this, although increases the number of algorithm parameters to be jointly tuned. 

In summary, the discontinuous rapid decrease of the SD every _L_ steps in GMC is replaced by a gradual decrease distributed over time with similar total decrease in SD. The resonances persist on short timescales albeit decay on longer timescales. Figure 10 suggests that the overall decay profile of the SD is determined by _σp_ , as in GMC, and the optimal tuning of _σδ p_ faces similar considerations as for _L_ , namely a dependency on the geometry of the subspace which a chain initially converges in. 

Returning to GMC, it may alternatively be possible to remove longer time-scale resonances by choosing a different momentum distribution, for example drawing the momentum 

045308-11 

KROUPA, CSÁNYI, AND HANDLEY 

PHYSICAL REVIEW E **111** , 045308 (2025) 

direction isotropically and the magnitude from an independent Gaussian, thus preventing the concentration of the expected jump length of the Markov chain. However, this does not remove the angular concentration present in the sphere, which is a consequence of any isotropic momentum distribution. This suggests that local preconditioning may be necessary, i.e., a coordinate transformation which depends on the current position of the particle. Furthermore, in the context of nested sampling, we expect that the resonances can be further suppressed by increasing the number of live points. In addition, it is an outstanding question if the average chord length, which is a global property of a particular volume, can be statistically inferred from an ensemble of live points to tune _σp_ , especially in a setting in which the volume is nonconvex. While we expect that the necessary noise level and number of live points depends on the maximum height of the particle distribution on a trajectory, the joint tuning of these parameters is beyond the scope of this work. 

## **VI. DISCUSSION** 

We have shown that, for the sphere and cube, an ensemble of particles initialized from the same position with a Gaussian momentum distribution evolving under GMC dynamics exhibits resonance phenomena, which manifest as oscillations in the SD. Additionally, we have shown that the relevant length scale of the sampling problem decreases as a power law in the dimension _n_ for both the sphere and cube, namely _n_[−][1] _[/]_[2] and _n_[(][−][9] _[.]_[86][±][0] _[.]_[02)][×][10][−][1] , respectively. In the cube, the scale is set by the average chord length. The persistence of the oscillations on long timescales is caused by the concentration of the Gaussian momentum distribution combined with the Dirac _δ_ initialization, which lead to an evolution of the particle density akin to a shock wave and hence reverberation of the particle density. On short time-scales, inexact reflections induce bunching, causing additional oscillations. As a consequence, the Markov chain defined by GMC dynamics does not mix monotonically in time but can temporarily unmix, especially in the many-chain and short-time regime. We stress that, even in the few-chain regime, the errors are still prevalent in nested sampling as errors accumulate over multiple nested sampling iterations. 

In particular, the dynamics in the sphere shows that the mixing in the radial coordinate is significantly slower than in the angular coordinates. This behavior is expected on general, nonspherical, boundaries in the high-dimensional limit, as the average length of the momentum vector projection onto the ( _n_ − 1)-dimensional tangent plane is significantly larger than the one-dimensional radial direction. In the context of nested sampling, this biases individual samples to be too close to the boundary, therefore causing a negative systematic error in the Bayesian model evidence, or equivalently the partition function, which grows with dimension. This is seen, for example in Fig. 12 in Ref. [10], wherein the volume at each iteration of nested sampling is nonspherical. This indicates indirectly that the results for the sphere transfer to the more general setting of ellipsoidal volumes. 

Moreover, current state-of-the-art nested sampling codes, e.g., [13], bring the volume at the current iteration in isotropic position, i.e., transform the coordinates such that the co- 

variance of the uniform distribution is the identity, which is a form of preconditioning. This transformation is motivated by the fact that for other Markov chains used on uniform distributions, such as hit-and-run slice sampling or Metropolis-Hastings with a Gaussian proposal, the spherical case is optimal. More precisely, the mixing time of hit-and-run slice sampling [23,49] depends on the square of a condition number, which is the ratio of radii of the smallest ball containing the volume and the largest ball inside the volume. This condition number becomes unity in the spherical case. 

To understand why the spherical case should also be the optimal case for RHMC, we first note that the fraction of rejected points increases as the condition number of the ellipsoid increases while keeping the step size fixed. For illustration, see the depiction of the rejective branch in Fig. 1. This inherently slows mixing down. Consequently, we need to decrease the step size below the spherical case in practice, which causes the propagation of the particles to slow down. Complementary to this picture, we can also analyze the diffusive limit of RHMC as follows. In the limit of a single step per trajectory ( _L_ = 1), RHMC reduces to Metropolis-Hastings with a Gaussian proposal distribution. Taking additionally the zero step size limit ( _σp_ → 0), we obtain Brownian motion. In such a case, the evolution of the particle ensemble is described by the diffusion equation, _∂t p_ ( **x** _, t_ ) = _D_ ∇[2] _p_ ( **x** _, t_ ), with reflective boundary conditions, where _p_ is the particle density and _D_ is a positive scalar diffusion coefficient. For a Dirac _δ_ initialization, _p_ ( **x** _,_ 0) = _δ_ ( **x** − **x** 0), the solution is formally given by 

**==> picture [174 x 13] intentionally omitted <==**

Introducing the eigenfunctions _fi_ of the Laplacian with reflective (Neumann) boundary conditions, ∇[2] _fi_ ( **x** ) = − _μi fi_ ( **x** ), where _μi_ ⩾ 0 is the corresponding eigenvalue, the solution can be expanded as 

**==> picture [209 x 29] intentionally omitted <==**

where _p_ ( **x** _,_ ∞) is the steady-state uniform distribution. We see that the spectral gap of Brownian motion, _μ_ 2, dominates the decay of the initial condition and the largest possible value among all domains for a given volume is attained for a sphere [50]. Hence, mixing in the sphere is fastest. 

In practice, _σp_ is tuned adaptively based on a tuning metric. As the sole measurable quantity which is informative about the environment of the particle is whether a proposed point lies inside or outside the volume, tuning metrics for RHMC are based on tracking this quantity along particle trajectories and computing _σp_ from this information [5,10]. A example method used in practice to tune GMC is the trajectorywise acceptance rate [5], which is the fraction of points (including proposed points in the reflection and rejection branches) along a trajectory which lie inside the volume. Note that this acceptance rate is distinct from the one used in Hamiltonian Monte Carlo for stepsize tuning, which is the acceptance rate of a single proposed point, which is always unity for rejection-free samplers such as GMC and consequently an uninformative metric. 

We argue that the trajectorywise acceptance rate is uninformative about mixing. Regardless of the value computed 

045308-12 

PHYSICAL REVIEW E **111** , 045308 (2025) 

RESONANCES IN REFLECTIVE HAMILTONIAN … 

in a Markov chain, it is not possible to detect if the Markov chain has converged to a subspace of the volume and stopped mixing or to what extent resonances are present in the dynamics. However, to establish at least a necessary condition for stationarity of the Markov chain, we calculate the steady-state value of this metric by preparing independent samples in the volume and running an independent chain from each point. Since the uniform distribution is stationary under the Markov chain [35], the overall particle distribution remains uniform for any choice of _σp_ so that the ensemble average of the trajectorywise acceptance rate is equal to the time average under a Markov chain sampling the stationary distribution. Taking the contrapositive of this statement, if a particular Markov chain does not achieve this acceptance rate, then it is not stationary. 

For the sphere, we find that the acceptance rate tends to 1[large] _[σ][p]_[.][This][is][expected][according][to][the][previously] 2[for] developed picture because most particles move along the boundary so that proposed steps alternate between stepping outside and inside the volume. In the limit of _σp_ → 0, the acceptance rate tends to unity, as it takes multiple steps to reach the boundary. As the dimensionality of the sphere is increased, the threshold speed is lowered above which the acceptance rate becomes 2[1][.] 

For the cube, above the critical value of _σp_ , individual particles become confined to one-dimensional paths. As _σp_ is increased further, the number of steps taken in a path shrinks to 1 so that all particles are trapped at their initial position with the momentum vector inverting at each step. Since the particles thus step outside at every third step, the limiting trajectorywise acceptance rate takes a value of[1][[.]] 

3[[.]] 

In general, for any boundary, the minimum possible value for this metric is[1] 3[. As] _[ σ][p]_[ is decreased, the value is expected to] increase. Hence, a value of at least[1] 3[must be the tuning target,] which stands in tension with the current tuning heuristic of 0 _._ 25–0 _._ 5 [5]. 

## **VII. CONCLUSIONS** 

We have provided a precise picture of the high-dimensional dynamics under inexact reflections and elucidated the mechanism underlying slow mixing, explaining long-standing practical problems with the algorithm, such as systematically negative errors in model evidences and partition functions. In particular, we showed that the particle distribution exhibits a transition between fluidlike and discretization-dominated behavior. The boundary momentum standard deviation _σp_ between these regimes scales as a power law in the dimension, where the exponent depends on the shape of the volume under consideration. Moreover, the particle distribution exhibits spontaneous unmixing, regardless of the regime the algorithm operates in. While the Markov chain eventually converges to the desired uniform distribution under multiple momentum rerandomizations, current tuning metrics, such as the trajectorywise acceptance rate, are disconnected from and therefore uninformative about the short-time dynamics of the algorithm which governs the mixing behavior in the setting under consideration. We therefore envision that our work motivates a revision of current tuning practices and provides a foundation for the development of informative tuning metrics and further 

piecewise-deterministic algorithms operating successfully in high dimensions. 

## **ACKNOWLEDGMENTS** 

N.K. was supported by the Harding Distinguished Postgraduate Scholarship. This work was performed using the Cambridge Service for Data Driven Discovery (CSD3), part of which is operated by the University of Cambridge Research Computing on behalf of the STFC DiRAC HPC Facility [51]. The DiRAC component of CSD3 was funded by BEIS capital funding via STFC capital Grants No. ST/P002307/1 and No. ST/R002452/1 and STFC operations Grant No. ST/R00689X/1. DiRAC is part of the National e-Infrastructure. 

## **DATA AVAILABILITY** 

The data that support the findings of this article are not publicly available upon publication because it is not technically feasible and/or the cost of preparing, depositing, and hosting the data would be prohibitive within the terms of this research project. The data are available from the authors upon reasonable request. 

## **APPENDIX A: EXPLICIT CONSTRUCTION OF THE ROTATION MAP** 

In this Appendix, we first construct basis vectors which then allow us to write down an explicit form of the rotation map (Fig. 11). 

We are given the initial position **q** (0) and **p** (0), which span the disk in which all points of a trajectory, { **q** ( _t_ )} _t_ , lie. Let **ˆn** 1 be the unit vector parallel to **q** (0). Pick an arbitrary unit vector **ˆn** 2 orthogonal to **ˆn** 1. The plane spanned by **ˆn** 1 and **ˆn** 2 defines the plane into which the trajectory will be rotated. Moreover, let **ˆa** be the unit vector produced by Gram-Schmidt orthonormalization of **ˆn** 1 and **p** (0), i.e., **ˆa** = **a** _/_ | **a** | with **a** = ( **1** − **ˆn** 1 **ˆn** 1[⊤][)] **[p]**[(0).][The][vectors] **[ˆn]**[1][and] **[ˆa]**[form][a][basis][for][the] plane of the trajectory. We now construct a rotation matrix **r** ( _ψ_ ) which performs rotations in the **ˆn** 2- **ˆa** plane with angle _ψ_ . Let **b[ˆ]** be the unit vector obtained by Gram-Schmidt orthonormalization of **ˆn** 2 and **ˆa** , i.e., **b[ˆ]** = **b** _/_ | **b** | with **b** = ( **1** − **ˆn** 2 **ˆn** 2[⊤][)] **[ˆa]**[.] Then, 

**==> picture [197 x 32] intentionally omitted <==**

is a rotation matrix which reduces to the two-dimensional rotation matrix in the plane spanned by **ˆn** 2 and **b[ˆ]** and acts as the identity on any vector orthogonal to this plane. Now, let _ψ_ 1 and _ψ_ 2 be the angles which rotate **ˆa** into **ˆn** 2 and − **ˆn** 2, respectively. That is, **r** ( _ψ_ 1) **ˆa** = **ˆn** 2 and **r** ( _ψ_ 2) **ˆa** = − **ˆn** 2. We can now define the rotation matrix in Eq. (4) as 

**==> picture [182 x 25] intentionally omitted <==**

Further, we can rewrite the two conditions in terms of **p** (0) as **ˆa** · **ˆn** 2 = **p** (0) · **ˆn** 2 since **ˆn** 1 · **ˆn** 2 = 0. 

Splitting the rotation matrix **R** into two cases as above is necessary to ensure that isotropic probability distributions are 

045308-13 

KROUPA, CSÁNYI, AND HANDLEY 

PHYSICAL REVIEW E **111** , 045308 (2025) 

**==> picture [122 x 117] intentionally omitted <==**

For a point **x** sampled uniformly from _S[n]_[−][1] , the map is summarized by _θ_ ( **x** ) = sgn( _x_ 2) cos[−][1] _x_ 1 [Eq. (A4)], where sgn( _x_ 2) = _x_ 2 _/_ | _x_ 2| is the sign function and cos[−][1] is the inverse cosine with codomain [0 _, π_ ]. That is, **x** is sent to the upper or lower half-circle depending on the sign of its _x_ 2 component. 

The induced density on the circle is therefore 

**==> picture [223 x 23] intentionally omitted <==**

where the integral is taken over _S[n]_[−][1] and d _S[n]_[−][1] is the surface area element of _S[n]_[−][1] such that | _S[n]_[−][1] | = � d _S[n]_[−][1] . To proceed, we split the density _p_ ( **x** ) at the plane _x_ 2 = 0, 

**==> picture [190 x 24] intentionally omitted <==**

FIG. 11. Vectors used in the construction of the rotation map for the choice **n** 2 = (0 _,_ 1 _,_ 0 _,_ · · · _,_ 0)[⊤] . 

mapped with equal probability into the upper and lower halfdisk, respectively. Concretely, the distribution in Eq. (B1) is symmetric about the **ˆn** 1 axis. 

The matrix **R** maps the **ˆn** 1- **ˆa** plane onto the **ˆn** 1- **ˆn** 2 plane but leaves **ˆn** 1 fixed. To wit, for any vector **q** ( _t_ ) = _q_ 1( _t_ ) **ˆn** 1 + ~~√~~ **q**[2] ( _t_ ) − _q_ 1[2][(] _[t]_[)] **[ˆa]**[in][the][plane][of][the][trajec-] tory, we have 

**Rq** ( _t_ ) = _q_ 1( _t_ ) **ˆn** 1 + sgn( **p** (0) · **ˆn** 2)� **q**[2] ( _t_ ) − _q_ 1[2][(] _[t]_[)] **[ˆn]**[2] _[,]_ (A3) as required, where sgn is the sign function. In particular, the angle _θ_ between **ˆn** 1 ∝ **q** (0) and **Rq** ( _t_ ) is _θ_ = sgn( **p** (0) · **ˆn** 2) cos[−][1] _q_ 1( _t_ ). 

The above construction simplifies significantly for specific choices of the axes. Without loss of generality, assume that the initial position of each particle lies on the _x_ 1 axis so that **ˆn** 1 ∝ **q** (0) = ( _q_ (0) _,_ 0 _, . . . ,_ 0)[⊤] . If this is not the case, then there is a global rotation of all particle trajectories which achieves this as they are initialized at the same position. Now, choose **ˆn** 2 = (0 _,_ 1 _,_ 0 _, . . . ,_ 0)[⊤] to be the _x_ 2 axis and relabel **x** = **q** ( _t_ ) = ( _x_ 1 _, . . . , xn_ ). Then the expression for the angle _θ_ simplifies to 

**==> picture [173 x 12] intentionally omitted <==**

Finally, we remark that if **x** lies on a sphere, then it is sent to the circle since **R** is a rotation. 

We can also consider the action of **R** on the initial momentum **p** (0) in a coordinate system centered at **q** (0). The angle _φ_ between **p** (0) and **q** (0) is the analog of _θ_ (Fig. 11). In particular, _φ_ also has a distribution ∝| sin _φ_ | _[n]_[−][2] if **p** (0) is distributed isotropically (Appendix B). 

where _�_ is the Heaviside step function. Inserting into Eq. (B2) splits the integral over the sphere into two half-spheres, each with a definite value of sgn _x_ 2: 

**==> picture [216 x 55] intentionally omitted <==**

In the first integral, substituting _x_ 2 →− _x_ 2 changes the domain of integration from the half-sphere _x_ 2 _>_ 0 to the halfsphere _x_ 2 _<_ 0 but leaves the area element d _S[n]_[−][1] invariant, thus giving 

**==> picture [197 x 52] intentionally omitted <==**

Adding both sides of this equation and using _�_ (− _x_ 2) + _�_ ( _x_ 2) = 1, we obtain 

**==> picture [186 x 51] intentionally omitted <==**

as expected, since mapping a half-sphere onto the upper halfcircle gives the same density as mapping the entire sphere onto the upper half-circle and dividing by two. 

We can now evaluate this integral directly. Splitting _S[n]_[−][1] along the _x_ 1 axis into ( _n_ − 2)-dimensional spheres of radius ~~√~~ 1 − _x_ 1[2][, each with arc length d] _[x]_[1] _[/]_ √1 − _x_ 1[2][, we have [][52][]] 

**==> picture [191 x 15] intentionally omitted <==**

Moreover, using the relation 

## **APPENDIX B: DERIVATION OF THE INDUCED PROBABILITY DENSITY ON THE CIRCLE** 

In the following, we show that a uniform density _p_ ( **x** ) = 1 _/_ | _S[n]_[−][1] | on the unit ( _n_ − 1)-sphere _S[n]_[−][1] with surface area | _S[n]_[−][1] | is mapped by Eq. (4) to the density 

yields 

**==> picture [205 x 15] intentionally omitted <==**

**==> picture [221 x 23] intentionally omitted <==**

**==> picture [438 x 26] intentionally omitted <==**

on the circle _S_[1] parameterized by the angle _θ_ ∈ [− _π, π_ ]. 

**==> picture [211 x 12] intentionally omitted <==**

045308-14 

PHYSICAL REVIEW E **111** , 045308 (2025) 

RESONANCES IN REFLECTIVE HAMILTONIAN … 

**==> picture [227 x 68] intentionally omitted <==**

**----- Start of picture text -----**<br>
7 0.4 ~4<br>n<br>1S)<br>ww<br>& 0.2 :<br>7<br>)<br>( ln (PSD)<br>**----- End of picture text -----**<br>


FIG. 12. Sketch of the trajectory for the derivation of the supersonic frequency. Magnitude of the momentum **v** is significantly exaggerated for visualization purposes. Here, **˜q** 1 and **˜q** 2 are a basis spanning the plane of the trajectory. 

where the Heaviside step function was inserted to ensure that the integral is only nonzero for _θ_ ∈ [0 _, π_ ]. 

Similarly, the second integral in Eq. (B4) evaluates to the same expression but with _θ_ →− _θ_ , which holds for _θ_ ∈ [− _π,_ 0]. Substituting both integrals into Eq. (B4) and using (3) ( _θ_ ) + (2) (− _θ_ ) = 1, we finally obtain Eq. (B1). We note that Eq. (B1) is correctly normalized since | _S[n]_[−][2] | _/_ | _S[n]_[−][1] | = ( _n_ − 2)!! _/_ [ _κn_ ( _n_ − 3)!!] and 2 _π_ 0 d _θ_ | sin _θ_ | _[n]_[−][2] = 2 _κn_ ( _n_ − 3)!! _/_ ( _n_ − 2)!!, where _κn_ = _π_ if _n_ is even and _κn_ = 2 if _n_ is odd. 

## **APPENDIX C: DERIVATION OF THE SUPERSONIC FREQUENCY** 

Assume a particle is at initial position **r** _i_ (Fig. 12). A trajectory which follows the boundary as closely as possible alternates between stepping into and out of the disk. We assume that the momentum is orthogonal to the particle position as this is the most probable configuration in high dimensions, according to Eq. (B1). After one Monte Carlo time step, the new particle position is **r** _f_ = **r** _i_ + 2( **1** − **r** _m_ **r** _m_[⊤][)] **[v]**[,] where **ˆr** _m_ = ( **r** _i_ + **r** _f_ ) _/_ | **r** _i_ + **r** _f_ |. Since **r** _i_ · **v** = 0, **r** _i_ · **ˆr** _m_ = _r_ 0 cos( A@/ 2) and **ˆr** _m_ · **v** = | **v** | sin( Aé/ 2), the traversed angle A@ = cos[−][1] ( **ˆr** _i_ · **ˆr** _f_ ) satisfies 

FIG. 13. Same as Fig. 5 but with a larger range of _σp_ on a logscale. 

_r_ 0 ≈ _R_ . Substituting these into Eq. (C2) gives the supersonic frequency _f_ super [Eq. (8)]. 

## **APPENDIX D: POWER SPECTRAL DENSITY FOR THE SPHERE** 

Figure 13 is identical to Fig. 5 but includes a wider range of _σp_ values. The aliasing discussed in Sec. III C is more clearly visible. At _σp_ significantly larger than _n_[−][1] _[/]_[2] , the frequency reaches the Nyquist limit. This is a consequence of almost all particles switching between the initial and antipodal position at every time step. Therefore, the Sinkhorn divergence remains at its maximum value and no mixing is observed. 

## **APPENDIX E: SCALING OF THE MEAN CHORD LENGTH WITH DIMENSION** 

For a given direction **ˆn** and point **x** 0, the chord length _ℓ_ is the length of the intersection of the line **x** ( _s_ ) = **x** 0 + _s_ **ˆn** with the cube. The vector **ˆn** and **x** 0 are sampled uniformly from a sphere and the cube, respectively. This gives 10[4] samples of _ℓ_ , from which we compute the mean ⟨ _ℓ_ ⟩. The dependence on dimension is shown in Fig. 14 and is described by a power law with exponent (−4 _._ 86 ± 0 _._ 02) × 10[−][1] . 

**==> picture [181 x 23] intentionally omitted <==**

which yields 

**==> picture [187 x 29] intentionally omitted <==**

choosing the branch for which A@ ∈ [0 _, π/_ 2]. The frequency with which such a particle moves between antipodal points is approximately Ad/1 , assuming that the discretization error is negligible. In high dimensions, the momentum distribution is concentrated in a thin shell around | **v** | ≈ _σp_ ~~√~~ _n_ and the initial position is close to the boundary, 

FIG. 14. Monte Carlo estimate of the mean chord length in the cube for dimensionalities _n_ ∈ [50 _,_ 350] on a log-log plot. 

045308-15 

KROUPA, CSÁNYI, AND HANDLEY 

PHYSICAL REVIEW E **111** , 045308 (2025) 

- [1] R. M. Neal, Slice sampling, Ann. Stat. **31** , 705 (2003). 

- [2] J. Skilling, Nested sampling for general Bayesian computation, Bayesian Anal. **1** , 833 (2006). 

- [3] F. Feroz, M. Hobson, and M. Bridges, Multinest: An efficient and robust Bayesian inference tool for cosmology and particle physics, Mon. Not. R. Astron. Soc. **398** , 1601 (2009). 

- [4] L. B. Pártay, A. P. Bartók, and G. Csányi, Efficient sampling of atomic configurational spaces, J. Phys. Chem. B **114** , 10502 (2010). 

- [5] L. B. Pártay, G. Csányi, and N. Bernstein, Nested sampling for materials, Eur. Phys. J. B **94** , 159 (2021). 

- [6] G. Ashton, N. Bernstein, J. Buchner, X. Chen, G. Csányi, A. Fowlie, F. Feroz, M. Griffiths, W. Handley, M. Habeck _et al._ , Nested sampling for physical scientists, Nat. Rev. Methods Primers **2** , 39 (2022). 

- [7] J. Buchner, Nested sampling methods, Stat. Surveys **17** , 169 (2023). 

- [8] J. Skilling, Bayesian computation in big spaces-nested sampling and Galilean Monte Carlo, in _Bayesian Inference and Maximum Entropy Methods in Science and Engineering: 31st International Workshop on Bayesian Inference and Maximum Entropy Methods in Science and Engineering_ (American Institute of Physics, Melville, New York, 2012), Vol. 1443, pp. 145–156. 

- [9] J. Skilling, Galilean and Hamiltonian Monte Carlo, in _Proceedings of the 39th International Workshop on Bayesian Inference and Maximum Entropy Methods in Science and Engineering_ (MDPI, Basel, Switzerland, 2019), Vol. 33, p. 19. 

- [10] P. Lemos, N. Malkin, W. Handley, Y. Bengio, Y. Hezaveh, and L. Perreault-Levasseur, Improving gradient-guided nested sampling for posterior inference, in _International Conference on Machine Learning_ (PMLR, 2024), pp. 27230–27253. 

- [11] J. Olander, _Constrained space MCMCmethods for Nested Sampling Bayesian Computations_ (Chalmers University of Technology, Gothenburg, Sweden, 2020). 

- [12] R. L. Smith, Efficient Monte Carlo procedures for generating points uniformly distributed over bounded regions, Oper. Res. **32** , 1296 (1984). 

- [13] W. Handley, M. Hobson, and A. Lasenby, Polychord: Nextgeneration nested sampling, Mon. Not. R. Astron. Soc. **453** , 4385 (2015). 

- [14] A. G. Baydin, B. A. Pearlmutter, A. A. Radul, and J. M. Siskind, Automatic differentiation in machine learning: A survey, J. Mach. Learn. Res. **18** , 1 (2018). 

- [15] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga _et al._ , PyTorch: An imperative style, high-performance deep learning library, in _33rd Conference on Neural Information Processing Systems (NeurIPS 2019), Vancouver, Canada_ 32 (2019). 

- [16] J. Ruiz-Zapatero, B. Hadzhiyska, D. Alonso, P. G. Ferreira, C. García-García, and A. Mootoovaloo, Analytical marginalization over photometric redshift uncertainties in cosmic shear analyses, Mon. Not. R. Astron. Soc. **522** , 5037 (2023). 

- [17] O. T. Unke, S. Chmiela, H. E. Sauceda, M. Gastegger, I. Poltavsky, K. T. Schütt, A. Tkatchenko, and K.-R. Müller, Machine learning force fields, Chem. Rev. **121** , 10142 (2021). 

- [18] S. Brooks, A. Gelman, G. Jones, and X.-L. Meng, _Handbook of Markov chain Monte Carlo_ (CRC Press, Boca Raton, FL, 2011). 

- [19] F. H. Stillinger, Exponential multiplicity of inherent structures, Phys. Rev. E **59** , 48 (1999). 

- [20] M. Hoare and J. McInnes, Statistical mechanics and morphology of very small atomic clusters, Faraday Discuss. Chem. Soc. **61** , 12 (1976). 

- [21] C. Tsai and K. Jordan, Use of an eigenmode method to locate the stationary points on the potential energy surfaces of selected argon and water clusters, J. Phys. Chem. **97** , 11227 (1993). 

- [22] C. J. Pickard and R. Needs, _Ab initio_ random structure searching, J. Phys.: Condens. Matter **23** , 053201 (2011). 

- [23] L. Lovász and S. Vempala, Hit-and-run from a corner, in _Proceedings of the 36th Annual ACM Symposium on Theory of Computing_ (ACM, New York, NY, 2004), pp. 310–314. 

- [24] L. Lovász and M. Simonovits, Random walks in a convex body and an improved volume algorithm, Random Struct. Algorithms **4** , 359 (1993). 

- [25] R. Kannan, L. Lovász, and R. Montenegro, Blocking conductance and mixing in random walks, Comb. Probab. Comput. **15** , 541 (2006). 

- [26] L. Lovász and M. Simonovits, The mixing rate of Markov chains, an isoperimetric inequality, and computing the volume, in _Proceedings of the 31st Annual Symposium on Foundations of Computer Science_ (IEEE, Piscataway, NJ, 1990), pp. 346–354. 

- [27] S. Vempala, Geometric random walks: A survey, Comb. Comput. Geom. **52** , 573 (2005). 

- [28] F. Feroz and J. Skilling, Exploring multi-modal distributions with nested sampling, in _Bayesian Inference and Maximum Entropy Methods in Science and Engineering: 32nd International Workshop on Bayesian Inference and Maximum Entropy Methods in Science and Engineering_ (American Institute of Physics, Melville, New York, 2013), Vol. 1553, pp. 106–113. 

- [29] I. Z. Emiris and V. Fisikopoulos, Efficient random-walk methods for approximating polytope volume, in _Proceedings of the 30th Annual Symposium on Computational Geometry, Kyoto, Japan_ (Association for Computing Machinery, New York, NY, 2014), pp. 318–327. 

- [30] A. Chevallier, F. Cazals, and P. Fearnhead, Efficient computation of the the volume of a polytope in high-dimensions using piecewise deterministic Markov processes, in _Proceedings of the International Conference on Artificial Intelligence and Statistics_ (PMLR, New York, NY, 2022), pp. 10146–10160. 

- [31] H. Mohasel Afshar and J. Domke, Reflection, refraction, and Hamiltonian Monte Carlo, Adv. Neural Info. Process, Syst. **28** , 1 (2015). 

- [32] S. Hee, W. Handley, M. P. Hobson, and A. N. Lasenby, Bayesian model selection without evidences: Application to the dark energy equation-of-state, Mon. Not. R. Astron. Soc. **455** , 2461 (2016). 

- [33] N. Kroupa, D. Yallup, W. Handley, and M. Hobson, Kernel-, mean-, and noise-marginalized gaussian processes for exoplanet transits and H0 inference, Mon. Not. R. Astron. Soc. **528** , 1232 (2024). 

- [34] A. Fowlie, W. Handley, and L. Su, Nested sampling with plateaus, Mon. Not. R. Astron. Soc. **503** , 1199 (2021). 

- [35] See Supplemental Material at http://link.aps.org/supplemental/ 10.1103/PhysRevE.111.045308 for a proof that the stationary distribution is uniform. 

- [36] J. A. Brofos and R. R. Lederman, On numerical considerations for Riemannian manifold Hamiltonian Monte Carlo, arXiv:2111.09995. 

- [37] J. Brofos and R. R. Lederman, Evaluating the implicit midpoint integrator for Riemannian Hamiltonian Monte Carlo, in 

045308-16 

PHYSICAL REVIEW E **111** , 045308 (2025) 

RESONANCES IN REFLECTIVE HAMILTONIAN … 

_Proceedings of the International Conference on Machine Learning_ (PMLR, New York, NY, 2021), pp. 1072–1081. 

- [38] C. Dellago, H. A. Posch, and W. G. Hoover, Lyapunov instability in a system of hard disks in equilibrium and nonequilibrium steady states, Phys. Rev. E **53** , 1485 (1996). 

- [39] M. Cuturi, Sinkhorn distances: Lightspeed computation of optimal transport, Adv. Neural Info. Process. Syst. **26** , 1 (2013). 

- [40] A. Genevay, M. Cuturi, G. Peyré, and F. Bach, Stochastic optimization for large-scale optimal transport, Adv. Neural Info. Process. Syst. **29** , 1 (2016). 

- [41] A. Genevay, G. Peyré, and M. Cuturi, Learning generative models with Sinkhorn divergences, in _Proceedings of the International Conference on Artificial Intelligence and Statistics_ (PMLR, New York, NY, 2018), pp. 1608–1617. 

- [42] J. Feydy, T. Séjourné, F.-X. Vialard, S.-i. Amari, A. Trouvé, and G. Peyré, Interpolating between optimal transport and MMD using Sinkhorn divergences, in _Proceedings of the 22nd International Conference on Artificial Intelligence and Statistics_ (PMLR, New York, NY, 2019), pp. 2681–2690. 

- [43] A. Genevay, L. Chizat, F. Bach, M. Cuturi, and G. Peyré, Sample complexity of Sinkhorn divergences, in _Proceedings of the 22nd International Conference on Artificial_ 

   - _Intelligence and Statistics_ (PMLR, New York, NY, 2019), pp. 1574–1583. 

- [44] M. Cuturi, L. Meng-Papaxanthos, Y. Tian, C. Bunne, G. Davis, and O. Teboul, Optimal transport tools (OTT): A JAX toolbox for all things Wasserstein, arXiv:2201.12324. 

- [45] R. Vershynin, _High-dimensional Probability: An Introduction with Applications in Data Science_ (Cambridge University Press, Cambridge, UK, 2018), Vol. 47. 

- [46] E. Ott, _Chaos in Dynamical Systems_ (Cambridge University Press, Cambridge, UK, 2002). 

- [47] K. Ball _et al._ , An elementary introduction to modern convex geometry, Flavors Geom. **31** , 1 (1997). 

- [48] T. M. Cover, _Elements of Information Theory_ (John Wiley & Sons, New York, NY, 1999). 

- [49] L. Lovász, Hit-and-run mixes fast, Math. Program. **86** , 443 (1999). 

- [50] H. F. Weinberger, An isoperimetric inequality for the _n_ - dimensional free membrane problem, J. Ration. Mech. Anal. **5** , 633 (1956). 

- [51] www.dirac.ac.uk. 

- [52] C. Müller, _Analysis of Spherical Symmetries in Euclidean Spaces_ (Springer Science & Business Media, Cham, 2012), Vol. 129. 

045308-17 

