Para executar os serviços de listagem é necessário definir variavel de ambiente "GOOGLE_ACCOUNT_KEY" com o path para o ficheiro com a key.



docker run -v /home/bosutike/pythonBigQuery_credentials.json:/services/list/pythonBigQuery_credentials.json -e GOOGLE_ACCOUNT_KEY=/services/list/pythonBigQuery_credentials.json -p 50084:50084 list-tweet-search


## Create Kubernets cluster

gcloud beta container --project "cadeira-nuvem-2122" clusters create "twitter-renato-services-cluster" --zone "europe-west1-d" --no-enable-basic-auth --cluster-version "1.21.6-gke.1503" --release-channel "regular" --machine-type "e2-medium" --image-type "COS_CONTAINERD" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/bigquery","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --max-pods-per-node "110" --num-nodes "3" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/cadeira-nuvem-2122/global/networks/default" --subnetwork "projects/cadeira-nuvem-2122/regions/europe-west1/subnetworks/default" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --enable-shielded-nodes --node-locations "europe-west1-d"





gcloud container --project "cadeira-nuvem-2122" clusters create "twitter-renato-services-cluster" --zone "europe-west1-d"

gcloud container clusters get-credentials twitter-renato-services-cluster --zone europe-west1-d --project cadeira-nuvem-2122


helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install --replace nginx-ingress ingress-nginx/ingress-nginx

kubectl get deployment nginx-ingress-ingress-nginx-controller

kubectl get service nginx-ingress-ingress-nginx-controller