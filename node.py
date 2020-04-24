import collections

class Node:
    def __init__(self, name, final):
        self.name = name
        self.final = final
        self.transitions = collections.OrderedDict()

    #Obtenim el nom del node
    def getName(self):
        return self.name
    
    #Definim el nom del node
    def setName(self, name):
        self.name = name

    #Obtenim l'estat del node
    def isFinal(self):
        return self.final

    #Definim el node com a node final
    def setFinal(self, isFinal):
        self.final = isFinal

    #Obtenim les transicions del node
    def getTransitions(self):
        return self.transitions

    #Obtenim una transicio del node
    def getTransition(self, symbol):
        if symbol in self.transitions:
            return self.transitions[symbol]
        else:
            return []

    #Afegim una transicio al node
    def addTransition(self, symbol, destination):
        if not symbol in self.transitions:
            self.transitions[symbol] = []

        if not destination in self.transitions[symbol]:
            self.transitions[symbol].append(destination)

    #Eliminem una transicio del node
    def removeTransition(self, symbol):
        del self.transitions[symbol]
  
    #Intercanviem les transicions de dos nodes diferents
    def replaceTransition(self, validNode, duplicatedNode):
        for symbol, transition in self.transitions.iteritems():
            for index, nodeName in enumerate(transition):
                if nodeName == duplicatedNode:
                    transition[index] = validNode
