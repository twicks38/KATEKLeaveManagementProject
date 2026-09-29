# For Devs:

## Git Commands/Standard Practice:

- **git status** - _Check which branch you're currently on_
- **git branch `<branch>`** - _Creating a new branch_
  - **git branch -D `<branch>`** - _Delete local branch_
- **git checkout `<branch>`** - _Switch to another branch_
  - **git checkout origin/main -b `<new branch name>`** - _Creates new branch from origin/main_
    - _alternative command to git branch._
- **git switch -c `<branch>`** - _Create a new branch and immediately switch to it_

- **git pull** - _Get the latest changes and branches from the repository_
- **git add** - _Stage changes_
  - **git add `<filename>`** - _Stage a specific file_
  - **git add `-A` / `-all`** - _Stage all changes_

- **git push** - _Push your changes up_ **Never push changes directly to main.**
  - **git push --set-upstream origin `your branch`** - _In case of upstream errors_
    - _If that fails because you already pushed up to it add a space and then_ **-f** _after your branch name._

### When making commits/pushing:

**Once again never push changes directly to main.**
Always check which branch you are currently on before committing or pushing.
Always ensure you have checked out into main before creating a branch (to avoid making branches of branches).

When making commits, always choose commit and push through the dropdown if pushing through the VSCode GUI
Ensure that files you want to commit/push have been selected to be Staged through the "+" symbol via GUI or by using a git add command

Push your branch to GitHub and open a Pull Request (PR) for review.
Only merge into main once the Pull Request has been approved and all required checks have passed.

When a branch has been pushed and is ready to be merged, a merge request can be made via Github in your browser.

## Starting project for testing.

_use `py` instead of `python` for some python versions_

Make sure DJANGO is installed

`python -m django --version`

If not installed
you can install it by:
`pip install django`

Once installed, run

`python manage.py makemigrations`
and
`python manage.py migrate`

then you can run the server by doing

`python manage.py runserver`

once it's running, go onto your browser and enter

http://127.0.0.1:8000/

If hosted on another port other than 8000 then just change the port number.
