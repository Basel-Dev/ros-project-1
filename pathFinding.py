
import heapq

grid_size = (100,100)
obstacles = set()

def add_horizontal_obstacle(x1, x2, y):
    obstacles.update([(x, y) for x in range(x1, x2 + 1)])

def add_vertical_obstacle(x, y1, y2):
    obstacles.update([(x, y) for y in range(y1, y2 + 1)])

def add_rectangle_obstacle(x1, x2, y1, y2):
    obstacles.update([(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)])

def clearObstacles():
    obstacles.clear()

def getObstacles():
    return obstacles

# obstacles.update(add_horizontal_obstacle(2, 5, 3))
# obstacles.update(add_rectangle_obstacle(4,6,3,4))
# obstacles.update(add_vertical_obstacle(1,2,5))
# obstacles.update(add_horizontal_obstacle(1,4,6))



def get_neighbors(current, grid_size, obstacles):
    neighbors = []
    x = current[0]
    y = current[1]
    width = grid_size[0]
    height = grid_size[1]

    if x+1 < width and (x+1,y) not in obstacles:
        neighbors.append((x+1,y))
    if x-1 >= 0 and (x-1,y) not in obstacles:
        neighbors.append((x-1,y))
    if y+1 < height and (x,y+1) not in obstacles:
        neighbors.append((x,y+1))
    if y-1 >= 0 and (x,y-1) not in obstacles:
        neighbors.append((x,y-1))

    return neighbors


def node_distance(node, goal):
    return abs(goal[0]-node[0]) + abs(goal[1]-node[1])


def find_path(start, goal):
    my_queue = []  
    came_from = {}
    path = []
    steps = 0
    total_distance = 0
    visited = set()

    heapq.heappush(my_queue, (0, start))

    while my_queue:
        f, current = heapq.heappop(my_queue)

        if current == goal:
            break

        if current in visited:
            continue

        visited.add(current)

        neighbors = get_neighbors(current, grid_size, obstacles)
        steps += 1

        for i in neighbors:
            if i not in visited:
                remaining_distance = node_distance(i, goal)
                total_distance = steps + remaining_distance

                heapq.heappush(my_queue, (total_distance, i))
                if i not in came_from:
                    came_from[i] = current
            
            
        
    while current in came_from:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()
    return path

##print(find_path((0,0),(3,4)))

        

    
    
    
