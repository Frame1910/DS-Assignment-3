import pyfiglet
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Print welcome banner for style points
welcome_banner = pyfiglet.figlet_format("HPaS Server")
print("\nWelcome to:\n", welcome_banner, "Stage 1")


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class Evaluator():
        def __init__(self):
            pass

        def displayScores(person_info):
            scores = person_info[1]
            for score in scores:
                print(score[0], score[1])

        def calculateGlobalAves():
            pass

        def twelveHighest():
            pass

        def calculateTopTwelveAves():
            pass

        def determineHonours():
            pass

        def sendResult():
            pass

    server.register_instance(Evaluator)

    server.serve_forever()
