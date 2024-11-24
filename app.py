from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)


def search_song(song_name, artist_name):
    search_url = "http://music.163.com/api/search/get/"

    params = {
        's': f'{song_name} {artist_name}',
        'type': 1,
        'offset': 0,
        'total': 'true',
        'limit': 5
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(search_url, params=params, headers=headers)
        result = json.loads(response.text)

        if 'result' in result and 'songs' in result['result']:
            songs = result['result']['songs']
            results = []

            for song in songs[:5]:
                song_id = song['id']
                music_url = "YOUR_API_HERE"
                results.append({
                    'music_url': music_url,
                    'song_name': song['name'],
                    'artist_name': song['artists'][0]['name'],
                    'album_name': song['album']['name']
                })

            return results

        return []

    except Exception as e:
        print(f"搜索出错: {str(e)}")
        return []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    song_name = data.get('song_name')
    artist_name = data.get('artist_name')

    if not song_name or not artist_name:
        return jsonify({'error': '请提供歌名和歌手名'}), 400

    results = search_song(song_name, artist_name)

    if results:
        return jsonify({
            'results': results
        })
    else:
        return jsonify({'error': '未找到匹配的歌曲'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
