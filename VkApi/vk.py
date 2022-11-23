import vk_api
from config import token 

session = vk_api.VkApi(token=token)
vk = session.get_api()

def GetUserNameById(userId):
    user = vk.users.get(user_ids = userId)
    return f"{user[0]['first_name']} {user[0]['last_name']}"

def GetFriendsByGroup(ownerId):
    friendsLists = vk.friends.getLists(user_id = ownerId)
    print()
    for fGroup in friendsLists['items']:
        friends = vk.friends.get(user_id = ownerId, list_id = fGroup['id'])
        friendsInString = ""
        for friend in friends['items']:
            if friend != friends['items'][- 1]:
                friendsInString += f"{GetUserNameById(friend)}, " 
            else:
                friendsInString += f"{GetUserNameById(friend)}." 
        print(f"{fGroup['name']}: {friendsInString}\n")

def GetAllFriends(ownerId):
    friends = vk.friends.get(user_id = ownerId, count = 50)
    print("Все друзья: ")
    for friend in friends['items']:
        print(GetUserNameById(friend)) 

def CreatePost(ownerId):
    vk.wall.post(owner_id = ownerId, friends_only = 1, message = "Я новый пост)", close_comments = 1, attachments = "photo156214810_457243367" )

def GetInfo(ownerId):
    print(f"\n{GetUserNameById(1)}\n")
    CreatePost(ownerId)
    GetFriendsByGroup(ownerId)
    GetAllFriends(ownerId)
