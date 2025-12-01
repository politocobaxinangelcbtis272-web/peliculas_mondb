from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client.get_default_database()
db = client['peliculas_db']
peliculas = db['peliculas']

db.peliculas.delete_many({})

peliculas = [
     {
        'pelicula': 'Avengers: Endgame',
        'año': 2019,
        'genero': 'Acción, Ciencia Ficción',
        'calificacion': 8.4,
        'comentario': 'Epico cierre de la saga del Infinity.',
        'imagen': 'marvel.jpeg',
        'fecha_creacion': datetime.now()
            },
    {
        'pelicula': 'superman',
        'año': 2025,
        'genero': 'Acción, Avenctura, fantasia',
        'calificacion': 9.0,
        'comentario': ' ser diferente es una virtud y que las decisiones que tomamos definen quiénes somos.',
        'imagen': 'superman.jpg',
        'fecha_creacion': datetime.now()
    },
    {
        'pelicula': 'minecraft',
        'año': 2025,
        'genero': 'fantasia, Avenctura, Acción',
        'calificacion': 8.8,
        'comentario': 'ser la adaptación que el videojuego.',
        'imagen': 'minecraft.jpeg',
        'fecha_creacion': datetime.now()
    },
    {
        'pelicula': 'spiderman 2',
        'año': 2004,
        'genero': 'fantasia, accion, Drama',
        'calificacion': 8.0,
        'comentario': 'spidermans medio del sufrimiento, la única opción es buscar la mejor forma de superar las adversidades.',
        'imagen': 'spiderman_2.jpg',
        'fecha_creacion': datetime.now()
    }
     {
        'pelicula': 'coco',
        'año': 2017,
        'genero': 'accion',
        'calificacion': 9.5,
        'comentario': 'dia de los muertos.',
        'imagen': 'coco.jpg',
        'fecha_creacion': datetime.now()
    }
      {
        'titulo': 'Spider-Man: No Way Home',
        'año': 2021,
        'genero': 'Acción, comedia,fantasia',
        'calificacion': 8.2,
        'comentario': 'Multiverso y spidermans de diferentes eras.',
        'imagen': 'spiderman_2021.jpeg',
        'fecha_creacion': datetime.now()
    } 
    
      {
        'titulo': 'Spider-Man: No Way Home',
        'año': 2021,
        'genero': 'sobrenatural , misterio',
        'calificacion': 8.2,
        'comentario': 'terro cosas sobre natural.',
        'imagen': 'terror.jpeg',
        'fecha_creacion': datetime.now()
    } 
    {
        'pelicula': 'zootopia 1',
        'año': 2019,
        'genero': comedia, Drama',
        'calificacion': 9.0,
        'comentario': 'zootopia medio del animales, la única opción es buscar la mejor forma de superar las adversidades.',
        'imagen': 'zootopia 1.webp',
        'fecha_creacion': datetime.now()
    },
]


db.peliculas.insert_many(peliculas)
print("Seed completado. Registros insertados:", db.peliculas.count_documents({}))
