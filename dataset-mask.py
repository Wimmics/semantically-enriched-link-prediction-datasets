from glob import glob
from sys import argv
from pickle import load, dump
from glob import glob
from tqdm import tqdm
from copy import deepcopy
from shutil import copy as copy_file
from os import makedirs
from os.path import exists, sep
import sys

printline=sys.stdout.write

#################
# Command check #
#################

if len(argv) != 6:
    print("""
Command line error, usage:

pyton dataset-mask.py dataset_folder dataset_target signed_rate domained_rate ranged_rate

    - dataset_folder: str, relative path to the folder containing the datasets
    - dataset_target: str, name of the folder containing the dataset to mask
    - signed_rate: int, target percentage of triples with known domain and range  
    - domained_rate: int, target percentage of triples with known domain but no range 
    - ranged_rate: int, target percentage of triples with known range but no domain 
    """)
    exit(0)

datasets_folder=argv[1]

if not exists(datasets_folder):
    print("""
Command line error: cannot find datasets folder
    """)
    exit(0)

datasets_folder=datasets_folder[:-1] if datasets_folder[-1] in ["\\", "/"] else datasets_folder

dataset_name=argv[2]
dataset_target=dataset_name[:-1] if dataset_name[-1] in ["\\", "/"] else dataset_name

dataset_target=f"{datasets_folder}{sep}{dataset_target}"

if not exists(dataset_target):
    print("""
Command line error: cannot find target dataset folder
    """)
    exit(0)

signed_rate=0
try:
    signed_rate=int(argv[3])
except:
    print("""
Command line error: signed_rate should be an integer
    """)
    exit(0)
    
domained_rate=0
try:
    domained_rate=int(argv[4])
except:
    print("""
Command line error: domained_rate should be an integer
    """)
    exit(0)

ranged_rate=0
try:
    ranged_rate=int(argv[5])
except:
    print("""
Command line error: ranged_rate should be an integer
    """)
    exit(0)

target_rates={
    split: {
        "signed": signed_rate/100,
        "domained_only": domained_rate/100,
        "ranged_only": ranged_rate/100,
        "unsigned": 1 - signed_rate/100 - domained_rate/100 - ranged_rate/100
    }
    for split in ["train", "test", "valid"]
}

for file in [
    "train2id.txt",
    "test2id.txt",
    "valid2id.txt",
    f"pickle{sep}ent2id.pkl",
    f"pickle{sep}rel2id.pkl",
    f"pickle{sep}class2id.pkl",
    f"pickle{sep}instype_all.pkl",
    f"pickle{sep}r2id2dom2id.pkl",
    f"pickle{sep}r2id2range2id.pkl",
    f"pickle{sep}observed_heads_original_kg.pkl",
    f"pickle{sep}observed_tails_original_kg.pkl"
]:
    path=f"{dataset_target}{sep}{file}"
    if not exists(path):
        print("""
Command line error: missing file """ + path + """
    """)
        exit(0)

###################
# Loading dataset #
###################

print("Loading dataset")

dataset_pkl_folder=f"{dataset_target}{sep}pickle{sep}"

ent2id = None

with open(f"{dataset_pkl_folder}ent2id.pkl", "rb") as handle:
    ent2id = load(handle)

id2ent = {v: k for k, v in ent2id.items()}

rel2id = None

with open(f"{dataset_pkl_folder}rel2id.pkl", "rb") as handle:
    rel2id = load(handle)

id2rel = {v: k for k, v in rel2id.items()}

class2id = None

with open(f"{dataset_pkl_folder}class2id.pkl", "rb") as handle:
    class2id = load(handle)

id2class = {v: k for k, v in class2id.items()}

r2id2dom2id = None

with open(f"{dataset_pkl_folder}r2id2dom2id.pkl", "rb") as handle:
    r2id2dom2id = load(handle)

r2id2range2id = None

with open(f"{dataset_pkl_folder}r2id2range2id.pkl", "rb") as handle:
    r2id2range2id = load(handle)

observed_heads_original_kg = None

with open(f"{dataset_pkl_folder}observed_heads_original_kg.pkl", "rb") as handle:
    observed_heads_original_kg = load(handle)

observed_tails_original_kg = None

with open(f"{dataset_pkl_folder}observed_tails_original_kg.pkl", "rb") as handle:
    observed_tails_original_kg = load(handle)

observed_heads_inv = None

with open(f"{dataset_pkl_folder}observed_heads_inv.pkl", "rb") as handle:
    observed_heads_inv = load(handle)

observed_tails_inv = None

with open(f"{dataset_pkl_folder}observed_tails_inv.pkl", "rb") as handle:
    observed_tails_inv = load(handle)

instype_all = None

with open(f"{dataset_pkl_folder}instype_all.pkl", "rb") as handle:
    instype_all = load(handle)

class2id2ent2id = None

with open(f"{dataset_pkl_folder}class2id2ent2id.pkl", "rb") as handle:
    class2id2ent2id = load(handle)

###########################
# Scoring best_solution dataset #
###########################

def score(solution):
    score=0
    counts={split: {sign_type: 0 for sign_type in ["signed", "domained_only", "ranged_only", "unsigned"]} for split in ["train", "test", "valid"]}
    for split in predicates_counts.keys():
        for rel in predicates_counts[split].keys():
            domained = solution[rel]["domain"]
            ranged = solution[rel]["range"]

            counts[split]["signed"] += predicates_counts[split][rel] if domained and ranged else 0
            counts[split]["domained_only"] += predicates_counts[split][rel] if domained and not ranged else 0
            counts[split]["ranged_only"] += predicates_counts[split][rel] if ranged and not domained else 0
            counts[split]["unsigned"] += predicates_counts[split][rel] if not domained and not ranged else 0

        split_sum=0
        for sign_type in counts[split]:
            split_sum += abs(counts[split][sign_type] - target_rates[split][sign_type] * sum(predicates_counts[split].values()))
        
        score += split_sum / sum(predicates_counts[split].values())
                                                                                                                                 
    return score
        

#####################
# Initialize search #
#####################

total=len(rel2id.values())

signed=[
    p
    for p in rel2id.values()
    if p in r2id2dom2id.keys() 
    and p in r2id2range2id.keys()
]

domain_no_range = [
    p
    for p in rel2id.values()
    if p in r2id2dom2id.keys() 
    and not p in r2id2range2id.keys()
]

range_no_domain = [
    p
    for p in rel2id.values()
    if not p in r2id2dom2id.keys() 
    and p in r2id2range2id.keys()
]

not_signed = [
    p
    for p in rel2id.values()
    if not p in r2id2dom2id.keys() 
    and not p in r2id2range2id.keys()
]

predicates_counts={split: {rel: 0 for rel in id2rel.keys()} for split in ["train", "test", "valid"]}

for split in ["train", "test", "valid"]:
    nb_lines=sum(1 for _ in open(f"{dataset_target}{sep}{split}2id.txt", "r", encoding="utf-8"))
    with open(f"{dataset_target}{sep}{split}2id.txt", "r", encoding='utf-8') as r:
        with tqdm(enumerate(r), total=nb_lines, disable=True) as bar:
            bar.set_description(f"Analizing split {split}")
            for i, line in bar:
                p = int(line.strip().split("\t")[1])
                predicates_counts[split][p] += 1

best_solution={rel: {"domain": rel in r2id2dom2id, "range": rel in r2id2range2id} for rel in id2rel.keys()}
best_score=score(best_solution)

true_count=0
for rel in best_solution.keys():
    for sign_side in best_solution[rel].keys():
        if not best_solution[rel][sign_side]:
            continue
        true_count+=1

with tqdm([], total=true_count) as bar:
    while True:
        search_ongoing = False
    
    
        next_solution=None
        next_score=None
    
        bar.set_description(f"Current score: {best_score}")
    
        for rel in best_solution.keys():
            for sign_side in best_solution[rel].keys():
                
                if not best_solution[rel][sign_side]:
                    continue
                    
                new_candidate=deepcopy(best_solution)
                new_candidate[rel][sign_side]=False
                new_score=score(new_candidate)
    
                if (not next_score is None) and next_score < new_score:
                    continue
    
                next_solution=new_candidate
                next_score=new_score
    
        if (not next_solution is None) and next_score < best_score:
            best_solution=next_solution
            best_score=next_score
            bar.update(1)
        else:
            bar.update(bar.total - bar.n)
            break

counts={
    split: {
        sign_type: 0 for sign_type in ["signed", "domained_only", "ranged_only", "unsigned"]
    } for split in ["train", "test", "valid"]
}

for split in predicates_counts.keys():
    for rel in predicates_counts[split].keys():
        domained = best_solution[rel]["domain"]
        ranged = best_solution[rel]["range"]

        counts[split]["signed"] += predicates_counts[split][rel] if domained and ranged else 0
        counts[split]["domained_only"] += predicates_counts[split][rel] if domained and not ranged else 0
        counts[split]["ranged_only"] += predicates_counts[split][rel] if ranged and not domained else 0
        counts[split]["unsigned"] += predicates_counts[split][rel] if not domained and not ranged else 0

for split in counts.keys():
    print(f"Split {split}")
    for sign_type in counts[split].keys():
        total_triples=sum(predicates_counts[split].values())
        ratio = counts[split][sign_type] / sum(predicates_counts[split].values())
        ratio = int(100000*ratio/1000)
        space1 = " " * (20-len(sign_type))
        space2 = space1[-len(str(counts[split][sign_type])):]
        print(f"    {sign_type}:{space1}{counts[split][sign_type]}{space2} ({ratio} %)")

#############################
# Exporting the new dataset #
#############################

new_dataset_name=f"{dataset_name}_{str(signed_rate)}_{str(domained_rate)}_{str(ranged_rate)}"
new_dataset_target=f"{datasets_folder}{sep}{new_dataset_name}"
new_pickle_folder=f"{new_dataset_target}{sep}pickle{sep}"

print(f"Exporting dataset in {new_dataset_target}")

makedirs(new_dataset_target, exist_ok=True)
makedirs(new_pickle_folder, exist_ok=True)

new_r2id2dom2id={
    relid: classid
    for relid, classid in r2id2dom2id.items()
    if best_solution[relid]["domain"]
}

new_r2id2range2id={
    relid: classid
    for relid, classid in r2id2range2id.items()
    if best_solution[relid]["range"]
}

with tqdm([
    ("ent2id",ent2id),
    ("rel2id",rel2id),
    ("class2id",class2id),
    ("r2id2dom2id",new_r2id2dom2id),
    ("r2id2range2id",new_r2id2range2id),
    ("observed_heads_original_kg",observed_heads_original_kg),
    ("observed_tails_original_kg",observed_tails_original_kg),
    ("observed_heads_inv",observed_heads_inv),
    ("observed_tails_inv",observed_tails_inv),
    ("instype_all",instype_all),
    ("class2id2ent2id",class2id2ent2id),
]) as bar:
    for filename, dictionary in bar:
        bar.set_description(f"Exporting dictionary {filename}")
        with open(f"{new_pickle_folder}{filename}.pkl", "wb") as handle:
            dump(dictionary, handle)

with tqdm(["train2id", "test2id", "valid2id"]) as bar:
    for filename in bar:
        bar.set_description(f"Exporting split {filename[:-3]}")
        copy_file(f"{dataset_target}{sep}{filename}.txt", f"{new_dataset_target}{sep}{filename}.txt")

print(f"Done, check folder {new_dataset_target}")