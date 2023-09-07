from flask import request
from Global.Classes.Usuario import Usuario
import json



def registrar_usuario():
    try:
        params = {
            'username': request.json.get('username'),
            'nombre': request.json.get('nombre'),
            'pass': request.json.get('pass'),
            'activo': request.json.get('activo'),
            'rol': request.json.get('rol')
        }
        usuario = Usuario(params, False)
        return f'El usuario: {usuario.username} para {usuario.nombre} fue registrado', 200
    except Exception as e:
        return {'error': str(e)}, 400

def iniciar_sesion():
    try:
        params = {
            'username': request.json.get('username'),
            'pass': request.json.get('pass'),
            'rol': request.json.get('rol')
        }
        try:
            usuario = Usuario(params)
        except Exception as e:
            return {'error': str(e)}, 400
        return usuario.web_token, 200
    except Exception as e:
        return {'error': str(e)}, 400