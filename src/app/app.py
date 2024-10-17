import pygame
import numpy as np
import sys
import json
import os
from bezier import bezier_curve
pygame.init()
pygame.font.init()

font_size = 32
font = pygame.font.Font(None, font_size)
text_position_x = 300 
spacing = 100

width, height = 1000, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bezier Draw")
panel_width = 100

# Colors
white = (255, 255, 255)
blue = (0, 148, 255)
grey = (200, 200, 200)
black = (0, 0, 0)

# Loading menu icons

sourceFileDir = os.path.dirname(os.path.abspath(__file__))

add_icon_path = os.path.join(sourceFileDir, '../assets/icons/add_button_unclicked.png')
add_icon_active_path = os.path.join(sourceFileDir, '../assets/icons/add_button_clicked.png')
move_icon_path = os.path.join(sourceFileDir, '../assets/icons/move_button_unclicked.png')
move_icon_active_path = os.path.join(sourceFileDir, '../assets/icons/move_button_clicked.png')
new_curve_icon_path = os.path.join(sourceFileDir, '../assets/icons/newcurve_button_unclicked.png')
new_curve_icon_active_path = os.path.join(sourceFileDir, '../assets/icons/add_button_unclicked.png')
delete_icon_path = os.path.join(sourceFileDir, '../assets/icons/delete_button_unclicked.png')
delete_icon_active_path = os.path.join(sourceFileDir, '../assets/icons/delete_button_clicked.png')
import_icon_path = os.path.join(sourceFileDir, '../assets/icons/import_button.png')
export_icon_path = os.path.join(sourceFileDir, '../assets/icons/export_button.png')
typing_icon_path = os.path.join(sourceFileDir, '../assets/icons/type_button.png')

add_icon = pygame.image.load(add_icon_path)
add_icon_active = pygame.image.load(add_icon_active_path)
move_icon = pygame.image.load(move_icon_path)
move_icon_active = pygame.image.load(move_icon_active_path)
new_curve_icon = pygame.image.load(new_curve_icon_path)
new_curve_icon_active = pygame.image.load(new_curve_icon_active_path)
delete_icon = pygame.image.load(delete_icon_path)
delete_icon_active = pygame.image.load(delete_icon_active_path)
import_icon = pygame.image.load(import_icon_path)
export_icon = pygame.image.load(export_icon_path)
typing_icon = pygame.image.load(typing_icon_path)

# Icon checker
current_add_icon = add_icon
current_move_icon = move_icon
current_new_curve_icon = new_curve_icon
current_delete_icon = delete_icon

# Constants for buttons
button_add = add_icon.get_rect(topleft=(10, 10))
button_move = move_icon.get_rect(topleft=(10, 100))
button_new_curve = new_curve_icon.get_rect(topleft=(10, 190))
button_delete_curve = delete_icon.get_rect(topleft = (10,280))
button_import = import_icon.get_rect(topleft = (10, 370))
button_export = export_icon.get_rect(topleft = (10, 460))
button_typing = typing_icon.get_rect(topleft = (10, 550))

mode = 'ADD' 
is_dialog_active = False
is_loading = False
is_typing = False
filename_to_load = ''
filename_to_save = ''
user_input = ''

# Bezier


# Point save and load functions
def save_control_points(points, filename):
    with open(filename, 'w') as file:
        json.dump(points, file)

def load_control_points(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def point_near_mouse(mouse_pos, point, threshold=10):
    return np.linalg.norm(np.array(mouse_pos) - np.array(point)) < threshold

def clear_control_points():
    global control_points_sets
    control_points_sets = [[] for _ in range(len(control_points_sets))]

# Function to draw given bezier curve control points set
def draw_bezier_curve(screen, points, offset=(0, 0), scale=1, color=black, width=2):
    if len(points) > 1:
        scaled_points = [(np.array(point) * scale + offset).astype(int) for point in points]
        curve_points = bezier_curve(scaled_points)
        pygame.draw.lines(screen, color, False, curve_points, width)
        

running = True
drawn_curves = []
control_points_sets = [[]]
current_curve = 0
selected_point = None
while running:
    if not is_typing:
        screen.fill(white)
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > panel_width:
                if mode == 'MOVE':
                    for curve_idx, control_points in enumerate(control_points_sets):
                        for point_idx, point in enumerate(control_points):
                            if point_near_mouse(event.pos, point):
                                current_curve = curve_idx 
                                selected_point = point_idx  
                                break
                        if selected_point is not None:
                            break  
                elif event.button == 3: 
                        for i, point in enumerate(control_points_sets[current_curve]):
                            if point_near_mouse(event.pos, point):
                                del control_points_sets[current_curve][i]
                                break    
                elif mode == 'ADD':
                    control_points_sets[current_curve].append(event.pos)
                elif mode == 'MOVE':
                    for i, point in enumerate(control_points_sets[current_curve]):
                        if point_near_mouse(event.pos, point):
                            selected_point = i
                            break
            elif button_add.collidepoint(mouse_pos):
                    mode = 'ADD'
                    current_add_icon = add_icon_active  
                    current_move_icon = move_icon
            elif button_move.collidepoint(mouse_pos):
                    mode = 'MOVE'
                    current_add_icon = add_icon
                    current_move_icon = move_icon_active    
            elif button_new_curve.collidepoint(mouse_pos):
                    control_points_sets.append([])  
                    current_curve = len(control_points_sets) - 1  
                    mode = 'ADD' 
                    current_add_icon = add_icon_active 
                    current_move_icon = move_icon
            elif button_delete_curve.collidepoint(mouse_pos):
                if len(control_points_sets) > 1 and current_curve < len(control_points_sets):
                    del control_points_sets[current_curve]
                    current_curve = max(0, current_curve - 1)
                elif len(control_points_sets) == 1:
                    control_points_sets[current_curve] = []
            elif button_export.collidepoint(mouse_pos):
                    is_saving = True
                    is_loading = False
                    is_dialog_active = True
                    filename_to_save = ''
            elif button_import.collidepoint(mouse_pos):
                is_saving = False
                is_loading = True
                is_dialog_active = True
                filename_to_save = ''
            
            elif button_typing.collidepoint(mouse_pos):
                is_typing = True
                print("Tryb pisania aktywowany") 
                text_position_x = 50
                drawn_curves = [] 

        elif event.type == pygame.MOUSEBUTTONUP:
            if mode == 'MOVE' and selected_point is not None and event.button == 3:
                del control_points_sets[current_curve][selected_point]
            selected_point = None
        elif event.type == pygame.MOUSEMOTION and selected_point is not None and mode == 'MOVE':
            control_points_sets[current_curve][selected_point] = event.pos
        
        elif is_dialog_active:
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_saving:
                        save_control_points(control_points_sets, user_input + ".json")
                    else:
                        control_points_sets = load_control_points(user_input + ".json")
                    is_dialog_active = False
                    user_input = ''
                    is_saving = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
    if is_typing:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and is_typing:
                if event.unicode:
                    print(f"Naciśnięto klawisz: {event.unicode}")
                    filename = f"{event.unicode}.json"
                    try:
                        with open(filename, 'r') as file:
                            points = json.load(file)
                            print(f"Wczytane punkty: {points}")
                            draw_bezier_curve(screen, points, offset=(0,0), scale=1)
                            drawn_curves.append((points, (text_position_x, height // 2), 0.5))
                            text_position_x += spacing
                    except FileNotFoundError:
                        print(f"Plik {filename} nie został znaleziony.")

    screen.fill(white)
    if is_dialog_active:
        input_box = pygame.Rect(100, 100, 200, 32)
        text_surface = font.render(user_input, True, black)
        pygame.draw.rect(screen, grey, input_box)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, black, input_box, 2)
    pygame.draw.rect(screen, (29,29,29), (0, 0, panel_width, height))
    if is_dialog_active:
        input_box = pygame.Rect(100, 100, 140, 32)
        text_surface = font.render(user_input, True, black)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, black, input_box, 2)
    


  # Bezier curves drawing 
    for idx, control_points in enumerate(control_points_sets):
        if len(control_points) > 1:
            curve_points = bezier_curve(control_points)
            pygame.draw.lines(screen, black, False, curve_points.astype(int), 2)
        for point in control_points:
            pygame.draw.circle(screen, blue if idx == current_curve else (200, 200, 200), point, 5)
    
    for curve_data in drawn_curves:
        points, offset, scale = curve_data
        draw_bezier_curve(screen, points, offset=offset, scale=scale)



    screen.blit(current_add_icon, button_add)
    screen.blit(current_move_icon, button_move)
    screen.blit(current_new_curve_icon, button_new_curve)
    screen.blit(current_delete_icon, button_delete_curve)
    screen.blit(export_icon, button_export)
    screen.blit(import_icon, button_import)
    screen.blit(typing_icon, button_typing)


    pygame.display.flip()

pygame.quit()
sys.exit()
