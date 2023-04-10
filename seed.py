from models import User, db, Post
from app import app
import datetime
# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Base Users
whiskey = User(first_name='Whiskey', last_name='Delta' )
bowser = User(first_name='Bowser', last_name='Cline' )
spike = User(first_name='Spike', last_name='Spice' )

# Add Base Dummy Post

dummy_post = Post(title="It's a Dummy", content="I'm a post, and I'm a dummy!", user_id=1)
dummy_post2 = Post(title="It's a Dummy", content="I'm a post, and I'm a dummy!", user_id=2)
dummy_post3 = Post(title="It's a Dummy", content="I'm a post, and I'm a dummy!", user_id=3)

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()

# create / commit post after users are created so that the user_id of 1 is valid upon post creation
db.session.add(dummy_post)
db.session.add(dummy_post2)
db.session.add(dummy_post3)
db.session.commit()