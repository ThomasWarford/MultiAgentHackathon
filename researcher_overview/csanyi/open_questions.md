

### 224313_1_5.0296997

## Open Questions

1. **Accuracy of DFT Forces**: The paper highlights significant discrepancies in DFT force calculations across various datasets. An open question remains on how to systematically improve the accuracy of DFT forces to ensure they are well below the error margins of MLIP force predictions. What are the best practices for achieving consistently accurate DFT forces across different computational setups?

2. **Impact on MLIP Training**: The study suggests that inaccuracies in DFT forces can affect the training and evaluation of MLIPs. How can MLIPs be designed or trained to be more robust against noisy DFT data? Are there alternative methods to mitigate the impact of DFT inaccuracies on MLIP performance?

3. **Optimization of DFT Settings**: The authors identify specific DFT settings that reduce force errors, such as disabling the RIJCOSX approximation and using tighter grids. What other computational settings or approximations could be optimized to further reduce errors in DFT calculations?

4. **Dataset Quality Control**: The presence of nonzero net forces in datasets indicates potential quality issues. What systematic approaches can be developed to assess and ensure the quality of DFT data in existing and future datasets? How can datasets be filtered or corrected to minimize the impact of these errors?

5. **Generalization to Periodic Systems**: While the study focuses on molecular datasets, it briefly mentions the relevance of net forces in periodic systems. How do the findings translate to periodic systems, and what specific challenges need to be addressed in this context?

6. **Role of Specific Elements**: The paper notes that large force discrepancies are often associated with the presence of bromine or iodine. What is the underlying cause of these discrepancies, and how can they be addressed in DFT calculations involving such elements?

7. **Cross-Software Consistency**: The study compares forces computed with different software packages and settings. How can consistency across different quantum chemistry software be improved to ensure reliable force calculations?

8. **Future Dataset Development**: As new datasets are developed, what guidelines should be established to ensure high-quality DFT data? How can the community standardize practices to minimize numerical errors and improve the reliability of datasets used for MLIP training?

9. **Error Quantification and Reporting**: The authors emphasize the importance of quantifying and reporting errors in DFT forces. What standardized metrics and reporting practices should be adopted to facilitate transparency and reproducibility in computational chemistry research?

10. **Integration with Machine Learning**: Given the increasing integration of machine learning in computational chemistry, how can machine learning techniques be leveraged to predict or correct DFT force errors in real-time? What role can active learning play in improving the quality of DFT datasets?

### 2602.19411v1

## Open Questions

1. **Long-Range Electrostatics and Charge Transfer**: While the MACE-POLAR-1 model addresses long-range electrostatics and charge transfer, the paper highlights the challenge of accurately modeling these interactions in large biomolecular systems and charged systems. Future work could explore more sophisticated methods for capturing these effects, potentially integrating higher-order correlation effects or alternative approaches to charge equilibration.

2. **Self-Consistent Field Iterations**: The authors mention the potential instability and computational cost of self-consistent field iterations. Future research could focus on developing more stable and efficient self-consistent methods or alternative approaches that maintain accuracy without the need for iterative solutions.

3. **Dataset Limitations**: The OMol25 dataset, while extensive, is based on hybrid DFT calculations, which may not capture all necessary quantum mechanical effects. Future datasets could incorporate higher-level quantum mechanical data, such as coupled-cluster calculations, to improve model accuracy, particularly for liquid properties and complex systems.

4. **Specialized Domain Models**: The paper suggests the development of specialized variants of the MACE-POLAR-1 model for specific domains like proteins, materials, and catalysis. This could involve tailoring the model architecture or training strategies to better capture the unique interactions and properties relevant to each domain.

5. **Machine-Learned Dispersion Corrections**: The authors propose incorporating machine-learned dispersion corrections to enhance the accuracy of van der Waals complexes. Future work could explore how these corrections can be integrated into the existing framework and their impact on model performance.

6. **External Field Response**: The ability of the model to extrapolate to external fields is highlighted as a challenging test. Future research could focus on improving the model's ability to predict response properties, such as dipoles and polarizabilities, potentially by incorporating explicit training on these properties or refining the model's treatment of induction physics.

7. **Quantitative Liquid-Property Accuracy**: The systematic deviation of liquid densities from experimental values suggests limitations in the reference DFT functional. Future work could explore alternative reference data or model architectures to achieve better quantitative accuracy for liquid properties.

8. **Error Analysis and Model Robustness**: The paper notes the importance of understanding error sources and improving model robustness, particularly for challenging systems like transition metals and redox reactions. Future research could focus on detailed error analysis and the development of strategies to enhance model reliability across diverse chemical spaces.

9. **Integration with Other Computational Methods**: The potential for integrating MACE-POLAR-1 with other computational methods, such as classical force fields or quantum mechanical calculations, is an area for future exploration. This could involve hybrid approaches that leverage the strengths of different modeling techniques.

10. **Scalability and Computational Efficiency**: While the model is designed to be computationally efficient, further improvements in scalability and efficiency could be explored, particularly for large-scale simulations or real-time applications in drug discovery and materials science.

### 2604.08143v1

## Open Questions

1. **Extension of Training Data**: The pre-trained models are primarily fitted to datasets dominated by collinear, predominantly ferromagnetic configurations. Extending the foundational training data to include antiferromagnetic, non-collinear, and frustrated magnetic orderings could broaden the applicability of pre-trained mMACE models. How can such datasets be effectively constructed and integrated into the training process?

2. **Self-consistent Integration of SOC**: While the study demonstrates that SOC-induced anisotropy can be fitted as a perturbative correction, integrating it self-consistently into the training procedure remains an open challenge. What methodologies could be developed to incorporate SOC effects directly into the training of machine-learned interatomic potentials?

3. **Unified Treatment of SOC and Non-SOC Systems**: The current model architecture requires data augmentation to handle systems without SOC. Developing an architecture that effectively treats both non-SOC and SOC systems without the need for data augmentation would enhance both accuracy and generality. What architectural innovations could achieve this?

4. **Coupling with Spin-lattice Dynamics**: Coupling mMACE to spin-lattice dynamics frameworks could enable the study of magnon-phonon interactions, demagnetization, and other dynamical phenomena beyond static relaxations and Monte Carlo sampling. What are the potential approaches to achieve such coupling, and what computational challenges might arise?

5. **Handling of Multiple Magnetic Solutions**: The study highlights the intrinsic ambiguity in datasets that mix multiple self-consistent magnetic solutions. How can magnetic datasets be curated or interpreted to better represent a single-valued energy landscape, and what metrics could be developed to evaluate magnetic MLIPs beyond single-point comparisons?

6. **Performance Optimization**: The mMACE model introduces additional computational overhead due to the inclusion of magnetic degrees of freedom. What strategies could be employed to optimize the performance of mMACE, particularly in large-scale simulations?

7. **Generalization to Diverse Chemical Environments**: The ability of mMACE to generalize across diverse chemical environments, particularly in predicting magnetocrystalline anisotropy, is crucial. How can the model's generalization capabilities be further improved, and what additional datasets or training techniques might be necessary?

8. **Evaluation of Magnetic Properties**: The study demonstrates the ability of mMACE to predict various magnetic properties, such as Curie temperatures and Heisenberg exchange constants. What additional magnetic properties could be targeted for prediction, and how might the model be adapted to improve accuracy in these areas?

9. **Robustness to Initial Conditions**: The model's performance in recovering non-collinear ground states from random initial spin orientations suggests robustness. However, what are the limits of this robustness, and how can the model be further tested or improved to ensure reliable predictions across a wider range of initial conditions?

10. **Integration with Experimental Data**: While the model is primarily trained on DFT data, integrating experimental data could enhance its predictive power. What are the challenges and potential methodologies for incorporating experimental observations into the training and validation of mMACE models?

### 2604.15394v1

## Open Questions

1. **Interfacial Disorder and Phonon Transport Mechanisms**: The study highlights the complex interplay between diffuse scattering and phonon bridging at disordered interfaces. However, the precise mechanisms by which disorder affects phonon transport, particularly in realistic device environments, remain underexplored. Further research is needed to fully understand these mechanisms and their implications for thermal management.

2. **Predictive Modeling of TBC**: While the integration of machine-learned interatomic potentials with a wave-particle hybrid model has advanced the understanding of thermal boundary conductance (TBC), the predictive accuracy of these models in diverse material systems and under varying conditions is still uncertain. Future work could focus on refining these models to improve their applicability and reliability across different interfaces.

3. **Experimental Validation Across Systems**: The study successfully validates theoretical predictions with experimental measurements for the _β_-Ga2O3/4H-SiC interface. However, extending this validation to other material systems with different lattice mismatches and interfacial characteristics could provide broader insights into the generalizability of the findings.

4. **Controlled Epitaxial Growth Techniques**: The research underscores the importance of achieving atomically sharp interfaces through controlled epitaxial growth. Developing more robust and scalable techniques for epitaxial growth that can consistently produce high-quality interfaces across various materials remains a significant challenge.

5. **Impact of Environmental Factors**: The study primarily focuses on the intrinsic properties of the interfaces. The impact of external factors such as temperature fluctuations, mechanical stress, and chemical exposure on TBC and interfacial stability warrants further investigation.

6. **Long-term Stability and Reliability**: While the study demonstrates high TBC in disorder-free interfaces, the long-term stability and reliability of these interfaces under operational conditions in electronic devices are not addressed. Future research could explore the durability of these interfaces over extended periods and under varying operational stresses.

7. **Integration with Device Design**: The practical integration of high-TBC interfaces into device architectures, particularly in terms of compatibility with existing manufacturing processes and materials, remains an open question. Research into the co-design of devices and interfaces could facilitate the adoption of these findings in commercial applications.

8. **Quantum Effects in Phonon Transport**: The study incorporates quantum statistics into the modeling of phonon transport, yet the full extent of quantum effects, especially at nanoscale interfaces, is not completely understood. Further exploration of quantum coherence and its role in thermal transport could yield new insights.

9. **Scalability of Machine Learning Approaches**: The use of machine learning to develop interatomic potentials is promising, but the scalability of these approaches to more complex systems with larger datasets and higher computational demands is an ongoing challenge. Future work could focus on optimizing these methods for broader applications.

### 3731545.3731594

## Open Questions

1. **Load Balancing and Randomness Trade-off**: The paper mentions that the developed load balancer sacrifices randomness, which may impact training effectiveness. How significant is this impact, and are there ways to mitigate it while maintaining efficient load balancing?

2. **Emerging Bottlenecks**: As the paper optimizes certain bottleneck operations in CFMs like MACE, it acknowledges that other operations may become new bottlenecks. What are these potential new bottlenecks, and what strategies could be employed to address them?

3. **Scalability of Optimizations**: The optimizations presented are shown to be effective on the Perlmutter supercomputer. How well do these optimizations scale on different hardware architectures or smaller-scale systems?

4. **Generalization to Other Models**: The paper claims that the optimizations are broadly applicable to other models built on equivariant GNN architectures. What specific challenges might arise when applying these optimizations to different models or datasets?

5. **Impact of Dataset Diversity**: The paper highlights the diversity in dataset sizes and sparsity patterns. How does this diversity affect the generalization capabilities of the optimized models, and are there specific dataset characteristics that could hinder performance?

6. **Optimal Configuration Parameters**: The paper discusses determining optimal bin capacity and mini-batch size empirically. Is there a theoretical framework that could guide these choices more systematically?

7. **Communication-Computational Balance**: The paper notes improvements in the computation-communication balance. What further optimizations could be explored to enhance this balance, especially in more communication-intensive environments?

8. **Future Bottlenecks in Kernel Optimization**: As kernel optimizations are applied, what are the anticipated future bottlenecks in kernel performance, and how might they be addressed?

9. **Long-term Impact of Kernel Fusion**: Kernel fusion is used to improve performance. What are the long-term impacts of this approach on model maintainability and adaptability to future hardware changes?

10. **Effectiveness Across Chemical Domains**: The paper evaluates performance across diverse chemical systems. How does the effectiveness of the proposed optimizations vary across different chemical domains, and what additional domain-specific challenges might arise?

11. **Impact of Data Distribution on Model Accuracy**: While the paper focuses on performance improvements, how does the optimized data distribution affect the accuracy and robustness of the trained models?

12. **Integration with Other Frameworks**: The optimizations are implemented in PyTorch. How feasible is it to integrate these optimizations into other machine learning frameworks, and what challenges might be encountered?

13. **Long-term Training Stability**: The paper demonstrates short-term performance improvements. What is the impact of these optimizations on the long-term stability and convergence of the training process?

### Thomas_2025_Nonlinearity_38_095024

## Open Questions

1. **Incorporation of Long-Range Electrostatics**: The paper discusses the inclusion of long-range electrostatic effects in machine learning interatomic potentials. However, the challenge remains in accurately modeling these effects in a way that is both computationally efficient and physically accurate. How can these models be further refined to better capture the nuances of long-range interactions?

2. **Charge Equilibration Schemes**: The authors propose a self-consistent charge equilibration scheme, but acknowledge that the quadratic-in-charge ansatz is too simplistic for systems with discontinuous electron densities, such as those with conical intersections. What alternative mathematical frameworks could be developed to address these limitations?

3. **Transferability and Generalization**: While the proposed models show promise, their transferability across different chemical environments and system sizes is not fully addressed. How can these models be generalized to ensure accuracy and reliability across a broader range of materials and conditions?

4. **Computational Efficiency**: The paper introduces a fixed-point scheme for practical computation, yet the scalability of this approach to larger systems or more complex environments is not fully explored. What strategies can be employed to enhance the computational efficiency of these models without sacrificing accuracy?

5. **Body-Ordered Approximations**: The authors demonstrate the potential of body-ordered approximations, but the convergence and accuracy of these approximations in the bulk limit remain uncertain. How can the theoretical framework be extended to ensure robust performance in larger systems?

6. **Canonical vs. Grand Canonical Ensemble**: The paper primarily focuses on the grand-canonical ensemble, with limited discussion on the canonical ensemble. How can the analysis be extended to the canonical ensemble, and what implications would this have for the applicability of the models?

7. **Handling of Conical Intersections**: The current framework struggles with systems exhibiting conical intersections. What new methodologies or modifications to existing models could be introduced to better handle these complex electronic phenomena?

8. **Dependence on System Size**: The results indicate a dependence on system size, which limits the extension of the analysis to the bulk limit. What approaches can be taken to mitigate this dependence and improve the scalability of the models?

9. **Numerical Validation and Real-World Applications**: While preliminary numerical experiments are presented, further validation against experimental data and real-world applications is necessary. What additional experiments and datasets are needed to thoroughly test and validate the proposed models?

10. **Integration with Existing Computational Frameworks**: The integration of these machine learning models with existing computational chemistry frameworks, such as DFT, is not fully explored. How can these models be seamlessly integrated to enhance the capabilities of current computational tools?

### computing-solvation-free-energies-of-small-molecules-with-experimental-accuracy

## Open Questions

1. **Compatibility with Existing Protocols**: The paper introduces a new alchemical free energy protocol using machine learned potentials (MLPs). However, it remains to be seen how seamlessly this approach can be integrated with existing well-tested free energy protocols and analysis packages like pymbar and pmx, which are currently optimized for classical force fields.

2. **Computational Expense**: While MLPs offer improved accuracy, their computational expense is higher compared to empirical force fields. The paper mentions that hydration free energy calculations are feasible within reasonable wall time, but the scalability of this approach to larger systems or more complex simulations, such as protein-ligand binding, remains an open question.

3. **Long-Range Interactions**: The lack of an explicit long-range contribution in the MACE-OFF models limits the chemical space where the model is expected to be accurate. Future work could explore incorporating long-range interactions to enhance the model's applicability.

4. **Transferability to Complex Systems**: The study shows promising results for small organic molecules, but the transferability of the MLPs to more complex, drug-like molecules and their interactions in biological systems is still uncertain. Further validation on diverse chemical spaces and larger biomolecular systems is needed.

5. **High-Temperature Regimes**: The paper notes that while the introduction of softcore interactions is not expected to affect the ensemble sampled at room temperature, this may not hold true at high temperatures. Investigating the performance and stability of the model under varying temperature conditions could be a valuable direction for future research.

6. **Parameter Optimization**: The choice of parameters for the softcore potential, such as the transition point for dimer curves, is crucial for maintaining numerical stability. Further optimization and understanding of these parameters could improve the robustness and accuracy of the simulations.

7. **Electrostatic Embedding**: The paper mentions recent developments in electrostatic embedding ML/MM schemes, but their performance in alchemical binding free energy calculations has not yet been established. Exploring these methods could provide insights into improving the accuracy of nonbonded interactions.

8. **Benchmarking Against Experimental Data**: While the model shows improved accuracy over classical force fields, the comparison is limited by the experimental error margins. More extensive benchmarking against high-quality experimental data could help in assessing the true potential and limitations of the MLP approach.

9. **Nonequilibrium Switching Approaches**: The paper suggests that the new approach is amenable to nonequilibrium switching approaches, but further exploration of these methods could provide additional computational savings and insights into the dynamics of alchemical transformations.

10. **Impact of Softcore Interactions on Sampling**: The introduction of softcore interactions is intended to improve numerical stability, but its impact on the sampling efficiency and convergence of free energy calculations, especially in complex systems, remains to be fully understood.

### ja5c10940

## Open Questions

1. **Compatibility with Standard Alchemical Methods**: The paper introduces a new alchemical free energy protocol using machine learned potentials (MLPs), but it remains to be seen how well this approach integrates with existing well-tested free energy protocols and analysis packages like pymbar and pmx. Further exploration is needed to ensure compatibility and ease of use within the broader computational chemistry community.

2. **Computational Expense and Efficiency**: While MLPs offer improved accuracy, their computational expense is a significant bottleneck. The paper mentions that the application of MLPs has been mostly restricted to corrective perturbations due to high sampling requirements. Future work could focus on optimizing computational efficiency to make MLPs more accessible for routine use in free energy calculations.

3. **Parameter Transferability**: The study highlights the challenge of parameter transferability from small molecules to larger, more complex systems. This is particularly relevant for drug-like molecules where empirical force fields often fail. Further research is needed to improve the transferability of MLPs across different chemical spaces.

4. **Handling of Long-Range Interactions**: The lack of an explicit long-range contribution in the MACE-OFF models limits their applicability. Future work could explore incorporating long-range interactions to expand the chemical space where these models can be accurately applied.

5. **High-Temperature Regimes**: The paper notes that while the introduction of softcore interactions is not expected to affect the ensemble sampled at room temperature, this may not hold true at high temperatures. Investigating the behavior of these models under different temperature conditions could provide insights into their robustness and applicability.

6. **Alchemical Scaling and Phase Space Overlap**: The linear formulation of the potential without explicit dependence on the alchemical parameter _λ_ can lead to challenges with phase space overlap. Future research could focus on developing more sophisticated scaling strategies to maintain reasonable overlap between replicas.

7. **Benchmarking Against Experimental Data**: While the study shows promising results, further benchmarking against a wider range of experimental data, particularly for complex systems, would be beneficial to validate the accuracy and reliability of the proposed methods.

8. **Integration with Emerging Computational Tools**: The paper mentions the potential for improved throughput with optimized computational kernels like NVIDIA’s cuEquivariance. Future work could explore the integration of these tools to enhance the performance of MLP-based free energy calculations.

9. **Exploration of Alternative Nonbonded Functional Forms**: The study briefly mentions alternative nonbonded functional forms with more natural softcore potentials. Further investigation into these alternatives could provide additional pathways to improve numerical stability and accuracy.

10. **Application to Protein-Ligand Binding Free Energies**: While the paper focuses on solvation free energies, extending the application of MLPs to protein-ligand binding free energy calculations remains an open question. This would require addressing the unique challenges posed by the complexity and size of protein-ligand systems.

### limitations-of-cluster-trained-mlips-for-liquid-density-and-diffusivity

## Open Questions

1. **Uncertainty in MLIP Predictions**: The study highlights significant uncertainties in the predictions of density and diffusivity when using cluster-trained MLIPs. This raises questions about the reliability of these models for simulating bulk liquid properties. How can these uncertainties be reduced, and what strategies can be employed to improve the predictive accuracy of cluster-trained MLIPs?

2. **Data Representation and Extrapolation**: The paper discusses the challenges of using cluster data for training MLIPs, particularly the risk of poor representation of bulk-like environments and the potential for out-of-domain extrapolation errors. What methods can be developed to ensure that cluster data adequately represents bulk properties, and how can the extrapolation capabilities of MLIPs be enhanced?

3. **Long-Range Interactions**: The lack of long-range interactions in cluster data is identified as a potential source of error. How can MLIPs be adapted to incorporate long-range interactions effectively, and what impact would this have on their accuracy and stability?

4. **Training Set Composition**: The study notes the skewness in the training data towards certain molecular compositions, which affects the model's performance. What are the best practices for selecting and balancing training data to ensure robust MLIP performance across different compositions?

5. **Comparison of DFT Functionals**: While the study successfully compares a few DFT functionals using periodic data, it suggests that a broader comparison is needed. What systematic approaches can be developed to benchmark a wide range of DFT functionals using MLIPs, and how can these approaches be validated against experimental data?

6. **Active Learning and Data Augmentation**: The paper mentions the potential need for active learning to stabilize MLIPs. What are the most effective active learning strategies for improving MLIP stability and accuracy, and how can data augmentation be used to enhance training sets?

7. **Transfer Learning and Fine-Tuning**: The potential for transfer learning on high-level QM data is discussed. How can transfer learning be optimized for MLIPs, and what are the key considerations for fine-tuning models to achieve high accuracy in predicting liquid properties?

8. **Impact of Random Seeds**: The sensitivity of MLIP predictions to random training seeds is highlighted. What methodologies can be developed to mitigate the impact of random seed variations on MLIP predictions, and how can model robustness be ensured?

9. **Integration of Electrostatics**: The study suggests that incorporating electrostatics might improve model robustness. How can electrostatic interactions be effectively integrated into MLIP frameworks, and what are the computational trade-offs involved?

10. **Future Directions for MLIP Development**: The paper implies several future directions, such as improving data representation, enhancing model stability, and expanding functional comparisons. What are the most promising research avenues for advancing MLIP technology, and how can these be prioritized to address current limitations?

### towards-routine-condensed-phase-simulations-with-delta-learned-coupled-cluster-accuracy-application-to-liquid-water

## Open Questions

1. **Routine Application of CCSD(T) MLPs**: While the study presents a practical approach to developing CCSD(T)-level machine learning potentials (MLPs) for liquid water, achieving routine application remains a challenge. The computational cost and complexity of generating large datasets for training these models are significant barriers.

2. **Constant-Pressure Simulations**: The study highlights that no CCSD(T) MLP model of liquid water has been applied at constant pressure, which is crucial for accurately predicting isothermal isobaric properties such as the density maximum of water. Developing models that can handle constant-pressure simulations reliably remains an open question.

3. **Long-Range Interactions**: The current Δ-learning approach assumes that the DFT baseline can describe long-range contributions, which may not be accurate for systems with significant long-range interactions. This limitation affects the model's applicability to interfacial systems and systems with broken translational symmetry.

4. **Data Efficiency and Cost Reduction**: Although the study proposes a more cost-effective approach, the computational cost is still high. Further reducing the number of large clusters required for training without compromising accuracy is an ongoing challenge.

5. **Error Accumulation in Δ-Learning**: The Δ-learning approach requires two MLP models, which may lead to an accumulation of errors from summing two models. Investigating and mitigating these potential errors is necessary for improving model reliability.

6. **Generalizability to Other Systems**: Extending the approach to more complex systems, such as aqueous solutions with ions or other solvents, is a future direction. The current model's ability to generalize beyond liquid water properties is yet to be fully explored.

7. **Incorporation of Long-Range Electrostatics**: The lack of long-range electrostatics in the current models limits their application. Developing methods to incorporate these effects, possibly through embedding procedures or higher-level baselines, is a critical area for future research.

8. **Transfer Learning and Multi-Head Fine-Tuning**: While promising, the efficacy of transfer learning and multi-head fine-tuning approaches for learning bulk behavior from clusters has not been fully demonstrated. Further exploration of these methods could enhance the development of CCSD(T)-quality MLPs.

9. **Exploration of Alternative Architectures**: The study mentions the potential of alternative architectures, such as neuroevolution potentials, to reduce computational costs. Investigating these architectures for their applicability and efficiency in achieving CCSD(T) accuracy is an open question.

10. **Benchmarking Electronic Structure Parameters**: Systematic benchmarking of electronic structure parameters, such as basis set size and local approximation thresholds, is necessary to optimize the balance between computational cost and accuracy.

11. **Handling of Reactive Systems**: Extending the approach to accurately predict reactions in various solvents, which requires high accuracy in electronic structure and extensive sampling, is a future goal.

12. **Development of a Comprehensive Water Model**: The study focuses on a limited subset of liquid water properties. Developing a more complete model that can address other challenging properties, such as solid-liquid and liquid-air interfaces, remains an open question.