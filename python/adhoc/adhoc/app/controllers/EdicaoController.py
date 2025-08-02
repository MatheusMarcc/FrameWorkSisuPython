from controllers.Controller import Controller
from models.Edicao import Edicao
from models.Curso import Curso
import cgi

class EdicaoController(Controller):
    def index(self):
        edicoes = Edicao.all()
        self.render("index.html", edicoes=edicoes)

    def create(self):
        cursos = Curso.all()
        self.render("form.html", edicao={}, detalhes=[], cursos=cursos)

    def store(self):
        data = self.loadNestedForm()
        cursos_data = data.pop("cursos", [])
        ed = Edicao()
        ed.nome = data.get("nome")
        ed.save_many(cursos_data)
        self.redirectPage("index")

    def edit(self):
        eid = int(self.environ['params']['id'])
        edicao = Edicao.find(eid)
        from models.EdicaoCurso import EdicaoCurso
        detalhes = EdicaoCurso.where('edicao_id', eid).get()
        cursos = Curso.all()
        self.render("form.html", edicao=edicao, detalhes=detalhes, cursos=cursos)

    def update(self):
        data = self.loadNestedForm()
        cursos_data = data.pop("cursos", [])
        eid = int(data.get("id", 0))
        ed = Edicao.find(eid)
        ed.nome = data.get("nome", ed.nome)
        ed.save_many(cursos_data)
        self.redirectPage("index")

    def delete(self):
        eid = int(self.environ['params']['id'])
        Edicao.find(eid).delete()
        self.redirectPage("index")
