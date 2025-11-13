import json
import os
from pathlib import Path
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit

# --- Disable Caching ---
# This is critical for OBS. It forces the browser to always load the newest file.
class MyFlask(Flask):
    def get_send_file_max_age(self, name):
        if name.lower().endswith('.html'):
            return 0  # Set cache to 0 seconds for HTML files
        return super(MyFlask, self).get_send_file_max_age(name)

app = MyFlask(__name__, static_folder='.', template_folder='.') # Serve static files from current directory
app.config['SECRET_KEY'] = 'your_secret_key_here' # Not super important for local use
socketio = SocketIO(app)

# --- Default Data ---
# This is the data that will be loaded if no data is saved yet.
default_data = {
    "player": {
        "name": "Player Name",
        "team": "Team Name",
        "pfp_url": "https://placehold.co/100x100/1c1c1c/f8f8f8?text=PFP",
        "squad_icon_url": "",
        "op_icon_url": "",
        "pos": {"x": 50, "y": 50},
        "scale": {"x": 1, "y": 1},
        "visible": True
    },
    "text_left": {
        "text": "Left Editable Text",
        "pos": {"x": 50, "y": 950},
        "scale": {"x": 1, "y": 1},
        "fontSize": 24,
        "visible": True
    },
    "text_right": {
        "text": "Right Editable Text",
        "pos": {"x": 1500, "y": 950},
        "scale": {"x": 1, "y": 1},
        "fontSize": 24,
        "visible": True
    },
    "discord_widget": {
        "url": "",
        "pos": {"x": 1500, "y": 50},
        "scale": {"x": 1, "y": 1},
        "visible": True
    },
    "twitch_chat": {
        "channel": "",
        "theme": "dark",
        "pos": {"x": 1200, "y": 50},
        "scale": {"x": 1, "y": 1},
        "visible": False
    }
}

# --- Data Persistence Helpers ---
DATA_FILE = Path(__file__).with_name('overlay_state.json')


def deep_copy(data):
    return json.loads(json.dumps(data))


def load_data():
    if not DATA_FILE.exists():
        return deep_copy(default_data)
    try:
        with DATA_FILE.open('r', encoding='utf-8') as f:
            stored = json.load(f)
        # Merge stored data on top of defaults to guard against missing keys
        merged = deep_copy(default_data)
        merged.update(stored)
        return merged
    except (json.JSONDecodeError, OSError) as exc:
        print(f'Failed to load saved overlay state: {exc}')
        return deep_copy(default_data)


def save_data(data):
    try:
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except OSError as exc:
        print(f'Failed to persist overlay state: {exc}')


# --- Data Handling ---
current_data = load_data()

# --- Server Routes ---
@app.route('/')
def index():
    """Serves the main overlay.html file."""
    # We explicitly serve 'overlay.html' from the template folder
    return render_template('overlay.html')

@app.route('/api/operators')
def list_operators():
    """Returns a list of available operator filenames."""
    operators_dir = Path(__file__).parent / 'img' / 'Operators'
    if not operators_dir.exists():
        return json.dumps([]), 200, {'Content-Type': 'application/json'}
    operators = sorted([f.name for f in operators_dir.glob('*.png')])
    return json.dumps(operators), 200, {'Content-Type': 'application/json'}

@app.route('/api/squads')
def list_squads():
    """Returns a list of available squad filenames."""
    squads_dir = Path(__file__).parent / 'img' / 'Squads'
    if not squads_dir.exists():
        return json.dumps([]), 200, {'Content-Type': 'application/json'}
    squads = sorted([f.name for f in squads_dir.glob('*.webp')])
    return json.dumps(squads), 200, {'Content-Type': 'application/json'}

@app.route('/img/<path:folder>/<path:filename>')
def serve_image(folder, filename):
    """Serves images from the img folder."""
    img_dir = Path(__file__).parent / 'img' / folder
    return send_from_directory(str(img_dir), filename)

# --- WebSocket Events ---
@socketio.on('connect')
def handle_connect():
    """A new user connected. Send them the current data."""
    print('Client connected')
    emit('data_update', current_data)

@socketio.on('data_change')
def handle_data_change(data):
    """Received a change from the control panel."""
    global current_data
    current_data = data
    save_data(current_data)
    # Broadcast the new data to ALL connected clients (except the sender)
    emit('data_update', current_data, broadcast=True, include_self=False)
    print('Data updated and broadcasted')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# --- Run the Server ---
if __name__ == '__main__':
    print('--- Starting Stream Overlay Server at http://localhost:8000 ---')
    # Use 'eventlet' for a production-ready server, 'gevent' is also an option
    # 'allow_unsafe_werkzeug=True' is needed for newer socketio versions
    socketio.run(app, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)