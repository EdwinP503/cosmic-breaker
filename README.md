# 🚀 Cosmic Breaker

**Cosmic Breaker** is a fast-paced arcade-style asteroid shooter where the player must navigate a spaceship, dodge incoming asteroids, and destroy them for points. The game has an **idle mode** where the ship moves automatically and **manual mode** for direct player control. This README will not only explain the project but also teach you the **Python concepts** used in it.

## 📚 Table of Contents 
- [1. Python Fundamentals Used](#python-fundamentals-used-in-this-project)
- [2. Pygame Concepts](#pygame-concepts-used-in-this-game)
- [3. How to Play](#how-to-play)

## 🎮 Game Features
- **Idle Mode**: The ship moves automatically and shoots asteroids.
- **Manual Mode**: After pressing **Play**, the player can control the ship using **arrow keys** or **A/D**.
- **Asteroids & Shooting**: The ship fires bullets at a fixed rate to destroy incoming asteroids.
- **Score System**: Gain **10 points** per asteroid destroyed.
- **Lives System**: The player has **3 lives** represented as pink circles.
- **Game Over & Continue**: If all lives are lost, a **Continue button** allows the player to restart.

## 🖥️ Controls
| Action | Key |
|--------|-----|
| Move Left | ⬅️ Left Arrow / A |
| Move Right | ➡️ Right Arrow / D |
| Start Manual Mode | Click "Play" Button |
| Restart After Game Over | Click "Continue" Button |

## 📌 What You'll Learn  
By studying this project, you'll understand:  
✔️ **Python Basics** – Variables, loops, and conditionals  
✔️ **Functions** – How to organize reusable code  
✔️ **Lists** – Managing game objects like bullets & asteroids  
✔️ **Object-Oriented Programming (OOP)** – Structuring code using classes  
✔️ **Pygame** – Handling graphics, collisions, and events

## Python Fundamentals Used in This Project

### ✅ Variables & Data Types
In Python, we use variables to store values like numbers, strings, and objects.
Example from the game:

```bash
WIDTH, HEIGHT = 800, 600  # Screen size (integers)
BG_COLOR = (10, 10, 30)   # RGB color (tuple)
ship_speed = 3.5          # Float value for movement speed
```

### ✅ Lists & Loops (Managing Bullets & Asteroids)
The game needs to store bullets and asteroids dynamically, so we use lists.
```bash
bullets = []    # Empty list to store bullets
asteroids = []  # Empty list for asteroids
```
Looping Through Bullets (For Loop)
```bash
for bullet in bullets:  
    bullet[1] -= 5  # Move bullet upwards
```
For loops help iterate over lists dynamically.

### ✅ Removing Objects From a List
When bullets leave the screen, they should be removed to save memory.
```bash
for bullet in bullets[:]:  # Iterate over a copy to avoid errors
    if bullet[1] < 0:  
        bullets.remove(bullet)  # Remove when off-screen
```

### ✅ Functions (Organizing Game Logic)
Python functions allow us to group logic into reusable blocks.
Example: Resetting the game:
```bash
def reset_game():
    global bullets, asteroids, score, lives
    bullets = []
    asteroids = []
    score = 0
    lives = 3
```
Functions prevent code duplication and improve readability.

### ✅ Conditional Statements (If-Else Logic)
Conditionals allow the game to make decisions dynamically.
Example: If the player loses all lives, stop manual movement.
```bash
if lives <= 0:
    manual_move = False  # Disable player control
```

### ✅ Event Handling (User Input in Pygame)
Pygame detects user interactions using an event loop.
Example: Checking if the player presses the Play button:
```bash
if play_button.collidepoint(pygame.mouse.get_pos()):
    if pygame.mouse.get_pressed()[0]:  # Left-click to start
        manual_move = True
        reset_game()
```

## Pygame Concepts Used in This Game

### 1️⃣ Drawing Graphics (Rectangles, Circles, Images)
Pygame allows us to draw objects on the screen.
Example: Drawing the spaceship and bullets:
```bash
pygame.draw.rect(screen, SHIP_COLOR, (ship_x, ship_y, SHIP_WIDTH, SHIP_HEIGHT))
for bullet in bullets:
    pygame.draw.rect(screen, BULLET_COLOR, (bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT))
```
pygame.draw.rect() is used to draw rectangles for objects.

### 2️⃣ Detecting Collisions (Bullet Hits Asteroid)
To check if a bullet hits an asteroid, we use collision detection.
```bash
for bullet in bullets[:]:  
    for asteroid in asteroids[:]:  
        if (bullet[0] > asteroid[0] and bullet[0] < asteroid[0] + ASTEROID_SIZE and
            bullet[1] > asteroid[1] and bullet[1] < asteroid[1] + ASTEROID_SIZE):
            asteroids.remove(asteroid)  # Destroy asteroid
            bullets.remove(bullet)  # Remove bullet
```
This uses **bounding box** collision detection.

### 3️⃣ Game Loop (While Loop to Keep the Game Running)
Pygame runs continuously using a while loop.
```bash
running = True
while running:
    screen.fill(BG_COLOR)  # Redraw background every frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game loop

    pygame.display.flip()  # Update display
```
The game loop updates the game every frame.


## How to Play
1. **Idle Mode**:
   - When the game starts, the ship **moves automatically** and fires bullets at asteroids.
   - The ship dodges incoming asteroids **based on AI movement logic**.

2. **Switching to Manual Mode**:
   - Click **Play** to start **manual movement**.
   - The ship's speed **increases** to 3.5 pixels/frame.
   - The bullet rate **increases** for faster shooting.
   - The ship **no longer has movement restrictions** and can reach the screen edges.

3. **Destroying Asteroids**:
   - Each asteroid destroyed gives **10 points**.
   - Asteroids spawn from the top of the screen.

4. **Losing Lives & Game Over**:
   - If an asteroid hits the ship, **one life is lost**.
   - When all **3 lives are gone**, the **Game Over** screen appears with a **Continue button**.

5. **Restarting the Game**:
   - Click **Continue** to reset the game and start fresh.

## 🛠️ Installation & Running the Game 

### **1️⃣ Install Pygame**
Ensure you have Python installed, then install Pygame:

```bash
pip install pygame
```

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/EdwinP503/cosmic-breaker.git
cd cosmic-breaker
```

### **3️⃣ Run the Game**
```bash
python game.py
```

## 🎨 Screenshots
![start](images/start_screen.jpg) ![gameplay](images/gameplay.jpg) ![endscreen](images/game_over.jpg)

## 📌 Future Enhancements
- **Power-Ups**: Special abilities like **piercing bullets** and **shield protection**.
- **Difficulty Levels**: Increase asteroid speed over time.
- **Background Effects**: Animated cosmic background for a better visual experience.

## 🏆 Credits
- **Developer:** Edwin Polanco  
- **Game Engine:** Pygame  
- **Language:** Python  

## 📜 License
This project is open-source under the **MIT License**.

---

🚀 **Blast through asteroids, dodge threats, and survive in Cosmic Breaker!** 🚀
