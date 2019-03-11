from user import User
from user_service import UserService

user_service = UserService(User("omigie"))

# print(user_service.get_user_timeline())
for user_description in user_service.get_followers_descriptions(100):
    print(user_description)
