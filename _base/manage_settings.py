import os
from decouple import Config, RepositoryEnv

# We check that what is the environment: development, production, test, ...
ENVIRONMENT = os.environ.get("ENV", "development").lower()
# TODO: We can add other environments such as staging and production here later.
if ENVIRONMENT == "development":
    env_file = "config/development.env"

config = Config(RepositoryEnv(env_file))
