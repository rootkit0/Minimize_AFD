from node import Node
from minimitzar import Automat
import sys

class Main:
    def __init__(self):
        args = sys.argv
        #Inicialitzem el automat
        automat = Automat()
        #Llegim el automat del fitxer
        self.loadFile(automat, "input.txt")
        #Executem la funcio per a minimitzar el automat
        automat.minimize()
        #Printem el automat resultant per pantalla
        self.printResult(automat)
        sys.exit()

    def loadFile(self, automat, arxiu):
        f = open(arxiu)
        #Llegim el fitxer linia per linia
        for line in f:
            line = line.rstrip()
            data = line.split()
            #Obtenim el node i el seu estat
            node_name = data[0]
            node_status = False
            if(data[1] == "F"):
                node_status = True
            #Inicialitzem el node
            node = Node(node_name, node_status)
            #Obtenim les transicions
            del data[:1]
            for transition in data:
                transition = transition.split("-")
                if(len(transition) == 2):
                    node.addTransition(transition[0], transition[1])
            #Afegim el node al automat
            automat.addNode(node)
        f.close()

    def printResult(self, automat):
        #Recorrem tots els nodes del automat
        nodes = automat.getNodes()
        for nodeName, node in nodes.items():
            #Afegim el nom del node
            line = node.getName()
            #Afegim el seu estat
            if(node.isFinal()):
                line += " F "
            else:
                line += " N "
            #Recorrem totes les transicions del node
            transicions = node.getTransitions()
            for symbol, transition in transicions.items():
                for destinationNode in transition:
                    #Afegim les transicions
                    line += "%s-%s " % (symbol, destinationNode)
            print(line)

Main()
