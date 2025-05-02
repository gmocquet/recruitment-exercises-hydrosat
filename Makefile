.PHONY: clean colima-start colima-stop colima-delete minio-start minio-stop minio-delete k8s-start k8s-stop k8s-delete k8s-update tf-init tf-apply tf-delete s3-seed s3-move-late-files

MINIO_DATA_DIR?=$(shell pwd)/tmp/minio_data

auto-setup:
	$(MAKE) colima-start
	$(MAKE) minio-start
	$(MAKE) k8s-init
	$(MAKE) tf-init
	$(MAKE) tf-apply
	$(MAKE) s3-seed
	$(MAKE) k8s-update
	uv sync
	dagster dev

clean: colima-delete
	rm -rf $(shell pwd)/tmp/ || true
	rm -rf $(shell pwd)/.venv/ || true

stop:
	$(MAKE) minio-stop
	$(MAKE) k8s-stop

delete:
	$(MAKE) colima-delete
	$(MAKE) minio-delete

colima-start:
	colima start --cpu 8 --memory 16 --disk 120

colima-stop:
	colima stop

colima-delete:
	colima delete

minio-start:
	MINIO_DATA_DIR=$(MINIO_DATA_DIR) docker compose -f $(shell pwd)/infra/local/docker-compose.yml up -d

minio-stop:
	MINIO_DATA_DIR=$(MINIO_DATA_DIR) docker compose -f $(shell pwd)/infra/local/docker-compose.yml down

minio-delete:
	MINIO_DATA_DIR=$(MINIO_DATA_DIR) docker compose -f $(shell pwd)/infra/local/docker-compose.yml kill

tf-init:
	$(MAKE) -C $(shell pwd)/infra/terraform init

tf-apply:
	$(MAKE) -C $(shell pwd)/infra/terraform apply

tf-delete:
	$(MAKE) -C $(shell pwd)/infra/terraform destroy

k8s-init:
	$(shell pwd)/infra/local/k8s-init.sh

k8s-start:
	$(shell pwd)/infra/local/k8s-start.sh

k8s-stop:
	$(shell pwd)/infra/local/k8s-stop.sh

k8s-update:
	$(shell pwd)/infra/local/k8s-update.sh

docker-build:
	MINIO_DATA_DIR=$(MINIO_DATA_DIR) docker compose -f $(shell pwd)/infra/local/docker-compose.yml build

docker-run:
	MINIO_DATA_DIR=$(MINIO_DATA_DIR) docker compose -f $(shell pwd)/infra/local/docker-compose.yml up --build -d

docker-stop:
	MINIO_DATA_DIR=$(MINIO_DATA_DIR) docker compose -f $(shell pwd)/infra/local/docker-compose.yml down

docker-delete:
	MINIO_DATA_DIR=$(MINIO_DATA_DIR) docker compose -f $(shell pwd)/infra/local/docker-compose.yml kill

s3-seed:
	$(shell pwd)/infra/local/s3-seed.sh

s3-move-late-files:
	$(shell pwd)/infra/local/s3-move-late-files.sh
