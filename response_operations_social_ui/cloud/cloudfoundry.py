import cfenv


class ONSCloudFoundry(object):
    def __init__(self, redis_name):
        self.cf_env = cfenv.AppEnv()
        self.redis_name = redis_name
        self._redis = None

    @property
    def detected(self):
        return self.cf_env.app

    @property
    def redis(self):
        self._redis = self._redis or self.cf_env.get_service(name=self.redis_name)
        return self._redis
