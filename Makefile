TAG := "game-engine-hiro"

AZ_REPO_LINK := "bzinfdevqacr.azurecr.io"
TARGET_REPOSITORY := "gaming" #temporarily using gaming registry


docker-build:
	docker build -f Dockerfile --tag bzinga-game-engine:${TAG} .
push:
	az acr login --name  bzinfdevqacr
	docker tag ${TARGET_REPOSITORY}:${TAG} ${AZ_REPO_LINK}/${TARGET_REPOSITORY}:${TAG}
	docker push ${AZ_REPO_LINK}/${TARGET_REPOSITORY}:${TAG}
images-push: docker-build push

deploy:
	make images-push
	ssh bz-dev
	kubectl set image deployment/game-engine -n bzinga game-engine=${TAG} --record
	kubectl rollout restart deployment/game-engine -n bzinga