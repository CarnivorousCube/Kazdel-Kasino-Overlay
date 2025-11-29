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
# Increase maxHttpBufferSize to 10MB to handle large base64-encoded images
# Base64 encoding increases size by ~33%, so this allows ~7.5MB image files
# Use WebSocket transport for better large message handling
# Increase ping_timeout and ping_interval to prevent disconnections
socketio = SocketIO(
    app, 
    maxHttpBufferSize=10*1024*1024,  # 10 MB
    ping_timeout=60,  # Increase timeout for large messages
    ping_interval=25,  # Check connection every 25 seconds
    cors_allowed_origins="*"  # Allow CORS if needed
)

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
        # Verify we have valid data before saving
        if not data:
            print('Warning: Attempted to save None/empty data')
            return False
        
        # Check if player.pfp_url exists and log preview
        if data.get('player') and data['player'].get('pfp_url'):
            pfp_preview = data['player']['pfp_url'][:50] if isinstance(data['player']['pfp_url'], str) else 'None'
            print(f'Saving data with pfp_url preview: {pfp_preview}...')
        
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f'Successfully saved data to {DATA_FILE}')
        
        # Verify the save by reading it back
        with DATA_FILE.open('r', encoding='utf-8') as f:
            saved = json.load(f)
            if saved.get('player') and saved['player'].get('pfp_url'):
                saved_preview = saved['player']['pfp_url'][:50] if isinstance(saved['player']['pfp_url'], str) else 'None'
                print(f'Verified saved data has pfp_url: {saved_preview}...')
        
        return True
    except Exception as exc:
        import traceback
        print(f'Failed to persist overlay state: {exc}')
        traceback.print_exc()
        return False


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
    try:
        # Verify we received valid data
        if not data:
            print('ERROR: Received None/empty data!')
            return
        
        # Check data size before processing
        import sys
        import json
        data_json = json.dumps(data)
        data_size = len(data_json)
        data_size_mb = data_size / 1024 / 1024
        max_size = 10 * 1024 * 1024  # 10 MB
        
        print(f'=== Received data_change, size: {data_size_mb:.2f} MB ===')
        
        if data_size > max_size:
            print(f'Warning: Data size ({data_size_mb:.2f} MB) exceeds limit, but attempting to save anyway')
        
        # Check if pfp_url is present and log its size and type
        if data.get('player') and data['player'].get('pfp_url'):
            pfp_url = data['player']['pfp_url']
            if isinstance(pfp_url, str):
                pfp_size = len(pfp_url)
                pfp_size_mb = pfp_size / 1024 / 1024
                pfp_type = 'unknown'
                if pfp_url.startswith('data:image/png'):
                    pfp_type = 'PNG'
                elif pfp_url.startswith('data:image/webp'):
                    pfp_type = 'WebP'
                elif pfp_url.startswith('data:'):
                    pfp_type = pfp_url.split(';')[0].split(':')[1] if ';' in pfp_url else 'data URL'
                print(f'Player PFP URL: {pfp_type}, size: {pfp_size_mb:.2f} MB, preview: {pfp_url[:60]}...')
            else:
                print(f'Player PFP URL is not a string: {type(pfp_url)}')
        else:
            print('No player.pfp_url in received data')
        
        # Update current_data BEFORE saving
        old_pfp = current_data.get('player', {}).get('pfp_url', '')[:50] if current_data.get('player', {}).get('pfp_url') else 'None'
        new_pfp = data.get('player', {}).get('pfp_url', '')[:50] if data.get('player', {}).get('pfp_url') else 'None'
        print(f'Updating data - Old PFP: {old_pfp}... -> New PFP: {new_pfp}...')
        
        current_data = data
        
        # Save the data and verify it succeeded
        save_success = save_data(current_data)
        if not save_success:
            print('ERROR: Failed to save data! Not broadcasting update.')
            return
        
        # Verify current_data still has the new image before broadcasting
        if current_data.get('player') and current_data['player'].get('pfp_url'):
            verify_preview = current_data['player']['pfp_url'][:50]
            print(f'Broadcasting with PFP: {verify_preview}...')
        
        # Broadcast the new data to ALL connected clients (except the sender)
        # Also send back to sender as confirmation
        try:
            emit('data_update', current_data, broadcast=True, include_self=False)
            # Also send confirmation back to sender
            emit('data_update', current_data)
            print('Data updated and broadcasted to all clients')
        except Exception as broadcast_error:
            import traceback
            print(f'Error broadcasting data_update: {broadcast_error}')
            traceback.print_exc()
            # Still try to send to sender
            try:
                emit('data_update', current_data)
            except Exception as e:
                print(f'Failed to send to sender: {e}')
    except Exception as e:
        import traceback
        print(f'Error handling data change: {e}')
        traceback.print_exc()
        # Send current data back to sender (might be old data if save failed)
        try:
            emit('data_update', current_data)
        except:
            pass

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# --- Run the Server ---
if __name__ == '__main__':
    print('--- Starting Stream Overlay Server at http://localhost:8000 ---')
    # Use 'eventlet' for a production-ready server, 'gevent' is also an option
    # 'allow_unsafe_werkzeug=True' is needed for newer socketio versions
    socketio.run(app, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)