**10502** 

_J. Phys. Chem. B_ **2010,** _114,_ 10502–10512 

## **Efficient Sampling of Atomic Configurational Spaces** 

## **Lı´via B. Pa´rtay,*[,†] Albert P. Barto´k,[‡] and Ga´bor Csa´nyi[§]** 

_Uni_ V _ersity Chemical Laboratory, Uni_ V _ersity of Cambridge, Lensfield Road, Cambridge CB2 1EW, United Kingdom, Ca_ V _endish Laboratory, Uni_ V _ersity of Cambridge, J. J. Thomson A_ V _enue, Cambridge CB3 0HE, United Kingdom, and Engineering Laboratory, Uni_ V _ersity of Cambridge, Trumpington Street, Cambridge CB2 1PZ, United Kingdom_ 

_Recei_ V _ed: February 10, 2010; Re_ V _ised Manuscript Recei_ V _ed: July 2, 2010_ 

We describe a method to explore the configurational phase space of chemical systems. It is based on the nested sampling algorithm recently proposed by Skilling ( _AIP Conf. Proc._ **2004** , 395; _J. Bayesian Anal._ **2006** , _1_ , 833) and allows us to explore the _entire_ potential energy surface (PES) efficiently in an unbiased way. The algorithm has two parameters which directly control the trade-off between the resolution with which the space is explored and the computational cost. We demonstrate the use of nested sampling on Lennard-Jones (LJ) clusters. Nested sampling provides a straightforward approximation for the partition function; thus, evaluating expectation values of arbitrary smooth operators at arbitrary temperatures becomes a simple - postprocessing step. Access to absolute free energies allows us to determine the temperature density phase diagram for LJ cluster stability. Even for relatively small clusters, the efficiency gain over parallel tempering in calculating the heat capacity is an order of magnitude or more. Furthermore, by analyzing the topology of the resulting samples, we are able to visualize the PES in a new and illuminating way. We identify a discretely valued order parameter with basins and suprabasins of the PES, allowing a straightforward and unambiguous definition of macroscopic states of an atomistic system and the evaluation of the associated free energies. 

## **Introduction** 

The study of potential energy hypersurfaces (PES) by computational tools is one of the most rapidly developing areas within chemistry and condensed matter physics. The potential energy (or Born-Oppenheimer) surface describes the energy of a group of atoms or molecules in terms of the geometrical structure (the set of nuclear coordinates), with the electrons in their ground state.[3] The local minima and the associated “basins” of the potential energy surface represent metastable states, and the global minimum corresponds to the stable equilibrium configuration at zero temperature. The saddle points (of index one) correspond to transition states that link neighboring local minima and, within the approximation of transition-state theory, dominate the processes that involve structural change in the atomic configuration. The dimensionality of the PES scales linearly with the number of atoms; however, the number of local minima is commonly thought to scale exponentially,[4] which makes exploration of the PES computationally very demanding. For soft matter, liquid, and disordered systems, the physics is often dominated by entropic effects, and the calculation of free energies requires a sampling over large regions of the PES. For solid-state systems, the unexpected discoveries of new lowenergy configurations in hitherto unexplored parts of the configurational phase space have consistently appeared prominently in leading scientific journals.[5][-][11] 

The past decade has seen huge activity in designing simulation schemes that map out complex energy landscapes.[12,13] Several methods have been developed to map different kinds of energy landscapes, optimized to discover different parts of the PES, 

> * Towhomcorrespondenceshouldbeaddressed.E-mail:lb415@cam.ac.uk. 

> † University Chemical Laboratory, University of Cambridge, Lensfield Rd. 

> ‡ Cavendish Laboratory, University of Cambridge, J. J. Thomson Ave. 

> § Engineering Laboratory, University of Cambridge, Trumpington St. 

applicable to different sorts of problems. Global optimization methods include basin hopping,[14] genetic algorithms (GA),[15,16] and minima hopping.[17] Temperature-accelerated dynamics[18] - samples rare events, while parallel tempering,[19,20] Wang Landau sampling,[21] and metadynamics[22] enable the evaluation of relative free energies. Each method has its particular set of advantages and disadvantages, but what they have in common is that they (except for some implementations of GA) are, in practice, all “bottom up” approaches, i.e. start from known energy minima and explore neighboring basins. The essential difference between the methods is in how they move from one basin to another. 

A new sampling scheme, nested sampling, was recently introduced by Skilling[1,2] in the field of applied probability and inference, to sample probability densities in high-dimensional spaces where the regions contributing most of the probability mass are exponentially localized. The data analysis method based on the same sampling scheme has already found use in the field of astrophysics.[23] In this paper we adapt the nested sampling approach for exploring atomic configurational phase spaces and not only provide a new framework for efficiently computing thermodynamic observables, but show a new way of visualizing the pertinent features of complex energy landscapes. 

To demonstrate the key idea of nested sampling, we illustrate its behavior in Figure 1 for a first-order phase transition and - compare it with parallel tempering and Wang Landau sampling. A first-order phase transition is characterized by a dramatic reduction of the available phase space as the energy of the system is reduced. All three methods operate by simultaneously or sequentially sampling states of the system at a series of energy or temperature levels (for a large system, these are equivalent). For the overall sampling to be successful, the samplers at each level have to equilibrate with those on every other level. We consider parallel tempering first, which samples at fixed temperatures (top panel). The overlap between the distributions 

10.1021/jp1012973  2010 American Chemical Society Published on Web 07/26/2010 

_J. Phys. Chem. B, Vol. 114, No. 32, 2010_ **10503** 

Exploration of Atomic Configurational Spaces 

with equal probability. Accordingly, the expectation value of an observable _A_ is the simple sum over the microstates of the system, 

**==> picture [160 x 30] intentionally omitted <==**

where _x_ and _p_ are the positions and momenta, respectively, and the partition function _Z_ is the normalization constant, in this case just the total phase space volume. However, when a system is in thermal equilibrium with its surroundings, the occupation probability of its internal states is given by the canonical distribution and the expectation value of the observable is 

**==> picture [182 x 25] intentionally omitted <==**

where _H_ is the Hamiltonian of the system, B is the inverse thermodynamic temperature, and _Z_ ( p ) is the canonical partition function, 

**Figure1.** Ilustrationofhowparalleltempering(toppanel),Wang-Landau sampling (middle panel), and nested sampling (bottom panel) deal with a first-order phase transition. In each panel, the width of the black curve at a given height represents the logarithm of the available configurational phase space, ln [Γ( _E_ )], as a function of potential energy, _E_ . This is an entropy-like quantity but considered as a function of potential energy, rather than temperature. The series of sampling regions (in temperatures or energies) are represented by horizontal lines. The thick lines on the top two panels on either side of the phase transition show the entropy jump that makes equilibration difficult. Nested sampling avoids this by constructing a series of energy levels equispaced in ln Γ. 

at levels just above and just below the phase transition is very small, vanishing in the thermodynamic limit, due to the entropy jump. It is well-understood that this makes equilibration of the samplers in the two phases especially difficult.[24] Furthermore, due to the steep increase of the energy near the transition temperature (see inset), the spacing of the corresponding energy levels becomes wider near the phase transition, making equilibration even harder. 

- Wang Landau sampling (middle panel) is done on energy levels constructed to be equispaced, but large systems are still very difficult to equilibrate due to the entropy jump, resulting in broken ergodicity. This phase equilibration problem can be solved by constructing a sequence of energy levels in such a way that the phase space volume ratios corresponding to successive energy levels is an _O_ (1) constant, as shown on the bottom panel. Hence, the energy level spacings near the phase transition will be narrow, precisely what is needed to allow good equilibration. The nested sampling algorithm, described below, constructs just such a sequence of energy levels using a single top-down pass. This sequence is similar in spirit to the sequence of temperatures that would be obtained at the _end_ of a parallel tempering run which adapts the temperature levels until all exchanges between neighboring levels is the same _O_ (1) constant.[25,26] 

## **Nested Sampling** 

The fundamental principle of statistical mechanics is that, in equilibrium, all accessible states of an isolated system occur 

**==> picture [210 x 136] intentionally omitted <==**

where _E_ is the potential energy, _V_ is the volume, _δV_ is the volume element of the spatial discretization, _N_ is the number of particles, and the momentum-dependent part has been separated out as usual, 

where _m_ is the mass of the particles and _h_ is Planck’s constant. Defining _w_ ≡ _δV_ / _V[N]_ , the position-dependent part of the partition function is 

**==> picture [162 x 22] intentionally omitted <==**

with 

**==> picture [139 x 23] intentionally omitted <==**

We assume that the operator _A_ does not depend explicitly on the momentum variables and consider estimating _A_ and _Zx_ ( B ) directly by turning them into sums over a set of _sample points_ { _xi_ }, 

**==> picture [186 x 62] intentionally omitted <==**

where _wi_ is the (now not necessarily uniform) weight factor representing the volume element associated with the sample point _xi_ , still with the normalization 

**==> picture [239 x 41] intentionally omitted <==**

In general, it is difficult to find a set of sample points that gives a good coverage of phase space and a good approximation of observables and the partition function at low and moderate temperatures because the Boltzmann factor is very sharply peaked near states with low energy, and such states occupy an extremely small volume in phase space. This, in essence, is the “sampling problem” in molecular simulation. Note that, in principle, eqs 7 and 8 could be used to estimate the partition function using samples from a regular Monte Carlo simulation by evaluating the ensemble average of the observable _A_ ) exp( _E_ ( _x_ )), 

**==> picture [200 x 24] intentionally omitted <==**

However, in practice, the above sum is essentially impossible to evaluate in finite time because the variance of exp( _E_ ) is divergent at low temperatures. This approximation is called the “harmonic mean approximation” in the probability literature;[27] for further details see the discussion by C. P. Robert and N. Chopin.[28] 

In the nested sampling method, illustrated in Figure 2, we instead break up the sums in eqs 7 and 8 into terms associated with a series of decreasing energy levels { _En_ } each with a corresponding weight factor, which are also decreasing. For each level, a set of _K_ sample points { _xj[n]_ } is obtained by uniform sampling from the energy landscape _below En_ : 

**==> picture [226 x 56] intentionally omitted <==**

where _n_ runs over the energy levels and for each level _j_ runs over those sample points that lie between the successive pair of levels. To complete the description of the algorithm, it remains to specify how the samples _xj[n]_ are drawn in eq 11. We use a simple rejection Gibbs sampler,[29,30] in the form of a strictly bounded random walker that at each level _n_ is constrained to remain inside the region { _x_ : _E_ ( _x_ ) < _En_ }. The nested sampling algorithm as described here is the generalization of the work of Skilling and equivalent to it for the choice R ) _K_ /( _K_ +1). For this special choice, which we also adopt in the rest of this work, the sum over _j_ in eq 12 has only one term, since precisely one sample is contained in the top 1/ _K_ fraction of each sample set. 

Thermodynamic quantities are obtained from the partition function; for example, the heat capacity is given by 

**==> picture [181 x 21] intentionally omitted <==**

The expectation value of the internal energy can be written, in terms of the samples, as 

**==> picture [166 x 12] intentionally omitted <==**

After iteration _n_ we create the new lowest energy level _En_ +1 at a fixed percentile, denoted by fraction R, of the energy distribution of the samples at level _n_ . Thus, the sample points corresponding to each energy level will have a combined phase space volume that is a factor R smaller than that of the previous level, so the phase space volume of the _n_ th level is (R) _[n]_ . The sample points that lie between levels _En_ and _En_ +1 contribute to the overall sample with a weight _wn_ that is the difference between the phase space volumes corresponding to the two levels, _wn_ ) (R) _[n]_ - (R) _[n]_[+][1] . Since the phase space volumes decrease exponentially for a fixed R, the overall sampling converges quickly and is able to locate exponentially small parts of configurational space. At the same time, because every pair of neighboring energy levels has a phase space volume ratio of R (even near energies that correspond to discontinuous phase transitions), there is no inherent difficulty in generating the samples, and there is no “equilibration problem”; see the bottom panel of Figure 1. 

After a sufficient number of iterations, using all the samples from eq 11 for all levels, the nested sampling approximation of the configurational partition function and of an observable becomes 

**==> picture [206 x 24] intentionally omitted <==**

**Figure 2.** Illustration of the nested sampling iterations. Each curve represents an energy histogram of samples: curves on the left are the samples of the current iteration, while those on the right are the weighted histograms of all the samples collected. The red part of the total histograms on the right represents the new contribution, appropriately scaled, from the current iteration on the left. After every iteration, once the new samples have been collected, the new lowest energy level is defined to be at a fixed percentile (as a fraction R) of the current sample histogram, illustrated by the red dashed line. This ensures that the new energy level corresponds to a phase space volume, which is a fraction R smaller than the previous one. 

_J. Phys. Chem. B, Vol. 114, No. 32, 2010_ **10505** 

Exploration of Atomic Configurational Spaces 

**==> picture [241 x 165] intentionally omitted <==**

The convergence of the nested sampling procedure has been extensively discussed,[31,32] and the error in ln _Z_ scales as _K_[-][1/2] . Note that in contrast to the case of general distributions, the convergence results in statistical mechanics are easier to obtain because the energy is bounded from below. 

Finally, note the absence of the temperature _�_ in the actual sampling algorithm. Since exp(- _�E_ ) is a monotonic function of _E_ , the above derivation of the sampling weights is independent of _�_ . Thus, the expectation value of any observable can be evaluated at an arbitrary temperature just by resumming over the same sample set, obviating the need to generate a new sample set specific to each desired temperature. The exponential refinement of the sampling for low energies becomes increasingly less relevant (but not incorrect) at higher temperatures for which the low-energy states contribute less to the partition function. This athermal aspect of the sampling scheme is similar - to that of the Wang Landau method.[21,33,34] However, the convergence problems[35,36] that typically arise for systems with broken ergodicity are not present in our case, due to the topdown nature of the method: the samples are uniformly distributed at each energy level, and the low-energy samples are directly obtained from the higher energy ones. For a given _K_ , nested sampling always converges, and _K_ determines the resolution with which we sample the basins of the PES. If a particular basin in its energy range has a phase space volume ratio relative to the rest of the space that is smaller than about 1/ _K_ , the probability that a sample point will ever fall into that basin is small. Therefore, by increasing _K_ , we are able to explore the PES with higher resolution. Notice how this limited resolution is related to an effective minimum temperature: if a sampling set explores basins whose phase space volumes are typically larger than some value, then there will be a corresponding temperature above which these basins will dominate the behavior of the system due to their entropy. 

## **Lennard-Jones Clusters** 

We demonstrate the new framework in the context of Lennard-Jones (LJ) clusters, which is a favorite testing ground for new phase space exploration schemes, partly because the potential energy function is cheap to calculate and partly because an enormous amount of data has been amassed about the potential energy landscape in the literature.[3,14,37,38] 

We performed nested sampling on a number of LJ particles, with potential parameters _ε_ and _σ_ , in a periodic box, corresponding to a low density of 2.31 × 10[-][3] _σ_[-][3] , using a cutoff of 3 _σ_ , such that at low temperature the particles aggregate into a cluster. The heat capacities of small LJ clusters are shown in Figure 3, calculated according to eq 16. Note that since the 

nested sampling procedure is independent of temperature, only one simulation was needed for each cluster size, after which the heat capacity is trivial to evaluate at an arbitrary temperature. For each cluster, a shoulder and a large peak is present, corresponding to melting and sublimation. For our largest clusters with 31, 36, and 38 atoms, the new peak at low temperature, discussed in more detail below, is traditionally - associated with the so-called Mackay anti-Mackay transition.[39,40] 

The size of the sample set was increased until convergence of the heat capacity was achieved, and it is shown in Table 1, together with the number of energy evaluations performed during the calculations. The inset of Figure 3 shows the average error in the heat capacity as a function of the sample size. The convergence shows a power law behavior with a slope that corresponds to an _O_ ( _K_[-][1/2] ) error, typical in statistical sampling. 

To demonstrate the power of nested sampling, we chose two Lennard-Jones clusters and calculated the heat-capacity curves using parallel tempering. The resulting comparison is shown in Figure 4. For the parallel tempering calculations we chose a set of equispaced temperatures with a spacing that can resolve the peaks. To achieve a fair comparison, both methods were converged until the respective maximum errors in the heat capacities were about the same. As mentioned above, nested sampling automatically yields the observables as a continuous function of temperature. In the case of parallel tempering, where heat capacity values are observed directly only at the discrete set of temperatures, to obtain values at intermediate temperatures we used Boltzmann reweighting on the samples from the Markov chains at successive pairs of temperatures.[41] For LJ17 the efficiency gain of nested sampling is a factor of 10 over parallel tempering, while for the larger LJ25 cluster, as the entropy jump is larger, the efficiency gain is a factor of 100. 

Our heat capacity curves for the largest clusters (LJ31, LJ36, and LJ38) are consistent with what is reported in the literature,[38,42] using computational resources of similar order of magnitude. Note, however, that advance knowledge of the global minimum is not required and was not used in the nested sampling simulations. The relatively large computational cost for LJ31 and LJ38 is precisely because these clusters have global minima which are hard to find.[43] See below for a more detailed discussion of the relative sizes of the basins containing the global and lowest local minima. 

## **LJ Cluster Phase Diagram** 

The ability to compute the partition function and hence the absolute free energy _A_ , as 

**==> picture [160 x 22] intentionally omitted <==**

enables us to plot in Figure 5 a phase diagram showing the stability of the Lennard-Jones clusters against the ideal gas (i.e., evaporation) as a function of density and temperature. The total partition function of the ideal gas is _Z_ p (see eq 4) since the potential energy is zero. We performed the nested sampling calculations at a single density (marked by an arrow in Figure 5), in which individual clusters are formed that do not interact with their periodic images. The partition function for lower densities can be approximated by multiplying the partition function by a _V_ ′/ _V_ factor, where the volume _V_ ′ corresponds to the new density; thus, the translational freedom of the cluster in a larger volume is included. Finally, for every Lennard-Jones cluster at a given density, the critical temperature at which its 

**10506** _J. Phys. Chem. B, Vol. 114, No. 32, 2010_ 

Pa´rtay et al. 

**Figure 3.** Heat capacity as a function of temperature, for Lennard-Jones clusters containing less (top) and more (bottom) than 10 atoms. The inset of the top panel shows the average error of the heat capacity as a function of sample size (logarithmic scale), computed relative to the largest sample. The inset of the bottom panel shows the magnified low-temperature region of the heat capacity curves of larger clusters. 

**TABLE 1: Size of Sample Set and Number of Energy Evaluations Needed To Produce a Converged Nested Sampling Run (So That the Error in the Heat Capacity Curve Is on the Order of the Line Thickness of Figure 3)** 

|LJ|size of|no. of|LJ|size of|no. of|
|---|---|---|---|---|---|
|cluster|sample set,|energy|cluster|sample set,|energy|
|size|_K_|evaluations|size|_K_|evaluations|
|2-5|300|1.6×106|21-25|1100|3.9×108|
|6-10|500|2.0×107|31|288000|3.4×1012|
|11-15|700|1.1×108|36|32000|2.8×1011|
|16-20|900|2.2×108|38|224000|2.6×1012|



free energy becomes larger than that of the ideal gas at the same density can be determined. In Figure 5 each colored area represents a region inside which the corresponding cluster is stable; i.e., _A_ LJ _N_ < _A_ LJ _N_ -1 + _A_ LJ1. Larger clusters are more stable; thus, the regions form a nested sequence of bands that correspond to areas where a given cluster is stable but smaller clusters are not. Particularly favorable clusters show up in this diagram. The band corresponding to LJ13 is wider than its neighboring bands, mostly obscuring the region corresponding to LJ14. LJ19 is so much more favorable than LJ20 that there is 

no region where the latter is stable and the former is not. Note that this is a phase diagram for clusters only; it does not include - cluster cluster interactions and so does not extend to high densities where solid phases are formed. 

## **Energy Landscape Charts** 

Visualization of the energy landscape can greatly enhance the understanding of a chemical system, but the representation of a 3 _N_ -dimensional function is a challenging task. One way to get around this problem is to reduce the dimensionality by projecting the energy landscape onto ad-hoc collective coordinates, but this does not provide a sufficient description in general, and it can be very misleading in some cases, depending on the choice of collective coordinates. A more adequate and usual way of depicting the topology of basins and transition states is the disconnectivity graph,[44,45] or the scaled disconnectivity graph,[46] where in the latter case the width of the graph is made proportional to the number of minima. While the complete disconnectivity graph would capture the entire landscape, it is impractical to calculate or draw for even moderate size systems, 

_J. Phys. Chem. B, Vol. 114, No. 32, 2010_ **10507** 

Exploration of Atomic Configurational Spaces 

**Figure 4.** Heat capacity as a function of temperature for Lennard-Jones clusters LJ17 and LJ25, using nested sampling (red lines) and parallel tempering (black lines with black dots indicating the temperature values where the simulations were performed in parallel tempering). The standard errors of the prediction are shown by dashed lines (nested sampling) and error bars (parallel tempering). The number of energy evaluations needed to calculate the curves are also indicated. 

estimate of the local minimum. The output of the algorithm is a hierarchical nested tree of basins, with known phase space volumes. 

**Figure 5.** Phase diagram of Lennard-Jones clusters as a function of temperature and density. Each colored band represents a region in which the corresponding cluster is thermodynamically stable against evaporation, while the smaller clusters are not. The black arrow indicates the density at which the nested sampling calculations were carried out. 

and more importantly, it does not contain the entropy information which controls the thermodynamic behavior. Nested sampling naturally provides a solution to this. 

In this section we introduce and illustrate an algorithm that identifies the large-scale basins of the energy landscape automatically by postprocessing the sample set produced by nested sampling. The key point is that we get a broad-brush view of the landscape, using relatively few samples (clearly not enough to discover all local minima), but nevertheless giving a helpful overview of the system. To carry out the topological analysis of the samples, we construct a graph in which the vertices are the sample points and connect them by edges based on the Cartesian distance between the sample points: each vertex is connected to its _k_ nearest neighbors which have a higher energy than itself. Then we successively remove vertices and their associated edges from the graph in a decreasing order in energy. When the removal of a vertex results in the graph splitting into two or more disconnected subgraphs, the vertices in the subgraphs are identified with new basins. The relative phase space volumes of the basins is estimated from the ratio of the number of samples belonging to each at the moment of splitting. The subgraphs are analyzed recursively using the same procedure. If a subgraph is eliminated without splitting further, it represents a basin associated with a local minimum, and we identify the sample with the lowest energy in this basin as our 

To demonstrate this procedure, we show how it works on a simple toy model, a two-dimensional potential energy surface given by the sum of three Gaussians, shown in the top left panel of Figure 6. This surface has two local minima in addition to the global minimum. We performed a nested sampling run on this surface using _K_ ) 100 samples and 1900 iterations, in this case choosing the new sample points randomly from the entire [0,10;0,10] range (thus satisfying eq 11 exactly). The final set of sample points are shown by green crosses in Figure 6, and to construct the graph, we have chosen _k_ ) 6. To help visualize the saddle point identification process, in the bottom panel of Figure 6 we show the state of the graph just before it splits into two subgraphs corresponding to the two larger basins. 

We draw an energy landscape chart, shown in the bottom left panel of Figure 6, in which the width of the landscape at a given energy level is proportional to the phase space volume enclosed by the subset of samples below that energy, as given by the nested sampling weights, _wn_ . Separate basins are drawn according to our graph analysis. Note that the ordering of the basins on the horizontal axis is arbitrarily chosen at each transition state, but their topological relationships are preserved. The gray shading in Figure 6 represents one standard deviation error in the overall phase space volume. The error in the relative phase space volumes of split basins is estimated as the standard deviation of the multinomial distribution with generator probabilities equal to the relative basin sizes. 

To construct the energy landscape charts for LJ clusters, a distance metric between the configurations has to be constructed that takes account of the exact symmetries of the Hamiltonian. The metric that we use has been described elsewhere;[47] it is calculated in an auxiliary space in which configurations related by an exact symmetry (translations, rotations, and particle permutations) are first mapped onto the same point by a continuous mapping. The resulting energy landscape charts are shown in Figure 7 for LJ7, LJ8, and LJ13 and in Figure 8 for LJ31 and LJ36. Note that in this case and in general for highdimensional systems, in contrast to the toy model, the horizontal scale on which the phase space volume is represented has to be an exponential function of the energy in order to fit the diagram comfortably on the page. It is particularly notable for LJ7 that the two local minima with the highest energies correspond to configurations in which one atom is in the gas phase and the 

**10508** _J. Phys. Chem. B, Vol. 114, No. 32, 2010_ 

Pa´rtay et al. 

**Figure 6.** Real energy landscape (top left panel) and the chart produced by nested sampling (bottom left panel) for the toy model, together with the corresponding disconnectivity graph. The global minimum is marked by A, while the two local minima are marked by B and C. The vertical scale is the energy; the horizontal dimension on the landscape chart represents the phase space volume enclosed by the set of samples at a given energy, separated out into different basins. This is achieved using a geometric analysis of the sample set, as described in the text. The gray shading represents the error in the overall phase space volumes, while the red lines indicate the error in the relative volumes of the three basins. The percentages refer to the relative size of the error as compared to the volume of the smaller of the basins at the energy level where the basins separate. The sample configurations and the graph constructed from them are shown on the right panels. The real minima and transition states are shown by red dots and stars, respectively, as well as the corresponding estimates from postprocessing the nested sampling data (see text). Top right, full graph; bottom right, in the process of elimination of vertices in order of decreasing energy, the step in which the graph is about to split into two identifies the sample point close to the saddle point. 

others form LJ6. Such a configuration is a valid one for seven atoms in a box, and naturally appear in a nested sampling run, because it samples the _entirety_ of phase space. Because one atom is in the gas phase, the phase space volume associated with these local minima depends on the box size (in contrast to the phase space volume of the local minima of the complete cluster). For much larger boxes, the entropy of the gas atom would dominate, as expected: matter sublimates at all temperatures in an infinite perfect vacuum. Other such configurations are not shown because they occur at higher energies. 

The energy landscape chart of LJ13 has a highly symmetrical global minimum. The landscape has previously been mapped extensively and has at least 1478 local minima.[48] Our sample set was clearly too small to discover all of them, but this is not the aim here. The figure shows an overall view of the PES, with its deep and wide global minimum and no significant local minima at this resolution. In contrast, for smaller clusters, such as LJ7 or LJ8, narrow metastable states are already visible. The advantage of using nested sampling is that we _do not_ have to discover all local minima to be able to make qualitative statements about the large-scale features of the PES. Further- 

more, the above difference between LJ13 and LJ7 or LJ8 cannot be gleaned from their respective disconnectivity graphs, even if they were mapped exactly. For larger or more complex systems, which have immense numbers of local minima, the nested sampling approach will likely remain useful. 

The smallest cluster for which a low-temperature peak is present in the heat capacity is LJ31, where the energy landscape chart shows that immediately above the peak (which is at _T_ ≈ 0.02) a handful of very similar states, distinct from the global minimum, dominate. At much higher temperature, _T_ ) 0.1, at the separation point of the basin containing the global minimum, the system transitions between many distinct configurations, which is confirmed by MD simulations. 

The case of the LJ36 cluster seems somewhat different in that near the energy value that corresponds to the temperature of the heat capacity peak, already above the separation point of the basin of the global minimum, a pronounced widening of the energy landscape can be observed, indicating that the number of available configurations is very large. This behavior has been well-documented previously but for much larger clusters.[49] The picture is confirmed by a short (10 ns) molecular 

_J. Phys. Chem. B, Vol. 114, No. 32, 2010_ **10509** 

Exploration of Atomic Configurational Spaces 

**Figure 7.** Energy landscape charts of clusters of 7 (top left), 8 (top right), and 13 (bottom) Lennard-Jones atoms (see Figure 6 for a detailed description of energy landscape charts). Here, basins where the error exceeds the basin size are colored red. 

dynamics run at _T_ ) 0.155, in which we observed the system making transitions between many states with none of them dominating. 

## **Free Energy and a Discrete Order Parameter** 

A large part of solid-state physics, chemistry, and materials science is concerned with determining phase diagrams. The existence of thermodynamic phase transitions can be discovered using the appropriate response functions, e.g., as illustrated above. However, the actual microscopic identification of the different phases is much more subjective, since it requires an externally defined _order parameter_ , typically a collective function of atomic coordinates. 

The degree of arbitrariness in the choice of order parameter becomes a major problem when dealing with phases that correspond to different atomic structures, e.g., the various local 

minima of clusters. Corresponding free energies can only be calculated once the order parameter is defined, but, in order to do that, one has to know _in ad_ V _ance_ what structures are to be distinguishedsbut, in an ideal world, that information should be the _result_ of the free energy calculation: the various phases correspond to the local minima of the _free energy landscape_ . Fluctuations at finite temperature make some ad-hoc order parameters unusable, and degeneracies between equivalent structures related by a permutation of atomic labels further complicate the task of defining collective variables suitable to be used as order parameters. 

Energy landscape charts suggest a different approach. Having explored the energy landscape at a given resolution, we obtain a hierarchical tree of basins. The order parameter that might correspond best to the natural philosopher’s question, “Which state is the system in?”, is simply the identity of an energy 

**10510** _J. Phys. Chem. B, Vol. 114, No. 32, 2010_ 

Pa´rtay et al. 

**Figure 8.** Energy landscape charts LJ31 (left) and LJ36 (right) clusters (see Figure 6 for a detailed description of energy landscape charts). The insets show the heat capacity in the range of the first peaks. The expectation value of the energy (see eq 15) corresponding to the specific temperatures marked are also shown on the energy landscape chart by blue lines. The boxed ratio for LJ31 represents the phase space volume ratio of the basin containing the global minimum at its separation energy. 

landscape basin or suprabasin (the latter can be formally defined as a collection of basins each reachable from the others without having to traverse a configuration with higher energy than the highest escape barrier from the collection). Accordingly, we label each basin and suprabasin and use this label as a _discrete order parameter_ . Since every sample point can then be assigned to a basin or suprabasin and therefore to a particular value of this order parameter, computing free energies by using partial partition functions (summing over just the samples in a given basin) is straightforward. 

We use this approach to determine the free energy difference between the icosahedral metastable minimum and the global minimum of the famous LJ38 cluster.[50] Previous estimates of the relative sizes of the corresponding suprabasins range from 20:1[46] (based on the number of local minima found in each suprabasin below the lowest transition point) to 10000:1[51] (based on the relative frequency of finding the two minima using random search). 

We carried out the nested sampling calculation for this analysis using _K_ ) 64000 for LJ38. The resulting energy landscape chart is shown in Figure 9. It shows three distinct large basins corresponding to the global minimum and two icosahedral minima, which we label “Global”, “L1”, and “L2” (we have ignored two apparent basins that are very small and not stable as the parameters of the graph analysis algorithm are varied). As the energy increases from the global minimum, first the global minimum and L1 merge (these states are labeled “B”); then this suprabasin merges with L2 (these states are labeled “A”). We plot the relative free energies of the various regions on the top panel, showing that the L1 state becomes stable at about _T_ ≈ 0.1 and the A state becomes stable at _T_ ≈ 0.16. These transitions show very good agreement with the positions of the peaks in the heat capacity curve (also shown). The match is not exact because the basin identification is based on energy, 

whereas the natural variable of the heat capacity is temperature. The energy landscape chart has therefore automatically identified the identity of the various distinct thermodynamically stable states without external input such as an order parameter. 

The relative sizes of the various basins at their separation energies are also indicated. In particular, the phase space volume ratio of the lowest energy icosahedral minimum to that of the global minimum is about 15:1. It is interesting to note that the separation energy of these basins (basically the energy at which the structures become identifiable as distinct) is much higher than the highest point on the minimum energy path.[52] The latter is indicated in Figure 9 by a wavy line, and the phase space volume ratio at that energy is 1:16; i.e., the basin of the global minimum is much larger there. 

## **Conclusion** 

We described a new framework for efficiently sampling complex energy landscapes, based on nested sampling. This “top-down” approach is inherently unbiased, and its resolution can be adjusted to suit the available computational resources. Although it can be used as a tool to search for minima, we expect that its main strength will be that it can provide an approximate picture of the large-scale features of the landscape using only modest resources. Beyond this qualitative description, the sample points can be used to evaluate the partition function with good accuracy at arbitrary temperatures, and hence also the expectation values of thermodynamic observables, such as response functions. 

Furthermore, the topological analysis of the samples can be used to discover large-scale basins and identify them with the macroscopic states of the system. We defined an order parameter which indexes the basins. The knowledge of the phase space volumes associated with each such basin allows the direct 

_J. Phys. Chem. B, Vol. 114, No. 32, 2010_ **10511** 

Exploration of Atomic Configurational Spaces 

knowledge of the location of the global minima. Because the efficiency gain comes from the natural handling of first-order phase transitions, we expect even better results in bulk systems, whose study is already underway. 

1— 

**Acknowledgment.** We are indebted to John Skilling, Daan Frenkel, and David Wales for carefully reading the manuscript and to Ben Hourahine, Noam Bernstein, Mike Hobson, Farhan Feroz, and Mike Payne for extensive discussions. The work has been partly performed under the Project HPC-EUROPA (Grant 4 RII3-CT-2003-506079), with the support of the European CommunitysResearch Infrastructure Action under the FP6 “Structuring the European Research Area” Programme. L.B.P. acknowledges support from the Eo¨tvo¨s Fellowship of the Hungarian State and the hospitality of the Engineering Laboratory in Cambridge. G.C. acknowledges support from the EPSRC under Grant No. EP/C52392X/1. 

1 

## **References and Notes** 

- (1) Skilling, J. Bayesian inference and maximum entropy methods in 

- science and engineering. _AIP Conf. Proc._ **2004** , 395. 

- (2) Skilling, J. _J. Bayesian Anal._ **2006** , _1_ , 833. 

- (3) Wales, D. _Energy Landscapes_ ; Cambridge University Press: 

- Cambridge, U.K., 2003. 

- (4) Hoare, M. R. _Ad_ V _an. Chem. Phys._ **1979** , _40_ , 49. 

- (5) Pandey, K. C. _Phys. Re_ V _. Lett._ **1986** , _57_ , 2287. 

- (6) Feibelman, P. J. _Phys. Re_ V _. Lett._ **1990** , _64_ , 729. 

- (7) Serra, S.; Cavazzoni, C.; Chiarotti, G.; Scandolo, S.; Tosatti, E. 

- _Science_ **1999** , _284_ , 788. 

- (8) Middleton, T. F.; Hernandez-Rojas, J.; Mortenson, P. N.; Wales, 

- D. J. _Phys. Re_ V _. B_ **2001** , _64_ , 184201. 

- (9) Goedecker, S.; Deutsch, T.; Billard, L. _Phys. Re_ V _. Lett._ **2002** , _88_ , 

- 235501. 

- (10) Pickard, C. J.; Needs, R. J. _Phys. Re_ V _. Lett._ **2006** , _97_ , 045504. 

- (11) Pickard, C. J.; Needs, R. J. _Nat. Mater._ **2008** , _7_ , 775. 

- (12) Liu, P.; Voth, G. A. _J. Chem. Phys._ **2007** , _126_ , 045106. 

- (13) Wales, D. J.; Bogdan, T. V. _J. Phys. Chem. B_ **2006** , _110_ , 20765. 

- (14) Wales, D. J.; Doye, J. P. K. _J. Phys. Chem. A_ **1997** , _101_ , 5111. 

- (15) Rata, I.; Shvartsburg, A. A.; Horoi, M.; Frauenheim, T.; Siu, K. W.; 

- Jackson, K. A. _Phys. Re_ V _. Lett._ **2000** , _85_ , 546. 

- (16) Abraham, N. L.; Probert, M. I. J. _Phys. Re_ V _. B_ **2006** , _73_ , 224104. 

- (17) Goedecker, S. _J. Chem. Phys._ **2004** , _120_ , 9911. 

- (18) Montalenti, F.; Voter, A. F. _J. Chem. Phys._ **2002** , _116_ , 4819. 

- (19) Swendsen, R. H.; Wang, J. S. _Phys. Re_ V _. Lett._ **1986** , _57_ , 2607. 

- (20) Frantz, D. D.; Freemann, D. L.; Doll, J. D. _J. Chem. Phys._ **1990** , 

- _93_ , 2769. 

**Figure 9.** Free energy of basins (top) and energy landscape chart (bottom) of LJ38. The colored regions identify the major basins: global fcc minimum (green), icosahedral local minimum (L1, red), alternative icosahedral structure (L2, gray). The dashed lines indicate the depth of the basins as obtained with direct minimization starting from the lowest local sample of nested sampling. The wavy line between L1 and the global minimum on the energy landscape chart indicates the approximate energy of the minimum energy path connecting to the minima.[52] The relative phase space volumes of the basins at the separation point are shown by the boxed ratios. The light blue region represents states in which the fcc and lowest energy icosahedral states cannot be distinguished; the dark blue region includes states in which L2 states also become indistinguishable. The top panel shows the free energy associated with each colored region, with respect to the free energy of the global minimum. For reference, the heat capacity curve is also plotted again. 

- (21) Wang, F.; Landau, D. P. _Phys. Re_ V _. Lett._ **2001** , _86_ , 2050. 

- (22) Micheletti, C.; Laio, A.; Parrinello, M. _Phys. Re_ V _. Lett._ **2004** , _92_ , 

- 170601. 

- (23) Feroz, F.; Hobson, M. P. _Mon. Not. R. Astron. Soc._ **2008** , _384_ , 

- 449–463. 

- (24) Marinari, E. Optimized Monte Carlo methods; In _Ad_ V _ances in_ 

- _Computer Simulation: Lectures Held at the Eöt_ V _s Summer School_ ; Kertész, J., Kondor, I., Eds.; Springer: Berlin, 1998. 

- (25) Mandelshtam, V. A.; Frantz, P. A.; Calvo, F. _J. Phys. Chem. A_ 

- **2006** , _110_ , 5326. 

(26) Hukushima, K.; Nemoto, K. _J. Phys. Soc. Jpn._ **1996** , _65_ , 1604. 

(27) Newton, M. A.; Raftery, A. _J. R. Stat. Soc. B_ **1994** , _56_ , 3. 

- (28) Raftery, A. E.; Newton, M. A.; Satagopan, J. M.; Krivitsky, P. N. 

- _Estimating the Integrated Likelihood_ V _ia Posterior Simulation Using the Harmonic Mean Identity_ . Oxford University Press: Oxford, U.K., 2007. 

- (29) von Neumann, J. _Nat. Bur. Stand._ **1951** , _12_ , 36–38. 

- (30) MacKay, D. J. C. _Information Theory, Inference, and Learning_ 

- _Algorithms_ ; Cambridge University Press: Cambridge, U.K., 2003. 

- (31) Skilling, J. Nested Sampling’s Convergence. _AIP Conf. Proc._ **2009** , 

- 277. 

evaluation of the free energy corresponding to each value of this order parameter, and hence give information on the relative stability of the macroscopic states, without need for a priori of these states. 

We demonstrated nested sampling in the well-studied system of Lennard-Jones clusters, where the efficiency of evaluating the heat capacity was more than an order of magnitude better than that of parallel tempering, without using any prior 

- (32) Evans, M. J. Discussion of Nested Sampling for Bayesian Com- 

- putations by John Skilling. _Proceedings of the Eighth Valencia International Meeting_ , 2006. 

(33) Ganzenmu¨ller, G.; Camp, P. J. _J. Chem. Phys._ **2007** , _127_ , 154504. 

- (34) Bogdan, T. V.; Wales, D. J.; Calvo, F. _J. Chem. Phys._ **2006** , _124_ , 

- 044102. 

(35) Yan, Q.; de Pablo, J. J. _Phys. Re_ V _. Lett._ **2003** , _90_ , 035701. 

- (36) Morozov, A. N.; Lin, S. H. _Phys. Re_ V _. E_ **2007** , _76_ , 026701. 

- (37) Doye, J. P. K.; Wales, D. J.; Miller, M. A. _J. Chem. Phys._ **1998** , 

- _109_ , 8143. 

**10512** _J. Phys. Chem. B, Vol. 114, No. 32, 2010_ 

Pa´rtay et al. 

- (38) Frantsuzov, P. A.; Mandelshtam, V. A. _Phys. Re_ V _. E_ **2005** , _72_ , 

- 037102. 

- (39) Mackay, A. L. _Acta Crystallogr._ **1962** , _15_ , 916. 

- (40) Northby, J. A. _J. Chem. Phys._ **1987** , _87_ , 6166. 

- (41) Ferrenberg, A. M.; Swendsen, R. H. _Phys. Re_ V _. Lett._ **1989** , _63_ , 

- 1195. 

- (42) Sharapov, V. A.; Mandelshtam, V. A. _J. Phys. Chem. A_ **2007** , _111_ , 

- 10284. 

- (43) Doye, J. P. K.; Miller, M. A.; Wales, D. J. _J. Chem. Phys._ **1999** , 

- _111_ , 8417. 

- (44) Becker, O. M.; Karplus, M. _J. Chem. Phys._ **1997** , _106_ , 1495. 

- (45) Wales, D. J.; Miller, M. A.; Walsh, T. R. _Nature_ **1998** , _394_ , 758. 

- (46) Wales, D. J.; Bogdan, T. V. _J. Phys. Chem. B_ **2006** , _110_ , 20765. (47) Barto´k, A. P.; Payne, M. C.; Kondor, R.; Csa´nyi, G. _Phys. Re_ V _._ 

- _Lett._ **2010** , _104_ , 136403. 

- (48) Ball, K.; Berry, R. _J. Chem. Phys._ **1999** , _111_ , 2060. 

- (49) Noya, E. G.; Doye, J. P. K. _J. Chem. Phys._ **2006** , _124_ , 104503. 

- (50) Pillardy, J.; Piela, L. _J. Phys. Chem._ **1995** , _99_ , 11805. 

- (51) Pickard, C. Private communication. 

- (52) Doye, J. P. K.; Miller, M. A.; Wales, D. J. _J. Chem. Phys._ **1999** , 

- _110_ , 6896. 

JP1012973 

