import uuid
import datetime

class Asset(object):
    ''' Model of asset, stored in DynamoDB.
        Stores metadata, links for its screenshot and asset file
    '''
    def __init__(self, id = str(uuid.uuid1()), name = None, author = None, area = None, version = 1,
                 tags = None, asset_path = None, screenshot_path = None):
        #super().__init__()

        self.id = id
        self.name = name
        self.version = version
        self.author = author
        self.tags = tags
        self.asset_path = asset_path
        self.screenshot_path = screenshot_path

        self.last_updated = datetime.datetime.utcnow().isoformat()
