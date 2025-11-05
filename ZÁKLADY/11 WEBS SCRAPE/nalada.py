from bs4 import BeautifulSoup
import request

def main():
    url = "https://www.arsenal.com/results" #odkaz kde je adresa webu ze ktere cerpame
    response = request.get(url) #stahne html kod stranky

    soup = BeautifulSoup(response.content,"htmp.parser")

    all_p = soup.find_all("p")

    team2 = soup.select(".scores__score")
    arsenal = soup.select(".scores__score scores__score--arsenal")

    def rozhodni():
        if 
  
if __name__ == "__main__":
    main()    