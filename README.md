# geco_commons
Cryptocurrency common libs and fundamental modules

# Under construction

## Env 
- Base env: python3.7
  -  Refer to requirement.txt and Dockerfile in detail.

## Dependency
- Postgress
  - Need to install  libpq-dev and python3.x-dev
  ```
  RUN apt-get install -y libpq-dev 
  ```

## Introduction
1. Put INI files in place.
ini
├── config.ini
├── env.ini
├── hparams.yaml
├── log_config.ini
├── logging.log
├── model_config.ini
├── mongo_config.ini
└── private_api.ini
├── postgres_config.ini
2. Update ini
3. Copy almost same env info to shell config using in shells in remote and jupyter
shell
└── shell_config.conf
4. Update shell config
5. Update docker-compose and dockerfiles in each module outside.
   - Basically, it doesn't needs to deal  with this secation.  However, if update in regard to ENV, need to update docker setting.
6. DONE

