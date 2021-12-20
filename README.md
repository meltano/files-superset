# files-superset

Meltano project [file bundle](https://meltano.com/docs/command-line-interface.html#file-bundle) for [Superset](https://superset.apache.org/).

Files:
- [`analyze/docker-compose-non-dev.yml`](./bundle/analyze/docker-compose-non-dev.yml) 
- [`analyze/docker/*.sh`](./bundle/analyze/docker/) All the scripts used by docker-compose
- [`analyze/docker/requirments-local.txt`](./bundle/analyze/docker/requirments-local.txt) A python requirements file for extra dependencies needed.


See [setup.py](./setup.py)) for the full list of bundled files.

## Installation

Automated installation is not yet available.

To manually install, first add the below or append to the `files:` section of your `meltano.yml` file

```yml
  files:
  - name: superset
    namespace: superset
    pip_url: git+https://github.com/pnadolny13/files-superset.git
    commands:
      # meltano invoke superset:ui
      ui:
        executable: /usr/local/bin/docker
        args: compose -f analyze/superset/docker-compose-non-dev.yml up
```

Next, run `meltano install files superset`.

If you're data source is not included in Superset out of the box then you need to install it in the `requirements-local.txt` for it to be avaiable. See [available database drivers](https://superset.apache.org/docs/databases/installing-database-drivers) and [installation instructions](https://superset.apache.org/docs/databases/dockeradddrivers).

Lastly, invoke via `meltano invoke superset:ui`
