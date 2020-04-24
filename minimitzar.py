import collections
from node import Node
import sys

class Automat:
    def __init__(self):
        self.nodes = collections.OrderedDict()
        self.symbols = []

    #Obtenim la llista de nodes
    def getNodes(self):
        return self.nodes

    #Afegim un node a la llista de nodes
    def addNode(self, node):
        self.nodes[node.getName()] = node
        self.updateSymbols()

    def updateSymbols(self):
        for nodeName, node in self.nodes.items():
            for symbol, transition in node.getTransitions().items():
                if (not symbol in self.symbols) and symbol != "E":
                    self.symbols.append(symbol)
                    self.symbols.sort()

    #Funcio per separar els nodes finals i no finals en dos subgrups
    def minimize(self):
        groups = {}
        groupByName = {}
        #Recorrem els nodes
        for nodeName, node in self.nodes.items():
            #La variable groupID ens servieix per distingir els nodes finals i els no finals
            groupID = 1
            if node.isFinal():
                groupID = 2
            if not groupID in groups:
                groups[groupID] = []
            #Afegim el node al grup corresponent
            groups[groupID].append(node)
            groupByName[node.getName()] = groupID

        self.minimize_groups(groups, groupByName)

    #Funcio per a minimitzar l'automat separat per estats finals i no finals
    def minimize_groups(self, groups, groupByName):
        nextGroupID = 1
        #Grups auxiliars
        newGroups = {}
        newGroupByName = {}
        for gID, group in groups.items():
            #Vector guardarem les transicions dels diferents grups
            groupByTransitions = {}
            #Iterem sobre els nodes del grup
            for node in group:
                transitions = node.getTransitions()
                sortedTransitions = []
                transitionGroups = []
                #Iterem pels simbols possibles del grup
                for symbol in self.symbols:
                    #Obtenim la transicio associada al simbol
                    sortedTransitions.append(transitions[symbol][0])
                #Identifiquem la transicio amb el grup que pertany
                for transition in sortedTransitions:
                    transitionGroups.append(groupByName[transition])
                transitionString = '|'.join(str(v) for v in transitionGroups)
                #Busquem l'id del group
                if transitionString in groupByTransitions:
                    groupID = groupByTransitions[transitionString]
                else:
                    #Creem un nou grup amb el id
                    groupID = nextGroupID
                    groupByTransitions[transitionString] = groupID
                    newGroups[groupID] = []
                    nextGroupID += 1
                newGroups[groupID].append(node)
                newGroupByName[node.getName()] = groupID
        #Si els vectors de grups coincideixen, eliminem els duplicats
        if groups == newGroups:
            self.deleteDuplicates(newGroups)
        else:
            #En cas contrari cridem a la funcio recursivament
            self.minimize_groups(newGroups, newGroupByName)

    #Un cop tenim el automat minimitzat eliminem els nodes duplicats
    def deleteDuplicates(self, groups):
        for groupId, group in groups.items():
            if len(group) > 1:
                validNode = None
                for duplicatedNode in group:
                    #Definim el node valid
                    if validNode is None:
                        validNode = duplicatedNode
                    else:
                        #Si ja tenim un node valid, eliminem els demes
                        del self.nodes[duplicatedNode.getName()]
                        #Canviem les transicions
                        for nodeName, node in self.nodes.items():
                            node.replaceTransition(validNode.getName(), duplicatedNode.getName())
