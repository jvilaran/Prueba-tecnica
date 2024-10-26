from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import datetime
import os

# Se crea la aplicación
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # El origen del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar a MongoDB a 27017 (Puerto predeterminado)
mongo_uri = os.getenv("MONGO_URI","mongodb://localhost:27017")
client = MongoClient(mongo_uri)

# Base de datos "biblioteca"
db = client['biblioteca']

# Colecciones de MongoDB
libros_col = db['libros']
prestamos_col = db['prestamos']
usuarios_col = db['usuarios']

# Modelo para el campo objeto_ID de MongoDB
class objeto_ID(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('ObjectId inválido') # 'raise' se utiliza para generar una excepción.
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

# Modelos Pydantic
class Libro(BaseModel):
    titulo: str
    autor: str
    cantidad: int
    disponible: bool = True

class Usuario(BaseModel):
    nombre: str
    correo: str
    telefono: int

class Prestamo(BaseModel):
    libro_id: str
    usuario_id: str
    fecha_prestamo: datetime.datetime = datetime.datetime.now()
    fecha_devolucion: datetime.datetime = None

# Mensaje para la raíz del back
@app.get("/")
def saludo():
    return "Si está funcionando"

# Crear un nuevo libro
@app.post("/libros/")
def crear_libro(libro: Libro):
    # Verificar si el libro ya existe en la colección
    libro_existente = libros_col.find_one({"titulo": libro.titulo})
    
    if libro_existente:
        # Retornar un mensaje de error si el libro ya existe
        raise HTTPException(status_code=400, detail="El libro ya existe y no se puede agregar.")
    
    nuevo_libro = libro.model_dump() # '.model_dump' genera una representación de diccionario del modelo, especificando opcionalmente qué campos incluir o excluir.
    result = libros_col.insert_one(nuevo_libro) # 'insert_one' Inserta un documento en MongoDB.
    return {"id": str(result.inserted_id)} # 'inserted_id' devuelve el identificador del nuevo documento.

# Listar todos los libros
@app.get("/libros/")
def listar_libros():
    libros = list(libros_col.find()) # 'find()' recupera todos los documentos de la colección. 'list()' devuelve la respuesta en una lista
    for libro in libros:
        libro['_id'] = str(libro['_id']) # FastAPI devuelve datos en formato JSON, es necesario convertir este campo "_id" en un string para poder enviarlo como respuesta.
    return libros # Retorna la lista de libros obtenida de la coleccion de MongoDB

# Crear un nuevo usuario
@app.post("/usuarios/")
def crear_usuario(usuario: Usuario):
    nuevo_usuario = usuario.model_dump()
    result = usuarios_col.insert_one(nuevo_usuario)
    return {"id": str(result.inserted_id)}

# Listar todos los usuarios
@app.get("/usuarios/")
def listar_usuarios():
    usuarios = list(usuarios_col.find())
    for usuario in usuarios:
        usuario['_id'] = str(usuario['_id'])
    return usuarios

# Eliminar algún usuario
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: str):
    # Convertir usuario_id a ObjectId y eliminar el usuario
    result =  usuarios_col.delete_one({"_id": ObjectId(usuario_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    return {"message": "Usuario eliminado con éxito"}

# Retornar usuario por ingreso de correo
@app.get("/usuarios/{correo}")
def obtener_usuario_por_correo(correo: str):
    usuario = usuarios_col.find_one({"correo": correo})  # Buscar por correo

    if usuario:
        usuario['_id'] = str(usuario['_id'])  # Convertir ObjectId a cadena
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Crear un préstamo
@app.post("/prestamos/")
def crear_prestamo(prestamo: Prestamo):
    # Convertir los IDs a ObjectId para realizar búsquedas en MongoDB
    libro_oid = ObjectId(prestamo.libro_id)
    usuario_oid = ObjectId(prestamo.usuario_id)
    
    # Buscar el libro en la base de datos
    libro =  libros_col.find_one({"_id": libro_oid})
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    
    # Verificar si el libro tiene suficiente cantidad
    if libro["cantidad"] <= 0:
        raise HTTPException(status_code=400, detail="No hay suficientes copias del libro.")

    # Actualizar la cantidad del libro en la base de datos
    libros_col.update_one({"_id": libro_oid},{"$inc": {"cantidad": -1}});
    if libro["cantidad"] <= 0:
        libros_col.update_one({"disponible":False})
    # Crear el registro de préstamo en la colección "prestamos"
    nuevo_prestamo = {
        "libro_id": libro_oid,
        "usuario_id": usuario_oid,
        "fecha_prestamo": datetime.datetime.now(),
        "fecha_devolucion": None
    }
    resultado =  prestamos_col.insert_one(nuevo_prestamo)

    return {"message": "Préstamo realizado con éxito", "prestamo_id": str(resultado.inserted_id)}

# Devolver un libro (actualizar préstamo)
@app.put("/prestamos/{prestamo_id}")
def devolver_libro(prestamo_id: str):
    prestamo = prestamos_col.find_one({"_id": ObjectId(prestamo_id)})
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if prestamo['fecha_devolucion']:
        raise HTTPException(status_code=400, detail="El libro ya ha sido devuelto")

    # Marcar el libro como disponible
    libros_col.update_one({"_id": ObjectId(prestamo['libro_id'])}, {"$set": {"disponible": True}})
    
    # Marcar el libro como disponible y aumentar la cantidad
    libro_id = prestamo['libro_id']

    # Actualizar la cantidad del libro en la colección
    libros_col.update_one({"_id": ObjectId(libro_id)},{"$inc": {"cantidad": 1}, "$set": {"disponible": True}})  # Incrementar cantidad y marcar como disponible

    # Actualizar la fecha de devolución en el préstamo
    prestamos_col.update_one({"_id": ObjectId(prestamo_id)}, {"$set": {"fecha_devolucion": datetime.datetime.now()}})

    # Eliminar el registro del préstamo de la colección
    prestamos_col.delete_one({"_id": ObjectId(prestamo_id)})
    
    return {"msg": "Libro devuelto con éxito"}

# Listar préstamos activos
@app.get("/prestamos/")
def listar_prestamos():
    # Obtener todos los préstamos
    prestamos =  prestamos_col.find().to_list(None)
    
    # Obtener todos los libros
    libros =  libros_col.find().to_list(None)

    # Crear un diccionario para mapear libro_id a título
    libros_dict = {str(libro['_id']): libro['titulo'] for libro in libros}

    # Agregar el título de cada libro al préstamo correspondiente
    for prestamo in prestamos:
        prestamo['_id'] = str(prestamo['_id'])
        prestamo['libro_id'] = str(prestamo['libro_id'])
        prestamo['usuario_id'] = str(prestamo['usuario_id'])

        # Obtener el título del libro usando libro_id
        prestamo['titulo_libro'] = libros_dict.get(prestamo['libro_id'], 'Título no encontrado')

    return prestamos

# Eliminar libro
@app.delete("/prestamos/{_id}")
def borrar_prestamo(_id: str):
    # Convertir el ID del préstamo a ObjectId y eliminar el documento correspondiente
    result =  prestamos_col.delete_one({"_id": ObjectId(_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado.")
    
    return {"message": "Préstamo eliminado con éxito"}

# Datos por defecto para libros
datalibros = [
    {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "cantidad": 5, "disponible": True},
    {"titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes", "cantidad": 3, "disponible": True},
    {"titulo": "1984", "autor": "George Orwell", "cantidad": 4, "disponible": True},
]

# Datos por defecto para usuarios
datausuarios = [
    {"nombre": "Jhunior Villamil", "correo": "jhunior@mail.com", "telefono": 3218188177},
    {"nombre": "test", "correo": "test@mail.com", "telefono": 3541874981}
]

def inicializar_datos(coleccion, datos):
    if coleccion.count_documents({}) == 0:  # Solo insertar si la colección está vacía
        coleccion.insert_many(datos)
        print(f"Datos insertados exitosamente en {coleccion.name}.")
    else:
        print(f"La colección {coleccion.name} ya tiene datos.")

# Insertar datos por defecto
inicializar_datos(libros_col, datalibros)
inicializar_datos(usuarios_col, datausuarios)
