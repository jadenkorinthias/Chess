import chess.pgn
import re
import subprocess
import csv
from multiprocessing import Pool
import os
import unittest

def parse_eval(eval_str):
    """ Parse the evaluation from the comment string. """
    mate_match = re.search(r'\#-?(\d+)', eval_str)
    if mate_match:
        mate_in = int(mate_match.group(1))
        # Assign high positive or negative value based on mate direction
        return 10000 / mate_in if eval_str.startswith('#-') else -10000 / mate_in

    eval_match = re.search(r'\[%eval ([-+]?[\d\.]+)\]', eval_str)
    if eval_match:
        return float(eval_match.group(1))

    return None

def parse_pgn(stream, csv_writer):
    """ Parse the PGN file and write FEN and evaluation to a CSV. """
    pgn = chess.pgn.read_game(stream)
    while pgn is not None:
        board = pgn.board()
        for move in pgn.mainline():
            board.push(move.move)
            eval_str = move.comment
            eval = parse_eval(eval_str)
            if eval is not None:
                fen = board.fen()
                csv_writer.writerow([fen, eval])
        pgn = chess.pgn.read_game(stream)


def process_file(file_path):
    """ Process a single PGN file. """
    # Ensure the path to zstdcat is correct as per your system's installation location
    zstd_path = 'C:\\ProgramData\\chocolatey\\lib\\zstandard\\tools\\zstd-v1.5.6-win64\\zstd.exe'
    with subprocess.Popen([zstd_path, '-d', file_path, '--stdout'], stdout=subprocess.PIPE, text=True) as proc:
        with open(f'{file_path}.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['FEN', 'Evaluation'])
            parse_pgn(proc.stdout, csv_writer)

def main():
    """ Main function to process multiple files using multiprocessing. """
    files = ['lichess_db_standard_rated_2013-01.pgn.zst']  # Example file names
    with Pool(os.cpu_count()) as p:
        p.map(process_file, files)

class TestChessDataParsing(unittest.TestCase):
    def test_parse_eval(self):
        """ Test the evaluation parsing function. """
        self.assertEqual(parse_eval('{ [%eval 0.17] }'), 0.17)
        self.assertEqual(parse_eval('{ [%eval #1] }'), 10000)

if __name__ == '__main__':
    main()
    unittest.main()