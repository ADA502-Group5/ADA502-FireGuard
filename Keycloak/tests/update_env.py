import os

import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

print(os.environ["token_user1"])
os.environ["token_user1"] = os.getenv('access_token1')
print(os.environ["token_user1"])

print(os.environ["token_user2"])
os.environ["token_user2"] = os.getenv('access_token2')
print(os.environ["token_user2"])

dotenv.set_key(dotenv_file, "token_user1", os.environ["token_user1"])
dotenv.set_key(dotenv_file, "token_user2", os.environ["token_user2"])
