

### 224313_1_5.0296997

## Methods

The study investigates the accuracy of density functional theory (DFT) forces in molecular datasets, focusing on the presence of nonzero net forces as indicators of numerical errors. The methodological approach involves several key components:

1. **Datasets Analyzed**: The research examines multiple molecular datasets, including SPICE, Transition1x, ANI-1x, ANI-1xbb, AIMNet2, QCML, and OMol25. These datasets are characterized by their size, level of theory, and the DFT codes used for calculations.

2. **DFT Calculations**: The study utilizes DFT to compute forces, with a focus on identifying errors in force components. The datasets employ various exchange-correlation functionals and basis sets, with calculations performed using different versions of DFT software such as ORCA, Gaussian, Psi4, and FHI-aims.

3. **Net Force Analysis**: The presence of nonzero net forces is used as a diagnostic tool to identify potential errors in DFT calculations. The net force is calculated by summing the force components on all atoms in each Cartesian direction, which should ideally be zero in the absence of external fields.

4. **Recomputation of Forces**: To quantify errors in individual force components, the study recomputes forces using more reliable DFT settings. This involves using the same DFT functional and basis set but with improved computational settings, such as disabling the RIJCOSX approximation and using tighter DFT grids (`DEFGRID3` keyword in ORCA).

5. **Error Quantification**: The discrepancies between original and recomputed force components are quantified by comparing random samples of 1000 configurations from each dataset. The root mean square deviation (RMSD) of force components is calculated to assess the magnitude of errors.

6. **Computational Settings**: The study identifies optimal computational settings to minimize errors, including the use of ORCA 6.0.1 with `DEFGRID3` grid settings and without the RIJCOSX approximation. For Psi4, denser spherical and radial DFT grids are used to reduce net forces.

7. **Comparison Across Software**: The study compares DFT forces computed with different software packages, ensuring consistency by using converged settings. This includes comparisons between ORCA and Psi4, as well as across different versions of the same software.

8. **Supplementary Analysis**: Additional analyses are conducted on subsets of datasets and periodic systems to further explore the impact of computational settings on net forces and force discrepancies.

This comprehensive methodological framework allows the authors to systematically assess the accuracy of DFT forces in molecular datasets and provide guidelines for improving the quality of DFT data used in training machine learning interatomic potentials (MLIPs).

### 2602.19411v1

## Methods

### Core Methodological Approaches
The research paper introduces MACE-POLAR-1, a machine learning model designed to accurately model long-range electrostatic interactions in molecular chemistry. The model extends the MACE architecture by incorporating explicit long-range interactions through a non-self-consistent field formalism. This approach updates learnable charge and spin densities via polarisable iterations and equilibrates global charge using learnable Fukui functions. The model is trained to handle variable charge and spin states, respond to external fields, and provide interpretable spin-resolved charge densities.

### Model Architecture
1. **Local Features Prediction**: The model uses MACE layers to predict local node features, capturing semi-local geometry and chemistry.
2. **Spin-Charge Density**: Introduces a learnable spin-resolved charge density as a central non-local feature, expanded using atomic multipoles and Gaussian type orbitals.
3. **Field Updates**: Performs long-range polarisable field updates to capture polarisation effects and long-range charge transfer.
4. **Fukui Equilibration**: Uses learnable Fukui functions to equilibrate charges, ensuring the correct total charge and spin.
5. **Energy Decomposition**: The total energy is decomposed into short-range, electrostatic, and non-local contributions, with explicit treatment of long-range interactions.

### Tools and Computational Framework
- **MACE Architecture**: Utilizes the MACE framework for message-passing neural networks to model local interactions.
- **Gaussian Type Orbitals (GTOs)**: Used for expanding the spin-charge density and computing electrostatic interactions.
- **Multilayer Perceptron (MLP)**: Employed for nonlinear transformations in the model, particularly in updating spin-charge densities.

### Datasets
- **OMol25 Dataset**: The model is trained on the OMol25 dataset, which includes 100 million hybrid DFT calculations across diverse molecular structures.
- **Benchmark Datasets**: The model's performance is evaluated on various benchmarks, including thermochemistry, reaction barriers, non-covalent interactions, protein-ligand interactions, and molecular crystals.

### Experimental Framework
- **Training Strategy**: Models were trained using distributed training across 64 NVIDIA H200 GPUs, with hyper-parameters tuned for different model variants.
- **Benchmarking**: The model's accuracy is assessed against state-of-the-art methods on a comprehensive suite of benchmarks, including static single-point benchmarks and dynamic simulations.
- **External Field Response**: The model's ability to extrapolate to external fields is tested by computing molecular dipoles and polarisabilities through finite differences of the total energy.

### Theoretical Framework
- **Electrostatic Energy Computation**: The model computes electrostatic energy using a Gaussian smearing scheme, with separate implementations for real-space and periodic systems.
- **Fukui Functions and Conceptual DFT**: The Fukui charge equilibration scheme is connected to conceptual density functional theory, providing a theoretical basis for the model's charge distribution approach.

This methodological framework enables MACE-POLAR-1 to achieve high accuracy in modeling complex molecular systems, particularly those involving long-range electrostatic interactions.

### 2604.08143v1

## Methods

### A. Equivariant Message Passing Neural Networks (EMPNNs)

The study introduces an equivariant message-passing graph neural network (mMACE) to model magnetic interactions in materials. The core methodology involves the use of Equivariant Message Passing Neural Networks (EMPNNs) to parameterize potential energy surfaces, incorporating atomic magnetic moments as explicit features. The atomic structure is represented as a graph where nodes correspond to atoms and edges define atomic neighborhood relations.

1. **Graph Construction**: Each node in the graph is characterized by its atomic position, magnetic moment, atomic number, and hidden features. The atomic neighborhood is defined by a cutoff radius.

2. **Message Passing**: At each layer of the EMPNN, messages are constructed by aggregating information from neighboring atoms. These messages are then transformed into new feature vectors through learnable update functions.

3. **Energy Calculation**: After several layers of message passing, learnable readout functions map node states to interaction site energies. The total potential energy is obtained by summing contributions from all sites, and forces are derived as negative gradients with respect to atomic positions.

4. **Magnetic Forces**: The gradients with respect to atomic magnetic moments provide magnetic forces, enabling optimization of magnetic degrees of freedom for equilibrated total energy.

### B. Equivariance and Spin-Orbit Coupling

The model incorporates O(3)-equivariant architectures to ensure that hidden features and outputs transform consistently under rotations. The symmetry considerations allow for the inclusion of spin-orbit coupling (SOC) effects, which are crucial for capturing magnetocrystalline anisotropy.

1. **Symmetry Considerations**: The model can handle both coupled and independent rotations of atomic positions and magnetic moments, allowing for the inclusion or exclusion of SOC effects.

2. **Model Architecture**: The mMACE architecture is designed to be equivariant under joint rotations of positions and magnetic moments, capturing SOC effects naturally.

### C. Model Architecture

The mMACE architecture builds on the MACE framework, with modifications to include magnetic moments as explicit degrees of freedom.

1. **Node Initialization**: Initial node states include atomic positions, magnetic moments, atomic numbers, and hidden features initialized as learnable embeddings.

2. **Feature Embedding**: Information along edges is embedded using invariant bases and real spherical harmonics, incorporating spin magnitudes as additional invariant inputs.

3. **Message Construction**: Equivariant edge features are constructed through operations involving spherical harmonics and solid harmonics, ensuring smoothness in the limit of zero magnetic moment.

4. **Node Update and Energy Readout**: Node features are updated via residual connections, and atomic interaction energies are obtained through readout functions applied to invariant node features.

5. **One-body Magnetic Contribution**: A one-body magnetic moment contribution is introduced to ensure correct large volume limits, fitted using Chebyshev polynomial expansions.

### D. Training and Fine-tuning

The model is trained on large foundational datasets and fine-tuned for specific magnetic systems.

1. **Pretraining**: mMACE models are pretrained on datasets like MATPES and MP-ALOE, achieving lower errors on magnetically active configurations.

2. **Fine-tuning**: Targeted fine-tuning is performed on specific systems like FeNi and Mn3Pt, demonstrating the model's ability to capture complex magnetic phenomena with minimal additional data.

### E. Experimental Validation

The model's performance is validated through various benchmarks and case studies.

1. **Benchmarks**: mMACE is benchmarked against DFT references on datasets like FeAl and CrN, showing significant error reductions in force and stress predictions.

2. **Case Studies**: The model is applied to study magnetocrystalline anisotropy and non-collinear magnetism, demonstrating its capability to capture SOC-induced energy differences and resolve complex magnetic states.

### F. Implementation Details

The implementation of mMACE is available for reproducing experiments, with details on parameter estimation and dataset generation provided in the appendices. The model's performance is analyzed in terms of computational efficiency and scalability.

### 2604.15394v1

## Methods

### Machine-learned Interatomic Potential (MLIP)
The study developed a machine-learned interatomic potential (MLIP) for the _β_-Ga2O3/4H-SiC heterostructure using the MACE framework. The training dataset included crystalline _β_-Ga2O3 and 4H-SiC, ideal Si-/O-terminated interfaces, and various amorphous phases. The dataset was generated using the universal potential MACE-MP-0b3 for efficient phase-space sampling. For crystalline structures, lattice constants were optimized, and configurations were generated by scaling the lattices and performing molecular dynamics (MD) simulations. For amorphous phases, random structures were generated and optimized. All structures were relabeled using density functional theory (DFT) to provide ground-truth energies and forces. The final MACE model was trained using a Huber loss function with specific parameters.

### DFT Calculation
Density functional theory (DFT) calculations were conducted using the Vienna Ab-Initio Simulation package with the Perdew–Burke–Ernzerhof exchange–correlation functional and the projector augmented-wave method. An energy cutoff of 600 eV was used, and the Brillouin zone was sampled using the Γ-point.

### Model Construction
A disorder-free interface model was constructed by stacking the O-terminated (2[−] 01) _β_-Ga2O3 surface onto the Si-terminated (001) 4H-SiC surface. Disordered interfaces were modeled by generating an amorphous SiO2 interlayer and subjecting the structure to a simulated melt-anneal process.

### Lattice Dynamics Calculation
The lattice dynamics (LD) method divided the system into three regions: a left semi-infinite _β_-Ga2O3 lead, a central device region with the interface, and a right semi-infinite 4H-SiC lead. The eigenvalue equation governed the dynamic behavior, and energy and momentum conservation were enforced to identify reflected and transmitted phonons. The total thermal boundary conductance (TBC) was calculated using the Landauer formula.

### Material Synthesis
The _β_-Ga2O3/4H-SiC heterojunction was synthesized via radio frequency magnetron sputtering on a Si-terminated 4H-SiC substrate. Different samples were prepared by varying the base pressure and temperature to control the interface structure. The deposition conditions were optimized to achieve atomically sharp interfaces.

### X-ray Diffraction
X-ray diffraction (XRD) measurements were performed to assess crystalline quality and film orientation. Rocking curves and φ-scans were used to evaluate the out-of-plane mosaic spread and in-plane crystallographic orientation relationship.

### Electron Microscopy
Cross-sectional transmission electron microscopy (TEM) specimens were prepared using a focused ion beam (FIB) system. High-angle annular dark-field scanning transmission electron microscopy (HAADF-STEM) images were acquired to analyze the interface regions.

### Atomic Force Microscopy
Surface topography was characterized using atomic force microscopy (AFM) in tapping mode.

### TDTR Measurement
Thermal properties were characterized using time-domain thermoreflectance (TDTR). A titanium-sapphire laser system was used, and the thermal response was modeled using a multilayer heat diffusion equation. The _β_-Ga2O3/4H-SiC interface was modeled as a 1 nm layer with minimal heat capacity. Measurements were performed at different frequencies to determine thermal conductivity and interface thermal conductance.

### 3731545.3731594

## Methods

The research paper "Optimizing Data Distribution and Kernel Performance for Efficient Training of Chemistry Foundation Models: A Case Study with MACE" employs a combination of methodological approaches, tools, datasets, and experimental frameworks to optimize the training of Chemistry Foundation Models (CFMs) using Graph Neural Networks (GNNs). The core methods are outlined as follows:

### 1. Data Distribution Optimization
- **Problem Formulation**: The distribution of 3D molecular graphs is formulated as a multi-objective bin packing problem. The objectives are to achieve balanced data distribution and minimize memory padding overhead.
- **Iterative Algorithm**: An efficient iterative algorithm is developed to create balanced batches. This algorithm sorts graphs by vertex count and distributes them across bins to minimize load imbalance and memory padding.
- **Implementation**: The algorithm is implemented by modifying PyTorch’s Distributed Sampler to become a batch sampler, determining batches at the beginning of each epoch.

### 2. Kernel Optimization
- **Symmetric Tensor Contraction**: Identified as a key computational kernel, symmetric tensor contraction is optimized to improve performance. This involves optimizing the tensor contraction and tensor product operations within the MACE architecture.
- **Kernel Fusion**: Combines multiple small operations into a single GPU kernel to reduce kernel launch overhead and improve memory access efficiency.
- **Exploiting Sparsity**: The sparsity of Clebsch-Gordan coefficients is exploited by pre-computing valid combinations and using lookup tables for fast access, reducing unnecessary computations.
- **Bandwidth Utilization**: Memory bandwidth is optimized through efficient thread layouts for coalesced access patterns and vectorized load/store operations.
- **Warp-Level Primitives and Loop Unrolling**: Utilizes warp-level primitives and loop unrolling to enhance parallel processing efficiency and reduce loop overhead.

### 3. Experimental Framework
- **Datasets**: A combined dataset of 2.65 million molecular graphs from eight different chemical systems is used. The dataset exhibits diversity in size, sparsity, and chemical composition.
- **Software and Hardware Configuration**: Experiments are conducted using PyTorch 2.3.1 and CUDA 12.2 on the NERSC Perlmutter system with NVIDIA A100 GPUs. The DistributedDataParallel (DDP) module is used for data distribution across GPUs.
- **Hyperparameters**: The learning rate is set to 0.005, with a batch size varying from 6 to 8 depending on system size. The Adam optimizer and an exponential moving average learning scheduler are used.

### 4. Evaluation
- **Ablation Studies**: Conducted to assess the individual impact of load balancing and kernel optimization on training performance.
- **Scaling Experiments**: Both strong and weak scaling experiments are performed to evaluate the performance improvements across different GPU counts and dataset sizes.
- **Performance Metrics**: Speedup is measured in terms of per-epoch execution time relative to the original MACE implementation.

These methods collectively aim to enhance the efficiency and scalability of training CFMs by addressing data distribution challenges and optimizing computational kernels.

### Thomas_2025_Nonlinearity_38_095024

## Methods

The research paper by Jack Thomas et al. introduces a methodological framework for incorporating long-range electrostatic effects into machine learning interatomic potentials. The core methodological approaches, tools, datasets, and experimental or theoretical frameworks used in the study are as follows:

### Methodological Approaches

1. **Mathematical Framework**: The study develops a mathematical framework to include long-range electrostatic effects in machine learning models of potential energy surfaces. This framework allows for charge equilibration while retaining the locality of atom-centered contributions.

2. **Body-Ordered Expansion**: The potential energy surface (PES) is decomposed into a sum of atom-centered site energy contributions, which are approximated using a body-ordered expansion. This approach ensures that the model can be systematically improved by increasing the body-order.

3. **Charge Equilibration Schemes**: The paper revisits classical electronegativity equalization methods and introduces a charge equilibration via neural network technique (CENT) to parameterize atomic electronegativities and hardness using machine learning.

4. **Self-Consistent Field Neural Network (SCFNN)**: The study justifies the use of SCFNN and similar approaches by introducing atom-centered features that describe the effective potential, which are then minimized to provide a self-consistent PES.

### Tools and Techniques

1. **Machine Learning Models**: The study employs machine learning models to parameterize the effective potential and electron density, using neural networks to learn from quantum mechanical calculations.

2. **Tight Binding Approximation**: The electronic structure models are approximated using a tight binding framework, which reduces the computational complexity by restricting the class of one-particle density operators.

3. **Polynomial Approximations**: Polynomial approximations are used for functions like the Fermi-Dirac distribution to facilitate the analysis and computation of the PES.

4. **Combes–Thomas Resolvent Estimate**: This mathematical tool is used to establish the exponential localization of observables, which is crucial for proving the locality of the energy contributions.

### Datasets

1. **Quantum Mechanical Calculations**: The study uses data from quantum mechanical calculations, specifically density functional theory (DFT) calculations, to extract total energy, electron density, and atomic features for training the machine learning models.

2. **Water Clusters**: Numerical experiments are conducted on a dataset of small clusters of water molecules, using DFT calculations to validate the proposed framework.

### Experimental Framework

1. **Numerical Experiments**: The study conducts numerical experiments to demonstrate the convergence of the proposed machine learning models with respect to the number of electric potential features per atom and the body-order of the functions.

2. **Parameterization of Energy and Density**: The energy and electron density are parameterized as body-ordered functions of atom-centered features, using elements from the MACE equivariant message passing network architecture.

3. **Convergence Analysis**: The paper provides a rigorous analysis of the convergence of the approximate energy and electron density as the body-order is increased, supported by theoretical results and numerical experiments.

Overall, the study combines theoretical insights with practical machine learning techniques to enhance the accuracy and transferability of interatomic potentials by incorporating long-range electrostatic interactions.

### computing-solvation-free-energies-of-small-molecules-with-experimental-accuracy

## Methods

### Core Methodological Approaches
The study introduces a novel alchemical free energy protocol that leverages machine learned potentials (MLPs) to compute solvation free energies with high accuracy. The approach is designed to address the limitations of empirical force fields by using a pretrained, transferable MLP model equipped with scalable soft-core interactions. This enables the calculation of rigorous free energy differences in condensed phase systems.

### Tools and Software
- **OpenMM**: The simulations were implemented using the OpenMM package, which was modified to interface with the MACE (Machine Learning Atomistic Chemical Environment) model.
- **pymbar**: Used for statistically optimal analysis of samples from multiple equilibrium states.
- **GROMACS**: Employed for empirical force field calculations, specifically using the GAFF2/ABCG2 force field.

### Datasets
- **SPICE2 Data Set**: Used for training the MACE-OFF24-SC model, including protein-ligand and solvated PubChem data sets.
- **FreeSolv Database**: Provided experimental hydration free energies for benchmarking.
- **MNSol Database**: Used for octanol solvation free energy predictions.
- **CHEMBL Database**: Provided drug-like compounds for log _P_ calculations.

### Experimental Framework
- **Alchemical Free Energy Calculations**: The study employs Hamiltonian replica exchange molecular dynamics (REMD) to perform alchemical transformations. This involves gradually decoupling intermolecular interactions between solute and solvent using a _λ_-dependent Hamiltonian.
- **Softcore Potentials**: The MACE-OFF24-SC model incorporates softcore potentials to handle nonbonded interactions smoothly during alchemical transformations, avoiding singularities and ensuring numerical stability.
- **Replica Exchange**: Simulations were conducted with 16 replicas, with exchanges attempted every 1 ps to ensure sufficient phase-space overlap and convergence of free energy estimates.

### Theoretical Framework
- **Machine Learned Potentials (MLPs)**: The MACE-OFF24-SC model is based on MLPs that predict total intermolecular interactions without distinguishing between different types of interactions, allowing for a unified treatment of the system.
- **Equivariant Features**: The model uses equivariant features (_L_ max = 1) to enhance the accuracy of force predictions, particularly for intermolecular interactions.

### Computational Performance
- Simulations were performed on NVIDIA A100 and L40S GPUs, achieving aggregated sampling rates of approximately 8 ns/day across 16 replicas.
- The computational efficiency was demonstrated by the ability to converge hydration free energy calculations within 48 hours of wall time.

This methodological framework enables the accurate prediction of solvation free energies and distribution coefficients, demonstrating the potential of MLPs to improve upon traditional empirical force fields in computational chemistry applications.

### ja5c10940

## Methods

### Core Methodological Approaches
The study introduces a novel alchemical free energy protocol that leverages machine learned potentials (MLPs) to compute solvation free energies with high accuracy. The approach is designed to address the limitations of empirical force fields by using a pretrained, transferable MLP model equipped with scalable soft-core interactions. This enables the calculation of rigorous free energy differences in condensed phase systems.

### Tools and Software
- **OpenMM**: The simulations were implemented using the OpenMM package, which was modified to interface with the MACE (Machine Learning Atomic Cluster Expansion) model.
- **OpenMM-ML and OpenMM-Torch**: These libraries were used to perform Hamiltonian replica exchange and integrate MACE with OpenMM.
- **pymbar**: Used for statistically optimal analysis of samples from multiple equilibrium states to compute free energy differences.
- **GROMACS**: Used for empirical force field calculations, specifically with GAFF2/ABCG2 parameters.

### Datasets
- **SPICE2 Dataset**: Used for training the MACE-OFF24-SC model, including protein-ligand and solvated PubChem data sets.
- **FreeSolv and MNSol Databases**: Provided experimental hydration and solvation free energy data for benchmarking the model's predictions.

### Experimental Framework
- **Alchemical Free Energy Calculations**: The study employs an alchemical transformation approach, where the free energy difference between two states is computed using a λ-dependent Hamiltonian. This involves gradually decoupling intermolecular interactions between solute and solvent.
- **Replica Exchange Molecular Dynamics (REMD)**: Used to enhance sampling efficiency, with exchanges attempted every 1 ps across 16 replicas.
- **Softcore Potentials**: Implemented to handle the divergence of potential energy when atoms overlap during alchemical transformations. This involves modifying nontrainable parameters to scale nonbonded interactions smoothly.

### Theoretical Framework
- **MACE-OFF24-SC Model**: A modified version of the MACE model that includes softcore repulsion and λ-dependent two-body interactions. This model is trained to predict total intermolecular interactions without distinguishing between different types of interactions, allowing for smooth interpolation between coupled and decoupled states.
- **Equivariant Features**: The model uses equivariant features to improve the accuracy of intermolecular force predictions, with a focus on maintaining the correct physical description of end states.

### Computational Performance
- Simulations were performed on NVIDIA A100 and L40S GPUs, achieving aggregated sampling of around 8 ns/day across 16 replicas. Most hydration free energies converged within this time frame, while more complex systems required extended simulation times.

This methodological framework demonstrates the potential of MLPs to improve the accuracy and efficiency of free energy calculations, particularly in drug discovery applications.

### limitations-of-cluster-trained-mlips-for-liquid-density-and-diffusivity

## Methods

### 2.1. Data Sets for MLIP Generation

The study utilized two primary data sources for generating machine-learned interatomic potentials (MLIPs): periodic structures from Magdau et al. and cluster structures from Dajnowicz et al. These data sets were developed through multiple rounds of active learning, involving potential energy scans and molecular dynamics (MD) simulation snapshots. The periodic data set included 935 structures with 66,188 atoms, while the cluster data sets varied in size, with the largest containing 362,382 structures and 7,781,985 atoms. The cluster data sets were further divided into subsets (Clusters-Small, Clusters-Medium, Clusters-Large) to assess the impact of data set size and composition on MLIP performance.

### 2.2. DFT Functionals

Density Functional Theory (DFT) calculations for periodic systems were performed using a plane-wave basis set with Projector Augmented Wave pseudopotentials in the Vienna Ab initio Simulation Package. The functionals used were PBE-D2, PBE-D3, and B97-D3, with a kinetic energy cutoff of 800 eV and Γ-point sampling. For cluster MLIPs, the original data set was labeled with the _ω_ B97X-D3 functional using the Psi4 program, employing the def2-TZVPD basis set. Additional DFT calculations at the B97-D3 level were performed for comparison.

### 2.3. MLIP Generation

MLIPs were trained using the MACE framework, which employs a message-passing equivariant neural network. The architecture included two interaction layers, a correlation order of 3, and angular momentum channels up to / = 3. Training involved minimizing a weighted loss function with contributions from energies and forces, using the Adam optimizer with AMSgrad, a batch size of 20, and a learning rate of 0.01. Models were trained for up to 1600 epochs with early stopping, and stochastic weight averaging was applied to ensure low energy errors.

### 2.4. MD Simulations and Property Calculations

MD simulations were conducted in the NPT ensemble for 1 ns using the trained MLIPs. Simulations were performed at 298 K (313 K for pure EC) and 1 atm pressure, with a time step of 1 fs. The Nosé−Hoover thermostat and Parrinello−Rahman barostat were used, with relaxation times of 50 and 2500 fs, respectively. Diffusion coefficients were calculated from mean-squared displacements, corrected for finite size effects, and reported with a 95% confidence level. The simulations were executed using the MACE implementation in the Atomic Simulation Environment package.

### towards-routine-condensed-phase-simulations-with-delta-learned-coupled-cluster-accuracy-application-to-liquid-water

## Methods

### 6.1. Machine Learning Potentials
The study employs the MACE architecture for machine learning potentials (MLPs), which utilizes equivariant message passing with local body-order descriptions of each atom. The baseline DFT MLPs are configured with 2 message passing layers, 128 channels, and a 6 Å cutoff, while the Δ-MLP uses 64 channels and a 4 Å cutoff to reduce inference costs without compromising accuracy. A validation set comprising 10% of each dataset was used.

### 6.2. Density Functional Theory
DFT calculations for both the baseline and Δ-MLP were conducted using FHI-AIMs, capable of handling both periodic and open boundary conditions. The tight family of basis sets and Grimme’s D3 dispersion correction were employed. Calculations were performed at the Γ-point, with datasets generated from a wide range of pressures and nuclear quantum effects, using revPBE-D3, PBE-D3, and r[2] SCAN as baselines.

### 6.3. Coupled Cluster Theory
CCSD(T) energies were calculated using ORCA and MRCC software, employing domain-based local pair natural orbital (DLPNO) and local natural orbital (LNO) approximations. ORCA used "TightPNO" DLPNO thresholds, while MRCC used "normal" LNO thresholds with density-fitting for Hartree−Fock calculations. The jul-cc-pV_X_Z basis sets were used, with CBS extrapolations for triple and quadruple-ζ basis sets.

### 6.4. Molecular Dynamics
Molecular dynamics simulations were performed using LAMMPS, coupled with the Symmetrix library, to obtain density isobar, RDF, and self-diffusion coefficient. Simulations were conducted with 126 water molecules at 298 K, using a 0.5 fs timestep for classical simulations and a 0.25 fs timestep for path integral molecular dynamics (PIMD) simulations. The CSVR thermostat was used for temperature control, and densities were obtained from NPT simulations with a barostat relaxation time of 1 ps. Path integral simulations used 32 beads for RPMD and T-RPMD simulations.

### Data Availability
The data required to reproduce the study is available on a GitHub repository, and all simulations were performed using publicly available software (ACEsuit, LAMMPS, Symmetrix).