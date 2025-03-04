
[[IoT.excalidraw.png]]

``` Power Shell
tree /F /A | findstr /V ".venv"|   .env
```
# Tree
|   .gitignore
|   docker-compose.yaml
|   Dockerfile
|   makefile
|   readMe.MD
|   requirements.txt
|   TODO.md
|   
+---.vscode
|       extensions.json
|       launch.json
|       
+---app
|   |   main.py
|   |
|   +---api
|   |       auth.py
|   |       __init__.py
|   |
|   +---db
|   |       database.py
|   |       security.py
|   |       __init__.py
|   |
|   +---models
|   |       model.py
|   |       session.py
|   |       __init__.py
|   |
|   \---router
|           sensor_data.py
|           server.py
|           __init__.py
|
+---modelos
\---test
        req.py
        test_model.py