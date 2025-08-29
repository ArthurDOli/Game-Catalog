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
        print(f'Erro ao buscar os jogos populares: {e}')
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
        print(f'Erro ao buscar os detalhes do jogo: {e}')
        return redirect(url_for('homepage'))