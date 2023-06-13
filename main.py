from fastapi import FastAPI
import pandas as pd
#Cargamos el dataset movies.csv como un dataframe de Pandas
movies = pd.read_csv("data/movies.csv", index_col='id')

#Convertimos las siguientes columnas en listas para facilitar la manipulación
movies[['id_genre', 'id_actor', 'id_directores']] = movies[[
    'id_genre', 'id_actor', 'id_directores']].apply(lambda x: x.apply(eval))

#Carga de datasets como diccionarios para facilitar el acceso
genres = pd.read_csv("data/genres.csv", index_col='genre').to_dict(
    orient='dict')['id']
actors = pd.read_csv("data/actors.csv", index_col='actor').to_dict(
    orient='dict')['id']
directors = pd.read_csv("data/directors.csv", index_col='director').to_dict(
    orient='dict')['id']

meses = {
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12
}


app = FastAPI()


# 1
#Función para obtener la cantidad de filmaciones en un mes solicitado
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    mes = mes.lower().strip()
    numero_mes = meses.get(mes, 0)

    cantidad = len(movies[movies['release_month'] == numero_mes])

    return {'mes': mes, 'cantidad': cantidad}


# 2
#Función para obtener la cantidad de filmaciones en un día solicitado
@app.get('/cantidad_filmaciones_dia{dia}')
def cantidad_filmaciones_dia(dia: str):
    dia = dia.lower().strip()
    cantidad = len(movies[movies['release_day'].str.lower() == dia])

    return {'dia': dia, 'cantidad': cantidad}


# 3
#Función para obtener por su título el año de estreno y el score de una película
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo_de_la_filmacion: str):
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower().strip()
    filmacion = movies[movies['title'].str.lower() == titulo_de_la_filmacion]

    if filmacion.empty:
        return "No se encontró la filmación especificada."
    else:
        titulo = filmacion['title'].values[0]
        año_estreno = filmacion['release_year'].values[0]
        score = filmacion['popularity'].values[0]

        return {'titulo': str(titulo), 'anio': str(año_estreno), 'popularidad': str(score)}


# 4
#Función para obtener por su título la cantidad de votos y el valor promedio
#de las votaciones de una película
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo_de_la_filmacion: str):
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower().strip()
    filmacion = movies[movies['title'].str.lower() == titulo_de_la_filmacion]

    if filmacion.empty:
        return "No se encontró la filmación especificada."

    vote_count = filmacion['vote_count'].values[0]
    vote_average = filmacion['vote_average'].values[0]
    release_year = filmacion['release_year'].values[0]

    if vote_count < 2000:
        return "La filmación no cumple con el requisito mínimo de 2000 valoraciones."

    return {'titulo': titulo_de_la_filmacion.title(), 'anio': str(release_year), 'voto_total': str(vote_count), 'voto_promedio': str(vote_average)}


# 5
#Función para obtener el éxito de un actor medido a través del promedio de retorno y la cantidad de películas en las que ha participado
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    nombre_actor = nombre_actor.lower().strip()

    if nombre_actor in actors:
        actor_id = actors[nombre_actor]
        participaciones = sum(
            movies['id_actor'].apply(lambda x: actor_id in x))
        retorno_total = movies[movies['id_actor'].apply(
            lambda x: actor_id in x)]['return'].sum()
        promedio_retorno = retorno_total / participaciones if participaciones > 0 else 0

        return {'actor': nombre_actor, 'cantidad_filmaciones': participaciones, 'retorno_total': retorno_total, 'retorno_promedio': promedio_retorno}
    else:
        return f"No se encontró el actor {nombre_actor} en el dataset."


# 6
#Función para obtener el nombre de cada película en la que participó el director, la fecha de lanzamiento, el costo y el retorno individual
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    nombre_director = nombre_director.lower().strip()

    if nombre_director in directors:
        director_id = directors[nombre_director]
        peliculas_director = movies[movies['id_directores'].apply(
            lambda x: director_id in x)]

        if peliculas_director.empty:
            return {"director": nombre_director, "películas": [], "retorno_total_director": 0}

        retorno_total = peliculas_director['return'].sum()

        resultado = {
            "director": nombre_director,
            "retorno_total_director": retorno_total,
            "películas": []
        }

        for index, pelicula in peliculas_director.iterrows():
            titulo = pelicula['title']
            fecha_lanzamiento = pelicula['release_date']
            retorno = pelicula['return']
            costo = pelicula['budget']
            ganancia = pelicula['revenue']

            pelicula_info = {
                "Título": titulo,
                "Fecha_lanzamiento": fecha_lanzamiento,
                "retorno": retorno,
                "presupuesto": costo,
                "recaudación": ganancia
            }

            resultado["películas"].append(pelicula_info)

        return resultado
    else:
        return {"director": nombre_director, "películas": [], "retorno_total_director": 0}
