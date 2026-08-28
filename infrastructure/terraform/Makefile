.PHONY: init plan apply destroy fmt validate output ssh

# Môi trường dev (nơi chứa main.tf)
ENV_DIR := enviroiments/dev

init:
	@echo "Initializing..."
	terraform -chdir=$(ENV_DIR) init -upgrade

plan:
	terraform -chdir=$(ENV_DIR) plan

apply:
	terraform -chdir=$(ENV_DIR) apply

destroy:
	terraform -chdir=$(ENV_DIR) destroy

fmt:
	terraform fmt -recursive

validate:
	terraform -chdir=$(ENV_DIR) validate

output:
	terraform -chdir=$(ENV_DIR) output

# SSH nhanh vào VM sau khi apply
ssh:
	@$$(terraform -chdir=$(ENV_DIR) output -raw ssh_command)
