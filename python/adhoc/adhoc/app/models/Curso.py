from orator import Model

class Curso(Model):
    __table__ = 'curso'
    __primary_key__ = 'id'
    __guarded__ = []
    __timestamps__ = False
