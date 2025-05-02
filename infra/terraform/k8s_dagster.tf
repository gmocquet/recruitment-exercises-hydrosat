resource "kubernetes_namespace" "dagster" {
  metadata {
    name = "dagster"
  }
}

# Deploy Dagster
resource "helm_release" "dagster" {
  name       = "dagster"
  repository = "https://dagster-io.github.io/helm"
  chart      = "dagster"
  namespace  = kubernetes_namespace.dagster.metadata[0].name

  timeout    = 3600
  wait       = true
  wait_for_jobs = true

  set {
    name  = "dagster-webserver.enabled"
    value = "true"
  }

  values = [
    file("${path.module}/../k8s/helm/dagster/values.yaml")
  ]
}

resource "kubernetes_manifest" "minio_external" {
  manifest = yamldecode(file("${path.module}/../k8s/minio-external-service.yaml"))
}

resource "kubernetes_config_map" "dagster_env" {
  metadata {
    name      = "dagster-env"
    namespace = "dagster"
  }

  data = {
    for line in split("\n", file("${path.module}/../../.env.k8s")) :
    split("=", line)[0] => join("=", slice(split("=", line), 1, length(split("=", line))))
    if can(split("=", line)[0]) && !startswith(trimspace(line), "#") && trimspace(line) != ""
  }
}
