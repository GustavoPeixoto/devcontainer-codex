FROM node:24.19.0-alpine AS development

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

ARG WORKSPACE_DIR
RUN : "${WORKSPACE_DIR:?WORKSPACE_DIR build arg is required}"

RUN apk add --no-cache bash

    # shadow é necessário para usermod e groupmod
RUN apk add --no-cache shadow \
    # renomea o usuário node (padrão da imagem)
    && groupmod --new-name ${USERNAME} node \
    && groupmod --gid ${USER_GID} ${USERNAME} \
    && usermod --login ${USERNAME} --uid ${USER_UID} --gid ${USER_GID} --move-home --home /home/${USERNAME} node \
    # cria as pastas relevantes
    && mkdir -p ${WORKSPACE_DIR} /home/${USERNAME}/.codex \
    # da permissões as pastas criadas
    && chown -R ${USERNAME}:${USERNAME} ${WORKSPACE_DIR} /home/${USERNAME}/.codex

RUN corepack enable

WORKDIR ${WORKSPACE_DIR}

USER ${USERNAME}

FROM node:24.19.0-alpine AS production

ARG WORKSPACE_DIR=/app

ENV NODE_ENV=production

WORKDIR ${WORKSPACE_DIR}

COPY apps/node/ ./

USER node

CMD ["node", "src/health.js"]
