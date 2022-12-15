from flask import Flask, render_template, request, redirect
import re
from db.config import get_db_connection
from utils.functions import create_user, logIn,  albumAndArtist, artista, create_artist, delete_artist
from pprint import pprint
from collections import defaultdict
from itertools import chain

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('inicio.html')

@app.route("/signup", methods = ['POST'])
def newUser():
    cur, conn  = get_db_connection()
    try:
        with conn:
            username = request.form['username']
            fullname = request.form['fullname']
            password = request.form['password']


            if len(username) < 4:
                 raise Exception("El nombre de usuario debe tener una longitud mayor a 4 caracteres")
            if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
                 raise Exception("La contraseña no cumple los requisitos")
            
            if username and fullname and password:
                user = username, fullname, password, 0

                create_user(conn, cur, user)

                return redirect('/')
            else:
                raise Exception("Debes ingresar todos los campos")
    except Exception:
        return {
            'error': True,
            'message': f'Algo salió mal'
        }

@app.route("/login", methods = ['POST'])
def login():
    cur, conn  = get_db_connection()
    with conn:
        username = request.form['username']
        password = request.form['password']

        if len(username) < 4:
                 raise Exception("El nombre de usuario debe tener una longitud mayor a 4 caracteres")

        user = logIn(conn, cur, username, password)
        isLogged = True if user else False

        if isLogged:
            return redirect('/search')
        else:
            return render_template('signin.html')


@app.route("/search", methods=['GET', 'POST'])
def searchCards():
    cur, conn  = get_db_connection()
    album = albumAndArtist(conn, cur)
    
    myList = []

    for artist in album:
        data = ('id', 'album', 'artist', 'track')
        if len(artist) == len(data):
            res = {data[i] : artist[i] for i, _ in enumerate(artist)}
            myList.append(res)

    filteredData = []

    vacio = []

    if request.method == 'POST':
       
        filter = request.form['filtering']


        for album in myList:
            filter = filter.upper()
            if album['album'].upper().startswith(filter) or album['artist'].upper().startswith(filter) or album['track'].upper().startswith(filter):
                filteredData.append(album)
            if not album['album'].upper().startswith(filter) or album['artist'].upper().startswith(filter) or album['track'].upper().startswith(filter):
                vacio.append("")


    return render_template('cards.html', myList=myList, filteredData=filteredData, vacio=vacio)

    
@app.route("/crud", methods=['GET', 'POST','DELETE'])
def crud():
    cur, conn  = get_db_connection()
    myList = []

    if request.method == 'GET':
        artistaa = artista(conn, cur)


        for i in artistaa:
                characters = "'(),"
                i = ''.join( x for x in i if x not in characters)
                myList.append(i)
    
    if request.method == 'POST':
            with conn:
                artistaform = request.form['artistaname']

                artistname = artistaform 

                create_artist(conn,cur,artistname)

                return redirect('/crud')

    if request.method == 'DELETE':
        with conn:
            artistadeleteform = request.form['artistadelete']

            artistadelete=artistadeleteform
                                
            delete_artist(conn,cur,artistadelete)

            return redirect('/crud')


    
    return render_template('crud.html', myList=myList)



if __name__ == '__main__':
    app.run(debug=True)