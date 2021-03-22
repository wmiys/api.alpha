# api.wmiys
Api for the the backend



## Starting up the flask server


In powershell:

Change your directory to the folder containing `main.py`

```
cd app\directory\with\main.py
```

Set `FLASK_APP` enviornment variables to `main.py`

```
$env:FLASK_APP = "main.py"
```

Set `FLASK_ENV` enviornment variables to `development`

```
$env:FLASK_ENV = "development"
```

Start up the server.

```
python -m flask run --host=0.0.0.0
```

Now in the browser go to [http://localhost:5000](http://localhost:5000)
