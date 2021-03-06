
import praw
import time
import configparser
import handlers
from database_handler import DatabaseHandler


# ==========================
# Global variables
# ==========================

#This will be included in the database when it's implemented.
database = DatabaseHandler()

def initiate_bot():
    '''
    Initiates the bot by retrieving settings from the config file.
    :returns The reddit object
    '''

    config = configparser.ConfigParser()
    config.read('config.cfg')

    #Retrieve the reddit specific information from the config
    user_agent = config.get('Reddit', 'user_agent')
    username = config.get('Reddit', 'username')
    password = config.get('Reddit', 'password')

    #Use the information to login
    reddit = praw.Reddit(user_agent)
    reddit.login(username, password)

    return reddit

def get_comments(reddit):
    '''
    Retrieves all comments from /r/asoiaf. This should be fixed to only retrieve
    the X latest comments.
    :returns All comments from /r/asoiaf
    '''
    subreddit = reddit.get_subreddit('asoiaf')
    return subreddit.get_comments(limit = 200)


def reply_to_comment(comment, handler):
    reply = handler.get_reply()

    reply += '\n_____\n'
    reply += '[^([More information])] (https://github.com/joakimskoog/ASOIAFBot) '
    reply += '[^([Bugs/Feedback])] (https://github.com/joakimskoog/ASOIAFBot/issues)'

    comment.reply(reply)

    print('Commented. ID: ' + comment.id)
    database.set_comment_as_answered(comment.id)

def handle_comment(comment):
    if not database.is_comment_answered(comment.id):
        handler = handlers.factory(comment.body, database)

        if handler != None:
            reply_to_comment(comment, handler)

def handle_comments(comments):
    for comment in comments:
        handle_comment(comment)


def main_loop(reddit):
    while True:
        try:
            comments = get_comments(reddit)
            handle_comments(comments)
        except praw.errors.RateLimitExceeded as error:
            time.sleep(error.sleep_time)
            print('Time to sleep for ' + error.sleep_time + ' seconds')
        except:
            sleep_duration = 30
            time.sleep(sleep_duration)
            print('Generic error: Time to sleep for ' + sleep_duration + ' seconds')
        time.sleep(30)

if __name__ == '__main__':
    reddit = initiate_bot()
    main_loop(reddit)
