import pickle

def save_notes(notes, filename="notes.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notes, f)

def load_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {}
