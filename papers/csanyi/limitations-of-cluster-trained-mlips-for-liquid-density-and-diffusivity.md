> This article is licensed under ~~____~~ CC-BY 4.0 ©@® 

pubs.acs.org/JCTC 

Article 

## **Limitations of Cluster-Trained MLIPs for Liquid Density and Diffusivity** 

Viktor Svahn, Ioan-Bogdan Magdau, Samuel P. Niblett, Gábor Csányi, Kersti Hermansson, and Jolla Kullgren* 

**Cite This:** _J. Chem. Theory Comput._ 2026, 22, 3660−3671 **Read Online** 

ACCESS Metrics & More Article Recommendations * **sı** Supporting Information 

ABSTRACT: Machine-learned interatomic potentials (MLIPs) de based on quantum-mechanical data are often used as a means to fg ‘ combine the performance of classical force-fields with the accuracy % 33 of electronic structure methods. In this work, MLIPs based on the BS < i MACE architecture were trained, starting from two publicly el Di D 3 available data sets: one based on periodic structures, and the other based on molecular cluster data. Two rather challenging liquid properties are in focus, density and diffusivity, here for the batteryCe goer gee wl relevant ethylene carbonate and ethyl methyl carbonate solvents and mixtures thereof. The focus of our study is the uncertainties in the generated MLIP models themselves (calculated for committees of models with different regression seeds and different training set sizes) and how these uncertainties reflect on the MD-simulated target properties. The second focus point is whether these uncertainties are small enough to allow the comparison and assessment of different density functional theory (DFT) functionals; here, only a small number of them are compared, but the workflow opens up for a more extensive assessment of many DFT functionals. We find that all our MACE-MLIPs, both cluster-trained ones and the periodic-structure-trained ones, produce stable 1 ns NPT trajectories, regardless of training set size and cluster composition, but the MACE-MLIPs trained on cluster data (labeled with the hybrid _ω_ B97X-D3 functional) are found to be sensitive to both the random training seed and the data selection, resulting in large uncertainties on the simulated diffusivity and density values. 

## **1. INTRODUCTION** 

Density and diffusivity are two key properties of molecular liquids. They are related via the strengths of intermolecular interactions and can both be calculated from MD simulations, where the system density generally considerably easier to converge than diffusivity. The latter typically requires longtime simulations in large simulation boxes, and, during many decades, the use of classical force fields has proven indispensable in achieving this task. Even so, the accuracy of inter- and intramolecular interactions obtained from classical force fields is in principle, and most often in practice as well limited compared to that of quantum-mechanical electronic structure methods such as density functional theory (DFT).[1][−][3] Currently, the development of DFT-based machine-learned force fields has opened up the possibility to predict properties with DFT accuracy using MD simulations. Here, as a proof of concept, we will make use of such a strategy to compare three DFT functionals in terms of their abilities to describe the density and diffusivity of battery-relevant ethylene carbonate (EC) and ethyl methyl carbonate (EMC) solvent systems. All these things considered, the path toward achieving stable machine-learned force fields, or interatomic potentials (Machine-learned interatomic potentials (MLIPs)), with DFT 

quality is unfortunately not always a straight one. MLIPs can be generated (fitted) offline, followed by running MD simulations or, alternatively, by fitting energies and forces on-the-fly, where the MLIP is gradually improved as the dynamics progresses and the model accumulates more data. Both these strategies have been used in the literature to enable molecular simulations of extended length and time scales at an accuracy that approaches the DFT world.[4][−][7] Multiple rounds of active learning is typically required before an MLIP becomes stable enough to be used for MD production (see, for example, the work by Magdau et al.[8] ). Generating the necessary training sets for MLIPs can therefore be both time-consuming and highly resource intensive. A way around this challenge is to either rely on publicly accessible databases[9][,][10] or reuse published training sets that have been demonstrated to produce reliable MLIPs. Moreover, there are many different 

Received: December 8, 2025 Revised: March 10, 2026 Accepted: March 11, 2026 Published: March 31, 2026 

© 2026 The Authors. Published by American Chemical Society **3660** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**Journal of Chemical Theory and Computation** 

**pubs.acs.org/JCTC** 

Article 

flavors of MLIPs to choose from[4][−][7][,][11][,][12] including the equivariant message passing graph neural network, MACE.[12] Niblett et al. successfully trained MACE models on a data set[8] that had been generated from active learning using a different MLIP architecture and showed that MACE-MLIPs demonstrate impressive stability across a committee of trained MLIPs without the need for data augmentation.[13] 

Another challenge is the selection of an appropriate electronic structure method for the system and purpose at hand. The intermolecular interactions in EC:EMC systems are − dominated by electrostatic dipole dipole interactions (permanent dipoles and weaker induced ones) as well as dispersion interactions. Thus, in addition to the exchange−correlation treatment in DFT calculations, the dispersion interaction treatment needs attention. DFT functionals are sometimes classified according to Perdew’s “Jacob’s ladder of DFT functionals.”[14] In this hierarchical picture, climbing Jacob’s ladder can be viewed as a systematic path toward higher accuracy, albeit at the price of increased computational effort. A large number of benchmark studies in the literature assess the capabilities of DFT functionals, sometimes even hundreds of them.[15] 

In the first part of this study, we assess the impact of the DFT functional on the MLIP models and, more specifically, on the MD-generated diffusion and density values of our target systems. A modest set of periodic training structures (960 of them, prepared in our previous work[8] ) are used. These structures are here labeled using three DFT functionals, PBED2, PBE-D3, and B97-D3, selected because Perdew, Burke, and Ernzerhof (PBE) and B97 are much used in the literature and because they exhibit some interesting similarities and differences. A key question in this study is whether these MACE-based MLIP models, trained on periodic data, manage to yield liquid densities and diffusivities of sufficient precision to discriminate between the selected DFT methods. Our answer will be “yes, they manage,” which we will subsequently contrast with results from models trained on DFT cluster data, using the same regression and MD simulation strategies. 

The second part of this work thus deals with MLIPs trained on cluster data. With the emerging methodologies for finetuning foundation models,[16][−][18] a wider use of MLIPs based on advanced electronic structure methods such as hybrid-DFT methods or, say, coupled-cluster methods, may soon become reality. Here, cluster-based MLIPs may appear as a natural choice. There are already successful examples of such a strategy, see, for example, the study of fine-tuned MLIPs for Ice Ih by Gawkowski et al.[19] 

Foundation MLIP models can demonstrate stable dynamics off-the-shelf,[19][−][21] but they still require additional fine-tuning to converge thermodynamic and kinetic properties. This is highlighted by the recent work of Beiersdorfer et al.[22] who compared a Gaussian Approximation Potential (GAP) and MACE to the MACE-MP-0[20] foundation model, fine-tuned to a liquid similar to the ones studied here, but with ions included. They found that MACE-MLIPs trained directly on their data set outperformed both GAP and MACE-MP-0. Our own GAP versus MACE comparison using the periodic data set show a similar behavior (see Figure S3 in the SI). 

In two recent studies, cluster-based data were used to create MLIPs for EC, EMC, and other solvents in combination with ions.[23][,][24] Also, in our current study, we have generated MLIPs based on higher-level (hybrid) cluster-based DFT data, here with the approach to use exactly the same MACE regression 

scheme and settings as those for the periodic training data in the first part of this study. Also, in this part of the paper, the purpose is to examine whether the resulting MLIPs (now cluster-based) will yield diffusivity and density values of a similar precision as those resulting from the periodic-databased MLIPs; this would then allow us to assess such higherlevel DFT functionals and wave function-based methods on the same footing as the three functionals. 

In the context of condensed-matter simulations, the use of cluster training data entails certain new challenges compared to periodic training data, in particular regarding the risk of not using (a sufficient number of) bulk-representative structures in the data set. Problems with cluster-to-liquid extrapolation and out-of-domain transfer may potentially result. 

In going from cluster-based MLIPs to bulk applications, the out-of-domain effect has at least two conceptually different origins. First, atoms that reside in the outer parts of a cluster do not provide examples of atomic environments that are representative of the liquid phase. Only atoms that are “rather well embedded” in a cluster provide such examples. Second, the use of finite clusters is an effective truncation and omission of long-range effects within the training data itself, both direct long-range effects and nonadditive cooperative effects such as polarization; in short, the training set will contain skewed forces and energies compared to typical bulk-like environments. The potential problem with clusters therefore becomes 2-fold: (i) Are there enough representations of atomic environments with local packing similar to a liquid? (ii) Will the exclusion of long-range effects lead to systematic errors in the generated MLIPs (subsequently in the simulated system properties)? 

In the first case, poor representation of liquid-like local environments might force models to extrapolate when used in simulating liquid systems, and in the second case, the trainingset forces and energies may be nonrepresentative, as they originate from skewed electron density distributions. Reference 25 provides indications that the training of neural networks on out-of-domain data may lead to considerable extrapolation errors that are sensitive to the random seed used during model initialization which motivated Gong et al.[24] to consider possible variations due to random seeds. In particular, they observed committee errors of the same order as in the work by Niblett et al. (0.03 g cm[−][3] for the densities of EC and EMC). While Gong et al. initially started their training from the data set generated by Dajnowicz et al.,[23] they required a few rounds of active learning until stable MLIPs were obtained. 

We examine whether the stability and reproducibility that characterize our MACE-MLIPs generated from periodic training data also hold for cluster-based training data. 

Concerning stability, the answer is yes: all our MLIPs turn out to be capable of sustaining 1 ns long trajectories even when trained on modest amounts of the original data from ref 23. However, we simultaneously find a low agreement across a committee of predictions for the cluster-based MLIPs (much lower compared to that of refs 13 and 24), which then also affects the capability of the MD simulations to discriminate between results from different DFT methods. Overall, the predictions from our cluster-based MLIPs are found to be highly sensitive to data selections, highlighting the problems of out-of-domain training. 

The layout of the paper is as follows. The Method section presents, in order, the data sets used for MLIP training, the DFT functionals and DFT calculations, the MLIP generation 

**3661** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

~~a~~ **Journal of Chemical Theory and Computation pubs.acs.org/JCTC** Article 

and adhering regression quality, and, finally, the MD simulation details and the MD property analyses. In the Results and Discussion section, we discuss our workflow for the systematic comparison of the MLIP-driven MD simulation results, especially with respect to system densities and molecular diffusion coefficients, and with special focus on the (possible) differences observed depending on the choice of DFT functional for the training-set data. The first part (Section 3.1) presents the MD results from MLIPs constructed from periodic training data, while the second part (Section 3.2) presents results from MLIPs based on training data consisting of molecular clusters. In Section 3.2, in addition to the DFT functionals, also data set size, data set sample, and variations in model prediction due to the training seed become important items of comparison and attention. 

## **2. METHODS** 

## **2.1. Data Sets for MLIP Generation** 

The structures for the generation of our MLIPs were taken from two sources: periodic structures from the work of Magdau et al.[8] and cluster structures from the work of Dajnowicz et al.[23] The respective publications describe in detail how their training sets were developed, involving many rounds of active learning with systematic potential energy scans, as well as MD simulation snapshots. In the current study, we make use of these training structures as the basis for our MLIPs. The data sets are described in Table 1 together with information regarding the number of structures and atoms present in them. 

Table 1. Summary of Data sets Used in this Work. The Table Lists Data set Names, Data set Sizes in Terms of Number of Structures and Atoms, and Provides a Short Description of the Contents of Each Dataset 

||number<br>of|number of||
|---|---|---|---|
|data set|structures|atoms|structure types|
|Periodic|935|66,188|MD snapshots, monomers, and|
|Clusters-<br>Small<br>Clusters-<br>Medium<br>Clusters-<br>Large|8016<br>42,824<br>221,824|327,089<br>1,269,916<br>4,805,916|volume scans<br>monomers and gas-phase<br>clusters (_N_mols ≤6)<br>monomers and gas-phase<br>clusters (_N_mols ≤6)<br>monomers and gas-phase<br>clusters (_N_mols ≤6)|
|Clusters-<br>Full_a_|362,382|7,781,985|monomers, gas-phase clusters<br>(_N_mols ≤6), ions and non-|
||||singlet electronic states|



> _a_ Not used by us for training models. 

Volume scans were included in the periodic data set that we use; the volume scans explicitly sample variations in density and the associated virial pressure response. Concerning cluster-based training sets, it is worth noting that the training set of Dajnowicz et al., which we make use of, actually contains clusters of varying “densities” in the sense that there is a large variation in the compactness of the clusters (see Figures 1 and S2 in the SI). In this way, the cluster data in fact indirectly contain information akin to that captured by volume scans. However, information about virial pressure is missing in the cluster data. 

Table 2. Summary of MLIPs Trained in This Work; the Names are Shown as **Dataset** - _n_ / **Functional** , Where _n_ Denotes the Numbering of the Dataset Subsample; the Subsamples have the Same Compositions (namely those depicted in Figure 2) but Differ in Terms of Specific Data Points (See Text); the Number of Training Seed-Replicas of Each Model Is Shown as Well 

|training set|number of seeds|
|---|---|
|Periodic/PBE-D3<br>Periodic/PBE-D2<br>Periodic/B97-D3<br>Clusters-Small-1/_ω_B97X-D3<br>Clusters-Small-2/_ω_B97X-D3|1<br>1<br>1<br>3<br>1|
|Clusters-Small-3/_ω_B97X-D3|1|
|Clusters-Medium-1/_ω_B97X-D3|3|
|Clusters-Medium-2/_ω_B97X-D3|1|
|Clusters-Medium-3/_ω_B97X-D3|1|
|Clusters-Large/_ω_B97X-D3|3|
|Clusters-Small-1/B97-D3|1|
|Clusters-Small-2/B97-D3|1|
|Clusters-Small-3/B97-D3|1|
|Clusters-Medium-1/B97-D3|1|
|Clusters-Medium-2/B97-D3|1|
|Clusters-Medium-3/B97-D3|1|
|total number of models|22|



We denote the data set of periodic structures Periodic and the full data set of the cluster structures Clusters-Full. The data sets contain geometries, virials (only the Periodic data), energies, and forces. We created a data set, denoted Clusters-Large, by selecting from the Clusters-Full data set all charge-neutral clusters with spin multiplicity 1, containing EC, PC, VC, DMC, EMC, or DEC molecules. We then created additional data sets from the Clusters-Large data set by selecting 25% (ClustersMedium), or 6.25% (Clusters-Small), of the structures from it in such a way that as many of the large clusters as possible were retained to minimize the oversampling of specific compositions, such as pure EC. Some statistics related to these data sets is listed in Table 

Figure 1. Different examples of clusters, ranging from dimers to hexamers (a−e), that are part of the Clusters-Large data set. These images illustrate the varied compactness of clusters in the data set. 

**3662** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**pubs.acs.org/JCTC** 

Article 

## **Journal of Chemical Theory and Computation** 

1. The DFT labelling of the structures is treated in the next section and details of the MLIP generation are described in the section after that. A list of all MLIPs trained in this work is given in Table 2. 

Three variants of the Clusters-Medium data set were created, sharing the same distribution of molecular composition but consisting of different specific data points (see Figure 2). Similarly, three data set variants of the Clusters-Small data set were created. 

## **2.2. DFT Functionals** 

For the periodic systems, the DFT calculations were performed using a plane-wave basis set in conjunction with Projector Augmented Wave[26] type pseudopotentials[26] as implemented in the Vienna Ab initio Simulation Package.[27][−][30] We used the PBE[31] and B97 functionals[32] with Grimme’s D3 corrections[33] and Becke−Johnson (BJ) damping.[34] The plane wave basis set was truncated using a kinetic energy cutoff of 800 eV. The Brillouin zone was sampled at the Γ-point only. We named these training sets Periodic/PBE-D3 and Periodic/B97-D3. The Periodic/PBE-D2 training set contains the same structures as the other periodic data sets but was labeled with energies and forces from CASTEP[35] calculations with the same energy cutoff and _k_ -point sampling as the other periodic training sets. The Periodic/PBE-D2 training set was taken as is from ref 

8. 

For the cluster MLIPs, the DFT labels in the original ClustersFull data set by Dajnowicz et al.[23] were computed by them with the Psi4 program,[36] which uses local atomic Gaussian basis sets; they used the _ω_ B97X-D3 functional[37] with a Grimme D3(BJ) dispersion correction and the def2-TZVP basis set[38] with diffuse augmentation[39] (def2-TZVPD). For clusters, no new DFT calculations were performed by us at the _ω_ B97X-D3 level, as our ClustersLarge/ _ω_ B97X-D3, Clusters-Medium/ _ω_ B97X-D3, and Clusters-Small/ _ω_ B97X-D3 data sets (cf. Table 1) are all subsets selected by us from the Clusters-Full data set. However, we performed a set of cluster DFT calculations at the B97-D3(BJ) level, also with Psi4 software and the def2-TZVPD basis set, for comparison with the _ω_ B97X-D3(BJ) results; those results are presented in Section 3.2. In the rest of this article, the “(BJ)” parenthesis is dropped from the D3 notation. 

## **2.3. MLIP Generation** 

The machine-learning interatomic potentials were trained by using the MACE framework. The training data were taken from the data sets in Table 1, with 5% of the configurations reserved for validation. The reference data also included the atomic energies (E0s), computed at the corresponding DFT level for each training set. 

The MACE architecture employed a message-passing equivariant neural network with two interaction layers, a correlation order of 3, angular momentum channels up to / = 3, and hidden irreducible representations of size 128 × 0e + 128 × 1o. The atomic environment in each message-passing layer with a smooth cutoff radius of 6.0 Å uses five basis functions. 

A weighted loss function with contributions from energies (weight 1.0) and forces (weight 100.0) was minimized during the training, using equal weights across configuration types. Optimization was carried out with the Adam method (of the AMSgrad flavor) using a batch size of 20, a weight decay of 5 × 10[−][7] , a learning rate of 0.01, and an exponential moving average (EMA decay 0.99). Models were initially set to train for 1600 epochs with early stopping (patience 50). In practice, models were considered finished when a plateau had been reached. The periodic models trained for around 750 epochs, whereas the number of epochs associated with the cluster data varied. Broadly, the small-cluster models used 1800 epochs, the medium models used 1200, and the large models used 400. Stochastic weight averaging was performed at the end of each fit to ensure low energy errors. Table S1 in the SI lists the training and validation RMSEs in energy per atom and forces for all MLIPs used in this study. 

Models were fitted to the Periodic data set labeled with PBED2, PBE-D3, and B97-D3 energies, forces, and virial stresses; the results are shown in Figure 3. Overall, force RMSEs of the trained 1 models compared to their labels were O (10 meV Å _ ) and the 

Figure 2. The first three panels show the distribution of compositions over the differently sized clusters for the three data set sizes. In these diagrams, green indicates structures that contain both EC and EMC and possibly something else (other), whereas yellow color indicates the presence of either EC or EMC and possibly something else (other). The term “other” refers to propylene carbonate (PC), vinylene carbonate (VC), fluoroethylene carbonate (FEC), dimethyl carbonate (DMC), and diethyl carbonate (DEC). The bottom panel includes all three data set sizes and compares their cluster size distributions and average cluster sizes (Note the log-scale on the y- axis in this plot). 

**3663** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**Journal of Chemical Theory and Computation** 

**pubs.acs.org/JCTC** Article 

Figure 3. Effects of the DFT functional on the regression quality. Regression metrics (scatter plots, root-mean-squared errors, absolute force errors) are shown for model forces trained on the Periodic data set labeled with PBE-D2, PBE-D3, and B97-D3. The model forces are compared with their respective DFT labels. The color bar indicates the point density in each bin. 

relative-RMSEs were less than one percent. The same figure also shows the error as a function of DFT reference force, revealing that the errors tend to be larger when the force is small. Most errors are very small (around 5 meV Å[−][1] ), but there is nevertheless a considerable number of data points where the error is substantial. To put this in perspective, in our simulations, an atom moves 0.025 Å per time step on average at temperatures around 300 K. Integration of the forces in Figure 3 over such a displacement yields a correlation that describes the training error of the forces in terms of an energy instead. Since this is a training error, this number gives a rough estimate of the lowest error per atom that may be associated with a single time step in an MD simulation and which can be viewed in relation to chemical accuracy (which is considered to be around 40 meV). In the present case, the resulting RMSEs (see Figure S1 in the SI) between integrated forces were less than 1 meV for all three models. 

## **2.4. MD Simulations and Property Calculations** 

Four liquids with different compositions were studied: pure EC, pure EMC, and EC:EMC mixtures in 7:3 and 3:7 molar ratios. The initial (isotropic) box dimensions for the respective compositions were 22.54 Å, 22.09 Å, 22.30 Å, and 22.38 Å. With the exception of the 7:3 mixture, which consisted of 1005 atoms, all of the other liquids contained 1000 atoms. 

The MD simulations were run in the _NPT_ ensemble for a duration of 1 ns each, using our trained MLIPs. The simulations were performed under a constant pressure of 1 atm, and the target temperature was 298 K except for the pure EC system which was simulated at a slightly higher temperature of 313 K due to EC’s low melting point. 

All MD simulations were performed using the MACE implementation (ver. 0.3.7) as a calculator in the Atomic Simulation Environment (ASE) package (ver. 3.22.1).[40] A time step of 1 fs was used, and the simulations were performed with the Nosé−Hoover thermostat and the Parrinello−Rahman barostat with relaxation times of 50 and 2500 fs, respectively. The bulk modulus value that is required to specify the barostat in the ASE implementation was set to 2.0 GPa. The trajectories were initiated from MD snapshots taken from ref 8. 

The diffusive regime is commonly said to have been reached once the logarithm of the time-dependent MSD curve has reached a unit slope with respect to log _t_ , and we define _tD_ to be the time at which the diffusive regime has been reached.[41] Since this regime is only transient between the ballistic and hydrodynamic regime, we calculated the log−log slopes over a moving window and selected the window with the best linear fit, with _tD_ being the starting time of said window. Here, we used a moving window of 2000 snapshots and allowed the slope to be 1.0. theory and computation. 

Molecular diffusion coefficients were determined from the meansquared displacements of the molecular center-of-mass by fitting the Einstein relation to the slopes of the MSD curves; they are reported with a 95% confidence level. The error bars in the graphs in Section 3.1 reflect this confidence. When diffusion coefficients are compared with the experiment, the former have been corrected for finite size effects using 

**==> picture [229 x 22] intentionally omitted <==**

where _DL_ is our value obtained from the MSD slope, _kB_ is Boltzmann’s constant, _T_ is the temperature, _η_ is the dynamic viscosity of the liquid, and _L_ is the average side length of the cubic simulation box. For more details regarding this expression, the reader is referred to refs 41 and 42. 

## **3. RESULTS AND DISCUSSION** 

## **3.1. Periodic Training Data: Impact of the DFT Functional on Densities and Diffusivities** 

The extrapolation capabilities of neural networks have been shown to vary, not only between specific implementations but also internally and with respect to the random seeds used in the training process.[25] In the work of Niblett et al.,[13] the effects of such seed variations on the simulated density and diffusivity of an EC:DMC liquid mixture were quantified for the very same MACE architecture that we have used in the present work. Compared to ref 13, in the present study, we deal with 

**3664** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**Journal of Chemical Theory and Computation** 

**pubs.acs.org/JCTC** Article 

Figure 4. Influence of DFT functional on the MD-generated liquid properties targeted in this study. Results from MD simulations with three different MLIPs are shown, all trained on the Periodic data set structures labeled with either PBE-D3, PBE-D2, or B97-D3 values (energies, forces, stresses). The colors denote the liquid compositions in the MD simulations (cf. the legend in the south-east frame). The first three columns display the time evolution of the system densities (top) and of the mean-squared-displacements (MSD) (bottom) on a log−log scale. The bar diagrams in the rightmost column display the corresponding average density (top frame) and the diffusion coefficients ( _DL_ ) (bottom frame) fitted from the MSD curves, starting from the respective vertical lines ( _tD_ ) in the MSD time evolution graphs. 

Figure 5. Comparison of MD-simulated densities and diffusion coefficients for pure bulk EC (red) and pure bulk EMC (blue). The MD simulations were performed with the MLIPs based on periodic or cluster training data as listed in the top row of the figure. The average values can be found in Tables 3 and 4. The widths of the boxes illustrate the uncertainties in the predicted properties of MLIPs associated with both data selection and random seeds. More precisely, for the periodic MLIPs, these correspond to committee errors obtained from ref 13, while in the case of our cluster MLIPs, they are given as the min/max values from the committees (jointly computed over all cluster data sets). For the cluster-based MLIPs, the large variations in the resulting densities and diffusion coefficients shown in the figure are coupled to the sensitivities of the MLIPs to the specific selection of data points present in the training sets, i.e. differences between the Clusters-Large, Clusters-Medium, Clusters-Small training sets,and between the subsample variants of the latter two; this becomes a crucial matter when cluster data needs to be extrapolated to represent bulk liquid scenarios. Altogether, the figure illustrates that our MLIPs fitted to periodic data can be used to compare functionals, while the cluster-based models produced in this study yield too large uncertainties to make such a comparison meaningful. Experimental values for both EC and EMC have been indicated with dashed lines. 

**3665** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**Journal of Chemical Theory and Computation** 

**pubs.acs.org/JCTC** 

Article 

Table 3. Summary of the Densities and Finite Size-Corrected Diffusion Coefficients of the Pure Solvents; Experimental Values Have Been Included as a Perspective; the Corrections Were Determined Using _**η**_ EC = 1.93 **×** 10[−][3] Pa s Taken from ref 43 and _**η**_ EMC = 6.5 **×** 10[−][4] Pa s Taken from ref 44; the Densities Are Reported with Mean and Standard Error across a Committee as Reported in ref 13, whereas the Diffusivity Is Reported with a 95% Confidence Level in the Linear Fit 

|solvent|training set|temperature /K|density/g cm−3|dif. coef. (_D_∞) /1 × 10−6 cm2 _s_−1|
|---|---|---|---|---|
|EC|Periodic/PBE-D3|313|1.23(0.02_a_)|8.53 ± 0.03|
||Periodic/PBE-D2|313|1.34(0.02_a_)|6.41 ± 0.01|
||Periodic/B97-D3|313|1.30(0.02_a_)|5.61 ± 0.01|
||expt._b_|313|1.312|8.0|
|EMC|Periodic/PBE-D3|298|0.97(0.02_a_)|20.49 ± 0.06|
||Periodic/PBE-D2|298|1.05(0.02_a_)|17.70 ± 0.06|
||Periodic/B97-D3|298|1.09(0.02_a_)|10.04 ± 0.02|
||expt._c_|298|1.006|18.3|



> _a_ The error represents the standard error of the mean prediction made using a five-membered committee of models evaluated at 500 K. This value was taken from ref 13. _[b]_ The density was computed from a specific gravity of 1.322 at 313 K[45] and the diffusivity comes from ref 43. _[c]_ The density value was taken from the Merck webpage and the diffusivity from personal communication with Prof. Clare P. Gray. 

four solution compositions, and the scientific focus is different, but the results from ref 13 are helpful to us. In their work, across a committee of five MACE MLIPs, all trained on the very same data set but initiated with different seeds, the density of a single EC/EMC mixture at 500 K was found to vary by ± 0.02 g cm[−][3] . Similarly, they found the error in the predicted diffusion coefficients across this committee to be around 1%. The motivation behind their use of elevated temperature was a desire to determine an upper bound to uncertainties in densities and diffusivities across the committee. Thus, as these modest committee errors with respect to the training seed were established for liquid EC:EMC in combination with MACE in ref 13, we have chosen to bypass such an assessment for our periodic-data-based MLIPs in the present study. In the following, we will therefore consider only a single model (one seed) trained for each periodic data set, i.e., for each DFT labeling of the Periodic data set. 

Three DFT functionals were examined: PBE-D2, PBE-D3 and B97-D3. For a given functional, a comparison of the results for the different liquid compositions (red, yellow, green, blue in Figure 4) shows that the diffusivity more or less follows the inverse of the density; see also the Periodic results in Figure 5. Overall, the density of the Periodic/PBE-D3 model is found to be lower than those for the other two DFT labels. The differences in the average densities across compositions between the Periodic/PBE-D2 and Periodic/B97-D3 models is around 0.01 g cm[−][3] , whereas the corresponding difference between Periodic/B97-D3 and Periodic/PBE-D3 is 0.1 g cm[−][3] . Compared to committee averages from ref 13, the latter difference is about five times larger, i.e., significant. 

Here, we used only three functionals, but there are, as mentioned, innumerable more DFT functionals to be tested in the search of adequately predictive functionals for studies of diffusion-dependent phenomena of organic liquids. Such systematic tests are beyond the scope of the current study, but our results demonstrate that access to the MACE machinery, and taking training seed variation into account, will make it feasible to perform comprehensive benchmark studies of a large number of DFT functionals, e.g., against experimental observations. 

We have shown that our MACE-fitted models trained on periodic data for the four EC:EMC systems are all stable. The resulting densities come out to be quite similar for the three 

functionals, while the diffusivities depend more strongly on the choice of DFT method, even for the seemingly similar functionals used here (see Figure 5 for an overview). Incidentally, compared with available experimental measurements for pure EC and EMC (Table 3), we note that the three selected DFT methods either reproduce available experimental densities or diffusion coefficients fairly well, but never both. Generating reference data at higher quantum-mechanical levels such as hybrid-DFT or post-HF wave function methods easily becomes prohibitively expensive for periodic systems. This raises an important question: can we train MACE MLIPs on molecular clusters for our EC:EMC systems and predict properties in the condensed phase? EC and EMC data are actually already available at the fourth rung (“meta-GGA and hybrid”) _ω_ B97X-D3 level through the work of Dajnowicz et al.[23] In the next section, we explore such possibilities using a strategy similar to the one we used here for the periodic systems but using a committee of models. 

## **3.2. Property Variability from MLIPs Fitted on Cluster Data** 

Here, a number of MLIP models were trained by us based on the extensive _ω_ B97X-D3 level cluster training set developed by Dajnowicz et al.[23] intended for organic electrolytes and consisting of organic solvent molecules such as EC, EMC, and a few others (see Figure 2). We essentially follow the procedure used for the periodic MLIPs in Section 3.1 with a couple of exceptions. First a committee of ClustersLarge MLIPs is trained with three different seeds and we monitor the variations in predicted properties resulting from those MLIPs. Then, in order to determine whether the skewness of the data toward EC (Figure 2) has a negative impact, we harmonize the data by partitioning it into smaller subsets and perform a similar analysis using committees of MLIP predictions. 

Figure 6 shows committee averages of densities and diffusion coefficients obtained from cluster-based MLIPs for the various EC:EMC compositions, and Table 4 lists the averages (for the pure liquids) and their associated uncertainties. The committee averages were computed jointly over both the various seeds and data composition for each size of the data sets. The variations in predicted properties with respect to either the seed or the data set samples for all compositions are presented in the SI. The MD-simulated liquid densities and diffusion coefficients from the Cluster- 

**3666** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**Journal of Chemical Theory and Computation** 

**pubs.acs.org/JCTC** 

Article 

**==> picture [220 x 356] intentionally omitted <==**

Figure 6. MD simulations results with the Clusters-Small/ _ω_ B97X-D3 and Clusters-Medium/ _ω_ B97X-D3 and Clusters-Large/ _ω_ B97X-D3 MLIPs. The error bars show committee averages calculated jointly over three MLIP seeds (for all three training set sizes) and over three data set samples for the Clusters-Small/ _ω_ B97X-D3 and Clusters-Medium/ _ω_ B97X-D3 training sets. With the exception of pure EC, which was simulated at 313 K, all other compositions were simulated at 298 K. 

data-trained and Periodic-data-trained MLIPs are compared in Figure 5. 

Before analyzing our results in more detail, we note that all of our MLIPs fitted to cluster data are capable of producing stable MD trajectories (1 ns long). This demonstrates the impressive stability of MACE MLIPs and the modest requirement for data amount, as pointed out in ref 13. 

Starting with the Clusters-Large-MLIPs, we immediately observe that there are significant variations in the predicted macroscopic quantities across the committee, with an approximately 4% variation in the density and a 25%−30% variation in the diffusion coefficients. These variations are substantially larger than what was reported by Gong et al.[24] who attempted to train MLIPs starting from the data of Dajnowicz et al.[23] In their work, stable MLIPs could only be obtained after three rounds of active learning, which required a considerable amount of data to be added to the ClustersFull data set. Dajnowicz et al. did not address committee variations, but their values for densities and diffusion coefficients of the pure EC and EMC solvents lie within two standard deviations from the committee average of our Clusters-Large-MLIPs. It should be noted that the MLIPs used in refs 24 and 23 incorporated long-range electrostatics, which may assist in making out-of-domain extrapolation more robust. The importance of long-range information is supported by the recent findings of Gawkowski et al.[19] where successful out-of-domain transfer could be achieved when a bulk-trained MLIP was fine-tuned on cluster data, i.e., where the MLIP had thus previously seen related structures in a bulk context. 

Many of the structures added by Gong et al. consisted of more than one hundred atoms. The largest clusters (in terms of the number of atoms) in our Clusters-Large data set contain 90 atoms, but there are only 16 such instances. In perspective, the number of structures with 90 or more atoms added by Gong et al. were in the tens of thousands. Thus, whether the significantly smaller committee variation obtained by Gong et al. originates from the added electrostatics in their model or from the data added in their active learning process is not clear. The large uncertainties of the committee values from the Cluster-trained MLIPs in Figures 5 and 6 illustrate that even in the case of these seemingly unproblematic organic 

Table 4. Summary of the Densities and Finite Size-Corrected Diffusion Coefficients of the Pure Solvents; Experimental Values Have B Included as a Perspective; the Corrections Were Determined Using _**η**_ EC = 1.93 **×** 10[−][3] Pa s Taken from ref 43 and _**η**_ EMC = 6.5 **×** 10[−][4] Pa s Taken from ref 44; the Values are Reported with Mean and Coefficient of Variation (CV in %), Defined as SD/Mean **×** 100 

|solvent|training set|temperature /K|density/g cm−3|dif. coef. (_D_∞)/<br>1 × 10−6 cm2 _s_−1|
|---|---|---|---|---|
||||mean<br>CV %|mean<br>CV %|
|EC<br>EMC|Clusters-Small/_ω_B97X-D3<br>Clusters-Medium/_ω_B97X-D3<br>Clusters-Large/_ω_B97X-D3<br>expt._a_<br>Clusters-Small/_ω_B97X-D3<br>Clusters-Medium/_ω_B97X-D3<br>Clusters-Large/_ω_B97X-D3<br>expt._b_|313<br>313<br>313<br>313<br>298<br>298<br>298<br>298|1.37<br>4.1<br>1.24<br>2.1<br>1.33<br>4.3<br>1.312<br>1.15<br>8.3<br>0.95<br>4.8<br>1.03<br>4.4<br>1.006|4.16<br>41<br>10.27<br>19<br>5.35<br>31<br>8.0<br>8.12<br>37<br>24.69<br>20<br>15.49<br>25<br>18.3|



> _a_ The density was computed from a specific gravity of 1.322 at 313 K45 and the diffusivity comes from ref 43. _b_ The density was taken from the Merck webpage and the diffusivity from personal communication with Prof. Clare P. Gray. 

**3667** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**Journal of Chemical Theory and Computation** 

Article 

**==> picture [64 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
pubs.acs.org/JCTC<br>**----- End of picture text -----**<br>


Figure 7. Illustration of two factors that will influence the extrapolation capacity of a cluster-trained MLIP, as a result of the cluster extraction for the training set generation. In Figure (a) a cluster is cut out from the liquid (the dashed line). First, the removal of the red atoms (molecules) is an effective truncation of long-range interactions. Second, the green atom is seen to not even have a full liquid-like atomic coordination within a typical MLIP cutoff (illustrated by the green disc). MLIPs trained on data where a majority of clusters are similar to the one in (a) will likely lack the necessary information to express the full structural fingerprint of an atom embedded in a liquid; this means that out-of-domain extrapolation will come into play when such MLIPs are used in subsequent liquid MD simulations. In contrast, (b) shows a larger cluster where at least some of the atoms have full liquid-like atomic coordination, but still lack long-range interactions. 

molecules, cluster data can present a challenging fitting task compared to periodic data if the end purpose is to simulate bulk liquids. RDF-type plots in Figure S2 show that most bulklike atomic environments in the Clusters-Full data set have coordinations that are much lower than those in the liquid (see the SI for a detailed analysis). The reason for our large committee variations is likely the result of at least one of the two effects illustrated in Figure 7. 

The figure illustrates the process of selecting clusters from a liquid to serve in a training set for MLIP generation, and the implication of this seection when the MLIP is subsequently applied in periodic MD simulations. Clearly, removing all the red molecules in the two figures will result in the loss of longrange interactions which can provide important contributions to energies and forces (Figure 7). The first effect stems from local coordination around the atoms inside a cluster. If we consider the local atomic environment defined by the green disc in Figure 7a, we know that a liquid will have a characteristic average structure around each atom. If we train an MLIP on data where the intermolecular coordination (within the green disc) is un-bulk-like compared to a liquid the sudden appearance of atoms in these regions during simulation may result in uncertain predictions of energies and forces. 

Regarding the representation of structures, we note that the original Clusters-Full data set as well as our Clusters-Large data set contains a disproportionate amount of EC monomers and dimers. The importance of adequate data representation was also highlighted in the work of Goodwin et al.[46] who trained MLIPs on ionic liquids with dissolved salts of different concentrations and found that training on the extreme concentrations (the smallest and the largest, together) and then predicting on medium concentrations turned out to be far more challenging than doing the reverse. 

To mitigate disturbing influences from skewness in the training data, we down-sampled (size reduction) the Clusters-Large data set into successively smaller training sets. 

For this reason, we created different variations of these subsamples. We also examined the effect of different training 

seeds in the same way as for the Clusters-Large MLIPs. As summarized in Section 2.1, the down-sampling of the Clusters-Large data set was performed in two steps where, in each step, 25% of the previous (larger) data set was selected with the aim of making it more bulk-like and more compositionally balanced. This resulted in two additional data set sizes: Clusters-Medium which contained 25% of Clusters-Large, and Clusters-Small which contained 25% of Clusters-Medium. Figure 2 shows the different molecular compositions of the various data set sizes. The transition from Clusters-Large to ClustersMedium is associated with a considerable reduction in pure EC clusters. The strategy behind generating the ClustersMedium composition was to include a more diverse set of atomic environments than only EC and EMC could provide. Despite not being part of the liquid simulations, the other molecules (see caption of Figure 2) are similar to either EC or EMC. Therefore, from the atomic-centered perspective of the MACE-MLIPs, many of the atomic environments present in these clusters are likely relevant also for EC and EMC. For example, clusters containing DEC may provide examples of atomic environments that are relevant also for EMC which happens to be poorly represented in the Clusters-Full and Clusters-Large data sets. The motivation behind the reduction from Clusters-Medium to ClustersSmall was based on similar grounds. Three copies were then made of each reduced data set which, for each data set size, all shared the same relative molecular composition but not exactly the same selection of clusters. To be precise, three copies were made of the Clusters-Medium data set which all shared the composition depicted in the second panel of Figure 2, but which did not share exactly the same cluster identities throughout. The same procedure was carried out for the Clusters-Small data set, resulting in a total of seven data sets (3 × Clusters-Small + 3 × Clusters-Medium + 1 × Clusters-Large). 

Figures 5 and 6 display similar large uncertainties for properties produced by the MLIPs trained on the smaller subsets of the cluster data, as found for the Cluster-Large MLIPs discussed above. The error bars are either touching or 

**3668** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**pubs.acs.org/JCTC** 

Article 

## **Journal of Chemical Theory and Computation** 

overlapping, making the results from the different MLIPs trained on different data set sizes statistically indistinguishable from one another. For completeness, MLIPs were also trained on the three variants of the Clusters-Small and of Clusters-Medium data sets that had been labeled with the B97-D3 functional. As the predictive quality of these MLIPs (see Figures S6 and S7 in the SI) did not improve, we conclude that the uncertainties of the cluster-based data is not coupled to the level of theory used to label the structures. A direct comparison among the Periodic/B97-D3, Clusters-Small/B97-D3, and Clusters-Medium/B97D3 models, shown in Figure S8, highlights this. 

In conclusion, the differences in predicted macroscopic quantities in our cluster fitted models are much larger than those from models fitted on different functionals for periodic data. These cluster data sets can therefore not be used to directly extend our functional comparison without further augmentation/modification of the data. This has important implications to both tailored MLIPs and foundational models. Whether or not explicit long-range interactions can serve to counter the variations that are due to the training seed remains to be seen and may be the subject of a future study. 

## **4. CONCLUDING REMARKS** 

The overall context of our study is the benchmarking of the DFT functionals. We have presented a strategy to enable the comparison of DFT functionals with respect to their ability to describe macroscopic liquid properties such as density and diffusivity here for EC:EMC mixtures. By training MACEMLIPs on periodic DFT-GGA data from the literature and subsequently relabeling the data using different GGA functionals, we were able to meaningfully compare both the densities and diffusion coefficients from long (and stable) MD simulations between functionals without having to resort to active learning. Here, only three functionals were compared as a proof-of-concept for the approach, but the same strategy can, in principle, be adopted for any functional applicable to periodic systems. 

The second part of our study deals with MLIPs trained on cluster data, starting from data available in the literature, namely, a large cluster data set of organic molecules labeled at the _ω_ B97X-D3 level of theory. Given the current interest in the fitting of MLIPs to cluster data, we highlight aspects that need to be taken into account when cluster-based MLIPs are trained for use in bulk simulations. We demonstrate that our MLIPs trained on clusters exhibit large uncertainties in densities and diffusivities. We attribute this problem to the lack of representative bulk coordination in the training data and/or long-range interactions, a challenge which translates into an out-of-domain extrapolation problem when the clusterbased models are being applied to MD bulk simulations (cf. Figure 7). Our study should be of particular relevance within the context of transfer learning on high-level QM data, a field that is quickly gaining ground in the MLIP community. 

While the resulting cluster-based MACE-MLIPs produced stable MD trajectories, the resulting variations of densities and diffusivities across model committees were significantly larger � than with the periodic-data-based MLIPs in fact, too large to make meaningful comparisons between functionals. Because of the impressive capability of MACE to produce stable MLIPs even for small/unbalanced training sets, treating MACE-MLIP stability as a quality indicator may be treacherous. 

## ■ **[ASSOCIATED][CONTENT]** 

## **Data Availability Statement** 

The training data was published in our previous work[8] and by Dajnowicz et al.[23] The MD trajectories generated here are freely available and accessible through the github-page: https://github.com/viktorsvahn/Limits_of_cluster_MLIPs, along with Jupyter-notebooks that contain analysis scripts. * **sı Supporting Information** 

The Supporting Information is available free of charge at https://pubs.acs.org/doi/10.1021/acs.jctc.5c02043. 

Details about MLIP performance measured in terms of structure, density, and diffusion coefficients; and detailed analysis about the compactness of clusters in the clusterbased training sets (PDF) 

## ■ **[AUTHOR][INFORMATION]** 

## **Corresponding Author** 

- Jolla Kullgren − _Department of Chemistry-Ångström, Uppsala University, S-75231 Uppsala, Sweden;_ orcid.org/00000003-3570-0050; Email: jolla.kullgren@kemi.uu.se 

## **Authors** 

- Viktor Svahn − _Department of Chemistry-Ångström, Uppsala University, S-75231 Uppsala, Sweden;_ orcid.org/00090000-1808-8352 

- Ioan-Bogdan Magdau − _School of Natural and Environmental Sciences, Newcastle University, Newcastle Upon Tyne NE1 7RU, U.K.;_ orcid.org/0000-0002-39635076 

- Samuel P. Niblett − _Yusuf Hamied Department of Chemistry, University of Cambridge, Cambridge CB2 1EW, U.K.; Dassault Systemes BIOVIA, Cambridge CB4 0WN, U.K.;_ orcid.org/0000-0003-0337-0464 

- Gábor Csányi − _Engineering Laboratory, University of Cambridge, Cambridge CB2 1PZ, U.K.;_ orcid.org/00000002-8180-2034 

- Kersti Hermansson − _Department of Chemistry-Ångström, Uppsala University, S-75231 Uppsala, Sweden;_ orcid.org/0000-0003-2352-0458 

Complete contact information is available at: https://pubs.acs.org/10.1021/acs.jctc.5c02043 

## **Notes** 

The authors declare the following competing financial interest(s): GC is a partner in Symmetric Group LLP that licenses force-fields commercially and also has equity interest in Angstrom AI. 

## ■ **[ACKNOWLEDGMENTS]** 

Financial support from the Swedish Research Council (Vetenskapsradet, Grant no 2024-05507_VR) and the National Strategic e-Science Program eSSENCE (Sweden) is gratefully acknowledged. S.P.N. acknowledges advice and support from Prof. P. Clare Grey, and funding from Prof. Grey’s ERC Advanced Investigator Grant “BATNMR,” Grant no. 83507, and from the Faraday Institution’s Nexgenna project (FIRG064). The project was also funded by the European Union’s Horizon 2020 Research and Innovation Program under Grant Agreement No. 957189 (BIG-MAP project). The calculations were performed using computational 

**3669** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

**Journal of Chemical Theory and Computation** 

**pubs.acs.org/JCTC** 

Article 

resources provided by the N8 Centre of Excellence in Computationally Intensive Research (N8 CIR), funded by the N8 research partnership and EPSRC (Grant No. EP/ T022167/1), and coordinated by the Universities of Durham, Manchester, and York. Computational resources were also provided by the Swedish National Infrastructure for Computing (SNIC/NAISS) on the Tetralith. We also acknowledge the EuroHPC Joint Undertaking for awarding this project access to the EuroHPC supercomputer LUMI, hosted by CSC (Finland) and the LUMI consortium through a EuroHPC Regular Access call. 

## ■ **[REFERENCES]** 

(1) Kuhne, T. D.; Khaliullin, R. Z. Electronic signature of the instantaneous asymmetry in the first coordination shell of liquid water. _Nat. Commun._ 2013, _4_ , 1450. 

(2) Morawietz, T.; Singraber, A.; Dellago, C.; Behler, J. How van der Waals interactions determine the unique properties of water. _Proc. Natl. Acad. Sci. U.S.A._ 2016, _113_ (30), 8368−8373. 

(3) Muller, T.; Sharma, S.; Gross, E. K. U.; Dewhurst, J. K. Extending Solid-State Calculations to Ultra-Long-Range Length Scales. _Phys. Rev. Lett._ 2020, _125_ (25), 256402. 

(4) Behler, J. First principles neural network potentials for reactive simulations of large molecular and condensed systems. _Angew. Chem., Int. Ed._ 2017, _56_ (42), 12828−12840. 

(5) Galib, M.; Limmer, D. T. Reactive uptake of N2O5 by atmospheric aerosol is dominated by interfacial processes. _Science_ 2021, _371_ (6532), 921−925. 

(6) Jaouni, T.; Di Colandrea, F.; Amato, L.; Cardano, F.; Karimi, E. _Quantum Process Tomography of Structured Optical Gates with Convolutional Neural Networks_ , 2024; . arXiv preprint arXiv:2402.16616. 

(7) Yang, Y.; Zhang, S.; Ranasinghe, K. D.; Isayev, O.; Roitberg, A. E. Machine learning of reactive potentials. _Annu. Rev. Phys. Chem._ 2024, _75_ (1), 371−395. 

(8) Magdau, I.-B.; Arismendi-Arrieta, D. J.; Smith, H. E.; Grey, C. P.; Hermansson, K.; Csányi, G. Machine learning force fields for molecular liquids: Ethylene carbonate/ethyl methyl carbonate binary solvent. _npj Comput. Mater._ 2023, _9_ (1), 146. 

(9) Scheidgen, M.; Himanen, L.; Ladines, A. N.; Sikter, D.; Nakhaee, M.; Fekete, A.; Chang, T.; Golparvar, A.; Márquez, J. A.; Brockhauser, S.; Bruckner, S.; Ghiringhelli, L. M.; Dietrich, F.; Lehmberg, D.; Denell, T.; Albino, A.; Näsström, H.; Shabih, S.; Dobener, F.; Kuhbach, M.; Mozumder, R.; Rudzinski, J. F.; Daelman, N.; Pizarro, J. M.; Kuban, M.; Salazar, C.; Ondracka, P.; Bungartz, H.-J.; Draxl, C. NOMAD: A distributed web-based platform for managing materials science research data. _J. Open Source Softw._ 2023, _8_ (90), 5388. 

(10) Horton, M. K.; Huck, P.; Yang, R. X.; Munro, J. M.; Dwaraknath, S.; Ganose, A. M.; Kingsbury, R. S.; Wen, M.; Shen, J. X.; Mathis, T. S.; Kaplan, A. D.; Berket, K.; Riebesell, J.; George, J.; Rosen, A. S.; Spotte-Smith, E. W. C.; McDermott, M. J.; Cohen, O. A.; Dunn, A.; Kuner, M. C.; Rignanese, G.-M.; Petretto, G.; Waroquiers, D.; Griffin, S. M.; Neaton, J. B.; Chrzan, D. C.; Asta, M.; Hautier, G.; Cholia, S.; Ceder, G.; Ong, S. P.; Jain, A.; Persson, K. A. Accelerated data-driven materials science with the Materials Project. _Nat. Mater._ 2025, _24_ , 1522−1532. 

(11) Bartók, A. P.; Csányi, G. Gaussian approximation potentials: A brief tutorial introduction. _Int. J. Quantum Chem._ 2015, _115_ (16), 1051−1057. 

(12) I., Batatia, D. P., Kovács, G. N. C., Simm, C., Ortner, G., Csányi MACE: Higher Order Equivariant Message Passing Neural Networks for Fast and Accurate Force Fields In _Advances in Neural Information Processing Systems_ , 11423−11436 Curran Associates, Inc. January 2023. arXiv:2206.07697 [cond-mat, physics:physics, stat]. 

(13) Niblett, S. P.; Kourtis, P.; Magdau, I.-B.; Grey, C. P.; Csányi, G. Transferability of data sets between machine-learned interatomic potential algorithms. _J. Chem. Theory Comput._ 2025, _21_ , 6096−6112. 

(14) Perdew, J. P.; Schmidt, K.. Jacob’s ladder of density functional approximations for the exchange-correlation energy. In _AIP Conference Proceedings_ ; American Institute of Physics; Vol. _577_ , pp 1−20.2001 

(15) Mardirossian, N.; Head-Gordon, M. Thirty years of density functional theory in computational chemistry: an overview and extensive assessment of 200 density functionals. _Mol. Phys._ 2017, _115_ (19), 2315−2372. 

(16) Zguns, P.; Pudza, I.; Kuzmin, A. Benchmarking CHGNet Universal Machine Learning Interatomic Potential against DFT and EXAFS: The Case of Layered WS2 and MoS2. _J. Chem. Theory Comput._ 2025, _21_ (16), 8142−8150. 

(17) Kaur, H.; Della Pia, F.; Batatia, I.; Advincula, X. R.; Shi, B. X.; Lan, J.; Csányi, Gábor; Michaelides, A.; Kapil, V. Data-efficient finetuning of foundational models for first-principles quality sublimation enthalpies. _Faraday Discuss._ 2025, _256_ (0), 120−138. 

(18) Radova, M.; Stark, W. G.; Allen, C. S.; Maurer, R. J.; Bartók, A. P. Fine-tuning foundation models of materials interatomic potentials with frozen transfer learning. _npj Comput. Mater._ 2025, _11_ (1), 237. 

(19) Gawkowski, M. J.; Li, M.; Shi, B. X.; Kapil, V. The Good, the Bad, and the Ugly of Atomistic Learning for “Clusters-to-Bulk” Generalization. _Mach. Learn.: Sci. Technol._ 2025, _7_ , 025004. 

(20) Batatia, I.; Benner, P.; Chiang, Y.; Elena, A. M.; Kovacs, D. P.; Riebesell, J.; Advincula, X. R.; Asta, M.; Avaylon, M.; Baldwin, W. J.; Berger, F.; Bernstein, N.; Bhowmik, A.; Bigi, F.; Blau, S. M.; Carare, V.; Ceriotti, M.; Chong, S.; Darby, J. P.; De, S.; Della Pia, F.; Deringer, V. L.; Elijosius, R.; El-Machachi, Z.; Fako, E.; Falcioni, F.; Ferrari, A. C.; Gardner, J. L. A.; Gawkowski, M.ła. J.; GenreithSchriever, A.; George, J.; Goodall, R. E. A.; Grandel, J.; Grey, C. P.; Grigorev, P.; Han, S.; Handley, W.; Heenen, H. H.; Hermansson, K.; Ho, C. H.; Hofmann, S.; Holm, C.; Jaafar, J.; Jakob, K. S.; Jung, H.; Kapil, V.; Kaplan, A. D.; Karimitari, N.; Kermode, J. R.; Kourtis, P.; Kroupa, N.; Kullgren, J.; Kuner, M. C.; Kuryla, D.; Liepuoniute, G.; Lin, C.; Margraf, J. T.; Magdau, I.-B.; Michaelides, A.; Moore, J. H.; Naik, A. A.; Niblett, S. P.; Norwood, S. W.; O’Neill, N.; Ortner, C.; Persson, K. A.; Reuter, K.; Rosen, A. S.; Rosset, L. A. M.; Schaaf, L. L.; Schran, C.; Shi, B. X.; Sivonxay, E.; Stenczel, T. K.; Sutton, C.; Svahn, V.; Swinburne, T. D.; Tilly, J.; van der Oord, C.; Vargas, S.; VargaUmbrich, E.; Vegge, T.; Vondrak, M.; Wang, Y.; Witt, W. C.; Wolf, T.; Zills, F.; Csanyi, G. A Foundation Model for Atomistic Materials Chemistry. _J. Chem. Phys._ 2025, _163_ (18), 184110. 

(21) Kovács, D. P.; Moore, J. H.; Browning, N. J.; Batatia, I.; Horton, J. T.; Pu, Y.; Kapil, V.; Witt, W. C.; Magdau, I.-B.; Cole, D. J.; et al. Mace-off: Short-range transferable machine learning force fields for organic molecules. _J. Am. Chem. Soc._ 2025, _147_ (21), 17598− 17611. 

(22) Beiersdorfer, A.; Hetzel, L.; Staacke, C.; Deißenbeck, F.; Stein, C. J. GAP vs. MACE: Efficiency Evaluation in a Liquid Electrolyte System. _ChemRxiv._ 2025. 

(23) Dajnowicz, S.; Agarwal, G.; Stevenson, J. M.; Jacobson, L. D.; Ramezanghorbani, F.; Leswing, K.; Friesner, R. A.; Halls, M. D.; Abel, R. High-Dimensional Neural Network Potential for Liquid Electrolyte Simulations. _J. Phys. Chem. B_ 2022, _126_ (33), 6271−6280. 

(24) Gong, S.; Zhang, Y.; Mu, Z.; Pu, Z.; Wang, H.; Han, Xu; Yu, Z.; Chen, M.; Zheng, T.; Wang, Z.; Chen, L.; Yang, Z.; Wu, X.; Shi, S.; Gao, W.; Yan, W.; Xiang, L. A predictive machine learning force-field framework for liquid electrolyte development. _Nat. Mach. Intell._ 2025, _7_ (4), 543−552. 

(25) S., Sahoo, C., Lampert, G.., Martius Learning Equations for Extrapolation and Control. In _Proceedings of the 35th International_ − _Conference on Machine Learning_ , pages 4442 4450. PMLR, July 2018. ISSN: 2640−3498. 

(26) Blöchl, P. E. Projector augmented-wave method. _Phys. Rev. B_ 1994, _50_ (24), 17953−17979. 

(27) Kresse, G.; Hafner, J. _Ab initio_ molecular dynamics for liquid metals. _Phys. Rev. B_ 1993, _47_ (1), 558−561. 

(28) Kresse, G.; Hafner, J. _Ab initio_ molecular-dynamics simulation of the liquid-metalamorphous-semiconductor transition in germanium. _Phys. Rev. B_ 1994, _49_ (20), 14251−14269. 

**3670** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

T **Journal of Chemical Theory and Computation** ~~T~~ **pubs.acs.org/JCTC** Article 

(29) Kresse, G.; Furthmuller, J. Efficiency of _ab initio_ total energy calculations for metals and semiconductors using a plane-wave basis set. _Comput. Mater. Sci._ 1996, _6_ (1), 15−50. 

(30) Kresse, G.; Furthmuller, J. Efficient iterative schemes for _ab initio_ total-energy calculations using a plane-wave basis set. _Phys. Rev. B - Condens. Matter Mater. Phys._ 1996, _54_ (16), 11169−11186. 

(31) Perdew, J. P.; Burke, K.; Ernzerhof, M. Generalized gradient approximation made simple. _Phys. Rev. Lett._ 1996, _77_ (18), 3865− 3868. 

(45) Anna; George, W. 3.7 - generic solvents. In Anna, G., Eds., _Wypych Databook of Green Solvents_ , pages 237−402. William Andrew Publishing, 2014. 

(46) Goodwin, Z. A. H.; Wenny, M. B.; Yang, J. H.; Cepellotti, A.; Ding, J.; Bystrom, K.; Duschatko, B. R.; Johansson, A.; Sun, L.; Batzner, S.; Musaelian, A.; Mason, J. A.; Kozinsky, B.; Molinari, N. Transferability and Accuracy of Ionic Liquid Simulations with Equivariant Machine Learning Interatomic Potentials. _J. Phys. Chem. Lett._ 2024, _15_ (30), 7539−7547. 

(32) Axel, D. B. Density-functional thermochemistry. v. systematic optimization of exchange-correlation functionals. _J. Chem. Phys._ 1997, _107_ (20), 8554−8560. 

(33) Grimme, S.; Antony, J.; Ehrlich, S.; Krieg, H. A consistent and accurate _ab initio_ parametrization of density functional dispersion correction (DFT-D) for the 94 elements H-Pu. _J. Chem. Phys._ 2010, _132_ (15), 154104. 

(34) Grimme, S.; Ehrlich, S.; Goerigk, L. Effect of the damping function in dispersion corrected density functional theory. _J. Comput. Chem._ 2011, _32_ (7), 1456−1465. 

(35) Stewart, J. C.; Segall, M. D.; Pickard, C. J.; Hasnip, P. J.; Probert, M. I. J.; Refson, K.; Payne, M. C. First principles methods using CASTEP. _Z. Kristallogr. Cryst. Mater._ 2005, _220_ (5−6), 567− 570. 

(36) Smith, D. G. A.; Burns, L. A.; Simmonett, A. C.; Parrish, R. M.; Schieber, M. C.; Galvelis, R.; Kraus, P.; Kruse, H.; Di Remigio, R.; Alenaizan, A.; James, A. M.; Lehtola, S.; Misiewicz, J. P.; Scheurer, M.; Shaw, R. A.; Schriber, J. B.; Xie, Y.; Glick, Z. L.; Sirianni, D. A.; O’Brien, J. S.; Waldrop, J. M.; Kumar, A.; Hohenstein, E. G.; Pritchard, B. P.; Brooks, B. R.; Schaefer, H. F., III; Sokolov, A. Y.; Patkowski, K.; DePrince, A. E., III; Bozkaya, U.; King, R. A.; Evangelista, F. A.; Turney, J. M.; Crawford, T. D.; Sherrill, C. D. Psi4 1.4: Open-source software for high-throughput quantum chemistry. _J. Chem. Phys._ 2020, _152_ (18), 184108. 

(37) Mardirossian, N.; Head-Gordon, M. _ω_ B97X-V: A 10parameter, range-separated hybrid, generalized gradient approximation density functional with nonlocal correlation, designed by a survival-of-the-fittest strategy. _Phys. Chem. Chem. Phys._ 2014, _16_ (21), 9904−9924. 

(38) Weigend, F.; Ahlrichs, R. Balanced basis sets of split valence, triple zeta valence and quadruple zeta valence quality for H to Rn: Design and assessment of accuracy. _Phys. Chem. Chem. Phys._ 2005, _7_ (18), 3297−3305. 

(39) Rappoport, D.; Furche, F. Property-optimized gaussian basis sets for molecular response calculations. _J. Chem. Phys._ 2010, _133_ (13), 134105. 

(40) Hjorth Larsen, A.; Mortensen, J. J. .; Blomqvist, J.; Castelli, I. E.; Christensen, R.; Dułak, M.; Friis, J.; Groves, M. N.; Hammer, B.; Hargus, C.; Hermes, E. D.; Jennings, P. C.; Jensen, P. B.; Kermode, J.; Kitchin, J. R.; Kolsbjerg, E. L.; Kubal, J.; Kaasbjerg, K.; Lysgaard, S.; Maronsson, Jón B.; Maxson, T.; Olsen, T.; Pastewka, L.; Peterson, A.; Rostgaard, C.; Schiøtz, J.; Schutt, O.; Strange, M.; Thygesen, K. S.; Vegge, T.; Vilhelmsen, L.; Walter, M.; Zeng, Z.; Jacobsen, K. W. The atomic simulation environment-a python library for working with atoms. _J. Phys.: Condens. Matter_ 2017, _29_ (27), 273002. 

(41) Maginn, E. J.; Messerly, R. A.; Carlson, D. J.; Roe, D. R.; Richard Elliot, J. Best Practices for Computing Transport Properties 1. Self-Diffusivity and Viscosity from Equilibrium Molecular Dynamics. _Living J. Comput. Mol. Sci._ https://tsapps.nist.gov/ publication/get_pdf.cfm?pub_id=925953 (Accessed March 23, 2026). 

(42) Spangberg, D.; Hermansson, K. Effective three-body potentials for Li[+] (aq) and Mg[2+] (aq). _J. Chem. Phys._ 2003, _119_ (14), 7263−7281. (43) Hayamizu, K.; Aihara, Y.; Arai, S.; Martinez, C. G. Pulsegradient spin-echo 1H, 7Li, and 19F NMR diffusion and ionic conductivity measurements of 14 organic electrolytes containing lin (SO2CF3) 2. _J. Phys. Chem. B_ 1999, _103_ (3), 519−524. 

(44) Xu, K. Nonaqueous liquid electrolytes for lithium-based rechargeable batteries. _Chem. Rev._ 2004, _104_ (10), 4303−4418. 

**3671** 

https://doi.org/10.1021/acs.jctc.5c02043 _J. Chem. Theory Comput._ 2026, 22, 3660−3671 

