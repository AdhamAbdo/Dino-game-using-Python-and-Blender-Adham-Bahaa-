import tkinter as tk
import winsound

root = tk.Tk()
root.title("Chrome Dino Game")

canvas = tk.Canvas(root, width=800, height=400, bg='white')
canvas.pack()

# Load images with reduced dimensions
dino_img = tk.PhotoImage(file='dino.png').subsample(4)  # Adjust subsample factor as needed
cactus_img = tk.PhotoImage(file='cactus.png').subsample(8)  # Adjust subsample factor as needed (smaller)

# Resize the cactus image and create the cactus on the canvas
cactus_resized = cactus_img.subsample(2)  # Adjust the subsample factor to resize the image further
cactus = canvas.create_image(100, 363, anchor=tk.NW, image=cactus_resized)  # Adjust initial cactus position
cactus_rect = canvas.create_rectangle(100, 363, 100 + cactus_resized.width(), 363 + cactus_resized.height(), outline='white')

# Draw the dino on the canvas with white rectangles around them
dino = canvas.create_image(100, 300, anchor=tk.NW, image=dino_img)
dino_rect = canvas.create_rectangle(100, 300, 100 + dino_img.width(), 300 + dino_img.height(), outline='white')

# Initialize variables
score = 0
is_jumping = False
game_over = False

# Score label
score_label = tk.Label(root, text=f"Score: {score}")
score_label.pack()

# Function to handle jump
def jump(event):
    global is_jumping, score
    if not is_jumping and not game_over:
        is_jumping = True
        score += 1  # Increase score by one when the dino jumps
        score_label.config(text=f"Score: {score}")
        jump_up()

def jump_up():
    global is_jumping
    for _ in range(10):  # Adjust the number of steps for a smoother jump
        canvas.move(dino, 0, -30)  # Adjust the jump distance
        canvas.move(dino_rect, 0, -30)
        check_collision()
        root.update()
        winsound.PlaySound('jumpp.wav', winsound.SND_ASYNC)  # Play the 'jump.wav' sound asynchronously
        root.after(35)
    jump_down()

def jump_down():
    global is_jumping
    for _ in range(10):  # Same number of steps for descent
        canvas.move(dino, 0, 30)
        canvas.move(dino_rect, 0, 30)
        check_collision()
        root.update()
        root.after(35)
    is_jumping = False

# Function to move the cactus and update score
def move_cactus():
    global game_over
    canvas.move(cactus, -35, 0)  # Adjust the speed of cactus movement by changing the value (-5 in this case)
    canvas.move(cactus_rect, -35, 0)
    cactus_coords = canvas.coords(cactus)
    if cactus_coords[0] + cactus_img.width() < 0:  # Check if the cactus has moved completely off the left side
        canvas.move(cactus, 800 + cactus_img.width(), 0)  # Move cactus to the right side
        canvas.move(cactus_rect, 800 + cactus_img.width(), 0)
        if not jumpcheck:
            score -= 1
            score_label.config(text=f"Score: {score}")
    if not game_over:
        root.after(30, move_cactus)  # Adjust the delay for smoother movement

# Function to check collision
def check_collision():
    dino_coords = canvas.coords(dino)
    cactus_coords = canvas.coords(cactus)
    
    dino_left = dino_coords[0]
    dino_right = dino_coords[0] + dino_img.width()
    dino_top = dino_coords[1]
    dino_bottom = dino_coords[1] + dino_img.height()
    
    cactus_left = cactus_coords[0]
    cactus_right = cactus_coords[0] + cactus_img.width()
    cactus_top = cactus_coords[1]
    cactus_bottom = cactus_coords[1] + cactus_img.height()
    
    if (dino_left < cactus_right and
            dino_right > cactus_left and
            dino_top < cactus_bottom and
            dino_bottom > cactus_top):
        end_game()

# Function to end the game
def end_game():
    global game_over
    game_over = True
    canvas.create_text(400, 200, text=f"Game Over! Score: {score}", font=('Helvetica', 24), fill='red')

# Bind spacebar to jump action
root.bind('<space>', jump)

# Start moving the cactus
move_cactus()

root.mainloop()