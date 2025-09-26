#This is a chess game in Python.
#It is a simple implementation that allows two players to play against each other.

import pygame
from contextlib import contextmanager
from Chess_Setup import *
import random
import webbrowser

#Initialization of the pieces
piece_names = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']

white_pieces_images = piece_sets[current_piece_set]['white']
black_pieces_images = piece_sets[current_piece_set]['black']

#Build "small" dicts (fallback to big if a _small is missing)
white_pieces_small_images = {
    p: piece_sets[current_piece_set]['white'].get(p + '_small', white_pieces_images[p])
    for p in piece_names
}
black_pieces_small_images = {
    p: piece_sets[current_piece_set]['black'].get(p + '_small', black_pieces_images[p])
    for p in piece_names
}

#To determine board has a border
def board_has_border(): 
    return current_board_name.lower().endswith('_border')

#Board geometry
def get_board_geometry(board_rect):
    if board_has_border():
        inner = board_rect.width - 44
        offx, offy = 23, 22
    else:
        inner = board_rect.width
        offx, offy = 0, 0
    sq = inner // 8
    return inner, sq, sq, offx, offy

#Function to wrap the text
def render_wrapped_text(text, font, color, x, y, max_width):
    words = text.split(' ')
    lines, current = [], ""
    for word in words:
        test = current + word + " "
        if font.size(test)[0] > max_width:
            lines.append(current)
            current = word + " "
        else:
            current = test
    lines.append(current)

    for line in lines:
        surface = font.render(line, True, color)
        screen.blit(surface, (x, y))
        y += font.get_linesize()

    return y

#Function to colour the text and frame
def draw_colored_title(text, font, center_y, colors, padding=20):
    #Pick random or cycling color
    color = colors[pygame.time.get_ticks() // 500 % len(colors)]
    label = font.render(text, True, color)
    #Make a rectangle with padding
    rect = label.get_rect(center=(width // 2, center_y))
    rect.inflate_ip(padding * 2, padding * 2)
    #Draw frame background
    pygame.draw.rect(screen, "#FFF8DC", rect, border_radius=12)  #Light background
    pygame.draw.rect(screen, color, rect, 6, border_radius=12)   #Colorful border
    screen.blit(label, label.get_rect(center=rect.center))
    return rect

def draw_framed_title(text, font, center_y, text_color="#2E8B57", frame_color="#006400", pad_x=60, pad_y=20):
    label = font.render(text, True, text_color)
    rect = label.get_rect(center=(width // 2, center_y))
    rect.inflate_ip(pad_x, pad_y)
    #Frame background
    pygame.draw.rect(screen, "#E6EEE6", rect, border_radius=12)  #Honeydew background
    pygame.draw.rect(screen, frame_color, rect, 8, border_radius=12)
    screen.blit(label, label.get_rect(center=rect.center))
    return rect

#Draw the menu page
def draw_menu():
    credit_text = pygame.font.SysFont(None, 36).render("Powered by Wong Hoong Liang @UM 2025", True, "white")
    screen.fill("#164D3A")
    #Draw logo at top
    screen.blit(logo_img, (width // 2 - logo_img.get_width() // 2 , 50))
    screen.blit(credit_text, (width // 2 - credit_text.get_width() // 2, height - 80))
    
    #Draw buttons
    button_font = pygame.font.SysFont(None, 60)
    buttons = ["Play", "Memes", "Customize", "Credits"]
    btn_rects = []
    for i, text in enumerate(buttons):
        rect = pygame.Rect(width//2 - 150, 300 + i*100, 300, 70)
        pygame.draw.rect(screen, "seagreen", rect, border_radius=12)
        label = button_font.render(text, True, "white")
        screen.blit(label, (rect.centerx - label.get_width()//2, rect.centery - label.get_height()//2))
        btn_rects.append((rect, text))
    return btn_rects

#Draw credits page
def draw_credits():
    global scroll_offset, status_message
    screen.fill("beige")
    
    #Reset cursor to default arrow
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    #Title
    title_font = pygame.font.SysFont(None, 80, bold=True)
    colors = ["#FF4500", "#1E90FF", "#32CD32", "#FFD700", "#BA55D3"]  #Orange, blue, green, gold, purple
    draw_colored_title("Credits", title_font, 60 + scroll_offset, colors)
    #Back button
    back_btn = pygame.Rect(20, 20, 120, 50)
    pygame.draw.rect(screen, "darkred", back_btn, border_radius=8)
    back_text = pygame.font.SysFont(None, 40).render("Back", True, "white")
    screen.blit(back_text, (back_btn.centerx - back_text.get_width()//2, back_btn.centery - back_text.get_height()//2))
    #Text font for emojis
    font = pygame.font.SysFont("Segoe UI Emoji", 28)
    
    y = 140 + scroll_offset
    line_spacing = 40
    clickable_links = []
    email_rect = None
    
    for role in ["Editor", "Designer", "Game Producer"]:
        text = font.render(f"{role}: Wong Hoong Liang", True, "black")
        screen.blit(text, (width//2 - text.get_width()//2, y))
        y += line_spacing
    appre_line = font.render("Big thanks to FSKTM UM for supporting this side project! :)", True, "darkblue")
    screen.blit(appre_line, (width//2 - appre_line.get_width()//2, y))
    y += line_spacing
    y = render_wrapped_text(
        "For future collaborations and ideas, drop an email to",
        font, "black", 80, y, width - 160
    )
    email = "hoongliang03@gmail.com"
    email_text = font.render(email, True, "blue")
    email_rect = email_text.get_rect(topleft=(80, y))
    screen.blit(email_text, email_rect)
    y += line_spacing
    
    #Divider line
    pygame.draw.line(screen, "black", (80, y), (width - 80, y), 2)
    y += line_spacing
    #Chess Board and Pieces Subtitle
    bold_font = pygame.font.SysFont("Segoe UI Emoji", 32, bold=True)
    draw_colored_title("Chess Board and Pieces Design", bold_font, y, colors, padding=12)
    y += line_spacing + 10
    links = [
        "https://www.xiangqi.com/graphics",
        "https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces"
    ]
    for link in links:
        link_text = font.render(link, True, "blue")
        rect = screen.blit(link_text, (80, y))
        clickable_links.append((rect, link))
        y += line_spacing
    y = render_wrapped_text(
        "I found most of the designs from Google but couldn't include it (since I have not saved it down🤡)",
        font, "black", 80, y, width - 160
    )
    y += line_spacing
    
    pygame.draw.line(screen, "black", (80, y), (width - 80, y), 2)
    y += line_spacing
    #Chess Memes Credit
    draw_colored_title("Chess Memes", bold_font, y, colors, padding=12)
    y += line_spacing + 15
    screen.blit(font.render("Mostly made by me hehe (Wong)", True, "black"), (80, y))
    y += line_spacing
    screen.blit(font.render("Some memes were taken from Chess.com:", True, "black"), (80, y))
    y += line_spacing
    meme_links = [
        "https://www.chess.com/article/view/chess-memes",
        "https://www.chess.com/article/view/en-passant-awareness"
    ]
    for link in meme_links:
        link_text = font.render(link, True, "blue")
        rect = screen.blit(link_text, (80, y))
        clickable_links.append((rect, link))
        y += line_spacing

    #Scroll bounds
    content_height = y + 100
    min_offset = 0
    max_offset = -(content_height - height + 150)
    
    mouse_pos = pygame.mouse.get_pos()
    #Email hover check
    if email_rect and email_rect.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    #Links hover check
    for rect, _ in clickable_links:
        if rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    #Draw the message when the email is copied        
    if status_message == "Email copied to clipboard!":
        now = pygame.time.get_ticks()
        if now - email_copied_timer < 2000:
            msg_font = pygame.font.SysFont(None, 22)
            msg_surface = msg_font.render(status_message, True, "white")
            box = msg_surface.get_rect()
            box.midtop = (email_rect.centerx, email_rect.bottom + 5)
            pygame.draw.rect(screen, "darkgreen", box.inflate(12, 8), border_radius=6)
            screen.blit(msg_surface, msg_surface.get_rect(center=box.center))
        else:
            status_message = None #Auto clear message after 2 seconds
    return back_btn, email_rect, clickable_links, min_offset, max_offset

#Draw the memes page with scrollable images
def draw_memes():
    global meme_rects
    screen.fill("beige")
    title_font = pygame.font.SysFont(None, 80)
    label = title_font.render("Chess Memes", True, "black")
    screen.blit(label, (width//2 - label.get_width()//2, 20 + scroll_offset))
    #Meme grid (2 columns, variable row height)
    meme_rects = []
    col_x = [100, 525]
    start_y = 100 + scroll_offset
    y = start_y
    i = 0
    total_height = 0
    meme_font = pygame.font.SysFont(None, 28)
    while i < len(meme_images):
        row_imgs = meme_images[i:i+2]
        row_height = max(img.get_height() for img in row_imgs) + 50  #+50 for labels
        for col, img in enumerate(row_imgs):
            x = col_x[col]
            rect = img.get_rect(topleft=(x, y))
            screen.blit(img, rect)
            #Frame around meme
            frame_rect = rect.inflate(10, 10)
            pygame.draw.rect(screen, "black", frame_rect, width=3, border_radius=8)
            meme_rects.append(rect)
            #Label meme number under each meme
            meme_number = i + col + 1
            num_text = meme_font.render(f"Meme #{meme_number}", True, "darkblue")
            text_rect = num_text.get_rect(midtop=(rect.centerx, rect.bottom + 10))
            screen.blit(num_text, text_rect)
        y += row_height
        total_height += row_height
        i += 2
    #Back button (page)
    back_btn = pygame.Rect(20, height - 75, 120, 50)
    pygame.draw.rect(screen, "darkred", back_btn, border_radius=8)
    back_text = pygame.font.SysFont(None, 40).render("Back", True, "white")
    screen.blit(back_text, (back_btn.centerx - back_text.get_width()//2, back_btn.centery - back_text.get_height()//2))
    #Calculate scroll bounds (return instead of modifying global)
    min_offset = 0
    max_offset = -(total_height - (height - 150))
    popup_buttons = {}
    #If a meme is selected, show popup description
    if selected_meme is not None:
        popup_rect = pygame.Rect(width//2 - 300, height//2 - 150, 600, 300)
        pygame.draw.rect(screen, "#FFD966", popup_rect, border_radius=12)
        pygame.draw.rect(screen, "black", popup_rect, 3, border_radius=12)
        #Show meme number at top
        num_font = pygame.font.SysFont(None, 36)
        num_text = num_font.render(f"Meme #{selected_meme + 1}", True, "black")
        screen.blit(num_text, (popup_rect.centerx - num_text.get_width()//2, popup_rect.top + 10))
        desc = meme_descriptions[selected_meme]
        #Emoji-friendly font
        font = pygame.font.SysFont("Segoe UI Emoji", 26)
        #Split lines by \n first, then wrap
        split_lines = desc.split("\n")
        wrapped_lines = []
        for raw_line in split_lines:
            words = raw_line.split(" ")
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if font.size(test_line)[0] < popup_rect.width - 40:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line.strip())
                    current_line = word + " "
            wrapped_lines.append(current_line.strip())
        for j, line in enumerate(wrapped_lines):
            text = font.render(line, True, "black")
            screen.blit(text, (popup_rect.left + 20, popup_rect.top + 50 + j*30))
        #Back button inside popup
        back_desc_btn = pygame.Rect(popup_rect.centerx - 60, popup_rect.bottom - 50, 120, 40)
        pygame.draw.rect(screen, "darkred", back_desc_btn, border_radius=8)
        screen.blit(pygame.font.SysFont(None, 30).render("Back", True, "white"),
                    (back_desc_btn.centerx - 25, back_desc_btn.centery - 12))
        #Left button
        left_btn = pygame.Rect(popup_rect.left + 20, popup_rect.centery - 20, 40, 40)
        pygame.draw.polygon(screen, "red", [
            (left_btn.right, left_btn.top),
            (left_btn.right, left_btn.bottom),
            (left_btn.left, left_btn.centery)
        ])
        #Right button
        right_btn = pygame.Rect(popup_rect.right - 60, popup_rect.centery - 20, 40, 40)
        pygame.draw.polygon(screen, "red", [
            (right_btn.left, right_btn.top),
            (right_btn.left, right_btn.bottom),
            (right_btn.right, right_btn.centery)
        ])
        popup_buttons = {"back": back_desc_btn, "left": left_btn, "right": right_btn}
    return back_btn, popup_buttons, min_offset, max_offset

#Draw the customization page
def draw_customization():
    global current_board_name, current_board_img, current_piece_set, customize_proceed_btn
    screen.fill("beige")

    title_font = pygame.font.SysFont(None, 70, bold=True)
    draw_framed_title("Customization", title_font, 50 + custom_scroll_y, text_color="#228B22", frame_color="#006400")

    #Board Section
    y_offset = 100 + custom_scroll_y
    screen.blit(pygame.font.SysFont(None, 40).render("Choose Board:", True, "black"), (50, y_offset))
    y_offset += 40 

    board_buttons = {}
    x = 50
    for name, img in board_designs.items():
        thumb = pygame.transform.scale(img, (150, 150))
        rect = screen.blit(thumb, (x, y_offset))
        board_buttons[name] = rect
        if name == current_board_name:
            pygame.draw.rect(screen, "red", rect, 4) 
        x += 170

    #Piece Selection
    y_offset += 200 
    screen.blit(pygame.font.SysFont(None, 40).render("Choose Pieces:", True, "black"), (50, y_offset))
    y_offset += 40 

    piece_buttons = {}
    piece_buttons = {}
    x = 50
    col = 0
    row_max_h = 0

    for set_name, data in piece_sets.items():
        #Governor preview bigger; others 80x80
        if set_name.lower() == "governor":
            #Large 300x300 king preview
            base_k = data["white"]["king"]
            base_q = data["white"]["queen"]
            preview_k = pygame.transform.smoothscale(base_k, (300, 300))
            preview_q = pygame.transform.smoothscale(base_q, (300, 300))
            rect_k = screen.blit(preview_k, (x, y_offset))
            rect_q = screen.blit(preview_q, (x + 90, y_offset))
            clickable = pygame.Rect(x, y_offset, 180, 90)
        else:
            #Two small (king+queen) previews
            k = pygame.transform.smoothscale(data["white"]["king"], (80, 80))
            q = pygame.transform.smoothscale(data["white"]["queen"], (80, 80))
            rect_k = screen.blit(k, (x, y_offset))
            rect_q = screen.blit(q, (x + 90, y_offset))
            clickable = rect_k.union(rect_q)
            cell_w, cell_h = 190, 100

        piece_buttons[set_name] = clickable
        if set_name == current_piece_set:
            pygame.draw.rect(screen, "red", clickable, 3)

        #Track layout
        col += 1
        x += 200  #Spacing between designs

        #4 per row -> wrap
        if col == 4:
            col = 0
            x = 50
            y_offset += 105
            row_max_h = 0

    #Mode Selection
    y_offset += 125
    screen.blit(pygame.font.SysFont(None, 40).render("Choose Mode:", True, "black"), (50, y_offset))
    y_offset += 50
    mode_buttons = {}
    classical_btn = pygame.Rect(100, y_offset, 200, 60)
    chess960_btn = pygame.Rect(400, y_offset, 200, 60)
    customize_btn = pygame.Rect(700, y_offset, 200, 60)
    pygame.draw.rect(screen, "green", classical_btn, border_radius=10)
    pygame.draw.rect(screen, "green", chess960_btn, border_radius=10)
    pygame.draw.rect(screen, "green", customize_btn, border_radius=10)
    mode_buttons = {"classical": classical_btn, "chess960": chess960_btn, "custom": customize_btn}
    mode_font = pygame.font.SysFont(None, 36)
    screen.blit(mode_font.render("Classical", True, "white"), (classical_btn.centerx - 60, classical_btn.centery - 15))
    screen.blit(mode_font.render("Chess960", True, "white"), (chess960_btn.centerx - 60, chess960_btn.centery - 15))
    screen.blit(mode_font.render("Custom", True, "white"), (customize_btn.centerx - 50, customize_btn.centery - 15))
    if game_mode == "classical":
        pygame.draw.rect(screen, "red", classical_btn, 4, border_radius=10)
    elif game_mode == "chess960":
        pygame.draw.rect(screen, "red", chess960_btn, 4, border_radius=10)
    elif game_mode == "custom":
        pygame.draw.rect(screen, "red", customize_btn, 4, border_radius=10)
    
    #Back button
    back_btn = pygame.Rect(20, 20, 120, 50)
    pygame.draw.rect(screen, "darkred", back_btn, border_radius=8)
    back_text = pygame.font.SysFont(None, 40).render("Back", True, "white")
    screen.blit(back_text, (back_btn.centerx - back_text.get_width()//2, back_btn.centery - back_text.get_height()//2))
    
    #Proceed button (Only visible when custom mode is selected)
    global customize_proceed_btn
    #Custom mode
    if game_mode == "custom":
        customize_proceed_btn = pygame.Rect(width//2 - 120, y_offset + 85, 240, 60)
        pygame.draw.rect(screen, "#1F7A8C", customize_proceed_btn, border_radius=12)
        go_font = pygame.font.SysFont(None, 40)
        label = go_font.render("Proceed", True, "white")
        screen.blit(label, (customize_proceed_btn.centerx - label.get_width()//2, customize_proceed_btn.centery - label.get_height()//2))
        y_offset = customize_proceed_btn.bottom + 20
    else:
        customize_proceed_btn = None
    
    #Calculate scroll bounds    
    content_height = y_offset + 100
    min_offset = 0
    max_offset = -(content_height - (height - 100))
    
    return board_buttons, piece_buttons, mode_buttons, back_btn, min_offset, max_offset

#Function to draw the chessboard
def draw_board(screen):
    #Available width for the board (leave 310px for right-side table)
    available_w = width - 280
    available_h = height
    #Scale the board so it fits through the width of the screen
    board_size = min(available_w, available_h)
    board_img = pygame.transform.smoothscale(current_board_img.convert_alpha(), (board_size, board_size))
    #Stick to top-left corner
    board_rect = board_img.get_rect(topleft=(0, 0))
    screen.blit(board_img, board_rect)
    #Highlight the table header
    pygame.draw.rect(screen, "black", (board_rect.width, 0, 140, 720))
    pygame.draw.rect(screen, "white", (board_rect.width + 140, 0, 140, 720))  
    #Add captured pieces labels
    label_font = pygame.font.SysFont(None, 36)
    black_label = label_font.render("Black", True, "white")
    white_label = label_font.render("White", True, "black")
    screen.blit(black_label, (board_rect.width + 30, 10))
    screen.blit(white_label, (board_rect.width + 175, 10))
    #Draw horizontal line below labels (table header)
    pygame.draw.line(screen, "lime green", (board_rect.width, 75), (board_rect.width + 310, 75), 4)

    return board_rect

def get_draw_image(color, piece, square_w, square_h):
    #Governor uses default sizing; others scale to the square
    chess_base = (white_pieces_images if color == 'white' else black_pieces_images)[piece]
    if current_piece_set.lower() == 'governor':
        return chess_base
    return pygame.transform.smoothscale(chess_base, (square_w, square_h))

#Draw the pieces on the board
def draw_pieces(board_rect):
    inner, sqw, sqh, offx, offy = get_board_geometry(board_rect)
    
    #For white pieces
    for i, piece in enumerate(white_pieces):
        x, y = white_location[i]
        img = get_draw_image('white', piece, sqw, sqh)
        screen.blit(img, (offx + int(x * sqw), offy + int(y * sqh)))
        if turn_step < 2 and selected_piece == i:
            pygame.draw.rect(screen, 'yellow',
                             (offx + int(x * sqw), offy + int(y * sqh), sqw, sqh), 3)
    #For black pieces
    for i, piece in enumerate(black_pieces):
        x, y = black_location[i]
        img = get_draw_image('black', piece, sqw, sqh)
        screen.blit(img, (offx + int(x * sqw), offy + int(y * sqh)))
        if turn_step >= 2 and selected_piece == i:
            pygame.draw.rect(screen, 'red',
                             (offx + int(x * sqw), offy + int(y * sqh), sqw, sqh), 3)
  
#Function to check valid moves for each piece
def check_options(pieces, locations, turn, include_castling=True):
    moves_list = []
    all_valid_moves = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn_moves(location, turn)
        elif piece == 'rook':
            moves_list = check_rook_moves(location, turn)
        elif piece == 'knight':
            moves_list = check_knight_moves(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop_moves(location, turn)
        elif piece == 'queen':
            moves_list = check_queen_moves(location, turn)
        elif piece == 'king':
            moves_list = check_king_moves(location, turn, include_castling)
        all_valid_moves.append(moves_list)
    return all_valid_moves

#Check valid moves for each piece type
def check_pawn_moves(location, turn):
    x, y = location
    valid_moves = []
    if turn == 'white':
        #Move forward only if the square is empty
        if y > 0 and (x, y - 1) not in black_location and (x, y - 1) not in white_location:
            valid_moves.append((x, y - 1))
        #Initial double move only if both squares are empty
        if (y == 6 and (x, y - 1) not in black_location and (x, y - 1) not in white_location 
        and (x, y - 2) not in black_location and (x, y - 2) not in white_location):
            valid_moves.append((x, y - 2))
        #Capture diagonally
        if x > 0 and y > 0 and (x - 1, y - 1) in black_location:
            valid_moves.append((x - 1, y - 1))
        elif x > 0 and y > 0 and (x - 1, y - 1) == black_en_passant:
            valid_moves.append((x - 1, y - 1))
        if x < 7 and y > 0 and (x + 1, y - 1) in black_location:
            valid_moves.append((x + 1, y - 1))
        elif x < 7 and y > 0 and (x + 1, y - 1) == black_en_passant:
            valid_moves.append((x + 1, y - 1))
        
    else:  #Black pawn moves
        #Move forward only if the square is empty
        if y < 7 and (x, y + 1) not in white_location and (x, y + 1) not in black_location:
            valid_moves.append((x, y + 1))
        #Initial double move only if both squares are empty
        if (y == 1 and (x, y + 1) not in white_location and (x, y + 1) not in black_location
        and (x, y + 2) not in white_location and (x, y + 2) not in black_location):
            valid_moves.append((x, y + 2))
        #Capture diagonally
        if x > 0 and y < 7 and (x - 1, y + 1) in white_location:
            valid_moves.append((x - 1, y + 1))
        elif x > 0 and y < 7 and (x - 1, y + 1) == white_en_passant:
            valid_moves.append((x - 1, y + 1))
        if x < 7 and y < 7 and (x + 1, y + 1) in white_location:
            valid_moves.append((x + 1, y + 1))
        elif x < 7 and y < 7 and (x + 1, y + 1) == white_en_passant:
            valid_moves.append((x + 1, y + 1))
    return valid_moves

#Function to check en passant
def check_en_passant(old_coord, new_coord):
    if turn_step <= 1:
        index = white_location.index(old_coord)
        ep_coords = (new_coord[0], new_coord[1] + 1)
        piece = white_pieces[index]
    else:
        index = black_location.index(old_coord)
        ep_coords = (new_coord[0], new_coord[1] - 1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coord[1] - new_coord[1]) == 2:
        pass
    else:
        ep_coords = (100,100)
    return ep_coords

def check_rook_moves(location, turn):
    x, y = location
    valid_moves = []
    #Right
    for i in range(x + 1, 8):
        coord = (i, y)
        if coord in white_location or coord in black_location:
            if (turn == 'white' and coord in black_location) or (turn == 'black' and coord in white_location):
                valid_moves.append(coord)  #Capture opponent
            break  #Stop at first piece
        valid_moves.append(coord)
    #Left
    for i in range(x - 1, -1, -1):
        coord = (i, y)
        if coord in white_location or coord in black_location:
            if (turn == 'white' and coord in black_location) or (turn == 'black' and coord in white_location):
                valid_moves.append(coord)
            break
        valid_moves.append(coord)
    #Down
    for j in range(y + 1, 8):
        coord = (x, j)
        if coord in white_location or coord in black_location:
            if (turn == 'white' and coord in black_location) or (turn == 'black' and coord in white_location):
                valid_moves.append(coord)
            break
        valid_moves.append(coord)
    #Up
    for j in range(y - 1, -1, -1):
        coord = (x, j)
        if coord in white_location or coord in black_location:
            if (turn == 'white' and coord in black_location) or (turn == 'black' and coord in white_location):
                valid_moves.append(coord)
            break
        valid_moves.append(coord)
    return valid_moves

def check_knight_moves(location, turn):
    x, y = location
    valid_moves = []
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    for dx, dy in knight_moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            coord = (new_x, new_y)
            if turn == 'white':
                if coord not in white_location:
                    valid_moves.append(coord)
            else:  #black
                if coord not in black_location:
                    valid_moves.append(coord)
    return valid_moves

def check_bishop_moves(location, turn):
    x, y = location
    valid_moves = []
    #Diagonal moves
    #Up-Right
    for i, j in zip(range(x + 1, 8), range(y - 1, -1, -1)):
        coord = (i, j)
        if coord in white_location or coord in black_location:
            if (turn == 'white' and coord in black_location) or (turn == 'black' and coord in white_location):
                valid_moves.append(coord)  #Capture opponent
            break  #Stop at first piece
        valid_moves.append(coord)
    #Up-Left
    for i, j in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
        coord = (i, j)
        if coord in white_location or coord in black_location:
            if (turn == 'white' and coord in black_location) or (turn == 'black' and coord in white_location):
                valid_moves.append(coord)
            break
        valid_moves.append(coord)
    #Down-Right
    for i, j in zip(range(x + 1, 8), range(y + 1, 8)):
        coord = (i, j)
        if coord in white_location or coord in black_location:
            if (turn == 'white' and coord in black_location) or (turn == 'black' and coord in white_location):
                valid_moves.append(coord)
            break
        valid_moves.append(coord)
    #Down-Left
    for i, j in zip(range(x - 1, -1, -1), range(y + 1, 8)):
        coord = (i, j)
        if coord in white_location or coord in black_location:
            if (turn == 'white' and coord in black_location) or (turn == 'black' and coord in white_location):
                valid_moves.append(coord)
            break
        valid_moves.append(coord)
    return valid_moves

def check_queen_moves(location, turn):
    #Queen combines rook and bishop moves
    rook_moves = check_rook_moves(location, turn)
    bishop_moves = check_bishop_moves(location, turn)
    return rook_moves + bishop_moves

def check_king_moves(location, turn, include_castling=True):
    x, y = location
    valid_moves = []
    king_moves = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]
    for dx, dy in king_moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            coord = (new_x, new_y)
            if turn == 'white':
                if coord not in white_location:
                    valid_moves.append(coord)
            else: 
                if coord not in black_location:
                    valid_moves.append(coord)
    #Add castling if legal
    if include_castling:
        valid_moves.extend(check_castling(turn, location))
    return valid_moves

#Check valid moves for the selected piece
def check_valid_moves():
    if turn_step < 2:  # White to move
        base_moves = white_options[selected_piece]
        return filter_moves(
            selected_piece, base_moves,
            white_pieces, white_location,
            black_pieces, black_location, black_options,
            'white'
        )
    else:              # Black to move
        base_moves = black_options[selected_piece]
        return filter_moves(
            selected_piece, base_moves,
            black_pieces, black_location,
            white_pieces, white_location, white_options,
            'black'
        )

#Check if the king is in check
def is_in_check(pieces, locations, opponent_options, color):
    if 'king' not in pieces:
        return False  #King already captured (game over condition)
    king_index = pieces.index('king')
    king_square = locations[king_index]
    return king_square in sum(opponent_options, [])

#Temporarily swap in simulated board positions so move validation runs on the fake state
@contextmanager
def temp_board_state(temp_white_loc, temp_black_loc):
    global white_location, black_location
    old_w, old_b = white_location, black_location
    white_location, black_location = temp_white_loc, temp_black_loc
    try:
        yield
    finally:
        white_location, black_location = old_w, old_b
        
#Filter moves to ensure they don't leave the king in check
def filter_moves(piece_index, moves, pieces, locations,
                 opp_pieces, opp_locations, opp_options, turn):
    safe_moves = []

    for move in moves:
        #Copies of current state
        temp_pieces = pieces.copy()
        temp_locations = locations.copy()
        temp_opp_pieces = opp_pieces.copy()
        temp_opp_locations = opp_locations.copy()

        #Simulate our moves
        temp_locations[piece_index] = move

        #Simulate capture (remove opponent piece if present)
        if move in temp_opp_locations:
            cap_idx = temp_opp_locations.index(move)
            del temp_opp_pieces[cap_idx]
            del temp_opp_locations[cap_idx]
            
        #If this move is castling (king moving to 6 or 2 on backrank), move the rook too
        if pieces[piece_index] == 'king':
            rank = 7 if turn == 'white' else 0
            if move[1] == rank and move[0] in (6, 2):
                #Find rook index on the castling side (Closest rook on that side)
                kx = locations[piece_index][0]
                if move[0] == 6:
                    #Kingside
                    rook_candidates = [(i, loc[0]) for i, loc in enumerate(locations)
                                       if pieces[i] == 'rook' and loc[1] == rank and loc[0] > kx]
                    if rook_candidates:
                        rook_idx = min(rook_candidates, key=lambda t: t[1])[0]
                        temp_locations[rook_idx] = (5, rank)
                else:
                    #Queenside
                    rook_candidates = [(i, loc[0]) for i, loc in enumerate(locations)
                                       if pieces[i] == 'rook' and loc[1] == rank and loc[0] < kx]
                    if rook_candidates:
                        rook_idx = max(rook_candidates, key=lambda t: t[1])[0]
                        temp_locations[rook_idx] = (3, rank)
        
        #Decide which temp board is White/Black for the context manager
        if turn == 'white':
            tw, tb = temp_locations, temp_opp_locations
            opp_turn = 'black'
        else:
            tw, tb = temp_opp_locations, temp_locations
            opp_turn = 'white'

        #Recompute opponent options on the simulated board
        with temp_board_state(tw, tb):
            temp_opp_options = check_options(
                temp_opp_pieces, temp_opp_locations, opp_turn
            )

        #Keep only moves where our king is safe on the simulated board
        if not is_in_check(temp_pieces, temp_locations, temp_opp_options, turn):
            safe_moves.append(move)

    return safe_moves

#Check for checkmate
def check_checkmate(turn):
    if turn == 'white':
        if is_in_check(white_pieces, white_location, black_options, 'white'):
            #Assume checkmate until proven otherwise
            for i, moves in enumerate(white_options):
                safe_moves = filter_moves(i, moves, white_pieces, white_location,
                                          black_pieces, black_location, black_options, 'white')
                if safe_moves:  #If any piece has a safe move, no checkmate
                    return False
            return True
    else:
        if is_in_check(black_pieces, black_location, white_options, 'black'):
            for i, moves in enumerate(black_options):
                safe_moves = filter_moves(i, moves, black_pieces, black_location,
                                          white_pieces, white_location, white_options, 'black')
                if safe_moves:
                    return False
            return True

#Draw custom setup screen
def get_board_square_from_pixel(board_rect, px, py):
    inner, sqw, sqh, offx, offy = get_board_geometry(board_rect)
    bx, by, bw, bh = board_rect
    x_rel = px - bx - offx
    y_rel = py - by - offy
    if x_rel < 0 or y_rel < 0 or x_rel >= inner or y_rel >= inner:
        return None
    file = int(x_rel // sqw)
    rank = int(y_rel // sqh)
    if file < 0 or file > 7 or rank < 0 or rank > 7:
        return None
    return (file, rank)

def draw_setup_pieces(board_rect):
    inner, sqw, sqh, offx, offy = get_board_geometry(board_rect)
    #Board placements
    for i, piece in enumerate(setup_white_pieces):
        x, y = setup_white_location[i]
        img_setup_white = get_draw_image('white', piece, sqw, sqh)
        screen.blit(img_setup_white, (board_rect.x + offx + int(x * sqw), board_rect.y + offy + int(y * sqh)))
    for i, piece in enumerate(setup_black_pieces):
        x, y = setup_black_location[i]
        img_setup_black = get_draw_image('black', piece, sqw, sqh)
        screen.blit(img_setup_black, (board_rect.x + offx + int(x * sqw), board_rect.y + offy + int(y * sqh)))

def draw_custom_setup():
    global setup_error_message, setup_error_timer
    screen.fill('light gray')
    board_rect = draw_board(screen)
    draw_setup_pieces(board_rect)

    #Right-side trays
    tray_font = pygame.font.SysFont(None, 28)
    screen.blit(tray_font.render("White tray", True, "black"), (board_rect.right + 20, 100))
    screen.blit(tray_font.render("Black tray", True, "black"), (board_rect.right + 20, 280))

    tray_rects = {'white': {}, 'black': {}}
    names = ['king','queen','rook','bishop','knight','pawn']
    spacing_x, spacing_y = 60, 60 
    max_cell = min(spacing_y - 5, spacing_x - 10)

    def tray_img(color, piece):
        src = (white_pieces_small_images if color == 'white' else black_pieces_small_images)[piece]
        if current_piece_set.lower() == 'governor':
            return src
        return pygame.transform.smoothscale(src, (max_cell, max_cell))

    for i, n in enumerate(names):
        col, row = i % 2, i // 2
        x = board_rect.right + 165 + col * spacing_x
        y = 130 + row * spacing_y
        rect = screen.blit(tray_img('white', n), (x, y))
        tray_rects['white'][n] = rect

    for i, n in enumerate(names):
        col, row = i % 2, i // 2
        x = board_rect.right + 165 + col * spacing_x
        y = 310 + row * spacing_y
        rect2 = screen.blit(tray_img('black', n), (x, y))
        tray_rects['black'][n] = rect2

    #Bottom buttons
    back_btn = pygame.Rect(20, height - 70, 120, 50)
    reset_btn = pygame.Rect(width//2 - 85, height - 70, 150, 50)
    proceed_btn = pygame.Rect(width - 180, height - 70, 160, 50)
    pygame.draw.rect(screen, "darkred", back_btn, border_radius=8)
    pygame.draw.rect(screen, "red", reset_btn, border_radius=8)
    pygame.draw.rect(screen, "green", proceed_btn, border_radius=8)
    btn_font = pygame.font.SysFont(None, 32)
    screen.blit(btn_font.render("Back", True, "white"), (back_btn.centerx - 30, back_btn.centery - 12))
    screen.blit(btn_font.render("Reset", True, "white"), (reset_btn.centerx - 30, reset_btn.centery - 12))
    screen.blit(btn_font.render("Proceed", True, "white"), (proceed_btn.centerx - 45, proceed_btn.centery - 12))

    #Popups
    confirm_rects = None
    if setup_reset_confirm:
        popup = pygame.Rect(width//2 - 200, height//2 - 90, 400, 180)
        pygame.draw.rect(screen, "#FFD966", popup, border_radius=12)
        qf = pygame.font.SysFont(None, 30)
        screen.blit(qf.render("Are you sure you want to reset?", True, "black"), (popup.centerx - 160, popup.top + 50))
        yes_btn = pygame.Rect(popup.left + 60, popup.bottom - 60, 100, 40)
        no_btn = pygame.Rect(popup.right - 160, popup.bottom - 60, 100, 40)
        pygame.draw.rect(screen, "green", yes_btn, border_radius=8)
        pygame.draw.rect(screen, "red", no_btn, border_radius=8)
        screen.blit(btn_font.render("Yes", True, "white"), (yes_btn.centerx - 18, yes_btn.centery - 12))
        screen.blit(btn_font.render("No", True, "white"), (no_btn.centerx - 14, no_btn.centery - 12))
        confirm_rects = (yes_btn, no_btn)
    choose_rects = None
    if setup_choose_side:
        popup = pygame.Rect(width//2 - 220, height//2 - 120, 440, 240)
        pygame.draw.rect(screen, "#FFD966", popup, border_radius=12)
        tf = pygame.font.SysFont(None, 34)
        screen.blit(tf.render("Choose the side to move", True, "black"), (popup.centerx - 160, popup.top + 20))
        white_btn = pygame.Rect(popup.left + 40, popup.centery - 40, 120, 80)
        black_btn = pygame.Rect(popup.right - 160, popup.centery - 40, 120, 80)
        pygame.draw.rect(screen, "white", white_btn, border_radius=10)
        pygame.draw.rect(screen, "black", black_btn, border_radius=10)
        pygame.draw.rect(screen, "black", white_btn, 2, border_radius=10)
        choose_rects = (white_btn, black_btn)
    if setup_drag:
        img = get_draw_image(setup_drag['color'], setup_drag['piece'], 64, 64)
        screen.blit(img, (setup_drag['px'] - 32, setup_drag['py'] - 32))
    #Error message (if any)
    if setup_error_message:
        now = pygame.time.get_ticks()
        if setup_error_timer is None:
            setup_error_timer = now
        #Clear after 2500 ms
        if now - setup_error_timer > 2500:
            setup_error_message = None
            setup_error_timer = None
        else:
            error_msg = pygame.font.SysFont(None, 32)
            label = error_msg.render(setup_error_message, True, (150, 0, 0))
            popup_w = label.get_width() + 40
            popup_h = label.get_height() + 20
            offset_x = 130
            popup_x = (width // 2 - popup_w // 2) - offset_x
            popup_y = 350
            popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)
            pygame.draw.rect(screen, "white", popup_rect, border_radius=10)
            pygame.draw.rect(screen, "Black", popup_rect, 2, border_radius=10)
            screen.blit(label, (popup_rect.centerx - label.get_width() // 2,
                                popup_rect.centery - label.get_height() // 2))
    return board_rect, tray_rects, back_btn, reset_btn, proceed_btn, confirm_rects, choose_rects

#Pawn promotion function
def check_pawn_promotion():
    white_promotion = False
    black_promotion = False
    promotion_index = 100
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn' and white_location[i][1] == 0:
            white_promotion = True
            promotion_index = i
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn' and black_location[i][1] == 7:
            black_promotion = True
            promotion_index = i
    return white_promotion, black_promotion, promotion_index

def draw_pawn_promotion():
    pygame.draw.rect(screen, "#9BDD7B", (150, 275, 500, 200))
    if white_promo:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            piece_image = white_pieces_images[piece]
            x = 180 + i * 120
            y = 325
            screen.blit(piece_image, (x, y))
    elif black_promo:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            piece_image = black_pieces_images[piece]
            x = 180 + i * 120
            y = 325
            screen.blit(piece_image, (x, y))
    pygame.draw.rect(screen, "dark green", (150, 275, 500, 200), 6)

#Check if castling is legal
def check_castling(color, king_pos):
    global white_pieces, white_location, black_pieces, black_location
    global white_moved, black_moved
    castling_moves = []
    if color == "white":
        pieces, locs, moved = white_pieces, white_location, white_moved
        opp_pieces, opp_locs = black_pieces, black_location
        rank = 7
    else:
        pieces, locs, moved = black_pieces, black_location, black_moved
        opp_pieces, opp_locs = white_pieces, white_location
        rank = 0
    if "king" not in pieces:
        return []
    king_idx = pieces.index("king")
    if moved[king_idx]:
        return [] #King has moved before
    #King must not currently be in check
    opp_opts = check_options(opp_pieces, opp_locs, "white" if color == "black" else "black", include_castling=False)
    if is_in_check(pieces, locs, opp_opts, color):
        return []
    kx, ky = king_pos
    #To test one side (target_king_x = 6 for kingside, 2 for queenside)
    def test_side(target_king_x):
        #Rook final square after castling
        rook_final_x = 5 if target_king_x == 6 else 3
        #Find rook candidate on the correct side (closest)
        if target_king_x == 6:
            rook_candidates = [(i, x) for i, (x, y) in enumerate(locs)
                               if pieces[i] == "rook" and y == rank and not moved[i] and x > kx]
            if not rook_candidates:
                return False
            rook_idx, rook_x = min(rook_candidates, key=lambda t: t[1])
        else:
            rook_candidates = [(i, x) for i, (x, y) in enumerate(locs)
                               if pieces[i] == "rook" and y == rank and not moved[i] and x < kx]
            if not rook_candidates:
                return False
            rook_idx, rook_x = max(rook_candidates, key=lambda t: t[1])

        #Compute minimal inclusive interval that contains king_initial, king_final, rook_initial, rook_final
        min_x = min(kx, target_king_x, rook_x, rook_final_x)
        max_x = max(kx, target_king_x, rook_x, rook_final_x)
        #Ensure all squares in the interval are empty except possibly king or the castling rook
        for x in range(min_x, max_x + 1):
            sq = (x, rank)
            if sq in locs:
                #If occupied either it must be the king or the chosen rook
                if sq != (kx, ky) and sq != (rook_x, rank):
                    return False
            if sq in opp_locs:
                return False
        #Compute the exact squares the king will traverse (including start and final)
        step = 1 if target_king_x > kx else -1
        king_path = []
        x = kx
        while True:
            king_path.append((x, rank))
            if x == target_king_x:
                break
            x += step
        #Ensure none of the king_path squares is attacked
        for sq in king_path:
            #Simulate king at sq on the locations
            temp_locs = locs.copy()
            temp_locs[king_idx] = sq
            opp_opts2 = check_options(opp_pieces, opp_locs, "white" if color == "black" else "black", include_castling=False)
            if is_in_check(pieces, temp_locs, opp_opts2, color):
                return False
        return True
    #Test kingside
    if test_side(6):
        castling_moves.append((6, rank))
    #Test queenside
    if test_side(2):
        castling_moves.append((2, rank))

    return castling_moves

#Handle castling move execution
def handle_castling(color, selected_piece, clicked_coord):
    global white_location, black_location, white_pieces, black_pieces
    global white_moved, black_moved
    if color == "white":
        pieces, locs, moved = white_pieces, white_location, white_moved
        rank = 7
    else:
        pieces, locs, moved = black_pieces, black_location, black_moved
        rank = 0
    king_idx = selected_piece
    kx, ky = locs[king_idx]
    #Kingside castling (to g-file)
    if clicked_coord == (6, rank):
        rook_idx = min((i for i, (x, y) in enumerate(locs)
                if pieces[i] == "rook" and y == rank and x > kx),
               key=lambda i: locs[i][0])
        locs[rook_idx] = (5, rank) 
        locs[king_idx] = clicked_coord
        moved[rook_idx] = True
        moved[king_idx] = True
    #Queenside castling
    elif clicked_coord == (2, rank):
        rook_idx = max((i for i, (x, y) in enumerate(locs)
                if pieces[i] == "rook" and y == rank and x < kx),
               key=lambda i: locs[i][0])
        locs[rook_idx] = (3, rank) 
        locs[king_idx] = clicked_coord
        moved[rook_idx] = True
        moved[king_idx] = True

#Check if stalemate has occurred
def check_stalemate(turn):
    if turn == 'white':
        if not is_in_check(white_pieces, white_location, black_options, 'white'):
            for i, moves in enumerate(white_options):
                safe_moves = filter_moves(i, moves, white_pieces, white_location,
                                          black_pieces, black_location, black_options, 'white')
                if safe_moves:  #White still has a valid move
                    return False
            return True
    else:  #Check if black has a valid move
        if not is_in_check(black_pieces, black_location, white_options, 'black'):
            for i, moves in enumerate(black_options):
                safe_moves = filter_moves(i, moves, black_pieces, black_location,
                                          white_pieces, white_location, white_options, 'black')
                if safe_moves:
                    return False
            return True
    return False

#Check for fifty-move rule draw
def check_fifty_move_draw():
    global halfmove_clock, winner, game_over, status_message
    if halfmove_clock >= 100:  #100 halfmoves = 50 full moves
        winner, game_over = "Draw", True
        status_message = "Draw by 50-move rule!"
        return True
    return False

#Check for insufficient material draw
def check_insufficient_material():
    global winner, game_over, status_message
    pieces = white_pieces + black_pieces
    if pieces == ['king', 'king']:
        winner, game_over = "Draw", True
        status_message = "Draw by insufficient material!"
        return True
    elif len(pieces) == 3 and pieces.count('king') == 2 and ('bishop' in pieces or 'knight' in pieces):
            winner, game_over = "Draw", True
            status_message = "Draw by insufficient material!"
            return True
    elif len(pieces) == 4 and pieces.count('king') == 2 and pieces.count('bishop') == 2:
            white_bishop_squares = [white_location[i] for i, p in enumerate(white_pieces) if p == 'bishop']
            black_bishop_squares = [black_location[i] for i, p in enumerate(black_pieces) if p == 'bishop']
            if len(white_bishop_squares) == 1 and len(black_bishop_squares) == 1:
                winner, game_over = "Draw", True
                status_message = "Draw by insufficient material!"
                return True
    elif len(pieces) == 4 and pieces.count('king') == 2 and pieces.count('knight') == 2:
        winner, game_over = "Draw", True 
        status_message = "Draw by insufficient material!"
        return True
    elif len(pieces) == 4 and pieces.count('king') == 2 and pieces.count('knight') == 1 and pieces.count('bishop') == 1:
        return True
    return False

#Check if the starting posture is insufficient material
def is_insufficient(wp, wl, bp, bl):
    pieces = wp + bp 
    if len(pieces) == 2 and pieces.count('king') == 2:
        return True
    elif len(pieces) == 3 and pieces.count('king') == 2 and ('bishop' in pieces or 'knight' in pieces):
        return True
    elif len(pieces) == 4 and pieces.count('king') == 2 and pieces.count('bishop') == 2:
        return True
    elif len(pieces) == 4 and pieces.count('king') == 2 and pieces.count('knight') == 2:
        return True
    elif len(pieces) == 4 and pieces.count('king') == 2 and pieces.count('knight') == 1 and pieces.count('bishop') == 1:
        return True
    return False

#Check for threefold repetition draw
def threefold_repetition():
    global board_history, winner, game_over, status_message
    current_board = (tuple(white_pieces), tuple(white_location), tuple(black_pieces), tuple(black_location))
    board_history.append(current_board)
    if board_history.count(current_board) >= 3:
        winner, game_over = "Draw", True
        status_message = "Draw by threefold repetition!"
        return True
    return False

#Function to set up a Chess960 game
def chess960_play():
    global white_pieces, black_pieces, white_location, black_location
    global white_moved, black_moved, captured_white_pieces, captured_black_pieces
    global turn_step, selected_piece, winner, game_over, status_message, draw_activated, board_history
    global white_rooks_start, black_rooks_start
    global chess960_backrow

    #Reset everything
    captured_white_pieces = []
    captured_black_pieces = []
    turn_step = 0
    selected_piece = 100
    winner = None
    game_over = False
    status_message = None
    draw_activated = False
    board_history = []

    #Pawns are fixed
    white_pieces = ["pawn"] * 8
    black_pieces = ["pawn"] * 8
    white_location = [(i, 6) for i in range(8)]
    black_location = [(i, 1) for i in range(8)]

    #Generate Chess960 back row
    if chess960_backrow is None:
        chess960_backrow = generate_chess960_backrow()

    #Add pieces to full lists
    white_pieces = chess960_backrow + white_pieces
    black_pieces = chess960_backrow + black_pieces
    white_location = [(i, 7) for i in range(8)] + white_location
    black_location = [(i, 0) for i in range(8)] + black_location

    white_moved = [False] * len(white_pieces)
    black_moved = [False] * len(black_pieces)
    white_rooks_start = [x for x, piece in enumerate(chess960_backrow) if piece == "rook"]
    black_rooks_start = [x for x, piece in enumerate(chess960_backrow) if piece == "rook"]

#To randomly generate a valid Chess960 backrow
def generate_chess960_backrow():
    pieces = [None] * 8
    squares = list(range(8))

    #Place bishops on opposite colors
    b1 = random.choice([0, 2, 4, 6])
    b2 = random.choice([1, 3, 5, 7])
    pieces[b1], pieces[b2] = "bishop", "bishop"
    squares.remove(b1)
    squares.remove(b2)

    #Place queen
    q = random.choice(squares)
    pieces[q] = "queen"
    squares.remove(q)

    #Place knights
    for _ in range(2):
        n = random.choice(squares)
        pieces[n] = "knight"
        squares.remove(n)

    #Place king and rooks
    squares.sort()
    #Pick a king position not at the edges
    king_candidates = [s for s in squares if s != squares[0] and s != squares[-1]]
    king_pos = random.choice(king_candidates)
    pieces[king_pos] = "king"

    #Place rooks: one left of king, one right of king
    left_rook = random.choice([s for s in squares if s < king_pos])
    right_rook = random.choice([s for s in squares if s > king_pos])
    pieces[left_rook] = "rook"
    pieces[right_rook] = "rook"

    return pieces

#Draw valid moves on the board
def draw_valid_moves(valid_moves):
    color = 'yellow' if turn_step < 2 else 'red'
    inner, sqw, sqh, offx, offy = get_board_geometry(board_rect)
    for x, y in valid_moves:
        #Calculate the center of the square using the same system as pieces
        center_x = int(offx + x * sqw + sqw // 2)
        center_y = int(offy + y * sqh + sqh // 2)
        pygame.draw.circle(screen, color, (center_x, center_y), 7.5) #7.5 is radius of the circle  

#Draw the captured pieces
def draw_captured_pieces():
    board_size = board_rect.width
    x_offset_white, x_offset_black = 20, 165
    y_offset, spacing_y = 80, 40
    spacing_x_white, spacing_x_black = 50, 45
    
    #Fit into one row cell; keep governor "small" as-is
    max_cell = min(spacing_y - 5, spacing_x_white - 10, spacing_x_black - 10)
    def cap_img(color, piece):
        src = (white_pieces_small_images if color == 'white' else black_pieces_small_images)[piece]
        if current_piece_set.lower() == 'governor':
            return src
        return pygame.transform.smoothscale(src, (max_cell, max_cell))

    #Draw captured white pieces (right of board, top)
    for i, piece in enumerate(captured_white_pieces):
        img = white_images.get(piece + "_small", white_images.get(piece))
        col, row = i % 2, i // 2
        x = board_size + x_offset_white + col * spacing_x_black
        y = y_offset + row * spacing_y
        screen.blit(cap_img('white', piece), (x, y))
        
    #Draw a vertical line to separate sections
    line_x = board_size + 140 #140 spacing so that it is balanced
    pygame.draw.line(screen, "lime green", (line_x, 0), (line_x, 720), 4)
    
    #Draw captured black pieces (right of board, below white)
    for i, piece in enumerate(captured_black_pieces):
        col, row = i % 2, i // 2
        x = board_size + x_offset_black + col * spacing_x_white #To draw two pieces per row
        y = y_offset + row * spacing_y
        screen.blit(cap_img('black', piece), (x, y))

#Draw check status if needed
def draw_check(board_rect):
    global counter, game_over, winner, in_check
    checkmate = False
    check_text = None
    king_square = None

    if game_over:
        return False
    
    if turn_step < 2:  #White’s turn
        in_check = is_in_check(white_pieces, white_location, black_options, 'white')
        if in_check:
            if check_checkmate('white'):
                checkmate = True
                winner, game_over = "Black", True
                check_text = big_font.render('Checkmate! Black wins!', True, 'red')
                king_square = white_location[white_pieces.index('king')]
            else:
                check_text = big_font.render('White King is in Check!', True, 'red')
                king_square = white_location[white_pieces.index('king')]

    else:               #Black’s turn
        in_check = is_in_check(black_pieces, black_location, white_options, 'black')
        if in_check:
            if check_checkmate('black'):
                checkmate = True
                winner, game_over = "White", True
                check_text = big_font.render('Checkmate! White wins!', True, 'red')
                king_square = black_location[black_pieces.index('king')]
            else:
                check_text = big_font.render('Black King is in Check!', True, 'red')
                king_square = black_location[black_pieces.index('king')]

    if in_check:
        #Draw flashing highlight on king square
        inner, sqw, sqh, offx, offy = get_board_geometry(board_rect)
        x, y = king_square
        square_x = offx + int(x * sqw)
        square_y = offy + int(y * sqh)
        if counter % 30 < 15:
            pygame.draw.rect(screen, 'red', (square_x, square_y, sqw, sqh), 6)
        screen.blit(check_text, (board_rect.width // 2 - check_text.get_width() // 4, height - 60))
        counter += 1
        return True
    return False

#Restart the game function
def restart_game():
    global white_pieces, black_pieces, white_location, black_location, white_moved, black_moved, board_history
    global captured_white_pieces, captured_black_pieces, turn_step, selected_piece, winner, game_over, draw_activated
    global status_message
    global game_mode
    global chess960_backrow
    global setup_start_turn
    
    #If the game mode is custom, reset back to the setup position
    if game_mode == "custom" and setup_white_pieces:
        #Restore from the most recent setup
        white_pieces[:] = setup_white_pieces[:]
        white_location[:] = setup_white_location[:]
        black_pieces[:] = setup_black_pieces[:]
        black_location[:] = setup_black_location[:]
        white_moved[:] = [False] * len(white_pieces)
        black_moved[:] = [False] * len(black_pieces)
        captured_white_pieces[:] = []
        captured_black_pieces[:] = []
        board_history[:] = []
        winner = None
        game_over = False
        status_message = None
        draw_activated = False
        #Restore starting turn if available
        try:
            turn_step = setup_start_turn
        except NameError:
            turn_step = 0
        selected_piece = 100
        white_options[:] = check_options(white_pieces, white_location, 'white')
        black_options[:] = check_options(black_pieces, black_location, 'black')
        if turn_step <= 1:
            if check_checkmate('white'):
                winner, game_over = "Black", True
                status_message = "Checkmate! Black wins!"
            elif check_stalemate('white'):
                winner, game_over = "Draw", True
                status_message = "Stalemate! It's a draw!"
            elif check_stalemate('black'):
                winner, game_over = "Draw", True
                status_message = "Stalemate! It's a draw!"
        elif turn_step > 1:
            if check_checkmate('black'):
                winner, game_over = "Black", True
                status_message = "Checkmate! White wins!"
            elif check_stalemate('white'):
                winner, game_over = "Draw", True
                status_message = "Stalemate! It's a draw!"
            elif check_stalemate('black'):
                winner, game_over = "Draw", True
                status_message = "Stalemate! It's a draw!"
        return
    
    if game_mode == "chess960":
        #Reset backrow to force new shuffle each restart
        chess960_backrow = generate_chess960_backrow()
        chess960_play()
        return
    
    elif game_mode == "classical":
        white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        white_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        white_moved = [False, False, False, False, False, False, False, False,
                    False, False, False, False, False, False, False, False]
        black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook', 
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        black_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        black_moved = [False, False, False, False, False, False, False, False,
                    False, False, False, False, False, False, False, False]
        captured_white_pieces = []
        captured_black_pieces = []
        turn_step = 0
        selected_piece = 100
        winner = None
        game_over = False
        status_message = None
        draw_activated = False
        board_history = []

#Main game loop
black_options = check_options(black_pieces, black_location, 'black')
white_options = check_options(white_pieces, white_location, 'white')
white_location_before = None
running = True

#Resign and restart button rectangles
white_resign_btn = pygame.Rect(width - 120, 35, 100, 30)
black_resign_btn = pygame.Rect(width - 265, 35, 100, 30)
restart_btn      = pygame.Rect(width - 135, height - 70, 120, 50)
play_back_btn = pygame.Rect(10, height - 70, 80, 50)

#Offer draw button
offer_draw_btn = pygame.Rect(width - 220, height - 120, 160, 40)
draw_offer_active = False
draw_offer_turn = None
draw_activated = False

while running:
    captured_flag = False
    timer.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Menu state
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, name in menu_buttons:
                    if rect.collidepoint(event.pos):
                        if name == "Play":
                            game_state = "play"
                            if game_mode == "classical":
                                restart_game()
                                white_options = check_options(white_pieces, white_location, 'white')
                                black_options = check_options(black_pieces, black_location, 'black')
                            elif game_mode == "chess960":
                                chess960_play()
                                white_options = check_options(white_pieces, white_location, 'white')
                                black_options = check_options(black_pieces, black_location, 'black')
                        else:
                            game_state = name.lower()
        elif game_state == "memes":
            memes_back_btn, popup_buttons, min_offset, max_offset = draw_memes()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if selected_meme is None:
                    if memes_back_btn.collidepoint(event.pos):
                        game_state = "menu"
                    else:
                        for i, rect in enumerate(meme_rects):
                            if rect.collidepoint(event.pos):
                                selected_meme = i
                else:
                    if popup_buttons["back"].collidepoint(event.pos):
                        selected_meme = None
                    elif popup_buttons["left"].collidepoint(event.pos):
                        selected_meme = (selected_meme - 1) % len(meme_images)
                    elif popup_buttons["right"].collidepoint(event.pos):
                        selected_meme = (selected_meme + 1) % len(meme_images)
            elif event.type == pygame.MOUSEWHEEL and selected_meme is None:
                scroll_offset += event.y * 40
                scroll_offset = min(min_offset, max(max_offset, scroll_offset))
            elif event.type == pygame.KEYDOWN:
                if selected_meme is not None:
                    if event.key == pygame.K_ESCAPE:
                        selected_meme = None
                    elif event.key == pygame.K_LEFT:
                        selected_meme = (selected_meme - 1) % len(meme_images)
                    elif event.key == pygame.K_RIGHT:
                        selected_meme = (selected_meme + 1) % len(meme_images)
                else:
                    if event.key == pygame.K_DOWN:
                        scroll_offset -= 40
                    elif event.key == pygame.K_UP:
                        scroll_offset += 40
                    scroll_offset = min(min_offset, max(max_offset, scroll_offset))
        elif game_state == "play":
            if event.type == pygame.QUIT:
                running = False
            #Restart with Enter key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                restart_game()
                white_options = check_options(white_pieces, white_location, 'white')
                black_options = check_options(black_pieces, black_location, 'black')
            #Mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Chess960 castling choice popup
                if castle_choice_active:
                    if castle_btn.collidepoint(event.pos):
                        color, king_idx, rook_idx, target = castle_choice_data
                        handle_castling(color, king_idx, target)
                        moved_piece = 'king'
                        captured_flag = False
                        white_options = check_options(white_pieces, white_location, 'white')
                        black_options = check_options(black_pieces, black_location, 'black')
                        #Reset en passant for opponent
                        if color == 'white':
                            black_en_passant = (100,100)
                            turn_step = 2
                        else:
                            white_en_passant = (100,100)
                            turn_step = 0
                        #Update halfmove clock (castling is not pawn/capture)
                        halfmove_clock += 1
                        if check_fifty_move_draw():
                            draw_activated = True
                        if threefold_repetition():
                            draw_activated = True
                        if check_insufficient_material():
                            draw_activated = True
                        if color == 'white':
                            if check_checkmate('black'):
                                winner, game_over = "White", True
                            if check_stalemate('black'):
                                winner, game_over = "Draw", True; status_message = "Stalemate! It's a draw!"
                        else:
                            if check_checkmate('white'):
                                winner, game_over = "Black", True
                            if check_stalemate('white'):
                                winner, game_over = "Draw", True; status_message = "Stalemate! It's a draw!"
                        castle_choice_active = False
                        castle_choice_data = None
                        selected_piece = 100
                        continue 
                    elif rook_btn.collidepoint(event.pos):
                        color, king_idx, rook_idx, target = castle_choice_data
                        selected_piece = rook_idx
                        turn_step = 1 if color == 'white' else 3
                        castle_choice_active = False
                        castle_choice_data = None
                        continue
                if play_back_btn.collidepoint(event.pos):
                    #If it is a custom game, go back custom setup
                    if game_mode == "custom":
                        game_state = "custom_setup"
                    else:
                        game_state = "menu"
                if white_promo or black_promo:
                    x, y = event.pos
                    if 150 <= x <= 650 and 275 <= y <= 475:
                        index = (x - 180) // 120
                        if white_promo and 0 <= index < len(white_promotions):
                            white_pieces[promo_index] = white_promotions[index]
                            #Reset promotion state
                            white_promo = False
                            black_promo = False
                        elif black_promo and 0 <= index < len(black_promotions):
                            black_pieces[promo_index] = black_promotions[index]
                            white_promo = False
                            black_promo = False
                        black_options = check_options(black_pieces, black_location, 'black')
                        white_options = check_options(white_pieces, white_location, 'white')
                if restart_btn.collidepoint(event.pos):
                    restart_game()
                    black_options = check_options(black_pieces, black_location, 'black')
                    white_options = check_options(white_pieces, white_location, 'white')
            #White resigns only on White's turn
                if white_resign_btn.collidepoint(event.pos) and turn_step < 2 and not game_over:
                    winner, game_over = "Black", True
                    status_message = 'White resigned. Black wins!'
            #Black resigns only on Black's turn
                if black_resign_btn.collidepoint(event.pos) and turn_step >= 2 and not game_over:
                    winner, game_over = "White", True
                    status_message = 'Black resigned, White wins!'
            #Accepts/declines a draw
                if draw_offer_active:
                    if accept_btn.collidepoint(event.pos):
                        draw_activated = True
                        winner, game_over = "Draw", True
                        status_message = "Draw by agreement!"
                        draw_offer_active = False
                    elif decline_btn.collidepoint(event.pos):
                        draw_offer_active = False
            #Offer a draw
                if offer_draw_btn.collidepoint(event.pos) and not draw_offer_active:
                    if (turn_step < 2 and not game_over):  #White offers the draw
                        draw_offer_active = True
                        draw_offer_turn = 'white'
                    elif (turn_step >= 2 and not game_over):  #Black offers the draw
                        draw_offer_active = True
                        draw_offer_turn = 'black'             
            #Normal game    
                x_coord, y_coord = event.pos[0], event.pos[1]
                clicked_coord = (x_coord // 86, y_coord // 86)
                if turn_step <= 1 and not game_over:
                    if turn_step == 0 and clicked_coord in white_location:
                        selected_piece = white_location.index(clicked_coord)
                        turn_step = 1
                    elif turn_step == 1 and not game_over:
                        #If clicking another white piece, change selection
                        if clicked_coord in white_location:
                            piece_idx = white_location.index(clicked_coord)
                            piece_name = white_pieces[piece_idx]
                            #Check if this rook can castle with its king
                            king_idx = white_pieces.index("king")
                            king_pos = white_location[king_idx]
                            legal_castles = check_castling("white", king_pos)
                            #If there’s a castling option that involves this rook (adjacent)
                            if legal_castles and piece_name in ("rook", "king"):
                                for target in legal_castles:
                                    tx = target[0]
                                    if tx == 6:   #Kingside
                                        rook_candidates = [(i, x) for i,(x,y) in enumerate(white_location)
                                                        if white_pieces[i] == "rook" and y == 7 and not white_moved[i] and x > king_pos[0]]
                                        if not rook_candidates:
                                            continue
                                        rook_idx = min(rook_candidates, key=lambda t: t[1])[0]
                                    else:         #Queenside
                                        rook_candidates = [(i, x) for i,(x,y) in enumerate(white_location)
                                                        if white_pieces[i] == "rook" and y == 7 and not white_moved[i] and x < king_pos[0]]
                                        if not rook_candidates:
                                            continue
                                        rook_idx = max(rook_candidates, key=lambda t: t[1])[0]
                                    if white_location[rook_idx] == clicked_coord or clicked_coord == target:
                                        castle_choice_active = True
                                        castle_choice_data = ("white", king_idx, rook_idx, target)
                                        break
                            selected_piece = piece_idx
                        #If clicking a valid move, move the piece
                        elif selected_piece != 100 and clicked_coord in check_valid_moves():
                            piece_name = white_pieces[selected_piece]
                            old_coord = white_location[selected_piece]
                            #Check for castling
                            legal_castles = check_castling("white", old_coord)
                            if piece_name == "king" and clicked_coord in legal_castles:
                                #Execute castling
                                handle_castling("white", selected_piece, clicked_coord)
                                moved_piece = "king"
                                captured_flag = False
                            #Handle en passant capture
                            else:
                                white_en_passant = check_en_passant(old_coord, clicked_coord) if piece_name == 'pawn' else (100,100)
                                white_location[selected_piece] = clicked_coord
                                white_moved[selected_piece] = True
                                moved_piece = piece_name
                                if piece_name == 'pawn' and clicked_coord == black_en_passant: #En passant capture
                                        captured_flag = True
                                        captured_black = black_location.index((clicked_coord[0], clicked_coord[1] + 1))
                                        captured_black_pieces.append(black_pieces[captured_black])
                                        del black_pieces[captured_black]
                                        del black_location[captured_black]
                                        del black_moved[captured_black]
                                if clicked_coord in black_location:
                                    captured_flag = True
                                    captured_black = black_location.index(clicked_coord)
                                    captured_black_pieces.append(black_pieces[captured_black])
                                    del black_pieces[captured_black]
                                    del black_location[captured_black]
                                    del black_moved[captured_black]
                                if "king" not in black_pieces:
                                    winner, game_over = "White", True
                                    status_message = "Black king captured! White wins!"
                            turn_step = 2
                            selected_piece = 100
                            #Update valid moves after move
                            white_options = check_options(white_pieces, white_location, 'white')
                            black_options = check_options(black_pieces, black_location, 'black')
                            if moved_piece != 'pawn' or not (white_en_passant != (100,100)):
                                black_en_passant = (100,100) #Reset en passant
                            if moved_piece == 'pawn' or captured_flag:  #Reset halfmove clock on pawn move or capture
                                halfmove_clock = 0
                            else:
                                halfmove_clock += 1
                            if check_fifty_move_draw():
                                draw_activated = True
                            if threefold_repetition():
                                draw_activated = True
                            if check_insufficient_material():
                                draw_activated = True
                            #Check if Black is in checkmate after White's move
                            if check_checkmate('black'):
                                winner, game_over = "White", True
                            if check_stalemate('black'):
                                winner, game_over = "Draw", True
                                status_message = "Stalemate! It's a draw!"
                            if "king" not in black_pieces:
                                winner, game_over = "White", True
                                status_message = "Black king captured! White wins!"
                else:
                    if turn_step == 2 and clicked_coord in black_location and not game_over:
                        selected_piece = black_location.index(clicked_coord)
                        turn_step = 3
                    elif turn_step == 3 and not game_over:
                        #If clicking another black piece, change selection
                        if clicked_coord in black_location:
                            piece_idx = black_location.index(clicked_coord)
                            piece_name = black_pieces[piece_idx]
                            king_idx = black_pieces.index("king")
                            king_pos = black_location[king_idx]
                            legal_castles = check_castling("black", king_pos)
                            if legal_castles and piece_name in ("rook", "king"):
                                for target in legal_castles:
                                    tx = target[0]
                                    if tx == 6:   #Kingside
                                        rook_candidates = [(i, x) for i,(x,y) in enumerate(black_location)
                                                        if black_pieces[i] == "rook" and y == 0 and not black_moved[i] and x > king_pos[0]]
                                        if not rook_candidates:
                                            continue
                                        rook_idx = min(rook_candidates, key=lambda t: t[1])[0]
                                    else:         #Queenside
                                        rook_candidates = [(i, x) for i,(x,y) in enumerate(black_location)
                                                        if black_pieces[i] == "rook" and y == 0 and not black_moved[i] and x < king_pos[0]]
                                        if not rook_candidates:
                                            continue
                                        rook_idx = max(rook_candidates, key=lambda t: t[1])[0]
                                    if black_location[rook_idx] == clicked_coord or clicked_coord == target:
                                        castle_choice_active = True
                                        castle_choice_data = ("black", king_idx, rook_idx, target)
                                        break
                            selected_piece = piece_idx
                        #If clicking a valid move, move the piece
                        elif selected_piece != 100 and clicked_coord in check_valid_moves():
                            piece_name = black_pieces[selected_piece]
                            old_coord = black_location[selected_piece]
                            #Check for castling
                            legal_castles = check_castling("black", old_coord)
                            if piece_name == "king" and clicked_coord in legal_castles:
                                #Execute castling
                                handle_castling("black", selected_piece, clicked_coord)
                                moved_piece = "king"
                                captured_flag = False
                            #Handle en passant capture
                            else:
                                black_en_passant = check_en_passant(old_coord, clicked_coord) if piece_name == 'pawn' else (100,100)
                                black_location[selected_piece] = clicked_coord
                                black_moved[selected_piece] = True
                                moved_piece = piece_name
                                if piece_name == 'pawn' and clicked_coord == white_en_passant: #En passant capture
                                        captured_flag = True
                                        captured_white = white_location.index((clicked_coord[0], clicked_coord[1] - 1))
                                        captured_white_pieces.append(white_pieces[captured_white])
                                        del white_pieces[captured_white]
                                        del white_location[captured_white]
                                        del white_moved[captured_white]
                                if clicked_coord in white_location:
                                    captured_flag = True
                                    captured_white = white_location.index(clicked_coord)
                                    captured_white_pieces.append(white_pieces[captured_white])
                                    del white_pieces[captured_white]
                                    del white_location[captured_white]
                                    del white_moved[captured_white]
                            turn_step = 0
                            selected_piece = 100
                            #Update valid moves after move
                            white_options = check_options(white_pieces, white_location, 'white')
                            black_options = check_options(black_pieces, black_location, 'black')
                            if moved_piece != 'pawn' or not (black_en_passant != (100,100)):
                                white_en_passant = (100,100) #Reset en passant
                            if moved_piece == 'pawn' or captured_flag:  #Reset halfmove clock on pawn move or capture
                                halfmove_clock = 0
                            else:
                                halfmove_clock += 1
                            if check_fifty_move_draw():
                                draw_activated = True
                            if threefold_repetition():
                                draw_activated = True
                            if check_insufficient_material():
                                draw_activated = True
                            #Check if White is in checkmate after Black's move
                            if check_checkmate('white'):
                                winner, game_over = "Black", True
                            if check_stalemate('white'):
                                winner, game_over = "Draw", True
                                status_message = "Stalemate! It's a draw!"
                            if "king" not in white_pieces:
                                winner, game_over = "Black", True
                                status_message = "White king captured! Black wins!"
        elif game_state == "credits":
            credits_back_btn, email_rect, clickable_links, min_offset, max_offset = draw_credits()
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * 40
                scroll_offset = min(min_offset, max(max_offset, scroll_offset))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if credits_back_btn.collidepoint(event.pos):
                    game_state = "menu"
                    scroll_offset = 0
                elif email_rect and email_rect.collidepoint(event.pos):
                    pygame.scrap.init()
                    pygame.scrap.put(pygame.SCRAP_TEXT, b"hoongliang03@gmail.com")
                    status_message = "Email copied to clipboard!"
                    email_copied_timer = pygame.time.get_ticks()
                else:
                    for rect, link in clickable_links:
                        if rect.collidepoint(event.pos):
                            webbrowser.open(link)
        elif game_state == "customize":
            board_buttons, piece_buttons, game_mode_buttons, customize_back_btn, min_offset, max_offset = draw_customization()
            if event.type == pygame.MOUSEWHEEL:
                custom_scroll_y += event.y * 40
                custom_scroll_y = min(min_offset, max(max_offset, custom_scroll_y))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if customize_back_btn.collidepoint(event.pos):
                    game_state = "menu"
                for name, rect in board_buttons.items():
                    if rect.collidepoint(event.pos):
                        current_board_name = name
                        current_board_img = board_designs[name]
                for set_name, rect in piece_buttons.items():
                    if rect.collidepoint(event.pos):
                        current_piece_set = set_name
                        white_pieces_images = piece_sets[current_piece_set]["white"]
                        black_pieces_images = piece_sets[current_piece_set]["black"]
                        #Also update "small" dicts for captured pieces
                        white_pieces_small_images = {
                            p: piece_sets[current_piece_set]["white"].get(p + "_small", white_pieces_images[p])
                            for p in piece_names
                        }
                        black_pieces_small_images = {
                            p: piece_sets[current_piece_set]["black"].get(p + "_small", black_pieces_images[p])
                            for p in piece_names
                        }
                for mode, rect in game_mode_buttons.items():
                    if rect.collidepoint(event.pos):
                        game_mode = mode
                if customize_proceed_btn and customize_proceed_btn.collidepoint(event.pos) and game_mode == "custom":
                    #Clear any prior setup
                    setup_white_pieces.clear(); setup_white_location.clear()
                    setup_black_pieces.clear(); setup_black_location.clear()
                    setup_error_message = None; setup_reset_confirm = False; setup_choose_side = False; setup_drag = None
                    game_state = "custom_setup"
        elif game_state == "custom_setup":
            board_rect, tray_rects, back_btn2, reset_btn2, proceed_btn2, confirm_rects, choose_rects = draw_custom_setup()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if setup_choose_side and choose_rects:
                    #Popup: Choose which side moves first
                    whbtn, bkbtn = choose_rects
                    if whbtn.collidepoint(event.pos):
                        #White moves first
                        white_pieces[:] = setup_white_pieces[:]
                        white_location[:] = setup_white_location[:]
                        black_pieces[:] = setup_black_pieces[:]
                        black_location[:] = setup_black_location[:]
                        white_moved[:] = [False] * len(white_pieces)
                        black_moved[:] = [False] * len(black_pieces)
                        captured_white_pieces[:] = []
                        captured_black_pieces[:] = []
                        winner = None
                        game_over = False
                        status_message = None
                        draw_activated = False
                        board_history[:] = []
                        turn_step = 0
                        setup_start_turn = turn_step
                        selected_piece = 100
                        white_options[:] = check_options(white_pieces, white_location, 'white')
                        black_options[:] = check_options(black_pieces, black_location, 'black')
                        if "king" not in white_pieces:
                            winner, game_over = "Black", True
                            status_message = "White king missing! Black wins!"
                        elif "king" not in black_pieces:
                            winner, game_over = "White", True
                            status_message = "Black king missing! White wins!"
                        else:
                            if check_checkmate('white'):
                                winner, game_over = "Black", True
                                status_message = "Checkmate! Black wins!"
                            elif check_stalemate('white'):
                                winner, game_over = "Draw", True
                                status_message = "Stalemate! It's a draw!"
                            elif check_stalemate('black'):
                                winner, game_over = "Draw", True
                                status_message = "Stalemate! It's a draw!"
                        game_state = "play"
                        setup_choose_side = False
                    elif bkbtn.collidepoint(event.pos):
                        #Black moves first
                        white_pieces[:] = setup_white_pieces[:]
                        white_location[:] = setup_white_location[:]
                        black_pieces[:] = setup_black_pieces[:]
                        black_location[:] = setup_black_location[:]
                        white_moved[:] = [False] * len(white_pieces)
                        black_moved[:] = [False] * len(black_pieces)
                        captured_white_pieces[:] = []
                        captured_black_pieces[:] = []
                        winner = None
                        game_over = False
                        status_message = None
                        draw_activated = False
                        board_history[:] = []
                        turn_step = 2 
                        selected_piece = 100
                        setup_start_turn = turn_step
                        white_options[:] = check_options(white_pieces, white_location, 'white')
                        black_options[:] = check_options(black_pieces, black_location, 'black')
                        if "king" not in white_pieces:
                            winner, game_over = "Black", True
                            status_message = "White king missing! Black wins!"
                        elif "king" not in black_pieces:
                            winner, game_over = "White", True
                            status_message = "Black king missing! White wins!"
                        else:
                            if check_stalemate('white'):
                                winner, game_over = "Draw", True
                                status_message = "Stalemate! It's a draw!"
                            elif check_checkmate('black'):
                                winner, game_over = "White", True
                                status_message = "Checkmate! White wins!"
                            elif check_stalemate('black'):
                                winner, game_over = "Draw", True
                                status_message = "Stalemate! It's a draw!"
                        game_state = "play"
                        setup_choose_side = False
                elif setup_reset_confirm and confirm_rects:
                    #Popup: Confirm reset
                    ybtn, nbtn = confirm_rects
                    if ybtn.collidepoint(event.pos):
                        setup_white_pieces.clear()
                        setup_white_location.clear()
                        setup_black_pieces.clear()
                        setup_black_location.clear()
                        setup_reset_confirm = False
                    elif nbtn.collidepoint(event.pos):
                        setup_reset_confirm = False
                else:
                    #Start dragging from trays
                    for color in ('white', 'black'):
                        for piece, r in tray_rects[color].items():
                            if r.collidepoint(event.pos):
                                setup_drag = {
                                    'color': color,
                                    'piece': piece,
                                    'dx': 0,
                                    'dy': 0,
                                    'px': event.pos[0],
                                    'py': event.pos[1]
                                }
                    #Or start dragging from board (pick up an existing piece)
                    if setup_drag is None:
                        sq = get_board_square_from_pixel(board_rect, *event.pos)
                        if sq:
                            if sq in setup_white_location:
                                idx = setup_white_location.index(sq)
                                piece = setup_white_pieces[idx]
                                setup_drag = {'color': 'white', 'piece': piece, 'dx': 0, 'dy': 0,
                                            'px': event.pos[0], 'py': event.pos[1]}
                                setup_white_pieces.pop(idx)
                                setup_white_location.pop(idx)
                            elif sq in setup_black_location:
                                idx = setup_black_location.index(sq)
                                piece = setup_black_pieces[idx]
                                setup_drag = {'color': 'black', 'piece': piece, 'dx': 0, 'dy': 0,
                                            'px': event.pos[0], 'py': event.pos[1]}
                                setup_black_pieces.pop(idx)
                                setup_black_location.pop(idx)
                    #Buttons
                    if back_btn2.collidepoint(event.pos):
                        game_state = "customize"
                    if reset_btn2.collidepoint(event.pos):
                        setup_reset_confirm = True
                    if proceed_btn2.collidepoint(event.pos):
                        # Validations
                        wk = setup_white_pieces.count('king')
                        bk = setup_black_pieces.count('king')
                        if wk != 1 or bk != 1:
                            setup_error_message = "Invalid chess position: Each side must have exactly one king."
                            setup_error_timer = pygame.time.get_ticks() 
                        else:
                            if is_insufficient(setup_white_pieces, setup_white_location,
                                            setup_black_pieces, setup_black_location):
                                winner = "Draw"
                                game_over = True
                                status_message = "Draw by insufficient material!"
                                draw_activated = True
                                white_pieces[:] = setup_white_pieces[:]
                                white_location[:] = setup_white_location[:]
                                black_pieces[:] = setup_black_pieces[:]
                                black_location[:] = setup_black_location[:]
                                white_moved[:] = [False] * len(white_pieces)
                                black_moved[:] = [False] * len(black_pieces)
                                captured_white_pieces[:] = []
                                captured_black_pieces[:] = []
                                board_history[:] = []
                                white_options[:] = check_options(white_pieces, white_location, 'white')
                                black_options[:] = check_options(black_pieces, black_location, 'black')
                                turn_step = 0
                                selected_piece = 100
                                #Remember the starting turn (so restart/back can reuse this)
                                setup_start_turn = turn_step
                                game_state = "play"
                            else:
                                setup_error_message = None
                                setup_choose_side = True
            elif event.type == pygame.MOUSEBUTTONUP:
                #Drop a dragged piece
                if setup_drag is not None:
                    sq = get_board_square_from_pixel(board_rect, *event.pos)
                    if sq:
                        #Replace any piece already there
                        if sq in setup_white_location:
                            i = setup_white_location.index(sq)
                            setup_white_location.pop(i)
                            setup_white_pieces.pop(i)
                        if sq in setup_black_location:
                            i = setup_black_location.index(sq)
                            setup_black_location.pop(i)
                            setup_black_pieces.pop(i)
                        if setup_drag['color'] == 'white':
                            setup_white_pieces.append(setup_drag['piece'])
                            setup_white_location.append(sq)
                        else:
                            setup_black_pieces.append(setup_drag['piece'])
                            setup_black_location.append(sq)
                    setup_drag = None
            elif event.type == pygame.MOUSEMOTION and setup_drag:
                    setup_drag['px'], setup_drag['py'] = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                #Right-click: clear a square
                sq = get_board_square_from_pixel(board_rect, *event.pos)
                if sq:
                    if sq in setup_white_location:
                        i = setup_white_location.index(sq)
                        setup_white_location.pop(i)
                        setup_white_pieces.pop(i)
                    elif sq in setup_black_location:
                        i = setup_black_location.index(sq)
                        setup_black_location.pop(i)
                        setup_black_pieces.pop(i)                
    #Drawing the game state
    if game_state == "menu":
        menu_buttons = draw_menu()
    elif game_state == "play":
        screen.fill('light gray')
        board_rect = draw_board(screen) #Draw board
        draw_pieces(board_rect) #Draw pieces on the board
        draw_captured_pieces() #Draw captured pieces
        #Draw buttons
        pygame.draw.rect(screen, "#9CAF88", white_resign_btn)
        pygame.draw.rect(screen, "darkgreen", black_resign_btn)
        pygame.draw.rect(screen, "green", restart_btn)
        pygame.draw.rect(screen, "orange", offer_draw_btn)
        pygame.draw.rect(screen, "darkred", play_back_btn, border_radius=8)
        
        play_back_text = pygame.font.SysFont(None, 40).render("Back", True, "white")
        button_font = pygame.font.SysFont(None, 30)
        screen.blit(button_font.render("Resign", True, "black"), white_resign_btn.move(17, 6)) #White resign words
        screen.blit(button_font.render("Resign", True, "white"), black_resign_btn.move(15, 6)) #Black resign words
        screen.blit(button_font.render("Restart", True, "black"), restart_btn.move(25, 15))
        screen.blit(button_font.render("Offer Draw", True, "black"), offer_draw_btn.move(28, 10))
        screen.blit(play_back_text, (play_back_btn.centerx - play_back_text.get_width()//2, play_back_btn.centery - play_back_text.get_height()//2))
        check_drawn = draw_check(board_rect) #Draw check status if needed
        
        if castle_choice_active:
            popup_rect = pygame.Rect(width//2 - 150, height//2 - 80, 400, 140)
            pygame.draw.rect(screen, "#FFD966", popup_rect)
            msg = big_font.render("Castle or Move Rook?", True, "black")
            screen.blit(msg, (popup_rect.centerx - msg.get_width()//2, popup_rect.top + 20))

            castle_btn = pygame.Rect(popup_rect.left + 30, popup_rect.bottom - 60, 100, 40)
            rook_btn = pygame.Rect(popup_rect.right - 130, popup_rect.bottom - 60, 100, 40)
            pygame.draw.rect(screen, "green", castle_btn)
            pygame.draw.rect(screen, "blue", rook_btn)
            screen.blit(button_font.render("Castle", True, "white"), castle_btn.move(15, 10))
            screen.blit(button_font.render("Rook", True, "white"), rook_btn.move(25, 10))
        
        if not game_over:
            white_promo, black_promo, promo_index = check_pawn_promotion()
            if white_promo or black_promo:
                draw_pawn_promotion()
    
        if game_over:
            end_text_rect = pygame.Rect((board_rect.width - 300) // 2, (board_rect.height - 34) // 2, 300, 80)
            pygame.draw.rect(screen, "#DEE09B", end_text_rect)
            if (check_stalemate('black') or check_stalemate('white')) and ("king" in white_pieces and "king" in black_pieces):
                end_text = pygame.font.SysFont(None, 72).render("Stalemate!", True, "black")
            elif draw_activated or check_fifty_move_draw():
                end_text = pygame.font.SysFont(None, 72).render("Draw!", True, "black")
            else:
                end_text = pygame.font.SysFont(None, 72).render(f"{winner} wins!", True, "black")
            screen.blit(end_text, (board_rect.width // 2 - end_text.get_width() // 2, board_rect.height // 2))    
        
        if not check_drawn:
            #Draw status text if it is not in check
            font_size = int(75 * 0.72)
            font = pygame.font.SysFont(None, font_size)
            if status_message:  #If game over/resign message exists
                status = status_message
                status_surface = font.render(status, True, "#0D0082")
            else:
                status_text = [
                    'White: Select a piece to move', 
                    'White: Select the place to move the piece',
                    'Black: Select a piece to move',
                    'Black: Select the place to move the piece'
                ]
                status = status_text[turn_step % 4]
                status_surface = font.render(status, True, 'dark green')
            status_rect = status_surface.get_rect(center=((width//2) - 20, height - 45))
            screen.blit(status_surface, status_rect)
        
        if draw_offer_active:
            popup_rect = pygame.Rect((board_rect.width - 400)//2, (board_rect.height - 150)//2, 400, 150)
            pygame.draw.rect(screen, "#FFD966", popup_rect)
            msg = big_font.render(f"{draw_offer_turn.capitalize()} offers a draw", True, "black")
            screen.blit(msg, (popup_rect.centerx - msg.get_width()//2, popup_rect.top + 20))

            accept_btn = pygame.Rect(popup_rect.left + 60, popup_rect.bottom - 60, 100, 40)
            decline_btn = pygame.Rect(popup_rect.right - 160, popup_rect.bottom - 60, 100, 40)
            pygame.draw.rect(screen, "green", accept_btn)
            pygame.draw.rect(screen, "red", decline_btn)
            screen.blit(button_font.render("Accept", True, "white"), accept_btn.move(15, 10))
            screen.blit(button_font.render("Decline", True, "white"), decline_btn.move(15, 10))
        
        if selected_piece != 100:
            valid_moves = check_valid_moves() #Get valid moves for the selected piece
            draw_valid_moves(valid_moves) #Draw valid moves on the board

    pygame.display.flip()
pygame.quit()