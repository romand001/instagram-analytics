#import matplotlib
import sys, time, json, smtplib
from os import system, name
from InstagramAPI import InstagramAPI

def clear():
    system("cls")

def dumpJson():
    with open('LastJson.txt', 'w') as outfile:
        json.dump(API.LastJson, outfile)

def login():
    global API

    username = input("Username: ")
    password = input("Password: ")

    API = InstagramAPI(username, password)
    clear()
    print("logging in.....")
    API.login()
    clear()
    print("Login successful!")

def optionMenu():

    selection = -1

    while selection not in range(0,7):

        try:
            selection = int(input("Which analysis would you like to perform?\n"
                  "[1] Not following me back\n"
                  "[2] I'm not following back\n"
                  "[3] Who likes my posts the most?\n"
                  "[4] Who blocked me?\n"
                  "[5] Who blocked me? (improved algorithm)\n"
                  "[6] Test option\n"
                  "[0] Close program\n\n"))
        except:
            clear()
            print("That is not a valid option, please ty again.\n\n")
            selection = -1

    clear()

    if selection == 0:
        sys.exit()
    elif selection == 1:
        option1()
    elif selection == 2:
        option2()
    elif selection == 3:
        option3()
    elif selection == 4:
        option4()
    elif selection == 5:
        option5()
    elif selection == 6:
        option6()

    command = input("\nPress Enter to perform another analysis, or type 'exit' to close the program.")

    if command == "exit":
        sys.exit()

def option1():
    global API

    followers = getTotalFollowers(API, API.username_id)
    followings = getTotalFollowings(API, API.username_id)

    followersUsernames = getUsernames(followers)
    followingsUsernames = getUsernames(followings)

    followAnalysis = listCompare(followersUsernames, followingsUsernames)

    print("Not following me back\n"
          "---------------------\n")

    for j in followAnalysis[1]:
        print(j)

    print("\n\n")

    followAnalysisDisplay = followAnalysis[1]

    i = 0
    for user in followAnalysis[1]:

        clear()
        for i in followAnalysisDisplay:
            print(i)

        print("\n\n")

        checkFollowStatus(followAnalysis[3][i])

        command = input(user.ljust(40) + "Unfollow? (y/n)   ")

        pk = followAnalysis[3][i]

        while checkFollowStatus(pk):

            if command == "y":
                API.unfollow(pk)

            if checkFollowStatus(pk):
                command = input("Could not unfollow %s. Try again in a few minutes? (y/n)   " %user)

            else:
                followAnalysisDisplay[i] = followAnalysisDisplay[i].ljust(40) + "unfollowed"

        i += 1




        '''
        idiots = []
        API.getUsernameInfo(pk)

        while API.LastJson["status"] == "fail":
            print("Instagram request limit reached, trying again in three minute.")
            time.sleep(180)
            API.getUsernameInfo(pk)

        try:
            user = API.LastJson["user"]

            if user["follower_count"] / user["following_count"] < 6 or user["follower_count"] < 1000:
                idiots.append((user["username"], user["pk"]))
                print(user["username"].ljust(40) + "unfollow")
            else:
                print(user["username"].ljust(40) + "keep")

        except:
            pass

        

    command1 = input("Would you like to unfollow accounts with 6:1 ratio or lower? (y/n)")


    if command1 == "y":

        if len(idiots) > 50:
            command2 = input("Instagram only allows 50 unfollows per hour, but you"
                             "are trying to unfollow %s. How would you like to proceed?\n"
                             %len(idiots) +
                             "[1] Unfollow first 50\n"
                             "[2] Unfollow 50 now, then automatically repeat every hour\n"
                             "[3] Cancel unfollow\n")
            if command2 == 1:
                for user in idiots[0:50]:
                    API.unfollow(user[1])
                    idiots.pop(idiots.index(user))

            elif command2 == 2:

                while len(idiots) > 50:

                    for user in idiots[0:50]:
                        API.unfollow(user[1])
                        idiots.pop(idiots.index(user))

                    secondsRemaining = 3600

                    while secondsRemaining != 0:
                        time.sleep(1)
                        secondsRemaining -= 1
                        clear()
                        print(str(secondsRemaining/60) + " minutes remaining")


        for user in idiots:
            API.unfollow(user[1])
            idiots.pop(idiots.index(user))

        '''

def option2():
    global API

    followers = getTotalFollowers(API, API.username_id)
    followings = getTotalFollowings(API, API.username_id)

    followersUsernames = getUsernames(followers)
    followingsUsernames = getUsernames(followings)

    followAnalysis = listCompare(followersUsernames, followingsUsernames)

    print("I'm not following back\n"
          "---------------------\n")

    for j in followAnalysis[0]:
        print(j)

def option3():
    API.getUserFeed(API.username_id)

    media = getMediaInfo()

    likers = {}

    for i in range(0, len(media)):
        API.getMediaLikers(media[i][1])

        for liker in API.LastJson["users"]:
            if liker["username"] in likers:
                likers[liker["username"]] += 1
            else:
                likers[liker["username"]] = 1

    for follower in getTotalFollowers(API, API.username_id):
        if follower["username"] not in likers:
            likers[follower["username"]] = 0


    #dumpJson()

    likersList = []

    for i in likers:
        likersList.append((i, likers[i]))

    likersList = sorted(likersList, key=lambda x: x[1])

    for liker in likersList:

        print(liker[0].ljust(25) + str(liker[1]))

def option4():

    trackerPK = 12389194238
    nadaPK = 201683479

    trackerUsername = "i.tracker2"
    trackerPassword = "asshole"

    API.getUsernameInfo(trackerPK)
    #dumpJson()

    trackerAPI = InstagramAPI(trackerUsername, trackerPassword)

    trackerAPI.login()
    clear()

    '''
    GET MEDIA LIKERS
    '''
    print("Building userbase of possible blockers...")

    API.getUserFeed(API.username_id)

    media = getMediaInfo()

    likers = {}

    for i in range(0, len(media)):
        API.getMediaLikers(media[i][1])

        for liker in API.LastJson["users"]:
            if liker["pk"] in likers:
                likers[liker["pk"]] += 1
            else:
                likers[liker["pk"]] = 1

    for follower in getTotalFollowers(API, API.username_id):
        if follower["pk"] not in likers:
            likers[follower["pk"]] = 0

    # dumpJson()

    likersList = []

    for i in likers:
        likersList.append((i, likers[i]))

    likersList = sorted(likersList, key=lambda x: x[1])

    topLikers = []

    accuracy = input("Choose an accuracy level from 1 to 10: ")

    for liker in likersList[0:(int(accuracy) * 5)]:

        topLikers.append(liker[0])


    '''
    BUILDING USERBASE
    '''

    userBase = []

    for liker in topLikers:
        trackerAPI.getUserFollowers(liker)
        #dumpJson()

        for user in getUsernames(trackerAPI.LastJson["users"]):
            userBase.append(user)

    userBase = list(set(userBase))
    userBaseSize = len(userBase)

    '''
    CHECKING BLOCK
    '''

    print("Testing %s accounts for block status..." %userBaseSize)

    blockers = []

    counter = 0

    for user in userBase:

        counter += 1

        if counter % 24 == 0:
            clear()
            print("Progress: " + str(int((counter / userBaseSize) * 100)) + "%\n" +
                  "Found so far:\n"
                  "-------------")
            for blocker in blockers:
                print(blocker[0])

        '''
        
        if not API.getUsernameInfo(user[1]):

            if API.LastJson["status"] == "fail":
                print("timeout, waiting 5 min...")
                time.sleep(300)

            else:
                blockers.append(user)
                print("added blocker: " + user[0])
        
        '''

        if counter % 90 == 0:
            time.sleep(360)

        if not API.getUsernameInfo(user[1]):
            if API.LastJson["status"] == "fail":
                time.sleep(360)
            blockers.append(user[0])

    '''
    DISPLAYING OUTCOME
    '''
    print("The following users are blocking you.\n"
          "This list may be incomplete:")
    for blocker in blockers:
        print(blocker[0])

def option5():

    '''
    ACCURACY SETTINGS
    '''

    accuracy = int(input("Select an accuracy from 1 to 10: "))

    commentcompareposts = accuracy * 3
    numTopLikers = accuracy * 5

    '''
    LOGGING IN TRACKER
    '''
    clear()
    print("Logging in tracker...")

    trackerPK = 12389194238
    nadaPK = 201683479

    trackerUsername = "i.tracker2"
    trackerPassword = "asshole"

    API.getUsernameInfo(trackerPK)

    trackerAPI = InstagramAPI(trackerUsername, trackerPassword)

    trackerAPI.login()
    clear()

    '''
    GETTING PUBLIC FOLLOWERS AND FOLLOWINGS
    '''
    clear()
    print("getting public followers and followings...")

    followers = getTotalFollowers(API, API.username_id)
    followings = getTotalFollowings(API, API.username_id)


    userBase1 = followers
    for user in followings:
        if user not in followers:
            userBase1.append(user)

    userBase2 = []
    for user in userBase1:
        if not user["is_private"]:
            userBase2.append(user)


    '''
    GETTING MEDIA IDs
    '''

    print("getting media IDs...")
    time.sleep(1)

    media_ids = []

    for user in userBase2:

        API.getUsernameInfo(user["pk"])

        try:
            num_posts = API.LastJson["user"]["media_count"]
        except KeyError:
            num_posts = 61
            print("timeout, waiting 6 mins")
            time.sleep(360)
            API.getUsernameInfo(user["pk"])

        if num_posts < 120 and API.LastJson["user"]["follower_count"] < 10000:

            clear()
            print(API.LastJson["user"]["username"] + " (%s/%s)"%(str(userBase2.index(user)), str(len(userBase2))) +
                  "    num media ids: " + str(len(media_ids)))


            API.getTotalUserFeed(user["pk"], timeout = 10)

            for item in API.LastJson["items"][0: commentcompareposts]:
                media_ids.append(item["id"])

    media_ids = list(set(media_ids))

    '''
    GETTING COMMENTERS
    '''

    seenCommenters = []
    trackerCommenters = []

    for media in media_ids:

        seenCommenters = list(set(seenCommenters + getCommenterUsernames(getAllComments(API, media))))
        trackerCommenters = list(set(trackerCommenters + getCommenterUsernames(getAllComments(trackerAPI, media))))

        dumpJson()

        clear()
        print("Fetching comments for post %s/%s"%(media_ids.index(media), len(media_ids)) +
              "\ncommenters gathered: %s"%len(trackerCommenters))

    '''
    CHECKING FOR BLOCKERS
    '''

    clear()
    print("Checking for blockers...")

    blockers = listCompare(seenCommenters, trackerCommenters)[1]

    clear()
    print("List of blockers so far:\n"
          "-----------------")
    for blocker in blockers:
        print(blocker)

    #command = input("\nPress enter to continue analysis: ")

    '''
    GETTING MEDIA LIKERS
    '''

    clear()
    print("Building second userbase of possible blockers...")

    API.getUserFeed(API.username_id)

    media = getMediaInfo()

    likers = {}

    for i in range(0, len(media)):
        API.getMediaLikers(media[i][1])

        for liker in API.LastJson["users"]:
            if liker["pk"] in likers:
                likers[liker["pk"]] += 1
            else:
                likers[liker["pk"]] = 1

    for follower in getTotalFollowers(API, API.username_id):
        if follower["pk"] not in likers:
            likers[follower["pk"]] = 0


    likersList = []

    for i in likers:
        likersList.append((i, likers[i]))

    likersList = sorted(likersList, key=lambda x: x[1])

    topLikers = []

    for liker in likersList[0:numTopLikers]:
        topLikers.append(liker[0])

    '''
    BUILDING SECOND USERBASE
    '''

    userBase3 = []

    for liker in topLikers:
        trackerAPI.getUserFollowers(liker)

        for user in getUsernames(trackerAPI.LastJson["users"]):
            if not user in trackerCommenters:
                userBase3.append(user)

    userBase3 = list(set(userBase3))
    userBase3Size = len(userBase3)

    '''
    CHECKING BLOCK
    '''

    print("Testing %s accounts for block status..." % userBase3Size)

    counter = 0

    for user in userBase3:

        counter += 1


        clear()
        print("Checking user %s/%s\n"%(counter, len(userBase3)) +
              "Found so far:\n" +
              "-------------")
        for blocker in blockers:
            print(blocker[0])


        if counter % 90 == 0:
            time.sleep(360)

        if not API.getUsernameInfo(user[1]):
            if API.LastJson["status"] == "fail":
                time.sleep(360)
            blockers.append(user[0])

    '''
    DISPLAYING OUTCOME
    '''
    print("The following users are blocking you.\n"
          "This list may be incomplete:")
    for blocker in blockers:
        print(blocker[0])

    gmail_user = 'darieroman10@gmail.com'
    gmail_password = 'Cupcake1@'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, [gmail_user], str(blockers))
        server.close()
    except:
        print('Something went wrong...')


def option6():

    exampleIDs = [
        "2041006699620658727_264500029",
        "2038659093078925734_264500029",
        "2023621173888616165_264500029",
        "2012789483616313244_264500029",
        "1988275827959233493_264500029",
        "1971457909452995345_264500029"
    ]

    print(getAllComments(API, exampleIDs[0]))

def getMediaInfo():
    API.getUserFeed(API.username_id)

    media = []

    for post in API.LastJson["items"]:
        media.append((
            post["device_timestamp"],
            post["id"]
        ))

    media = sorted(media, key=lambda x: x[0])

    return media

def getAllComments(api, mediaId):

    count = 100

    has_more_comments = True
    max_id = ''
    comments = []

    while has_more_comments:

        _ = api.getMediaComments(mediaId, max_id=max_id)


        try:

            for c in reversed(api.LastJson['comments']):
                comments.append(c)

            has_more_comments = api.LastJson.get('has_more_comments', False)

            if count and len(comments) >= count:
                comments = comments[:count]
                has_more_comments = False

            if has_more_comments:
                max_id = api.LastJson.get('next_max_id', '')
                time.sleep(2)

        except KeyError:

            try:
                if api.LastJson["comments_disabled"]:
                    has_more_comments = False
                    break

            except KeyError:

                dumpJson()
                print("timeout, waiting 6 mins...")
                time.sleep(360)
                has_more_comments = False


    return comments

def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

def getTotalFollowings(api, user_id):
    """
    Returns the list of followings of the user.
    It should be equivalent of calling api.getTotalFollowings from InstagramAPI
    """

    followings = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followings.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followings

def checkFollowStatus(pk):
    API.userFriendship(pk)

    return API.LastJson["following"]

def getUsernames(userList):

    usernameList = []

    for user in userList:
        usernameList.append((
            user['username'],
            user['pk']
        ))

    return usernameList

def getCommenterUsernames(comments):

    commenters = []

    for comment in comments:
        commenters.append((comment["user"]["username"],
                          comment["user"]["pk"]))

    return commenters

def listCompare(list1, list2):

    ex1 = []
    ex2 = []
    ex1pk = []
    ex2pk = []

    for i in list1:
        if i not in list2:
            ex1.append(i[0])
            ex1pk.append(i[1])

    for j in list2:
        if j not in list1:
            ex2.append(j[0])
            ex2pk.append(j[1])

    return ex1, ex2, ex1pk, ex2pk

def startProgram():
    global API

    clear()

    print("Welcome to Instagram Analytics.\n"
          "To begin, enter your username and password.\n")

    time.sleep(1.5)

    login()

    time.sleep(1)

    while True:
        optionMenu()


startProgram()

