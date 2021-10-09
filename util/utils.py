import joblib
def loadJbl(filepath):
    with open(filepath, mode="rb") as f:
        data = joblib.load(f)
    return data

def readJbl(data, filepath):
    with open(filepath, mode="wb") as f:
        joblib.dump(data, f)
    return 