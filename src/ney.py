import curses
import time
import random

# Configuración inicial del juego
class Game:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.players = {"X": {"name": "Jugador 1", "wins": 0}, "O": {"name": "Jugador 2", "wins": 0}}
        self.timer = 30  # tiempo en segundos

    def draw_board(self, win):
        win.clear()
        win.border(0)  # Dibuja bordes
        for i in range(3):
            win.addstr(i + 1, 1, "|".join(self.board[i]))
            if i < 2:
                win.addstr(i + 1, 0, "-----")
        win.addstr(5, 1, "Introduce coordenadas (fila,columna): ")
        win.refresh()

    def draw_info(self, win):
        win.clear()
        win.border(0)  # Dibuja bordes
        win.addstr(1, 1, f"Tiempo restante: {self.timer} segundos", curses.A_BOLD)
        win.addstr(3, 1, f"Turno: {self.players[self.current_player]['name']} ({self.current_player})", curses.A_BOLD)
        win.addstr(5, 1, f"Probabilidad de victoria: {random.randint(0, 100)}%")
        win.addstr(7, 1, f"Puntuación - {self.players['X']['name']}: {self.players['X']['wins']} | {self.players['O']['name']}: {self.players['O']['wins']}")
        win.refresh()

    def check_winner(self):
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != " ":
                return row[0]
        for col in range(3):
            if all(self.board[row][col] == self.board[0][col] and self.board[0][col] != " " for row in range(3)):
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]
        return None

    def is_full(self):
        return all(cell != " " for row in self.board for cell in row)

# Función principal del juego
def main(stdscr):
    curses.curs_set(1)  # Muestra el cursor
    game = Game()
    height, width = stdscr.getmaxyx()
    left_win = curses.newwin(height, width // 2, 0, 0)
    right_win = curses.newwin(height, width // 2, 0, width // 2)

    while True:
        # Muestra el tablero y la información
        game.draw_board(left_win)
        game.draw_info(right_win)

        # Manejo del temporizador
        for i in range(game.timer, 0, -1):
            time.sleep(1)
            game.timer = i
            game.draw_info(right_win)

        # Obtener coordenadas del jugador
        left_win.addstr(5, 32, " " * 20)  # Limpia la línea de entrada
        left_win.move(5, 32)  # Mueve el cursor a la posición correcta
        user_input = left_win.getstr(5, 32).decode("utf-8")

        # Procesar la entrada del usuario
        try:
            row, col = map(int, user_input.split(","))
            if 0 <= row < 3 and 0 <= col < 3 and game.board[row][col] == " ":
                game.board[row][col] = game.current_player
                winner = game.check_winner()
                if winner:
                    right_win.addstr(9, 1, f"{game.players[winner]['name']} ha ganado!")
                    right_win.refresh()
                    time.sleep(2)
                    break
                if game.is_full():
                    right_win.addstr(9, 1, "¡Empate!")
                    right_win.refresh()
                    time.sleep(2)
                    break
                game.current_player = "O" if game.current_player == "X" else "X"
                game.timer = 30  # Reiniciar el temporizador
            else:
                left_win.addstr(5, 32, "Posición ocupada o fuera de rango. Intenta de nuevo.")
        except (ValueError, IndexError):
            left_win.addstr(5, 32, "Entrada no válida. Usa formato fila,columna.")

        # Asegurarse de que el cursor esté en la ventana izquierda
        left_win.move(5, 32)

    # Fin del juego
    stdscr.clear()
    stdscr.addstr(height // 2, width // 2 - 10, "Juego terminado. Gracias por jugar!")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
