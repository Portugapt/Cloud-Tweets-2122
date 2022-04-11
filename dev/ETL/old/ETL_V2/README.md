Deploy Cloud Function

```bash
gcloud functions deploy upload_data \
    --region europe-west1 \
    --memory 1024MB \
    --runtime python38 \
    --trigger-resource gs://cloud-computing-2122-bjr-data \
    --trigger-event google.storage.object.finalize
```

Send data to bucket

```bash
gsutil cp data/220312-subset.csv gs://cloud-computing-2122-bjr-data/
```