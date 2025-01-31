import pgzrun
import random
from pygame import Rect

WIDTH, HEIGHT = 700, 500
background = Actor("background", (WIDTH // 2, HEIGHT // 2))
TITLE = "Roguelike Adventure"
game_state = "menu"
time_left = 20
music.play("background_music")
music.set_volume(0.5)

class Hero:
    def __init__(self):
        self.images = ["hero_1", "hero_2", "hero_idle_1", "hero_idle_2"]
        self.index = 0
        self.sprite = Actor(self.images[self.index], (WIDTH // 2, HEIGHT // 2))
        self.speed = 5
        self.timer = 0
        self.idle_timer = 0
        self.moving = False
        self.health = 100
        self.shield_timer = 0 
        self.shield_active = True 
    def move(self):
        self.moving = False
        if keyboard.left and self.sprite.left > 0:
            self.sprite.x -= self.speed
            self.moving = True
        if keyboard.right and self.sprite.right < WIDTH:
            self.sprite.x += self.speed
            self.moving = True
        if keyboard.up and self.sprite.top > 0:
            self.sprite.y -= self.speed
            self.moving = True
        if keyboard.down and self.sprite.bottom < HEIGHT:
            self.sprite.y += self.speed
            self.moving = True
        if self.moving:
            self.idle_timer = 0
        else:
            self.idle_timer += 1
    def animate(self):
        self.timer += 1
        if self.moving:
            if self.timer % 10 == 0:
                self.index = (self.index + 1) % 2
                self.sprite.image = self.images[self.index]
        else:
            if self.timer % 30 == 0:
                self.index = 2 if self.index < 2 else 3
                self.sprite.image = self.images[self.index]
            if self.timer % 50 == 0:
                self.sprite.y += 1
            elif self.timer % 50 == 25:
                self.sprite.y -= 1
        if self.shield_active:
            self.shield_timer += 1
            if self.shield_timer > 90:
                self.shield_active = False
    def draw(self):
        self.sprite.draw()
        screen.draw.rect(Rect((10, 10), (self.health * 2, 20)), color="red")
        screen.draw.text("Health", (self.health * 2 + 15, 10), fontsize=20, color="red")
        if self.shield_active:
            screen.draw.rect(Rect((WIDTH - 150, 10), (100, 20)), color="blue")
            screen.draw.text("Shield", (WIDTH - 150 + 105, 10), fontsize=20, color="blue")

class Enemy:
    def __init__(self, x, y):
        self.images = ["enemy_1", "enemy_2", "enemy_idle_1", "enemy_idle_2"]
        self.index = 0
        self.sprite = Actor(self.images[self.index], (x, y))
        self.direction = random.choice(["horizontal", "vertical", "diagonal", "random"])
        self.speed = random.randint(3, 6)
        self.timer = 0
        self.health = 50
    def move(self):
        if self.direction == "horizontal":
            self.sprite.x += self.speed
            if self.sprite.right > WIDTH or self.sprite.left < 0:
                self.speed *= -1
        elif self.direction == "vertical":
            self.sprite.y += self.speed
            if self.sprite.bottom > HEIGHT or self.sprite.top < 0:
                self.speed *= -1
        elif self.direction == "diagonal":
            self.sprite.x += self.speed
            self.sprite.y += self.speed
            if self.sprite.right > WIDTH or self.sprite.left < 0 or self.sprite.bottom > HEIGHT or self.sprite.top < 0:
                self.speed *= -1
        elif self.direction == "random":
            move_direction = random.choice(["up", "down", "left", "right"])
            if move_direction == "up":
                self.sprite.y -= self.speed
            elif move_direction == "down":
                self.sprite.y += self.speed
            elif move_direction == "left":
                self.sprite.x -= self.speed
            elif move_direction == "right":
                self.sprite.x += self.speed
    def animate(self):
        self.timer += 1
        if self.timer % 15 == 0:
            self.index = (self.index + 1) % 2
            self.sprite.image = self.images[self.index]
    def draw(self):
        self.sprite.draw()
hero = Hero()
enemies = [Enemy(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(5)]

class Button(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.original_pos = pos  # Store original position

    def is_clicked(self, pos):
        # Use the button's rect for collision detection
        return self.colliderect(Rect(pos, (1, 1)))  # Create a 1x1 rect at mouse position

    def move_to_center(self):
        self.x = self.original_pos[0]
        self.y = self.original_pos[1]


start_button = Button("start_button", (WIDTH // 2, HEIGHT // 2 - 50))
start_button.move_to_center()
quit_button = Button("quit_button", (WIDTH // 2, HEIGHT // 2 + 50))
quit_button.move_to_center()
restart_button = Button("restart_button", (WIDTH // 2, HEIGHT // 2 - 50)) 
restart_button.move_to_center()
music_button = Button("music_on", (WIDTH // 2, HEIGHT // 2 + 150)) 
music_playing = True  

def draw_menu():
    screen.clear()
    background.draw()
    screen.draw.text("Roguelike Games", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="white")
    start_button.draw()
    music_button.draw()
    quit_button.draw()
    

def draw_game_over():
    screen.clear()
    background.draw()
    screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="red")
    restart_button.draw()
    music_button.draw()
    quit_button.draw()

def draw_won():
    screen.clear()
    background.draw()
    screen.draw.text("You Won!", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="green")
    restart_button.draw()
    music_button.draw()
    quit_button.draw()


def update():

    global game_state, time_left, enemies  # Declare enemies as global

    if game_state == "playing":
        time_left -= 1 / 60
        if time_left <= 0:
            game_state = "won"  # Correct win condition

        hero.move()
        hero.animate()

        if hero.idle_timer >= 180:
            sounds.game_over_sound.play()
            game_state = "game_over"

        for enemy in enemies[:]:  # Iterate over a copy to allow removal
            enemy.move()
            enemy.animate()
            if hero.sprite.colliderect(enemy.sprite):
                if hero.shield_active:
                    continue
                else:
                    hero.health -= 10
                    enemy.health -= 10
                    sounds.hit_sound.play()
                    if hero.health <= 0:
                        sounds.game_over_sound.play()
                        game_state = "game_over"
                    if enemy.health <= 0:
                        enemies.remove(enemy)  # Now safe to remove
                        if not enemies:  # Check if all enemies are gone
                            game_state = "won"
                            time_left = 0 # Stop the timer when the player wins
        if keyboard.escape:
            game_state = "menu"

    elif game_state in ["menu", "game_over", "won"]:
        pass 

def on_mouse_down(pos):
    global game_state, music_playing

    if game_state == "menu":
        if start_button.is_clicked(pos):
            reset_game()
        elif quit_button.is_clicked(pos):
            exit()

    elif game_state in ["game_over", "won"]:
        if restart_button.is_clicked(pos):
            reset_game()
        elif exit_button.is_clicked(pos):
            exit()

    if music_button.is_clicked(pos):
        music_playing = not music_playing
        if music_playing:
            music.play("background_music")
            music_button.image = "music_on"
        else:
            music.stop()
            music_button.image = "music_off"

def reset_game():
    global game_state, time_left, hero, enemies
    game_state = "playing"
    time_left = 20
    hero = Hero()
    enemies = [Enemy(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(5)]

def draw():
    screen.clear()
    background.draw()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        hero.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Time Left: {int(time_left)}", (10, 40), fontsize=30, color="white")
        screen.draw.text(f"Idle Timer (MAX 180!!!): {hero.idle_timer} frames", (10, 70), fontsize=30, color="yellow")
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "won":
        draw_won()



pgzrun.go()