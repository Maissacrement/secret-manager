# Intro

This service was not written to read the secrets inside containers !!!<br>Nor is it a way for you to update your secrets on a container !!!!<br>This service is able, from the environment variable provided locally in the context of the "secret-manager" container, to parse a file or a directory recursively and to provision it on the container or group of containers mentioned in a totally transparent manner. The variables will be taken directly from the read-only file

Conventional writing of an automatically deploy file:<br>`<name|id>_path.to.file`

<img src="./assets/provider.diagram.png" style="width:100%;">

## Default config

## Reload config

## Provide config

## Constraint containers