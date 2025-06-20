# CourseTrack - SHIELD Foundry Course Scheduler - Backend

**Mark James Bonifacio** - MAR 10 2025 - JUN 9 2025

---

# 1. Setup the App

[1] Go to this website:
`https://github.com/lsibal/courseratracker_api`

[2] Once the repo is opened, click the **`<>Code`** button. Click HTTPS, and copy the URL. You will be getting this:

```
https://github.com/lsibal/courseratracker_api.git
```

[3] Open a command prompt in the desktop or any folder, and type this command:

```
git clone https://github.com/lsibal/courseratracker_api.git
```

The git repo will be cloned in the directory.

---

# 2. Run the App

## Make sure to run the courseratracker_ui SIMULTANEOUSLY for Hourglass API communication.

[1] Navigate to courseratracker_api folder in the file explorer. In the address bar, type `cmd`, or open a new command prompt in the folder directory.

[2] Once done, it will open a command prompt. Type `python app.py`.

[3] The command prompt will print a line something like this:

```
API Key loaded: 20fa96...2add
←[32mINFO←[0m:     Will watch for changes in these directories: ['C:\\Users\\Mark James\\Desktop\\SHIELD_FOUNDRY\\temp-repo-backend']
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://0.0.0.0:5000←[0m (Press CTRL+C to quit)
←[32mINFO←[0m:     Started reloader process [←[36m←[1m15420←[0m] using ←[36m←[1mStatReload←[0m
API Key loaded: 20fa96...2add
API Key loaded: 20fa96...2add
←[32mINFO←[0m:     Started server process [←[36m8748←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
Making request to https://hourglass-qa.shieldfoundry.com/api/resources with params: {'activeOnly': 'true', 'resourceType': 'Course', 'serviceOffering': '8'}
Response status: 200
```

[4] Go to the local address in a web browser. Type the `http://localhost:5173/` in the address bar.

---

# The End