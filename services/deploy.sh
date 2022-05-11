### Please make sure you run this script on path ./Cloud-Tweets-2122/services

# Create cluster
gcloud container --project "cadeira-nuvem-2122" clusters create "twitter-renato-services-cluster" --zone "europe-west1-d"

# Kubeconfig
gcloud container clusters get-credentials twitter-renato-services-cluster --zone europe-west1-d --project cadeira-nuvem-2122

# Create secret "bigquery-key" with content of file Cloud-Tweets-2122/services/keys/pythonBigQuery_credentials.json
kubectl create secret generic bigquery-key --from-file=pythonBigQuery_credentials.json=keys/pythonBigQuery_credentials.json

# Install ingress-nginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install --replace nginx-ingress ingress-nginx/ingress-nginx

# Deploy ingress-nginx
kubectl get deployment nginx-ingress-ingress-nginx-controller

# Get ingress-nginx controller ip as a variable
nginx_ingress_external_ip=0
while ! [[ $nginx_ingress_external_ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]
do
    kubectl get service nginx-ingress-ingress-nginx-controller --output jsonpath='{.status.loadBalancer.ingress[0].ip}'
    sleep 1
    nginx_ingress_external_ip=$(kubectl get service nginx-ingress-ingress-nginx-controller --output jsonpath='{.status.loadBalancer.ingress[0].ip}')   
done

# Generate ingress.yaml from template_ingress.yaml file updated with new ip
cp template_ingress.yaml ingress.yaml
sed -i "s/HOST_IP/$nginx_ingress_external_ip/g" ingress.yaml

# Apply list services
kubectl apply -f services-deployment-list.yaml
# Apply admin services
kubectl apply -f services-deployment-admin.yaml
# Apply nginx ingress
kubectl apply -f ingress.yaml