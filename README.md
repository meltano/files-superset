# files-superset

Note: This file-bundle is functional but is still Beta. Its intended for local instances only. Please test it out and provide feedback, contributions are always welcome too!

Meltano project [file bundle](https://meltano.com/docs/command-line-interface.html#file-bundle) for [Superset](https://superset.apache.org/). These files were pulled from the [Superset docker guide](https://superset.apache.org/docs/installation/installing-superset-using-docker-compose) with some minor adjustments.

Files:
- [`analyze/docker-compose.yml`](./bundle/analyze/docker-compose.yml) 
- [`analyze/docker/*.sh`](./bundle/analyze/docker/) All the scripts used by docker-compose
- [`analyze/docker/requirments-local.txt`](./bundle/analyze/docker/requirments-local.txt) A python requirements file for extra dependencies needed.
- [`analyze/assets/`](./bundle/analyze/assets) A directory with subdirectories for Superset assets that are exported. Currently charts and dashboards are the only required assets since they include content for their respective databases and datasets.

See [setup.py](./setup.py)) for the full list of bundled files.

## Installation

To install this file bundle run the following command and provide `git+https://gitlab.com/meltano/files-superset.git` for the `pip_url`:


```bash
meltano add files --custom superset
```

Then in order to call the docker-compose files properly you must add a custom utility to the meltano.yml manually. This sets the ui command needed to start the containers.

```yml
plugins:
  utilities:
  - name: superset
    namespace: superset
    commands:
      up:
        executable: /usr/local/bin/docker
        args: compose -f analyze/superset/docker-compose.yml up -d
      down:
        executable: /usr/local/bin/docker
        args: compose -f analyze/superset/docker-compose.yml down
      ui:
        executable: /usr/local/bin/docker
        args: compose -f analyze/superset/docker-compose.yml up
      export:
        executable: python
        args: analyze/superset/export.py
      import:
        executable: python
        args: analyze/superset/import.py
      compile_datasources:
        executable: python
        args: analyze/superset/compile_datasources.py
    settings:
      - name: tables
        kind: array
      - name: load_all_dbt_models
        kind: boolean
        value: false
    config:
      tables:
      - model.my_meltano_project.table_name_x
environments:
  - name: dev
    env:
      SUPERSET_API_URL: http://localhost:8088
      SUPERSET_USER: admin
      SUPERSET_PASS: admin
```

If you're datasource is not included in Superset out of the box then you need to install it in the `requirements-local.txt` for it to be avaiable. See [available database drivers](https://superset.apache.org/docs/databases/installing-database-drivers) and [installation instructions](https://superset.apache.org/docs/databases/dockeradddrivers).

Add execution permission on the script files that were installed so that docker can use them on startup: 

`chmod +x analyze/superset/docker/*.sh`

If you'd like to sync your dbt tables to Superset, first run a dbt compile, then run the `compile_datasources` command before turning Superset on. Then turn on Superset and navigate to http://localhost:8088/. The default Superset username and password are both `admin`.


```bash
meltano --environment=dev invoke dbt:compile
meltano --environment=dev invoke superset:compile_datasources
meltano --environment=dev invoke superset:ui
```

The other available commands are:

* `meltano --environment=dev invoke superset:up` - Starts all required docker containers in the background using the docker-compose.yml.

* `meltano --environment=dev invoke superset:down` - Stops all docker containers defined in the docker-compose.yml. This includes the `-v` argument which destroys all volumes so any assets in the local instance of Superset will be destroyed. If you want stop Superset but still preserve your assets you can either remove this `-v` argument or use the following export/import workflow.

* `meltano --environment=dev invoke superset:export` - Runs the export.py script that uses the API to export all dashboards and charts from Superset to the `superset/assets` directory.

* `meltano --environment=dev invoke superset:import` - Runs the import.py script that uses the API to import all the dashboards and charts in the `superset/assets` directory into Superset. Currently databases are excluded from importing so you will need to manually add them prior to importing.

* `meltano --environment=dev invoke superset:compile_datasources` - Uses the dbt manifest.json file to generate a Superset compliant datasource.yml which is then imported on startup.

## Notes and Warnings

A caveat with the export/import commands are that you currently need to open up imported databases in the Superset UI and define a password as it will be masked during the export process.

A few configurations that come default with Superset have been adjusted to support the API import/export workflow:

1. The `WTF_CSRF_ENABLED` is set to false since the import API has bugs that dont allow a valid CSRF token to be used right now. This configuration should be carefully considered in a production environment.
