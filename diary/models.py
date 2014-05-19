from google.appengine.ext import db
    
class Diary(db.Model):
    author = db.StringProperty()
    weather = db.StringProperty()
    date = db.StringProperty()
    content = db.StringProperty(multiline=True)
    
    @classmethod
    def get_key_from_name(cls, diary_owner=None):
        return db.Key.from_path('Diary', diary_owner or 'anonymous')