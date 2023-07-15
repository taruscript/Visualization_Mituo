import numpy as np
import matplotlib.pyplot as plt
import imageio
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
import os

def circle_points(r, n, center=(0, 0)):
    angles = np.linspace(0, 2*np.pi, n+1)[:-1]
    return np.array([r*np.cos(angles), r*np.sin(angles)]).T + center

class StaticAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

class CircleModel(Model):
    def __init__(self, N, width, height, radius):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)

        # Create agents
        positions = circle_points(radius, N, center=(width/2, height/2))
        for i in range(self.num_agents):
            a = StaticAgent(i, self, positions[i])
            self.schedule.add(a)
            self.space.place_agent(a, positions[i])

    def step(self):
        self.schedule.step()

def plot_agents(model, step, connection):
    fig, ax = plt.subplots()
    for agent in model.schedule.agents:
        x, y = agent.pos
        ax.scatter(x, y)
    agent_a, agent_b = connection
    agent_a = next(a for a in model.schedule.agents if a.unique_id == agent_a)
    agent_b = next(a for a in model.schedule.agents if a.unique_id == agent_b)
    ax.plot([agent_a.pos[0], agent_b.pos[0]], [agent_a.pos[1], agent_b.pos[1]], 'k-')

    # Add text near the 'After' agent's position based on the step number
    if step == 1:
        ax.text(agent_b.pos[0], agent_b.pos[1], 'Sec!', fontsize=12, ha='right')
    elif step == 2:
        ax.text(agent_b.pos[0], agent_b.pos[1], 'Hack!', fontsize=12, ha='right')
    elif step == 3:
        # ax.text(agent_b.pos[0]-0.2, agent_b.pos[1]-0.2, '365!', fontsize=12, ha='right')
        prev_agent = model.schedule.agents[(agent_b.unique_id - 1) % len(model.schedule.agents)]
        next_agent = model.schedule.agents[(agent_b.unique_id + 1) % len(model.schedule.agents)]
        ax.text(prev_agent.pos[0]-0.2, prev_agent.pos[1]-0.2, '365!', fontsize=12, ha='right')
        ax.text(next_agent.pos[0]-0.2, next_agent.pos[1]-0.2, '365!', fontsize=12, ha='right')


    ax.set_xlim(0, model.space.x_max)
    ax.set_ylim(0, model.space.y_max)
    plt.savefig(f'image/agents_{step}.png')
    plt.close(fig)



class Step():
    def __init__(self):
        self.model = CircleModel(5, 10, 10, 3)
    
    def exec(self, connection, stepNum):
        plot_agents(self.model, stepNum, connection)
        self.model.step()



def convertToGif():

    # Count the number of files in the directory
    saved_files_num = len([f for f in os.listdir("image") if os.path.isfile(os.path.join("image", f)) and f.endswith('.png')])
    images = []
    for i in range(saved_files_num):
        images.append(imageio.imread(f'image/agents_{i + 1}.png'))
    imageio.mimsave('agents.gif', images)
