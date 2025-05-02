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
check_software "k3d" "kubectl"


k3d cluster start $K3D_CLUSTER_NAME --wait
sleep 10
kubectl wait --for=condition=Ready nodes --all --timeout=120s
