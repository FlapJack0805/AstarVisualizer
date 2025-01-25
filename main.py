import pygame
import time
import sys

def grid_maker(grid, screen):
    for posx in range(50):
        for posy in range(50):
            if grid[posx][posy] == 0:
                color = (255, 0, 0)  # Red for traversable squares
            elif grid[posx][posy] == 1:
                color = (0, 255, 0)  # Green for path
            elif grid[posx][posy] == 2:
                color = (0, 0, 0)    # Black for start and end points
            elif grid[posx][posy] == 3:
                color = (255, 255, 255) # White for boundaries
            elif grid[posx][posy] == 4:
                color = (0, 0, 255) # Blue for open set
    
            # Draw rectangle representing the grid cell
            rectangle = (posx * 10 + 10, posy * 10 + 10, 9.8, 9.8)
            pygame.draw.rect(screen, color, rectangle)
    # Update the display
    pygame.display.flip()

def coordinate_checker(x, y):
    return 0 <= x < 50 and 0 <= y < 50

def mouse_position(mousex, mousey, i, j):
    return mousex == i and mousey == j
    
def distance_between(start, end):
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5

def path_construction(current_node, cameFrom):
    path = [current_node]
    while current_node in cameFrom:
        current_node = cameFrom[current_node]
        path.append(current_node)
    return path[::-1]

def astar(start, end, grid, screen):
    open_set = []
    closed_set = []
    f_set = []
    g_map = [[float('inf') for _ in range(50)] for _ in range(50)]
    cameFrom = {}

    open_set.append(start)
    f_set.append(0)
    g_map[start[0]][start[1]] = 0

    changer = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        parent_index = f_set.index(min(f_set))
        current_node = open_set[parent_index]

        if current_node == end:
            return path_construction(current_node, cameFrom)

        open_set.pop(parent_index)
        closed_set.append(current_node)
        f_parent = f_set.pop(parent_index)
        g_parent = g_map[current_node[0]][current_node[1]]

        for change in changer:
            neighbor_node = (current_node[0] + change[0], current_node[1] + change[1])

            if not coordinate_checker(neighbor_node[0], neighbor_node[1]):
                continue

            if neighbor_node in closed_set or grid[neighbor_node[0]][neighbor_node[1]] == 3:
                continue

            neighbor_g = g_parent + distance_between(current_node, neighbor_node)

            if neighbor_node in open_set:
                index = open_set.index(neighbor_node)
                if g_map[neighbor_node[0]][neighbor_node[1]] <= neighbor_g:
                    continue

            open_set.append(neighbor_node)
            g_map[neighbor_node[0]][neighbor_node[1]] = neighbor_g
            f_set.append(neighbor_g + distance_between(neighbor_node, end))
            cameFrom[neighbor_node] = current_node

            grid[neighbor_node[0]][neighbor_node[1]] = 4  # Open set
            grid_maker(grid, screen)
            time.sleep(0.01)  # Control the speed of the visualization

    return None

def path_creater(path, grid):
    for pos in path:
        grid[pos[0]][pos[1]] = 1
    return

def main():
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Pathfinding Visualization")

    mouse_presses = 0
    mouse_dragging = False
    x1, y1, x2, y2 = None, None, None, None
    grid = [[0 for _ in range(50)] for _ in range(50)]
    b = False

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and mouse_presses < 2:
                mouse_pos = pygame.mouse.get_pos()
                mousex = mouse_pos[0] // 10 - 1
                mousey = mouse_pos[1] // 10 - 1
                if mouse_presses == 0:
                    x1 = mousex
                    y1 = mousey
                else:
                    x2 = mousex
                    y2 = mousey
                mouse_presses += 1

            if mouse_presses >= 2:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    b = True

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_dragging = True

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_dragging = False

                elif event.type == pygame.MOUSEMOTION and mouse_dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    mousex = mouse_pos[0] // 10 - 1
                    mousey = mouse_pos[1] // 10 - 1
                    if coordinate_checker(mousex, mousey):
                        grid[mousex][mousey] = 3

        if mouse_presses >= 1:
            grid[x1][y1] = 2

        if mouse_presses >= 2:
            grid[x2][y2] = 2
            start_point = (x1, y1)
            end_point = (x2, y2)

        if b:
            path = astar(start_point, end_point, grid, screen)
            if path:
                path_creater(path, grid)
            else:
                print("No possible paths found")
            b = False

        grid_maker(grid, screen)

    pygame.quit()

if __name__ == '__main__':
    main()

