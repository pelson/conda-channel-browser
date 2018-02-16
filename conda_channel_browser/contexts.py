from collections import defaultdict
import json
from pathlib import Path


class Channel(object):
    def __init__(self, channel_indexes):
        self.channel_indexes = channel_indexes

    def full_index(self):
        """Blend together all of the indexes into a single index."""
        return dict(*[index.get('packages', {}) for index in self.channel_indexes])

    @property
    def binaries(self):
        return self.full_index()

    @property
    def packages(self):
        packages = defaultdict(list)
        for binary, pkg_info in self.full_index().items():
            pkginfo = pkg_info.copy()
            pkginfo['binary_name'] = binary
            packages[pkg_info['name']].append(pkg_info)
        return packages

    @classmethod
    def from_channel(cls, channel_url):
        channel_data = []
        # Fetch the metadatas
        for stream in ['linux-64', 'osx-64', 'win-64', 'noarch'][:1]:
            # TODO: Use http if necessary...
            full_path = f'{channel_url}/{stream}/repodata.json'
            if full_path.startswith('file://'):
                full_path = Path(full_path[7:])
                if not full_path.exists():
                    raise RuntimeError(f'Path {full_path} does not exist.')
                with full_path.open() as fh:
                    stream_data = json.load(fh)
            else:
                raise RuntimeError('Protocol not yet implemented.')
            channel_data.append(stream_data)
        return cls(channel_data)


class PackageContext(object):
    def __init__(self, channel, package):
        self.channel = channel
        self.package = package
