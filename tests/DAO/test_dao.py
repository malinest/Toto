import unittest
import Toto.database.DAO.DAOBoard as DAOBoard
import Toto.database.DAO.DAOPosts as DAOPosts

class TestDAOBoard(unittest.TestCase):
    def test_getAllBoards(self):
        boards = DAOBoard.getAllBoards()
        self.assertTrue(len(boards) > 0)

class TestDAOPosts(unittest.TestCase):
    def test_getAllPostsFromBoard(self):
        posts = DAOPosts.getAllPostsFromBoard("Board_Technology")
        self.assertTrue(len(posts) > 0)

if __name__ == "__main__":
    unittest.main()