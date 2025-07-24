from .base_persistence_engine import PersistenceEngine

class FlatFilePersistenceEngine(PersistenceEngine):

    def __init__(self, file_path : str):
        self.file_path = file_path

    def create_structure(self) -> bool:
        import os, csv

        file_exists = os.path.isfile(self.file_path)
        
        if file_exists:
            os.remove(self.file_path)

        header = ['Id', 'Name', 'TimeAdded', 'Hash', 'Content']

        with open(self.file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

        return True


    def connect(self) -> bool:
        
        import os
        file_exists = os.path.isfile(self.file_path)
        
        if file_exists:
            return True
        else:
            return False
            
    def add_content(self, name : str, time_added : str, hash : str, content : str):
        
        import os, csv

        header = ['Id', 'Name', 'TimeAdded', 'Hash', 'Content']

        file_exists = os.path.isfile(self.file_path)

        with open(file=self.file_path, mode="a", newline='') as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(header)

            writer.writerow([666, name, time_added, hash, content])
