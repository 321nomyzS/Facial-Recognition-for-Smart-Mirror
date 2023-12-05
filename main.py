from proc.screen_proc import FaceRecognitionMirrorApp
import tkinter as tk
from multiprocessing import freeze_support


if __name__ == '__main__':
    freeze_support()
    root = tk.Tk()
    app = FaceRecognitionMirrorApp(root)
    root.mainloop()
