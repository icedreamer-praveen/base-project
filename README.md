## To use project init script

```bash
- 1. Run project_init.py
- 2. Enter new project location(absolute path)
- 3. Enter new project name
```

## DOCKER 
```
- 1. Install [docker](https://get.docker.com/) and [docker-compose](https://docs.docker.com/compose/install/)
- 2. Run the server docker-compose up -d
```

## Guidelines
1. Update in SPECTACULAR_SETTINGS title and description
2. Update in LOGGING format and filename
3. Replace backend keyword with your project name in Jenkins file
- For Example: select backend keyword and enter keyboard shortcut ``ctrl+shift+L `` then replace with your project name.

## <<<< Backend with bolier plate codes >>>>

## Features
## Prometheus:
   ```Description : Django-Prometheus

                    This library contains code to expose some monitoring metrics relevant to Django internals so they can be monitored by Prometheus.io.

    in files : backend > settings.py > THIRD_PARTY_APPS, MIDDLEWARE
              utilis > views.py, urls.py
              requirements.txt
```