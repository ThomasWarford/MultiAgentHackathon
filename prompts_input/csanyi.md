# Csanyi — Researcher Prompt

## Current focus
Developing the MACE family of equivariant machine-learning interatomic potentials (MLIPs) to bring quantum-mechanical accuracy (DFT and beyond — up to CCSD(T) via delta-learning) to condensed-phase and large-scale molecular simulations. Active work spans: long-range electrostatics and self-consistent charge equilibration (MACE-POLAR-1, Thomas et al. 2025), magnetic degrees of freedom (mMACE), solvation free energies of drug-like molecules with MACE-OFF24-SC, thermal transport at lattice-mismatched interfaces, and the engineering side of training foundation models efficiently on >700 GPUs.

## Recent milestones
- MACE-POLAR-1: non-self-consistent field formalism extends MACE to long-range electrostatics, charge transfer, and induction; sub-kcal/mol on molecular crystal formation energies.
- mMACE: explicit atomic magnetic moments enable non-collinear magnetism, spin-orbit coupling, magnetocrystalline anisotropy, and Curie temperature prediction.
- MACE-OFF24-SC + alchemical free-energy protocol: subchemical-accuracy solvation free energies for drug-like molecules in aqueous and non-aqueous solvents.
- Delta-learned CCSD(T) MLP for liquid water at constant pressure, reproducing the experimental density maximum.
- Identified systematic DFT-force inaccuracies (up to 33 meV/Å) across widely used MLIP training sets (SPICE, ANI-1x, Transition1x) and published mitigation guidelines.
- 6× per-epoch speedup for MACE foundation-model training via multi-objective bin-packing data distribution and symmetric tensor-contraction kernel optimization on 740 GPUs.

## Blockers
- Cluster-trained MLIPs show large, seed-dependent uncertainty in bulk liquid density and diffusivity — periodic training data, active learning, and explicit long-range interactions all only partially fix it.
- Self-consistent field iterations for charge equilibration are expensive and can be unstable; quadratic-in-charge ansatz fails on systems with discontinuous electron densities (e.g. conical intersections).
- No clean architectural treatment that handles SOC and non-SOC systems without data augmentation.
- Routine application of CCSD(T)-quality MLPs is gated by the cost of generating training data and by error accumulation in the two-model delta-learning stack.
- DFT reference data quality is heterogeneous across community datasets, with the worst force errors correlated with bromine/iodine and grid/RIJCOSX settings — no standard reporting practice exists.

## Notes
Methodological style: equivariant message-passing GNNs on 3D molecular graphs, body-ordered/local-by-construction representations, fit to QM reference data, validated against bulk thermodynamic properties and experimental observables. Strong interest in transferability across chemical environments and in turning expensive electronic-structure methods into routine simulation tools.
