FROM mcr.microsoft.com/devcontainers/javascript-node:24-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        build-essential \
        ca-certificates \
        curl \
        fd-find \
        git \
        jq \
        less \
        openssh-client \
        pkg-config \
        python3 \
        python3-pip \
        python3-venv \
        ripgrep \
        tar \
        unzip \
        xz-utils \
        zip \
    && rm -rf /var/lib/apt/lists/*

RUN corepack enable

RUN yarn global add @fission-ai/openspec@latest
