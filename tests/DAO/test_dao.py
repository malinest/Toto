import unittest
import Toto.database.DAO.DAOBoard as DAOBoard

class TestDAOBoard(unittest.TestCase):
    def test_getAllBoards(self):
        boards = DAOBoard.getAllBoards()
        self.assertTrue(len(boards) > 0)

if __name__ == "__main__":
    unittest.main()