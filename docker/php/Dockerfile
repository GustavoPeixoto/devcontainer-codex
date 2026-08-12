FROM php:8.5.9-alpine AS development

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

ARG WORKSPACE_DIR
RUN : "${WORKSPACE_DIR:?WORKSPACE_DIR build arg is required}"

RUN apk add --no-cache bash

    # cria o usuário
RUN addgroup -g ${USER_GID} ${USERNAME} \
    && adduser -D -u ${USER_UID} -G ${USERNAME} -h /home/${USERNAME} ${USERNAME} \
    # cria as pastas relevantes
    && mkdir -p ${WORKSPACE_DIR} /home/${USERNAME}/.codex \
    # da permissões as pastas criadas
    && chown -R ${USERNAME}:${USERNAME} ${WORKSPACE_DIR} /home/${USERNAME}/.codex

WORKDIR ${WORKSPACE_DIR}

USER ${USERNAME}

FROM php:8.5.9-alpine AS production

ARG WORKSPACE_DIR=/app

WORKDIR ${WORKSPACE_DIR}

COPY apps/php/ ./

USER www-data

CMD ["php", "src/health.php"]
