# Kazdel Kasino Stream Overlay

A customizable, real-time stream overlay system designed for OBS Studio. This overlay allows you to display player information, team details, operator and squad icons, Discord widgets, Twitch chat, and customizable text elements on your stream.

## 📋 Table of Contents

- [What is This?](#what-is-this)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [Setting Up in OBS](#setting-up-in-obs)
- [Using the Control Panel](#using-the-control-panel)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)

---

## 🎯 What is This?

This is a web-based overlay system that creates customizable widgets for your OBS stream. You can:

- Display player names, team names, and profile pictures
- Show operator and squad icons from your game
- Add Discord reactive widgets
- Embed Twitch chat
- Display custom text at the bottom of your stream
- Control everything in real-time through a web-based control panel

The overlay runs on a local web server and displays in OBS as a browser source. Changes you make in the control panel update instantly on your stream!

---

## 📦 Prerequisites

Before you begin, make sure you have:

1. **Python 3.7 or higher** installed on your computer
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation by opening Command Prompt/Terminal and typing: `python --version`

2. **OBS Studio** installed
   - Download from [obsproject.com](https://obsproject.com/)
   - Any recent version will work

3. **A web browser** (Chrome, Firefox, Edge, etc.)

---

## 🚀 Installation

### Step 1: Download/Clone the Project

If you have Git installed:
```bash
git clone <repository-url>
cd "Kazdel Kasino Overlay"
```

Or simply download the project folder and extract it to a location you can easily find (like your Desktop or Documents folder).

### Step 2: Install Python Dependencies

1. **Open Command Prompt (Windows) or Terminal (Mac/Linux)**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `Terminal`, press Enter
   - Linux: Press `Ctrl + Alt + T`

2. **Navigate to the project folder**
   ```bash
   cd "D:\Kazdel Kasino Overlay"
   ```
   *(Replace with your actual folder path)*

3. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - Flask (web server framework)
   - Flask-SocketIO (real-time communication)
   - eventlet (server engine)

   **Note:** If you get a "pip is not recognized" error, try:
   ```bash
   python -m pip install -r requirements.txt
   ```

### Step 3: Verify Installation

You should see messages like:
```
Successfully installed Flask-X.X.X Flask-SocketIO-X.X.X eventlet-X.X.X
```

If you see any errors, make sure Python is installed correctly and try again.

---

## 🖥️ Running the Server

### Starting the Server

1. **Open Command Prompt/Terminal** (same as before)

2. **Navigate to your project folder**
   ```bash
   cd "D:\Kazdel Kasino Overlay"
   ```

3. **Run the server**
   ```bash
   python server.py
   ```

   You should see:
   ```
   --- Starting Stream Overlay Server at http://localhost:8000 ---
   ```

4. **Keep this window open!** The server needs to keep running for the overlay to work.

### Accessing the Overlay

Once the server is running, you can access:

- **Main Overlay** (for OBS): `http://localhost:8000/`
- **Control Panel**: `http://localhost:8000/?controls`

Open these URLs in your web browser to verify they work before adding to OBS.

---

## 📺 Setting Up in OBS

### Step 1: Add Browser Source

1. Open OBS Studio
2. In your scene, right-click in the "Sources" panel
3. Select **Add → Browser Source**
4. Name it something like "Kazdel Overlay" and click OK

### Step 2: Configure Browser Source

In the Browser Source properties window:

1. **URL**: Enter `http://localhost:8000/`
   - This is the main overlay (what viewers see)

2. **Width**: `1920`
   - The overlay is designed for 1920x1080 resolution

3. **Height**: `1080`

4. **Custom CSS**: Leave empty (not needed)

5. **Shutdown source when not visible**: Unchecked (so it stays active)

6. **Refresh browser when scene becomes active**: Checked (ensures updates show)

7. Click **OK**

### Step 3: Position and Resize (Optional)

- The overlay elements are draggable and resizable when the control panel is closed
- You can adjust positions later using the control panel

### Step 4: Test It

You should now see the overlay in OBS! If you see a black screen or nothing:
- Make sure the server is running (`python server.py`)
- Check that the URL in OBS is exactly `http://localhost:8000/`
- Try refreshing the browser source in OBS

---

## 🎮 Using the Control Panel

The control panel is where you customize everything about your overlay.

### Opening the Control Panel

1. **Open your web browser** (keep it separate from OBS)
2. Go to: `http://localhost:8000/?controls`
3. You should see a dark control panel with various sections

### Control Panel Sections

#### 1. **Visibility Controls**
Toggle which widgets are visible on stream:
- ✅ Player Widget
- ✅ Left Text
- ✅ Right Text
- ✅ Discord Widget
- ✅ Twitch Chat

#### 2. **Player Controls**
- **Player Name**: The name displayed on the player widget
- **Team Name**: The team name displayed
- **Discord PFP**: Upload a profile picture (supports any image format)
- **Squad Icon**: Select from available squads in the dropdown
- **Operator Icon**: Select from available operators in the dropdown

#### 3. **Bottom Text Controls**
- **Bottom Left Text**: Custom text displayed at the bottom left
- **Bottom Right Text**: Custom text displayed at the bottom right

#### 4. **Discord Reactive Widget**
- **Discord Reactive URL**: Paste your Discord reactive widget URL
  - To get this: Go to Discord → Server Settings → Widget → Enable Widget → Copy the URL

#### 5. **Twitch Chat Widget**
- **Twitch Channel**: Enter your Twitch channel name (without the @ or twitch.tv/)
- **Theme**: Choose Dark or Light theme

### Using the Dropdowns

The Operator and Squad dropdowns are searchable:

1. **Click** in the input field or the dropdown arrow
2. **Type** to filter the list
3. **Click** an item to select it
4. **Click the × button** to clear the selection
5. The preview updates immediately!

### Dragging and Resizing Widgets

When the control panel is **closed** (not visible):

1. **Hover** over any widget on the overlay
2. You'll see drag handles appear
3. **Click and drag** to move widgets around
4. **Use the resize handle** (bottom-right corner) to resize
5. **Use the font resize handle** (bottom-left corner, text widgets only) to change font size

**Note:** The control panel must be closed to drag/resize. Close it by clicking "Close Panel" or refreshing the overlay page.

### Saving Your Settings

- All changes are **automatically saved** to `overlay_state.json`
- Settings persist between server restarts
- Multiple OBS instances can connect to the same server

---

## ✨ Features

### Real-Time Updates
- Changes in the control panel update instantly on stream
- No need to refresh OBS browser sources
- Multiple browser sources can connect simultaneously

### Customizable Widgets
- **Player Widget**: Shows player name, team, profile picture, squad icon, and operator icon
- **Text Widgets**: Two customizable text areas at the bottom
- **Discord Widget**: Embed Discord reactive widgets
- **Twitch Chat**: Display your Twitch chat overlay

### Drag & Drop Interface
- Move widgets anywhere on the 1920x1080 canvas
- Resize widgets with visual handles
- Adjust font sizes for text widgets

### Image Management
- Upload custom profile pictures
- Select from pre-loaded operator and squad icons
- Searchable dropdown lists with image previews

---

## 🔧 Troubleshooting

### Server Won't Start

**Error: "python is not recognized"**
- Python is not installed or not in PATH
- Reinstall Python and check "Add Python to PATH"
- Or use `py server.py` instead of `python server.py`

**Error: "No module named 'flask'"**
- Dependencies aren't installed
- Run: `pip install -r requirements.txt`

**Error: "Address already in use"**
- Port 8000 is already in use
- Close other applications using port 8000
- Or modify `server.py` to use a different port (change `port=8000`)

### Overlay Not Showing in OBS

**Black screen or nothing visible:**
1. Verify server is running (check the terminal window)
2. Test the URL in a browser: `http://localhost:8000/`
3. Check OBS Browser Source URL is exactly `http://localhost:8000/`
4. Try refreshing the browser source (right-click → Refresh)

**Widgets not appearing:**
1. Open the control panel: `http://localhost:8000/?controls`
2. Check the Visibility section - make sure widgets are enabled
3. Verify widgets aren't positioned off-screen

### Control Panel Not Working

**Can't access control panel:**
- Make sure you're using: `http://localhost:8000/?controls`
- The `?controls` part is required!

**Changes not saving:**
- Check that `overlay_state.json` exists and is writable
- Look for error messages in the server terminal
- Try restarting the server

### Images Not Loading

**Operator/Squad icons not showing:**
- Verify images exist in `img/Operators/` and `img/Squads/` folders
- Check file names match exactly (case-sensitive)
- Ensure server is running and can access the `img` folder

**Profile picture not uploading:**
- Check file size (very large images may cause issues)
- Try a different image format (PNG, JPG, WEBP)
- Check browser console for errors (F12)

### Twitch Chat Not Working

**Chat not appearing:**
- Twitch chat requires the overlay to be served over HTTP/HTTPS (not file://)
- Make sure you're accessing via `http://localhost:8000/` in OBS
- Verify your Twitch channel name is correct (no @ symbol, no twitch.tv/)
- Check that the channel name is set in the control panel

---

## 📁 File Structure

```
Kazdel Kasino Overlay/
│
├── server.py              # Main server file (run this!)
├── overlay.html            # The overlay webpage
├── overlay_state.json      # Saved settings (auto-generated)
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
└── img/                   # Image assets
    ├── Operators/         # Operator icon images (.png)
    └── Squads/           # Squad icon images (.webp)
```

### Important Files

- **`server.py`**: The web server - run this to start the overlay system
- **`overlay.html`**: Contains all the overlay code and control panel
- **`overlay_state.json`**: Stores your settings (don't delete this!)
- **`requirements.txt`**: Lists required Python packages

---

## 💡 Tips & Best Practices

1. **Keep the Server Running**: The server must stay running while streaming. Consider creating a desktop shortcut or batch file to start it easily.

2. **Create a Startup Script** (Windows):
   Create a file `start_server.bat` with:
   ```batch
   @echo off
   cd /d "D:\Kazdel Kasino Overlay"
   python server.py
   pause
   ```
   Double-click this file to start the server!

3. **Multiple Scenes**: You can add the same browser source to multiple OBS scenes - they'll all show the same overlay.

4. **Browser Source Refresh**: If changes don't appear, right-click the browser source in OBS → Refresh.

5. **Backup Settings**: Copy `overlay_state.json` to backup your configuration.

6. **Network Access**: By default, the server only accepts connections from `localhost`. To access from other devices on your network, modify `server.py` (change `host='0.0.0.0'` - it's already set, but you'll need to use your computer's IP address).

---

## 🆘 Getting Help

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Check the server terminal for error messages
3. Open browser console (F12) to see JavaScript errors
4. Verify all prerequisites are installed correctly
5. Make sure you're using the correct URLs (`http://localhost:8000/` and `http://localhost:8000/?controls`)

---

## 📝 Notes

- The overlay is designed for **1920x1080** resolution
- All settings are saved automatically
- The server runs on **port 8000** by default
- Images are served from the `img/` folder
- The overlay uses WebSockets for real-time updates

---

## 🎉 You're All Set!

You now have a fully functional stream overlay system! Experiment with the different widgets, customize the appearance, and make it your own.

Happy streaming! 🎮📺

