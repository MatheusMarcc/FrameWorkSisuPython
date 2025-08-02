from orator import Model

class Candidato(Model):
    __table__ = 'candidato'
    __primary_key__ = 'id'
    __guarded__ = []
    __timestamps__ = False
