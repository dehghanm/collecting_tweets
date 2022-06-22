import os.path


def check_file_if_exist():
    if os.path.exists('all_tweets.csv'):
        return True
    return False


def remove_csv_file():
    if os.path.exists("all_tweets.csv"):
        os.remove("all_tweets.csv")
    else:
        print("The file does not exist")
