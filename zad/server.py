from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import uuid
from jsonrpc import JSONRPCResponseManager, dispatcher

@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]

def wypisz(s):
    return s

def dodaj(a, b):
    return a + b

def generuj():
    return str(uuid.uuid4())

@Request.application
def application(request):
    dispatcher["echo"] = wypisz
    dispatcher["add"] = dodaj
    dispatcher["generate"]=generuj

    response = JSONRPCResponseManager.handle(
        request.get_data(cache=False, as_text=True), dispatcher)
    return Response(response.json, mimetype='application/json')

if __name__ == '__main__':
    run_simple('localhost', 4000, application)
