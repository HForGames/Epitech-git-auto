# Epitech-git-auto

This Python script automates the process of cloning and updating GitHub repositories, specifically targeting repositories within the **EpitechPromo** organization. It utilizes the GitHub API to fetch repositories, clone them to a local directory, and optionally update existing clones. The script also supports multithreading for faster execution.
## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/HForGames/Epitech-git-auto
   cd Epitech-git-auto
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your GitHub token:
   ```env
   GITHUB_TOKEN=your_github_token_here
   ```

   You can generate a token [here](https://github.com/settings/tokens/new). Make sure to enable **full control of private repositories** and enable SSO if required.

## Usage

```bash
python3 update.py [options]
```

### Options

- `--help`, `-h`: Display the help message.
- `--token`, `-t`: Change your GitHub token.
- `--update`, `-u`: Update all existing cloned repositories.
- `--base`, `-b [path]`: Set a custom base path for cloning repositories (default is `./`).
- `--quiet`, `-q`: Suppress output.
- `--thread`, `-th`: Enable multithreading for faster execution.

## Notes

- Ensure your GitHub token has sufficient permissions and SSO enabled if needed.
- The script organizes repositories into directories based on semesters (e.g., `Tek-1`, `Tek-2`).
