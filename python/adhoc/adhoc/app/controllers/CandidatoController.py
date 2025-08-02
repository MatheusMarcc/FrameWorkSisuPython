from controllers.Controller import Controller
from models.Candidato import Candidato
import cgi

class CandidatoController(Controller):
    def index(self):
        candidatos = Candidato.all()
        self.render("index.html", candidatos=candidatos)

    def create(self):
        self.render("form.html", candidato={}, error=None)

    def store(self):
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        data = self.form2dict(form)
        existente = Candidato.where("cpf", data.get("cpf")).first()
        if existente:
            self.render("form.html",
                        candidato=data,
                        error="CPF já cadastrado. Use outro CPF.")
            return
        candidato = Candidato()
        candidato.fill(data)
        candidato.save()

        self.redirectPage("index")

    def edit(self):
        id = int(self.environ['params']['id'])
        candidato = Candidato.find(id)
        self.render("form.html", candidato=candidato, error=None)

    def update(self):
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        data = self.form2dict(form)
        id = int(data.get("id", 0))
        nome = data.get("nome", "")
        cpf = data.get("cpf", "")
        data_nascimento = data.get("data_nascimento", "")
        categoria = data.get("categoria", "")
        curso_id = int(data.get("curso_id", 0))
        nota = float(data.get("nota", 0))
        candidato = Candidato.find(id)
        if cpf != candidato.cpf:
            existe = Candidato.where("cpf", cpf).first()
            if existe:
                candidato_dict = {
                    "id": id,
                    "nome": nome,
                    "cpf": cpf,
                    "data_nascimento": data_nascimento,
                    "categoria": categoria,
                    "curso_id": curso_id,
                    "nota": nota
                }
                self.render("form.html", candidato=candidato_dict,
                            error="CPF já cadastrado. Use outro CPF.")
                return
        candidato.nome = nome
        candidato.cpf = cpf
        candidato.data_nascimento = data_nascimento
        candidato.categoria = categoria
        candidato.curso_id = curso_id
        candidato.nota = nota
        candidato.save()

        self.redirectPage("index")

    def delete(self):
        id = int(self.environ['params']['id'])
        candidato = Candidato.find(id)
        candidato.delete()
        self.redirectPage("index")
