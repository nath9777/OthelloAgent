
import numpy as np

def reversi_run():

    with open("input.txt", "r") as input_file:
        p = input_file.readline().strip()
        left_time, _ = map(float, input_file.readline().split())
        board = np.array([list(input_file.readline().strip()) for _ in range(12)])

        with open("output.txt", "w") as output_file:
            output_file.write(str(board))


if __name__ == "__main__":
    reversi_run()
