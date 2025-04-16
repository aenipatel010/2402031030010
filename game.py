import tkinter as tk
import numpy as np
import random

class NumberDodgerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("💥 Number Dodger")
        self.canvas_width = 400
        self.canvas_height = 500
        self.block_size = 40
        self.player_speed = 20

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        self.root.bind("<Left>", lambda e: self.move_player(-self.player_speed))
        self.root.bind("<Right>", lambda e: self.move_player(self.player_speed))
        self.canvas.bind("<Button-1>", lambda e: self.restart_game() if not self.running else None)

        self.start_game()

    def start_game(self):
        self.fall_speed = 3
        self.score = 0
        self.running = True
        self.enemies = []
        self.canvas.delete("all")

        # Create player
        self.player = self.canvas.create_rectangle(180, 460, 220, 500, fill="blue")
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 12),
                                                  text=f"Score: {self.score}")
        self.update_game()

    def restart_game(self):
        self.start_game()

    def move_player(self, dx):
        if not self.running:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if 0 <= x1 + dx and x2 + dx <= self.canvas_width:
            self.canvas.move(self.player, dx, 0)

    def create_enemy(self):
        x = random.randint(0, (self.canvas_width - self.block_size) // self.block_size) * self.block_size
        number = str(random.randint(0, 9))
        rect = self.canvas.create_rectangle(x, 0, x + self.block_size, self.block_size, fill="red")
        text = self.canvas.create_text(x + self.block_size / 2, self.block_size / 2, text=number, fill="white", font=("Arial", 16))
        self.enemies.append((rect, text))

    def update_game(self):
        if not self.running:
            return

        if random.random() < 0.05:  # Less frequent
            self.create_enemy()

        for rect, text in self.enemies:
            self.canvas.move(rect, 0, self.fall_speed)
            self.canvas.move(text, 0, self.fall_speed)

        player_coords = self.canvas.coords(self.player)
        new_enemies = []
        for rect, text in self.enemies:
            x1, y1, x2, y2 = self.canvas.coords(rect)
            if self.check_collision(player_coords, (x1, y1, x2, y2)):
                self.game_over()
                return
            elif y1 < self.canvas_height:
                new_enemies.append((rect, text))
            else:
                self.canvas.delete(rect)
                self.canvas.delete(text)
                self.score += 1
                self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
                self.fall_speed += 0.03

        self.enemies = new_enemies
        self.root.after(30, self.update_game)

    def check_collision(self, a, b):
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

    def game_over(self):
        self.running = False
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2 - 20,
                                text=f"💀 Game Over", fill="white", font=("Arial", 20))
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2 + 20,
                                text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2 + 60,
                                text="🖱️ Click to replay", fill="white", font=("Arial", 12))

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberDodgerGame(root)
    root.mainloop()
