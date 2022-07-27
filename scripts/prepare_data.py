"""
Prepare the OHSUMED dataset for indexing. Records from the dataset 
are saved as individual JSON files.
"""

import pandas as pd
import json
import os
import argparse
import logging
from tqdm import tqdm
# See https://github.com/huggingface/datasets for the
# installation instruction of the "datasets" package.
from datasets import load_dataset

# Set logging level
logging.basicConfig(level=logging.INFO)

# Read the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--dir", required=True,
                help='Output directory')

args, _ = ap.parse_known_args()
args = vars(args)
dir = args["dir"]

logging.info(f"[INFO] Input arguments{args}")


def main():
    # Download the dataset from the HuggingFace repository,
    # see https://huggingface.co/datasets/ohsumed for more details on the dataset.
    # The combined train and test dataset (348,564 records) will be used for indexing.
    logging.info(f"[INFO] Loading the dataset")
    ohsumed_dataset = load_dataset("ohsumed", split='train+test')

    # Store the dataset in a pandas dataframe
    logging.info(f"[INFO] Preprocessing the dataset")
    df_json = pd.DataFrame(ohsumed_dataset)

    # Preprocess the data
    df_json["medline_ui"] = df_json["medline_ui"].astype("string")
    df_json["author"] = df_json["author"].str.split("; ")
    df_json["mesh_terms"] = df_json["mesh_terms"].str.split("; ")

    # Convert the dataframe to a JSON array
    json_array = df_json.to_json(orient="records")
    parsed = json.loads(json_array)

    # Save each record as a JSON file in the specified output directory
    logging.info(f"[INFO] Saving each record as a JSON file")
    file_type = ".json"
    # The use of the tqdm function is optional. It's used to show the progress bar.
    for entry in tqdm(parsed):
        file_name = os.path.join(dir, entry["medline_ui"]+file_type)
        with open(file_name, 'w') as f:
            json.dump(entry, f)


# Usage example: python prepare_data.py -o ../../output
if __name__ == '__main__':
    main()
