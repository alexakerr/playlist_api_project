from flask import Flask, jsonify, request

app = Flask(__name__)

playlists = { }

@app.route('/playlist/create', methods=['POST'])
def create_playlist():
    data = request.json
    playlist_name = data.get('name')
    playlist_description = data.get('description')
    playlist_id = str(len(playlists) + 1)
    new_playlist = {'name': playlist_name, 'description': playlist_description, 'songs': []}
    playlists[playlist_id] = new_playlist
    return jsonify({'playlist_id': playlist_id})


@app.route('/playlist/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    playlist = playlists.get(playlist_id)
    if playlist:
        return jsonify(playlist)
    else:
        return jsonify({'error': 'Playlist does not exist.'}), 404


@app.route('/playlist/update/<playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    playlist = playlists.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist does not exist.'}), 404
    data = request.json
    playlist.update({
        'name': data.get('name', playlist.get('name')),
        'description': data.get('description', playlist.get('description'))
    })
    return jsonify({'message': 'Playlist updated'}), 200


@app.route('/playlist/delete/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    if playlist_id in playlists:
        del playlists[playlist_id]
        return jsonify({'message': 'Playlist deleted'}), 200
    else:
        return jsonify({'error': 'Playlist does not exist.'}), 404
    

@app.route('/playlist/<playlist_id>/add_song', methods=['POST'])
def add_song_to_playlist(playlist_id):
    playlist = playlists.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist does not exist'}), 404
    data = request.get_json()
    song_title = data.get('title')
    song_artist = data.get('artist')
    songs = playlist.setdefault('songs', [])
    songs.append({'title': song_title, 'artist': song_artist})
    return jsonify({'message': 'Song has been added to playlist'}), 200
    

@app.route('/playlist/<playlist_id>/remove_song/<int:song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist = playlists.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist does not exist'}), 404
    songs = playlist.get('songs')
    if not songs:
        return jsonify({'error': 'Playlist does not have any songs'}), 404
    if song_id >= len(songs):
        return jsonify({'error': 'Song does not exist in playlist'}), 404
    del songs[song_id]
    return jsonify({'message': 'Song has been removed from playlist'}), 200
    

@app.route('/playlist/search_song', methods=['GET'])
def search_song():
    song_artist = request.args.get('artist')
    result = []
    for playlist_id, playlist in playlists.items():
        if 'songs' in playlist:
            for song in playlist['songs']:
                if song['artist'] == song_artist:
                    result.append({'playlist_id': playlist_id, 'song': song})
    return jsonify(result)







if __name__ == '__main__':
    app.run(debug=True)
