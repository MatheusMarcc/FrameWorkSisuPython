from controllers.Controller import Controller
from models.Curso import Curso
import cgi

class CursoController(Controller):
    def index(self):
        cursos = Curso.all()
        self.render("index.html", cursos=cursos)

    def create(self):
        self.render("form.html", curso={})

    def store(self):
        curso = Curso()
        self.loadForm(curso)
        curso.save()
        self.redirectPage("index")

    def edit(self):
        id = int(self.environ['params']['id'])
        curso = Curso.find(id)
        self.render("form.html", curso=curso)

    def update(self):
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        data = self.form2dict(form)
        id = int(data.get("id", 0))
        nome = data.get("nome", "")
        curso = Curso.find(id)
        curso.nome = nome
        curso.save()

        self.redirectPage("index")

    def delete(self):
        id = int(self.environ['params']['id'])
        curso = Curso.find(id)
        curso.delete()
        self.redirectPage("index")
