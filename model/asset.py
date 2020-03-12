import uuid
import datetime

class Asset(object):
    ''' Model of asset, stored in DynamoDB.
        Stores metadata, links for its screenshot and asset file
    '''
    def __init__(self, id = None, name = None, author = None, area = None, version = 1,
                 tags = None, asset_path = None, screenshot_path = None):
        #super().__init__()
        if id is None:
            id = str(uuid.uuid1())

        self.id = id
        self.name = name
        self.version = version
        self.author = author
        self.tags = tags.split(',')
        self.asset_path = asset_path
        self.screenshot_path = screenshot_path

        self.last_updated = datetime.datetime.utcnow().isoformat()

    def to_dict(self):
        ''' Json representation of Asset - for API access '''
        data = {
            'id'                : self.id,
            'name'              : self.name,
            'version'           : self.version,
            'author'            : self.author,
            'tags'              : self.tags,
            'asset_path'        : self.asset_path,
            'screenshot_path'   : self.screenshot_path,
            'last_updated'      : self.last_updated
        }

        return data