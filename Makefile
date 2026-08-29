SERVICES := dev node php csharp

.DEFAULT_GOAL := help

.PHONY: help env env-dev env-node env-php env-csharp

help:
	@printf '%s\n' 'Available targets:'
	@printf '  %-16s %s\n' 'make help' 'Show this help message.'
	@printf '  %-16s %s\n' 'make env' 'Create root and service .env files for every service.'
	@printf '  %-16s %s\n' 'make env-dev' 'Create root .env and docker/dev/.env files.'
	@printf '  %-16s %s\n' 'make env-node' 'Create root .env and docker/node/.env files.'
	@printf '  %-16s %s\n' 'make env-php' 'Create root .env and docker/php/.env files.'
	@printf '  %-16s %s\n' 'make env-csharp' 'Create root .env and docker/csharp/.env files.'

env:
	@./bin/env $(SERVICES)

env-dev:
	@./bin/env dev

env-node:
	@./bin/env node

env-php:
	@./bin/env php

env-csharp:
	@./bin/env csharp
