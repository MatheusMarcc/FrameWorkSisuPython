from jinja2 import Environment, FileSystemLoader
import os
import cgi
from html import escape
from urllib.parse import urlencode

class Controller:
    def __init__(self, env):
        self.environ = env
        self.data = ""
        self.status = "200 OK"
        self.redirect_url = ""
        self.session = env.get('session', {})
        self.nome = (self.__class__.__name__).lower()[:-len("controller")]
        self.env = Environment(loader=FileSystemLoader(os.getcwd() + f'/views/{self.nome}'))

    def form2dict(self, form):
        d = {}
        for key in form.keys():
            val = form.getvalue(key)
            if isinstance(val, (list, tuple)):
                val = val[0]
            d[key] = escape(str(val)) if val is not None else ""
        return d

    def loadForm(self, model):
        form = cgi.FieldStorage(fp=self.environ.get("wsgi.input"), environ=self.environ)
        model.fill(self.form2dict(form))

    def loadNestedForm(self):
        form = cgi.FieldStorage(fp=self.environ.get("wsgi.input"), environ=self.environ)
        nested_data = {}
        for key in form:
            value = escape(str(form.getvalue(key)))
            if "[" in key and "]" in key:
                base, rest = key.split("[", 1)
                idx, field = rest[:-1].split("][")
                idx = int(idx)
                nested_data.setdefault(base, [])
                while len(nested_data[base]) <= idx:
                    nested_data[base].append({})
                nested_data[base][idx][field] = value
            else:
                nested_data[key] = value
        return nested_data

    def render(self, template_name, **context):
        template = self.env.get_template(template_name)
        self.data = template.render(**context)

    def redirectPage(self, path: str, params=None):
        self.status = "302 OK"
        self.redirect_url = f'/app/{self.nome}/{path}'
        if params:
            self.redirect_url += f'?{urlencode(params)}'

    def notFound(self):
        self.status = "404 Not Found"
        tmpl = Environment(loader=FileSystemLoader(os.getcwd() + '/views/public')).get_template("404.html")
        self.data = tmpl.render()
