[![semantically-enriched-link-prediction-datasets DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.15834518-blue?logo=doi)](https://doi.org/10.5281/zenodo.15834518)
[![semantically-enriched-link-prediction-datasets SWHID](https://archive.softwareheritage.org/badge/directory/a16d8bfc3387e575a20d238f2f3804f6b056293c/)](https://archive.softwareheritage.org/browse/origin/directory/?branch=refs/tags/1.0&origin_url=https://github.com/Wimmics/semantically-enriched-link-prediction-datasets)


# Introduction

This repository contains:

* The datasets DB100k+, Yago3-10+ and NELL-995+ which are the enrichments of the standard datasets DB100k, Yago3-10 and NELL-995 with entity types infered from class hierarchies and property domains and ranges
* The notebooks that generated these datasets
* A masking algorithm allowing to create variants of these datasets with target proportion of the predicates domain/range information
* An example of such dataset with a version of NELL-995 with 10% of triples with fully signed predicates (domain and range), 30% of triples with predicates with only the domain declared (no range), 10% of triples with predicates with only the range declared (no domain) and 50% of triples with unsigned predicates (no domain and no range).

This repository has been published under the [LGPL-2.1 license](./LICENSE) 

This repository is affiliated to the [WIMMICS research team](https://www.inria.fr/fr/wimmics), check the other [WIMMICS projects](https://www.inria.fr/fr/wimmics).

# How to use 

## Datasets

Each of the datasets [DB100k+](./DB100k+), [YAGO3-10+](./YAGO3-10+), [NELL-995+](./NELL-995+) and [NELL-995+_10_30_10](./NELL-995+_10_30_10) contain the following files:

* A notebook for the creation of the enriched dataset, using the URL of the original dataset for downloading it
* A notebook for dataset analysis that provides key information about the dataset
* The dataset files themselves
    * The dataset splits **train2id.txt**, **test2id.txt** and **valid2id.txt**
    * The dataset splits variants including the explicit modelling of inverse relations **train2id_inv.txt**, **test2id_inv.txt** and **valid2id_inv.txt**
    * A Sankey diagram that decomposes the dataset triples given their **semantic information**
    * a `pickle/` folder containing different __pickle__ dictionnaries
        * **ent2id** translating each entity to its related **id** (int)
        * **rel2id** translating each relation to its related **id** (int)
        * **class2id** translating each class to its related **id** (int)
        * **inst_type** linking ids of entities to their types (no inferred types included)
        * **inst_type_all** linking ids of entities to their types (including those that were got from subsumption axiom closure in any dataset, and domain/range in YAGO3-10+ and NELL-995+)
        * **classid2entid** linking ids of classes to the ids of their instances (including those that were infered from subsumption axiom closure in any dataset, and domain/range in YAGO3-10+ and NELL-995+)
        * **subclassof2id** linking ids of classes to their direct superclasses ids (set of ids)
        * **subclassof_all2id** linking ids of classes to their direct and indirect superclasses ids (set of ids)
        * **rid2domid** linking predicates ids to their related domain classes ids (set of ids)
        * **rid2rangeid** linking predicates ids to their related range classes ids (set of ids)
        * **observed_tails_original_kg** contains a head/relation/tail index of the dataset in the form of nested dictionaries using ids of entities and relations
        * **observed_heads_original_kg** contains a tail/relation/head index of the dataset in the form of nested dictionaries using ids of entities and relations
        * **observed_tails_inv** is an equivalent of **observed_tails_original_kg** that also contains explicit modelling of inverse relations
        * **observed_heads_inv** is an equivalent of **observed_heads_original_kg** that also contains explicit modelling of inverse relations
     
## Masking script

The script has the following usage:

```
python /path/to/dataset-mask.py /path/to/dataset-folder dataset_name full_signed_proportion domain_only_signed_proportion range_only_signed_proportion
```

where:

* `/path/to/dataset-folder` is the path to the folder containing the datasets. If the command is launched in the repository root it's simply `.`
* `dataset_name` is the name of the folder of the dataset to mask. In the example below, it is `NELL995+`
* `full_signed_proportion` is an int that is the desired percentage of triples with predicates having known domain and range (in train, test and valid splits)
* `domain_only_signed_proportion` is an int that is the desired percentage of triples with predicates having known domain but no range (in train, test and valid splits)
* `range_only_signed_proportion` is an int that is the desired percentage of triples with predicates having known range but no domain (in train, test and valid splits)

The resulting dataset is saved in the dataset folder, in a proper subfolder.

For example, launching the following command in the repository root:

```
python dataset-mask.py . NELL-995+ 10 30 10
```

generates the dataset that is in [folder NELL995+_10_30_10](./NELL995+_10_30_10)

# Key stats

### DB100k+

|Split|# Fully signed triples|# Domain-only triples|# Range-only triples|# Unsigned triples|Total|
|-----|----------------------|---------------------|--------------------|------------------|-----|
|Train|196,877|41,267|297,209|62,219|597,572|
|Test|16,517|3,527|24,827|5,129|50,000|
|Valid|16,437|3,426|24,909|5,228|50,000|
|**Total**|**229,831**|**48,220**|**346,945**|**72,576**|**697,572**|

### NELL-995+

|Split|# Fully signed triples|# Domain-only triples|# Range-only triples|# Unsigned triples|Total|
|-----|----------------------|---------------------|--------------------|------------------|-----|
|Train|103,255|6,545|25,779|14,099|149,678|
|Test|3,992|0|0|0|3,992|
|Valid|543|0|0|0|543|
|**Total**|**107,790**|**6,545**|**25,779**|**14,099**|**154,213**|

### YAGO3-10+

|Split|# Fully signed triples|# Domain-only triples|# Range-only triples|# Unsigned triples|Total|
|-----|----------------------|---------------------|--------------------|------------------|-----|
|Train|1,057,339|21,701|0|0|1,079,040|
|Test|4,886|114|0|0|5,000|
|Valid|4,912|88|0|0|5,000|
|**Total**|**1,067,137**|**21,903**|**0**|**0**|**1,089,040**|
