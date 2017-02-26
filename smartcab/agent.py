import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.epslion = 0.8
        self.alpha = 0.8
        self.gamma = 0.2
        
        self.q = {}
        self.action_counts = 0.
        self.fall_count = 0.
        
    def getQ(self, state, action):

        return self.q.get((state, action), 0.0)
    
        
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.epslion = self.epslion * 0.9
        self.alpha = self.alpha * 0.95
        

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        #question2 :Inform the Driving Agent
        
        self.state = (inputs['light'],
                      inputs['oncoming'],
                      inputs['left'],
                      inputs['right'],
                      self.next_waypoint)
                      #,deadline)
            
        # TODO: Select action according to your policy
        #Implement a Basic Driving Agent
        #action = random.choice(self.env.valid_actions)
        
        #question3 :Implement a Q-Learning Driving Agent
        
        if random.random() < self.epslion :
            action = random.choice(self.env.valid_actions)
        else :
            q = [self.getQ(self.state, a) for a in self.env.valid_actions]

            maxQ = max(q)

            count = q.count(maxQ)

            if count > 1:

                best = [i for i in range(len(self.env.valid_actions)) if q[i] == maxQ]

                i = random.choice(best)

            else:

                i = q.index(maxQ)



            action = self.env.valid_actions[i]
            
            
        # Execute action and get reward
        reward = self.env.act(self, action)
        self.action_counts += 1
        if reward < 0:
            self.fall_count += 1
        print "The action counts is {} and the fall is {}".format(self.action_counts,self.fall_count)
        

        # TODO: Learn policy based on state, action, reward
        
        #get the next state
        new_inputs =  self.env.sense(self)
        new_state = ( new_inputs['light'],
                      new_inputs['oncoming'],
                      new_inputs['left'],
                      new_inputs['right'],
                      self.next_waypoint)
        #print "The old state is {}".format(self.state)
        #print "The new state is {}".format(new_state)
        
        maxqnew = max([self.getQ(new_state, a) for a in self.env.valid_actions])
        
        oldv = self.q.get((self.state, action), None)

        if oldv is None:

            self.q[(self.state, action)] = reward

        else:

            self.q[(self.state, action)] = oldv + self.alpha * (reward + self.gamma * maxqnew - oldv)

        

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=1, display= True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    #print "action_times = {}, action_fall = {}".format(action_times, action_fall)
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
