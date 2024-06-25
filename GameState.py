from Commercial import Commercial
from Road import Road
from Industry import Industry
from Residential import Residential
from Park import Park

class GameState:
    def __init__(self, mode, board_size, coins):
        self.mode = mode
        self.board = [[None for _ in range(board_size)] for _ in range(board_size)]
        self.coins = coins
        self.score = 0
        self.turn = 1
        self.profit = 0
        self.upkeep = 0

    def print_board(self):
        size = len(self.board)
        column_headers = '  '.join(f'{i + 1:^{2}}' for i in range(size))
        print('     ' + column_headers)
        print('   +' + '---+' * size)
        for idx, row in enumerate(self.board):
            row_letter = chr(ord('A') + idx)
            print(f'{row_letter:2} |' + '|'.join(f' {cell.__class__.__name__[0] if cell else " "} ' for cell in row) + '|')
            print('   +' + '---+' * size)

    def place_building(self, coord, building):
        row, col = self.convert_coord(coord)
        if row is not None and col is not None:
            if self.board[row][col] is None:
                if self.mode == "free_play" or self.is_adjacent_to_building(row, col) or self.turn == 1:
                    self.board[row][col] = building
                    self.update_coins_and_scores(row, col, building)
                    return True
                else:
                    print("You can only place buildings next to existing buildings.")
                    return False
            else:
                print("That cell is already occupied.")
                return False
        else:
            print("Invalid coordinate.")
            return False

    def demolish_building(self, coord):
        row, col = self.convert_coord(coord)
        if row is not None and col is not None:
            if self.board[row][col] is not None:
                if self.coins >= 1:
                    self.board[row][col] = None
                    self.coins -= 1
                    print(f"Building at {coord} demolished. You have {self.coins} coins left.")
                    return True
                else:
                    print("Not enough coins to demolish the building.")
                    return False
            else:
                print("No building to demolish at the given coordinate.")
                return False
        else:
            print("Invalid coordinate.")
            return False

    def update_coins_and_scores(self, row, col, building):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacent_buildings = [self.board[row + dr][col + dc] for dr, dc in directions if 0 <= row + dr < len(self.board) and 0 <= col + dc < len(self.board) and self.board[row + dr][col + dc] is not None]

        if isinstance(building, Residential):
            for adjacent in adjacent_buildings:
                if isinstance(adjacent, Industry):
                    self.score += 1
                    return
            for adjacent in adjacent_buildings:
                if isinstance(adjacent, Residential):
                    self.score += 1
                elif isinstance(adjacent, Commercial):
                    self.score += 1
                elif isinstance(adjacent, Park):
                    self.score += 2

        elif isinstance(building, Industry):
            self.score += 1
            for adjacent in adjacent_buildings:
                if isinstance(adjacent, Residential):
                    self.coins += 1

        elif isinstance(building, Commercial):
            adjacent_commercials = sum(1 for adjacent in adjacent_buildings if isinstance(adjacent, Commercial))
            self.score += adjacent_commercials
            for adjacent in adjacent_buildings:
                if isinstance(adjacent, Residential):
                    self.coins += 1

        elif isinstance(building, Park):
            adjacent_parks = sum(1 for adjacent in adjacent_buildings if isinstance(adjacent, Park))
            self.score += adjacent_parks

        elif isinstance(building, Road):
            connected_roads = sum(1 for i in range(len(self.board)) if isinstance(self.board[row][i], Road))
            self.score += connected_roads

    def is_adjacent_to_building(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < len(self.board) and 0 <= c < len(self.board) and self.board[r][c] is not None:
                return True
        return False

    def convert_coord(self, coord):
        if len(coord) != 2:
            return None, None
        row = ord(coord[0].lower()) - ord('a')
        col = int(coord[1]) - 1
        if 0 <= row < len(self.board) and 0 <= col < len(self.board):
            return row, col
        else:
            return None, None

    def calculate_profit_and_upkeep(self):
        residential_clusters = []
        commercial_count = 0
        industry_count = 0
        park_count = 0
        road_segments = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if isinstance(self.board[row][col], Residential):
                    in_cluster = False
                    for cluster in residential_clusters:
                        if self.is_adjacent_to_cluster(row, col, cluster):
                            cluster.append((row, col))
                            in_cluster = True
                            break
                    if not in_cluster:
                        residential_clusters.append([(row, col)])
                elif isinstance(self.board[row][col], Commercial):
                    commercial_count += 1
                elif isinstance(self.board[row][col], Industry):
                    industry_count += 1
                elif isinstance(self.board[row][col], Park):
                    park_count += 1
                elif isinstance(self.board[row][col], Road):
                    if not self.is_connected_road(row, col):
                        road_segments.append((row, col))

        residential_upkeep = len([cluster for cluster in residential_clusters if len(cluster) > 1])
        commercial_upkeep = 2 * commercial_count
        industry_upkeep = 1 * industry_count
        park_upkeep = 1 * park_count
        road_upkeep = 1 * len(road_segments)

        residential_profit = sum([len(cluster) for cluster in residential_clusters])
        commercial_profit = 3 * commercial_count
        industry_profit = 2 * industry_count

        self.profit = residential_profit + commercial_profit + industry_profit
        self.upkeep = residential_upkeep + commercial_upkeep + industry_upkeep + park_upkeep + road_upkeep

    def is_adjacent_to_cluster(self, row, col, cluster):
        for r, c in cluster:
            if abs(row - r) + abs(col - c) == 1:
                return True
        return False

    def is_connected_road(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < len(self.board) and 0 <= c < len(self.board) and isinstance(self.board[r][c], Road):
                return True
        return False

    def end_turn(self):
        self.calculate_profit_and_upkeep()
        self.coins += self.profit - self.upkeep
        print(f"Profit: {self.profit}. Upkeep: {self.upkeep}\n")
        print(f"Turn {self.turn} ended. Coins: {self.coins}, Score: {self.score}\n")

        if self.coins < 0:
            print("You have run out of coins. Game over!")
            return False
        else:
            self.turn += 1
            return True
