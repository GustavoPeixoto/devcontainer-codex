FROM mcr.microsoft.com/devcontainers/javascript-node:24-bookworm

ARG USERNAME=dev

ARG WORKSPACE_DIR
RUN : "${WORKSPACE_DIR:?WORKSPACE_DIR build arg is required}"

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
        util-linux \
        xz-utils \
        zip \
    && rm -rf /var/lib/apt/lists/*

# renomea o usuário node (padrão da imagem)
RUN usermod --login ${USERNAME} --move-home --home /home/${USERNAME} node \
    && groupmod --new-name ${USERNAME} node

# habilita o usuário a usar sudo sem senha
RUN mkdir -p /etc/sudoers.d \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

RUN corepack enable

RUN python3 -m venv /opt/headroom \
    && /opt/headroom/bin/pip install --no-cache-dir --only-binary=headroom-ai 'headroom-ai[proxy]==0.39.1' \
    && ln -s /opt/headroom/bin/headroom /usr/local/bin/headroom

COPY docker/dev/bin/ /usr/local/bin/
COPY docker/dev/.codex/ /usr/local/.codex/
RUN chmod +x \
    /usr/local/bin/codex \
    /usr/local/bin/setup-codex-context-mode \
    /usr/local/bin/setup-codex-headroom \
    /usr/local/bin/start-headroom-proxy

RUN git config --system --add safe.directory ${WORKSPACE_DIR}

RUN yarn global add @fission-ai/openspec@1.14.0 \
    && openspec config set profile custom \
    && openspec config set workflows '["propose","explore","apply","update","sync","archive","verify"]'

RUN yarn global add context-mode@1.0.169

USER ${USERNAME}

RUN openspec config set profile custom \
    && openspec config set workflows '["propose","explore","apply","update","sync","archive","verify"]'