FROM node:24.19.0-alpine AS development

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

ARG WORKSPACE_DIR
RUN : "${WORKSPACE_DIR:?WORKSPACE_DIR build arg is required}"

ENV COREPACK_HOME=/home/${USERNAME}/.cache/node/corepack

RUN apk add --no-cache bash shadow \
    # renomea o usuário node (padrão da imagem)
    && groupmod --new-name ${USERNAME} node \
    && groupmod --gid ${USER_GID} ${USERNAME} \
    && usermod --login ${USERNAME} --uid ${USER_UID} --gid ${USER_GID} --move-home --home /home/${USERNAME} node \
    # cria as pastas relevantes
    && mkdir -p ${WORKSPACE_DIR} ${COREPACK_HOME} \
    # da permissões as pastas criadas
    && chown -R ${USERNAME}:${USERNAME} ${WORKSPACE_DIR} /home/${USERNAME}

RUN corepack enable

WORKDIR ${WORKSPACE_DIR}

USER ${USERNAME}

CMD ["sleep", "infinity"]

FROM node:24.19.0-alpine AS build

ARG WORKSPACE_DIR=/app

ENV COREPACK_HOME=/home/node/.cache/node/corepack

WORKDIR ${WORKSPACE_DIR}

RUN corepack enable \
    && mkdir -p ${COREPACK_HOME} \
    && chown -R node:node /home/node/.cache ${WORKSPACE_DIR}

COPY --chown=node:node apps/node/package.json apps/node/yarn.lock apps/node/.yarnrc.yml ./

USER node

RUN yarn install --immutable

COPY --chown=node:node apps/node/tsconfig.json ./tsconfig.json
COPY --chown=node:node apps/node/src ./src

RUN yarn build \
    && yarn workspaces focus --production

FROM node:24.19.0-alpine AS production

ARG WORKSPACE_DIR=/app

ENV NODE_ENV=production

WORKDIR ${WORKSPACE_DIR}

COPY --from=build --chown=node:node ${WORKSPACE_DIR}/package.json ./package.json
COPY --from=build --chown=node:node ${WORKSPACE_DIR}/node_modules ./node_modules
COPY --from=build --chown=node:node ${WORKSPACE_DIR}/dist ./dist

USER node

CMD ["node", "dist/index.js"]
