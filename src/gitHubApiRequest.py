import requests
import sys
import time


def getHeades():
    return {"Authorization": 'Bearer {0}'.format(sys.argv[1])}


def requestApiGitHubV4(query, variables={}, numAttempt=20):
    while numAttempt > 0:
        try:
            request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables},
                                    headers=getHeades(), timeout=30)
            if request.status_code == 200:
                return request.json()
            else:
                print(request)
                print(request.text)
                print('Tentativa Request Api V4 GitHub n° ' + str(20 - numAttempt + 1))
                if 'timeout' in request.json()["errors"][0]["message"]:
                    raise Exception
                numAttempt -= 1
                time.sleep(3)
        except:
            if numAttempt < 17:
                time.sleep(3)

                variables["numPage"] = (variables["numPage"] - 10) if variables["numPage"] > 10 else 10
    print(query)
    return {}


def performRequest(url, numAttempt=10):
    attempt = 1
    while True:
        try:
            request = requests.get(url, headers=getHeades())
            if request.status_code == 200:
                return request
            elif attempt > numAttempt:
                return request
            else:
                attempt += 1
                print('dormindo: tentativa {}'.format(attempt))
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            print('performRequest: ', e)
            time.sleep(5)
