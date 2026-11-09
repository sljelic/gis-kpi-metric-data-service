from importlib import metadata
from pathlib import Path
import os
name = 'gis-kpi-metric-data-service'
dist = metadata.distribution(name)
assert Path(dist.locate_file('')).is_relative_to(Path(os.environ['VIRTUAL_ENV']))
for entry in dist.entry_points:
    if entry.group == 'apache_airflow_provider':
        info = entry.load()()
        assert info['package-name'] == name
        assert info['versions'][0] == dist.version
print('Installed distribution and provider metadata verified')
