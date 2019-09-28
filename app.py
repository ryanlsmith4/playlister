from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

# playlists = [
#   { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#   { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' },
#   { 'title': 'Cool people', 'description': 'Dancing and dancing!'}
# ]

@app.route('/')
def playlists_index():
  """Show all playlist"""
  return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlists_new():
  """Create Playlists"""
  return render_template('playlists_new.html')

@app.route('/playlists', methods=['POST'])
def playlists_submit():
  playlist = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
    'videos': request.form.get('videos').split(),
    'drop':request.form.get('drop')
  }
  playlist_id = playlists.insert_one(playlist).inserted_id
  print(playlist_id)
  return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)

if __name__ == '__main__':
  app.run(debug=True)