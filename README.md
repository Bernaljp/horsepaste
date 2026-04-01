# Image Codenames

A local-network web app that lets you play [Codenames](https://en.wikipedia.org/wiki/Codenames_(board_game)) with your own images instead of word cards. Works on any device connected to the same Wi-Fi — phones, tablets, laptops.

Built with Python (Flask + Socket.IO). No internet connection required during play.

---

## How It Works

- A 5×5 grid of images is dealt at random from your `static/images/` folder
- Cards are secretly assigned colors: **9 Red**, **8 Blue**, **7 Neutral**, **1 Black Assassin**
- One player per team enables **Spymaster mode** to see the color layout
- Operatives click cards to reveal them — colors flip in real time across all devices
- Revealing the **Black card** instantly loses the round for the clicking team

---

## Downloading the Project

### Option A — Without Git (download ZIP)

1. Go to the repository page on GitHub
2. Click the green **Code** button → **Download ZIP**
3. Unzip the file — you will get a folder called `horsepaste-main` (or similar)
4. Rename it to `horsepaste` if you like

### Option B — With Git

```bash
git clone https://github.com/Bernaljp/horsepaste.git
cd horsepaste
```

---

## Setup & Run on macOS

### 1. Install Python

Open **Terminal** (`Cmd + Space` → type "Terminal").

Check if Python 3 is already installed:

```bash
python3 --version
```

If you see `Python 3.x.x` you are good. If not, download it from [python.org/downloads](https://www.python.org/downloads/) and install it.

### 2. Navigate to the project folder

If you downloaded the ZIP, replace the path with wherever you unzipped it:

```bash
cd ~/Downloads/horsepaste
```

If you cloned with git:

```bash
cd horsepaste
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Your Terminal prompt will change to show `(venv)` — this means the environment is active.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Add your images

Drop at least **25 image files** (`.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp`) into the `static/images/` folder.

> You can use any photos you like — family photos, movie stills, memes, etc. The more the better!

### 6. Start the server

```bash
python app.py
```

You should see output like:

```
(65127) wsgi starting up on http://0.0.0.0:5001
```

> **Note for macOS users:** macOS uses port 5000 for AirPlay Receiver. This app runs on **port 5001** by default to avoid the conflict. If you want to disable AirPlay Receiver, go to **System Settings → General → AirDrop & Handoff** and turn off **AirPlay Receiver**.

### 7. Open in your browser

- On the same machine: [http://localhost:5001](http://localhost:5001)
- On other devices (phones, tablets): use your Mac's local IP address — see [Playing on Multiple Devices](#playing-on-multiple-devices)

### Stopping the server

Press `Ctrl + C` in the Terminal window.

---

## Setup & Run on Windows

### 1. Install Python

Download the latest Python 3 installer from [python.org/downloads](https://www.python.org/downloads/).

**Important during installation:** Check the box that says **"Add Python to PATH"** before clicking Install Now.

After installing, open **Command Prompt** (`Win + R` → type `cmd` → press Enter) and verify:

```cmd
python --version
```

You should see `Python 3.x.x`.

### 2. Navigate to the project folder

If you downloaded the ZIP, unzip it first (right-click → "Extract All"). Then:

```cmd
cd C:\Users\YourName\Downloads\horsepaste
```

Replace `YourName` with your Windows username and adjust the path if you unzipped elsewhere.

If you cloned with git:

```cmd
cd horsepaste
```

### 3. Create a virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

Your prompt will change to show `(venv)` — this means the environment is active.

### 4. Install dependencies

```cmd
pip install -r requirements.txt
```

### 5. Add your images

Drop at least **25 image files** (`.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp`) into the `static\images\` folder.

### 6. Start the server

```cmd
python app.py
```

You should see output like:

```
(12345) wsgi starting up on http://0.0.0.0:5001
```

### 7. Open in your browser

- On the same machine: [http://localhost:5001](http://localhost:5001)
- On other devices: see [Playing on Multiple Devices](#playing-on-multiple-devices) below

### Stopping the server

Press `Ctrl + C` in the Command Prompt window.

> **Windows Firewall:** The first time you run the app, Windows may ask if you want to allow Python through the firewall. Click **Allow** to enable access from other devices on your network.

---

## Playing on Multiple Devices

To let phones and other computers join the game, they need your host machine's **local IP address**.

### Find your IP on macOS

```bash
ipconfig getifaddr en0
```

Or go to **System Settings → Wi-Fi → Details** and look for the IP address field.

### Find your IP on Windows

```cmd
ipconfig
```

Look for the line that says **IPv4 Address** under your Wi-Fi adapter. It usually looks like `192.168.x.x` or `10.0.x.x`.

### Connect from another device

On any phone, tablet, or laptop connected to the **same Wi-Fi network**, open a browser and go to:

```
http://<your-ip>:5001
```

For example: `http://192.168.1.50:5001`

---

## Game Controls

| Button | What it does |
|--------|-------------|
| **Spymaster** | Toggles color hints on (borders + tints). This is local only — enable it on the Spymaster's device. |
| **End Turn** | Passes the turn to the other team without revealing another card. |
| **New Game** | Reshuffles images and assigns new colors. All connected devices reset simultaneously. |

---

## Project Structure

```
horsepaste/
├── app.py                 # Flask server + game logic
├── requirements.txt       # Python dependencies
├── static/
│   └── images/            # Drop your 25+ images here
└── templates/
    └── index.html         # Frontend (HTML + CSS + JS, single file)
```

---

## Troubleshooting

**"Not enough images" error on startup**
→ Make sure there are at least 25 image files in `static/images/`. Subfolders are not scanned.

**Port already in use**
→ Something else is using port 5001. Open `app.py`, find the last line, and change `port=5001` to another number like `port=5002`. Use that port in the browser URL too.

**Other devices can't connect**
→ Make sure your phone/tablet is on the same Wi-Fi network as the host machine. On Windows, confirm you clicked "Allow" on the firewall prompt.

**Page shows but no images load**
→ Image filenames with spaces or special characters can sometimes cause issues. Try renaming your images to use only letters, numbers, and underscores.

**Cards aren't syncing between devices**
→ Hard-refresh the browser (`Ctrl + Shift + R` or `Cmd + Shift + R`) on the lagging device.
