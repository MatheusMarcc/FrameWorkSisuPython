from controllers.Controller import Controller
from models.EdicaoCurso import EdicaoCurso
from models.Candidato import Candidato
from models.Curso import Curso
from models.Edicao import Edicao
import cgi

class ConvocacaoController(Controller):
    def index(self):
        edicoes = Edicao.all()
        cursos  = Curso.all()
        self.render("form.html", edicoes=edicoes, cursos=cursos)

    def gerar(self):
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        data = self.form2dict(form)

        edicao_id     = int(data.get("edicao_id",     0))
        multiplicador = int(data.get("multiplicador", 1))
        raw = form.getvalue("curso_ids")
        if isinstance(raw, list):
            curso_ids = [int(x) for x in raw if x]
        elif raw:
            curso_ids = [int(raw)]
        else:
            curso_ids = []

        edicao = Edicao.find(edicao_id)

        modalidades = [
            ("vagas_ac",          "Ampla Concorrência"),
            ("vagas_ppi_br",      "PPI - Baixa Renda"),
            ("vagas_publica_br",  "Pública - Baixa Renda"),
            ("vagas_ppi_publica", "PPI - Pública"),
            ("vagas_publica",     "Pública"),
            ("vagas_deficientes", "Deficientes"),
        ]

        listas = []
        for curso_id in curso_ids:
            bloco = {
                "curso":    Curso.find(curso_id),
                "resultado": {}
            }
            ec = (EdicaoCurso
                  .where("edicao_id", edicao_id)
                  .where("curso_id",  curso_id)
                  .first())

            for coluna, categoria in modalidades:
                vagas = getattr(ec, coluna) if ec else 0
                qtd   = int(vagas) * multiplicador
                if qtd > 0:
                    candidatos = (Candidato
                                  .where("curso_id", curso_id)
                                  .where("categoria", categoria)
                                  .order_by("nota", "desc")
                                  .limit(qtd)
                                  .get())
                else:
                    candidatos = []
                bloco["resultado"][categoria] = candidatos

            listas.append(bloco)

        self.render("resultado.html", listas=listas, edicao=edicao)
