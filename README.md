# semantically-enriched-link-prediction-datasets

In this repository is available:

* The datasets DB100k+, Yago3-10+ and NELL-995+ which are the standard datasets DB100k, Yago3-10 and NELL-995 which are enriched with their related entity types and related predicates domains and range
* The notebooks that generated these datasets
* A masking algorithm allowing to create variants of these datasets with target proportion of the predicates domain/range information
* An example of such dataset with a version of NELL-995 with 10% of triples with predicates with dfines domain and range, 30% with only the domain known, 10% with nly the range known and 50% of unknown domain and range

This repository has been published under the [LGPL-2.1 license](./LICENSE) 

This repository is affiliated to the [WIMMICS research team](https://www.inria.fr/fr/wimmics), check the other [WIMMICS projects](https://www.inria.fr/fr/wimmics)

# How to use 

## Datasets

Each of the datasets [DB100k+](./DB100k+), [YAGO3-10+](./YAGO3-10+), [NELL995+](./NELL995+) and [NELL995+_10_30_10](./NELL995+_10_30_10) contain the following files:

* A notebook of creation of datasets, downloading the files from their related URIs and generates the datasets from scratch
* A notebook of dataset analysis that provides key information about the dataset
* The dataset files themselves
    * The datasets splits **train2id.txt**, **test2id.txt** and **valid2id.txt**
    * The datasets splits variants including the explicit modelling of iverse relations **train2id_inv.txt**, **test2id_inv.txt** and **valid2id_inv.txt**
    * A Sankey diagram that decomposes the dataset triples given their **semantic information**
    * a `pickle/` folder containing different __pickle__ dictionnaries
        * **ent2id** translating each entity to its related **id** (int)
        * **rel2id** translating each relation to its related **id** (int)
        * **class2id** translating each class to its related **id** (int)
        * **instype_all** linking ids of entities to its types (including those that were got from subsomption axiom closure in any dataset, and domain/range in YAGO3-10+ and NELL-995+)
        * **class2id2ent2id** linking ids of class to their related ids of instances (including those that were got from subsomption axiom closure in any dataset, and domain/range in YAGO3-10+ and NELL-995+)
        * **r2id2dom2id** linking predicates ids to their related domain class id
        * **r2id2range2id** linking predicates ids to their related range class id
        * **observed_tails_original_kg** contains a head/relation/tail index of the dataset in the form of nested dictionaries using ids of entities and relations
        * **observed_heads_original_kg** contains a tail/relation/head index of the dataset in the form of nested dictionaries using ids of entities and relations
        * **observed_tails_inv** is an equivalent of **observed_tails_original_kg** that also contains explicit modelling of inverse relations
        * **observed_heads_inv** is an equivalent of **observed_heads_original_kg** that also contains explicit modelling of inverse relations
     
## Masking script

The script has the following usage:

```
python /path/to/dataset-mask.py /path/to/dataset-folder dataset_name full_signed_proportion domain_only_signed_proportion range_only_signed_proportion
```

Given:

* `/path/to/dataset-folder` is the path to the folder containing the datasets. If the command is launched in the repository root it's simply `.`
* `dataset_name` is the name of the folder of the dataset to mask. For example `NELL995+` for the example provided for the example dataset
* `full_signed_proportion` is an int that is the desired percentage of triples with predicates having known domain and range (in train, test and valid splits)
* `domain_only_signed_proportion` is an int that is the desired percentage of triples with predicates having known domain but no range (in train, test and valid splits)
* `range_only_signed_proportion` is an int that is the desired percentage of triples with predicates having known range but no domain (in train, test and valid splits)

The resulting dataset will be saved in the dataset folder, in a proper subsfolder;

For example, launching the following command in the repository root:

```
python dataset-mask.py dataset_folder dataset_target signed_rate domained_rate ranged_rate
```

Generates the dataset that is in [folder NELL995+_10_30_10](./NELL995+_10_30_10)

# Key stats

### DB100k+

|Split|# Fully signed triples|# Domain-only triples|# Range-only triples|# Unsigned triples|Total|
|-----|----------------------|---------------------|--------------------|------------------|-----|
|Train|196,877|41,267|297,209|62,219|149678|
|Test|16,437|3,426|24,909|5,228|50,000|
|Valid|16,517|3,527|24,827|5,129|50,000|
|**Total**|**229,831**|**48,220**|**346,945**|**72,576**|**697,572**|

### NELL-995+

|Split|# Fully signed triples|# Domain-only triples|# Range-only triples|# Unsigned triples|Total|
|-----|----------------------|---------------------|--------------------|------------------|-----|
|Train|109,800|0|0|39,878|149,678|
|Test|3,992|0|0|0|3,992|
|Valid|543|0|0|0|543|
|**Total**|**114,335**|**0**|**0**|**39,878**|**154,213**|

### YAGO3-10+

|Split|# Fully signed triples|# Domain-only triples|# Range-only triples|# Unsigned triples|Total|
|-----|----------------------|---------------------|--------------------|------------------|-----|
|Train|1,057,339|21,701|0|0|1,079,040|
|Test|4,886|114|0|0|5,000|
|Valid|4,912|88|0|0|5,000|
|**Total**|**1,067,137**|**21,903**|**0**|**0**|**1,089,040**|
