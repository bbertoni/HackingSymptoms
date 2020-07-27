# Hacking Symptoms
Resources, docs and code repository for Hackathon 2020: Diagnosing rare diseases with AI - Hacking symptoms.

## Background information
Rare diseases are more common than what one could initially estimate. They are reported (sorry that I am no including references in this document) to affect ~6-8 % of the global population, although each one of them has a much smaller prevalence. Many patients take a very long time to be diagnosed, a time that can be greatly reduced by new technological developments on precision medicine. One technology that can greatly impact the diagnostic odyssey is the utilization of NLP to analyze patient medical records and identify the symptoms a patient presents. These symptoms can then be fed to a prediction algorithms of simply shown to a clinician for interpretation with or without genetic information.
 
Therefore, providing the patient symptoms stands as the entry point to leveraging the power of accurate disease clinical descriptions and, if available, the information contained in the patient genetic information. The symptoms are represented by Human Phenotype Ontology (HPO) terms, you have a short introduction at the HPO section.

## Objectives
The goal of this team is to:
1. Develop a framework (MVP-like) in which NLP algorithms capable of recognising medical concepts (HPO terms) can be compared.
2. Perform a comparison between such algorithms and establish a performance baseline.
3. If possible, further develop or improve the models.

## Algorithms to compare
We will focus the comparison on the following algorithms:
1. Neural Concept Recognizer (NCR).
2. Microsoft's Text Analytics.

However, if time permits, I'd like to include others:
1. Biolink NLP Annotator.
2. IHP
3. ClinPhen

### Neural Concept Recogniser (NCR)
This algorithm, by Arbabi et al [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6533869/], is deployed in Foundation 29's Azure subscription. An API will be provided. It was trained in the 228 pubmed abstracts here used, which implies that it's performance will be overestimated. Clearly suboptimal.
 
### Microsoft Text Analytics
You deployed this, so you are well aware about how to use it. I simply want to raise the case that probably it has already seen the data used in this project. I don't know how it was developed.

### Add-ons if you are interested and there is time:
1. Biolink NLP annotator: A rule-based annotation engine deployed at the biolink API (https://api.monarchinitiative.org/api/nlp/annotate).
2. IHP: Developed by Lobo et al (https://doi.org/10.1155/2017/8565739) and, again, trained on the GSC data. Downloadable from: https://github.com/lasigeBioTM/IHP.
3. ClinPhen: Developed by Deisseroth et al. (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6551315/), it can be obtained here: https://bitbucket.org/bejerano/clinphen/src/master/. Hopefully the PIP package is still valid. If not, give it a try to this one: https://github.com/kingmanzhang/clinphen.
4. Want a real challenge? It would be interesting to develop a matching strategy between HPO terms and the concepts trained on clinicalBERT (https://github.com/EmilyAlsentzer/clinicalBERT) so that they can be used directly for HPO term recognition.

## Data availability
Public data is very scarce in this context with limited available resources. The datasets required would be medical text labelled with HPO terms (see HPO section for details on what HPO is). In principle, there are two datasets that we could use: the Gold Standard Corpora and OMIM.
 
### Gold Standard Corpora
In order to test (or train) the algorithms we will use the dataset known as Gold Standard Corpora (GSC). The data consists of 228 annotated abstracts cited by OMIM (http://www.omim.org). The data can be found here: https://github.com/lasigeBioTM/IHP.
 
There is an improved version of the corpora fixing some issues as identified by Lobo et al. (https://doi.org/10.1155/2017/8565739).
 
We are requesting access to the OMIM API in order to be able to download clinical synopsis along with HPO annotations. This could bring the whole dataset to the order of 5000 annotated documents. But it is uncertain if they will be available for the Hackathon.
 
It is worth noting that the GSC is the same dataset that has been used by IHP and NCR for training, therefore there is a clear bias in the results that is difficult to solve. Ideas are welcomed.
 
### OMIM
OMIM has collected a large set of genetic diseases along with their phenotypic (symptom) description. They have an API available to which we have requested access and through which we can query the clinical synopsis of the disease and the disease symptoms. Then, we can compare what terms each algorithm extracts.
 
In the case access to OMIM's API is not granted in time, we could scrape the information from the website. In order to do so a list of OMIM identifiers would come in handy. This list can be accessed through the API Foundation29 has developed. This API is described in a dedicated section.



