# Password Manager

- Open your terminal and clone this repository

    First make sure you have a ssh key if you dont have go to my dotfiles repository and follow the instructions

    ```
    git clone git@github.com:ayushkpai/password-manager-tools.git
    ```
    
- Next install python and add dependencies

    Also documented in dotfiles

    ```
    uv add python-dotenv
    ```

- Create a .env

  ```
  echo VAULT_FILE=<where_you_want_file.json> >> .env
  ```

- To run the project

    ```
    uv run src/pm_tools/code.py
    ```
