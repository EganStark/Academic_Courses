# -*- coding: utf-8 -*-
"""Lab2(task1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dw5_BhhrEOFyh3FODen7DPPDJUJeGUdr

<a href="https://colab.research.google.com/github/raihanewubd/cse366-01/blob/main/AI_Lab3.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
"""

import random
import math
import matplotlib.pyplot as plt

"""![x6.png](data:image/png;base64,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)

Consider a household trading agent that monitors the price of some commodity, such as toilet paper, by checking for deals online, as well as how much the household has in stock. It must decide whether to order more and how much to order. Assume the percepts are the price and the amount in stock. The command is the number of units the agent decides to order (which is zero if the agent does not order any). A percept trace specifies for each time point (e.g., each day) the price at that time and the amount in stock at that time.

# **Task 1**
Modify the existing code to fullfill following condtions

1.   If the last_price is less than 70% of the average (ave) and the instock quantity is less than 30, then set tobuy to 15.
2.   Otherwise, if the instock quantity is less than 10, set tobuy to 5.
If none of the above conditions apply, set tobuy to 0.

Utilities
"""

def argmaxall(gen):
    """gen is a generator of (element,value) pairs, where value is a real.
    argmaxall returns a list of all of the elements with maximal value.
    """
    maxv = -math.inf       # negative infinity
    maxvals = []      # list of maximal elements
    for (e,v) in gen:
        if v>maxv:
            maxvals,maxv = [e], v
        elif v==maxv:
            maxvals.append(e)
    return maxvals

def argmaxe(gen):
    """gen is a generator of (element,value) pairs, where value is a real.
    argmaxe returns an element with maximal value.
    If there are multiple elements with the max value, one is returned at random.
    """
    return random.choice(argmaxall(gen))

def argmax(lst):
    """returns maximum index in a list"""
    return argmaxe(enumerate(lst))

def argmaxd(dct):
   """returns the arg max of a dictionary dct"""
   return argmaxe(dct.items())

def flip(prob):
    """return true with probability prob"""
    return random.random() < prob

def select_from_dist(item_prob_dist):
  #{6:0.1, 5:0.1, 4:0.1, 3:0.3, 2:0.2, 1:0.2}
    """ returns a value from a distribution.
    item_prob_dist is an item:probability dictionary, where the
        probabilities sum to 1.
    returns an item chosen in proportion to its probability
    """
    ranreal = random.random()
    for (it,prob) in item_prob_dist.items():
        if ranreal < prob:
            return it
        else:
            ranreal -= prob
    raise RuntimeError(f"{item_prob_dist} is not a probability distribution")

"""Display Class"""

class Displayable(object):
    """Class that uses 'display'.
    The amount of detail is controlled by max_display_level
    """
    max_display_level = 1   # can be overridden in subclasses or instances

    def display(self,level,*args,**nargs):
        """print the arguments if level is less than or equal to the
        current max_display_level.
        level is an integer.
        the other arguments are whatever arguments print can take.
        """

        if level <= self.max_display_level:
            print(*args, **nargs)  ##if error you are using Python2 not Python3

class Plot_history(object):
    """Set up the plot for history of price and number in stock"""
    def __init__(self, ag, env):
        self.ag = ag
        self.env = env
        plt.ion()
        plt.xlabel("Time")
        plt.ylabel("Value")


    def plot_env_hist(self):
        """plot history of price and instock"""
        num = len(env.stock_history)
        plt.plot(range(num),env.price_history,label="Price")
        plt.plot(range(num),env.stock_history,label="In stock")
        plt.legend()
        #plt.draw()

    def plot_agent_hist(self):
        """plot history of buying"""
        num = len(ag.buy_history)
        plt.bar(range(1,num+1), ag.buy_history, label="Bought")
        plt.legend()
        #plt.draw()

"""Agent Conntroller"""

#from display import Displayable

class Agent(Displayable):

    def initial_action(self, percept):
        """return the initial action."""
        return self.select_action(percept)   # same as select_action

    def select_action(self, percept):
        """return the next action (and update internal state) given percept
        percept is variable:value dictionary
        """
        raise NotImplementedError("go")   # abstract method

"""Environment"""

class Environment(Displayable):
    def initial_percept(self):
        """returns the initial percept for the agent"""
        raise NotImplementedError("initial_percept")   # abstract method

    def do(self, action):
        """does the action in the environment
        returns the next percept """
        raise NotImplementedError("Environment.do")   # abstract method

"""Simulate"""

class Simulate(Displayable):
    """simulate the interaction between the agent and the environment
    for n time steps.
    Returns a pair of the agent state and the environment state.
    """
    def __init__(self,agent, environment):
        self.agent = agent
        self.env = environment
        self.percept = self.env.initial_percept()
        self.percept_history = [self.percept]
        self.action_history = []

    def go(self, n):
        for i in range(n):
            action = self.agent.select_action(self.percept)
            print(f"i={i} action={action}")

            self.percept = self.env.do(action,i)
            print(f"      percept={self.percept}")

"""TP Env"""

class TP_env(Environment):
    price_delta = [0, 0, 0, 21, 0, 20, 0, -64, 0, 0, 23, 0, 0, 0, -35,
        0, 76, 0, -41, 0, 0, 0, 21, 0, 5, 0, 5, 0, 0, 0, 5, 0, -15, 0, 5,
       0, 5, 0, -115, 0, 115, 0, 5, 0, -15, 0, 5, 0, 5, 0, 0, 0, 5, 0,
       -59, 0, 44, 0, 5, 0, 5, 0, 0, 0, 5, 0, -65, 50, 0, 5, 0, 5, 0, 0,
       0, 5, 0]
    sd = 5  # noise standard deviation

    def __init__(self):
        """paper buying agent"""
        self.time=0
        self.stock=30
        self.stock_history = []  # memory of the stock history
        self.price_history = []  # memory of the price history

    def initial_percept(self):
        """return initial percept"""
        self.stock_history.append(self.stock)
        self.price = round(234+self.sd*random.gauss(0,1))
        self.price_history.append(self.price)
        #print(f"Initial price: {self.price} ,instock: {self.stock}")
        return {'price': self.price,
                'instock': self.stock}

    def do(self, action, time_unit):
        """does action (buy) and returns percept consisting of price and instock"""
        used = select_from_dist({6:0.1, 5:0.1, 4:0.1, 3:0.3, 2:0.2, 1:0.2})
        print(f"i={time_unit} used={used}")
        # used = select_from_dist({7:0.1, 6:0.2, 5:0.2, 4:0.3, 3:0.1, 2:0.1}) # uses more paper
        bought = action['buy']
        self.stock = self.stock+bought-used
        self.stock_history.append(self.stock)
        self.time += 1
        self.price =  round(self.price
                        + self.price_delta[self.time%len(self.price_delta)] # repeating pattern
                        + self.sd*random.gauss(0,1)) # plus randomness
        self.price_history.append(self.price)
        return {'price': self.price,
                'instock': self.stock}

class TP_agent(Agent):
    def __init__(self):
        self.spent = 0
        percept = env.initial_percept()
        self.ave = self.last_price = percept['price']
        self.instock = percept['instock']
        self.buy_history = []

    def select_action(self, percept):
        """return next action to carry out
        """
        self.last_price = percept['price']
        self.ave = self.ave+(self.last_price-self.ave)*0.05
        self.instock = percept['instock']
        if self.last_price < 0.7*self.ave and self.instock < 30:
            tobuy = 15
        elif self.instock < 10:
            tobuy = 5
        else:
            tobuy = 0
        self.spent += tobuy*self.last_price
        self.buy_history.append(tobuy)
        #print(f"agent buy:{tobuy}")
        return {'buy': tobuy}

env = TP_env()
ag = TP_agent()
sim = Simulate(ag,env)
sim.go(n=5)
ag.spent/env.time

sim.go(50);

sim.go(100);
print(f"agent spent ${ag.spent/100}")
pl = Plot_history(ag,env); pl.plot_env_hist(); pl.plot_agent_hist()

