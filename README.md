## **PROYECTO INDIVIDUAL º1**
## Machine Learning Operations (MLOps)

Autor: *Yuri Díaz Córdova*

¡Bienvenido al repositorio de este proyecto! 

Basados en un dataset de películas haremos un sistema de recomendación. Con este propósito realizaremos los siguientes procesos:

* ETL (Extracción, Transformación y Limpieza de datos)
* Desarrollo de la API
* EDA (Análisis exploratorio de datos)
* Modelo de machine learning (ML)

**Objetivos del proyecto**
* Cargar dos dataset y unirlos.
* Limpieza y transformación de variables.
* Exportar los datasets depurados.
* Crear los endpoints para la API. 
* Deployment en Render
* Realización del EDA

 

**Desarrollo**

1. **Ingesta de datos y extracción**

Utilizaremos los archivos: *credits.csv* y *movies_dataset.csv*.

**Fuente de los datos**:

Puedes encontrar el dataset con los dos archivos en el siguiente [link](https://drive.google.com/drive/folders/1nvSjC2JWUH48o3pb8xlKofi8SNHuNWeu).

2. **Preparación del entorno de trabajo**

* py -m venv venv | Otras opciones pueden ser python o python3

Activamos el entorno con uno de estos tres comandos:

* *source venv/Scripts/activate* | o
* *source venv\Scripts\activate* | o
* *source venv/bin/activate* | Linux y Mac


Por último se instalan las librerías necesarias para el proyecto:

* *pip install -r requirements.txt*

Tenemos todo listo para empezar a trabajar.

3. **Transformación**

Para el ETL utilizaremos la librería Pandas de Python. 

* Código dentro del notebook: ETL.ipynb

![Código](Fotos_proyecto\1.jpg)


a. **Desanidación de columnas**

Los datasets tienen varias columnas anidadas. Un ejemplo son las columnas belongs_to_collection y genres.

![Código](Fotos_proyecto\Anidadas.jpg)

La desanidación la realizamos utilizando funciones:

![Código](Fotos_proyecto\funcion_desanidar.jpg)

b. **Tratamiento de valores nulos**

![Código](Fotos_proyecto\tratamiento_nulos.jpg)

c. **Exportación de datos limpios**

Exportamos el dataframe *movies.csv* junto a otros csv que contienen el id de los actores, directores y géneros de las películas. 
![Código](Fotos_proyecto\exportación1.jpg)

4. **Desarrollo de la API**

a. **Carga y lectura en FastAPI**

En el archivo *main.py* cargamos y leemos los datasets exportados anteriormente para que FastAPI pueda usarlos en sus ednpoints.
![Código](Fotos_proyecto\carga_main.jpg)

b. **Creación de los endpoints de la API**

![Código](Fotos_proyecto\función4.jpg)

Probamos los endpoints de forma local con los siguientes comandos. 
* *uvicorn main:app --reload*

Una vez que todo funciona pasamos al siguiente paso: el *deploy*.

5. **Deployment en Render**
* Subir el repositorio a GitHub
* Entrar en render.com y crear un usuario.
* Elegir la opción Web Service
* Bajamos hasta el final y encontramos la opción Public Git Repository en la cual tendremos que ingresar el link de nuestro repositorio (asegurarse de que el mismo esté público).
* Completamos los campos requeridos (branch: main, runtime: python3, start command: 'uvicorn main:app --host 0.0.0.0 --port 10000')
* Le damos a la opción Create Web Service y esperamos unos minutos a que cargue e inicie la aplicación y la podremos acceder con el siguiente link [link](https://api-movies-l45c.onrender.com)

6. **EDA (Análisis exploratorio de datos)**

a. Importamos las librerías que utilizaremos y cargamos los datasets.
![Código](Fotos_proyecto\EDA1.jpg)

b. Exploramos la distribución gráfica de las variables y extraemos la distribución en porcentaje de los datos.
![Código](Fotos_proyecto\vote_average.jpg)

C. Eliminación de columnas irrelevantes
![Código](Fotos_proyecto\Elimina_EDA.jpg)

d. Aplicamos la transformación one-hote a la columna de géneros para dejarla preparada para el modelamiento.

![Código](Fotos_proyecto\onehot.jpg)

d. Exportamos el dataset resultante del EDA.

![Código](Fotos_proyecto\export_model.jpg)