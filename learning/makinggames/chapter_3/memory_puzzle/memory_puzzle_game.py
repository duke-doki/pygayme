import random, pygame, sys
from pygame.locals import *
from config import *



def generate_revealed_boxes_data(value) -> list:
    revealed_boxes = []
    for i in range(BOARDWIDTH):
        revealed_boxes.append([value] * BOARDHEIGHT)
    return revealed_boxes


def get_randomized_board() -> list[list]:
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    num_icons_used = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:num_icons_used] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def split_into_groups_of(group_size, the_list):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i + group_size])
    return result


def get_left_top_coords_of_box(box_x, box_y) -> tuple:
    # Convert board coordinates to pixel coordinates
    left = box_x * (BOXSIZE + GAPSIZE) + XMARGIN
    top = box_y * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def get_box_at_pixel(x, y) -> tuple:
    for box_x in range(BOARDWIDTH):
        for box_y in range(BOARDHEIGHT):
            left, top = get_left_top_coords_of_box(box_x, box_y)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(x, y):
                return box_x, box_y
    return None, None


def draw_icon(shape, color, box_x, box_y) -> None:
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = get_left_top_coords_of_box(box_x, box_y) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAY_SURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAY_SURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY_SURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAY_SURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAY_SURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAY_SURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY_SURF, color, (left, top + quarter, BOXSIZE, half))


def get_shape_and_color(board, box_x, box_y) -> tuple:
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[box_x][box_y][0], board[box_x][box_y][1]


def draw_box_covers(board, boxes, coverage) -> None:
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = get_left_top_coords_of_box(box[0], box[1])
        pygame.draw.rect(DISPLAY_SURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is a coverage
            pygame.draw.rect(DISPLAY_SURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPS_CLOCK.tick(FPS)


def reveal_boxes_animation(board, boxes_to_reveal) -> None:
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, -REVEALSPEED, -REVEALSPEED):
        draw_box_covers(board, boxes_to_reveal, coverage)


def cover_boxes_animation(board, boxes_to_cover) -> None:
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        draw_box_covers(board, boxes_to_cover, coverage)


def draw_board(board, revealed) -> None:
    # Draws all the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = get_left_top_coords_of_box(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAY_SURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = get_shape_and_color(board, boxx, boxy)
                draw_icon(shape, color, boxx, boxy)


def draw_highlight_box(box_x, box_y) -> None:
    left, top = get_left_top_coords_of_box(box_x, box_y)
    pygame.draw.rect(DISPLAY_SURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def start_game_animation(board)-> None:
    # Randomly reveal the boxes 8 at a time.
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = split_into_groups_of(8, boxes)

    draw_board(board, covered_boxes)
    for boxGroup in boxGroups:
        reveal_boxes_animation(board, boxGroup)
        cover_boxes_animation(board, boxGroup)


def game_won_animation(board) -> None:
    # flash the background color when the player has won
    coveredBoxes = generate_revealed_boxes_data(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAY_SURF.fill(color1)
        draw_board(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def has_won(revealed_boxes) -> bool:
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealed_boxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True


def main():
    global FPS_CLOCK, DISPLAY_SURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mouse_x, mouse_y  = 0, 0
    pygame.display.set_caption('Memory Puzzle')

    main_board = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None # stores the (x, y) of the first box clicked.

    DISPLAY_SURF.fill(BGCOLOR)
    start_game_animation(main_board)

    clicks = 0
    font = pygame.font.Font('freesansbold.ttf', 20)  # Font name and size

    while True: # main game loop
        mouse_clicked = False

        DISPLAY_SURF.fill(BGCOLOR) # drawing the window

        # Set up a font
        text_surface = font.render(f'Suggestions made: {clicks}', True,
                                   RED)  # Text, anti-aliasing, color
        text_rect = text_surface.get_rect()
        text_rect.center = (320, 435)
        DISPLAY_SURF.blit(text_surface, text_rect)

        draw_board(main_board, revealed_boxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

        box_x, box_y = get_box_at_pixel(mouse_x, mouse_y)
        if box_x is not None and box_y is not None:
            # The mouse is currently over a box.
            if not revealed_boxes[box_x][box_y]:
                draw_highlight_box(box_x, box_y)
            if not revealed_boxes[box_x][box_y] and mouse_clicked:
                reveal_boxes_animation(main_board, [(box_x, box_y)])
                revealed_boxes[box_x][box_y] = True # set the box as "revealed"
                if first_selection is None: # the current box was the first box clicked
                    first_selection = (box_x, box_y)
                else:
                    # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    clicks += 1
                    icon_1_shape, icon_1_color = get_shape_and_color(main_board, first_selection[0], first_selection[1])
                    icon_2_shape, icon_2_color = get_shape_and_color(main_board, box_x, box_y)

                    if icon_1_shape != icon_2_shape or icon_1_color != icon_2_color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        cover_boxes_animation(main_board, [(first_selection[0], first_selection[1]), (box_x, box_y)])
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[box_x][box_y] = False
                    elif has_won(revealed_boxes): # check if all pairs found
                        game_won_animation(main_board)
                        pygame.time.wait(2000)

                        # Reset the board
                        main_board = get_randomized_board()
                        revealed_boxes = generate_revealed_boxes_data(False)

                        # Show the fully unrevealed board for a second.
                        draw_board(main_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        start_game_animation(main_board)
                        clicks = 0
                    first_selection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()