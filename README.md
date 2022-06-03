# files-superset

Meltano project [file bundle](https://docs.meltano.com/concepts/plugins#file-bundles) for [Superset](https://superset.apache.org/).

Files:
- [`analyze/superset/superset_config.py`](./bundle/analyze/superset/superset_config.py)
- [`analyze/superset/superset-init.sh`](./bundle/analyze/superset/superset-init.sh)

```py
# Add Superset utility and this file bundle to your Meltano project
meltano add utility superset

# Add only this file bundle to your Meltano project
meltano add files superset
```

Checkout Superset on [MeltanoHub](https://hub.meltano.com/utilities/superset) for more details on usage and configurations.
