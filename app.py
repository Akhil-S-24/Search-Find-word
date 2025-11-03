import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Wizard - Word Search")

# Colors
WHITE, BLACK, BLUE, RED, GREEN = (255,255,255), (0,0,0), (0,0,255), (255,0,0), (0,255,0)
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class WordSearch:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.words = ['PYTHON', 'CODE', 'GAME', 'WORD', 'SEARCH', 'FUN']
        self.word_positions = {}  # Store where each word is placed
        self.found_words = []
        self.generate_grid()
    
    def generate_grid(self):
        # Place words
        for word in self.words:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                row = random.randint(0, self.size-1)
                col = random.randint(0, self.size-1)
                direction = random.choice(['H', 'V', 'D'])
                
                if self.can_place_word(word, row, col, direction):
                    self.place_word(word, row, col, direction)
                    placed = True
                attempts += 1
        
        # Fill empty spaces with random letters
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    def can_place_word(self, word, row, col, direction):
        if direction == 'H' and col + len(word) <= self.size:
            return all(self.grid[row][col+i] in [' ', word[i]] for i in range(len(word)))
        elif direction == 'V' and row + len(word) <= self.size:
            return all(self.grid[row+i][col] in [' ', word[i]] for i in range(len(word)))
        elif direction == 'D' and row + len(word) <= self.size and col + len(word) <= self.size:
            return all(self.grid[row+i][col+i] in [' ', word[i]] for i in range(len(word)))
        return False
    
    def place_word(self, word, row, col, direction):
        positions = []
        for i, letter in enumerate(word):
            if direction == 'H': 
                self.grid[row][col+i] = letter
                positions.append((row, col+i))
            elif direction == 'V': 
                self.grid[row+i][col] = letter
                positions.append((row+i, col))
            elif direction == 'D': 
                self.grid[row+i][col+i] = letter
                positions.append((row+i, col+i))
        self.word_positions[word] = positions
    
    def check_selected_word(self, selected_cells):
        if len(selected_cells) < 2:
            return None
            
        # Convert to string
        word = ''.join(self.grid[r][c] for r, c in selected_cells)
        reversed_word = word[::-1]
        
        # Check both directions
        if word in self.words and word not in self.found_words:
            return word
        elif reversed_word in self.words and reversed_word not in self.found_words:
            return reversed_word
        return None

# Game setup
word_search = WordSearch()
cell_size = 40
grid_x, grid_y = 100, 100
selected_cells = []
dragging = False

running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            x, y = pygame.mouse.get_pos()
            col = (x - grid_x) // cell_size
            row = (y - grid_y) // cell_size
            if 0 <= row < word_search.size and 0 <= col < word_search.size:
                selected_cells = [(row, col)]
        
        elif event.type == pygame.MOUSEMOTION and dragging:
            x, y = pygame.mouse.get_pos()
            col = (x - grid_x) // cell_size
            row = (y - grid_y) // cell_size
            if (0 <= row < word_search.size and 0 <= col < word_search.size and 
                (row, col) not in selected_cells):
                selected_cells.append((row, col))
        
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            # Check if selected cells form a valid word
            found_word = word_search.check_selected_word(selected_cells)
            if found_word:
                word_search.found_words.append(found_word)
                selected_cells = []
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                word_search = WordSearch()
                selected_cells = []
    
    # Draw title
    screen.blit(font.render("WORD WIZARD - Word Search", True, BLUE), (250, 30))
    
    # Draw word list
    screen.blit(small_font.render("Find these words:", True, BLACK), (500, 100))
    for i, word in enumerate(word_search.words):
        color = GREEN if word in word_search.found_words else BLACK
        screen.blit(small_font.render(word, True, color), (500, 130 + i*30))
    
    # Draw grid and letters
    for row in range(word_search.size):
        for col in range(word_search.size):
            x, y = grid_x + col * cell_size, grid_y + row * cell_size
            
            # Highlight selected cells
            if (row, col) in selected_cells:
                pygame.draw.rect(screen, (200, 200, 255), (x, y, cell_size, cell_size))
            
            # Draw cell border
            pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size), 1)
            
            # Draw letter
            letter = word_search.grid[row][col]
            text = small_font.render(letter, True, BLACK)
            screen.blit(text, (x + cell_size//3, y + cell_size//4))
    
  
    screen.blit(small_font.render("Click and drag to select words | R for new puzzle", True, BLACK), (180, 550))
  
    screen.blit(small_font.render(f"Found: {len(word_search.found_words)}/{len(word_search.words)}", True, RED), (500, 300))
    
    pygame.display.flip()

pygame.quit()
sys.exit()