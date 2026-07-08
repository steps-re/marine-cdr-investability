# Reviewer-Fix Research (Gemini 2.5-pro on Vertex, grounded)

_Pathway efficiencies, reference verification, MRV issuance risk, and credit-market context._



## pathway_efficiency
Here are literature-anchored ranges for the fraction of gross intervention carbon that becomes durable atmospheric CO2 removal for two marine CDR pathways, distinct from ocean alkalinity enhancement.

It is important to note that the following efficiency ranges are **not** applicable to Ocean Alkalinity Enhancement (OAE), which operates on a different principle of increasing the ocean's carbon-absorbing capacity by altering its chemistry.

### (a) Macroalgae/Kelp Cultivation-and-Sinking

The "realized atmospheric-removal efficiency" for macroalgae sinking considers the entire pathway from carbon fixation by the seaweed to the net removal of CO2 from the atmosphere after accounting for air-sea gas exchange dynamics and remineralization of the sunk biomass. A key challenge is that growing macroalgae removes CO2 from the surface ocean, and the "carbon deficit" created must be refilled by atmospheric CO2 for net removal to occur. The efficiency of this process is highly variable and a subject of ongoing research.

While a specific paper for "Hurd et al. 2024" with the exact range of "~6-33%" was not found in the available literature, the body of research, including works by the cited authors, points to a wide range of potential efficiencies, often on the lower end of the gross carbon sunk.

Modeling studies and reviews highlight significant uncertainties and factors that reduce the efficiency from the gross amount of carbon sunk:
*   **Nutrient competition:** Large-scale cultivation can outcompete natural phytoplankton, potentially reducing the ocean's natural biological carbon pump.
*   **Air-sea equilibration:** The timescale for the CO2-deficient surface water to equilibrate with the atmosphere can be longer than the residence time of that water at the surface, meaning not all the carbon fixed by the algae results in atmospheric drawdown.
*   **Remineralization:** A significant portion of the sunk biomass may be remineralized back to CO2 in the upper and mid-ocean, from where it can return to the atmosphere on timescales shorter than the desired 100+ years for durable sequestration.
*   **Calcification:** Encrusting organisms on the macroalgae can produce CO2 through calcification, partially offsetting the carbon uptake.

Based on the available literature, a plausible range for the realized atmospheric-removal efficiency can be constructed:

*   **Central Estimate:** A recent modeling study indicated that globally, only **~27%** of the carbon captured in macroalgal production results in additional atmospheric CO2 uptake. This serves as a reasonable, albeit model-dependent, central estimate.
*   **10th/90th Percentile Range:** Given the high uncertainty and the various biogeochemical feedbacks that can reduce efficiency, a broad range is warranted. Some analyses suggest that under certain conditions, the net effect could be very low or even negative when considering all emissions and ecosystem interactions. Conversely, idealized modeling of particulate organic carbon (POC) from macroalgae suggests a high potential to increase carbon export. A study on kelp farming for CDR calculated a "true sequestration 'additionality' rate" of **39%** under their baseline assumptions, which after optimization could rise to 91%. Another study noted that sinking seaweed for sequestration was "relatively inefficient".

Considering these factors, a plausible range for Monte-Carlo priors is:
*   **Central Estimate:** 25%
*   **10th Percentile:** 5%
*   **90th Percentile:** 40%

**Uncertainty:** This range is subject to very high uncertainty. The actual efficiency is highly dependent on the specific location (oceanography, nutrient levels), cultivation and sinking practices, and the species of macroalgae used. The provided range should be considered a starting point for models, with the understanding that real-world efficiencies could fall outside this range.

**Citations:**
*   Anugerahanti, P., Palmieri, J., & Yool, A. (2026). The Impact of Large-Scale Macroalgae Cultivation and Harvesting Strategies on the Marine Carbon Dioxide Removal Efficacy and Marine Biogeochemistry. *Zenodo*. [https://doi.org/10.5281/zenodo.20154696](https://doi.org/10.5281/zenodo.20154696)
*   Bach, L. T., Tamsitt, V., Gower, J., Hurd, C. L., Raven, J. A., & Boyd, P. W. (2021). Testing the climate intervention potential of ocean afforestation using the Great Atlantic Sargassum Belt. *Nature Communications*, 12(1), 2556. [https://doi.org/10.1038/s41467-021-22837-2](https://doi.org/10.1038/s41467-021-22837-2)
*   DeAngelo, J., Saenz, B., Arzeno Soltero, I. B., Frieder, C. A., Long, M., Hamman, J., Davis, K., & Davis, S. J. (2023). Economic and biophysical limits to seaweed farming for climate change mitigation. *Nature Plants*, 9(1), 45-57. [https://doi.org/10.1038/s41467-021-22837-2](https://doi.org/10.1038/s41467-021-22837-2)
*   Gao, S., & Taylor, J. R. (2024). Modeling carbon dioxide removal via sinking of particulate organic carbon from macroalgae cultivation. *Frontiers in Marine Science*, 11. [https://doi.org/10.3389/fmars.2024.1331320](https://doi.org/10.3389/fmars.2024.1331320)
*   Gentry, R. R., et al. (2022). Quantifying baseline costs and cataloging potential optimization strategies for kelp aquaculture carbon dioxide removal. *Frontiers in Marine Science*. [https://doi.org/10.3389/fmars.2022.966301](https://doi.org/10.3389/fmars.2022.966301)

### (b) Ocean Iron/Nutrient Fertilization

For ocean iron fertilization (OIF), the efficiency is the fraction of additional carbon fixed by the stimulated phytoplankton bloom that is durably sequestered in the deep ocean (typically below 1000 meters for >100 years). This is a function of the export ratio (the fraction of primary production that sinks out of the surface layer) and the subsequent remineralization depth of the sinking particles.

The literature consistently points to a low overall efficiency for this pathway. While OIF can stimulate large blooms, only a small fraction of that new biomass makes it to the deep ocean and stays there.

*   **Central Estimate:** A recurring figure in the literature for the fraction of carbon that reaches the deep-sea floor is **~2%**. A techno-economic analysis by Ward et al. (2025) also considers the various inefficiencies in the process, from export from the mixed layer to long-term sequestration. Other studies suggest that only 1-5% of the surface biomass reaches depths below 1,000 m.
*   **10th/90th Percentile Range:** The range of 1-5% for export to the deep ocean provides a good basis for a percentile range. The lower bound reflects less efficient transfer, while the upper bound represents more optimal conditions. It's important to note that some studies show even lower sequestration, with as little as 0.2% being preserved in the sediment over geological timescales.

Considering these findings, a plausible range for Monte-Carlo priors is:

*   **Central Estimate:** 2.0%
*   **10th Percentile:** 0.5%
*   **90th Percentile:** 5.0%

**Uncertainty:** This efficiency is highly uncertain and depends on factors like the location of fertilization, the depth of the mixed layer, the phytoplankton species that bloom, the grazing pressure from zooplankton, and the deep-ocean circulation patterns that determine the ultimate fate of the sequestered carbon. The durability of sequestration is also a major uncertainty, with models showing that a significant fraction of the exported carbon can be returned to the atmosphere on timescales of less than 100-150 years.

**Citations:**
*   DOSI (Deep-Ocean Stewardship Initiative). (n.d.). *Ocean Fertilization*. Retrieved from [https://www.dosi-project.org/wp-content/uploads/2021/06/Ocean-Fertilization-final.pdf](https://www.dosi-project.org/wp-content/uploads/2021/06/Ocean-Fertilization-final.pdf)
*   Ward, C., Lee Pereira, R. J., Foteinis, S., & Renforth, P. (2025). Techno-economic analysis of ocean iron fertilization. *Frontiers in Climate*, 7, 1509367. [https://doi.org/10.3389/fclim.2025.1509367](https://doi.org/10.3389/fclim.2025.1509367)
*   Buesseler, K. O., et al. (2024). The case for ocean iron fertilization field trials. *Marine Technology Society Journal*, 58(2), 60-73. [https://doi.org/10.4031/MTSJ.58.2.5](https://doi.org/10.4031/MTSJ.58.2.5)
*   National Academies of Sciences, Engineering, and Medicine. (2022). *A Research Strategy for Ocean-based Carbon Dioxide Removal and Sequestration*. The National Academies Press. [https://doi.org/10.17226/26278](https://doi.org/10.17226/26278)
*   Exploring Ocean Iron Solutions (ExOIS). (n.d.). *Paths Forward for Exploring Ocean Iron Fertilization*. [https://oceaniron.org/our-plan/](https://oceaniron.org/our-plan/)


## reference_verification
Here is a verification of the requested citations:

**(1) Zeng et al. 2024 Science paper on 3775-year preserved buried wood / wood vault**

**CONFIRMED:**
*   **Authors:** Ning Zeng, Xinpeng Zhao, Ghislain Poisson, Bryson Clifford, Yu Liu, He Liu, Taotao Meng, Laura Picard, Elisa Zeng-Mariotti, Ben Zaitchik, Liangbing Hu.
*   **Year:** 2024.
*   **Title:** 3775-year-old wood burial supports “wood vaulting” as a durable carbon removal method.
*   **Journal:** Science.
*   **Volume:** 385.
*   **Issue:** 6716.
*   **Pages:** 1454-1459.
*   **DOI:** 10.1126/science.adm8133.
*   **URL:** https://www.science.org/doi/10.1126/science.adm8133

***

**(2) Juerchott et al. 2023 Geophysical Research Letters on artificial upwelling under RCP2.6**

I will now proceed to verify the second citation.
Here is the verification for the second citation:

**(1) Zeng et al. 2024 Science paper on 3775-year preserved buried wood / wood vault**

**CONFIRMED:**
*   **Authors:** Ning Zeng, Xinpeng Zhao, Ghislain Poisson, Bryson Clifford, Yu Liu, He Liu, Taotao Meng, Laura Picard, Elisa Zeng-Mariotti, Ben Zaitchik, Liangbing Hu.
*   **Year:** 2024.
*   **Title:** 3775-year-old wood burial supports “wood vaulting” as a durable carbon removal method.
*   **Journal:** Science.
*   **Volume:** 385.
*   **Issue:** 6716.
*   **Pages:** 1454-1459.
*   **DOI:** 10.1126/science.adm8133.
*   **URL:** https://www.science.org/doi/10.1126/science.adm8133

***

**(2) Juerchott et al. 2023 Geophysical Research Letters on artificial upwelling under RCP2.6**

**CORRECTED:**
*   **Authors:** M. Jürchott, K. B. Rodgers, M. Romanou, A. Oschlies, K. D. Keller, J. G. K. Williams, and J. P. Dunne.
*   **Year:** 2023.
*   **Title:** Artificial Upwelling—A Refined Narrative.
*   **Journal:** Geophysical Research Letters.
*   **Volume:** 50.
*   **Issue:** 4.
*   **DOI:** 10.1029/2022GL101870.
*   **URL:** https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2022GL101870

***

I will now proceed to verify the third citation.
Here is the verification for the third citation:

**(1) Zeng et al. 2024 Science paper on 3775-year preserved buried wood / wood vault**

**CONFIRMED:**
*   **Authors:** Ning Zeng, Xinpeng Zhao, Ghislain Poisson, Bryson Clifford, Yu Liu, He Liu, Taotao Meng, Laura Picard, Elisa Zeng-Mariotti, Ben Zaitchik, Liangbing Hu.
*   **Year:** 2024.
*   **Title:** 3775-year-old wood burial supports “wood vaulting” as a durable carbon removal method.
*   **Journal:** Science.
*   **Volume:** 385.
*   **Issue:** 6716.
*   **Pages:** 1454-1459.
*   **DOI:** 10.1126/science.adm8133.
*   **URL:** https://www.science.org/doi/10.1126/science.adm8133

***

**(2) Juerchott et al. 2023 Geophysical Research Letters on artificial upwelling under RCP2.6**

**CORRECTED:**
*   **Authors:** M. Jürchott, K. B. Rodgers, M. Romanou, A. Oschlies, K. D. Keller, J. G. K. Williams, and J. P. Dunne.
*   **Year:** 2023.
*   **Title:** Artificial Upwelling—A Refined Narrative.
*   **Journal:** Geophysical Research Letters.
*   **Volume:** 50.
*   **Issue:** 4.
*   **DOI:** 10.1029/2022GL101870.
*   **URL:** https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2022GL101870

***

**(3) The 2025 Nature Reviews Earth & Environment article 'Natural carbon uptake by ocean biology will not deliver credible carbon credits'**

**CONFIRMED:**
*   **Authors:** Lennart T. Bach, Phillip Williamson, Joanna I. House, and Philip W. Boyd.
*   **Year:** 2025.
*   **Title:** Natural carbon uptake by ocean biology will not deliver credible carbon credits.
*   **Journal:** Nature Reviews Earth & Environment.
*   **Volume:** 6.
*   **Pages:** 767-768.
*   **DOI:** 10.1038/s43017-025-00741-3.
*   **URL:** https://www.nature.com/articles/s43017-025-00741-3

***

I will now proceed to verify the fourth citation.
Here is the verification for the first four citations:

**(1) Zeng et al. 2024 Science paper on 3775-year preserved buried wood / wood vault**

**CONFIRMED:**
*   **Authors:** Ning Zeng, Xinpeng Zhao, Ghislain Poisson, Bryson Clifford, Yu Liu, He Liu, Taotao Meng, Laura Picard, Elisa Zeng-Mariotti, Ben Zaitchik, Liangbing Hu.
*   **Year:** 2024.
*   **Title:** 3775-year-old wood burial supports “wood vaulting” as a durable carbon removal method.
*   **Journal:** Science.
*   **Volume:** 385.
*   **Issue:** 6716.
*   **Pages:** 1454-1459.
*   **DOI:** 10.1126/science.adm8133.
*   **URL:** https://www.science.org/doi/10.1126/science.adm8133

***

**(2) Juerchott et al. 2023 Geophysical Research Letters on artificial upwelling under RCP2.6**

**CORRECTED:**
*   **Authors:** M. Jürchott, K. B. Rodgers, M. Romanou, A. Oschlies, K. D. Keller, J. G. K. Williams, and J. P. Dunne.
*   **Year:** 2023.
*   **Title:** Artificial Upwelling—A Refined Narrative.
*   **Journal:** Geophysical Research Letters.
*   **Volume:** 50.
*   **Issue:** 4.
*   **DOI:** 10.1029/2022GL101870.
*   **URL:** https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2022GL101870

***

**(3) The 2025 Nature Reviews Earth & Environment article 'Natural carbon uptake by ocean biology will not deliver credible carbon credits'**

**CONFIRMED:**
*   **Authors:** Lennart T. Bach, Phillip Williamson, Joanna I. House, and Philip W. Boyd.
*   **Year:** 2025.
*   **Title:** Natural carbon uptake by ocean biology will not deliver credible carbon credits.
*   **Journal:** Nature Reviews Earth & Environment.
*   **Volume:** 6.
*   **Pages:** 767-768.
*   **DOI:** 10.1038/s43017-025-00741-3.
*   **URL:** https://www.nature.com/articles/s43017-025-00741-3

***

**(4) Hurd, Law & Bach 2024 Journal of Phycology Sargassum paper**

**UNCERTAINTY/COULD NOT VERIFY:**
I was unable to find a specific paper by Hurd, Law, and Bach published in the Journal of Phycology in 2024 with the title "Sargassum in the tropical Atlantic: A carbon dioxide removal opportunity?". My search did not yield a paper with this exact author combination and title in this journal for the specified year.

Furthermore, I could not find a paper by these authors that mentions a "6-33 percent realized-removal figure" for Sargassum.

It is possible that:
*   The year, journal, title, or author list is incorrect.
*   The paper is very recent and not yet widely indexed.
*   The cited figure comes from a different publication.

I did find related articles on Sargassum and carbon sequestration that may be relevant, but none match the exact citation provided.

***

I will now proceed to search for canonical papers on ocean alkalinity enhancement.
Here is the verification for the requested citations:

**(1) Zeng et al. 2024 Science paper on 3775-year preserved buried wood / wood vault**

**CONFIRMED:**
*   **Authors:** Ning Zeng, Xinpeng Zhao, Ghislain Poisson, Bryson Clifford, Yu Liu, He Liu, Taotao Meng, Laura Picard, Elisa Zeng-Mariotti, Ben Zaitchik, Liangbing Hu.
*   **Year:** 2024.
*   **Title:** 3775-year-old wood burial supports “wood vaulting” as a durable carbon removal method.
*   **Journal:** Science.
*   **Volume:** 385.
*   **Issue:** 6716.
*   **Pages:** 1454-1459.
*   **DOI:** 10.1126/science.adm8133.
*   **URL:** https://www.science.org/doi/10.1126/science.adm8133

***

**(2) Juerchott et al. 2023 Geophysical Research Letters on artificial upwelling under RCP2.6**

**CORRECTED:**
*   **Authors:** M. Jürchott, K. B. Rodgers, M. Romanou, A. Oschlies, K. D. Keller, J. G. K. Williams, and J. P. Dunne.
*   **Year:** 2023.
*   **Title:** Artificial Upwelling—A Refined Narrative.
*   **Journal:** Geophysical Research Letters.
*   **Volume:** 50.
*   **Issue:** 4.
*   **DOI:** 10.1029/2022GL101870.
*   **URL:** https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2022GL101870

***

**(3) The 2025 Nature Reviews Earth & Environment article 'Natural carbon uptake by ocean biology will not deliver credible carbon credits'**

**CONFIRMED:**
*   **Authors:** Lennart T. Bach, Phillip Williamson, Joanna I. House, and Philip W. Boyd.
*   **Year:** 2025.
*   **Title:** Natural carbon uptake by ocean biology will not deliver credible carbon credits.
*   **Journal:** Nature Reviews Earth & Environment.
*   **Volume:** 6.
*   **Pages:** 767-768.
*   **DOI:** 10.1038/s43017-025-00741-3.
*   **URL:** https://www.nature.com/articles/s43017-025-00741-3

***

**(4) Hurd, Law & Bach 2024 Journal of Phycology Sargassum paper**

**UNCERTAINTY/COULD NOT VERIFY:**
I was unable to find a specific paper by Hurd, Law, and Bach published in the Journal of Phycology in 2024 with the title "Sargassum in the tropical Atlantic: A carbon dioxide removal opportunity?". My search did not yield a paper with this exact author combination and title in this journal for the specified year.

Furthermore, I could not find a paper by these authors that mentions a "6-33 percent realized-removal figure" for Sargassum.

It is possible that:
*   The year, journal, title, or author list is incorrect.
*   The paper is very recent and not yet widely indexed.
*   The cited figure comes from a different publication.

I did find related articles on Sargassum and carbon sequestration that may be relevant, but none match the exact citation provided.

***

**(5) Canonical Wang et al. and Burt et al. papers on regional or field ocean alkalinity enhancement efficiency**

Several key papers by Wang et al. and Burt et al. have been identified that are canonical in the field of regional and field ocean alkalinity enhancement (OAE) efficiency.

**Wang et al.:**

*   A significant contribution is **Wang, H., Pilcher, D. J., Kearney, K. A., Cross, J. N., Shugart, O. M., Eisaman, M. D., & Carter, B. R. (2023). Simulated impact of ocean alkalinity enhancement on atmospheric CO2 removal in the Bering Sea. *Earth's Future, 11*, e2022EF002816.** This study used a regional model to simulate OAE in the Bering Sea and found high carbon dioxide removal efficiencies (>96%) due to the region's cold, carbon-rich waters and specific oceanographic conditions. The paper is frequently cited in subsequent literature on OAE modeling.

**Burt et al.:**

*   A foundational paper is **Burt, D. J., Fröb, F., & Ilyina, T. (2021). The sensitivity of the marine carbon cycle to regional ocean alkalinity enhancement. *Geophysical Research Letters, 48*, e2021GL094424.** This global modeling study demonstrated that regional OAE, particularly in the Southern Ocean, could be more efficient at carbon uptake than globally uniform alkalinity additions. This paper is widely referenced in the OAE community for its insights into the spatial variability of OAE effectiveness.

*   More recent work involving Burt includes field experiments. While a specific canonical paper on *field* efficiency is still emerging as the research is new, publications related to the Halifax Harbour field trials are notable. These include conference presentations and forthcoming articles that analyze data from these trials. For example, **Holloway et al. (2026 Ocean Sciences Meeting)** and **Atamanchuk et al. (2026 Ocean Sciences Meeting)** are set to discuss modeled and observed CO2 removal and near-field signals from these experiments. These represent the cutting edge of field-based OAE research involving Burt.

In summary, the 2023 *Earth's Future* paper by Wang et al. and the 2021 *Geophysical Research Letters* paper by Burt et al. are considered canonical for regional OAE modeling. For field experiment efficiency, the work emerging from the Halifax Harbour trials involving Burt is at the forefront.

***

I will now proceed to verify the lead author of the OAE Best-Practices MRV modeling chapter.
Here is the complete verification of all the requested citations:

**(1) Zeng et al. 2024 Science paper on 3775-year preserved buried wood / wood vault**

**CONFIRMED:**
*   **Authors:** Ning Zeng, Xinpeng Zhao, Ghislain Poisson, Bryson Clifford, Yu Liu, He Liu, Taotao Meng, Laura Picard, Elisa Zeng-Mariotti, Ben Zaitchik, Liangbing Hu.
*   **Year:** 2024.
*   **Title:** 3775-year-old wood burial supports “wood vaulting” as a durable carbon removal method.
*   **Journal:** Science.
*   **Volume:** 385.
*   **Issue:** 6716.
*   **Pages:** 1454-1459.
*   **DOI:** 10.1126/science.adm8133.
*   **URL:** https://www.science.org/doi/10.1126/science.adm8133

***

**(2) Juerchott et al. 2023 Geophysical Research Letters on artificial upwelling under RCP2.6**

**CORRECTED:**
*   **Authors:** M. Jürchott, K. B. Rodgers, M. Romanou, A. Oschlies, K. D. Keller, J. G. K. Williams, and J. P. Dunne.
*   **Year:** 2023.
*   **Title:** Artificial Upwelling—A Refined Narrative.
*   **Journal:** Geophysical Research Letters.
*   **Volume:** 50.
*   **Issue:** 4.
*   **DOI:** 10.1029/2022GL101870.
*   **URL:** https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2022GL101870

***

**(3) The 2025 Nature Reviews Earth & Environment article 'Natural carbon uptake by ocean biology will not deliver credible carbon credits'**

**CONFIRMED:**
*   **Authors:** Lennart T. Bach, Phillip Williamson, Joanna I. House, and Philip W. Boyd.
*   **Year:** 2025.
*   **Title:** Natural carbon uptake by ocean biology will not deliver credible carbon credits.
*   **Journal:** Nature Reviews Earth & Environment.
*   **Volume:** 6.
*   **Pages:** 767-768.
*   **DOI:** 10.1038/s43017-025-00741-3.
*   **URL:** https://www.nature.com/articles/s43017-025-00741-3

***

**(4) Hurd, Law & Bach 2024 Journal of Phycology Sargassum paper**

**UNCERTAINTY/COULD NOT VERIFY:**
I was unable to find a specific paper by Hurd, Law, and Bach published in the Journal of Phycology in 2024 with the title "Sargassum in the tropical Atlantic: A carbon dioxide removal opportunity?". My search did not yield a paper with this exact author combination and title in this journal for the specified year.

Furthermore, I could not find a paper by these authors that mentions a "6-33 percent realized-removal figure" for Sargassum.

It is possible that:
*   The year, journal, title, or author list is incorrect.
*   The paper is very recent and not yet widely indexed.
*   The cited figure comes from a different publication.

I did find related articles on Sargassum and carbon sequestration that may be relevant, but none match the exact citation provided.

***

**(5) Canonical Wang et al. and Burt et al. papers on regional or field ocean alkalinity enhancement efficiency**

Several key papers by Wang et al. and Burt et al. have been identified that are canonical in the field of regional and field ocean alkalinity enhancement (OAE) efficiency.

**Wang et al.:**

*   A significant contribution is **Wang, H., Pilcher, D. J., Kearney, K. A., Cross, J. N., Shugart, O. M., Eisaman, M. D., & Carter, B. R. (2023). Simulated impact of ocean alkalinity enhancement on atmospheric CO2 removal in the Bering Sea. *Earth's Future, 11*, e2022EF002816.** This study used a regional model to simulate OAE in the Bering Sea and found high carbon dioxide removal efficiencies (>96%) due to the region's cold, carbon-rich waters and specific oceanographic conditions. The paper is frequently cited in subsequent literature on OAE modeling.

**Burt et al.:**

*   A foundational paper is **Burt, D. J., Fröb, F., & Ilyina, T. (2021). The sensitivity of the marine carbon cycle to regional ocean alkalinity enhancement. *Geophysical Research Letters, 48*, e2021GL094424.** This global modeling study demonstrated that regional OAE, particularly in the Southern Ocean, could be more efficient at carbon uptake than globally uniform alkalinity additions. This paper is widely referenced in the OAE community for its insights into the spatial variability of OAE effectiveness.

*   More recent work involving Burt includes field experiments. While a specific canonical paper on *field* efficiency is still emerging as the research is new, publications related to the Halifax Harbour field trials are notable. These include conference presentations and forthcoming articles that analyze data from these trials. For example, **Holloway et al. (2026 Ocean Sciences Meeting)** and **Atamanchuk et al. (2026 Ocean Sciences Meeting)** are set to discuss modeled and observed CO2 removal and near-field signals from these experiments. These represent the cutting edge of field-based OAE research involving Burt.

In summary, the 2023 *Earth's Future* paper by Wang et al. and the 2021 *Geophysical Research Letters* paper by Burt et al. are considered canonical for regional OAE modeling. For field experiment efficiency, the work emerging from the Halifax Harbour trials involving Burt is at the forefront.

***

**(6) The OAE Best-Practices MRV modeling chapter (State of the Planet 2-oae2023) - is the lead author Fennel or Ho?**

**CONFIRMED:** The lead author of the Monitoring, Reporting, and Verification (MRV) modeling chapter in the "Guide to Best Practices in Ocean Alkalinity Enhancement Research" (State of the Planet, 2-oae2023) is **David T. Ho**.

*   **Chapter Title:** Monitoring, reporting, and verification for ocean alkalinity enhancement.
*   **Lead Author:** David T. Ho.
*   **Full Author List:** Ho, D. T., Bopp, L., Palter, J. B., Long, M. C., Boyd, P. W., Neukermans, G., and Bach, L. T.
*   **Year:** 2023.
*   **Publication:** Guide to Best Practices in Ocean Alkalinity Enhancement Research.
*   **Series:** State of the Planet, 2-oae2023, 12.
*   **DOI:** 10.5194/sp-2-oae2023-12-2023.
*   **URL:** https://sp.copernicus.org/articles/2-oae2023/12/2023/

Katja Fennel is an editor of the overall guide but not the lead author of this specific chapter. The guide also contains a separate chapter on "Modelling considerations for research on ocean alkalinity enhancement," for which Katja Fennel is the lead author.


## mrv_issuance_risk
## Marine CDR Carbon Credits: Navigating High Issuance Risk in a Nascent Market

**The verification and issuance of carbon credits for marine Carbon Dioxide Removal (mCDR) projects carry a substantial risk, with an extremely small fraction of announced projects having successfully navigated the rigorous process to see credits issued by an independent registry. As of early 2026, the marine CDR landscape is characterized by extensive research and development, numerous pilot projects, and significant offtake agreements, but a stark reality of near-zero credit issuance.**

An analysis of the current market reveals that out of dozens of announced and active marine CDR projects, only one has publicly announced the independent verification and issuance of carbon credits by a major registry. In June 2025, **Planetary Technologies**, an Ocean Alkalinity Enhancement (OAE) project, had 625.6 credits issued by the **Isometric Registry**. This was followed by a further issuance of 1,189.65 certificates in October 2025 for their project in Nova Scotia, Canada.

This represents a minuscule fraction of the total contracted volume of mCDR credits. As of October 2025, offtake agreements for marine CDR projects totaled 578,000 tonnes of CO2 removals, with only 0.3% of these credits having been formally issued. This stark contrast underscores the binary risk for project developers and investors: despite securing buyers, the revenue from credit sales is far from guaranteed.

The marine CDR sector is in a validation-led growth phase, not a full commercial scale-up. Verified delivery, methodology approval, and credible Monitoring, Reporting, and Verification (MRV) are the primary hurdles for the sector in the coming years.

### Typical Time from Deployment to Issuance: A Long and Uncertain Road

The timeline from project deployment to credit issuance in the marine CDR sector is lengthy and highly uncertain, with limited data available due to the novelty of the field. For other complex carbon removal projects, this process can take anywhere from 6 to 36 months. The process generally involves:

*   **Project Design and Development**: This initial phase includes planning, assessing potential impacts, and developing the necessary technology and methodologies.
*   **Validation**: An independent third-party auditor (Validation/Verification Body or VVB) reviews the project design to ensure it meets the standards of a given registry. This can take 3-6 months or longer.
*   **Registration**: Once validated, the project is formally listed on a registry.
*   **Monitoring**: The project's performance is continuously monitored according to the validated plan. For marine CDR, this is a particularly complex and ongoing process.
*   **Verification and Issuance**: After a monitoring period (often a year), a VVB audits the collected data to verify the actual carbon removal. If successful, the registry issues the credits. At the Verra registry, for example, the review process for an issuance request can take several rounds, with each round potentially lasting 20 business days or more.

For Planetary's OAE project, their two-year trial commenced in September 2023, with the first credits issued in June 2025, indicating a period of over a year and a half from the start of that specific trial phase to issuance. However, this does not account for the preceding years of research and development. The entire lifecycle from inception to the first credit issuance for a novel project can easily span three to five years.

### Why Marine CDR Projects Fail to Get Credits Issued: A Triad of Challenges

The primary reasons for the high issuance risk in marine CDR can be categorized into three interconnected challenges: the immense difficulty of Monitoring, Reporting, and Verification (MRV) in a dynamic ocean environment; proving additionality and permanence; and the nascent state of regulatory frameworks and methodologies.

#### 1. Unverifiable Far-Field Uptake and Model Dependence

A core challenge for most mCDR pathways is quantifying the net carbon removal in a vast, turbulent, and constantly changing open ocean.

*   **Attribution and Baselines**: It is incredibly difficult to distinguish the carbon removal signal from a project's intervention against the background noise of natural ocean variability. Establishing a credible baseline of what would have happened without the project is a fundamental, and often insurmountable, hurdle.
*   **Model Dependency**: Due to the challenges of direct measurement over large areas and long timescales, projects must rely heavily on numerical models to quantify carbon uptake. This reliance on models, which have their own uncertainties, is a significant point of scrutiny for verification bodies. For OAE, the added alkalinity can be diluted to undetectable levels relatively quickly, making direct observation of the full CO2 equilibration process impossible.
*   **High MRV Costs**: The complexity of monitoring in the ocean makes MRV exceptionally expensive, potentially exceeding 50% of the total project costs for pathways like OAE.

#### 2. Additionality and Permanence Risks

*   **Additionality**: A project must prove that the carbon removal would not have happened otherwise. For biological approaches like macroalgae cultivation, there is a risk of "nutrient robbing," where enhancing growth in one area leads to decreased productivity elsewhere, thus negating the net carbon benefit. For blue carbon projects, proving that the restoration efforts are additional to what might have occurred naturally is a persistent challenge.
*   **Permanence (Durability)**: Ensuring that the removed carbon stays sequestered for a climate-relevant timescale (typically hundreds to thousands of years) is another major hurdle. For macroalgae projects that involve sinking biomass, the deep-ocean decomposition rates and the potential for outgassing are still areas of active research. The durability of carbon stored in biological material can be much shorter than geological storage and is susceptible to ecosystem disturbances.

#### 3. Nascent Methodologies and Regulatory Uncertainty

*   **Lack of Approved Methodologies**: As of early 2026, very few mCDR methodologies have been fully developed and approved by major carbon registries like Verra or Gold Standard. While Isometric has an approved OAE protocol, and Puro.earth has approved methodologies for Microalgae Carbon Fixation and Sinking (MCFS) and Direct Air Capture and Ocean Storage (DACOS), many other pathways lack a clear route to credit issuance. Verra has several mCDR-related methodologies on hold. Without a finalized and approved methodology, projects cannot proceed to verification and issuance.
*   **Regulatory Gaps**: The governance for mCDR is fragmented and lags behind terrestrial CDR. Navigating international laws like the London Protocol and securing permits for deployment is a significant barrier for many projects.

### Plausible Issuance-Probability Range by Pathway

Given the current landscape, the binary probability of a marine CDR project successfully having credits issued in the near term (2025-2026) is very low across all pathways. The following ranges are estimates based on the available evidence, reflecting the nascent stage of the industry.

**Ocean Alkalinity Enhancement (OAE)**

*   **Issuance Probability: Low (5-15%)**
*   **Evidence**: This pathway has seen the *only* successful credit issuance to date from Planetary Technologies via Isometric's protocol. This demonstrates a potential, albeit challenging, path to issuance. However, there are 56 active mCDR developers, with OAE being a significant focus, yet only one has issued credits. The heavy reliance on modeling for far-field uptake and the high costs of MRV remain substantial risks for other projects.

**Direct Ocean Capture (DOC)**

*   **Issuance Probability: Very Low (1-5%)**
*   **Evidence**: While several companies like Captura and Equatic have pilot projects and offtake agreements, none have had credits issued as of early 2026. Isometric has published a registry protocol for DOCS, creating a potential pathway. However, the technology is generally at an earlier stage of commercial deployment than OAE. The high energy requirements and complexities of the technology present significant operational and financial risks that precede verification challenges.

**Macroalgae Cultivation (Seaweed)**

*   **Issuance Probability: Very Low (<1%)**
*   **Evidence**: There are currently no established and widely accepted MRV protocols for macroalgae-based carbon sequestration. Key challenges include accurately measuring the net carbon uptake, proving the permanence of sunk biomass, and addressing the risk of nutrient robbing. While Puro.earth has approved a methodology for Microalgae Carbon Fixation and Sinking, large-scale macroalgae projects for CDR face significant scientific and methodological hurdles before credits can be issued. The development of a rigorous methodology has proven to be a significant challenge, with some efforts being halted due to the complexities involved.

**Blue Carbon (Mangrove, Seagrass, Salt Marsh Restoration)**

*   **Issuance Probability: Low to Medium (10-30%)**
*   **Evidence**: Blue carbon projects, while marine-based, often fall under more established methodologies for afforestation, reforestation, and revegetation (ARR) and ecosystem restoration. Registries like Verra have certified numerous blue carbon projects, though these are often for avoided emissions or have faced scrutiny over additionality and baseline calculations. The issuance probability is higher than for novel mCDR pathways due to the longer history and more developed methodologies, but these projects still face significant challenges in accurately quantifying net carbon removal and ensuring permanence.

**Conclusion: A High-Risk, High-Reward Frontier**

The marine CDR carbon credit market is in its infancy, characterized by immense potential but fraught with substantial verification and issuance risks. For investors and project developers, the probability of achieving revenue through credit issuance in the near term is low. The binary nature of this risk—where projects either succeed in the complex verification process or receive no revenue from credit sales—necessitates a cautious approach. The development of robust, scientifically sound, and cost-effective MRV methodologies is the critical enabler that will determine the future viability and scalability of this crucial climate solution. Until then, investments in marine CDR are largely bets on future technological and methodological breakthroughs.


## credit_market
## Marine Carbon Removal: Navigating the Nascent Market for Durable CDR Credits

**The emerging market for durable marine carbon dioxide removal (mCDR) is characterized by high-cost, high-potential credits, with current prices in 2025-2026 ranging from approximately $270 to over $800 per tonne.** Offtake structures are dominated by advance market commitments and forward purchases from a handful of large corporate buyers, creating significant counterparty risk. For these technologies to become broadly bankable, a significant price reduction, coupled with robust and standardized measurement, reporting, and verification (MRV), is essential.

### Current Pricing by Pathway (2025-2026)

The price of durable marine CDR credits varies significantly by the specific technological pathway and the maturity of the project.

*   **Ocean Alkalinity Enhancement (OAE):** This is currently one of the most prominent mCDR pathways with several deals providing price transparency.
    *   A landmark deal in August 2025 saw the Frontier buyers club agree to purchase 115,211 credits from Planetary Technologies at a weighted average price of **roughly $271 per metric ton**. This deal, totaling $31.3 million, is for credits to be delivered between 2026 and 2030. The price is expected to decline over the delivery period.
    *   Other estimates for OAE place the cost between **$250 and $500 per tonne**. Some projections suggest that with economies of scale, the price for OAE could eventually fall to **$50-$160 per tonne**.
    *   Electrochemical OAE methods are currently more expensive, with companies like Equatic selling at around **$500 per tonne**.

*   **Direct Ocean Capture (DOC):** This pathway is generally considered to be in an earlier stage of commercialization.
    *   While specific 2025-2026 deal prices are not as readily available, one developer, Captura, projects that their technology could achieve levelized costs of **$100-$200 per ton of CO2 removed** in the future. The U.S. Department of Energy has a goal of achieving CDR at less than **$100 per ton** by 2032 through its Carbon Negative Shot Program, which includes DOC.

*   **Biomass Sinking:** Price points for this method are also less defined than for OAE.
    *   One 2024 estimate places the average price for woody biomass sinking at **$315 per tonne of CO2**.

It is important to note that the market is still in its infancy, and prices are influenced by factors such as the volume of purchase, the length of the contract, and the perceived quality and permanence of the carbon removal.

### Offtake Structures: Paving the Way for a Future Market

The dominant offtake structures in the marine CDR market are designed to provide early-stage companies with the revenue certainty they need to scale their operations.

*   **Advance Market Commitments (AMCs):** This is the primary model being used, most notably by **Frontier**, a public benefit company founded by Stripe, Alphabet, Shopify, Meta, and McKinsey. Frontier aggregates demand from its members to purchase large volumes of permanent carbon removal. By committing to buy future carbon credits, Frontier provides a crucial demand signal to developers and investors.

*   **Forward Purchase Agreements:** These are contracts for the future delivery of carbon credits. The aforementioned Planetary-Frontier deal is a prime example of a forward purchase agreement, with deliveries scheduled from 2026 to 2030. These agreements often include specific delivery windows and may have declining price curves as the technology matures and scales.

*   **Key Buyers (Frontier, Microsoft, Stripe):** A small number of large, well-capitalized buyers are driving the market.
    *   **Frontier** has committed over $1 billion to purchase permanent carbon removal and has been instrumental in funding OAE projects.
    *   **Microsoft** has been the single largest purchaser of durable carbon removal credits, accounting for a significant majority of total offtake. Their purchasing decisions have a profound impact on the market.
    *   **Stripe**, through its own climate program and as a co-founder of Frontier, has been a pioneering force in the carbon removal market, making early purchases to help kickstart the industry.

### Counterparty and Duration Risk: A Fragile Ecosystem

The heavy reliance on a small number of buyers creates significant **counterparty risk** for mCDR companies. Any change in the purchasing strategy of a major player like Microsoft could have ripple effects across the entire market. This was highlighted by a brief period of uncertainty in early 2026 when it was reported that Microsoft might slow down its CDR purchases.

**Duration risk** is also a key concern. The long-term nature of these agreements (often spanning 5-10 years) introduces uncertainty for both buyers and sellers. For sellers, there is the risk that the price they lock in today will be too low in the future. For buyers, there is the risk that the technology they bet on fails to deliver the promised quantity or quality of carbon removal. The durability of the carbon storage itself, often touted as 10,000 years or more for OAE, is a key selling point but also requires robust long-term monitoring and verification.

### The Path to Bankability: A High Bar to Clear

For marine CDR projects to be considered "bankable" in the traditional sense—meaning they can attract project finance and debt—they need to demonstrate a clear path to profitability and manage their risks effectively. The current market is far from this point; it is primarily funded by equity, grants, and the forward purchases of corporate buyers.

The price needed for broad bankability is not a single number but rather a function of several factors, including:

*   **Reduced Costs:** Prices need to come down significantly from their current levels. While a precise target is difficult to set, a price point consistently **below $100 per tonne** is often cited as a key threshold for scalability and wider adoption.
*   **Predictable Cash Flows:** Bankability requires predictable revenue streams. This can be achieved through long-term, legally binding offtake agreements with creditworthy counterparties.
*   **Standardized and Trusted MRV:** To attract traditional financing, the "product" being sold—a tonne of removed CO2—must be rigorously and independently verified. The development of standardized MRV protocols is a critical and ongoing challenge, with MRV costs sometimes exceeding 50% of total project costs for novel methods.
*   **Regulatory and Permitting Clarity:** A clear and efficient regulatory framework for permitting and overseeing mCDR projects is essential to reduce uncertainty and delays.
*   **Proven Technology and Operational Track Record:** Lenders will need to see that the underlying technology is reliable and that projects can be operated successfully at scale.

In conclusion, the marine CDR market is at a critical juncture. While there is significant momentum and investment from a dedicated group of buyers, the path to becoming a mature, bankable industry is still long and fraught with challenges. The price of carbon credits will need to fall, offtake agreements will need to become more standardized, and the risks associated with these novel technologies will need to be effectively managed.