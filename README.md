## Project members
- Stijn Lievaart 
- Michail Panagiotis Bofos
- Stavros Spyrou
- Dennis Mertens

## Problem description
Contextualized embeddings have enabled ambiguous words to carry their ambiguousness. This ambiguity is carried over into the embeddings because the context has an effect on the resulting embedding. As such, one expects ambiguous words to have specific (or well-defined) embeddings when paired with appropriate contexts.

We would like to look at the biases found within these embeddings and the effects of defined and ill-defined genders of occupations. Much like the previous paper (<a href="caliskan_et_al.pdf">Semantics derived automatically from language corpora contain human-like biases, Aylin Caliskan et al.</a>), but then applied to contextualized embeddings. 

The results will be of interest as these embeddings are used as the foundational meaning of words for LLMs such as ChatGPT, which will have an ever-increasing impact on society.

## A description of the dataset(s)
We would require a set of words that are expected to be similar regardless of gender - such as doctor, lawyer, cleaner, nurse, etc. 

We would require two sets of words for the attributes (he-she,man-woman,male-female), much like the words used in the works by Aylin Caliskan. 

The embeddings that we look into would be generated using the <a href="https://platform.openai.com/docs/guides/embeddings">openAI Embeddings API</a> and would be generated as such:

- female doctor/ she is a doctor/ the doctor is a woman -> embeddings of doctor[Female] 
- male doctor/ he is a doctor/ the doctor is a man -> embeddings of doctor[Male] 
- doctor -> embedding of doctor[Ill-defined]

## A description of the experimental setup (incl. methods and evaluation)
We could then test if the following holds: 

```<embedding of male/ he> - <embedding of female/ she> = <embedding of a male doctor> - <embedding of a female doctor>```, 

much like the typical comparison as: `He is to she as “male doctor” is to “female doctor”`.

After establishing the female and male definitions of the doctor, it would then be interesting to see where the genderless definition lies (embedding of “doctor” or `“they is a doctor”`), which we would expect to lay somewhere between the two. The distances to both vectors would then also denote the bias of the ill-defined word towards one direction. Showing, f.e. that `<embedding of a ill-defined doctor>` is closer to `<embedding of a male doctor>` than `<embedding of a female doctor>`.  

As such we hypothesize that contextualized embeddings can solve biases within appropriate contexts, but remain to present problems when genders are ill-defined. 


## What is the biggest ‘risk’ of your plan? If that happens, what will you do?
It could turn out that these contextualized embeddings would not work out as we expect them, in which the embeddings of female, male and genderless doctors are not at all similar. In this case we could project them onto one axis or look at the angles between them. This approach would be similar to the projections made in training an unbiased method as seen in (Mitigating Unwanted Biases with Adversarial Learning, Brian Hu Zhang et al.)


## Comments

- Overall interesting topic!
- Evaluation of bias in contextualized embeddings (specifically BERT embeddings) has been studied in various works. You propose to use Caliskan's et al. WEAT to measure bias in embeddings, however they have more recent study which modifies this for the contextualized embeddings: Contextualized Embedding Association Test (CEAT) (title: Detecting Emergent Intersectional Biases: Contextualized Word Embeddings Contain a Distribution of Human-like Biases). They also make the data and source-code available which is a great starting point. You can build upon this work by also using the measure for OpenAI embeddings.
- Generally, there’s quite some literature on measuring bias in contextual embeddings, this might also be a useful starting point: https://aclanthology.org/N19-1063.pdf
- Interesting to look at the OpenAI embeddings, since they have been investigated less in the literature. Be clear about which model you use in your report.
- If time allows, it could be interesting to compare fairness of downstream ML models (corefence resolution etc.) by using different embeddings and checking how intrinsic measures align with overall downstream model bias.
- “they is a doctor” --> “they are a doctor” (singular they)
