import praw
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

auth_token = "EVERNOTE_TOKEN"
if auth_token == "EVERNOTE_TOKEN":
    print("Please fill in your developer token")
    print("To get a developer token, visit " \
          "https://sandbox.evernote.com/api/DeveloperToken.action")
    exit(1)
user_agent = ("Reddit Evernote Saver 0.1 by Sapping"
                "github.com/sapping/reddit-evernote-saver")
r = praw.Reddit(user_agent=user_agent)
user_name = "REDDIT_USER"
user = r.get_redditor(user_name)
comment_limit = 10
gen = user.get_comments(limit=comment_limit)
reddit_comments = []

for comment in gen:
    comment_data=[comment.id, comment.link_title, comment.body, comment.subreddit, comment.link_url]
    reddit_comments.append(comment_data)
    print(comment_data)

# Authenticate Evernote server
client = EvernoteClient(token=auth_token, sandbox=True)

user_store = client.get_user_store()
note_store = client.get_note_store()

# Create a new note
note = Types.Note()
note.title = str(user_name+"'s comment in "+reddit_comments[0][1])
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM ' \
                '"http://xml.evernote.com/pub/enml2.dtd">'
note.content += "<en-note>"
note.content += reddit_comments[0][2]
note.content += "</en-note>"
note_store.createNote(note)