import sys, re, optparse
import json
import requests

#organization=Twitter and N=10

#https://github.com/twitter
#To get a user's repo:    https://api.github.com/users/limingr/repos
#To get a org's repo      https://api.github.com/orgs/twitter/repos

#
# Top-N repos by number of stars.
# Top-N repos by number of forks.
# Top-N repos by number of Pull Requests (PRs).
# Top-N repos by contribution percentage (PRs/forks).
#

if len(sys.argv) < 3:
   sys.exit("Please privide an org name and N such as  organization=Twitter N=5")

org_para=sys.argv[1];
top_Npara=sys.argv[2];


org_len=len("organization=");
organization=org_para[org_len:]
top_NLen=len("N=")

try:
    top_N=(int)(top_Npara[top_NLen:])
except ValueError:
    sys.exit("Please privide an org name and N such as  organization=Twitter N=5")


#print("organization="+organization)
#print("N="+str(top_N))

if  top_N<0:
    sys.exit("The value of N={N} is invalid".format(N=top_N))

if len(organization) == 0:
   sys.exit("The value of organization={organization} is invalid".format(organization=organization))

username = 'limingr'
password = 'kj1016sy@G'

if len(password)==0:
   sys.exit("Please privide a valid user name and password, thanks.")

contents = requests.get("https://api.github.com/orgs/"+organization+"/repos", auth=(username, password))
print(contents)

repos = contents.json()
print("There are "+str(len(repos))+" repos");
repos=sorted(repos, key=lambda x:x["stargazers_count"], reverse=True)

#stars
print("Top-{N} repos by number of stars:".format(N=top_N))
for i in range(min(len(repos), top_N)):
    #print(str(i)+ "  "+ repos[i]["name"] +"  "+ str(repos[i]["stargazers_count"]))
    print("{index:5d}  {name:40s}  {stargazers_count:10d}".format(index=i, name=repos[i]["name"], stargazers_count=repos[i]["stargazers_count"]))


print("Top-{N} repos by number of forks:".format(N=top_N))
repos=sorted(repos, key=lambda x:x["forks_count"], reverse=True)
for i in range(min(len(repos), top_N)):
    #print(str(i)+ "  "+ repos[i]["name"] +"  "+ str(repos[i]["forks_count"]))
    print("{index:5d}  {name:40s}  {stargazers_count:10d}".format(index=i, name=repos[i]["name"], stargazers_count=repos[i]["forks_count"]))


#https://api.github.com/repos/twitter/twurl/pulls?state=all

#Pull Requests dictionary
prdict={} 
print("Retrieving pull request counts (may take a min.) ....");
for i in range(len(repos)):
    request_url="https://api.github.com/repos/{org}/{repo}/pulls?state=all".format(org=organization, repo=repos[i]["name"])
    pullrequests= requests.get(request_url)
    pullrequests=pullrequests.json();
    prdict[repos[i]["name"]]=len(pullrequests)

#top PR
print("Top-{N} repos by number of pull requests:".format(N=top_N))
i=0
for k, v in sorted(prdict.items(), key=lambda items: items[1],  reverse=True):
    print("{index:5d}  {name:40s}  {pullrequest_count:10d}".format(index=i, name=k, pullrequest_count=v))
    i=i+1
    if i>=top_N :
        break

#contribution percentage
contribution_dict={}
for x in range(len(repos)):
    name=repos[x]["name"]
    pullrequests_count=prdict[name] if name in  prdict  else 0
    forks_count=repos[x]["forks_count"]
    contribution_dict[name]=0.0 if forks_count==0 else (pullrequests_count/forks_count)

print("Top-{N} repos by number of contribution percentage (PRs/forks):".format(N=top_N))
i=0
for k, v in sorted(contribution_dict.items(), key=lambda items: items[1],  reverse=True):
    print("{index:5d}  {name:40s}  {contribution_count:10.4f}".format(index=i, name=k, contribution_count=v))
    i=i+1
    if i>=top_N :
        break