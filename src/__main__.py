from json import JSONDecodeError

import pandas as pd
import json
import sys
import os


from src.gitHubApiRequest import performRequest
from src.userGitHubInfo import getUserInfo, getUserInfByYear, repositoryUser, getUserRepositoryCommit
from src.utils import createFolderIfDoesntExist, developerOverviewAux, saveCSV, addLogFile, jsonPrettify


def getContributors(path, language, numeroContribuidores=100, numeroProjetos=2):
    listRepo = {}
    listDev = []

    for lang in language:
        url = 'https://api.github.com/search/repositories?q=language:{}&per_page={}&page=1&order=desc'.format(lang.lower(), numeroProjetos)
        print(url)
        request = performRequest(url)
        listRepo[lang] = []

        for proj in request.json()['items']:
            pag = 1
            requestUser = []

            while True:
                url = '{}{}{}{}'.format(proj['contributors_url'], '?per_page={}'.format(str(numeroContribuidores)), '&page={}'.format(pag), '&order=desc')
                print(url)
                request = [dev for dev in performRequest(url).json() if dev['type'] == 'User']
                requestUser += request
                pag += 1

                if len(request) == 0 or len(requestUser) > numeroContribuidores:
                    break

            contributors = [urlUser['login'] for urlUser in requestUser[:numeroContribuidores]]
            listDev += contributors
            print('Size -> ', len(listDev))
            listRepo[lang].append({proj['full_name']: contributors})

    file = open('{}{}'.format(path, '\\ProjWithUser.json'), 'w')
    json.dump(listRepo, file, indent=4)
    file.close()

    file = open('{}{}'.format(path, '\\devs.json'), 'w')
    json.dump(listDev, file, indent=4)
    file.close()

    return listDev


def devInfoMining(standardDirectory, listDev):
    createFolderIfDoesntExist(standardDirectory)
    devInfos = []
    errorNoneGit = {}

    for index, loginDev in enumerate(listDev):
        print(index + 1, ' -> ', loginDev)
        try:
            print('User Info ... ')
            devInfo = getUserInfo(loginDev)

            print('User Info By Year ... ')
            userInfoByYear, keys = getUserInfByYear(loginDev, devInfo['data']['user']['createdAt'])
            userInfoAllTime = pd.DataFrame.from_dict(userInfoByYear, orient='index', columns=keys).sum(axis=0)
            OWNER, COLLABORATOR = repositoryUser(loginDev)
            repositories = {
                'owner': OWNER,
                'collaborator': COLLABORATOR
            }

            print('User Commits ... ')
            userId = devInfo['data']['user']['id']
            userCommits = getUserRepositoryCommit(userId, repositories['owner'] + repositories['collaborator'])
            userCommitInfo = {
                'changedFiles': 0,
                'additions': 0,
                'deletions': 0
            }

            for index, commit in enumerate(userCommits):
                if not commit:
                    errorNoneGit[index] = commit
                    continue
                userCommitInfo['changedFiles'] += commit['changedFiles'] if commit['changedFiles'] else 0
                userCommitInfo['additions'] += commit['additions'] if commit['additions'] else 0
                userCommitInfo['deletions'] += commit['deletions'] if commit['deletions'] else 0

            # print(userCommitInfo)
            developerOverview = developerOverviewAux(devInfo, repositories, userInfoAllTime, userCommitInfo)
            devInfos.append(developerOverview)
        except:
            print('EROOR +++++> ', loginDev)
            addLogFile(standardDirectory + 'log.txt', loginDev)
            continue

    print('\n\nNone Error Git --> ', errorNoneGit)
    standardDirectory = '{}\\{}\\'.format(standardDirectory, 'generalInformation')
    createFolderIfDoesntExist(standardDirectory)
    saveCSV(devInfos, standardDirectory + 'devInfos.csv')


if __name__ == '__main__':
    try:
        # 'C:\\Users\\luiz_\\Desktop\\devs.json'
        # 'C:\Users\luiz_\Desktop\devs.json'

        path = '{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)), 'data2')
        sysLength = len(sys.argv)

        if sysLength == 1:
            raise IndexError

        elif sysLength == 2:
            createFolderIfDoesntExist(path)
            language = ['JavaScript']
            listDev = getContributors(path, language, 202, 1)
            devInfoMining(path, listDev[200:])

        elif sysLength == 3:
            createFolderIfDoesntExist(path)
            with open(sys.argv[2], 'r') as json_file:
                devInfoMining(path, json.load(json_file))

        else:
            raise Exception

    except IndexError:
        print('Passe seu token de acesso pessoal via parametro. ' + '(https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line)')
        print('E um arquivo json com os desenvolvedores')
        exit(1)

    except JSONDecodeError:
        print('Arquivo de formato invalido')
        exit(1)

    except FileNotFoundError:
        print('Não foi possivel encontrar o arquivo: {}'.format(sys.argv[2]))
        exit(1)

    except Exception:
        print('Numero invalido de parametros')
        exit(1)
