#! /usr/bin/env python3

# imports
import numpy as np

# create the empty room
def create_room(size = 10):
    room = np.zeros((size, size))

    # walls
    for i in range(size):
        room[i][0] = 2
        room[i][size-1] = 2
        room[0][i] = 2
        room[size-1][i] = 2
    
    return room

# filling the room
def fill_room(room, fraction=0.5):
    # fraction of the room to be filled
    num_replaced = int(fraction*room.shape[0]*room.shape[1])

    # Random (x, y) coordinates
    indices_x = np.random.randint(1, room.shape[0]-1, num_replaced)
    indices_y = np.random.randint(1, room.shape[1]-1, num_replaced)

    room[indices_x, indices_y] = 1
    
    return room

# create initial robots
def create_robots(number_of_robots = 10):
    robots = []
    
    for n in range(number_of_robots):
        robots.append(np.random.randint(7, size=3**5))
        
    return robots

# generate new robots
def update_robots(robots, scores, mutation = 0.2):
    # sort the robots according to score and steps, score = score + steps left to max
    sorted_index = np.argsort(scores)

    robots_to_pick = int(len(robots)/2)
    
    tmp = []
    # first half have the best scores
    for best in sorted_index[robots_to_pick:]:
        tmp.append(robots[best])

    # the other half, take from previous set, randomly changing 20% of the array
    for best in sorted_index[robots_to_pick:]:
        new_genes = np.random.randint(0, len(robots[best]), int(mutation*len(robots[best])))

        robots[best][new_genes] = np.random.randint(7, size=1)[0]
        
        tmp.append(robots[best])

    return tmp[:len(robots)]

# simulation
def simulation(room, robots, steps = 100):
    # fill the room with cans in random positions, filling a given amount of positions
    room = fill_room(room)

    scores = []

    for r in range(len(robots)):
        # start the robot at position 0,0
        x = 10
        y = 10
        score = 0

        # loop of 200 steps, stop if score = 500
        for s in range(steps+1):
            # in the loop, the informations of the environment "up, down, left, right and middle"
            # combined with the possible values "empty = 0, can = 1, wall = 2" returns a number
            # this number is the index of the array of actions

            # from the position, get the index of action
            # up, down, left, right and middle
            action = int(room[x][y+1]*3**4 + room[x][y-1]*3**3 + room[x-1][y]*3**2 + room[x+1][y]*3**1 + room[x][y])

            # create a random array of actions for each robot, 6 possible values each positino
            # 0 = do nothing
            if robots[r][action] == 0:
                continue

            # 1 = go left
            elif robots[r][action] == 1:
                if room[x-1][y] == 2:
                    score -= 5
                else:
                    x -= 1

            # 2 = go right
            elif robots[r][action] == 2:
                if room[x+1][y] == 2:
                    score += 5
                else:
                    x += 1

            # 3 = go up
            elif robots[r][action] == 3:
                if room[x][y+1] == 2:
                    score -= 5
                else:
                    y += 1

            # 4 = go down
            elif robots[r][action] == 4:
                if room[x][y-1] == 2:
                    score -= 5
                else:
                    y -= 1

            # 5 = go random direction
            elif robots[r][action] == 5:
                move_x = np.random.randint(-1, 2, size=1)[0]
                move_y = np.random.randint(-1, 2, size=1)[0]

                if room[x+move_x][y+move_y] == 2:
                    score -= 5
                else:
                    x += move_x
                    y += move_y

            # 6 = try take can
            elif robots[r][action] == 6:
                if room[x][y] == 1:
                    room[x][y] = 0
                    score += 10
                else:
                    score -= 1

            if score > 500:
                break

        scores.append(score+10*(steps-s))
    
    # return scores and steps
    return scores

# optimization

# create the room
room = create_room(20)

# create a random array of actions for each robot
robots = create_robots(50)

scores = np.zeros(len(robots))

generations = 1000
average = 100

for g in range(generations):
    # take average of scores
    for i in range(average):
        # passa actions array to the simulation
        scores += simulation(room, robots)
        scores /= average
    if g % 10 == 0:
        print(sum(scores)/len(scores))
        print(sorted(scores[-5:]))

    # produce new generation
    robots = update_robots(robots, scores, 0.5)

# run the simulation again for some amount of generations