class Config:
    def __init__(
        self,
        clientId, secretClientId, userPoolId, identityPoolId,
        region, accesskey, secretAccessKey
    ):
        self.CLIENT_ID = clientId
        self.CLIENT_SECRET = secretClientId
        self.USER_POOL_ID = userPoolId
        self.IDENTITY_POOL_ID = identityPoolId
        self.REGION = region
        self.ACCESSKEYID = accesskey
        self.SECRETACCESSKEY = secretAccessKey

    CLIENT_ID = None
    CLIENT_SECRET = None
    USER_POOL_ID = None
    IDENTITY_POOL_ID = None
    REGION = None
    ACCESSKEYID = None
    SECRETACCESSKEY = None
