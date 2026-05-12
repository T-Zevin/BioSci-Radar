# Bio-Omics and AI Literature Recommendations

- Generated at: 2026-05-12T14:15:18
- Search window: last 7 days
- Paper count: 32
- Source stats: {'PubMed': 8, 'bioRxiv': 8, 'medRxiv': 8, 'arXiv': 8}

## Machine Learning / Deep Learning Methods

### 1. Systematic contextual biases in SegmentNT potentially relevant to other nucleotide transformer models

- **Type**: ML Algorithm
- **Score**: 0.46
- **Source**: bioRxiv
- **Authors**: Ebbert, M. T. W., Ho, A., Page, M. L., Dutch, B., Byer, B. K., Hankins, K. L., Sabra, H., Aguzzoli Heberle, B.
- **Topics**: Foundation Models for Biology
- **Omics**: None
- **ML areas**: Transformer
- **Why relevant**: matches Foundation Models for Biology; uses Transformer
- **URL**: https://doi.org/10.1101/2025.04.09.647946

**Abstract**

Recent advances in large language models (LLMs) have extended to genomic applications, yet model robustness relative to context is unclear. Here, we demonstrate two intrinsic biases (input sequence length and nucleotide position) affecting SegmentNT results, a model included with the Nucleotide Transformer that provides nucleotide-level predictions of biological features. We demonstrate that nucleotide position within the input sequence (beginning, middle, or end) alters the nature of SegmentNTs raw prediction probabilities, which can be standardized to improve prediction consistency. While longer input sequence length improves model performance, diminishing returns suggest a surprisingly small input length of [~]3,072 nucleotides might be sufficient for many applications. We further identify a 24-nucleotide periodic oscillation in SegmentNTs prediction probabilities, revealing an intrinsic bias potentially linked to the models training tokenization (6-mers) and architecture. We identify potential approaches to account for these biases and provide generalizable insights for utilizing nucleotide-resolution functional prediction models.

### 2. Histology-Derived Signatures Predict Recurrence Risk and Chemotherapy Benefit in Randomized Trials of Early Breast Cancer

- **Type**: ML Algorithm
- **Score**: 0.42
- **Source**: medRxiv
- **Authors**: Howard, F. M., Li, A., Kochanny, S., Sullivan, M., Flores, E. M., Dolezal, J., Khramtsova, G., Jain-Liu, S.
- **Topics**: Cancer Multi-omics, Survival and Clinical Prediction
- **Omics**: None
- **ML areas**: Survival
- **Why relevant**: matches Cancer Multi-omics, Survival and Clinical Prediction; uses Survival
- **URL**: https://doi.org/10.64898/2026.04.23.26351499

**Abstract**

PurposeTo test whether histology-derived gene-expression signatures from routine hematoxylin and eosin slides are prognostic for recurrence and predictive of chemotherapy benefit in early breast cancer. MethodsWe conducted a multi-cohort study including CALGB 9344 (anthracycline {+/-} paclitaxel), CALGB 9741 (standard vs dose-dense chemotherapy), a pooled Chicago real-world cohort, and the American Cancer Society (ACS) Cancer Prevention Studies-II and -3. Whole-slide images were processed with a previously described pipeline to generate 61 histology-derived signatures per patient. The primary endpoint was distant recurrence-free interval (DRFI), except in ACS, where breast cancer-specific survival was used. Secondary endpoints include distant recurrence-free survival (DRFS) and overall survival. The most prognostic signature in CALGB 9344, selected by Harrells C-index, was evaluated in additional cohorts. Signature-treatment interaction was assessed by likelihood-ratio tests. Multivariable Cox models incorporating age, tumor size, nodal status, estrogen/progesterone receptor status, and signature were fit in CALGB 9344 to improve risk stratification. ResultsA total of 7,170 patients were included across four cohorts. The top histology-derived signature in CALGB 9344 showed strong prognostic performance for 5-year DRFI (C-index 0.63) and performed well across validation cohorts (C-index 0.60, 0.70, and 0.62 in CALGB 9741, Chicago, and ACS, respectively). The strongest predictive signal for treatment benefit was observed for DRFS. High-risk cases identified by the signature demonstrated greater benefit from taxane in CALGB 9344 (adjusted hazard ratio [aHR] 0.76 for DRFS, 95% CI 0.66-0.88; interaction p=0.028), from dose-dense chemotherapy in CALGB 9741 (aHR 0.69, 95% CI 0.56-0.85; interaction p=0.039), and differential chemotherapy benefit in the Chicago cohort (aHR 0.84, 95% CI 0.59-1.21; interaction p=0.009). Combined clinical-histology models improved risk stratification and identified low-risk groups with a 2%-10% risk of distant recurrence or breast cancer death. ConclusionHistology-derived signatures from H&E images are broadly prognostic and, unlike clinical factors, may predict chemotherapy benefit. HighlightsO_LIHistology-derived H&E signatures consistently predicted recurrence risk across randomized trials and real-world cohorts. C_LIO_LIA single cutoff of a low-risk histology signature predicted taxane benefit and dose-dense chemotherapy benefit. C_LIO_LICombined clinical-histology models identified low-risk groups with 2%-10% risk of distant recurrence. C_LI

### 3. Patient2Sentence: Large Language Model-based Semantic Compression for Oncology Trial Eligibility Screening

- **Type**: ML Algorithm
- **Score**: 0.37
- **Source**: medRxiv
- **Authors**: Yoshinari, G. H., Goulart, W. C. S., Urbano, A. B. O., Rabello, M. M., Zorzetto, M. M., Macedo, S. O. d., Vitorino, L. M.
- **Topics**: Cancer Multi-omics
- **Omics**: None
- **ML areas**: Transformer
- **Why relevant**: matches Cancer Multi-omics; uses Transformer
- **URL**: https://doi.org/10.1101/2025.11.14.25340276

**Abstract**

Efficient clinical trial recruitment in oncology is constrained by the need to interpret long, heterogeneous electronic health records (EHRs) that remain largely unstructured and difficult to automate. We present Patient2Sentence (P2S), a large language model-based framework that performs semantic compression of full oncology EHRs into concise, standardized natural-language "patient sentences" while preserving eligibility-defining clinical logic. Using 75 fully synthetic EHRs modeled after the KATHERINE, MONARCH-E, and OLYMPIA breast cancer trials, we compared trial eligibility classifications derived from full clinical narratives with those obtained exclusively from compressed patient sentences. Eligibility decisions were evaluated against expert adjudication using agreement metrics and paired statistical testing. Sentence-based classifications achieved 94.7% concordance with expert judgments (Cohens {kappa} = 0.83), with no statistically significant difference in diagnostic accuracy compared to full-record assessments (McNemars p = 1.00), demonstrating non-inferiority of semantic compression for eligibility screening. Trial-specific agreement reached 100% for MONARCH-E, 96% for OLYMPIA, and 88% for KATHERINE, indicating robust performance across heterogeneous eligibility criteria. Semantic compression reduced token consumption by an average of 67.1%, corresponding to a threefold gain in computational efficiency without loss of reasoning fidelity. By reformulating complex oncologic records into human-interpretable, semantically dense sentences, P2S provides an explainable, scalable, and privacy-preserving approach to AI-assisted trial screening. This framework advances biomedical computing by enabling interoperable processing of unstructured clinical narratives and supports the integration of large language models into translational research workflows aimed at accelerating clinical trial recruitment.

### 4. Quantifying Concentration Phenomena of Mean-Field Transformers in the Low-Temperature Regime

- **Type**: ML Algorithm
- **Score**: 0.37
- **Source**: arXiv
- **Authors**: Albert Alcalde, Leon Bungert, Konstantin Riedl, Tim Roith
- **Topics**: None
- **Omics**: None
- **ML areas**: Transformer
- **Why relevant**: uses Transformer
- **URL**: https://arxiv.org/abs/2605.10931v1

**Abstract**

Transformers with self-attention modules as their core components have become an integral architecture in modern large language and foundation models. In this paper, we study the evolution of tokens in deep encoder-only transformers at inference time which is described in the large-token limit by a mean-field continuity equation. Leveraging ideas from the convergence analysis of interacting multi-particle systems, with particles corresponding to tokens, we prove that the token distribution rapidly concentrates onto the push-forward of the initial distribution under a projection map induced by the key, query, and value matrices, and remains metastable for moderate times. Specifically, we show that the Wasserstein distance of the two distributions scales like $\sqrt{{\log(β+1)}/β}\exp(Ct)+\exp(-ct)$ in terms of the temperature parameter $β^{-1}\to 0$ and inference time $t\geq 0$. For the proof, we establish Lyapunov-type estimates for the zero-temperature equation, identify its limit as $t\to\infty$, and employ a stability estimate in Wasserstein space together with a quantitative Laplace principle to couple the two equations. Our result implies that for time scales of order $\logβ$ the token distribution concentrates at the identified limiting distribution. Numerical experiments confirm this and, beyond that, complement our theory by showing that for finite $β$ and large $t$ the dynamics enter a different terminal phase, dominated by the spectrum of the value matrix.

## Bioinformatics Methods

### 1. MBD2 suppresses SFRP1 expression and promotes colorectal cancer development by blocking MED19 binding to its methylated promoter.

- **Type**: Bioinformatics Method
- **Score**: 0.25
- **Source**: PubMed
- **Authors**: Huang X, Luo T, Ke L, Guan S, Wu H, Li B, Liu Y, Qi J
- **Topics**: Cancer Multi-omics, Deep Learning for Omics
- **Omics**: bulk RNA-seq, epigenomics
- **ML areas**: None
- **Why relevant**: matches Cancer Multi-omics, Deep Learning for Omics; covers bulk RNA-seq, epigenomics
- **URL**: https://pubmed.ncbi.nlm.nih.gov/42084802/

**Abstract**

BACKGROUND: The Wnt signaling pathway antagonist SFRP1 is frequently silenced by promoter DNA hypermethylation in colorectal cancer (CRC). MBD2, a DNA methylation reader, is known to contribute to SFRP1 epigenetic silencing. Previous work showed that MBD2 critically suppresses SFRP1 expression without altering promoter methylation, though the underlying mechanism remained unclear. Elucidating how DNA methylation silences tumor suppressor genes, such as SFRP1 , could reveal novel therapeutic targets with significant clinical potential. METHODS: MBD2 was inhibited in CRC models using either siRNA or a small molecule inhibitor (KCC07). The effects on SFRP1 and β-catenin expression, Wnt pathway activity, cell proliferation, and apoptosis were assessed. Tumor growth was also evaluated in vivo. Mechanistic studies investigated the role of MBD2 in mediating MED19 binding to the SFRP1 promoter and its impact on RNA polymerase II CTD-S7 phosphorylation. RESULTS: The IC50 of KCC07 was 23.25 μM in SW480 cells, 26.83 μM in HCT116 cells, and 39.66 μM in NCM460 cells. Inhibition of MBD2, either genetically or pharmacologically with KCC07, upregulated SFRP1 expression, downregulated β-catenin, and suppressed the Wnt pathway. KCC07 treatment also inhibited CRC cell proliferation, promoted apoptosis, and suppressed tumor growth in vivo. Mechanistically, MBD2 was found to silence SFRP1 by blocking MED19 binding to its promoter, which subsequently reduced RNA polymerase II CTD-S7 phosphorylation and impaired transcription. CONCLUSIONS: This study reveals a novel mechanism whereby DNA methylation suppresses gene expression via MBD2, independent of changes in methylation status, by disrupting MED19 binding and subsequent transcription. Targeting MBD2 represents a promising therapeutic strategy for colorectal cancer.

### 2. Counterfactual Stress Testing for Image Classification Models

- **Type**: Bioinformatics Method
- **Score**: 0.17
- **Source**: arXiv
- **Authors**: Moritz Stammel, Fabio De Sousa Ribeiro, Raghav Mehta, Mélanie Roschewitz, Ben Glocker
- **Topics**: Deep Learning for Omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Deep Learning for Omics
- **URL**: https://arxiv.org/abs/2605.10894v1

**Abstract**

Deep learning models in medical imaging often fail when deployed in new clinical environments due to distribution shifts in demographics, scanner hardware, or acquisition protocols. A central challenge is underspecification, where models with similar validation performance exhibit divergent real-world failure modes. Although stress testing has emerged as a tool to assess this, current methods typically rely on simple, uninformed perturbations (e.g., brightness or contrast changes), which fail to capture clinically realistic variation and can overestimate robustness. In this work, we introduce a counterfactual stress testing framework based on causal generative models that create realistic "what if" images by intervening on attributes such as scanner type and patient sex while preserving anatomical identity, enabling controlled and semantically meaningful evaluation under targeted distribution shifts. Across two imaging modalities (chest X-ray and mammography), three model architectures, and multiple shift scenarios, we show that counterfactual stress tests provide a substantially more accurate proxy for real out-of-distribution performance than classical perturbations, capturing the direction and relative magnitude of performance changes as well as model ranking. These results suggest that causal generative models can serve as practical simulators for robustness assessment, offering a more reliable basis for evaluating medical AI systems prior to deployment.

### 3. Prevalence and Determinants of Musculoskeletal Symptoms Among Field Health Workers in Bin Qasim Town, Karachi

- **Type**: Bioinformatics Method
- **Score**: 0.12
- **Source**: medRxiv
- **Authors**: Mazhar, A., Rasheed, A., Khakwani, S., Hoodbhoy, Z.
- **Topics**: None
- **Omics**: None
- **ML areas**: None
- **Why relevant**: weak but potentially relevant keyword match
- **URL**: https://doi.org/10.64898/2026.05.03.26352346

**Abstract**

BackgroundWork-related musculoskeletal symptoms such as pain, stiffness, and swelling are a common occupational health issue that affect well-being and increase healthcare costs. Continuous physical effort, long hours of sitting, and poor awareness of proper ergonomics often lead to or worsen these conditions. ObjectiveThis study determined the frequency of musculoskeletal symptoms and the associated risk factors with musculoskeletal symptoms among field health workers in Bin Qasim Town, Karachi. Material & MethodsA cross-sectional study was employed and collected data from Karachi based pre-urban communities i.e.: Ibrahim Hydri, Rehri Goth and Bhains Colony. Study duration was 9 months. MSK symptoms were assessed using the standardized Nordic Musculoskeletal Questionnaire (NMQ). Prevalence of MSK symptoms was assessed over 12 months and 7 days. Participants with pain in [≥]2 regions of the upper or lower limbs were classified as having upper or lower limb symptoms, respectively. Multivariable logistic regression was used to identify associated factors for MSK symptoms in last 12 months. Results132 participants were recruited. Most frequently reported pain region in the last 12 months was lower back 111(84%) and shoulder 81(61%). Similarly, the most affected region in the last 7 days was also lower back 39(29%) followed by shoulder 33(25%). Upper limb MSK symptoms were significantly associated with bachelors or higher educated (OR=3.38; 95% CI: 0.67-7.42), sitting 3-4 h/day (OR=3.46; 95% CI: 1.11-10.75), and walking 3-4 h/day (OR=2.88; 95% CI: 1.05-7.85). In lower limb, married workers had 2 times higher odds of lower limb MSK symptoms (OR=2.36; 95% CI:1.04 - 5.35), while those who worked > 30 hours/week had 67% lower odds of having lower limb MSK symptoms (OR=0.33, 95% CI:0.15 - 0.72). ConclusionField health workers frequently reported MSK symptoms in both limbs. Preventive strategies such as ergonomic training, task rotation, and targeted support for married female workers are recommended to reduce the long-term impact.

### 4. SPISE index and ensemble machine learning refine cardiovascular risk stratification in stage 0-3 CKM syndrome.

- **Type**: Bioinformatics Method
- **Score**: 0.10
- **Source**: PubMed
- **Authors**: Wang L, Wang H, Liu T, Zhang N, Zhao L
- **Topics**: Survival and Clinical Prediction
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Survival and Clinical Prediction
- **URL**: https://pubmed.ncbi.nlm.nih.gov/42101474/

**Abstract**

BACKGROUND: While the single-point insulin sensitivity estimator (SPISE) shows promise as an insulin resistance biomarker, its association with cardiovascular disease (CVD) in early CKM stages (0-3) remains underexplored. METHODS: We analyzed 6480 participants with CKM stage 0-3 from the China Health and Retirement Longitudinal Study. CVD outcomes were assessed relative to SPISE index levels. An ensemble machine learning model was employed to predict CVD risk. RESULTS: 6480 subjects were enrolled, of whom 967 developed CVD. After stratifying participants into SPISE quartiles (Q1-Q4) and adjusting for covariates, higher quartiles were linked to a lower CVD risk. This study developed an LR+GMM (Logistic Regression + Gaussian Mixture Model) ensemble model to predict CVD risk using five strong predictors: SPISE, high-density lipoprotein cholesterol (HDL-c), diastolic blood pressure (DBP), body mass index (BMI), and glycated hemoglobin (HbA1c). The model performed well, achieving an accuracy (ACC) of 0.986 and an area under the receiver operating characteristic curve (AUC) of 0.932. CONCLUSIONS: The SPISE index is a significant inverse predictor of CVD risk in individuals with stage 0-3 CKM syndrome. The LR+GMM ensemble model, incorporating the SPISE index and four clinical metrics, demonstrated outstanding predictive performance.

## Biomedical / Multi-omics Studies

### 1. Altered crosstalk of bacterial lipopolysaccharide with immune cells in colorectal cancer compared to paired adjacent intestinal tissue.

- **Type**: Bio Study
- **Score**: 0.25
- **Source**: PubMed
- **Authors**: Walberg Å, Reuss AM, Ziadlou R, Mamie C, Gottier C, White A, Ameri M, Brüggen MC
- **Topics**: Bioinformatics Multi-omics, Single-cell and Spatial Omics, Cancer Multi-omics
- **Omics**: bulk RNA-seq, spatial
- **ML areas**: None
- **Why relevant**: matches Bioinformatics Multi-omics, Single-cell and Spatial Omics; covers bulk RNA-seq, spatial
- **URL**: https://pubmed.ncbi.nlm.nih.gov/42084500/

**Abstract**

Commensal bacteria play a crucial role in modulating human immune responses in the intestine. Under homeostatic conditions, the gut microbiota is tightly regulated by interactions with the mucosal immune system. However, colorectal cancer (CRC) is characterized by an imbalance in bacterial composition and bacterial translocation across the intestinal barrier. The spatial distribution of bacteria and their interactions with immune cells in CRC tumors are poorly understood. By applying 3D light-sheet imaging, spatial transcriptomics, and imaging mass cytometry to patient-derived CRC and adjacent intestinal tissue, bacterial lipopolysaccharide (LPS) can be visualized alongside immune cells and vessels. The results showed regional bacterial LPS accumulation and colocalization with distinct immune cell subsets. In CRC-adjacent tissue, bacterial LPS is mainly associated with CD11c + dendritic cells, CD15 + neutrophils, and CD163 + macrophages. In matched CRC tissue, the number and LPS colocalization of CD163 + macrophages and CD11c + dendritic cells decreased, while CD15 + neutrophils and their colocalization with LPS increased. Notably, immune cell composition and immune cell‒bacteria interactions differ between tumors and adjacent tissue, offering insights into host‒microbiota dynamics and mechanistic interactions.

### 2. Long-Read Haplotype Phasing Resolves Allelic Configuration as a Missing Layer of Precision Oncology

- **Type**: Bio Study
- **Score**: 0.21
- **Source**: medRxiv
- **Authors**: Vo, J. N., Wu, Y.-M., Wang, R., Pham, T., Cao, X., Yeung, S., Park, M., Kleyman-Smith, Y.
- **Topics**: Cancer Multi-omics
- **Omics**: epigenomics
- **ML areas**: None
- **Why relevant**: matches Cancer Multi-omics; covers epigenomics
- **URL**: https://doi.org/10.64898/2026.05.05.26351600

**Abstract**

Conventional short-read sequencing cannot determine whether co-occurring variants within a cancer gene reside on the same allele (cis) or on opposing alleles (trans), a distinction with direct biological and therapeutic consequences. Trans configurations confirm biallelic tumor suppressor inactivation and inform therapy selection, while cis configurations generate compound oncogenic alleles with enhanced activity. We analyzed 768 patients with prostate, breast, or ovarian cancers in the PROBLEM cohort, using mutational signatures to nominate cryptic genomic instability cases where the causative biallelic event was not apparent from short-read sequencing. Long-read nanopore sequencing resolved 32 of 46 cryptic cases (69.6%), leveraging its unique advantages in direct methylation detection, long insertion resolution, and complex structural variant characterization, confirming trans biallelic inactivation in all resolved tumor suppressor cases. Systematic analysis of 4,496 MiOncoSeq samples identified 17,519 multi-hit gene pairs, of which 78.7% exceeded the 500 bp short-read phasing limit. Long-read phasing further revealed recurrent compound cis oncogenic alleles in NOTCH1, PIK3CA, PDGFRB, and KIT with functionally synergistic activity. Haplotype phasing resolves a systematically overlooked gap in cancer variant interpretation and warrants broader integration into precision oncology workflows. Statement of SignificanceShort-read sequencing cannot resolve whether co-occurring variants within a cancer gene are cis or trans, a distinction critical for clinical interpretation. Long-read nanopore sequencing addresses this gap through direct haplotype phasing, methylation detection, and complex structural variant resolution, confirming biallelic tumor suppressor inactivation and revealing compound cis oncogenic alleles with enhanced activity.

### 3. Algae-specific Immune Modulation Influences Responses to Heat and Pathogen Challenge in a Symbiotic Coral

- **Type**: Bio Study
- **Score**: 0.18
- **Source**: bioRxiv
- **Authors**: Da-Anoy, J., Chen, M.-H., Bouchie, A., Dougherty, J., Lapadula, A., Skena, A., Wang, W., Abraham, T.
- **Topics**: Deep Learning for Omics
- **Omics**: bulk RNA-seq
- **ML areas**: None
- **Why relevant**: matches Deep Learning for Omics; covers bulk RNA-seq
- **URL**: https://doi.org/10.1101/2025.11.05.684850

**Abstract**

The role of symbiotic algae in coral life history and host health is well documented, but the immune and physiological trade-offs of hosting these symbionts remain less explored. While association with the algal symbionts of the genus Durusdinium is known to confer thermotolerance, it has also been linked to coral tissue loss under stress. We investigated whether algal type influences host immunity and stress responses in the tropical coral Pocillopora acuta. Durusdinium-hosting (D-hosting) P. acuta have distinct transcriptomic profiles, higher immune-related gene expression, and elevated baseline levels of immunity transcription factor NF-{kappa}B as compared to corals hosting Cladocopium (C-hosting). Under heat challenge, D-hosting P. acuta exhibited tissue loss, oxidative stress, immune and microbial dysregulation, whereas C-hosting P. acuta were more susceptible to bleaching, metabolic dysregulation, and decline in nitrogen-fixing and antioxidant-producing bacteria. Finally, infection with the the bacterium Vibrio coralliilyticus caused high tissue loss in D-hosting corals, but not in C-hosting corals. Our results suggest a mechanism for how Durusdinium association enhances thermotolerance yet predisposes corals to tissue damage under stress, suggesting immune trade-offs that can compromise host survival under multiple stressors.

### 4. Beyond malaria prevention: sulfadoxine-pyrimethamine treatment in pregnancy selectively remodels the maternal gut microbiome to increase gestational weight gain and improve birthweight

- **Type**: Bio Study
- **Score**: 0.17
- **Source**: medRxiv
- **Authors**: Waltmann, A., Puerto-Meredith, S. M., Chinkhumba, J., Mzembe, E., Kayange, M., Carroll, I., Roach, J., Mathanga, D. P.
- **Topics**: Bioinformatics Multi-omics
- **Omics**: microbiome
- **ML areas**: None
- **Why relevant**: matches Bioinformatics Multi-omics; covers microbiome
- **URL**: https://doi.org/10.64898/2026.05.03.26352319

**Abstract**

Intermittent preventive treatment in pregnancy (IPTp) with sulfadoxine-pyrimethamine (SP), an antifolate drug with antimalarial and antibiotic activity, reproducibly improves birthweight across sub-Saharan Africa and the Western Pacific. This clinical protection is independent of SPs original malaria indication: it is not diminished by widespread antimalarial resistance or reduced transmission, and SP outperforms more potent non-antibiotic antimalarials (e.g., dihydroartemisinin-piperaquine, DP) for fetal growth. The biological mechanism is unexplained. We previously showed that gestational weight gain (GWG) is a significant component of this mechanism and mediates two-thirds of SPs overall birthweight benefit (NCT03009526). In the first longitudinal characterization of antifolate antibiotic effects on the pregnant gut microbiome, we show that [~]45% of SPs GWG advantage over DP is explained by gut microbial changes consistent with its pharmacology. Microbiome-mediated GWG coincided with 126g higher birthweight in SP but not DP recipients (95%CI 22.6-229.3g; p=0.019). Relative to DP, SP suppressed gastrointestinal pathobionts and enriched anaerobic commensals with recognized roles in mucosal immunity and host metabolism, a microbiome-sparing pattern distinct from conventional antibiotic-associated dysbiosis.

### 5. Deep learning based on CD3 histological slides for prediction of colon cancer outcome: analysis of three international stage III colon cancer cohorts.

- **Type**: Bio Study
- **Score**: 0.16
- **Source**: PubMed
- **Authors**: Lécuelle J, Truntzer C, Basile D, Laghi L, Greco L, Ilie A, Rageot D, Huppé T
- **Topics**: Cancer Multi-omics, Deep Learning for Omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Cancer Multi-omics, Deep Learning for Omics
- **URL**: https://pubmed.ncbi.nlm.nih.gov/42100890/

**Abstract**

Prognostic stratification in stage III colon cancer remains poor, despite treatment advances. Tumor-infiltrating lymphocytes, particularly CD3+ T cells, are potential prognostic markers, but manual assessment is labor-intensive and not robust. This study aimed to develop a deep learning model for automated analysis of CD3-stained histological slides to improve prognostic prediction. A total of 1737 patients from three international cohorts (PETACC08, PRODIGE-13, and HARMONY) were analyzed. The deep learning model (VGG19) identified tumor core (TC) and invasive margin (IM) regions on CD3-stained slides. Features from VGG19 and UNI models were used to cluster patients using hierarchical classification. Prognostic performance was evaluated using disease-free survival (DFS) across training, internal validation, and external validation sets. Deep learning classifiers identified distinct patient clusters with significantly different DFS based on TC and IM. For both IM and TC analysis, patients in the favorable group had a better DFS in all sets (IM: p < 0.001, p = 0.04, p = 0.02; TC: p = 0.002, p = 0.01, p = 0.12, respectively). Combining classifiers enhanced prognostic accuracy in all sets ( p < 0.001, p = 0.01, p = 0.06, respectively). The model outperformed traditional clinical variables and CD3 enumeration, which demonstrated variability across cohorts. Automated deep learning analysis of CD3-stained slides enables robust and reproducible prognostic stratification in stage III colon cancer, independently of staining and scanning variations. This approach holds promise for guiding personalized treatment strategies. ClinicalTrials.gov Identifiers: NCT00265811, NCT00995202.

### 6. Metabolic Salvage and Acyl-chain Remodeling Support Glycosphingolipid Synthesis within the PDAC Tumor Microenvironment

- **Type**: Bio Study
- **Score**: 0.15
- **Source**: bioRxiv
- **Authors**: Trimble, A. S., Kubota, C. S., Zhao, E., Ruchhoeft, M. L., Weitz, J. R., Jung, W., Peck, K. L., Ogawa, S.
- **Topics**: Single-cell and Spatial Omics, Cancer Multi-omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Single-cell and Spatial Omics, Cancer Multi-omics
- **URL**: https://doi.org/10.64898/2026.04.14.718544

**Abstract**

Pancreatic ductal adenocarcinoma (PDAC) is a highly lethal malignancy where metabolic homeostasis is maintained by tumor and stromal cells within the tumor microenvironment (TME). To better assess pathways supporting macromolecule biosynthesis in PDAC tumors, we apply 13C metabolic flux analysis (MFA) to slice cultures of treatment-naive human tumors and mouse models that retain the native TME. Glycans, lipid headgroups, and very long-chain fatty acids are the most dynamic metabolic pools, while long chain fatty acids, purines, and pyrimidines are predominantly salvaged locally in situ. We use targeted pharmacological modulators to highlight the importance of recycling pathways and metabolic redundancies which mitigate changes in lipid abundances. Finally, we leverage targeted lipid fluxomics and the distinct ganglioside and globoside profiles of tumor and stromal cells, respectively, to demonstrate the role of the lipid kinase PIKfyve in supporting ganglioside homeostasis via sialic acid and ceramide salvage. These data establish application of MFA to slice cultures of PDAC tumors as an effective approach for assessing metabolic mechanisms and therapeutic responses within an intact TME.

### 7. Exploiting the dynamics of hyperthermia-enhanced delivery of thermosensitive liposomal doxorubicin to solid tumors.

- **Type**: Bio Study
- **Score**: 0.15
- **Source**: PubMed
- **Authors**: Namakshenas P, Crezee J, Kok HP
- **Topics**: Cancer Multi-omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Cancer Multi-omics
- **URL**: https://pubmed.ncbi.nlm.nih.gov/42108654/

**Abstract**

Thermosensitive liposomal (TSL) drug delivery with intravascular release under hyperthermia is a promising approach for chemotherapy of solid tumors, where the hyperthermia schedule strongly influences delivery efficacy. This study uses mathematical modeling to evaluate these effects. A compartmental modeling approach was used to simulate TSL-encapsulated doxorubicin (DOX) delivery. The model was calibrated and validated against published in vivo data from murine tumor models. Key variables included hyperthermia timing relative to TSL-DOX administration (0-60 min), duration (15-90 min), and heating pattern (continuous vs. fractional). Tumor cells exhibiting multidrug resistance (MDR), based on uptake characteristics of non-small cell lung cancer (NSCLC) and breast cancer cells, were modeled by varying cellular efflux rates. Initiating hyperthermia at peak plasma TSL levels increased the maximum intracellular DOX concentration by up to twofold compared with a 60-min delay. Tumor models characterized by NSCLC-like uptake were less responsive to prolonged hyperthermia than MCF-7 and MDA-468 breast cancer cells, showing minimal additional intracellular accumulation beyond 60 min. Low-MDR tumor models exhibited greater hyperthermia-enhanced uptake than high-MDR models. Prolonged hyperthermia increased systemic exposure to free DOX; however, the relative enhancement in tumor exposure exceeded that in systemic plasma. Continuous hyperthermia yielded a 20% higher intracellular DOX concentration after 60 min compared with a fractional schedule (4 × 15 min with 15-min cool-down intervals). For optimal delivery, hyperthermia in the stationary phase is most effective when synchronized with peak plasma TSL-DOX levels. Hyperthermia duration may require cancer-type-specific adjustment. These findings provide a mechanistic basis to inform hyperthermia protocol design.

### 8. Lamins and lineage-relevant transcription factors coordinate gene expression in lineage development

- **Type**: Bio Study
- **Score**: 0.15
- **Source**: bioRxiv
- **Authors**: Debic, S., Zheng, X., Hu, J., Kristiani, L., Marsela, R., Kim, Y., Zheng, Y.
- **Topics**: Deep Learning for Omics
- **Omics**: bulk RNA-seq
- **ML areas**: None
- **Why relevant**: matches Deep Learning for Omics; covers bulk RNA-seq
- **URL**: https://doi.org/10.64898/2026.04.30.722071

**Abstract**

HighlightsO_LILamin-A and lamin-B1 are essential for midgestational embryogenesis. C_LIO_LILamin-A/B1 are required for proper yolk sac endoderm (YSE) gene regulation. C_LIO_LILamin-A/B1 maintain LADs organization and chromatin interactions in YSE. C_LIO_LILamin-A/B1 and YSE transcription factors support proper YSE gene expression. C_LI Lamins are intermediate filament proteins functioning as ubiquitous structural components of the nuclear lamina that interact with and organize the Lamina-Associated chromatin Domains (LADs). LADs remodel during development and lamins maintain LADs and gene expression profile specific to a given cell type. How ubiquitous lamins achieve cell-type-specific functions during development remains unknown. We show lamin-A and -B1 are required for mouse midgestational embryogenesis and maintain LADs, 3D chromatin interactions, and gene expression in the yolk sac endoderm (YSE). Both lamin-regulated genes and remodeled LADs in YSE cells contain binding motifs of YSE-relevant transcription factors. By analyzing changes in chromatin interactions upon lamin-A and -B1 knockout, we reveal that chromatin neighborhoods maintained by these lamins can influence gene expression orchestrated by YSE-relevant transcription factors. Our findings explain how the ubiquitously expressed lamins can collaborate with lineage-relevant transcription factors to maintain LADs and gene expression programs in specific cell types.

### 9. Localized Gastrointestinal Light Chain (AL) Amyloidosis Under Surveillance for Five Years: A Case Report.

- **Type**: Bio Study
- **Score**: 0.14
- **Source**: PubMed
- **Authors**: Kojimahara S, Tominaga K, Yamamiya A, Kanazawa M, Tanaka T, Sugaya T, Katoh N, Irisawa A
- **Topics**: Cancer Multi-omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Cancer Multi-omics
- **URL**: https://pubmed.ncbi.nlm.nih.gov/42111927/

**Abstract**

Amyloidosis, characterized by the deposition of abnormal protein fibrils in organs, is classified as systemic or localized. Amyloid light chain (AL)-type localized amyloidosis is uncommon, particularly when confined to the gastrointestinal tract. Herein, we report a case of localized gastrointestinal AL-type amyloidosis that was incidentally detected and remained endoscopically and clinically stable over a 5-year follow-up period. The patient, a man in his 40s, had undergone a colonoscopy for colorectal cancer screening, during which scattered erosions were detected in the colon. Amyloid deposits were identified on biopsy. No cardiac or renal involvement, or evidence of multiple myeloma, was found. He was ultimately diagnosed with localized AL-type gastrointestinal amyloidosis. Following diagnosis, the patient underwent regular surveillance with transoral and transanal small-bowel endoscopy. No endoscopic progression or gastrointestinal symptoms were observed during the follow-up period, and the patient remained asymptomatic. This case suggests that conservative observation may be reasonable in carefully selected patients after exclusion of systemic involvement.

### 10. Anatomical dynamics define cancer cachexia subtypes and identify systemic inflammation as a marker of lethal wasting

- **Type**: Bio Study
- **Score**: 0.14
- **Source**: medRxiv
- **Authors**: Boscenco, S., Castillon, V. J., Wang, J., Tse, E., Freeman, S. S., Bakouny, Z., Mohan, S., Guo, X. A.
- **Topics**: None
- **Omics**: None
- **ML areas**: None
- **Why relevant**: weak but potentially relevant keyword match
- **URL**: https://doi.org/10.64898/2026.05.04.26352250

**Abstract**

Cancer cachexia is a wasting syndrome that remodels the anatomy of the patient. How this remodeling unfolds across tissues, whether it defines distinct disease states, and how these states relate to underlying biology remain unknown. We used longitudinal computed tomography imaging from 4,516 patients to quantify evolution of muscle, adipose, and organs during cachexia. Across two independent institutional cohorts, unsupervised analysis identified three reproducible anatomical subtypes of cachexia, including an inflammatory Type A marked by progressive hepatosplenic enlargement and inferior survival, a Type B dominated by visceral organ atrophy, and a mild Type C. These anatomical subtypes were associated with distinct serological signatures and reflected in molecular phenotypes in tumors and non-cancerous liver tissue, establishing cachexia as discrete anatomical disease states that link whole-body remodeling to systemic and tissue-level biology. This anatomy-first framework for cachexia classification provides a foundation for future patient stratification and development of subtype-specific anti-cachexia therapies.

### 11. Multi-omics profiling reveals MAGEL2-driven defects in human corticogenesis shared across Prader-Willi and Schaaf-Yang syndromes.

- **Type**: Bio Study
- **Score**: 0.13
- **Source**: bioRxiv
- **Authors**: Buecking, J., Güler, B. E., Eibl, M., Ali, A. S., Walczuch, T., Beschauner, T., Theiss, S., Spanjaard, M.
- **Topics**: Bioinformatics Multi-omics, Deep Learning for Omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Bioinformatics Multi-omics, Deep Learning for Omics
- **URL**: https://doi.org/10.64898/2026.05.01.722223

**Abstract**

The human cortex acquires its advanced cognitive capacity through tightly regulated developmental programs, disruption of which underlies neurodevelopmental disorders such as Schaaf-Yang syndrome (SYS) and Prader-Willi syndrome (PWS). While SYS results from pathogenic variants in the imprinted gene MAGEL2, PWS arises from chromosomal deletions, imprinting defects or uniparental disomy encompassing the MAGEL2 locus. However, the contribution of MAGEL2 to disease pathogenesis and human corticogenesis is not fully understood. Here, we performed integrated transcriptomic, proteomic, and ubiquitinomic profiling of cortical neurons derived from CRISPR/Cas9-engineered isogenic human pluripotent stem cells (hiPSC) modeling SYS and PWS. Beyond PWS-specific signatures including dysregulated ribosomal processes, we identified MAGEL2-dependent defects shared across both disorders. These include reduced progenitor proliferation, accelerated neuronal maturation, impaired migration and adhesion, as well as abnormal synaptic development, collectively linking PWS and SYS at the level of cortical development. Notably, these phenotypes partially overlap with those observed in other neurodevelopmental disorders, suggesting that MAGEL2 governs core pathways broadly vulnerable in disease. Together, our findings establish MAGEL2 as a key regulator of human cortical development, provide a unifying mechanistic framework for SYS and PWS, accessible via a web-based platform.

### 12. Sex-based considerations in the choice for a TLR9 or TLR7/8 agonist to arm the sentinel lymph node in early-stage melanoma.

- **Type**: Bio Study
- **Score**: 0.13
- **Source**: PubMed
- **Authors**: Notohardjo JCL, Toffoli EC, Muijlwijk T, van den Hout MFCM, Kandiah V, Labots M, van de Ven R, van den Eertwegh AJM
- **Topics**: Cancer Multi-omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Cancer Multi-omics
- **URL**: https://pubmed.ncbi.nlm.nih.gov/42093471/

**Abstract**

Intradermal delivery of the Toll-like receptor (TLR)-9 agonist agatolimod/CPG7909, prior to sentinel lymph node (SLN) biopsy was previously shown to induce locoregional and systemic immunity, reduce tumor-involved SLN rates, and improve recurrence-free survival in patients with early-stage melanoma. Remarkably, men exhibited superior dendritic cell (DC) maturation. Here, we report on further sex-based differences in the immune response after intradermal administration of CPG7909, which included higher CD80/CD83 expression levels in conventional (c) DC subsets in men's as compared to women's SLN, as well as higher ex-vivo release levels of IL-1β, TNF, and IL-6 (all contributors to cDC activation) and Th1/Th2 cytokines. In an effort to identify a more effective DC-activating therapy for women, we compared the in-vitro effects of CPG7909 with those of the TLR7/8 agonist resiquimod/R848 on SLN single cells from female patients. R848 induced superior cDC subset activation and TNF, IL-6, IL-10, IL-12, IFNγ, and CXCL10 release. Correlation analyses suggested that IFNα, TNF, and IL-6 were key for CPG7909-induced LNR-cDC activation, whereas R848's effect appeared more cytokine-independent. We conclude that combining locally delivered CPG7909 and R848 in early-stage melanoma will ensure full-range DC subset activation and robust pro-inflammatory T-cell responses in melanoma SLN, independent of sex.

### 13. Cell-type-resolved genetic regulatory variation shapes inflammatory bowel disease risk

- **Type**: Bio Study
- **Score**: 0.12
- **Source**: medRxiv
- **Authors**: Alegbe, T., Harris, B. T., Fachal, L., Ramirez Navarro, L., Tutert, M., Krzak, M., Ghouraba, M., Strickland, M.
- **Topics**: None
- **Omics**: None
- **ML areas**: None
- **Why relevant**: weak but potentially relevant keyword match
- **URL**: https://doi.org/10.1101/2025.06.24.25330216

**Abstract**

Most genetic variants associated with complex diseases lie in non-coding regions, complicating efforts to identify effector genes and relevant cell types. Here, we map cis-eQTLs across 2.2 million single cells from blood and intestinal biopsies of 421 individuals, including 125 with inflammatory bowel disease (IBD). Cell-type-level eQTLs were more distal to transcription start sites, enriched in enhancers, less likely to regulate the nearest gene, and over two-fold more likely to colocalise with IBD GWAS loci than eQTLs detected at tissue-level resolution. We nominate effector genes at over half of known IBD loci, including MAML2, PSEN2, and ZMIZ1 in myeloid cells, implicating reduced Notch signalling in intestinal immune dysfunction. We also identify Wnt regulated genes, including MYC, in epithelial stem and progenitor cells, suggesting that impaired renewal contributes to barrier breakdown. Our results provide a mechanistic map linking genetic risk to specific genes and cell types in IBD, and a framework for effector gene discovery in complex disease.

### 14. Pten Orchestrates Neurogenic Radial Glia Lineage Progression and Tunes Neocortical Astrocyte Production

- **Type**: Bio Study
- **Score**: 0.12
- **Source**: bioRxiv
- **Authors**: Miranda, O. A., Contreras, X., Pauler, F. M., Davaatseren, A., Amberg, N., Streicher, C., Villalba, A., Heger, A.
- **Topics**: Single-cell and Spatial Omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Single-cell and Spatial Omics
- **URL**: https://doi.org/10.64898/2026.05.01.722191

**Abstract**

The cerebral cortex consists of immense numbers of neuronal and glial cell-types derived from radial glial progenitor (RGP) cells. How RGPs generate appropriate quantities of distinct cortical cell-types to safeguard a brain of correct size, is not well understood. However, genetic aberration in human, including mutations in PTEN, lead to cortical malformation such as macrocephaly, albeit with unknown etiology. Here we utilized Mosaic Analysis with Double Markers (MADM)-based clonal analysis and single cell phenotyping to decipher the role of Pten in neurogenic and gliogenic RGP lineage progression during cortical ontogeny. While neurogenic RGP lineage progression and projection neuron production was moderately altered in the absence of Pten, cortical astrocyte production was drastically increased. Through genetic epistasis experiments we show that the loss of Pten uncouples astrocyte generation from essential growth factor signaling hubs, funneling into MAPK. Collectively, our results suggest that Pten regulates RGP lineage progression with distinct sequential functions in cortical projection neurogenesis and astrocyte production to ensure the emergence of a correctly-sized cerebral cortex.

### 15. DECO: Sparse Mixture-of-Experts with Dense-Comparable Performance on End-Side Devices

- **Type**: Bio Study
- **Score**: 0.10
- **Source**: arXiv
- **Authors**: Chenyang Song, Weilin Zhao, Xu Han, Chaojun Xiao, Yingfa Chen, Zhiyuan Liu
- **Topics**: None
- **Omics**: None
- **ML areas**: None
- **Why relevant**: weak but potentially relevant keyword match
- **URL**: https://arxiv.org/abs/2605.10933v1

**Abstract**

While Mixture-of-Experts (MoE) scales model capacity without proportionally increasing computation, its massive total parameter footprint creates significant storage and memory-access bottlenecks, which hinder efficient end-side deployment that simultaneously requires high performance, low computational cost, and small storage overhead. To achieve these properties, we present DECO, a sparse MoE architecture designed to match the performance of dense Transformers under identical total parameter budgets and training tokens. DECO utilizes the differentiable and flexible ReLU-based routing enhanced by learnable expert-wise scaling, which adaptively balances the contributions of routed and shared experts. Furthermore, we introduce NormSiLU, an activation function that normalizes inputs prior to SiLU operators, producing a more stable trend of routed-expert activation ratio and a higher intrinsic sparsity level. We also identify an empirical advantage in using non-gated MLP experts with ReLU-based routing, indicating the possibility of MoE architecture simplification. Experiments demonstrate that DECO, activating only 20% of experts, matches dense performance and outperforms established MoE baselines. Our specialized acceleration kernel delivers a 3.00$\times$ speedup on real hardware compared with dense inference. Codes and checkpoints will be released.

### 16. Gut microbiota-regulated glutathione metabolic rhythms restore obesity-induced colonic inflammatory oscillations.

- **Type**: Bio Study
- **Score**: 0.08
- **Source**: PubMed
- **Authors**: Zhao Z, Shi R, Ye J, Wang D, Zhao B, Ren B, Wang L, Liu X
- **Topics**: Bioinformatics Multi-omics, Deep Learning for Omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Bioinformatics Multi-omics, Deep Learning for Omics
- **URL**: https://pubmed.ncbi.nlm.nih.gov/42105281/

**Abstract**

Obesity disrupts circadian inflammatory rhythms, a defining feature of metabolic syndrome. However, the mechanisms connecting microbial and host circadian communication remain unclear. By using the fermentable fiber fructo-oligosaccharide (FOS) to restore microbial rhythmicity, we found that a high-fat diet (HFD) disrupts microbiota-regulated oscillations in glutathione metabolism, thereby dampening colonic inflammatory rhythms independently of the core clock machinery. Fecal microbiota transplantation (FMT) further supported a causal role for rhythmic fecal microbial signals in restoring inflammatory oscillations. Integrated multi-omics analysis highlighted circadian glutathione metabolism as a prominent candidate pathway linking microbial rhythmicity to host inflammatory oscillations. Importantly, colon-specific knockdown of Gclc , the rate-limiting enzyme in glutathione synthesis, abolished the restorative effects of microbial rhythms, functionally positioning host glutathione metabolism as a critical downstream mediator. Collectively, our study supports the existence of a microbiota-glutathione axis that contributes to the regulation of colonic inflammatory rhythms, uncovering a new chronobiological layer of microbial control over host inflammation.

## Datasets and Resources

### 1. MolGene-E: Inverse Molecular Design to Modulate Single Cell Transcriptomics

- **Type**: Dataset
- **Score**: 0.28
- **Source**: bioRxiv
- **Authors**: Ohlan, R., Murugan, R., Xie, L., Nallabolu, V., Mottaqi, M., Zhang, S., Xie, L.
- **Topics**: Bioinformatics Multi-omics, Single-cell and Spatial Omics, Deep Learning for Omics
- **Omics**: bulk RNA-seq
- **ML areas**: Contrastive
- **Why relevant**: matches Bioinformatics Multi-omics, Single-cell and Spatial Omics; covers bulk RNA-seq; uses Contrastive
- **URL**: https://doi.org/10.1101/2025.02.19.638723

**Abstract**

Designing drugs that can restore a diseased cell to its healthy state is an emerging approach in systems pharmacology to address medical needs that conventional target-based drug discovery paradigms have failed to meet. Single-cell transcriptomics can comprehensively map the differences between diseased and healthy cellular states, making it a valuable technique for systems pharmacology. However, single-cell omics data is noisy, heterogeneous, scarce, and high-dimensional. As a result, no machine learning methods currently exist to use single-cell omics data to design new drug molecules. We have developed a new deep generative framework named MolGene-E to tackle this challenge. MolGene-E combines two novel models: 1) a cross-modal model that can harmonize and denoise chemical-perturbed bulk and single-cell transcriptomics data, and 2) a contrastive learning-based generative model that can generate new molecules based on the transcriptomics data. MolGene-E consistently outper-forms baseline methods in generating high-quality, hit-like molecules on gene expression profiles from two evaluation settings: CRISPR knock-out perturbation profiles from L1000toRNAseq dataset, and single-cell gene expression profiles from Sciplex-3 dataset, both in zero-shot molecule generation setting. This superior performance is demonstrated across diverse de novo molecule generation metrics. Extensive evaluations demonstrate that MolGene-E achieves state-of-the-art performance for zero-shot molecular generations. This makes MolGene-E a potentially powerful new tool for drug discovery.

### 2. Count Anything at Any Granularity

- **Type**: Dataset
- **Score**: 0.22
- **Source**: arXiv
- **Authors**: Chang Liu, Haoning Wu, Weidi Xie
- **Topics**: None
- **Omics**: None
- **ML areas**: Multimodal
- **Why relevant**: uses Multimodal; mentions code
- **URL**: https://arxiv.org/abs/2605.10887v1

**Abstract**

Open-world object counting remains brittle: despite rapid advances in vision-language models (VLMs), reliably counting the objects a user intends is far from solved. We argue that a central reason is that counting granularity is left implicit; users may refer to a specific identity, an attribute, an instance type, a category, or an abstract concept, yet most methods treat "what to count" as a single, category-level matching problem. In this work, we redefine open-world counting as multi-grained counting, where visual exemplars specify target appearance and fine-grained text, with optional negative prompts, specifies the intended semantic granularity across five explicit levels. Making granularity explicit, however, exposes a critical data bottleneck: existing counting datasets lack the multi-category scenes, controlled distractors, and instance-level annotations needed to verify fine-grained prompt semantics. To address this, we propose the first fully automatic data-scaling pipeline that integrates controllable 3D synthesis with consistent image editing and VLM-based filtering, and use it to construct KubriCount, the largest and most comprehensively annotated counting dataset to date, supporting both training and multi-grained evaluation. Systematic benchmarking reveals that both multimodal large language models and specialist counting models exhibit severe prompt-following failures under fine-grained distinctions. Motivated by these findings, we train HieraCount, a multi-grained counting model that jointly leverages text and visual exemplars as complementary target specifications. HieraCount substantially improves multi-grained counting accuracy and generalizes robustly to challenging real-world scenarios. The project page is available here: https://verg-avesta.github.io/KubriCount/.

### 3. BEACON: A Multimodal Dataset for Learning Behavioral Fingerprints from Gameplay Data

- **Type**: Dataset
- **Score**: 0.22
- **Source**: arXiv
- **Authors**: Ishpuneet Singh, Gursmeep Kaur, Uday Pratap Singh Atwal, Guramrit Singh, Gurjot Singh, Maninder Singh
- **Topics**: Deep Learning for Omics
- **Omics**: None
- **ML areas**: Multimodal
- **Why relevant**: matches Deep Learning for Omics; uses Multimodal; mentions code
- **URL**: https://arxiv.org/abs/2605.10867v1

**Abstract**

Continuous authentication in high-stakes digital environments requires datasets with fine-grained behavioral signals under realistic cognitive and motor demands. But current benchmarks are often limited by small scale, unimodal sensing or lack of synchronised environmental context. To address this gap, this paper introduces BEACON ( Behavioral Engine for Authentication \& Continuous Monitoring), a large-scale multimodal dataset that captures diverse skill tiers in competitive \textit{Valorant} gameplay. BEACON contains approximately 430 GB of synchronised modality data (461 GB total on-disk including auxiliary \textit{Valorant} configuration captures) from 79 sessions across 28 distinct players, estimated at 102.51 hours of active gameplay, including high-frequency mouse dynamics, keystroke events, network packet captures, screen recordings, hardware metadata, and in-game configuration context. BEACON leverages the high precision motor skills and high cognitive load that are inherent to tactical shooters, making it a rigorous stress test for the robustness of behavioral biometrics. The dataset allows for the study of continuous authentication, behavioral profiling, user drift and multimodal representation learning in a high-fidelity esports setting. The authors release the dataset and code on Hugging Face and GitHub to create a reproducible benchmark for evaluating next-generation behavioral fingerprinting and security models

### 4. A novel metric reveals previously unrecognized distortion in dimensionality reduction of scRNA-Seq data

- **Type**: Dataset
- **Score**: 0.20
- **Source**: bioRxiv
- **Authors**: Hamilton, T., Sparta, B., Cooley, S. M., Aragones, S. D., Ray, J. C. J., Deeds, E. J.
- **Topics**: Single-cell and Spatial Omics
- **Omics**: bulk RNA-seq, scRNA-seq
- **ML areas**: None
- **Why relevant**: matches Single-cell and Spatial Omics; covers bulk RNA-seq, scRNA-seq
- **URL**: https://doi.org/10.1101/689851

**Abstract**

High-dimensional data are becoming increasingly common in nearly all areas of science. Developing approaches to analyze these data and understand their meaning is a pressing issue. This is particularly true for single-cell RNA-seq (scRNA-seq), a technique that simultaneously measures the expression of tens of thousands of genes in thousands to millions of single cells. Popular analysis pipelines significantly reduce the dimensionality of the dataset before performing downstream analysis. One problem with this approach is that dimensionality reduction can introduce substantial distortion into the data, particularly by disrupting the local neighborhoods of certain points. Since many scRNA-seq analyses like cell type clustering or trajectory inference rely on these near-neighbor relationships, distortion in this aspect of the data could significantly influence the outcomes of these analyses. Here, we introduce a straightforward approach to quantifying this distortion by comparing the local neighborhoods of points before and after dimensionality reduction. We found that popular techniques like t-SNE and UMAP introduce substantial distortion even for simple simulated data sets. For scRNA-seq data, we found the distortion in local neighborhoods was often greater than 95%, and that there was no consistent set of neighborhoods across the various steps in the consensus scRNA-seq analysis pipeline. We also found that this distortion had profound impacts on the outcomes of cell type clustering and other downstream analyses. Our findings suggest that caution must be applied when interpreting results in terms of 2-D visualizations produced by tools like UMAP, and that there is a critical need for new dimensionality reduction tools that more effectively preserve the local topological structure of the data.

### 5. Confidence-Guided Diffusion Augmentation for Enhanced Bangla Compound Character Recognition

- **Type**: Dataset
- **Score**: 0.18
- **Source**: arXiv
- **Authors**: Md. Sultan Al Rayhan, Maheen Islam
- **Topics**: Foundation Models for Biology
- **Omics**: None
- **ML areas**: Transformer, Diffusion
- **Why relevant**: matches Foundation Models for Biology; uses Transformer, Diffusion
- **URL**: https://arxiv.org/abs/2605.10916v1

**Abstract**

Recognition of handwritten Bangla compound characters remains a challenging problem due to complex character structures, large intra-class variation, and limited availability of high-quality annotated data. Existing Bangla handwritten character recognition systems often struggle to generalize across diverse writing styles, particularly for compound characters containing intricate ligatures and diacritical variations. In this work, we propose a confidence-guided diffusion augmentation framework for low-resolution Bangla compound character recognition. Our framework combines class-conditional diffusion modeling with classifier guidance to synthesize high-quality handwritten compound character samples. To further improve generation quality, we introduce Squeeze-and-Excitation enhanced residual blocks within the diffusion model's U-Net backbone. We additionally propose a confidence-based filtering mechanism where pre-trained classifiers act as quality gates to retain only highly class-consistent synthetic samples. The filtered synthetic images are fused with the original training data and used to retrain multiple classification architectures. Experiments conducted on the AIBangla compound character dataset demonstrate consistent performance improvements across ResNet50, DenseNet121, VGG16, and Vision Transformer architectures. Our best-performing model achieves 89.2\% classification accuracy, surpassing the previously published AIBangla benchmark by a substantial margin. The results demonstrate that quality-aware diffusion augmentation can effectively enhance handwritten character recognition performance in low-resource script domains.

### 6. Masked Generative Transformer Is What You Need for Image Editing

- **Type**: Dataset
- **Score**: 0.15
- **Source**: arXiv
- **Authors**: Wei Chow, Linfeng Li, Xian Sun, Lingdong Kong, Zefeng Li, Qi Xu, Hang Song, Tian Ye
- **Topics**: Foundation Models for Biology
- **Omics**: None
- **ML areas**: Transformer
- **Why relevant**: matches Foundation Models for Biology; uses Transformer
- **URL**: https://arxiv.org/abs/2605.10859v1

**Abstract**

Diffusion models dominate image editing, yet their global denoising mechanism entangles edited regions with surrounding context, causing modifications to propagate into areas that should remain intact. We propose a fundamentally different approach by leveraging Masked Generative Transformers (MGTs), whose localized token-prediction paradigm naturally confines changes to intended regions. We present EditMGT, an MGT-based editing framework that is the first of its kind. Our approach employs multi-layer attention consolidation to aggregate cross-attention maps into precise edit localization signals, and region-hold sampling to explicitly prevent token flipping in non-target areas. To support training, we construct CrispEdit-2M, a 2M-sample high-resolution (>1024) editing dataset spanning seven categories. With only 960M parameters, EditMGT achieves state-of-the-art image similarity on multiple benchmarks while delivering 6x faster editing, demonstrating that MGTs offer a compelling alternative to diffusion-based editing.

### 7. V4FinBench: Benchmarking Tabular Foundation Models, LLMs, and Standard Methods on Corporate Bankruptcy Prediction

- **Type**: Dataset
- **Score**: 0.12
- **Source**: arXiv
- **Authors**: Marcin Kostrzewa, Sebastian Tomczak, Roman Furman, Anna Poberezhna, Michał Furgała, Oleksii Furman, Maciej Zięba
- **Topics**: None
- **Omics**: None
- **ML areas**: None
- **Why relevant**: weak but potentially relevant keyword match
- **URL**: https://arxiv.org/abs/2605.10896v1

**Abstract**

Corporate bankruptcy prediction is a high-stakes financial task characterized by severe class imbalance and multi-horizon forecasting demands. Public datasets supporting it remain scarce and small: widely used free benchmarks contain between 6,000 and 80,000 company-year observations, while larger resources are behind subscription paywalls. To address this gap, we introduce V4FinBench, a benchmark of over one million company-year records from the Visegràd Group (V4) economies (2006-2021), with 131 financial and non-financial features, six prediction horizons, and a composite distress criterion jointly capturing solvency, profitability, and liquidity deterioration. V4FinBench is designed to support the evaluation of tabular and foundation-model methods under realistic class imbalance, with positive rates between 0.19% and 0.36%. We provide reference evaluations of standard tabular baselines, finetuned TabPFN, and QLoRA-finetuned Llama-3-8B. With imbalance-aware finetuning, TabPFN matches or exceeds gradient boosting at longer time horizons on both $F_1$-score and ROC-AUC. In contrast, Llama-3-8B trails gradient boosting on ROC-AUC at every horizon and is generally weaker on $F_1$-score, with the gap widening sharply beyond the immediate horizon. In an external evaluation on the American Bankruptcy Dataset, the V4FinBench-finetuned TabPFN checkpoint improves over vanilla TabPFN, suggesting that adaptation captures transferable financial-distress structure rather than only V4-specific patterns. V4FinBench is publicly released to support further evaluation and development of prediction methods on realistic financial data.

## Reviews

### 1. Optimizing Screening for Intrauterine Fetal Growth Restriction in Low-Resource Settings Using 2D Ultrasound: A Deep Learning Approach

- **Type**: Review
- **Score**: 0.15
- **Source**: medRxiv
- **Authors**: Enywaku, A., Asiku, R. A.
- **Topics**: Deep Learning for Omics
- **Omics**: None
- **ML areas**: None
- **Why relevant**: matches Deep Learning for Omics
- **URL**: https://doi.org/10.64898/2026.05.04.26352354

**Abstract**

Severe fetal growth restriction (sFGR) affects 5 to 10% of pregnancies worldwide and is a major contributor to perinatal morbidity and mortality, particularly in low- and middle-income countries (LMICs). Traditional 2D ultrasound detection methods suffer from operator dependency, gestational age uncertainty, and limited access to Doppler in many low-resource facilities. This study presents a deep learning framework for sFGR screening and triage using 2D fetal abdominal ultrasound images designed to operate independently of precise gestational dating. Growth restriction severity labels were derived by mapping abdominal circumference measurements to INTERGROWTH-21st term percentiles as a gestational-age-normalized proxy for fetal size restriction when case-level gestational age or birth-weight data are unavailable. A systematic literature review of 37 studies revealed gaps in severity stratification and generalizability. We implemented a DenseNet-121-based model with abdominal circumference measurement for severity-aware classification using a retrospective single-center dataset of 1588 annotated fetal abdominal images from 169 term pregnancies. Patient-wise 3-fold cross-validation and ensemble testing yielded 93.7% accuracy, a weighted F1-score of 0.76, and ROC AUC [≥] 0.98 per class on heldout data. The approach outperforms previously reported single-center methods on this dataset while explicitly targeting LMIC-specific constraints. It demonstrates potential as a gestational-age-independent first-line triage layer for equitable prenatal screening, subject to prospective multi-site validation.
