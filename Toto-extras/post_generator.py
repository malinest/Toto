import sys
import io
import requests
from faker import Faker

def generatePosts(posts_number):
    faker = Faker()
    for i in range(posts_number):
        data = {"title": "Generated post", "username": faker.simple_profile()["username"], "content": faker.paragraphs()}
        image_request = requests.get(faker.image_url())
        image = io.BytesIO(image_request.content)
        file = {"media": image}
        request = requests.post("http://localhost:5000/api/create_post?board=Board_Technology", data=data, files=file)

if __name__ == "__main__":
    args = sys.argv

    if len(args) == 2:
        if isinstance(int(args[1]), int):
            posts_number = int(args[1])
            print("You are about to generate {0} posts, do you want to continue? (y/n)".format(posts_number))
            user_response = sys.stdin.read(1)
            if user_response == 'y' or user_response == 'Y':
                generatePosts(posts_number)
                print("Post/s generated successfully")
            else:
                print("Aborting...")
        else:
            raise TypeError("The argument must be a number")
    else:
        raise TypeError("This scripts only takes 1 argument ({0} supplied)".format(len(args)))