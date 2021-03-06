import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def playlist_to_Fir(title, artist, dt, fileName, data_name):

    db = firestore.client()
    try:
        data = {'title': title,
                'artist': artist,
                'date': dt,
                'fileName': fileName
                }
        db.collection(data_name).add(data)
    except Exception as e:
        print('Problem sending data to: ' + data_name)
