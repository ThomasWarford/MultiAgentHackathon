

### Baker_2025_Environ._Res._Lett._20_034028

## Methods

### 2.1. Calculating Carbon Emissions

The study employs a bottom-up approach to estimate fire-driven carbon emissions in the UK from 2001 to 2021. The methodology integrates spatially explicit vegetation cover maps with burned area estimates derived from satellite data. The Global Fire Emissions Database (GFED) serves as a benchmark for emissions validation. The core components of the emission calculations include:

- **Data Sources**: High-resolution land cover data and burned area estimates from the FireCCI51: MODIS Fire_cci Burned Area Pixel Product, Version 5.1, and the European Forest Fire Information System (EFFIS) at a 250 m resolution.
- **Carbon Mapping**: Aboveground carbon maps for Great Britain and Northern Ireland, using data from Henrys et al. (2016) and Spawn et al. (2020), to estimate carbon density specific to vegetation types.
- **Emission Calculation**: Emissions are calculated by multiplying fuel loads by satellite-derived burned area and a combustion completeness (CC) metric, following methodologies similar to those in GFED and van Wees et al. (2022).
- **Vegetation Classification**: Land cover maps from various years (2007, 2015, 2017-2020) are used to classify vegetation into categories such as 'Forests and Woodlands', 'Moorlands and Heathlands', 'Peatlands', and 'Other Natural and Managed Lands'.
- **SOC Emissions**: Soil organic carbon (SOC) emissions are calculated using burn depth estimates, peat carbon bulk density, and the fraction of peat in burned grid cells. The burn depth is estimated using a linear function tied to soil moisture content from ERA5 land monthly average volumetric soil water data.

### 2.2. Fire Weather Index (FWI) and ISI

The study utilizes the Fire Weather Index (FWI) and the Initial Spread Index (ISI) from the Copernicus ERA5 reanalysis data to assess fire danger. These indices are based on the Canadian FWI system, which considers variables such as fuel moisture, temperature, relative humidity, wind, and rain effects on fire spread.

### 2.3. Projected Soil Moisture Changes at 2°C Global Warming Level (GWL)

Future soil moisture projections are derived from Kay et al. (2022), using the UK Climate Projections 2018 regional projections. These projections simulate soil moisture changes under a 2°C global warming scenario, using a 12-member perturbed parameter ensemble of the Hadley Centre RCM. The study calculates potential SOC emissions under these future conditions, assuming no change in burned area.

### Sensitivity Analyses

The study conducts sensitivity analyses to evaluate the impact of variations in bulk density and the relationship between soil moisture and burn depth on SOC emissions. This involves testing different combustion completeness values and burn depth equations to refine emission estimates.

### Tools and Frameworks

- **Satellite Data**: MODIS Fire_cci and EFFIS for burned area mapping.
- **Emission Models**: Adaptations of GFED methodologies for calculating carbon emissions.
- **Climate Data**: ERA5 reanalysis for fire weather indices and soil moisture projections.
- **Land Cover Maps**: High-resolution maps for vegetation classification and carbon density estimation.

This comprehensive methodological framework allows for a detailed assessment of fire-driven carbon emissions in UK peatlands, considering both historical data and future climate projections.

### Journal of Ecology - 2023 - Coetsee - Soil organic carbon is buffered by grass inputs regardless of woody cover or fire

## Methods

### Study Design
The study was conducted using long-term experimental burn plots in Kruger National Park (KNP), South Africa, established in 1954. The experiment aimed to assess the impact of fire frequency and season on vegetation structure. The experimental design included 16 replicates, with four replicates each in four major vegetation types within KNP. Each replicate, or 'string', consisted of 12-14 fire treatments. This study focused on four strings in two vegetation types: Pretoriuskop and Skukuza. The fire treatments included annual late dry season burns (Aug 1yr), triennial late dry season burns (Aug 3yr), triennial wet season burns (Feb 3yr), and fire exclusion (NB).

### Data Collection
- **Woody Cover and Grass Biomass**: Woody biomass was estimated using surveys conducted in 1956-1957 and 2016. Historical aerial photography from 1944 to 2018 was used to document changes in woody cover. Herbaceous biomass was estimated using a disc pasture meter (DPM) along transects in each plot.
- **Soil Sampling**: Soil samples were collected under and away from the canopy of large trees in each plot in 2016. Samples were taken at four depths (0-5 cm, 5-10 cm, 10-20 cm, and 20-30 cm) and analyzed for soil organic carbon (SOC) and δ[13]C.

### Analytical Techniques
- **Isotope Analysis**: The δ[13]C values of soil samples were determined using a Thermo Finnigan Delta plus XP mass spectrometer. A standard end-member mixing model was used to determine the relative proportion of C derived from C3 (trees) and C4 (grass) plants.
- **Soil Texture Analysis**: Soil texture was analyzed using the hydrometer method to determine the proportions of sand, clay, and silt.

### Statistical Analysis
- **Variance and Model Testing**: The Fligner-Killeen test was used to assess homogeneity of variance. Nonparametric Kruskal-Wallis tests were used for data with unequal variance. Linear mixed-effects models were employed to test the effects of fire treatment on herbaceous biomass and SOC, with treatment and canopy type as fixed effects and plot ID as a random effect. The lmerTest package provided p-values for linear mixed models.
- **Post-hoc Comparisons**: The emmeans package was used for post-hoc comparisons with Bonferroni adjustments.
- **ANCOVA**: An ANCOVA model tested the effect of C type (C4-derived vs. C3-derived C) on soil C, with soil C as the dependent variable and woody cover as a covariate.

### Tools and Software
- **Geospatial Analysis**: ArcGIS Pro was used for image preparation and analysis of historical aerial photographs.
- **Statistical Software**: R version 3.4.2 was used for all statistical analyses, employing packages such as lme4, lmerTest, and emmeans.

### Experimental Framework
The study utilized a long-term fire manipulation experiment to explore the effects of different fire regimes on SOC sequestration and the contributions of C3 and C4 plant inputs. The experimental framework allowed for the isolation of local- and landscape-level effects of woody plant encroachment on SOC.

### main

## Methods

### Data Collection

#### Literature Search
The study conducted a comprehensive literature search using Web of Science and SCOPUS databases to identify studies that quantified both yield and soil carbon impacts of four agricultural practices: cover cropping, complex crop rotations, reduced tillage, and crop residue retention. The search targeted studies involving four staple crops: maize, wheat, rice, and soybeans. The search included all English-language primary articles published until November 17, 2022, resulting in 13,945 unique articles after removing duplicates.

#### Data Compilation & Management
A total of 510 papers published between 1978 and 2024 met the inclusion criteria, yielding 2975 paired yield and topsoil SOC observations from 402 unique study sites. The study included observations comparing a single sustainable practice or combination of practices to a control lacking that practice. Data collected included means, number of replications, and estimates of variability for SOC and yield parameters. Missing standard deviations were imputed using the average coefficient of variation for all observations with reported standard deviations. Bulk density values were imputed separately for topsoil and subsoil observations to account for depth effects.

### Meta-Analysis

#### Effect Size Calculation
The natural log of the response ratio (lnRR) was used as the effect size to measure the impact of sustainable agricultural practices on soil carbon stocks and crop yields. The lnRR was calculated for each paired observation, with the numerator being the mean yield or SOC stock of the sustainable practice and the denominator being the mean of the conventional practice. Observations were weighted by the inverse of the variance, and outliers were identified and removed based on a z-score threshold.

#### Univariate Mixed Effects Models
Univariate mixed effects models were fitted using the _rma.mv_ function from the _metafor_ package to visualize soil carbon and yield responses across different environmental and agronomic variables. Study sites were included as a random effect to account for potential non-independencies of data.

#### Variable Importance and Meta-Regressions
The study used the _metaforest_ package to fit meta-regression models, which are robust to overfitting and non-linear relationships. Recursive variable pre-selection was performed with 10,000 iterations and 100 replications, retaining variables that improved model performance in over 90% of iterations. Important predictors were identified using an importance threshold of 0.7. Meta-regressions were conducted to visualize the effects of important predictors on topsoil SOC and yield responses.

### Model Assumptions
Publication bias was assessed using funnel plots, Egger's regression tests, the trim-and-fill method, and Fail-Safe N Analysis. The representativeness of the dataset in terms of global distributions of important environmental covariates was also evaluated.

### Tools and Software
All statistical analyses were conducted in R v4.3.2 using packages such as _metafor_ for meta-analysis and _metaforest_ for meta-regression models. The _caret_ package was used for optimizing tuning hyperparameters.

### Datasets
Environmental and agronomic covariate data were supplemented with global gridded datasets, using latitude and longitude provided by the studies or based on the nearest landmark. The degree of saturation of mineral-associated organic carbon was derived from existing datasets.

### rstb.2024.0001

## Methods

The research presented in this paper was conducted through a series of targeted workshops and surveys involving UK- and USA-based wildfire science researchers from academic and government institutions. The methodological approach was designed to gather perspectives on wildfire science research needs from both historically wildfire-prone and emerging wildfire-prone countries, specifically the USA and the UK.

### Workshops

1. **Participant Selection**: Researchers from diverse disciplines within the physical sciences and engineering, affiliated with academic and government institutions in the UK and USA, were invited to participate. The selection aimed to capture a broad spectrum of expertise in wildfire science.

2. **Workshop Structure**: 
   - Three initial workshops were conducted in 2023, focusing on identifying global wildfire research challenges. Participants were encouraged to consider strengths, weaknesses, and opportunities for synergistic research collaborations between the two countries.
   - Discussions were open-ended to explore a wide range of ideas without limiting the direction of conversations. Recent notable wildfire events were often used as focal points for discussions.

3. **Themes Identification**: Through these workshops, four broad themes were identified:
   - Fire behaviour and fire danger
   - Wildland–urban interface/rural–urban interface (WUI/RUI) and social themes
   - Fire ecology and fire severity
   - Smoke and emissions

4. **Survey Dissemination**: An online survey was distributed to a wider group of wildfire researchers and attendees of the international Leverhulme Wildfire’s Summer Conference in July 2023. The survey aimed to gather additional insights on existing strengths in wildfire research and potential areas for international collaboration.

5. **Final Workshop**: A subsequent workshop was held with all participants to discuss the findings from the initial workshops and survey. This led to the identification of three key topic areas for wildfire research:
   - Understanding and predicting fire occurrence, fire behaviour, and fire impacts
   - Increasing human and ecosystem resilience to fire
   - Understanding the atmospheric and climate impacts of fire

### Data Collection and Analysis

- **Qualitative Data**: The workshops and surveys provided qualitative data on perceived research gaps and priorities in wildfire science. This data was analyzed to identify common themes and specific research questions within the identified topic areas.
- **Thematic Literature Review**: The research questions identified during the workshops guided a thematic literature review to contextualize the findings within the existing scientific literature.

### Limitations

The perspectives gathered through this methodological approach are limited to the views of the participating researchers and do not represent the full diversity of wildfire expertise at an international and transdisciplinary scale. The workshops and surveys were designed to provide a focused perspective on wildfire research needs, which may not encompass all possible viewpoints or areas of expertise.

### s11104-025-08031-z

## Methods

This mini-review synthesizes existing literature to propose a bottom-up framework for understanding the effects of fire on ecosystem biogeochemistry through plant-soil interactions. The methodological approach involves a comprehensive literature review and synthesis of previous studies on fire effects on soil processes, plant-soil interactions, and ecosystem biogeochemistry. The authors highlight key processes and mechanisms that are influenced by fire, including:

1. **Soil Carbon Saturation and Mineral Stabilization Dynamics**: The review discusses how fire affects soil carbon storage, particularly focusing on the dynamics of mineral-associated organic carbon versus free or aggregate-occluded particulate organic carbon. The authors emphasize the importance of understanding carbon accrual and stability in different contexts, such as boreal forests, tundra, savannas, and grasslands.

2. **Nutrient-Acquisition Strategies and Biogeochemical Feedbacks**: The review explores how fire influences nutrient cycling and plant-microbial symbioses, which in turn affect biogeochemical feedbacks. The authors discuss the role of microbial activity and plant-microbial interactions in nutrient acquisition and cycling, highlighting the importance of plant-microbial symbioses in fire-prone ecosystems.

3. **Physical Soil Changes**: The review addresses the direct effects of fire on soil physical properties, such as soil heating, hydrological dynamics, and organic matter decomposition. The authors discuss how fire-induced changes in soil structure and composition can influence microbial communities and soil carbon dynamics.

The review also incorporates findings from recent studies and meta-analyses to provide a comprehensive understanding of the complex interactions between fire, plant-soil interactions, and ecosystem biogeochemistry. The authors propose that a bottom-up perspective, which considers microbially mediated processes and direct thermal impacts on physical changes, is essential for explaining the myriad effects of fire on soil biogeochemistry. This approach contrasts with the traditional top-down perspective that focuses primarily on biomass inputs and aboveground processes.

### s41467-025-59272-6

## Methods

### Data Sources
The study utilized global datasets to analyze the risk of wildfires in timber production systems. The primary data sources included:

1. **Forest Management Data**: The map produced by Lesiv et al. (2022) was used, which provides data on forest management types across the world's forests at a 100 m resolution for the year 2015. This map categorizes forests into seven management types, of which three were used in this study: naturally regenerating forests with signs of management, plantation forests (short rotation, up to 15 years), and planted forests (longer rotation, over 15 years).

2. **Fire Data**: The study used the map of forest loss due to fire by Tyukavina et al. (2022), which identifies forest loss events caused by wildfires from 2001 to 2022 using MODIS and Landsat imagery. This dataset focuses on high-severity wildfires that result in significant forest cover loss.

### Spatial Analysis
The spatial analysis involved overlaying the forest management map with the fire data to calculate the total spatial extent and distribution of stand-replacing fires in timber-producing forests. The analysis was conducted using the R packages `sf` and `terra`.

### Statistical Matching
To control for confounding variables that might influence fire occurrence, statistical matching was employed:

- **Covariates**: Ten environmental and anthropogenic variables were considered, including elevation, slope, climate variables (temperature and precipitation), fire weather index, burn area history, tree cover, distance to roads, and population density.
- **Matching Technique**: Nearest neighbor matching was used, with exact matching for biome. The MatchIt package in R was utilized for this process. Propensity score matching with a caliper of 0.2 was selected as the most effective method based on diagnostic checks for covariate balance.

### Modelling
Generalized Additive Mixed Models (GAMMs) were fitted to the matched datasets to further resolve covariate imbalances:

- **Model Structure**: Forest management type was included as a parametric term, with numeric covariates as cubic regression smoothing splines. Random intercepts for country and biome, and interaction terms between biome and country, biome and management type, and biome and tree cover were included.
- **Spatial Autocorrelation**: X and Y coordinate splines were used to account for spatial autocorrelation. Post-fitting checks indicated no significant spatial autocorrelation except in the largest countries.

### Simulation and Analysis
A counterfactual approach was used to isolate the effect of forest management type on burn probability:

- **Simulation**: For each country, 1000 forest points were randomly sampled, and their outcomes (burn or non-burn) were simulated under both natural production and plantation management conditions.
- **Outcome Comparison**: The predicted burned area under both management types was compared to calculate the difference in burn probability.

### Data and Code Availability
All data used in the study are publicly available online, and the code for the analysis is provided in the supplementary information. The fire data can be accessed from the GLAD website, and the forest management data from Zenodo.

### s41558-023-01800-7

## Methods

### Meta-analysis
The study conducted a meta-analysis to evaluate the impact of altered fire regimes on soil organic carbon (SOC) storage in drylands. The meta-analysis included data from 53 sites with 434 replicate plots, focusing on ecosystems such as savannahs, grasslands, and seasonal woodlands and forests. The analysis considered fire return intervals ranging from 1 to 17 years, with a mean duration of 33 years for altered fire frequencies. The sites spanned a range of climatic conditions, with mean annual temperatures from 3.9 to 27.1 °C and mean annual precipitation from 342 to 2,448 mm yr⁻¹.

### Study Compilation and Overview
Data were compiled from existing literature and field surveys. The literature search targeted studies measuring the response of mineral soils to repeated burning, yielding 156 articles. The analysis focused on mineral soils, particularly the uppermost layers (<20 cm depth), as these are most responsive to burning. The majority of sites were from fire-manipulation experiments, with fire treatments prescribed and replicated at the landscape scale.

### Environmental Variables and Model Selection
The study used WorldClim data to obtain climate variables, focusing on mean annual temperature, precipitation seasonality, and aridity. Aridity was calculated using the Aridity Index, defined as the ratio of mean annual precipitation to mean annual potential evapotranspiration. Soil texture data were compiled from study site measurements or extrapolated based on soil classification. The meta-analysis employed Akaike Information Criterion-based model selection on mixed-effects meta-regression models to identify important environmental variables influencing SOC changes.

### Statistical Analysis
Log response ratios of SOC concentrations in high-frequency fire plots relative to unburned plots were calculated. The analysis used multivariate meta-analysis models to determine overall effects and 95% confidence intervals. Model selection was performed using the glmulti package in R, considering first-order effects of environmental variables.

### Field Sampling and δ¹³C Analysis
Field sampling was conducted in six long-duration fire-manipulation experiments across South Africa, Brazil, and North America. Soil samples were collected from the top 0–20 cm of the mineral horizon, and δ¹³C was measured to partition tree vs. grass biomass contributions to SOC. Isotopic mixing models were used to calculate the proportion of SOC derived from C3 trees vs. C4 grasses.

### Fire Model Intercomparison Project Simulations
The study compared empirical findings with simulations from seven fire-enabled Dynamic Global Vegetation Models (DGVMs) provided by the Fire Model Intercomparison Project (FireMIP). Simulations included a fully transient scenario with fire and a sensitivity experiment without fire to assess the long-term impact of fire on SOC.

### Upscaling Calculations
The statistical model of fire effects on SOC was upscaled to global savannah–grasslands using environmental covariates and SOC content from global maps. Trends in burned area from 1998 to 2015 were used to estimate potential SOC changes, with areas experiencing declines in burned area potentially gaining SOC and areas with increasing fire frequency potentially losing SOC.

### s41561-024-01384-7

## Methods

### Data Sources and Processing

The study utilized observationally derived climate and edaphic datasets at a 0.5 × 0.5° resolution to analyze soil carbon (C) stocks, focusing on unprotected (particulate) and protected (mineral-associated) C pools. Mean annual temperature (MAT) was estimated from the CRU dataset (version 3.10), and mean annual precipitation was sourced from the GPCC dataset. Land cover data were obtained from the MODIS MCD12C1 product, and productivity was estimated using the MODIS net primary productivity product. Soil organic C stocks to a depth of 1 m were estimated as the mean of the Harmonized World Soil Database and SoilGrids maps. Mineral-associated C stocks were estimated using a machine-learning (random forest) algorithm, with cross-validation approaches to assess predictability. The study focused on non-permafrost mineral soils with MAT > 0 °C, excluding soils with more than 50% peat coverage or those in hyperarid regions.

### Global Land Model Output

Model outputs were sourced from CMIP6 Earth System Models (ESMs) and three offline biogeochemical testbed models for historical and future projections. The study used models that reported soil C pool distributions, with details listed in supplementary tables. Carbon stocks and climate covariates were averaged over specific periods to match observation-based quantities. The study used total soil C stocks from CMIP6 models, with protected C estimated from the slowest-cycling pools in both CMIP6 and offline models. The study excluded TaiESM1 due to its unique parameterization and focused on models broadly based on the Century model.

### Model Pool Interpretability

The study compared protected C across different model formulations, recognizing inherent mismatches between operationally defined soil C fractions and modelled states. The passive pool in first-order models was aligned with mineral-associated fractions, with turnover times consistent with radiocarbon estimates. The study emphasized the need for detailed documentation on parameterizations in CMIP ESMs and encouraged future benchmarking studies to refine model formulations.

### Data Analysis

The relationship between soil C stocks and MAT was investigated using log-transformed data and linear regression to reflect an exponential relationship with temperature. Multiple linear regression controlled for confounding variables such as productivity, precipitation, and clay and silt content. Climatological temperature sensitivity was calculated as the proportional decline in C stocks for every 10 °C increase in MAT, with analyses performed across different temperature regimes. The study used observational synthesis to validate temperature sensitivity trends and deemed differences statistically significant when 95% confidence intervals did not overlap.

### s41561-025-01735-y

## Methods

### Data Compilation and Sampling
The study compiled a comprehensive global dataset consisting of 56,031 plankton (particulate) and 388,515 seawater (dissolved) samples collected from 1971 to 2020. These samples were collected from various depths ranging from the surface to 1,000 meters across major ocean basins. The dataset was used to assess spatial and temporal dynamics in marine C:N:P ratios.

### Stoichiometric Analysis
- **Planktonic Stoichiometry**: The analysis of planktonic ecological stoichiometry was based on particulate organic carbon, nitrogen, and phosphorus. The samples were collected on glass fiber filters and analyzed using combustion gas chromatography–infrared spectroscopy elemental analyzers.
- **Oceanic Stoichiometry**: For oceanic stoichiometry, dissolved inorganic carbon, nitrate plus nitrite, and phosphate were measured. These measurements followed globally standardized protocols.

### Statistical Framework
- **Redfield Ratio Comparison**: The study employed Redfield's statistical framework to calculate the stoichiometric ratios using median values of C:N:P. The biological activity ratio was derived from the slopes of least-squares fitted equations correlating C, N, and P molar concentrations.
- **Confidence Intervals and Statistical Testing**: Confidence intervals for the medians were computed to evaluate the variability of marine ecological stoichiometry relative to the Redfield ratio. The Wilcoxon rank-sum test was used to assess the significance of differences between current stoichiometric ratios and the Redfield ratio.

### Visualization and Data Analysis
- **Density Maps**: The R package 'Hexbin' was used to visualize the distribution of C:N:P ratios across different oceanic zones. The concentration range of oceanic C, N, and P was divided into hexagonal cells to represent specific regions, with density reflected by the number of data points within each hexagon.
- **Vertical and Temporal Trends**: The study applied power and exponential functions to model depth-dependent variations in oceanic stoichiometry. Temporal trends were analyzed using area-weighted averages across global marine regions, and breakpoints in linear fits were identified using the 'segmented' package in R.

### Depth and Temporal Analysis
- **Depth-Dependent Variability**: The study observed notable depth variability in oceanic stoichiometry, modeled using relative changes in concentrations and ratios of C, N, and P with increasing depth.
- **Temporal Trends**: Temporal changes in stoichiometric ratios from 1971 to 2020 were assessed using segmented regression analysis to identify potential shifts in marine ecological stoichiometry.

### Data Availability
The datasets generated and analyzed during the study are available via figshare, providing access to the comprehensive data used in the analysis.

### v1_covered_6e57e2fa-8f17-4450-93e7-975b221490dd

## Methods

### Climate Conditions and Fuel Load

The study utilized data from NASA's Soil Moisture Active Passive (SMAP) mission to assess climatic and environmental conditions around the Dava Moor fire. SMAP provides observations in the microwave spectrum to track soil moisture and vegetation optical depth (VOD), which are indicators of water content in soils and vegetation. The SMAP soil moisture data, derived from the baseline single channel algorithm (SMAP-SCA), and VOD data from the dual channel algorithm (DCA), were used to analyze monthly anomalies relative to the 2015-2025 long-term average. Additionally, monthly precipitation estimates from the Met Office’s HadUK-Grid dataset were used to further assess dry conditions, converted to monthly anomalies.

The Fire Weather Index (FWI) was analyzed using data from the Canadian Forest Service Fire Weather Index Rating System, accessed via the Copernicus Climate Change Service.

### Characterizing Fire Behavior and Severity

Fire behavior was characterized using fire radiative power data from VIIRS (375m resolution) and MODIS (500m resolution), which helped track the evolution of the fire front. The fire extent and severity were mapped using Sentinel-2 imagery at 20 m resolution, with burn severity assessed using the differenced Normalized Burn Ratio (dNBR) and relative dNBR (RdNBR). Pre- and post-fire images were used to calculate dNBR, with severity categories defined as unchanged, low, moderate, and high.

Land cover classification data from the UK Centre for Ecology and Hydrology (2023) were used to categorize burned areas into 'Bogs', 'Moorlands and Heathlands', 'Forests and Woodlands', and 'Other Natural'. These classifications were used to assign carbon stock values for emissions modeling.

A field sampling campaign was conducted to measure peat burn depth across the wildfire area. Measurements were taken at 107 locations within the burn scar, using a 200 m grid, to determine maximum and minimum burn depths, which were averaged to estimate peat burn depth.

### Quantifying Carbon Emissions

Carbon emissions were quantified using a bottom-up approach, considering both aboveground and belowground emissions. Aboveground emissions were calculated by multiplying the burned fraction, available biomass carbon, combustion completeness, and carbon fraction for each vegetation class within burned pixels.

For belowground emissions, two approaches were used:

1. **Field Data Approach**: Burn depths were constrained by field data, using the 25th, 50th, and 75th quantiles of field-measured burn depths within burn severity classes. The mean bulk density used was 58.2 ± 38.75 Mg m^-3, determined from nearby intact heathland measurements.

2. **Model Approach**: A UK-wide model estimated peat combustion based on a soil moisture scaler, considering only the 'Bog' land cover fraction. Peat stocks were estimated using a gridded peat map of Scotland, with peat burn depth calculated using soil moisture data from SMAP.

Total fire carbon emissions were calculated as the sum of above- and belowground losses. These estimates were compared with values from the Global Fire Assimilation System (GFAS), which uses fire radiative power to estimate emissions.

### Data Sources and Tools

- **SMAP**: Soil moisture and VOD data for climatic analysis.
- **HadUK-Grid**: Precipitation data for assessing dry conditions.
- **Sentinel-2**: Satellite imagery for mapping fire extent and severity.
- **VIIRS and MODIS**: Fire radiative power data for characterizing fire behavior.
- **Land Cover Data**: From the UK Centre for Ecology and Hydrology for emissions modeling.
- **Field Sampling**: For measuring peat burn depths and validating model estimates.
- **GFAS**: For comparison of emissions estimates.