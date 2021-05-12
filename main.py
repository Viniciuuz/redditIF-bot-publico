import praw
from praw.reddit import Subreddit

from PIL import Image
import imagehash

import requests
import shutil

import os
from time import sleep

reddit = praw.Reddit(client_id = "",
                    client_secret = "",
                    username = "",
                    password = "",
                    user_agent = "IF-moderator")

subreddit = reddit.subreddit("IFFans")


def timer():
    while True:
        main()
        sleep(10)

def remove_post(post_id):
    ac_post = reddit.submission(post_id)
    ac_post.mod.remove()
    reddit.redditor(str(ac_post.author)).message('Seu post foi removido',
                                                f"""o seu [post](https://reddit.com/{post_id}) em r/IFFans foi removido por ir contra as nossas regras.  
                                                (Esta ação foi feita por um bot, se você acha que foi um engano, fale com o criador do bot: u/_3DWaffle_)""",
                                                from_subreddit="IFFans")

def compare(image):
    l = os.listdir('memes/')

    post = image

    for i in l:
        meme = imagehash.average_hash(Image.open("memes/" + i))
        post = imagehash.average_hash(Image.open(post))
        if (meme - post) >= 50:
            return True
            
def download_image(url, name):
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        
        with open(name,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('imagem baixada: ', name)


def main():
    for submission in subreddit.new(limit=1):
    # for submission in subreddit.stream.submissions():
        if not submission.stickied:
            if submission.url.endswith((".jpg", ".png")):

                print(f"começando analise do post: {submission.title} - {submission.author}")


                download_image(submission.url, f"{submission.title.lower()}.{submission.url.lower()[-3:]}")
                print("comparando imagens...")

                if compare(f"{submission.title.lower()}.{submission.url.lower()[-3:]}"):
                    print("semelhança de imagem confere, apagando post...")
                    remove_post(submission)
                    print("post apagado")

                else:
                   print('semelhança de imagem baixa')
                   sleep(5)
                   os.system("cls")
            else: 
                print('post não pode ser analisado por não ser uma imagem')
                print(f"Post: {submission.title}, Por: {submission.author}")

main()
