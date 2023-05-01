#cython: language_level=3
#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=False

cpdef get_all_random_blocks(int[:, :] board,int rows,int cols):
    cdef list empty = []

    for i in range(1,rows):
        for j in range(1,cols):
            if board[i][j] == 0:
                empty.append([i,j])

    return empty

cdef class VisionLine:
    cdef double wall_distance
    cdef double apple_distance
    cdef double segment_distance

    def __init__(self, double wall_output, double apple_output, double segment_output):
        self.wall_distance = wall_output
        self.apple_distance = apple_output
        self.segment_distance = segment_output

    @property
    def wall_dist(self):
        return self.wall_distance

    @property
    def apple_dist(self):
        return self.apple_distance

    @property
    def segment_dist(self):
        return self.segment_distance


cpdef get_vision_lines_snake_head(int[:, :] board, int[:] snake_head,int vision_direction_count, str apple_return_type, str segment_return_type):

    cdef int directions[8][2]
    directions[0][0] = -1
    directions[0][1] = 0
    directions[1][0] = 1
    directions[1][1] = 0
    directions[2][0] = 0
    directions[2][1] = -1
    directions[3][0] = 0
    directions[3][1] = 1
    directions[4][0] = -1
    directions[4][1] = 1
    directions[5][0] = -1
    directions[5][1] = -1
    directions[6][0] = 1
    directions[6][1] = -1
    directions[7][0] = 1
    directions[7][1] = 1

    cdef list vision_lines = []
    cdef int x_offset, y_offset
    cdef int[2] apple_coord = [0,0]
    cdef int[2] segment_coord = [0,0]
    cdef int[2] current_block = [0,0]
    cdef int[2] wall_coord = [0,0]

    cdef float wall_output, apple_output, segment_output, output_distance
    cdef int board_element
    cdef bint apple_found = False
    cdef bint segment_found = False
    cdef bint wall_found = False
    cdef int dx
    cdef int dy

    for i in range(vision_direction_count):
        current_block = [0,0]
        apple_coord = [0,0]
        wall_coord = [0,0]
        segment_coord = [0,0]

        apple_found = False
        segment_found = False
        wall_found = False

        x_offset = directions[i][0]
        y_offset = directions[i][1]

        # search starts at one block in the given direction otherwise head is also check in the loop
        current_block[0] = snake_head[0] + x_offset
        current_block[1] = snake_head[1] + y_offset
        board_element = board[current_block[0], current_block[1]]

        if board_element == -2:
            segment_coord[0] = current_block[0]
            segment_coord[1] = current_block[1]
            segment_found = True

        if board_element == -1:
            wall_coord[0] = current_block[0]
            wall_coord[1] = current_block[1]
            wall_found = True

        # loop the blocks in the given direction and store position and coordinates
        while board_element != -1:
            if board_element == 2 and apple_found == False:
                apple_coord[0] = current_block[0]
                apple_coord[1] = current_block[1]
                apple_found = True
            current_block[0] = current_block[0] + x_offset
            current_block[1] = current_block[1] + y_offset
            board_element = board[current_block[0], current_block[1]]

        if wall_found:
            dx = abs(snake_head[0] - wall_coord[0])
            dy = abs(snake_head[1] - wall_coord[1])
            output_distance =  max(dx, dy)
            wall_output = 1.0 / output_distance
        else:
            wall_output = 0.0

        if apple_return_type == "boolean":
            apple_output = 1.0 if apple_found else 0.0
        else:
            if apple_found:
                dx = abs(snake_head[0] - apple_coord[0])
                dy = abs(snake_head[1] - apple_coord[1])
                output_distance =  max(dx, dy)
                apple_output = 1.0 / output_distance

            else:
                apple_output = 0.0

        if segment_return_type == "boolean":
            segment_output = 1.0 if segment_found else 0.0
        else:
            if segment_found:
                dx = abs(snake_head[0] - segment_coord[0])
                dy = abs(snake_head[1] - segment_coord[1])
                output_distance =  max(dx, dy)

                segment_output = 1.0/output_distance
            else:
                segment_output = 0.0

        vision_lines.append(VisionLine(wall_output, apple_output, segment_output))

    return vision_lines

cpdef update_board_from_snake(int[:, :] board,int[:,:]body):
    cdef int x, y
    cdef int width = board.shape[0]
    cdef int height = board.shape[1]
    for x in range(width):
        for y in range(height):
            board_val = board[x,y]
            if board_val == 1:
                board[x,y] = 0
            if board_val == -2:
                board[x, y] = 0

    board[body[0][0],body[0][1]] = 1
    for i in range(1,len(body)):
        board[body[i][0],body[i][1]] = -2

    return board
