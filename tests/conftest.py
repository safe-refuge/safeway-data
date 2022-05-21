import betamax

from config import PROJECT_PATH


with betamax.Betamax.configure() as config:
    config.cassette_library_dir = f"{PROJECT_PATH}/tests/cassettes/"
