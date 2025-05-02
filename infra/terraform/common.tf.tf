locals {
  common_tags = {
    Creator           = var.creator
    Environment       = var.environment
    GitRepository     = "Hydrosat/hydrosat-recruitment-exercise"
    PlatformTeamOwner = "engineering"
    Terraform         = "true"
    Workspace         = terraform.workspace
  }
}
