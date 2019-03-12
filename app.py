from user import Handle
from data_collection_service import DataCollectionService



def aggregage_user_data(user: str):
    target_user = Handle(user)
    dc = DataCollectionService()

    targets_followers = dc.get_users_followers(target_user.username, 5)
    all_row = [dc.get_aggregate_timeline_text(follower) for follower in targets_followers]
    print(all_row)






user = "etsu"


