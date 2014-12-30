import praw
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

auth_token = "EVERNOTE_TOKEN"
if auth_token == "EVERNOTE_TOKEN":
    print("Please fill in your developer token")
    print("To get a developer token, visit " \
          "https://sandbox.evernote.com/api/DeveloperToken.action")
    exit(1)
user_agent = ("Reddit Evernote Saver 0.2 by Sapping"
                "github.com/sapping/reddit-evernote-saver")
r = praw.Reddit(user_agent=user_agent)
user_name = "REDDIT_USERNAME"
if user_name == "REDDIT_USERNAME":
    print("Please fill in a valid reddit username")
    exit(1)
user = r.get_redditor(user_name)
# Fetches only the 10 most recent comments.
comment_limit = 10
gen = user.get_comments(limit=comment_limit)
reddit_comments = []

# Create a list of all notes and their associated data
for comment in gen:
    comment_data=[comment.id, comment.link_title, comment.body, comment.subreddit.display_name, comment.link_url, comment.link_id]
    reddit_comments.append(comment_data)

# Authenticate Evernote server. Sandbox mode is set to True
client = EvernoteClient(token=auth_token, sandbox=True)

user_store = client.get_user_store()
note_store = client.get_note_store()
attributes = Types.NoteAttributes()

tags = []
tags.append(reddit_comments[0][3])
print(tags)

# Create a new note and publish it to Evernote
i = 0
for comments in reddit_comments:
    tags = []
    note = Types.Note()
    attributes.sourceURL = reddit_comments[i][4]
    note.attributes = attributes
    note.title = str(user_name+"'s comment in "+reddit_comments[i][1])
    tags.append(reddit_comments[i][3])
    note.tagNames = tags
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
                    '"http://xml.evernote.com/pub/enml2.dtd">'
    note.content += "<en-note>"
    note.content += "<div>"
    note.content += "<a href="+"\"http://reddit.com/"+reddit_comments[i][5][3:]+"\">"+"Link to reddit comments"+"</a>"
    note.content += "</div>"
    note.content += "<p/>"+reddit_comments[i][2]
    note.content += "</en-note>"
    print(note)
    note_store.createNote(note)
    i += 1