> This article is licensed under ~~——~~ CC-BY 4.0 © ® 

pubs.acs.org/JACS 

Article 

## **Computing Solvation Free Energies of Small Molecules with Experimental Accuracy** 

J. Harry Moore,* Daniel J. Cole, and Gábor Csányi 

**Cite This:** _J. Am. Chem. Soc._ 2026, 148, 4928−4937 **Read Online** 

## ACCESS Metrics & More 

Article Recommendations * **sı** Supporting Information 

ABSTRACT: Free energies play a central role in characterizing the behavior of chemical systems and are among the most important quantities that can be calculated by molecular dynamics simulations. Solvation free energies in various organic solvents, in particular, are well-studied physicochemical properties of drug-like molecules and are commonly used to assess and optimize the accuracy of nonbonded parameters in empirical force fields and also as a fast-to-compute surrogate of performance for protein−ligand binding free energy estimation. Machine learned potentials (MLPs) show great promise as more accurate alternatives to empirical force fields but are not readily decomposed into physically motivated functional forms, which has thus far rendered them incompatible with standard alchemical free energy methods that manipulate individual pairwise interaction terms. However, since the accuracy of free energy calculations is highly sensitive to the force field, this is a key area in which MLPs have the potential to address the shortcomings of empirical force fields. In this work, we introduce an efficient alchemical free energy protocol that enables calculations of rigorous free energy differences in condensed phase systems modeled entirely by MLPs. Using a pretrained, transferable, alchemically equipped MLP model, we demonstrate subchemical accuracy for the solvation free energies of a wide range of organic molecules. 

## **1. INTRODUCTION** 

Free energies are arguably the most important quantities accessible by molecular simulation in soft matter and play an important role in computational drug discovery.[1][,][2] Free energy methods rely on rigorous thermodynamic protocols, enabling prediction of protein−ligand binding,[3][,][4] small-molecule solvation and solubility,[5] organic crystal polymorphs ranking,[6] and protein residue mutation.[7] 

Driven by the widespread availability of efficient GPU hardware, highly optimized molecular dynamics (MD) software[8] and carefully parametrized force fields,[9][,][10] free energy calculations have become an industry standard tool, accounting for a large fraction of the computation performed in pharmaceutical R&D. Relative binding free energy (RBFE) calculations in particular have emerged as a crucial aspect of structure-based drug discovery, helping to screen and rank congeneric series of compounds during hit-to-lead and lead optimization campaigns.[1] 

formations have emerged as the _de facto_ standard approach, allowing free energy estimates to be obtained in a few GPU hours per compound.[11][,][12] Rather than explicitly simulating a compound undergoing a change of state as it would happen in reality (which would be computationally prohibitive), alchemical calculations take advantage of the fact that the free energy is a state function, and so the free energy difference between two state points is independent of the pathway connecting them. By introducing an alchemical parameter, _λ_ , a new Hamiltonian is constructed as a linear combination of the Hamiltonians describing the two end states 

Received: June 28, 2025 Revised: January 12, 2026 Accepted: January 15, 2026 Published: January 27, 2026 

While various methods for calculating free energies for small molecules via MD have been proposed, alchemical trans- 

© 2026 The Authors. Published by American Chemical Society **4928** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

**Journal of the American Chemical Society** 

**pubs.acs.org/JACS** 

Article 

**==> picture [229 x 12] intentionally omitted <==**

The free energy difference associated with the transformation can then be computed by a variety of estimators, for example, by thermodynamic integration 

**==> picture [222 x 28] intentionally omitted <==**

where ⟨···⟩ _λ_ denotes the ensemble average corresponding to the Hamiltonian _H_ ( _λ_ ). Using such artificial pathways leads to enormous computational savings since the sampling required to explore intermediate state points is orders of magnitude less than it would be for a real pathway describing the physical process. In practice, the transformation is accomplished by identifying the atoms that change during the transformation (i.e., those atoms whose chemical element changes, or that disappear entirely) and interpolating the corresponding force field parameters between the end states. This requires the use of so-called “dummy atoms” to model particles that disappear during the transformation. These atoms maintain their bonded terms but have their interactions with their surroundings switched off. This allows for transformations like morphing a methyl group to a hydrogen atom or isolating a molecule from its environment while minimally perturbing the phase space required to be explored by the system. 

Early attempts to perform free energy calculations with MD faced energy conservation and convergence issues due to the divergence of the nonbonded energy (usually a combination of Lennard-Jones and Coulomb contributions) when partially decoupled atoms overlap.[13][,][14] Beutler et al. were the first to address this issue by incorporating softening parameters to scale nonbonded interactions as a function of the alchemical parameter _λ_ , thus averting singularities in the potential energy as atoms come into contact[15] 

**==> picture [229 x 75] intentionally omitted <==**

where _ϵ_ and _σ_ are the Lennard-Jones well depth and radius, respectively, and _α_ LJ, _m_ , and _n_ are positive, tunable constants that control the smoothness and decay of the softcore function. In the original implementation, _α_ LJ = 0.5, _n_ = 4, and _m_ = 2, although _m_ = _n_ = 1 has been shown to reduce the variance of the free energy estimate.[15][−][17] Although Beutler-type softcore potentials are commonly used in various simulation packages, it is worth noting that several alternative approaches have been suggested to further improve numerical stability and address specific failure modes,[18][,][19] and alternative nonbonded functional forms with a more natural softcore have also been tried.[20] 

While these soft-core potentials have been widely successful, a significant limitation of current state-of-the-art free energy calculations lies in the accuracy of the empirical force fields. Specifically, the constraints imposed by the functional form, omission of energetic contributions, and restricted atom-type parameters in small-molecule force fields have a significant impact on accuracy.[1] Particularly notable are the widespread use of fixed-charge electrostatic models that do not account for geometry-dependent polarization, and the limited accuracy of 

torsional barriers, which often require refitting to bespoke DFT calculations of each new compound to achieve reasonable accuracy.[21][−][23] 

In recent years, transferable machine learned potentials (MLPs) have been introduced as a compelling alternative to empirical force fields, demonstrating significant advances in materials modeling and biomolecular simulation.[24][−][29] Building upon Behler and Parinello’s initial work,[30] the field has expanded rapidly, with many architectures being proposed to accurately model the QM potential energy surface. A particularly successful innovation has been the specific encoding of permutational, rotatational, and translational symmetries.[31] These approaches have led to a series of dataefficient, universal potentials for biomolecular and materials simulation, enabling accurate prediction of atomistic and thermodynamic properties for a wide range of chemical compositions, albeit at an increased cost compared to empirical potentials. 

Although MLPs can deliver significant accuracy improvements compared to empirical force fields, their computational expense and the high sampling requirements of free energy calculations have meant that their application has been mostly restricted to corrective perturbations.[32][−][34] In this approach, the intramolecular interactions of a subset of atoms (usually the organic molecule) are modeled by the MLP, while the remaining bonded interactions and all nonbonded interactions are modeled by the empirical force field. Although there is some evidence that this approach can modestly improve the accuracy of RBFE calculations, it does not address the parametrization of nonbonded interactions, which are known to be crucial for obtaining accurate free energies.[33] Indeed, it has recently been shown that, for hydration free energies, MLP corrections with mechanical embedding fail to provide statistically significant accuracy improvements.[34] It is worth noting that more sophisticated electrostatic embedding ML/ MM schemes have recently been proposed.[35][−][37] However, the performance of these methods in alchemical binding free energy calculations has not yet been established. 

In parallel, a handful of free energy methods that do not rely on alchemical transformations have been proposed, making the calculation conceptually more straightforward, easier to set up, and more amenable to MLPs. One promising example uses the alchemical transfer method (ATM),[38] which relies on a coordinate transformation to interpolate between two physical end states.[39][,][40] It has been shown that, especially in combination with the ANI-2x potential for modeling the ligand intramolecular potential energy surface,[24] this method is competitive with the commercially available FEP+ package,[3] which uses the empirical OPLS4 force field.[41] This work still relies upon a mechanically embedded ML/MM Hamiltonian, and since both physical end states must be accommodated within the same simulation box, it is less efficient than alchemical perturbation methods due to the large amount of excess solvent required.[38] 

Given the potential for significant accuracy improvements, there is a need for rigorous and efficient alchemical free energy methods that are compatible with (i) describing the entire system using MLPs, and (ii) existing well-tested free energy protocols and analysis packages (e.g., pymbar,[42] pmx[43][,][44] ) that are currently in use with classical force fields. In this work, we present a pretrained, transferable biomolecular MLP based on the recently introduced MACE-OFF potentials[25] that is uniquely equipped with scalable soft-core interactions, 

**4929** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

**Journal of the American Chemical Society** 

**pubs.acs.org/JACS** 

Article 

enabling numerically stable simulations of condensed phase systems with alchemically decoupled intermolecular interactions. We provide an efficient implementation of the method in the widely used OpenMM package.[8] Furthermore, we demonstrate the fast convergence and subchemical accuracy of our approach in the calculation of solvation free energies and distribution coefficients for a series of organic molecules. 

precautions, this approach can lead to artificial softening of the minimum of the dimer curve if the switching point is too close to the minimum. Conversely, a switching point that is too far from equilibrium would lead to large energy and force values for small separations, which are more challenging for the model to learn. 

To balance these competing factors, the transition point was adjusted for each dimer curve to minimize the gradient of the force at the switching point, down to a minimum value of 3 eV/Å[2] , which in turn limited the maximum energy of pairwise interactions to a numerically stable value, typically around 300 kcal/mol above the minimum. However, by setting a minimum gradient for the switching point, the transition point was chosen so as not to alter the position and curvature of the energy minimum, thereby preserving the equilibrium properties of the potential. This therefore ensures that the softcore region is only explored during alchemical simulations in which the nonbonded interactions are (partially) decoupled, since this region of the energy landscape lies several hundred kcal/ mol higher in energy than equilibrium. All switching point distances are listed in Section S4. 

## **2. RESULTS AND DISCUSSION** 

## **2.1. Alchemical Simulations with MLPs** 

To address the divergence of the potential energy predicted by an MLP fitted to DFT, as atoms overlap when sampling intermediate values of _λ_ , we augmented the training set with dimer configurations containing artificially softened two-body interactions. We further incorporated a _λ_ dependence via modification of the nontrainable parameters of the model architecture to scale nonbonded interactions between the solute and the solvent. This combined approach results in _λ_ - dependent many-body interactions that enable smooth and regularized interpolation between the coupled and decoupled end states. We note that, since only the nontrainable parameters are modulated during the simulation, no major changes to the training protocol are required. In all cases, the potential was trained corresponding to the _λ_ = 1 or fully interacting state, while the message scaling is only applied at inference time to the fitted potential. 

The steeper curvature of tenth-order functions enables smaller maximum forces and energies compared to lower-order polynomials that have been employed in previous softcore formulations.[18] Using the MACE-OFF24 training data set[25] augmented with the synthetic dimer curves, we then fitted the softcore potential from scratch. Since it is expected that the learned radial embeddings will differ substantially from the MACE-OFF models due to the new softcore data, we found that this resulted in lower force and energy errors compared to transfer learning from the original MACE-OFF checkpoints. 

**2.1.1. Softcore Dimer Curves.** To construct the softcore dimer curves, we first computed dimer curves with DFT at the same _ω_ B97M-D3BJ/def2-TZVPPD level of theory as the SPICE data set[45] for all combinations of the 10 elements covered by MACE-OFF.[25] For each pair, we started by matching the value and gradient of the DFT force with a polynomial of the form _ax_[10] + _b_ that approaches a constant value as _r_ → 0 (Figure 1). The softcore energies were then obtained by analytical integration of the polynomial to ensure consistent energy and force data. Without appropriate 

The test set errors for the MACE-OFF data set were comparable to the performance of the original potentials,[25] indicating that the model’s ability to learn energies and forces of equilibrium configurations is not affected by additional softcore data (Section S1). We further confirmed that the predicted density of liquid water is unaffected by the new potential, with an average value of 1.02 ± 0.02 g/mL at 298 K (compared with 0.98 g/mL for MACE-OFF24(M)). 

It is worth noting that, while the introduction of softcore interactions is not expected to affect the ensemble sampled by the model at room temperature, since the curvature of the minimum is not affected and a substantial repulsive component is still learned by the model, this may not necessarily translate to high temperature regimes. In this case, the softcore region of the potential may be thermally accessible in the fully interacting state rather than only being accessible in the partially decoupled states. 

**==> picture [263 x 28] intentionally omitted <==**

**----- Start of picture text -----**<br>
§1 is still<br>={<br>w 500 1<br>Y!<br>**----- End of picture text -----**<br>


**2.1.2. Alchemical Modification to MACE.** While in principle the softcore formulation described above is sufficient to perform stable alchemical free energy calculations, in practice, the resulting linear formulation, where the functional form of the potential has no explicit dependence on _λ_ , can lead to significant challenges with phase space overlap.[46] Functions lacking this _λ_ dependence typically require complex reweighting strategies to adjust window spacing on the fly to maintain reasonable overlap between neighboring replicas. To avoid these issues, we also modified the nonlearnable parameters in MACE to enable alchemical scaling of selected nonbonded interactions, resulting in a formulation analogous to classical soft-core force fields.[15][,][18][,][19] By modifying only the nontrainable parameters of MACE, our approach enables alchemical simulations of arbitrary systems without additional 

Figure 1. Construction of the soft-core dimer curve for the Br−O diatomic pair by matching the gradient at a set switching point to that given by DFT. 

**4930** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

**pubs.acs.org/JACS** 

Article 

## **Journal of the American Chemical Society** 

fine-tuning of the model or modification of the training protocol. 

While we introduce alchemical modifications in terms of the MACE architecture, we stress that our approach can be applied to any architecture that parametrizes the local energy as a function of two-body terms, as has been recently demonstrated elsewhere.[47] Here we describe the changes to the MACE architecture required to implement scaled nonbonded interactions. For a full description of the architecture, we direct the reader to the original publications.[31][,][48] 

MACE predicts the total energy of a system as a sum of atom-wise contributions. Each atom’s environment is constructed from the relative coordinates and atomic numbers of its neighbors, up to a fixed cutoff. These high-body-order atomic features are efficiently constructed by taking tensor products of two-body terms that describe pairwise interactions. 

For each atom, the initial features of its neighbors are combined with the interatomic displacement vectors, _rij_ , to form the one-particle basis _ϕ_ ( _ijt_ , _k_ ) _η_ 1 _l_ 3 _m_ 3. The radial distance is used as an input into a learnable radial function _R_ ( _rij_ ) with several outputs that correspond to the different ways in which the displacement vector and the node features can be combined while preserving equivariance[49] 

**==> picture [229 x 36] intentionally omitted <==**

where _Ylm_ are the spherical harmonics, and _C_ l _η_ 31 _m_ , 3 _l_ 1 _m_ 1 _l_ 2 _m_ 2 denotes the Clebsch-Gordan coefficients. There are multiple ways of constructing an equivariant combination with a given symmetry ( _l_ 3, _m_ 3), and these multiplicities are enumerated by the path index _η_ 1.[48][,][50] 

In a similar approach to other recently published work,[51] our formulation modifies MACE by including an additional factor of _αij_ that scales selected two-body terms in the one-particle basis. These terms are selected as those that cross the alchemical boundary, for example, edges connecting atoms in the solute and solvent in the case of a solvation free energy calculation. 

**==> picture [229 x 29] intentionally omitted <==**

The one-particle basis functions _ϕ_ ( _ijt_ , _k_ ) _η_ 1 _l_ 3 _m_ 3 are then passed through multiple layers of message passing, during which tensor products are taken to construct the many-body symmetric features. 

**==> picture [229 x 25] intentionally omitted <==**

This approach (named MACE-OFF24-SC) enables smoothly scaled many-body nonbonded interactions while maintaining the correct physical description of the end states, where the decoupled system’s graph is identical to that of the separated components, ensuring consistent free energy calculations. 

In MACE-OFF24-SC, an approximately linear _λ_ schedule can be applied to the alchemical transformation (Figure 2), regardless of the size of the perturbation, compared to the highly skewed schedule required for linear softcore potentials.[46] It is also worth noting that, unlike linear scaling 

Figure 2. Dependence of softcore two-body interactions on _λ_ for a C−F diatomic pair learned by MACE-OFF24-SC. 

schemes, this approach is amenable to nonequilibrium switching approaches, in which _λ_ is driven at a constant rate between the end states[4][,][52] (Section S5). 

While this approach can be applied in principle to any manybody potential that constructs site-wise energies as a tensor product of two-body features, we note that the success of this approach depends on the strong regularization of MACE to enable smooth interpolation between the end states, as the contributions to the node energies are a nonlinear function of the (scaled) two-body features. 

We also note that our alchemical modifications to the MACE graph share similarities with recently published work by Nam et al.[51] In particular, this work also introduces a scaling factor on the one-particle basis functions of MACE to compute free energy changes in solids. While this is sufficient for studying crystalline systems, the additional inclusion of the softcore potential is crucial for stable alchemical condensed phase simulations, where, unlike materials applications, direct atomic overlap in partially decoupled states must be handled. 

## **2.2. Solvation Free Energy Calculations** 

Solvation free energies play a crucial role in assessing the accuracy of the intermolecular interactions within a force field and are an essential component of the standard evaluation of thermodynamic property prediction. These simulations probe the subtle nonbonded interactions between molecules, but their sampling requirements remain small relative to, for example, protein−ligand binding free energies; hence, errors can be primarily attributed to the accuracy of the force field. 

However, unlike properties such as densities and enthalpies of vaporization and mixing, which are directly observable as ensemble averages from MD trajectories, free energies require evaluation of expectation values such as that shown in eq 2. Here we employ the MBAR estimator to compute the free energy difference between the end states A and B, by combining information from a series of intermediate alchemical windows in a statistically optimal fashion.[42][,][53] We stress, however, that our approach is agnostic to the estimator used. 

These calculations can be efficiently performed using perturbations in parameter space, where the intermolecular interactions are gradually decoupled between the solute and solvent. Although such free energy calculations are routine with empirical force fields, to the best of our knowledge, this 

**4931** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

e **Journal of the American Chemical Society** ~~e~~ **pubs.acs.org/JACS** Article ~~|~~ 

work demonstrates the first rigorous, _ab initio_ quality solvation free energy calculations with all molecules treated using MLPs. **2.2.1. Hydration Free Energies.** We first evaluated the ability of MACE-OFF24-SC to compute accurate, converged hydration free energies for a series of organic molecules (Figure 3). For this test, we selected a diverse set of 

Figure 4. Convergence of the ethane hydration free energy with simulation time. OeC._ SI cm ATTA TA Table 1. Summary of Hydration Free Energy Errors (kcal/ mol) 

|MACE-OFF24-SC<br>GAFF<br>OpenFF 2.1|MAE<br>0.69<br>1.09<br>0.98|RMSE<br>0.80<br>1.24<br>1.15|
|---|---|---|



charges on aliphatic hydroxyl groups.[56][,][57] Since our approach is not dependent upon the coarse-grained chemical space through atom-typing, our approach is not susceptible to the same inaccuracies. 

Figure 3. Comparison of MACE-OFF24-SC hydration free energies with classical force fields and experiment. Experimental error bars are shown for those compounds in which the value exceeds 0.6 kcal/mol. The shaded region represents a 1 kcal/mol deviation. 

compounds from the FreeSolv database designed to cover a diverse range of functional groups relevant to medicinal chemistry.[54] Compounds were first binned according to their functional groups and subsequently filtered to remove those that were not unambiguously neutral at pH 7, as determined by Schrodinger’s Epik program.[55] This ensured compatibility with MACE-OFF24-SC, which was trained on neutral molecules only. Compounds were then randomly sampled from each bin, ensuring a good functional group coverage. The identities of the selected 36 compounds are tabulated in Section S3. 

We performed replica exchange molecular dynamics with an ensemble of replicas with _λ_ windows spaced in the interval [0,1] to connect the physical end states. To expedite phase space exploration, exchanges of replicas between adjacent _λ_ windows were attempted every 1 ps. 

Notwithstanding atom-type-specific parametrization issues, it is encouraging to find that MACE-OFF24-SC is capable of exceeding the accuracy of classical force fields, especially considering that the nonbonded parameters of both OpenFF 2.1 and GAFF2 have been parametrized to reproduce condensed phase properties of similar small molecules, whereas MACE-OFF24-SC must learn these interactions directly from the quantum mechanical training data. It is also worth noting that all force fields are approaching the average experimental error of the data set, around 0.6 kcal/mol, making further quantitative comparison challenging (Figure 3). 

**2.2.2. Solvation Free Energies in a Nonaqueous Solvent.** We have shown that MACE-OFF24-SC is capable of obtaining highly accurate solvation free energy predictions across a range of small organic molecules. However, while these serve as a useful and important benchmark, often the more relevant quantity in drug discovery is the distribution 

In all cases, simulations were performed with 16 replicas, which we found enabled sufficient phase-space overlap to converge the free energy simulations (Figure 5). The replica spacing was hand-tuned from an initial linear spacing to concentrate sampling in the region 0.15 ≤ _λ_ ≤ 0.4, where the _H_ curvature of ~~a~~ ah is greatest (Section S5). For each system, convergence of the free energy as a function of time was confirmed (Figures 4 and S2). 

Across the range of molecules studied here, we find that free energy predictions computed using MACE-OFF24-SC match or, in many cases, outperform widely used classical force fields, with a consistent improvement in MAE and RMSE compared to the classical force fields (Table 1). 

For example, compared to OpenFF 2.1[9] and GAFF2, we find that the MACE-OFF24-SC prediction for methanol falls within the experimental error, while the classical force fields underpredict the magnitude of the hydration free energy. This trend has previously been studied in the context of empirical force fields and has been attributed to the assignment of partial 

Figure 5. Transition probability matrix between 16 replicas from the REMD simulation of phenol in water. 

**4932** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

**Journal of the American Chemical Society** 

**pubs.acs.org/JACS** 

Article 

coefficient, which additionally requires the calculation of a solvation free energy in a nonpolar solvent. This probes the ability of the model to describe accurately the intermolecular interactions between the solute and the nonpolar organic solvent, in this case, octanol. Although the greater conformational flexibility of the solvent makes convergence of the octanol leg of the thermodynamic cycle slightly more challenging, these calculations were still performed in reasonable computational time, requiring at most 48 h of wall time (see Section 2.2.4). We first confirmed that MACEOFF24-SC is capable of capturing the basic thermodynamic properties of liquid octanol, resulting in a density within 5% of the experimental value (Figure S4). 

In this section, we evaluate the accuracy of MACE-OFF24SC predictions on 10 octanol solvation free energies extracted from the MNSol database.[58] While MNSol does not provide experimental uncertainties, we adopt the best practice developed by the FreeSolv authors and assume an experimental error of 0.6 kcal/mol. With this threshold, all MACE-OFF24-SC predictions fall within the experimental error (Figure 6 and Section S2), indicating that the model is 

**==> picture [181 x 179] intentionally omitted <==**

Figure 6. Solvation free energies of a series of 10 small organic molecules in octanol. The shaded region represents a 0.6 kcal/mol deviation. 

indeed capable of successfully predicting these interactions. Here, we compare the GAFF2 force field equipped with the recently published ABCG2 charge model instead of the normal AM1-BCC, which has been tuned to improve the accuracy of hydration and transfer free energy calculations compared to the standard charge model.[57] Hence, this test represents an extremely stringent comparison for MACE-OFF24-SC, since the empirical force field has been directly optimized for the task. 

Similar to the hydration free energy results, we find MACEOFF24-SC has a moderately lower prediction error compared to GAFF2/ABCG2; however, both values fall below the presumed experimental error, again making further quantitative comparison difficult. 

**2.2.3. Log** _**P**_ **Calculations for Drug-like Molecules.** In order to probe the boundaries of the model’s capabilities, we performed full solvation free energy calculations, in both water and octanol solvents, on a selection of 16 drug-like compounds from the CHEMBL database for which an experimental log _P_ value is available via retention time-based UPLC/MS 

chromatographic analysis. All compounds satisfy Lipinski’s Rule of 5 criteria[59] and are representative of the chemical complexity and flexibility of molecules typical of a medicinal chemistry campaign. Structures of the compounds are shown in Section S9. 

Using the same alchemical free energy methodology as for the earlier calculations, we calculated log _P_ as the difference between the water and octanol free energy legs 

**==> picture [229 x 25] intentionally omitted <==**

Figure 7 compares both MACE-OFF24-SC and OpenFF 2.1 with experimental measurements. Here, for the first time, we see MACE-OFF24-SC significantly outperforming the classical force fields, with an RMSE of 0.45 log units, compared to 4.02 for OpenFF 2.1 and 8.64 for GAFF2/ABCG2. This result is extremely encouraging, suggesting that the model is capable of transferring nonbonded interactions learned from the training set to highly functionalized, conformationally complex molecules. This result validates our hypothesis that machine learning force fields, which have learned these interactions from first-principles, may show superior transferability to drug-like chemical space, compared to the explicit parametrization approach used to fit empirical force fields.[60] Given the accurate predictions of GAFF2/ABCG2 on small molecule octanol solvation free energies, this suggests that the error arises in the transferability of the parameters from small molecules on which the nonbonded parameters are fitted to larger, more complex, and conformationally flexible systems. These results are in qualitative agreement with other recently published benchmarking studies, which show that, while ABCG2 charges lead to improved performance on hydration free energies of small molecules, they fail to outperform AM1BCC charges on closely related protein−ligand binding free energy calculations, further highlighting that parameter transferability remains a significant challenge for classical small molecule force fields.[61] 

**2.2.4. Computational Performance.** Free energy calculations, even with classical force fields, are known to be computationally expensive. Hydration free energy calculations ameliorate the sampling problem for the purposes of benchmarking since the phase space perturbations are small and expected to converge rapidly compared to protein−ligand binding free energies. Running free energy calculations with machine learned potentials raises the issue of whether converged results can be obtained within a reasonable wall time. 

Here, all calculations were performed on single nodes, containing either 8 NVIDIA A100 or 8 NVIDIA L40S GPUs. For both machine types, we achieved aggregated sampling of around 8 ns/day across 16 replicas, corresponding to approximately 500 replica exchange iterations of 1 ps each per day. Most hydration free energies converged within this time, while some were extended to run for 1 ns per replica, requiring 48 h of wall time. MNSol octanol solvation free energies were all run for 1 ns per replica to account for the additional conformational sampling requirement. 

Owing to the size of the solutes in the log _P_ calculations, these calculations took longer to converge, with the average hydration and octanol leg requiring 4 and 7 days of wall time, respectively. 

**4933** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

**Journal of the American Chemical Society** 

**pubs.acs.org/JACS** 

Article 

**==> picture [500 x 191] intentionally omitted <==**

Figure 7. Experimental log _P_ for CHEMBL compounds compared to OpenFF 2.1, MACE-OFF24-SC, and GAFF2/ABCG2. *Experimental value recorded as >5.4, so quantitative comparison is not possible. 

## **3. CONCLUSIONS** 

We have introduced a modified version of the MACE-OFF24 transferable organic MLPs that enables theoretically rigorous condensed phase alchemical free energy simulations with firstprinciples based MLPs. A dual approach of softcore repulsion and _λ_ -dependent two-body interactions enables numerically well-behaved simulations of weakly interacting atoms, directly analogous to softcore formulations of classical force fields. Our method enables access to quantities directly relevant to drug discovery at _ab initio_ quality. 

We tested the accuracy of our approach by calculating free energies of solvation, in water and octanol solvents, for a range of small organic molecules from the FreeSolv and MNSol databases.[54][,][58] Our approach achieves excellent accuracy on a wide range of functional groups, improving on state-of-the-art empirical force field accuracy and approaching the experimental errors of the data sets. 

As a final stringent test of the accuracy of the model, we computed log _P_ values for a series of compounds from the CHEMBL database. These compounds are drug-like in terms of size, complexity, and functionality, are expected to be neutral at physiological pH and have experimental log _P_ values. On this benchmark, we report an order of magnitude improvement in RMSE compared to OpenFF 2.1, a state-ofthe-art classical force field, and GAFF2/ABCG2, which utilizes a recently developed charge partitioning scheme.[57] This performance is highly encouraging for future applications of machine learning force fields in drug discovery and represents a significant step toward replacing labor and resource-intensive chemical synthesis and experiment with fast and accurate molecular simulation. 

Equally importantly, we demonstrate that convergence of the free energy is feasible within a reasonable simulation time, even for absolute solvation free energy calculations in octanol, which present additional sampling challenges compared with aqueous free energy calculations. Since this work was performed, optimized computational kernels such as NVIDIA’s cuEquivariance have been released _[1]_ , which we expect to significantly improve the throughput of these calculations. 

As previously noted for MACE-OFF models, the lack of an explicit long-range contribution limits the chemical space in 

which the model is expected to be accurate. This has been addressed by recent transferable MLPs, including AIMNet2[27] and FeNNix-Bio1,[47] which include an explicit Coulomb term. The latter employs the alchemical methods developed in this work and uses solvation and protein−ligand binding free energies to benchmark the accuracy of the model for condensed phase systems. 

We believe soft-core-equipped machine learning potentials will become an increasingly exploited avenue for accurate and efficient calculation of free energies. As well as being an important quantity in force field benchmarking, free energies represent key optimization quantities in drug discovery, where − they can give direct access to protein ligand binding affinities. Hence, accurate and efficient computational methods are an important tool when rigorous and accurate predictions are required. 

## **4. METHODS** 

## **4.1. MACE-OFF24-SC Training** 

In previous work, it was found that the use of equivariant features ( _L_ max > 0) in the tensor product significantly increased the accuracy of intermolecular force predictions compared to the invariant MACEOFF23 model.[25] All simulations in this work were performed using a model with _L_ max = 1, 128 channels, and a layerwise cutoff of 6 Å. These hyperparameters were adopted from the MACE-OFF24(M) model, given its ability to accurately describe the properties of condensed phase systems.[25] 

MACE-OFF24-SC was trained on the same neutral-only filtering of the SPICE2 data set that we previously reported, which included, crucially, the newly added protein−ligand and solvated PubChem data sets, which provided extensive sampling of the intermolecular interactions required for accurate liquid phase free energy calculations.[62] 

## **4.2. Equilibrium Free Energy Calculations** 

Equilibrium free energy calculations were performed using OpenMM, and made use of modified versions of the openmmtools, openmm-ml, and openmm-torch libraries to perform Hamiltonian replica exchange and interface MACE with OpenMM.[8][,][63][−][67] This approach enabled interpolation between the coupled and decoupled end states via a _λ_ -dependent Hamiltonian. _[2]_ 

Since MACE predicts total intermolecular interactions without distinguishing between repulsive exchange and attractive Coulomb and dispersion terms, solvent−solute interactions are switched off 

**4934** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

**pubs.acs.org/JACS** 

Article 

## **Journal of the American Chemical Society** 

using a single transformation, parametrized by the alchemical parameter _λ_ . We adopt a direct decoupling approach in which the organic molecule is decoupled from the surrounding solvent, while all other interactions are unmodified. This results in a decoupled end state equivalent to a separated solvent box and small molecule in vacuum. 

Initial solvated structures were generated with pdbfixer, using a rhombic dodecahedral box and a padding of 1.3 nm from solute to box edge, ensuring the minimum image convention is correctly applied for the 12 Å receptive field of MACE. Structures were energy minimized using the L-BFGS algorithm, and subsequently equilibrated in the NPT ensemble for 50 ps. The last frame was used to seed the replica exchange calculations. 

Replicas were then propagated in the NPT ensemble under Langevin dynamics with an integration time step of 1 fs and a friction coefficient of 1/ps. Pressure was maintained at 1 atm with a Monte Carlo barostat, as implemented in OpenMM. 

The phase space perturbation was spanned in all cases by 16 replicas, which resulted in at least a tridiagonal overlap in all cases. Hamiltonian replica exchanges between all replicas were attempted every 1000 steps of dynamics (1 ps). It was found that 1 ns of sampling per replica was sufficient to converge the free energy estimates in all cases. A full sample input file is provided in Section S7. 

Replica exchange calculations were performed using the ReplicaExchangeSampler class from openmmtools. Replicas were assigned a single MPI rank, and two MPI ranks were mapped to each GPU, enabling full utilization of the GPU’s compute bandwidth, thus slightly increasing throughput compared to running the replicas in multiple waves. 

Automated equilibration detection and trajectory subsampling were performed following Chodera et al., as implemented in pymbar, to ensure only decorrelated samples were used to solve the MBAR equations.[42][,][68] 

## **4.3. Empirical Force Field Solvation Free Energies** 

GAFF solvation free energies and standard errors were taken from the FreeSolv Data set.[54] OpenFF values were calculated using OpenFF 2.1.0 via the Absolv code, using an equilibrium free energy protocol _[3]_ . An example script can be found in Section S8. 

GAFF2/ABCG2 calculations were performed with GROMACS 2024.1. Parameters were assigned with an Antechamber. Systems were energy minimized for a maximum of 50,000 steps and subsequently equilibrated for 1 ns in the NVT ensemble and the NPT ensemble for 1 ns. Eight and 16 windows were used to annihilate the Coulomb and van der Waals interactions, respectively. Each alchemical window was run for 500 ps. An example MDP file for the production free energy calculations is included in Section S11. Free energy estimates were calculated using gmx bar. 

- CHEMBL compounds (S9); octanol density (S10); example GROMACS MDP file (S11) (PDF) SMILES (CSV) 

## ■ **[AUTHOR][INFORMATION]** 

## **Corresponding Author** 

- J. Harry Moore − _Engineering Laboratory, University of Cambridge, Cambridge CB2 1PZ, U.K.; Ångström AI, San Francisco, California 94107, United States;_ orcid.org/ 0000-0001-5116-3027; Email: jhm72@cam.ac.uk 

## **Authors** 

- Daniel J. Cole − _School of Natural and Environmental Sciences, Newcastle University, Newcastle upon Tyne NE1 7RU, U.K._ 

- Gábor Csányi − _Engineering Laboratory, University of Cambridge, Cambridge CB2 1PZ, U.K.; Ångström AI, San Francisco, California 94107, United States;_ orcid.org/ 0000-0002-8180-2034 

Complete contact information is available at: https://pubs.acs.org/10.1021/jacs.5c10940 

## **Notes** 

The authors declare the following competing financial interest(s): GC has equity stake in Symmetric Group LLP. GC and JHM have equity stake in Ångstrom AI Inc. Both companies are engaged in the application of machine learning to material and molecular simulation. 

## ■ **[ACKNOWLEDGMENTS]** 

J.H.M. acknowledges support from an AstraZeneca NonClinical PhD studentship, and thanks Prof. Ola Engkvist, Dr Marco Klähn, and Dr Graeme Robb for their helpful discussions. D.J.C. acknowledges support from a UKRI Future Leaders Fellowship (grant MR/T019654/1). We acknowledge computational resources provided by the Cambridge Service for Data-Driven Discovery (CSD3), the AstraZeneca Scientific Computing Platform (SCP), the U.K. national high-performance computing service, ARCHER2, for which access was obtained via the UKCP consortium and the EPSRC grant ref EP/P022561/1, and Ångström AI. 

## ■ **[ADDITIONAL][NOTES]** 

## ■ **[ASSOCIATED][CONTENT]** 

## **Data Availability Statement** 

An example script to reproduce the replica exchange calculations is provided in the SI. The mace-md package used to run the simulations is available at https://github.com/ jharrymoore/mace-md/tree/master. Calculated solvation free energy values for all force fields are available in the Supporting Information. 

## * **sı Supporting Information** 

The Supporting Information is available free of charge at https://pubs.acs.org/doi/10.1021/jacs.5c10940. 

- Training and test set energy and force errors (S1); octanol solvation free energy results (S2); FreeSolv hydration free energy results (S3); switching points (S4); example of nonequilibrium switching (S5); free energy convergence plots (S6); sample replica exchange input file (S7); example Absolv run script (S8); 

> _1_ https://github.com/NVIDIA/cuEquivariance 

> _2_ https://github.com/jharrymoore/mace-md 

> _3_ https://github.com/SimonBoothroyd/absolv/ 

## ■ **[REFERENCES]** 

(1) Cournia, Z.; Allen, B.; Sherman, W. Relative Binding Free Energy Calculations in Drug Discovery: Recent Advances and Practical Considerations. _J. Chem. Inf. Model._ 2017, _57_ , 2911−2937. (2) Schindler, C. E. M. H.; Baumann, A.; Blum, D.; Bose, D.; Buchstaller, H.-P.; Burgdorf, L.; Cappel, D.; Chekler, E.; Czodrowski, P.; Dorsch, D.; Eguida, M. K. I.; Follows, B.; Fuchß, T.; Gradler, U.; Gunera, J.; Johnson, T.; Lebrun, C. J.; Karra, S.; Klein, M.; Knehans, T.; Koetzner, L.; Krier, M.; Leiendecker, M.; Leuthner, B.; Li, L.; Mochalkin, I.; Musil, D.; Neagu, C.; Rippmann, F.; Schiemann, K.; Schulz, R.; Steinbrecher, T.; Tanzer, E.-M.; Lopez, A. U.; Follis, A. V.; Wegener, A.; Kuhn, D. Large-Scale Assessment of Binding Free Energy Calculations in Active Drug Discovery Projects. _J. Chem. Inf. Model._ 2020, _60_ , 5457−5474. 

(3) Wang, L.; Wu, Y.; Deng, Y.; Kim, B.; Pierce, L.; Krilov, G.; Lupyan, D.; Robinson, S.; Dahlgren, M. K.; Greenwood, J.; Romero, 

**4935** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

**Journal of the American Chemical Society** 

**pubs.acs.org/JACS** 

Article 

D. L.; Masse, C.; Knight, J. L.; Steinbrecher, T.; Beuming, T.; Damm, W.; Harder, E.; Sherman, W.; Brewer, M.; Wester, R.; Murcko, M.; Frye, L.; Farid, R.; Lin, T.; Mobley, D. L.; Jorgensen, W. L.; Berne, B. J.; Friesner, R. A.; Abel, R. Accurate and Reliable Prediction of Relative Ligand Binding Potency in Prospective Drug Discovery by Way of a Modern Free-Energy Calculation Protocol and Force Field. _J. Am. Chem. Soc._ 2015, _137_ , 2695−2703. 

(4) Gapsys, V.; Pérez-Benito, L.; Aldeghi, M.; Seeliger, D.; Van Vlijmen, H.; Tresadern, G.; De Groot, B. L. Large Scale Relative Protein Ligand Binding Affinities Using Non-Equilibrium Alchemy. _Chem. Sci._ 2020, _11_ , 1140−1152. 

(5) Loeffler, H. H.; Bosisio, S.; Matos, G. D. R.; Suh, D.; Roux, B.; Mobley, D. L.; Michel, J. Reproducibility of Free Energy Calculations across Different Molecular Simulation Software Packages. _J. Chem. Theory Comput._ 2018, _14_ , 5567−5582. 

(6) Abraham, N. S.; Shirts, M. R. Statistical Mechanical Approximations to More Efficiently Determine Polymorph Free Energy Differences for Small Organic Molecules. _J. Chem. Theory Comput._ 2020, _16_ , 6503−6512. 

(7) Gapsys, V.; Michielssens, S.; Seeliger, D.; de Groot, B. L. Accurate and Rigorous Prediction of the Changes in Protein Free Energies in a Large-Scale Mutation Scan. _Angew. Chem., Int. Ed._ 2016, _55_ , 7364−7368. 

(8) Eastman, P.; Galvelis, R.; Peláez, R. P.; Abreu, C. R. A.; Farr, S. E.; Gallicchio, E.; Gorenko, A.; Henry, M. M.; Hu, F.; Huang, J.; Krämer, A.; Michel, J.; Mitchell, J. A.; Pande, V. S.; Rodrigues, J. P.; Rodriguez-Guerra, J.; Simmonett, A. C.; Swails, J.; Zhang, I.; Chodera, J. D.; De Fabritiis, G.; Markland, T. E. OpenMM 8: Molecular Dynamics Simulation with Machine Learning Potentials. _J. Phys. Chem. B_ 2023, _128_ , 109−116. 

(9) Boothroyd, S.; Behara, P. K.; Madin, O. C.; Hahn, D. F.; Jang, H.; Gapsys, V.; Wagner, J. R.; Horton, J. T.; Dotson, D. L.; Thompson, M. W.; Maat, J.; Gokey, T.; Wang, L.-P.; Cole, D. J.; Gilson, M. K.; Chodera, J. D.; Bayly, C. I.; Shirts, M. R.; Mobley, D. L.; et al. Development and Benchmarking of Open Force Field 2.0.0: The Sage Small Molecule Force Field. _J. Chem. Theory Comput._ 2023, _19_ , 3251−3275. 

(10) Wang, J.; Wang, W.; Kollman, P. A.; Case, D. A. Automatic Atom Type and Bond Type Perception in Molecular Mechanical Calculations. _J. Mol. Graphics Modell._ 2006, _25_ , 247−260. 

(11) Chodera, J. D.; Mobley, D. L.; Shirts, M. R.; Dixon, R. W.; Branson, K.; Pande, V. S. Alchemical Free Energy Methods for Drug Discovery: Progress and Challenges. _Curr. Opin. Struct. Biol._ 2011, _21_ , 150−160. 

(12) Mey, A. S.; Allen, B. K.; Macdonald, H. E. B.; Chodera, J. D.; Hahn, D. F.; Kuhn, M.; Michel, J.; Mobley, D. L.; Naden, L. N.; Prasad, S.; Rizzi, A.; Scheen, J.; Shirts, M. R.; Tresadern, G.; Xu, H. Best Practices for Alchemical Free Energy Calculations [Article v1.0]. _Living J. Comput. Mol. Sci._ 2020, _2_ , No. 18378, DOI: 10.33011/ livecoms.2.1.18378. 

(13) Squire, D. R.; Hoover, W. G. Monte Carlo Simulation of Vacancies in Rare-Gas Crystals. _J. Chem. Phys._ 1969, _50_ , 701−706. (14) Mezei, M.; Beveridge, D. L. Free Energy Simulationsa. _Ann. N.Y. Acad. Sci._ 1986, _482_ , 1−23. 

(15) Beutler, T. C.; Mark, A. E.; Van Schaik, R. C.; Gerber, P. R.; Van Gunsteren, W. F. Avoiding Singularities and Numerical Instabilities in Free Energy Calculations Based on Molecular Simulations. _Chem. Phys. Lett._ 1994, _222_ , 529−539. 

(16) Steinbrecher, T.; Mobley, D. L.; Case, D. A. Nonlinear Scaling Schemes for Lennard-Jones Interactions in Free Energy Calculations. _J. Chem. Phys._ 2007, _127_ , No. 214108. 

(17) Shirts, M. R.; Pande, V. S. Solvation Free Energies of Amino Acid Side Chain Analogs for Common Molecular Mechanics Water Models. _J. Chem. Phys._ 2005, _122_ , No. 134508. 

(18) Gapsys, V.; Seeliger, D.; de Groot, B. L. New Soft-Core Potential Function for Molecular Dynamics Based Alchemical Free Energy Calculations. _J. Chem. Theory Comput._ 2012, _8_ , 2373−2382. (19) Lee, T.-S.; Lin, Z.; Allen, B. K.; Lin, C.; Radak, B. K.; Tao, Y.; Tsai, H.-C.; Sherman, W.; York, D. M. Improved Alchemical Free 

Energy Calculations with Optimized Smoothstep Softcore Potentials. _J. Chem. Theory Comput._ 2020, _16_ , 5512−5525. 

(20) Horton, J. T.; Boothroyd, S.; Behara, P. K.; Mobley, D. L.; Cole, D. J. A Transferable Double Exponential Potential for Condensed Phase Simulations of Small Molecules. _Digital Discovery_ 2023, _2_ , 1178−1187. 

(21) Harder, E.; Damm, W.; Maple, J.; Wu, C.; Reboul, M.; Xiang, J. Y.; Wang, L.; Lupyan, D.; Dahlgren, M. K.; Knight, J. L.; Kaus, J. W.; Cerutti, D. S.; Krilov, G.; Jorgensen, W. L.; Abel, R.; Friesner, R. A.; et al. OPLS3: A Force Field Providing Broad Coverage of Drug-like Small Molecules and Proteins. _J. Chem. Theory Comput._ 2016, _12_ , 281−296. 

(22) Abel, R.; Wang, L.; Harder, E. D.; Berne, B. J.; Friesner, R. A. Advancing Drug Discovery through Enhanced Free Energy Calculations. _Acc. Chem. Res._ 2017, _50_ , 1625−1632. 

(23) Horton, J. T.; Boothroyd, S.; Wagner, J.; Mitchell, J. A.; Gokey, T.; Dotson, D. L.; Behara, P. K.; Ramaswamy, V. K.; Mackey, M.; Chodera, J. D.; Anwar, J.; Mobley, D. L.; Cole, D. J. Open Force Field BespokeFit: Automating Bespoke Torsion Parametrization at Scale. _J. Chem. Inf. Model._ 2022, _62_ , 5622−5633. 

(24) Devereux, C.; Smith, J. S.; Huddleston, K. K.; Barros, K.; Zubatyuk, R.; Isayev, O.; Roitberg, A. E. Extending the Applicability of the ANI Deep Learning Molecular Potential to Sulfur and Halogens. _J. Chem. Theory Comput_ 2020, _16_ , 4192−4202. 

(25) Kovács, D. P.; Moore, J. H.; Browning, N. J.; Batatia, I.; Horton, J. T.; Pu, Y.; Kapil, V.; Witt, W. C.; Magdau, I.-B.; Cole, D. J.; Csányi, G. MACE-OFF: Short-Range Transferable Machine Learning Force Fields for Organic Molecules. _J. Am. Chem. Soc._ 2025, _147_ , 17598−17611. 

(26) Batatia, I.; Benner, P.; Chiang, Y.; Elena, A. M.; Kovács, D. P.; Riebesell, J.; Advincula, X. R.; Asta, M.; Avaylon, M.; Baldwin, W. J.; Berger, F.; Bernstein, N.; Bhowmik, A.; Blau, S. M.; Carare, V.; Darby, J. P.; De, S.; Della Pia, F.; Deringer, V. L.; Elijosius, R.; El-Machachi, Z.; Falcioni, F.; Fako, E.; Ferrari, A. C.; Genreith-Schriever, A.; George, J.; Goodall, R. E. A.; Grey, C. P.; Grigorev, P.; Han, S.; Handley, W.; Heenen, H. H.; Hermansson, K.; Holm, C.; Jaafar, J.; Hofmann, S.; Jakob, K. S.; Jung, H.; Kapil, V.; Kaplan, A. D.; Karimitari, N.; Kermode, J. R.; Kroupa, N.; Kullgren, J.; Kuner, M. C.; Kuryla, D.; Liepuoniute, G.; Margraf, J. T.; Magdau, I.-B.; Michaelides, A.; Moore, J. H.; Naik, A. A.; Niblett, S. P.; Norwood, S. W.; O’Neill, N.; Ortner, C.; Persson, K. A.; Reuter, K.; Rosen, A. S.; Schaaf, L. L.; Schran, C.; Shi, B. X.; Sivonxay, E.; Stenczel, T. K.; Svahn, V.; Sutton, C.; Swinburne, T. D.; Tilly, J.; van der Oord, C.; Varga-Umbrich, E.; Vegge, T.; Vondrák, M.; Wang, Y.; Witt, W. C.; Zills, F.; Csányi, G. A Foundation Model for Atomistic Materials Chemistry 2024, arXiv:2401.00096v3. arXiv.org e-Print archive. https://doi.org/10.48550/arXiv.2401.00096. 

(27) Anstine, D.; Zubatyuk, R.; Isayev, O. AIMNet2: A Neural Network Potential to Meet your Neutral, Charged, Organic, and Elemental-Organic Needs. _Chem. Sci._ 2025, _16_ , 10228−10244, DOI: 10.1039/D4SC08572H. 

(28) Deng, B.; Zhong, P.; Jun, K.; Riebesell, J.; Han, K.; Bartel, C. J.; Ceder, G. CHGNet as a Pretrained Universal Neural Network Potential for Charge-Informed Atomistic Modelling. _Nat. Mach. Intell._ 2023, _5_ , 1031−1041. 

(29) Unke, O. T.; Meuwly, M. PhysNet: A Neural Network for Predicting Energies, Forces, Dipole Moments, and Partial Charges. _J. Chem. Theory Comput._ 2019, _15_ , 3678−3693. 

(30) Behler, J.; Parrinello, M. Generalized neural-network representation of high-dimensional potential-energy surfaces. _Phys. Rev. Lett._ 2007, _98_ , No. 146401, DOI: 10.1103/PhysRevLett.98.146401. 

(31) Batatia, I.; Batzner, S.; Kovács, D. P.; Musaelian, A.; Simm, G. N. C.; Drautz, R.; Ortner, C.; Kozinsky, B.; Csányi, G. The Design Space of E(3)-Equivariant Atom-Centered Interatomic Potentials. _Nat. Mach. Intell._ 2025, _7_ , 56−67, DOI: 10.1038/s42256-024-00956x. 

**4936** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

**Journal of the American Chemical Society** 

**pubs.acs.org/JACS** 

Article 

(32) Cole, D. J.; Mones, L.; Csányi, G. A Machine Learning Based Intramolecular Potential for a Flexible Organic Molecule. _Faraday Discuss._ 2020, _224_ , 247−264. 

(33) Rufa, D. A.; Macdonald, H. E. B.; Fass, J.; Wieder, M.; Grinaway, P. B.; Roitberg, A. E.; Isayev, O.; Chodera, J. D. Towards Chemical Accuracy for Alchemical Free Energy Calculations with Hybrid Physics-Based Machine Learning/Molecular Mechanics Potentials _BioRxiv_ 2020. 

(34) Karwounopoulos, J.; Wu, Z.; Tkaczyk, S.; Wang, S.; Baskerville, A.; Ranasinghe, K.; Langer, T.; Wood, G.; Wieder, M.; Boresch, S. Insights and Challenges in Correcting Force Field Based Solvation Free Energies Using A Neural Network Potential. _J. Phys. Chem. B_ 2024, _128_ , 6693−6703, DOI: 10.1021/acs.jpcb.4c01417. 

(35) Zinovjev, K. Electrostatic Embedding of Machine Learning Potentials. _J. Chem. Theory Comput._ 2023, _19_ , 1888−1897, DOI: 10.1021/acs.jctc.2c00914. 

(36) Morado, J.; Zinovjev, K.; Hedges, L.; Cole, D.; Michel, J. Enhancing electrostatic embedding for ML/MM free energy calculations. _J. Chem. Theory Comput._ 2025, _21_ , 11805−11819, DOI: 10.1021/acs.jctc.5c01464. 

(37) Pultar, F.; Thurlemann, M.; Gordiy, I.; Doloszeski, E.; Riniker, S. Neural Network Potential with Multiresolution Approach Enables Accurate Prediction of Reaction Free Energies in Solution. _J. Am. Chem. Soc._ 2025, _147_ , 6835−6856. 

(38) Zariquiey, F. S.; Galvelis, R.; Gallicchio, E.; Chodera, J. D.; Markland, T. E.; De Fabritiis, G. Enhancing Protein-Ligand Binding Affinity Predictions Using Neural Network Potentials. _J. Chem. Inf. Model._ 2024, _64_ , 1481−1485. 

(39) Wu, J. Z.; Azimi, S.; Khuttan, S.; Deng, N.; Gallicchio, E. Alchemical Transfer Approach to Absolute Binding Free Energy Estimation. _J. Chem. Theory Comput._ 2021, _17_ , 3309−3319. 

(40) Chen, L.; Wu, Y.; Wu, C.; Silveira, A.; Sherman, W.; Xu, H.; Gallicchio, E. Performance and Analysis of the Alchemical Transfer Method for Binding-Free-Energy Predictions of Diverse Ligands. _J. Chem. Inf. Model._ 2024, _64_ , 250−264. 

(41) Lu, C.; Wu, C.; Ghoreishi, D.; Chen, W.; Wang, L.; Damm, W.; Ross, G. A.; Dahlgren, M. K.; Russell, E.; Von Bargen, C. D.; Abel, R.; Friesner, R. A.; Harder, E. D. OPLS4: Improving Force Field Accuracy on Challenging Regimes of Chemical Space. _J. Chem. Theory Comput._ 2021, _17_ , 4291−4300. 

(42) Shirts, M. R.; Chodera, J. D. Statistically Optimal Analysis of Samples from Multiple Equilibrium States. _J. Chem. Phys._ 2008, _129_ , No. 124105. 

(43) Seeliger, D.; de Groot, B. L. Protein Thermostability Calculations Using Alchemical Free Energy Simulations. _Biophys. J._ 2010, _98_ , 2309−2316. 

(44) Gapsys, V.; Michielssens, S.; Seeliger, D.; de Groot, B. L. pmx: Automated protein structure and topology generation for alchemical perturbations. _J. Comput. Chem._ 2015, _36_ , 348−354. 

(45) Eastman, P.; Behara, P. K.; Dotson, D. L.; Galvelis, R.; Herr, J. E.; Horton, J. T.; Mao, Y.; Chodera, J. D.; Pritchard, B. P.; Wang, Y.; et al. Spice, a dataset of drug-like molecules and peptides for training machine learning potentials. _Sci. Data_ 2023, _10_ , No. 11. 

(46) Buelens, F. P.; Grubmuller, H. Linear-Scaling Soft-Core Scheme for Alchemical Free Energy Calculations. _J. Comput. Chem._ 2012, _33_ , 25−33. 

(47) Plé, T.; Adjoua, O.; Benali, A.; Posenitskiy, E.; Villot, C.; Lagardere, L.; Piquemal, J.-P. A Foundation Model for Accurate Atomistic Simulations in Drug Design _ChemRxiv_ 2025. 

(51) Nam, J.; Peng, J.; Gómez-Bombarelli, R. Interpolation and Differentiation of Alchemical Degrees of Freedom in Machine Learning Interatomic Potentials. _Nat. Commun._ 2025, _16_ , No. 4350, DOI: 10.1038/s41467-025-59543-2. 

(52) Gapsys, V.; Yildirim, A.; Aldeghi, M.; Khalak, Y.; van der Spoel, D.; de Groot, B. L. Accurate Absolute Free Energies for Ligand− Protein Binding Based on Non-Equilibrium Approaches. _Commun. Chem._ 2021, _4_ , No. 61. 

(53) Bennett, C. H. Efficient Estimation of Free Energy Differences from Monte Carlo Data. _J. Comput. Phys._ 1976, _22_ , 245−268. 

(54) Mobley, D. L.; Guthrie, J. P. FreeSolv: A Database of Experimental and Calculated Hydration Free Energies, with Input Files. _J. Comput.-Aided Mol. Des._ 2014, _28_ , 711−720. 

(55) Johnston, R. C.; Yao, K.; Kaplan, Z.; Chelliah, M.; Leswing, K.; Seekins, S.; Watts, S.; Calkins, D.; Elk, J. C.; Jerome, S. V.; Repasky, M. P.; Shelley, J. C. Epik: pKa and Protonation State Prediction through Machine Learning. _J. Chem. Theory Comput._ 2023, _19_ , 2380− 2388. 

(56) He, X.; Man, V. H.; Yang, W.; Lee, T.-S.; Wang, J. A Fast and High-Quality Charge Model for the next Generation General AMBER Force Field. _J. Chem. Phys._ 2020, _153_ , No. 114502. 

(57) He, X.; Man, V. H.; Yang, W.; Lee, T.-S.; Wang, J. ABCG2: A Milestone Charge Model for Accurate Solvation Free Energy Calculation. _J. Chem. Theory Comput._ 2025, _21_ , 3032−3043. 

(58) Marenich, A. V.; Kelly, C. P.; Thompson, J. D.; Hawkins, G. D.; Chambers, C. C.; Giesen, D. J.; Winget, P.; Cramer, C. J.; Truhlar, D. G. _Minnesota Solvation Database_ , version 2012; University of Minnesota 2020. 

(59) Lipinski, C. A. Lead- and Drug-like Compounds: The Rule-ofFive Revolution. _Drug Discovery Today: Technol._ 2004, _1_ , 337−341. 

(60) Hagler, A. T. Force Field Development Phase II: Relaxation of Physics-Based Criteria··· or Inclusion of More Rigorous Physics into the Representation of Molecular Energetics. _J. Comput.-Aided Mol. Des._ 2019, _33_ , 205−264. 

(61) Behera, S.; Gapsys, V.; De Groot, B. Evaluation of the ABCG2 Charge Model in Protein-Ligand Binding Affinity Calculations _ChemRxiv_ 2025. 

(62) Eastman, P.; Behara, P. K.; Dotson, D.; Galvelis, R.; Herr, J.; Horton, J.; Mao, Y.; Chodera, J.; Pritchard, B.; Wang, Y.; De Fabritiis, G.; Markland, T. SPICE 2.0.1. 2024. 

(63) Chodera, J. D.; Shirts, M. R. Replica Exchange and Expanded Ensemble Simulations as Gibbs Sampling: Simple Improvements for Enhanced Mixing. _J. Chem. Phys._ 2011, _135_ , No. 194110. 

(64) Eastman, P.; Pande, V. S. Constant Constraint Matrix Approximation: A Robust, Parallelizable Constraint Method for Molecular Simulations. _J. Chem. Theory Comput._ 2010, _6_ , 434−437. 

(65) Eastman, P.; Pande, V. S. Efficient Nonbonded Interactions for Molecular Dynamics on a Graphics Processing Unit. _J. Comput. Chem._ 2010, _31_ , 1268−1272. 

(66) Eastman, P.; Pande, V. OpenMM: A Hardware-Independent Framework for Molecular Simulations. _Comput. Sci. Eng._ 2010, _12_ , 34−39. 

(67) Friedrichs, M. S.; Eastman, P.; Vaidyanathan, V.; Houston, M.; Legrand, S.; Beberg, A. L.; Ensign, D. L.; Bruns, C. M.; Pande, V. S. Accelerating Molecular Dynamic Simulation on Graphics Processing Units. _J. Comput. Chem._ 2009, _30_ , 864−872. 

(68) Chodera, J. D. A. Simple Method for Automated Equilibration Detection in Molecular Simulations. _J. Chem. Theory Comput._ 2016, _12_ , 1799−1805. 

(48) Batatia, I.; Kovacs, D. P.; Simm, G. N. C.; Ortner, C.; Csanyi, G. In _MACE: Higher Order Equivariant Message Passing Neural Networks for Fast and Accurate Force Fields_ , Advances in Neural Information Processing Systems; Oh, A. H.; Agarwal, A.; Belgrave, D.; Cho, K., Eds.; NIPS, 2022. 

(49) Wigner, E. _Group Theory: and Its Application to the Quantum Mechanics of Atomic Spectra_ ; Elsevier, 2012; Vol. _5_ . 

(50) Dusson, G.; Bachmayr, M.; Csányi, G.; Drautz, R.; Etter, S.; van der Oord, C.; Ortner, C. Atomic cluster expansion: Completeness, efficiency and stability. _J. Comput. Phys._ 2022, _454_ , No. 110946. 

**4937** 

https://doi.org/10.1021/jacs.5c10940 _J. Am. Chem. Soc._ 2026, 148, 4928−4937 

