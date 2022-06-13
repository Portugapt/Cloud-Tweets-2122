import pulumi
from pulumi_gcp import storage

# Create a GCP resource (Storage Bucket)
bucket = storage.Bucket('tweets-landing-zone')

# Export the DNS name of the bucket
pulumi.export('tweets-landing-zone',  bucket.url)
