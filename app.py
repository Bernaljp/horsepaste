import os
import random
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

IMAGE_DIR = os.path.join(app.static_folder, 'images')
VALID_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

GAME_STATE = {}
AVAILABLE_IMAGES = []  # pool of images not currently on the board
NO_BOMB = False        # persistent setting: replace black card with neutral


def opposite(team):
    return 'blue' if team == 'red' else 'red'


def make_new_game():
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    all_images = [
        f for f in os.listdir(IMAGE_DIR)
        if os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
    ]

    if len(all_images) < 25:
        raise ValueError(
            f'Need at least 25 images in static/images/ — found {len(all_images)}. '
            'Drop more images there and restart.'
        )

    selected = random.sample(all_images, 25)

    first = random.choice(['red', 'blue'])
    second = opposite(first)
    neutral_count = 8 if NO_BOMB else 7
    bomb = [] if NO_BOMB else ['black']
    colors = [first] * 9 + [second] * 8 + ['neutral'] * neutral_count + bomb
    random.shuffle(colors)

    cards = [
        {'id': i, 'image': selected[i], 'color': colors[i], 'revealed': False}
        for i in range(25)
    ]

    # Rebuild the pool of unused images (mutate in place so global ref stays valid)
    selected_set = set(selected)
    AVAILABLE_IMAGES[:] = [f for f in all_images if f not in selected_set]

    return {
        'cards': cards,
        'current_turn': first,
        'game_over': False,
        'winner': None,
        'red_remaining': 9 if first == 'red' else 8,
        'blue_remaining': 9 if first == 'blue' else 8,
        'no_bomb': NO_BOMB,
    }


try:
    GAME_STATE = make_new_game()
except ValueError as e:
    print(f'WARNING: {e}')
    GAME_STATE = {
        'cards': [],
        'current_turn': 'red',
        'game_over': False,
        'winner': None,
        'red_remaining': 9,
        'blue_remaining': 8,
        'no_bomb': NO_BOMB,
        'error': str(e),
    }


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    emit('state_update', GAME_STATE)


@socketio.on('get_state')
def handle_get_state():
    emit('state_update', GAME_STATE)


@socketio.on('reveal_card')
def handle_reveal(data):
    if GAME_STATE.get('game_over'):
        return

    card_id = data.get('card_id')
    card = next((c for c in GAME_STATE['cards'] if c['id'] == card_id), None)
    if card is None or card['revealed']:
        return

    card['revealed'] = True
    color = card['color']

    if color == 'black':
        GAME_STATE['winner'] = opposite(GAME_STATE['current_turn'])
        GAME_STATE['game_over'] = True

    elif color == 'red':
        GAME_STATE['red_remaining'] -= 1
        if GAME_STATE['red_remaining'] == 0:
            GAME_STATE['winner'] = 'red'
            GAME_STATE['game_over'] = True
        elif GAME_STATE['current_turn'] != 'red':
            GAME_STATE['current_turn'] = 'red'

    elif color == 'blue':
        GAME_STATE['blue_remaining'] -= 1
        if GAME_STATE['blue_remaining'] == 0:
            GAME_STATE['winner'] = 'blue'
            GAME_STATE['game_over'] = True
        elif GAME_STATE['current_turn'] != 'blue':
            GAME_STATE['current_turn'] = 'blue'

    elif color == 'neutral':
        GAME_STATE['current_turn'] = opposite(GAME_STATE['current_turn'])

    socketio.emit('state_update', GAME_STATE)


@socketio.on('end_turn')
def handle_end_turn():
    if GAME_STATE.get('game_over'):
        return
    GAME_STATE['current_turn'] = opposite(GAME_STATE['current_turn'])
    socketio.emit('state_update', GAME_STATE)


@socketio.on('replace_card')
def handle_replace_card(data):
    # Only allowed before any card has been revealed
    if GAME_STATE.get('game_over'):
        return
    if any(c['revealed'] for c in GAME_STATE['cards']):
        return

    card_id = data.get('card_id')
    card = next((c for c in GAME_STATE['cards'] if c['id'] == card_id), None)
    if card is None or card['revealed']:
        return

    if not AVAILABLE_IMAGES:
        emit('error', {'message': 'No more images available to swap in.'})
        return

    new_image = random.choice(AVAILABLE_IMAGES)
    AVAILABLE_IMAGES.remove(new_image)
    AVAILABLE_IMAGES.append(card['image'])  # return old image to pool
    card['image'] = new_image

    socketio.emit('state_update', GAME_STATE)


@socketio.on('toggle_no_bomb')
def handle_toggle_no_bomb():
    global NO_BOMB
    NO_BOMB = not NO_BOMB
    GAME_STATE['no_bomb'] = NO_BOMB
    socketio.emit('state_update', GAME_STATE)


@socketio.on('new_game')
def handle_new_game():
    global GAME_STATE
    try:
        GAME_STATE = make_new_game()
        socketio.emit('state_update', GAME_STATE)
    except ValueError as e:
        emit('error', {'message': str(e)})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
