# Flask-chat

## Manage Conda ENV

### Create
```
conda env create -n python-flask-chat-env -f ./env.yml
```

### Update
```
conda env update -n python-flask-chat-env -f ./env.yml
```

### Remove
```
conda env remove --n python-flask-chat-env
```

### List
```
conda env list
```

### Activate
```
conda activate python-flask-chat-env
```

## To Execute

```
uvicorn src.main:asgi_app --host 0.0.0.0 --port 8000 --workers 4 --reload
```

## Links

[github_author](https://github.com/Diegoomal)
[github_template_1](https://github.com/Diegoomal/rag-module)
[github_template_2](https://github.com/Diegoomal/PythonFlaskPlatformSetup)

[generate-token](https://github.com/settings/tokens)
[freecodecamp-tutorial](https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/)
[digitalocean-migration-tutorial](https://www.digitalocean.com/community/tutorials/how-to-perform-flask-sqlalchemy-migrations-using-flask-migrate)