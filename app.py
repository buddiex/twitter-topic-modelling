from user import User
from user_service import UserService

user_service = UserService(User("etsu"))

# print(user_service.get_user_timeline())
# out = user_service.get_followers_descriptions(100)
out = user_service.get_user_timeline()
for pp in out:
    print(pp)
