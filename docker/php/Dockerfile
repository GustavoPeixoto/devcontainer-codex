FROM ghcr.io/php/pie:1.4.10-bin AS pie

FROM php:8.5.10-alpine AS base

RUN docker-php-ext-install -j"$(nproc)" pdo_mysql

FROM base AS development

RUN cp "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
COPY docker/php/php.ini $PHP_INI_DIR/conf.d/90-project.ini
COPY docker/php/php.ini-development $PHP_INI_DIR/conf.d/99-environment.ini

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

ARG WORKSPACE_DIR
RUN : "${WORKSPACE_DIR:?WORKSPACE_DIR build arg is required}"

RUN apk add --no-cache bash git unzip

# PIE é montado apenas neste RUN; ele também habilita a extensão instalada.
# Dependências de compilação ficam disponíveis apenas durante a instalação.
RUN --mount=type=bind,from=pie,source=/pie,target=/usr/local/bin/pie \
    apk add --no-cache --virtual .xdebug-build-deps $PHPIZE_DEPS linux-headers libtool \
    && pie install --no-interaction --no-cache \
        --no-system-dependencies-check xdebug/xdebug:3.5.3 \
    && rm -rf /root/.pie \
    && apk del .xdebug-build-deps

COPY --from=composer:2.10.3 /usr/bin/composer /usr/local/bin/composer

    # cria o usuário
RUN addgroup -g ${USER_GID} ${USERNAME} \
    && adduser -D -u ${USER_UID} -G ${USERNAME} -h /home/${USERNAME} ${USERNAME} \
    # cria as pastas relevantes
    && mkdir -p ${WORKSPACE_DIR} /home/${USERNAME} \
    # da permissões as pastas criadas
    && chown -R ${USERNAME}:${USERNAME} ${WORKSPACE_DIR} /home/${USERNAME}

WORKDIR ${WORKSPACE_DIR}

USER ${USERNAME}

CMD ["sleep", "infinity"]

FROM base AS production

RUN cp "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY docker/php/php.ini $PHP_INI_DIR/conf.d/90-project.ini
COPY docker/php/php.ini-production $PHP_INI_DIR/conf.d/99-environment.ini

ARG WORKSPACE_DIR=/app

WORKDIR ${WORKSPACE_DIR}

COPY apps/php/ ./

USER www-data

CMD ["php", "src/health.php"]
