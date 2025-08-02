from controllers.Controller import Controller
from models.Edicao import Edicao
from models.Curso import Curso
from models.Candidato import Candidato

class DashboardController(Controller):
    def index(self):
        edicoes    = Edicao.all()
        cursos     = Curso.all()
        candidatos = Candidato.all()

        params        = self.environ.get('params', {})
        edicao_to_edit = None
        detalhes       = []

        if 'id' in params:
            edicao_to_edit = Edicao.find(int(params['id']))
            from models.EdicaoCurso import EdicaoCurso
            detalhes = EdicaoCurso.where('edicao_id', edicao_to_edit.id).get()

        modalidades = [
            "Ampla Concorrência",
            "PPI - Baixa Renda",
            "Pública - Baixa Renda",
            "PPI - Pública",
            "Pública",
            "Deficientes"
        ]

        # Qual seção deve aparecer aberta?
        section = params.get('section', 'edicao')

        self.render(
            "index.html",
            edicoes=edicoes,
            cursos=cursos,
            candidatos=candidatos,
            edicao_to_edit=edicao_to_edit,
            detalhes=detalhes,
            modalidades=modalidades,
            section=section
        )
