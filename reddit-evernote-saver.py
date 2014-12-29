import praw
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

auth_token = "EVERNOTE_TOKEN"
user_agent = ("Reddit Evernote Saver 0.1 by Sapping"
                "github.com/sapping/reddit-evernote-saver")
r = praw.Reddit(user_agent=user_agent)
user_name = "REDDIT_USERNAME"
user = r.get_redditor(user_name)
comment_limit = 10
gen = user.get_comments(limit=comment_limit)

reddit_comments =[]
for comment in gen:
    reddit_comments.append(comment.body)
