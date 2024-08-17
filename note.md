```py
# Remove the existing virtual environment
rm -rf venv

# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Jupyter Notebook and other dependencies
pip install notebook ipykernel
```


The error indicates that the _sqlite3 module is missing, which is required by the sqlite3 module in Python. This often happens if the SQLite development libraries are not installed on your system.

Here's a step-by-step plan to resolve this issue:

Install SQLite development libraries:

On a Fedora system, you can install the necessary libraries using dnf.
Reinstall Python:

If you are using pyenv to manage your Python versions, you need to reinstall Python after installing the SQLite development libraries.
Recreate the virtual environment:

Delete the existing virtual environment and create a new one to ensure all dependencies are correctly installed.
Step-by-Step Commands
Install SQLite development libraries:
```py
sudo dnf install sqlite-devel
```

Reinstall Python using pyenv:
```py
pyenv uninstall 3.11.6
pyenv install 3.11.6
pyenv global 3.11.6
```

Recreate the virtual environment:
```py
cd ~/Dev/Nomadcoders/fullstack-gpt
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run Jupyter Notebook:
```py
jupyter notebook
```

This should resolve the issue with the missing _sqlite3 module and allow you to run Jupyter Notebook successfully.
