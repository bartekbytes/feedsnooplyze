class FileNotifier:

    def notify(self, message):
        with open("notifier.log", "a") as f:
            f.write(f"HIHI: {message}" + "\n")