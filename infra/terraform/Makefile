ENVIRONMENT?=local
TERRAFORM ?= terraform

# Auto-fill the creator name if possible
# If that fails here, the creator will be asked interactively
TF_VAR_creator ?= $(shell echo "$(USER)")
ifneq ($(TF_VAR_creator),)
    export TF_VAR_creator
endif

TF_VAR_environment ?= $(ENVIRONMENT)
export TF_VAR_environment

.PHONY: fmt init upgrade-providers plan apply destroy

fmt:
	$(TERRAFORM) fmt -recursive

init:
	rm -rf .terraform
	rm -f terraform.tfstate || true
	rm -f terraform.tfstate.backup || true
	$(TERRAFORM) init

lock:
	rm -rf .terraform.lock.hcl
	$(TERRAFORM) providers lock -platform=linux_amd64 -platform=darwin_amd64 -platform darwin_arm64

# Upgrade providers according to versions constraints defined in versions.tf
upgrade-providers:
	$(TERRAFORM) init -upgrade
	$(TERRAFORM) providers lock -platform=linux_amd64 -platform=darwin_amd64 -platform darwin_arm64

plan:
	./tf-vars.sh $(TERRAFORM) plan

apply:
	@echo
	@echo "Do you want to perform these actions?"
	@echo "  Terraform will perform the actions described above."
	@echo "  Only 'yes' will be accepted to approve."
	@echo
	@read -p "   Enter a value: " -r \
		&& [ "$${REPLY}" == "yes" ] \
		&& ./tf-vars.sh $(TERRAFORM) apply

destroy:
	@echo
	@echo "You are about to destroy local env?"
	@read -p "Type \"yes\" to confirm the destruction: " -r \
		&& [ "$${REPLY}" == "yes" ] \
		&& ./tf-vars.sh $(TERRAFORM) destroy
