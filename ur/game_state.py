from abc import ABC, abstractmethod


class InvalidMoveException(Exception):
    pass


class BoardTile(ABC):
    p1_token = '⦵'
    p2_token = '⦶'
    empty_token = '⬜'
    rosette_token = '✪'

    def __init__(self, is_rosette=False):
        self.players = [0, 0]
        self.is_rosette = is_rosette

    @abstractmethod
    def is_valid(self):
        """
        Whether the current tile stat is valid
        :return: Whether the current tile stat is valid
        """

        pass

    @abstractmethod
    def is_move_valid(self, player):
        """
        Whether a move by player into this square would be valid
        :param player: the player making the move
        :return: Whether a move by player into this square would be valid
        """

        pass

    @abstractmethod
    def move_to(self, source, player):
        """
        Moves the given player's piece from the source tile to this tile
        :param source: a BoardTile object that the piece is moving from
        :param player: the player making the move
        :return: Whether an other player's token was knocked back
        """

        if not self.is_move_valid(player):
            raise InvalidMoveException

    def default_token(self):
        """
        The default appearance of the tile
        :return: The default appearance of the tile
        """

        return BoardTile.rosette_token if self.is_rosette else BoardTile.empty_token

    @abstractmethod
    def token(self):
        """
        The current appearance of the tile
        :return: The current appearance of the tile, as a string, or pair of strings
        """

        pass


class StartBoardTile(BoardTile):
    def __init__(self, num_pieces):
        super().__init__()
        self.players = [num_pieces, num_pieces]

    def is_valid(self):
        return True

    def is_move_valid(self, player):
        return False

    def move_to(self, source, player):
        super().move_to(source, player)
        raise InvalidMoveException

    def token(self):
        pass


class EndBoardTile(BoardTile):
    def is_valid(self):
        return True

    def is_move_valid(self, player):
        return True

    def move_to(self, source, player):
        super().move_to(source, player)
        source.players[player] -= 0
        self.players[player] += 1

        return False

    def token(self):
        pass


class SoloBoardTile(BoardTile):
    def is_valid(self):
        return (self.players[0] == 1 or self.players[0] == 0) and (self.players[1] == 1 or self.players[1] == 0)

    def is_move_valid(self, player):
        return self.players[player] == 0

    def move_to(self, source, player):
        super().move_to(source, player)
        source.players[player] -= 1
        self.players[player] += 1

        return False

    def token(self):
        result = [self.default_token(), self.default_token()]
        if self.players[0] == 1:
            result[0] = BoardTile.p1_token

        if self.players[1] == 1:
            result[1] = BoardTile.p2_token

        return tuple(result)


class SharedBoardTile(BoardTile):
    def is_valid(self):
        return (self.players[0] == 0 and self.players[1] == 0) or \
               (self.players[0] == 1 and self.players[1] == 0) or \
               (self.players[1] == 1 and self.players[0] == 0)

    def is_move_valid(self, player):
        occupied = False
        if self.is_rosette:
            if self.players[1 - player] == 0:
                occupied = False
            else:
                occupied = True
        return self.players[player] == 0 and not occupied

    def move_to(self, source, player):
        super().move_to(source, player)

        source.players[player] -= 1
        self.players[player] += 1

        if self.players[1 - player] > 0:
            self.players[1 - player] = 0
            return True
        else:
            return False

    def token(self):
        if self.players[0] == 1:
            return BoardTile.p1_token
        elif self.players[1] == 1:
            return BoardTile.p2_token
        else:
            return self.default_token()


class GameState:
    def __init__(self, num_pieces):
        self.num_pieces = num_pieces
        self.tiles = [
            StartBoardTile(num_pieces),
            SoloBoardTile(),
            SoloBoardTile(),
            SoloBoardTile(),
            SoloBoardTile(is_rosette=True),
            SharedBoardTile(),
            SharedBoardTile(),
            SharedBoardTile(),
            SharedBoardTile(is_rosette=True),
            SharedBoardTile(),
            SharedBoardTile(),
            SharedBoardTile(),
            SharedBoardTile(),
            SoloBoardTile(is_rosette=True),
            SoloBoardTile(),
            EndBoardTile()
        ]

    def is_valid(self):
        """
        Whether the current state represented by this object is valid
        :return: Whether the current state represented by this object is valid
        """

        return all(tile.is_valid() for tile in self.tiles)

    def is_move_valid(self, source, dest, player):
        """
        Determines whether a move is valid from the current state
        :param source: the source tile
        :param dest: the dest tile
        :param player: the player making the move
        :return: Whether the move from source to dest is valid
        """

        return source in range(len(self.tiles)) and \
            dest in range(len(self.tiles)) and \
            source < dest and \
            self.tiles[source].players[player] > 0 and \
            self.tiles[dest].is_move_valid(player)

    def move(self, source, dest, player):
        """
        Moves players piece from source to dest if it is possible. Raises ValueError if the move is not valid
        :param source: the tile from which to move the piece
        :param dest: the tile to which to move the piece
        :param player: the player moving the piece
        :return: None
        """

        if not self.is_move_valid(source, dest, player):
            raise InvalidMoveException

        if self.tiles[dest].move_to(self.tiles[source], player):
            self.tiles[0].players[1 - player] += 1

    def won(self):
        """
        The winner of the current state.
        :return: The winner of the current state. None if there is no winner
        """
        if self.tiles[-1].players[0] == self.num_pieces:
            return 1
        elif self.tiles[-1].players[1] == self.num_pieces:
            return 2
