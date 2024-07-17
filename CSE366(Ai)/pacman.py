The provided `pacman.py` script from UC Berkeley's Pacman AI projects contains the main code to run a Pacman game and is divided into three main sections: 

1. **Your interface to the pacman world**: This section contains the parts of the code that users need to understand to complete their projects. The main class here is `GameState`, which holds the logic for the game state, including food, capsules, agent configurations, and score changes. Accessor methods are provided to interact with this state, such as getting legal actions, generating successor states, and retrieving various game elements' positions.

2. **The hidden secrets of pacman**: This section includes the core logic that determines how Pacman and the ghosts interact with the environment. It includes classes like `ClassicGameRules`, `PacmanRules`, and `GhostRules`, which handle the movement and interactions of the agents. Constants like `SCARED_TIME`, `COLLISION_TOLERANCE`, and `TIME_PENALTY` define specific game behaviors.

3. **Framework to start a game**: This section includes the code to read the command line input, set up the game environment, and start the game. The `readCommand` function processes the command line arguments, and the `runGames` function initiates the game loop. Utility functions like `loadAgent` and `replayGame` are also included to manage agent loading and game replay.

Here is a summarized version of the script with the core functionality highlighted:

```python
from game import GameStateData, Game, Directions, Actions
from util import nearestPoint, manhattanDistance
import util, layout, sys, types, time, random, os

class GameState:
    explored = set()
    
    def getAndResetExplored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp
    getAndResetExplored = staticmethod(getAndResetExplored)

    def getLegalActions(self, agentIndex=0):
        if self.isWin() or self.isLose(): return []
        if agentIndex == 0:
            return PacmanRules.getLegalActions(self)
        else:
            return GhostRules.getLegalActions(self, agentIndex)

    def generateSuccessor(self, agentIndex, action):
        if self.isWin() or self.isLose():
            raise Exception('Cannot generate a successor of a terminal state.')

        state = GameState(self)
        if agentIndex == 0:
            state.data._eaten = [False for i in range(state.getNumAgents())]
            PacmanRules.applyAction(state, action)
        else:
            GhostRules.applyAction(state, action, agentIndex)

        if agentIndex == 0:
            state.data.scoreChange += -TIME_PENALTY
        else:
            GhostRules.decrementTimer(state.data.agentStates[agentIndex])

        GhostRules.checkDeath(state, agentIndex)

        state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state

    def getPacmanPosition(self):
        return self.data.agentStates[0].getPosition()

    def getGhostStates(self):
        return self.data.agentStates[1:]

    def getNumAgents(self):
        return len(self.data.agentStates)

    def getScore(self):
        return float(self.data.score)

    def isLose(self):
        return self.data._lose

    def isWin(self):
        return self.data._win

    def __init__(self, prevState=None):
        if prevState != None:
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()

    def deepCopy(self):
        state = GameState(self)
        state.data = self.data.deepCopy()
        return state

    def __eq__(self, other):
        return hasattr(other, 'data') and self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def initialize(self, layout, numGhostAgents=1000):
        self.data.initialize(layout, numGhostAgents)

SCARED_TIME = 40
COLLISION_TOLERANCE = 0.7
TIME_PENALTY = 1

class ClassicGameRules:
    def __init__(self, timeout=30):
        self.timeout = timeout

    def newGame(self, layout, pacmanAgent, ghostAgents, display, quiet=False, catchExceptions=False):
        agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        initState = GameState()
        initState.initialize(layout, len(ghostAgents))
        game = Game(agents, display, self, catchExceptions=catchExceptions)
        game.state = initState
        self.initialState = initState.deepCopy()
        self.quiet = quiet
        return game

    def process(self, state, game):
        if state.isWin(): self.win(state, game)
        if state.isLose(): self.lose(state, game)

    def win(self, state, game):
        if not self.quiet:
            print(f"Pacman emerges victorious! Score: {state.data.score}")
        game.gameOver = True

    def lose(self, state, game):
        if not self.quiet:
            print(f"Pacman died! Score: {state.data.score}")
        game.gameOver = True

class PacmanRules:
    PACMAN_SPEED = 1

    def getLegalActions(state):
        return Actions.getPossibleActions(state.getPacmanState().configuration, state.data.layout.walls)
    getLegalActions = staticmethod(getLegalActions)

    def applyAction(state, action):
        legal = PacmanRules.getLegalActions(state)
        if action not in legal:
            raise Exception("Illegal action " + str(action))

        pacmanState = state.data.agentStates[0]
        vector = Actions.directionToVector(action, PacmanRules.PACMAN_SPEED)
        pacmanState.configuration = pacmanState.configuration.generateSuccessor(vector)

        next = pacmanState.configuration.getPosition()
        nearest = nearestPoint(next)
        if manhattanDistance(nearest, next) <= 0.5:
            PacmanRules.consume(nearest, state)
    applyAction = staticmethod(applyAction)

    def consume(position, state):
        x, y = position
        if state.data.food[x][y]:
            state.data.scoreChange += 10
            state.data.food = state.data.food.copy()
            state.data.food[x][y] = False
            state.data._foodEaten = position
            if state.getNumFood() == 0 and not state.data._lose:
                state.data.scoreChange += 500
                state.data._win = True
        if position in state.getCapsules():
            state.data.capsules.remove(position)
            state.data._capsuleEaten = position
            for index in range(1, len(state.data.agentStates)):
                state.data.agentStates[index].scaredTimer = SCARED_TIME
    consume = staticmethod(consume)

class GhostRules:
    GHOST_SPEED = 1.0

    def getLegalActions(state, ghostIndex):
        conf = state.getGhostState(ghostIndex).configuration
        possibleActions = Actions.getPossibleActions(conf, state.data.layout.walls)
        reverse = Actions.reverseDirection(conf.direction)
        if Directions.STOP in possibleActions:
            possibleActions.remove(Directions.STOP)
        if reverse in possibleActions and len(possibleActions) > 1:
            possibleActions.remove(reverse)
        return possibleActions
    getLegalActions = staticmethod(getLegalActions)

    def applyAction(state, action, ghostIndex):
        legal = GhostRules.getLegalActions(state, ghostIndex)
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        ghostState = state.data.agentStates[ghostIndex]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0:
            speed /= 2.0
        vector = Actions.directionToVector(action, speed)
        ghostState.configuration = ghostState.configuration.generateSuccessor(vector)
    applyAction = staticmethod(applyAction)

    def decrementTimer(ghostState):
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.configuration.pos = nearestPoint(ghostState.configuration.pos)
        ghostState.scaredTimer = max(0, timer - 1)
    decrementTimer = staticmethod(decrementTimer)

    def checkDeath(state, agentIndex):
        pacmanPosition = state.getPacmanPosition()
        if agentIndex == 0:
            for index in range(1, len(state.data.agentStates)):
                ghostState = state.data.agentStates[index]
                ghostPosition = ghostState.configuration.getPosition()
                if GhostRules.canKill(pacmanPosition, ghostPosition):
                    GhostRules.collide(state, ghostState, index)
        else:
            ghostState = state.data.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.getPosition()
            if GhostRules.canKill(pacmanPosition, ghostPosition):
                GhostRules.collide(state, ghostState, agentIndex)
    checkDeath = staticmethod(checkDeath)

    def collide(state, ghostState, agentIndex):
        if ghostState.scaredTimer > 0:
            state.data.scoreChange += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
            state.data._eaten[agentIndex] = True
        else:
            if not state.data._win:
                state.data.scoreChange -= 500
                state.data._lose = True
    collide = staticmethod(collide)

    def canKill(pacmanPosition, ghostPosition):
        return manhattan

Distance(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE
    canKill = staticmethod(canKill)

    def placeGhost(state, ghostState):
        ghostState.configuration = ghostState.start
    placeGhost = staticmethod(placeGhost)

def default(string):
    return string + ' [Default: %default]'

def parseAgentArgs(string):
    if string == None or string == '': return {}
    pieces = string.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key, val = p, 1
        opts[key] = val
    return opts

def readCommand(argv):
    from optparse import OptionParser
    usageStr = """
    USAGE:      python pacman.py <options>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2"""
    parser = OptionParser(usageStr)
    parser.add_option('-n', '--numGames', dest='numGames', type='int', help=default('the number of GAMES'), metavar='GAMES', default=1)
    parser.add_option('-l', '--layout', dest='layout', type='string', help=default('the LAYOUT_FILE from which to load the map layout'), metavar='LAYOUT_FILE', default='mediumClassic')
    parser.add_option('-p', '--pacman', dest='pacman', type='string', help=default('the agent TYPE in the pacmanAgents module to use'), metavar='TYPE', default='KeyboardAgent')
    parser.add_option('-t', '--textGraphics', action='store_true', dest='textGraphics', help='Display output as text only', default=False)
    parser.add_option('-q', '--quietTextGraphics', action='store_true', dest='quietGraphics', help='Generate minimal output and no graphics', default=False)
    parser.add_option('-g', '--ghosts', dest='ghost', type='string', help=default('the ghost agent TYPE in the ghostAgents module to use'), metavar='TYPE', default='RandomGhost')
    parser.add_option('-k', '--numghosts', type='int', dest='numGhosts', help=default('The maximum number of ghosts to use'), default=4)
    parser.add_option('-z', '--zoom', type='float', dest='zoom', help=default('Zoom the size of the graphics window'), default=1.0)
    parser.add_option('-f', '--fixRandomSeed', action='store_true', dest='fixRandomSeed', help='Fixes the random seed to always play the same game', default=False)
    parser.add_option('-r', '--recordActions', action='store_true', dest='record', help='Writes game histories to a file (named by the time they were played)', default=False)
    parser.add_option('--replay', dest='gameToReplay', type='string', help='A recorded game file (pickle) to replay', default=None)
    parser.add_option('-a', '--agentArgs', dest='agentArgs', help='Comma separated values sent to agent', default='')
    parser.add_option('-x', '--numTraining', dest='numTraining', type='int', help=default('How many episodes are training (suppresses output)'), default=0)
    parser.add_option('--frameTime', dest='frameTime', type='float', help=default('Time to delay between frames; <0 means keyboard'), default=0.1)
    parser.add_option('-c', '--catchExceptions', action='store_true', dest='catchExceptions', help='Turns on exception handling and timeouts during games', default=False)
    parser.add_option('--timeout', dest='timeout', type='int', help=default('Maximum length of time an agent can spend computing in a single game'), default=30)

    options, other_junk = parser.parse_args(argv)
    if len(other_junk) != 0:
        raise Exception('Command line input not understood: ' + str(other_junk))
    args = dict()

    if options.fixRandomSeed: random.seed('cs188')
    args['layout'] = layout.getLayout(options.layout)
    if args['layout'] == None: raise Exception("The layout " + options.layout + " cannot be found")
    pacmanType = loadAgent(options.pacman, nographics=options.textGraphics)
    agentOpts = parseAgentArgs(options.agentArgs)
    pacman = pacmanType(**agentOpts)
    args['pacman'] = pacman
    ghostType = loadAgent(options.ghost, nographics=options.textGraphics)
    args['ghosts'] = [ghostType(i + 1) for i in range(options.numGhosts)]
    args['display'] = textDisplay.NullGraphics() if options.textGraphics else graphicsDisplay.PacmanGraphics(options.zoom, frameTime=options.frameTime)
    args['numGames'] = options.numGames
    args['record'] = options.record
    args['numTraining'] = options.numTraining
    args['catchExceptions'] = options.catchExceptions
    args['timeout'] = options.timeout

    return args

def loadAgent(pacman, nographics):
    moduleName = 'pacmanAgents' if pacman.endswith('Agent') else 'ghostAgents'
    module = __import__(moduleName)
    return getattr(module, pacman)

def runGames(layout, pacman, ghosts, display, numGames, record, numTraining=0, catchExceptions=False, timeout=30):
    import __main__
    __main__.__dict__['_display'] = display

    rules = ClassicGameRules(timeout)
    games = []

    for i in range(numGames):
        beQuiet = i < numTraining
        if beQuiet:
            gameDisplay = textDisplay.NullGraphics()
            rules.quiet = True
        else:
            gameDisplay = display
            rules.quiet = False
        game = rules.newGame(layout, pacman, ghosts, gameDisplay, beQuiet, catchExceptions)
        game.run()
        if not beQuiet:
            games.append(game)
        if record:
            import time
            fname = f'recorded-game-{(i + 1)}-{int(time.time())}.game'
            with open(fname, 'wb') as f:
                import pickle
                pickle.dump(game.state, f)

    if numGames > 1:
        scores = [game.state.getScore() for game in games]
        print('Average Score:', sum(scores) / float(numGames))
        print('Scores:       ', ', '.join([str(score) for score in scores]))
        print('Win Rate:      %d/%d (%.2f%%)' % (sum([game.state.isWin() for game in games]), numGames,
                                                 100.0 * sum([game.state.isWin() for game in games]) / numGames))
        print('Record:       ', ', '.join([f"{('Loss', 'Win')[game.state.isWin()]}" for game in games]))

    return games

if __name__ == '__main__':
    args = readCommand(sys.argv[1:])
    runGames(**args)

def replayGame(gamefile):
    import pickle
    with open(gamefile, 'rb') as f:
        recorded = pickle.load(f)
    rules = ClassicGameRules()
    game = rules.newGame(recorded.layout, recorded.agents[0], recorded.agents[1:],
                         recorded.display, recorded.quiet, recorded.catchExceptions)
    game.state = recorded
    game.run()
```
