from github import Github
from dotenv import load_dotenv
import os
load_dotenv()


g = Github(os.getenv("GITHUB_TOKEN"))

for repo in g.get_user().get_repos():
    if repo.organization is not None:
        if repo.organization.login.startswith("EpitechPromo"):
            semester = int(repo.name[6])
            semester = semester // 2 if semester % 2 == 0 else (semester+1) // 2
            module = repo.name[:9]
            if not os.path.exists(f"./Tek-{semester}"):
                os.mkdir(f"./Tek-{semester}")
            if not os.path.exists(f"./Tek-{semester}/{module}"):
                os.mkdir(f"./Tek-{semester}/{module}")
            if not os.path.exists(f"./Tek-{semester}/{module}/{repo.name}"):
                os.system(f"git clone {repo.ssh_url} ./Tek-{semester}/{module}/{repo.name}")
            else:
                print("Already cloned > " + repo.name)
                print("pulling...")
                os.system(f"git -C ./Tek-{semester}/{module}/{repo.name} pull")


