from loader import Loader

def trigger_loader(path='/Users/nsoria/Documents/github-nsoria/g-data-exercise/endpoint/test/jobs.csv'):
    try:
        loader = Loader(path)
    except AssertionError:
        # Filename wrong
        print(False)
    else:
        loader.process_data()
        status = loader.status
        print(status)