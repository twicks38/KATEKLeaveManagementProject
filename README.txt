Git Commands/Standard Practice:

git pull                  # Get the latest changes and branches from the repository
git add .                 # Stage all changes
git add <filename>        # Stage a specific file

git branch <branch>       # Creating a new branch
git checkout <branch>     # Switch to another branch
git status                # Check which branch you're current on
git swtich -c <branch>    # Create a new branch and immediately switch to it         

When making commits/pushing:

Never push changes directly to main.
Always check which branch you are currently on before committing or pushing.
Always ensure you have checked out into main before creating a branch (to avoid making branches of branches).

When making commits, always choose commit and push through the dropdown if pushing through the VSCode GUI
Ensure that files you want to commit/push have been selected to be Staged through the "+" symbol via GUI or by using a git add command

Push your branch to GitHub and open a Pull Request (PR) for review.
Only merge into main once the Pull Request has been approved and all required checks have passed.

When a branch has been pushed and is ready to be merged, a merge request can be made via Github in your browser.
