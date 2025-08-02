from orator import Model

class EdicaoCurso(Model):
    __table__ = 'edicao_curso'
    __primary_key__ = 'id'
    __guarded__ = []
    __timestamps__ = False
