import multiprocessing
import tkinter as tk
from proc.detector_proc import detector_function
from db.database import *
from bin.add_entity import add_entity
from bin.train_model import train_model


class FaceRecognitionMirrorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Moja Aplikacja")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")

        self.program_state = tk.IntVar()
        self.program_state.set(0)

        self.shared_variable = multiprocessing.Value('i', -1)
        self.detector_process = None

        self.label = tk.Label(self.root, text="", font=("Helvetica", 24), fg="white", bg="black")
        self.label.pack(expand=True)

        self.button_frame = tk.Frame(self.root, bg="black")
        self.button_frame.pack(expand=True)

        self.update_screen()

    def update_screen(self, user_id=None):
        current_value = self.program_state.get()

        if current_value == 0:
            self.state_0()
        elif current_value == 1:
            self.state_1(user_id)
        elif current_value == 2:
            self.state_2()
        elif current_value == 3:
            self.state_3()
        elif current_value == 4:
            self.state_4()

    def state_0(self):
        self.label.config(text="", fg="white")
        for button in self.button_frame.winfo_children():
            button.destroy()

        # Starting face detector process
        self.shared_variable.value = -1

        self.detector_process = multiprocessing.Process(target=detector_function, args=(self.shared_variable,))
        self.detector_process.start()

        self.check_variable()

    def state_1(self, user_id):
        user_name = get_user_name(user_id)
        self.label.config(text=f"Witaj {user_name}!")

        # Usunięcie poprzednich przycisków
        for button in self.button_frame.winfo_children():
            button.destroy()

        self.create_buttons(["Rozpocznij", "Anuluj"], [self.go_to_4, self.go_back_to_0])

    def state_2(self):
        self.label.config(text="Witaj Nieznajomy! Czy chciałbyś abym dodał ciebie do bazy?")
        self.create_buttons(["Tak", "Nie"], [self.yes_action, self.go_back_to_0])

    def state_3(self):
        self.label.config(text="Wpisz swoje imię:")

        # Usunięcie poprzednich przycisków
        for button in self.button_frame.winfo_children():
            button.destroy()

        self.entry_label = tk.Label(self.button_frame, text="", font=("Helvetica", 14), fg="white", bg="black")
        self.entry_label.pack()
        self.entry = tk.Entry(self.button_frame, width=30)
        self.entry.pack(pady=10)
        self.button_submit = tk.Button(self.button_frame, text="Zatwierdź", font=("Helvetica", 12),
                                       command=self.submit_action, fg="white", bg="black")
        self.button_submit.pack()

    def state_4(self):
        for button in self.button_frame.winfo_children():
            button.destroy()

        self.label.config(text="Wybierz jedną z tych opcji:")
        self.create_buttons(["Origami", "Gotowanie", "Spacer VR", "Anuluj"],
                            [self.origami_action, self.cooking_action, self.vr_walk_action, self.go_back_to_0])

    def check_variable(self):
        value = self.shared_variable.value

        if value == -1:
            # if noone was detected
            self.root.after(100, self.check_variable)
        else:
            # if someone was detected
            self.detector_process.kill()
            if value == 0:
                # if stranger was detected
                self.program_state.set(2)
                self.update_screen()
            else:
                # if friend was detected
                self.program_state.set(1)
                self.update_screen(user_id=value)

    def create_buttons(self, labels, commands):
        for label, command in zip(labels, commands):
            button = tk.Button(self.button_frame, text=label, font=("Helvetica", 18), command=command, fg="white", bg="black")
            button.pack(side="left", padx=10)

    def create_entry_button(self, entry_label, command):
        label = tk.Label(self.button_frame, text=entry_label, font=("Helvetica", 14), fg="white", bg="black")
        label.pack()
        entry = tk.Entry(self.button_frame, width=30)
        entry.pack(pady=10)
        button_submit = tk.Button(self.button_frame, text="Zatwierdź", font=("Helvetica", 12), command=lambda: command(entry.get()), fg="white", bg="black")
        button_submit.pack()

    def go_to_4(self):
        self.program_state.set(4)
        self.update_screen()

    def go_back_to_0(self):
        self.program_state.set(0)
        self.update_screen()

    def yes_action(self):
        self.program_state.set(3)
        self.update_screen()

    def submit_action(self):
        name = self.entry.get()
        # Handle action for option 3
        print(f"Action for Submit: {name}")

        # ukryj odpowiednie elementy
        self.entry_label.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.pack_forget()
        self.button_submit.pack_forget()

        # aktualizuj etykietę
        self.label.config(text="Trwa dodawanie ciebie do bazy, spójrz w kamerę")

        # Utwórz nowy proces i przekaż imię wprowadzone przez użytkownika
        add_entity_process = multiprocessing.Process(target=add_entity, args=(name,))
        add_entity_process.start()

        self.check_add_entity_process(add_entity_process)

    def check_add_entity_process(self, process):
        if process.is_alive():
            self.root.after(100, self.check_add_entity_process, process)
        else:
            self.start_training_model()

    def start_training_model(self):
        self.label.config(text="Trwa trenowanie modelu. To może zająć chwilę...")
        train_model_process = multiprocessing.Process(target=train_model)
        train_model_process.start()

        self.check_training_model_process(train_model_process)

    def check_training_model_process(self, process):
        if process.is_alive():
            self.root.after(100, self.check_training_model_process, process)
        else:
            self.program_state.set(0)
            self.update_screen()



    def origami_action(self):
        # Handle action for option 4
        print("Action for Origami")

    def cooking_action(self):
        # Handle action for option 4
        print("Action for Cooking")

    def vr_walk_action(self):
        # Handle action for option 4
        print("Action for VR Walk")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionMirrorApp(root)
    root.mainloop()
