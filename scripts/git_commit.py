import subprocess
from scripts.constants import BASE_DIR


def commit_and_push():

    subprocess.run(
        ["git", "add", "."],
        cwd=BASE_DIR,
        check=True,
    )

    subprocess.run(
        ["git", "commit", "-m", "chore: update dns rules"],
        cwd=BASE_DIR,
        check=False,
    )

    subprocess.run(
        ["git", "push"],
        cwd=BASE_DIR,
        check=False,
    )
