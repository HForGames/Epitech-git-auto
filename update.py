import sys
from github import Github
from dotenv import load_dotenv
import os
import subprocess
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
NothingDONE = True
BASE_PATH = "./"
PROC_MAX = multiprocessing.cpu_count()


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def print_q(text):
    if "--quiet" not in sys.argv and "-q" not in sys.argv:
        print(text)


def update_clone_repo(repo):
    global NothingDONE, BASE_PATH
    if repo.organization is None or not repo.organization.login.startswith("EpitechPromo"):
        return
    semester = int(repo.name[6])
    semester = semester // 2 if semester % 2 == 0 else (semester + 1) // 2
    module = repo.name[:9]
    if not os.path.exists(f"{BASE_PATH}/Tek-{semester}"):
        os.mkdir(f"{BASE_PATH}/Tek-{semester}")
    if not os.path.exists(f"{BASE_PATH}/Tek-{semester}/{module}"):
        os.mkdir(f"{BASE_PATH}/Tek-{semester}/{module}")
    if not os.path.exists(f"{BASE_PATH}/Tek-{semester}/{module}/{repo.name}"):
        print_q(f"Cloning {colored(0, 255, 0, repo.name)}")
        subprocess.run(
            ["git", "clone", repo.ssh_url, f"{BASE_PATH}/Tek-{semester}/{module}/{repo.name}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        NothingDONE = False
    elif "--update" in sys.argv or "-u" in sys.argv:
        print_q(f"Updating {colored(0, 255, 0, repo.name)}")
        subprocess.run(["git", "-C", f"{BASE_PATH}/Tek-{semester}/{module}/{repo.name}", "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        NothingDONE = False


def main(user):
    global TOKEN, NothingDONE
    if "--thread" in sys.argv or "-th" in sys.argv:
        pool = ThreadPool(PROC_MAX)
        pool.map(update_clone_repo, user.get_repos())
        pool.close()
        pool.join()
        return

    for repo in user.get_repos():
        update_clone_repo(repo)


def add_new_token():
    global TOKEN
    print_q("You don't have any token yet. "
            "You can create one with https://github.com/settings/tokens/new. "
            "You just have to only accept full control of private repository (Don't forget to enable SSO)")
    r = input("Your token :")
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(f"GITHUB_TOKEN={r}")
        return
    with open(".env", "r") as f:
        data = f.read()
    data = data.replace(f"GITHUB_TOKEN={TOKEN}", f"GITHUB_TOKEN={r}")
    with open(".env", "w") as f:
        f.write(data)
    TOKEN = r


def check_orgs(user):
    for i in user.get_orgs():
        if "EpitechPromo" in i.login:
            return True
    return False


def help():
    print("Usage: python3 update.py [options]")
    print("Options:")
    print("  --help / -h: Display this help")
    print("  --token / -t: Change your token")
    print("  --update / -u: Update all your repository")
    print("  --base / -b: Change the base path (Default: ./)")
    print("  --quiet / -q: Don't display anything")
    print("  --thread / -th: Use multithreading")


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        help()
        exit(0)
    if TOKEN is None or "--token" in sys.argv or "-t" in sys.argv:
        add_new_token()
    if "--base" in sys.argv or "-b" in sys.argv:
        BASE_PATH = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else sys.argv[
            sys.argv.index("-b") + 1]
    user = Github(TOKEN).get_user()
    try:
        print_q(f"Logged as {colored(0, 0, 255, user.login)}")
    except:
        print("Token is invalid please change it with --token", file=sys.stderr)
        exit(1)
    if not check_orgs(user):
        print(f"Please configure SSO for the token", file=sys.stderr)
        exit(1)
    main(user)
    if NothingDONE:
        print_q("Nothing to do")
    else:
        print_q("Done")
