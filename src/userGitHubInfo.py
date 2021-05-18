from src.gitHubApiRequest import requestApiGitHubV4, performRequest
from datetime import date
import os


def getQueryFile(nameQuery):
    atualPath = os.path.dirname(os.path.abspath(__file__)).replace('\\', '\\\\')
    file = open('{}\\querys\\{}.graphql'.format(atualPath, nameQuery), 'r')
    gitHubQuery = file.read()
    file.close()
    return gitHubQuery


def getUserInfo(usuerName):
    query = getQueryFile('userInformation')
    queryVariables = {'nameUser': usuerName}
    return requestApiGitHubV4(query, queryVariables)


def getUserInfByYear(loginUser, dateCreated):
    dateCreated = dateCreated.split("-")
    yearCreated = int(dateCreated[0])

    todayDate = str(date.today()).split('-')
    todayYear = int(todayDate[0])
    userYearInfo = {}

    while yearCreated <= todayYear:
        yearCreated = yearCreated
        queryVariables = {
            "nameUser": loginUser,
            "fromDate": '{}-01-01T04:00:00Z'.format(yearCreated),
            "toDate": '{}-12-31T23:59:59Z'.format(yearCreated),
        }
        # print(query)
        # print(queryVariables)

        query = getQueryFile('userInfoContributionsCollection')
        userYearInfo[yearCreated] = requestApiGitHubV4(query, queryVariables)['data']['user']["contributionsCollection"]
        # print('{}: {}'.format(yearCreated, list(userYearInfo[yearCreated].values())))
        keys = userYearInfo[yearCreated].keys()
        yearCreated += 1

    return userYearInfo, keys


def repositoryUser(loginUser, numPage=80):
    queryVariables = {
        "nameUser": loginUser,
        "numPage": numPage
    }
    # repositoryAffiliation = {'OWNER': [], 'COLLABORATOR': [], 'ORGANIZATION_MEMBER': []}
    repositoryAffiliation = {'OWNER': [], 'COLLABORATOR': []}
    for repAff in repositoryAffiliation.keys():
        # print("\n")
        queryVariables["RepositoryAffiliation"] = repAff
        query = getQueryFile('repositoryInfo')
        while True:
            resp = requestApiGitHubV4(query, queryVariables)
            for rep in resp['data']['user']['repositories']['nodes']:
                # print(repAff + '---> ' + rep["nameWithOwner"])
                repositoryAffiliation[repAff].append(rep)
            if not resp['data']['user']['repositories']['pageInfo']['hasNextPage']:
                break
            query = getQueryFile('repositoryInfNext')
            queryVariables["after"] = resp['data']['user']['repositories']['pageInfo']['endCursor']
    # return repositoryAffiliation['OWNER'], repositoryAffiliation['COLLABORATOR'], repositoryAffiliation['ORGANIZATION_MEMBER']
    return repositoryAffiliation['OWNER'], repositoryAffiliation['COLLABORATOR']


def getUserRepositoryCommit(userID, arrayRepository, numPage=100):
    arrayCommits = []
    for index, repository in enumerate(arrayRepository):
        # print(index, '-> ', repository['nameWithOwner'])
        owner, name = repository['nameWithOwner'].split('/')
        if name == "linux":
            'Ignorou repositorio linux por nao retornar o historico via api'
            continue

        queryVariables = {
            "numPageIssues": numPage,
            "idUser": userID,
            "owner": owner,
            "name": name
        }
        query = getQueryFile('userRepositoryCommit')

        while True:
            resp = requestApiGitHubV4(query, queryVariables)
            # print(resp)
            if not resp['data']['repository']['defaultBranchRef'] or \
                    resp['data']['repository']['defaultBranchRef']['target']['history']['totalCount'] == 0:
                break

            resp = resp['data']['repository']['defaultBranchRef']['target']['history']
            for number, commit in enumerate(resp['nodes']):
                # print(number, commit['url'])
                arrayCommits.append(commit)

            if not resp['pageInfo']['hasNextPage']:
                break

            query = getQueryFile('userRepositoryCommitNext')
            queryVariables["after"] = resp['pageInfo']['endCursor']
    return arrayCommits

