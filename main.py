import sys
import os

# Ensure the project root is on the path so all imports resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import ExamTrainerApp


def main() -> None:
    app = ExamTrainerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
