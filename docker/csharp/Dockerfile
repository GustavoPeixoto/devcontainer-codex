FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS development

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

ARG WORKSPACE_DIR
RUN : "${WORKSPACE_DIR:?WORKSPACE_DIR build arg is required}"

RUN apk add --no-cache bash

    # shadow é necessário para usermod e groupmod
RUN apk add --no-cache shadow \
    # renomea o usuário app (padrão da imagem)
    && groupmod --new-name ${USERNAME} app \
    && groupmod --gid ${USER_GID} ${USERNAME} \
    && usermod --login ${USERNAME} --uid ${USER_UID} --gid ${USER_GID} --move-home --home /home/${USERNAME} app \
    # cria as pastas relevantes
    && mkdir -p ${WORKSPACE_DIR} /home/${USERNAME} \
    # da permissões as pastas criadas
    && chown -R ${USERNAME}:${USERNAME} ${WORKSPACE_DIR} /home/${USERNAME}

WORKDIR ${WORKSPACE_DIR}

USER ${USERNAME}

FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build

ARG WORKSPACE_DIR=/src

WORKDIR ${WORKSPACE_DIR}

COPY apps/csharp/*.csproj ./
RUN dotnet restore

COPY apps/csharp/ ./
RUN dotnet publish --configuration Release --no-restore --output /app/publish

FROM mcr.microsoft.com/dotnet/runtime:10.0-alpine AS production

ARG WORKSPACE_DIR=/app

WORKDIR ${WORKSPACE_DIR}

COPY --from=build /app/publish ./

USER app

ENTRYPOINT ["dotnet", "Health.dll"]
