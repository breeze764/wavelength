#program to play the wavelength game - work in progress

from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO, emit, join_room
from rooms import create_room, rooms

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create', methods=['POST'])
def create():
    room_code = create_room()
    return redirect(url_for('host', room_code=room_code))

@app.route('/join', methods=['POST'])
def join():
    #gets the info from our form so they can join
    room_code = request.form.get('room_code').upper()
    username = request.form.get('username')
    #adds them to the room
    if room_code in rooms:
        rooms[room_code]["players"].append(username)
        #tells the server someone has joined so it can tell the host to refresh
        socketio.emit('update_player_list',room=room_code)
        return redirect(url_for('player', room_code=room_code, username=username))
    else:
        return "Room not found!", 404

@app.route('/host/<room_code>')
def host(room_code):
    return render_template('host.html',room_code=room_code,players=rooms[room_code]["players"])

@app.route('/player/<room_code>')
def player(room_code):
    return render_template('player.html', room_code=room_code)

@socketio.on('join_room')
def handle_join_room(room_code):
    join_room(room_code)

if __name__ == '__main__':
    socketio.run(app, debug=True)

