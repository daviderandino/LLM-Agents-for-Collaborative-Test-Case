import sys
import os
from src.main import main

if __name__ == "__main__":
    # Adds the current project folder to Python's path so it finds 'src'
    sys.path.append(os.getcwd())
    main()