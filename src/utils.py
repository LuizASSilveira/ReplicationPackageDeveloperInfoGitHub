import pandas as pd
import json
import os




def developerOverviewAux(userInfo, repositories, userInfoAllTime, userCommitInfo):
    developerOverview = {
        "login": userInfo['data']['user']['login'],
        "nome": userInfo['data']['user']['name'],
        "email": userInfo['data']['user']['email'],
        "dataCriacaoContaGithub": userInfo['data']['user']['createdAt'],
        "location": userInfo['data']['user']['location'],
        "company": userInfo['data']['user']['company'],
        "watching": userInfo['data']['user']['watching']['totalCount'],
        "followers": userInfo['data']['user']['followers']['totalCount'],
        "following": userInfo['data']['user']['following']['totalCount'],
        "organizations": userInfo['data']['user']['organizations']['totalCount'],
        "projects": userInfo['data']['user']['projects']['totalCount'],
        "repositories": userInfo['data']['user']['repositories']['totalCount'],
        "repositoriesOwner": len(repositories['owner']),
        "repositoriesCollaborator": len(repositories['collaborator']),
        "pullRequests": userInfo['data']['user']['pullRequests']['totalCount'],
        "issues": userInfo['data']['user']['issues']['totalCount'],
        "gists": userInfo['data']['user']['gists']['totalCount'],
        "commitComments": userInfo['data']['user']['commitComments']['totalCount'],
        "issueComments": userInfo['data']['user']['issueComments']['totalCount'],
        "gistComments": userInfo['data']['user']['gistComments']['totalCount'],
        "totalIssueContributions": userInfoAllTime['totalIssueContributions'],
        "totalCommitContributions": userInfoAllTime['totalCommitContributions'],
        "totalRepositoryContributions": userInfoAllTime['totalRepositoryContributions'],
        "totalPullRequestContributions": userInfoAllTime['totalPullRequestContributions'],
        "totalPullRequestReviewContributions": userInfoAllTime['totalPullRequestReviewContributions'],
        "totalRepositoriesWithContributedIssues": userInfoAllTime['totalRepositoriesWithContributedIssues'],
        "totalRepositoriesWithContributedCommits": userInfoAllTime['totalRepositoriesWithContributedCommits'],
        "totalRepositoriesWithContributedPullRequests": userInfoAllTime['totalRepositoriesWithContributedPullRequests'],
        "totalRepositoriesWithContributedPullRequestReviews": userInfoAllTime['totalRepositoriesWithContributedPullRequestReviews'],
        'totalChangedFiles': userCommitInfo['changedFiles'],
        'totalAdditions': userCommitInfo['additions'],
        'totalDeletions': userCommitInfo['deletions']
    }
    return developerOverview


def jsonPrettify(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))


def saveCSV(data, path):
    pd.json_normalize(data).to_csv(path)


def saveDictCSV(data, orient, columns, path):
    pd.DataFrame.from_dict(data, orient=orient, columns=columns).to_csv(path)


def createFolderIfDoesntExist(standardDirectory):
    if not os.path.exists(standardDirectory):
        os.mkdir(standardDirectory)
    return standardDirectory + '\\'


def saveJson(data, path, typeOpen='w', encodingFile='UTF-8'):
    file = open(path, typeOpen, encoding=encodingFile)
    if data:
        json.dump(data, file, indent=4)
    file.close()


def addLogFile(path, nameUser):
    with open(path, 'a') as json_file:
        json_file.write(nameUser+'\n')