VER=0.0.11
HOSTNAME=us-east4-docker.pkg.dev
PROD_PROJECT_ID=lakehouse-production
STAG_PROJECT_ID=lakehouse-staging
REPOSITORY=airflow
IMAGE_NAME=quickbooks-jobs
BLD_IMG=$(HOSTNAME)/$(PROD_PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VER)
STG_IMG=$(HOSTNAME)/$(STAG_PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):staging-$(VER)

git:
	git add .
	git commit -m "$m"
	git push -u origin main 

docker-pull:
	docker pull $(BLD_IMG)

docker-build:
	docker build -f Dockerfile \
		--platform=linux/amd64 \
		--tag $(BLD_IMG) .

docker-build-stg:
	docker build -f Dockerfile \
		--platform=linux/amd64 \
		--tag $(STG_IMG) .

docker-push:
	docker push $(BLD_IMG)

docker-push-stg:
	docker push $(STG_IMG)

docker-bash:
	docker run -it --rm $(STG_IMG) /bin/bash
	
docker-run-stg: 
	docker run --rm $(STG_IMG) 