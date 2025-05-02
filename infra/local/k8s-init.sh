#!/usr/bin/env bash
set -eu

SCRIPT_ROOT_DIR="$(realpath $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))"

K3D_CLUSTER_NAME="local-hydrosat-cluster"   # Get with: k3d cluster list
K8S_CLUSTER_NAME="k3d-${K3D_CLUSTER_NAME}"  # Get with: kubectl config get-clusters

K8S_DAGSTER_NAMESPACE="dagster"


check_software() {
    local programs=("$@")
    for program in "${programs[@]}"; do
        if ! command -v "$program" &> /dev/null; then
        echo "Error: $program is not installed. Please install it and try again."
        exit 1
        fi
    done
}
check_software "k3d" "kubectl" "docker"


if k3d cluster list | grep -q "$K3D_CLUSTER_NAME"; then
     echo "A cluster named '$K3D_CLUSTER_NAME' already exists."
     read -p "Do you want to delete the previous cluster? (y/n): " answer

     if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
         echo "Deleting existing cluster..."
         k3d cluster delete $K3D_CLUSTER_NAME
         echo "Cluster deleted. Creating a new one..."
     else
         echo "Keeping existing cluster. Exiting."
         exit 0
     fi
fi
echo "Creating new cluster '$K3D_CLUSTER_NAME'..."
k3d cluster create $K3D_CLUSTER_NAME \
    --agents 0 \
    --api-port 6443 \
    --port 3001:30001@loadbalancer \
    --k3s-arg "--disable=traefik@server:0"
sleep 10
kubectl wait --for=condition=Ready nodes --all --timeout=120s
k3d cluster list

MINIO_DATA_DIR="$(SCRIPT_ROOT_DIR)/../../tmp/minio_data" docker compose -f "$SCRIPT_ROOT_DIR/docker-compose.yml" build
k3d image import dagster-app:latest -c "$K3D_CLUSTER_NAME"
