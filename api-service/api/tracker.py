
import os
import asyncio
from glob import glob
import json
import pandas as pd

import tensorflow as tf
from google.cloud import storage


gcp_project = os.environ["GCP_PROJECT"]
bucket_name = "cryptist-data"
local_experiments_path = "/persistent/experiments"

# Setup experiments folder
if not os.path.exists(local_experiments_path):
    os.mkdir(local_experiments_path)


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def download_data():
    # Get all model metrics
    models_metrics_list = tf.io.gfile.glob(
        "gs://"+bucket_name+"/*/*/*_model_metrics.json")
    filename1 = "gs://"+bucket_name+"/ffnn_data_array_bid_price1.npy"
    filename2 = "gs://"+bucket_name+"/ffnn_model.h5"
    filename3 = "gs://"+bucket_name+"/ffnn_model_df_max.csv"
    filename4 = "gs://"+bucket_name+"/ffnn_model_df_min.csv"
    filename5 = "gs://"+bucket_name+"/ffnn_x_test_5steps.npy"
    filename6 = "gs://"+bucket_name+"/test-bucket-access.txt"
    models_metrics_list = [filename1, filename2,
                           filename3, filename4, filename5, filename6]
    timestamp = 0

    for metrics_file in models_metrics_list:
        path_splits = metrics_file.split("/")
        local_metrics_file = path_splits[-1]

        local_metrics_file = os.path.join(
            local_experiments_path, local_metrics_file)

        if not os.path.exists(local_metrics_file):
            print("Copying:", metrics_file, local_metrics_file)

            metrics_file = metrics_file.replace(
                "gs://"+bucket_name+"/", "")
            # Download the metric json file
            download_blob(bucket_name, metrics_file,
                          local_metrics_file)

            file_timestamp = os.path.getmtime(local_metrics_file)
            if file_timestamp > timestamp:
                timestamp = file_timestamp

    return timestamp


class TrackerService:
    def __init__(self):
        self.timestamp = 0

    async def track(self):
        while True:
            await asyncio.sleep(60)
            print("Tracking experiments...")

            # Download new model metrics
            timestamp = download_data()

            #if timestamp > self.timestamp:
                # Aggregate all experiments across users
                # agg_experiments()

                # Compute Leaderboard and find best model
                # compute_leaderboard()

                # Download best model
                # download_best_models(
