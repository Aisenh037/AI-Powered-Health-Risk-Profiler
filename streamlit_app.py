import sys
import os

# Add the current directory to python path to ensure frontend package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.main import main

if __name__ == "__main__":
    main()
