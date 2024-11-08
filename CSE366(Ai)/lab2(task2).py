# -*- coding: utf-8 -*-
"""lab2(task2).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rGzieT9nfVVfIhZGDfxP9IGx6IEb_BU4

# **Task 2**

# Trading Agent for Smartphone Inventory Management:

**Percepts**:

The agent receives two percepts:

* **Price:** The current price of a specific smartphone model.
* **Amount in Stock:** The quantity of that smartphone model available in the store.

**Decision Process:**

* The agent’s goal is to optimize stock levels while minimizing costs.
* It must decide whether to order more smartphones and, if so, how many to order.

**Decision Rules:**
* If the price of the smartphone drops significantly (indicating a deal or promotion), the agent considers ordering more units.

**Threshold:** Let’s say the threshold is a 20% discount from the average price.

* If the amount in stock falls below a certain level (e.g., 10 units), the agent prioritizes restocking.
* Otherwise, the agent decides not to place an order.

**Actions:**

* If the smartphone price is below the threshold (20% discount) and the stock level is not critically low, the agent orders a specific quantity (let’s call it tobuy).


> **Example:** If the smartphone price drops to 500 BDT (from an average of 600 BDT) and there are 20 units in stock, the agent might decide to order 15 more units.


* If the stock level is critically low (e.g., less than 10), the agent orders a minimum quantity (e.g., 10 units).
* Otherwise, if neither condition is met, the agent does not place an order (i.e., tobuy = 0).

**Submition**
* Submit the code in python file .py not .ipynb.
* The code should behave like the above and generate a graph as shown in example.
"""

import random
import math
import matplotlib.pyplot as plt

"""Utilities"""

def argmaxall(gen):
    """gen is a generator of (element, value) pairs, where value is a real.
    argmaxall returns a list of all of the elements with maximal value.
    """
    maxv = -math.inf
    maxvals = []
    for (e, v) in gen:
        if v > maxv:
            maxvals, maxv = [e], v
        elif v == maxv:
            maxvals.append(e)
    return maxvals

def argmaxe(gen):
    """gen is a generator of (element, value) pairs, where value is a real.
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
    """ returns a value from a distribution.
    item_prob_dist is an item:probability dictionary, where the
        probabilities sum to 1.
    returns an item chosen in proportion to its probability
    """
    ranreal = random.random()
    for (it, prob) in item_prob_dist.items():
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
    max_display_level = 1  # can be overridden in subclasses or instances

    def display(self, level, *args, **nargs):
        """print the arguments if level is less than or equal to the
        current max_display_level.
        level is an integer.
        the other arguments are whatever arguments print can take.
        """
        if level <= self.max_display_level:
            print(*args, **nargs)

# Plot history class
class Plot_history(object):
    """Set up the plot for history of price and number in stock"""
    def __init__(self, ag, env):
        self.ag = ag
        self.env = env
        plt.ion()
        plt.xlabel("Time")
        plt.ylabel("Value")

    def plot_env_hist(self):
        """plot history of price and in stock"""
        num = len(self.env.stock_history)
        plt.plot(range(num), self.env.price_history, label="Price")
        plt.plot(range(num), self.env.stock_history, label="In stock")
        plt.legend()
        plt.show()

    def plot_agent_hist(self):
        """plot history of buying"""
        num = len(self.ag.buy_history)
        plt.bar(range(1, num + 1), self.ag.buy_history, label="Bought")
        plt.legend()
        plt.show()

"""Agent Conntroller"""

class Agent(Displayable):
    def initial_action(self, percept):
        """return the initial action."""
        return self.select_action(percept)

    def select_action(self, percept):
        """return the next action (and update internal state) given percept
        percept is variable:value dictionary
        """
        raise NotImplementedError("select_action")  # abstract method

"""Environment"""

class Environment(Displayable):
    def initial_percept(self):
        """returns the initial percept for the agent"""
        raise NotImplementedError("initial_percept")  # abstract method

    def do(self, action):
        """does the action in the environment
        returns the next percept """
        raise NotImplementedError("do")  # abstract method

"""Simulate"""

class Simulate(Displayable):
    """simulate the interaction between the agent and the environment
    for n time steps.
    Returns a pair of the agent state and the environment state.
    """
    def __init__(self, agent, environment):
        self.agent = agent
        self.env = environment
        self.percept = self.env.initial_percept()
        self.percept_history = [self.percept]
        self.action_history = []

    def go(self, n):
        for i in range(n):
            action = self.agent.select_action(self.percept)
            print(f"i={i} action={action}")

            self.percept = self.env.do(action, i)
            self.percept_history.append(self.percept)
            self.action_history.append(action)
            print(f"      percept={self.percept}")

"""TP Env"""

class SP_env(Environment):
    price_delta = [0, 0, 0, 21, 0, 20, 0, -64, 0, 0, 23, 0, 0, 0, -35,
                   0, 76, 0, -41, 0, 0, 0, 21, 0, 5, 0, 5, 0, 0, 0, 5, 0, -15, 0, 5,
                   0, 5, 0, -115, 0, 115, 0, 5, 0, -15, 0, 5, 0, 5, 0, 0, 0, 5, 0,
                   -59, 0, 44, 0, 5, 0, 5, 0, 0, 0, 5, 0, -65, 50, 0, 5, 0, 5, 0, 0,
                   0, 5, 0]
    sd = 5  # noise standard deviation

    def __init__(self):
        """smartphone buying agent"""
        self.time = 0
        self.stock = 20
        self.stock_history = []  # memory of the stock history
        self.price_history = []  # memory of the price history

    def initial_percept(self):
        """return initial percept"""
        self.stock_history.append(self.stock)
        self.price = round(600 + self.sd * random.gauss(0, 1))
        self.price_history.append(self.price)
        return {'price': self.price, 'instock': self.stock}

    def do(self, action, time_unit):
        """does action (buy) and returns percept consisting of price and instock"""
        used = select_from_dist({6: 0.1, 5: 0.1, 4: 0.1, 3: 0.3, 2: 0.2, 1: 0.2})
        print(f"i={time_unit} used={used}")
        bought = action['buy']
        self.stock = self.stock + bought - used
        self.stock_history.append(self.stock)
        self.time += 1
        self.price = round(self.price
                           + self.price_delta[self.time % len(self.price_delta)]  # repeating pattern
                           + self.sd * random.gauss(0, 1))  # plus randomness
        self.price_history.append(self.price)
        return {'price': self.price, 'instock': self.stock}

class SP_agent(Agent):
    def __init__(self):
        self.spent = 0
        percept = env.initial_percept()
        self.ave = self.last_price = percept['price']
        self.instock = percept['instock']
        self.buy_history = []

    def select_action(self, percept):
        """return next action to carry out"""
        self.last_price = percept['price']
        self.ave = self.ave + (self.last_price - self.ave) * 0.05
        self.instock = percept['instock']
        tobuy = 0
        if self.last_price < 0.8 * self.ave and self.instock < 60:
            tobuy = 15
        elif self.instock < 10:
            tobuy = 10
        self.spent += tobuy * self.last_price
        self.buy_history.append(tobuy)
        return {'buy': tobuy}

env = SP_env()
ag = SP_agent()
sim = Simulate(ag, env)

sim.go(100);

print(f"agent spent ${ag.spent/100}")

pl = Plot_history(ag, env)
pl.plot_env_hist()
pl.plot_agent_hist()