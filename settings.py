from environment import read_env, env_var

read_env()

CLOCKWORK_API_KEY = env_var('CLOCKWORK_API_KEY', '')

LICENCE_NUMBER = env_var('LICENCE_NUMBER', '')
TEST_REF = env_var('TEST_REF', '')

APP_NAME = 'Booker T'
PHONE_NUMBER = env_var('PHONE_NUMBER', '')

# Time interval before checking for earlier dates again
MIN_SECONDS = env_var('MIN_SECONDS', 300)
MAX_SECONDS = env_var('MAX_SECONDS', 1200)
