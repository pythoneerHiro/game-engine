
alias redis="kubectl config set-context --current --namespace=redis"
alias bzinga="kubectl config set-context --current --namespace=bzinga"

today=$(date '+%d-%m-%Y-%H-%M-%S')
dockerTag=user-svc-hiro-$today
acr=bzinfdevqacr.azurecr.io/gaming:$dockerTag

cd user-svc
git pull
git branch -v

docker build -f Dockerfile --tag $dockerTag  .
docker login bzinfdevqacr.azurecr.io --username bzinfdevqacr --password w9OgXTm2+y669pFPZRzJ9VRc/GGpqDhb
#az acr login --name  bzinfdevqacrc
docker tag $dockerTag $acr
docker push $acr
kubectl set image deployment/user-svc -n bzinga user-svc=$acr
kubectl scale deployment user-svc --replicas=10
watch -n 0 kubectl get pods


