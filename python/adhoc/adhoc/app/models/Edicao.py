from orator import Model
from orator.exceptions.query import QueryException
from models.EdicaoCurso import EdicaoCurso

class Edicao(Model):
    __table__ = 'edicao'
    __primary_key__ = 'id'
    __guarded__ = []
    __timestamps__ = False

    def save_many(self, cursos_data):
     
        db = Model.get_connection_resolver()
        conn = db.connection(self.get_connection_name())

        conn.begin_transaction()
        try:
            self.save()
            EdicaoCurso.where('edicao_id', self.id).delete()
            for cd in cursos_data:
                ec = EdicaoCurso()
                ec.fill(cd)
                ec.edicao_id = self.id
                ec.save()

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise QueryException(self, [], e)
