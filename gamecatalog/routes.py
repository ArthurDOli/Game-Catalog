from flask import render_template, url_for, request, redirect, jsonify
from gamecatalog import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.rawg.io/api/games'
PLATFORMS_URL = 'https://api.rawg.io/api/platforms'
GENRES_URL = 'https://api.rawg.io/api/genres'
DEVELOPERS_URL = 'https://api.rawg.io/api/developers'

@app.route('/', methods=['GET'])
def homepage():
    now = datetime.now()
    params = {
        'key': API_KEY,
        'dates': f'{now.strftime("%Y-%m-%d")},2025-12-31',
        'page_size': 6,
    }
    try:
        resposta = requests.get(BASE_URL, params=params)
        resposta.raise_for_status()
        data = resposta.json()
        jogos = data.get('results', [])
        return render_template('homepage.html', jogos=jogos, now=now)
    except requests.exceptions.RequestException as e:
        print(f'Error searching for popular games: {e}')
        return render_template('homepage.html', jogos=[], erro_api="Não foi possível carregar os jogos. Tente novamente mais tarde.")
    
@app.route('/games/<string:game_slug>', methods=['GET', 'POST'])
def game_page(game_slug):
    url = f"{BASE_URL}/{game_slug}"
    params = {
        'key': API_KEY,
    }
    try:
        resposta = requests.get(url, params=params)
        resposta.raise_for_status()
        jogo_detalhes = resposta.json()
        return render_template('game_page.html', jogo=jogo_detalhes)
    except requests.exceptions.RequestException as e:
        print(f'Error fetching the details of the game: {e}')
        return redirect(url_for('homepage'))
    
@app.route('/tags/platforms/<string:platform_id>', methods=['GET'])
def platforms(platform_id):
    params = {
        'key': API_KEY,
        'platforms': platform_id,
        'page_size': 10,
    }
    try:
        resposta = requests.get(BASE_URL, params=params)
        resposta.raise_for_status()
        jogos = resposta.json().get('results', [])

        platform_url = f'{PLATFORMS_URL}/{platform_id}'
        platform_resposta = requests.get(platform_url, params={'key': API_KEY})
        platform_resposta.raise_for_status()
        platform_detalhes = platform_resposta.json()
        platform_name = platform_detalhes.get('name', 'Plataforma')
        return render_template('platforms.html', jogos=jogos, platform_name=platform_name)
    except requests.exceptions.RequestException as e:
        print(f'Error searching for games on the platform: {e}')
        return redirect(url_for('homepage'))
    
@app.route('/tags/genre/<string:genre_id>', methods=['GET'])
def genre(genre_id):
    params = {
        'key': API_KEY,
        'genres': genre_id,
        'page_size': 10,
    }
    try:
        resposta = requests.get(BASE_URL, params=params)
        resposta.raise_for_status()
        jogos = resposta.json().get('results', [])

        genres_url = f'{GENRES_URL}/{genre_id}'
        genres_resposta = requests.get(genres_url, params={'key': API_KEY})
        genres_resposta.raise_for_status()
        genres_detalhes = genres_resposta.json()
        genres_name = genres_detalhes.get('name', 'Genre')
        return render_template('genres.html', jogos=jogos, genres_name=genres_name)
    except requests.exceptions.RequestException as e:
        print(f"Error searching for games of the genre: {e}")
        return redirect(url_for('homepage'))
    
@app.route('/tags/creators/<string:developers_id>', methods=['GET'])
def creators(developers_id):
    params = {
        'key': API_KEY,
        'developers': developers_id,
        'page_size': 10,
    }
    try:
        resposta = requests.get(BASE_URL, params=params)
        resposta.raise_for_status()
        jogos = resposta.json().get('results', [])

        developers_url = f'{DEVELOPERS_URL}/{developers_id}'
        developers_resposta = requests.get(developers_url, params={'key': API_KEY})
        developers_resposta.raise_for_status()
        developers_detalhes = developers_resposta.json()
        developers_name = developers_detalhes.get('name', 'Developers')
        return render_template('creators.html', jogos=jogos, developers_name=developers_name)
    except requests.exceptions.RequestException as e:
        print(f'Error seaching for games of the genre: {e}')
        return redirect(url_for('homepage'))