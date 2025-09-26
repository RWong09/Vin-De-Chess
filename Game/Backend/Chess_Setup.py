#Chess Setup File, contains all variables and images used in the game
import pygame
import os

pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Vin De Chess')
font = pygame.font.Font(None, 20)
big_font = pygame.font.Font(None, 50)
timer = pygame.time.Clock()
fps = 60
status_message = None

#Menu variables and images
logo_img = pygame.image.load('C:\\Users\\HP\\OneDrive\\Documents\\VSC codes\\Chess Game\\logo\\Vin De Chess.png')
logo_img = pygame.transform.scale(logo_img, (300, 180))

#Board and Pieces Directories
boards_dir = "C:\\Users\\HP\\OneDrive\\Documents\\VSC codes\\Chess Game\\chess boards"
pieces_dir = "C:\\Users\\HP\\OneDrive\\Documents\\VSC codes\\Chess Game\\chess pieces"

#Scale the board to match the game board size
board_size = 688
board_designs = {}
for file in os.listdir(boards_dir):
    if file.endswith((".png", ".jpg", ".jpeg")):
        name = os.path.splitext(file)[0]   #e.g. "Black White", "spring_border"
        img = pygame.image.load(os.path.join(boards_dir, file))
        scaled = pygame.transform.scale(img, (board_size, board_size))
        board_designs[name] = scaled

#Current selected board
current_board_name = "Black White"
current_board_img = board_designs[current_board_name]

#Game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
white_promotions = ['queen', 'rook', 'bishop', 'knight']
white_moved = [False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                 (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_promotions = ['queen', 'rook', 'bishop', 'knight']
black_moved = [False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False] 
captured_white_pieces = []
captured_black_pieces = []

#Map for shortcode-style filenames
shortcode_map = {
    "queen": ("qw", "qb"),
    "rook": ("rw", "rb"),
    "knight": ("nw", "nb"),
    "bishop": ("bw", "bb"),
    "king": ("kw", "kb"),
    "pawn": ("pw", "pb"),
}

#Piece names for full descriptive style
descriptive_names = {
    "king":   ("White King", "Black King"),
    "queen":  ("White Queen", "Black Queen"),
    "rook":   ("White Rook", "Black Rook"),
    "bishop": ("White Bishop", "Black Bishop"),
    "knight": ("White Knight", "Black Knight"),
    "pawn":   ("White Pawn", "Black Pawn"),
}

#Special mapping for Animals set
animal_map = {
    "Elephant": "pawn",   
    "Zebra": "knight",   
    "Ship": "rook",       
    "Giraffe": "bishop",  
    "Queen": "queen",     
    "King": "king"        
}

#Function to load and scale piece images
def load_piece_image(path, big_size=(310,310), small_size=(140,140)):
    img = pygame.image.load(path)
    return (
        pygame.transform.scale(img, big_size),
        pygame.transform.scale(img, small_size)  
    )

#Load piece designs
piece_sets = {}
for folder in os.listdir(pieces_dir):
    set_path = os.path.join(pieces_dir, folder)
    if not os.path.isdir(set_path):
        continue

    white_images, black_images = {}, {}

    #Collect all filenames in folder
    files = {os.path.splitext(f)[0]: f for f in os.listdir(set_path)}

    #Case 1: Shortcode style (check if "qw"/"kb" exist)
    if any("qw" in f or "kb" in f for f in files):
        for piece, codes in shortcode_map.items():
            w_code, b_code = codes
            for color, code in [("white", w_code), ("black", b_code)]:
                matches = [fname for fname in files if fname.lower().endswith(code)]
                if matches:
                    path = os.path.join(set_path, files[matches[0]])
                    big, small = load_piece_image(path)
                    if color == "white":
                        white_images[piece] = big
                        white_images[piece + "_small"] = small
                    else:
                        black_images[piece] = big
                        black_images[piece + "_small"] = small
    #Case 2: Animals style (check if "White Elephant" etc exist)
    elif folder.lower() == "animals":
        for piece, mapped in animal_map.items():
            w_name, b_name = f"White {piece}", f"Black {piece}"
            if w_name in files:
                path = os.path.join(set_path, files[w_name])
                big, small = load_piece_image(path)
                white_images[mapped] = big
                white_images[mapped + "_small"] = small
            if b_name in files:
                path = os.path.join(set_path, files[b_name])
                big, small = load_piece_image(path)
                black_images[mapped] = big
                black_images[mapped + "_small"] = small
                
    #Case 3: Descriptive style (check if "White King" etc exist)
    elif any("White King" in f or "Black King" in f for f in files):
        for piece, names in descriptive_names.items():
            w_name, b_name = names
            if w_name in files:
                path = os.path.join(set_path, files[w_name])
                big, small = load_piece_image(path)
                white_images[piece] = big
                white_images[piece + "_small"] = small
            if b_name in files:
                path = os.path.join(set_path, files[b_name])
                big, small = load_piece_image(path)
                black_images[piece] = big
                black_images[piece + "_small"] = small

    #Store in master dict
    piece_sets[folder] = {"white": white_images, "black": black_images}
    
current_piece_set = "governor"

#Meme variables and images
memes_dir = "C:\\Users\\HP\\OneDrive\\Documents\\VSC codes\\Chess Game\\chess memes"
meme_files = [
    "Bishops Z97 Meme.png",
    "Bishops Z99 Meme.png",
    "Blundered Queen Meme.png", 
    "Double up Rooks Meme.png",
    "Draw Meme.png",
    "Elo Meme.png",
    "En Passant Meme.jpeg",
    "Find Fork Meme.png",
    "Finding Moves Meme.jpeg",
    "Forced En Passant Meme.png",
    "Fork Meme.png",
    "Knight Fork Meme.png",
    "Laughing at Low Elo Memes.png",
    "Low Elo Blundered Queen Meme.png",
    "Not Checkmate Meme.png",
    "Not End Meme.png",
    "Pawns Promoting Meme.png",
    "Queen Running Meme.png",
    "Sacrificed The Rook Meme.png",
    "Scared for Knight Meme.png",
    "Smothered Mate Memes.jpeg",
    "Stalemate Meme.png",
    "Try To Get To 1000 Elo Meme.png",
    "Win On Time Meme.png"
]

meme_images = []
meme_rects = []
meme_descriptions = [
    "Always when I try to checkmate somebody, there's a freaking bishop from Z97!!!😡",
    "When bishops control the diagonals like bosses! (Spawning from space from Z99)",
    "Yep, always blunder my queen at the worst moments. (No wonder I am three digits) 😂",
    "Oh yeahhhhh, when rooks double up...😏",
    "There's always a wise man said: 'When there's BMW on Stockfish's eval, find a draw!'",
    '"My elo is 4 digits"\nThe elo in question:',
    "En passant is forced, right? RIGHT???",
    "I just prefer to find that fork...",
    "And the opponent finds the best move...😑",
    "When en passant is forced, and you just have to do it...😤",
    "I don't know why they think it's a blunder...(Oh!🫣)",
    "You know, they are waiting for you.🫵",
    "HAHAAHAHAHA! (Proceed to lose another game of bullet)",
    "IT'S ALWAYS THE QUEEN!!! (but it's a brilliant move)",
    "Goddamnit, the bishop from T699 again...",
    "Where's the end game screen? Why does it not sound?",
    "The best buddy to the king😎",
    "*Proceeds to blunder it*",
    "Definitely a brilliant one! (against 200 elo)",
    "It's over when he sacrifices... THE KNIGHT!!!",
    "Opponent: I feel the power!",
    "This is why I don't play chess...😒",
    "*Loses the game in 1 move*\nMe:...(loses 100 elo ratings)",
    "A win is a win!"
]

#Load and scale meme images
for file in meme_files:
    img = pygame.image.load(os.path.join(memes_dir, file))
    #Scale to a reasonable size
    scale_w = 375
    scale_h = int(img.get_height() * (scale_w / img.get_width()))
    img = pygame.transform.scale(img, (scale_w, scale_h))
    meme_images.append(img)

#Check variables/Flashing counter
counter = 0
game_over = False
winner = None
white_en_passant = (100,100)
black_en_passant = (100,100)
white_promo = False
black_promo = False
promo_index = 100
in_check = False
halfmove_clock = 0  #Counts half-moves since last pawn move or capture
board_history = []
game_state = "menu"
scroll_offset = 0
selected_meme = None
game_mode = "classical" 
chess960_backrow = None
castle_choice_active = False
castle_choice_data = None
setup_error_timer = None
setup_start_turn = 0
email_copied_timer = 0

#0-1 for white, 2-3 for black
#0,2 for turn without selection, 1,3 for turn with selection
turn_step = 0
selected_piece = 100
valid_moves = []

#Customizable setup variables
setup_white_pieces = []
setup_white_location = []
setup_black_pieces = []
setup_black_location = []
setup_reset_confirm = False
setup_error_message = None
setup_choose_side = False
#Dragging payload
setup_drag = None
custom_scroll_y = 0