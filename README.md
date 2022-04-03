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
        executable: /bin/bash
        args: analyze/superset/start_ui.sh
      export_dashboards:
        executable: /bin/bash
        args: analyze/superset/export_dashboards.sh
      import_dashboards:
        executable: /bin/bash
        args: analyze/superset/import_dashboards.sh
      load_datasources:
        executable: /bin/bash
        args: analyze/superset/load_datasources.sh
    settings:
          - name: tables
            description: An array of table names to import into Supserset. They must be in dbt format e.g. `model.my_meltano_project.customers`.
            kind: array
          - name: load_all_dbt_models
            description: A boolean whether to import all known models from dbt or not. If not, use the `tables` array to select by name.
            kind: boolean
            value: false
          - name: sqlalchemy_uri
            description: The full SQLAlchemy uri for your database engine.
              Make sure additional dependencies are installed to use the particular engine.
          - name: database_name
            description: The alias for your database once imported into Superset.
          - name: additional_dependencies
            kind: array
            description: An array of python dependencies to include as part of startup.
              A list of database driver dependencies can be found here https://superset.apache.org/docs/databases/installing-database-drivers
    config:
      database_name: my_postgres
      sqlalchemy_uri: postgresql+psycopg2://${PG_USERNAME}:${PG_PASSWORD}@host.docker.internal:${PG_PORT}/${PG_DATABASE}
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

If you'd like to sync your dbt tables to Superset, first run a dbt compile, then use the `ui` command to turn Superset on.
Use the settings in the example meltano.yml entry to configure what tables to sync into Superset.
If you change these settings or update your dbt models, just run the `load_datasources` command to refresh Superset.

```bash
meltano --environment=dev invoke dbt:compile
meltano --environment=dev invoke superset:ui
```

Once Superset is on, navigate to http://localhost:8088/. The default Superset username and password are both `admin`.

The other available commands are:

* `meltano --environment=dev invoke superset:up` - Starts all required docker containers in the background using the docker-compose.yml.

* `meltano --environment=dev invoke superset:down` - Stops all docker containers defined in the docker-compose.yml. This includes the `-v` argument which destroys all volumes so any assets in the local instance of Superset will be destroyed. If you want stop Superset but still preserve your assets you can either remove this `-v` argument or use the following export/import workflow.

* `meltano --environment=dev invoke superset:export_dashboards` - Runs the export_dashboards.sh script that uses the CLI to export all dashboards from Superset to the `superset/assets/dashboard` directory.

* `meltano --environment=dev invoke superset:import_dashboards` - Runs the import_dashboards.sh script that uses the CLI to import the dashboard definitions in the `superset/assets/dashboard` directory into Superset.

* `meltano --environment=dev invoke superset:load_datasources` - Uses the dbt manifest.json file to generate a Superset compliant datasource.yml which is then imported via the CLI.

## Notes and Warnings

A caveat with the export/import commands are that you currently need to open up imported databases in the Superset UI and re-save them because the passwords dont seem to be initialized properly when imported using the CLI.
