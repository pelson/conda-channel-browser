
class Channel(object):
    def __init__(self, channel_data):
        self.channel_data = channel_data

    @classmethod
    def from_channel(cls, channel_url):
        channel_data = []
        # Fetch the metadatas
        for stream in ['linux-64', '...']:
            stream_data = {}
            channel_data.append(stream_data)
        return channel_data


class PackageContext(object):
    def __init__(self, channel, package):
        self.channel = channel
        self.package = package
