import os
import git
from urllib.parse import urlparse

class Deployer:
    def __init__(self, site_path: str):
        self.site_path = site_path

    def deploy(self, remote_url, github_token=None):
        """
        Deploys the generated website to GitHub Pages.
        """
        # remove .git directory if it exists
        git_dir = os.path.join(self.site_path, ".git")
        if os.path.exists(git_dir):
            import shutil
            shutil.rmtree(git_dir)

        repo = git.Repo.init(self.site_path)
        repo.git.add(A=True)
        repo.index.commit("Deploy to GitHub Pages")

        # Create a gh-pages branch if it doesn't exist
        if "gh-pages" not in repo.branches:
            repo.git.branch("gh-pages")

        # Push to the gh-pages branch
        if github_token:
            url = urlparse(remote_url)
            if url.scheme == 'https':
                url = url._replace(netloc=f"x-access-token:{github_token}@{url.netloc}")
                remote_url = url.geturl()
            elif url.scheme == '' and url.path.startswith('git@'):
                remote_url = f"https://x-access-token:{github_token}@{url.path[4:].replace(':', '/')}"

        try:
            repo.git.remote("add", "origin", remote_url)
        except git.exc.GitCommandError:
            # remote already exists
            repo.git.remote("set-url", "origin", remote_url)
        repo.git.push("origin", "gh-pages", "--force")