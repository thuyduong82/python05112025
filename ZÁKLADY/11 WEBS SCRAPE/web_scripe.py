from bs4 import BeautifulSoup
import request

def main():
    url = "https:/www.trebesin.cz"
    response = request.get(url)

    soup = BeautifulSoup(response.content,"htmp.parser")

    all_p = soup.find_all("p")

    gym = soup.find(id="favimage-title4")
    print(gym.text)

    print(all_p)

if __name__ == "__main__":
    main()    