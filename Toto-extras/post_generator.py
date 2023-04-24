"""
Script that generates a specified number of posts on a board
The script only takes 2 arguments:
    1. board_name: This is the name of the collection that contains the board (ex: Board_Technology)
    2. posts_number: This is the number of posts that will be generated on said board
"""
import sys
import io
import requests
from faker import Faker

def generatePosts(board_name, posts_number):
    faker = Faker()
    for i in range(posts_number):
        data = {"title": "Generated post", "username": faker.simple_profile()["username"], "content": faker.paragraphs()}
        image_request = requests.get(faker.image_url())
        image = io.BytesIO(image_request.content)
        file = {"media": image}
        request = requests.post("http://localhost:5000/api/create_post?board={0}".format(board_name), data=data, files=file)
        if request.status_code == 404:
            raise ValueError("Invalid board")


if __name__ == "__main__":
    args = sys.argv

    if len(args) == 3:
        if isinstance(int(args[2]), int):
            board_name = args[1]
            posts_number = int(args[2])
            print("You are about to generate {0} posts on {1}, do you want to continue? (y/n)".format(posts_number, board_name))
            user_response = sys.stdin.read(1)
            if user_response == 'y' or user_response == 'Y':
                generatePosts(board_name, posts_number)
                print("Post/s generated successfully")
            else:
                print("Aborting...")
        else:
            raise ValueError("The argument must be a number")
    else:
        raise ValueError("This scripts only takes 2 arguments (board/posts_number) ({0} supplied)".format(len(args)))