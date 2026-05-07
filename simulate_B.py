import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import pathFinding
from drone import Drone, DroneStatus

class UIDrone(Drone):
    def __init__(self, ax, drone_id, max_weight):
        super().__init__(drone_id, max_weight)
        droneMarker = ax.scatter([], [], c="red", marker="o", zorder=10)
        droneLabel = ax.text(0, -.4, drone_id, ha="center", va="top", zorder=10)

        self.point = (droneMarker, droneLabel)

class Path:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.pathList = pathFinding.find_path(start, goal)

    def getReversePath(self):
        return Path(self.goal, self.start)


def drawPath(ax, path, placeMarker=True):
    xPoints = [x for [x, y] in path]
    yPoints = [y for [x, y] in path]

    (goalX, goalY) = path[-1]
    ax.plot(xPoints, yPoints, color="tab:blue")
    if placeMarker:
        ax.plot([goalX], [goalY], "g^", zorder=9)


def drawObstacleGrid(ax, cmap, obstacles):
    grid = np.zeros((100, 100))

    for (x, y) in obstacles:
        grid[49-y][x+50] = 1

    ax.imshow(grid, cmap=cmap, extent=[-50.5, 49.5, -50.5, 49.5])


def interpolatePath(drone, state, path, subdivisionsPerPoint):
    denseSampleArray = []
    interpolationArray = np.linspace(0, 1, subdivisionsPerPoint)

    for step, point in enumerate(path):
        if step+1 < len(path):
            npPoint = np.array(point)
            npNextPoint = np.array(path[step+1])
            ##drone.battery -= mission.battery_use(1, package.weight)

            for t in interpolationArray:
                sample = npPoint * (1-t) + npNextPoint * t
                denseSampleArray.append((sample.tolist(), drone.battery, state))

    return denseSampleArray

def getFinalInterpolatedSequence(drone, path, subdivisionsPerPoint, totalTime, pauseTime):
    firstRunArray = interpolatePath(drone, DroneStatus.DELIVERING, path, subdivisionsPerPoint)
    returnBackArray = interpolatePath(drone, DroneStatus.RETURNING, path[::-1], subdivisionsPerPoint)

    interval = (totalTime * 1000) / (2 * len(firstRunArray))
    pauseFrames = int((pauseTime * 1000) / interval)

    pausePosition, pauseBattery, s = firstRunArray[len(firstRunArray)-1]

    pauseArray = [(pausePosition, pauseBattery, DroneStatus.IDLE) for x in range(pauseFrames)]

    return (firstRunArray + pauseArray + returnBackArray, interval)


def executePathwalk(fig, ax, drone, package, path, totalTime, pauseTime):
    drawPath(ax, path)
    drawPath(ax, path[::-1], False)
    subdivisions = 10
    
    sampleArray, interval = getFinalInterpolatedSequence(drone, path, subdivisions, totalTime, pauseTime)
    
    def animate(i, drone, sampleArray):
        marker, label = drone.point
        
        sample, battery, state = sampleArray[i]
        x, y = sample

        marker.set_offsets([x, y])
        label.set_position((x, y-.4))

        return [marker, label]

    anim = FuncAnimation(fig, 
                         animate, 
                         fargs=(drone, sampleArray), 
                         frames=len(sampleArray), 
                         interval=interval, 
                         repeat=False,
                         blit=True)
    return anim

TIME_RUNNING = 4
PAUSE_TIME = 0.2

def simulateDrone(drone, package, path):
    fig, ax = plt.subplots(layout="constrained", figsize=(8, 8))
    manager = plt.get_current_fig_manager()

    limitNum = 10
    limitRange = [x for x in range(-limitNum, limitNum+1)]

    cmap = ListedColormap([(0, 0, 0, 0), (0.5, 0.5, 0.5, 1)])

    ax.grid()
    ax.set_aspect("equal")
    ax.set_xlim(-limitNum, limitNum)
    ax.set_ylim(-limitNum, limitNum)
    ax.set_xticks(limitRange)
    ax.set_yticks(limitRange)

    manager.window.geometry("800x800+900+120")

    ax.scatter([0], [0], marker="*", c="#FFD700", s=100, zorder=9)

    drawObstacleGrid(ax, cmap, pathFinding.obstacles)
    uiDrone = UIDrone(ax, drone.drone_id, drone.max_weight)
    uiDrone.battery = drone.battery
    uiPath = path
    anim = executePathwalk(fig, ax, uiDrone, package, uiPath, TIME_RUNNING, PAUSE_TIME)
    plt.show()


# pathFinding.obstacles.update(pathFinding.add_horizontal_obstacle(0,5,3))
##simulateDrone(Drone("D1", 10), examplePackage, (0, 0), (2, 4))