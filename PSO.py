import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Define the landscape (a 2D Gaussian hill)
def landscape(x, y):
    return np.exp(-(x ** 2 + y ** 2))


# Define Particle class
class Particle:
    def __init__(self):
        self.position = np.array([np.random.uniform(-2, 2), np.random.uniform(-2, 2)])
        self.velocity = np.array([np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5)])
        self.best_position = np.copy(self.position)
        self.best_score = landscape(self.position[0], self.position[1])


# Create PSO algorithm
def PSO(num_particles, num_iterations, alpha=0.5, beta=1.5, gamma=1.5):
    particles = [Particle() for _ in range(num_particles)]
    g_best_position = np.random.uniform(-2, 2, 2)
    g_best_score = landscape(g_best_position[0], g_best_position[1])

    history = []  # to store positions for visualization

    for _ in range(num_iterations):
        for particle in particles:
            # Update personal best
            score = landscape(particle.position[0], particle.position[1])
            if score > particle.best_score:
                particle.best_score = score
                particle.best_position = np.copy(particle.position)

            # Update global best
            if score > g_best_score:
                g_best_score = score
                g_best_position = np.copy(particle.position)

        for particle in particles:
            inertia = alpha * particle.velocity
            personal_attraction = beta * np.random.random() * (particle.best_position - particle.position)
            global_attraction = gamma * np.random.random() * (g_best_position - particle.position)

            # Update velocity and position
            particle.velocity = inertia + personal_attraction + global_attraction
            particle.position += particle.velocity

        history.append([np.copy(particle.position) for particle in particles])

    return history


# Visualization
history = PSO(num_particles=5, num_iterations=50)

x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)
Z = landscape(X, Y)

fig, ax = plt.subplots()
CS = ax.contourf(X, Y, Z, 20, cmap='inferno')
particles, = plt.plot([], [], 'ro', markersize=10)

# For storing particle numbers
particle_numbers = [ax.text(0, 0, str(i)) for i in range(len(history[0]))]


def init():
    particles.set_data([], [])
    for number in particle_numbers:
        number.set_position((0, 0))
        number.set_visible(False)
    return particles, particle_numbers


def animate(i):
    positions = np.array(history[i])
    particles.set_data(positions[:, 0], positions[:, 1])

    # Update position of particle numbers
    for j, number in enumerate(particle_numbers):
        number.set_position(positions[j] + 0.1)  # offset for better visibility
        number.set_visible(True)
    return particles, particle_numbers


ani = FuncAnimation(fig, animate, frames=len(history), init_func=init, blit=False)
plt.title('Particle Swarm Optimization on 2D Hill')
plt.colorbar(CS)
plt.show()

ani.save('PSO_animation.gif', writer='imagemagick', fps=3)
