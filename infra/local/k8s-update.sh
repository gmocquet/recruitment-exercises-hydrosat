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
check_software "k3d" "docker" "kubectl" "helm"


kubectl config use-context "$K8S_CLUSTER_NAME"


kubectl delete configmap dagster-env -n dagster --ignore-not-found
kubectl create configmap dagster-env --from-env-file=.env.k8s -n dagster
kubectl get configmap dagster-env -n dagster -o yaml


MINIO_DATA_DIR="$(SCRIPT_ROOT_DIR)/../../tmp/minio_data" docker compose -f "$SCRIPT_ROOT_DIR/docker-compose.yml" build
k3d image import dagster-app:latest -c "$K3D_CLUSTER_NAME"
helm upgrade --install dagster dagster/dagster -f $SCRIPT_ROOT_DIR/../k8s/helm/dagster/values.yaml --namespace "$K8S_DAGSTER_NAMESPACE"
