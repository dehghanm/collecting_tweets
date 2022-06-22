#! /usr/bin/python3

import os
import sys

proj_path = os.getcwd()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twitterAPI.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# ============================================================================

import twint
import pandas as pd
import nest_asyncio
# import os
import datetime
import re
import numpy as np
from core.models import TwitterAccount


def remove_emoji(tweet):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               u"\u2069"
                               u"\u2066"
                               u"\u2068"
                               u"\u2067"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', tweet)


def clean_tweet(tweet):
    tweet = str(tweet)
    tweet = tweet.replace("\n", " ").replace("\r", " ")
    tweet = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})\S*', '', tweet)
    tweet = re.sub(r'@\w*', '', tweet)
    tweet = re.sub(r'[a-zA-Z]+', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'_', ' ', tweet)
    tweet = remove_emoji(tweet)
    return tweet


def get_tweets(user_name, output_path, start_date):
    # Configure
    c = twint.Config()
    c.Username = user_name
    c.Since = start_date
    c.Store_csv = True
    c.Format = "Username: {username} |  Date: {date} {time}"
    c.Output = output_path
    twint.run.Search(c)


if __name__ == "__main__":
    with open("last_date.txt", "r", encoding="utf-8") as dates_file:
        start_date = dates_file.readline().strip()
    last_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_path = "tweets.csv"

    # orientations = [0] * 30 + [1] * 38 + [2] * 27
    # twitter_account = ["Khamenei_fa", "meysammotiee1", "EsQaani", "GhadiriNetwork", "Panahian_IR", "sabeti_twt",
    #                    "jafaritwt", "DrSaeedJalili", "sm_bathaei", "nazokbin_ir", "syjebraily", "dr_a_ganji",
    #                    "A_raefipur", "MojtabaAmini13", "mmohammadii61", "hasan_abbasi", "hamidrasaee",
    #                    "m_r_hadadpour", "nezammousavi", "mb_ghalibaf", "aseyedp", "faridebrahimi62", "darabi_hossien",
    #                    "aghplt", "hamshahrinews", "Jebelli_ir", "arzakani4", "rahimpourazqadi", "SoroushAbolfazl",
    #                    "HaddadAdel_ir", "sadeghZibakalam", "sabaazarpeik", "ir_aref", "mah_sadeghi", "drpezeshkian",
    #                    "abb_abdi", "MB_Nobakht", "MansooriAzar", "mohsenmirdamadi", "kavakebian_ir", "Eshaq_jahangiri",
    #                    "P_Salahshouri", "Hemmati_ir", "S_A_Salehi", "elmira_sharifi", "ghkarbaschi", "feyzarab",
    #                    "yasharsoltani", "Saeedhajjarian", "EbHFL9CLFaaK3t8", "Alireza_Jalalii", "AliTajernia",
    #                    "Mfazeli114",
    #                    "hesamodin1", "abtahi_m", "alishakourirad", "MahmoudianMe", "abdollahram", "Khatamimedia",
    #                    "Mohmohajeri",
    #                    "majazestan", "zandizadeh", "tondgouyan", "BehnoudMasoud", "alilarijani_ir", "mazaniahmad",
    #                    "ParvanehMafi", "mostafatajzade", "hasanasadiz", "jedaaal", "hosseinbastani", "Omid_M",
    #                    "pouriazeraati", "MJ_Akbarin", "AlinejadMasih", "kayvanabbassi", "PahlaviReza", "AmmarMaleki",
    #                    "IsraelPersian", "kambizhosseini", "FardadFarahzad", "BBCFarnaz", "AfsharMahnaz",
    #                    "Kayvan_Hosseini",
    #                    "Parpanchi", "SamanArbabi", "sinavaliollah", "HosseinRonaghi", "SalomeSeyednia", "Alighazizade",
    #                    "KavehMoussavi", "rezahn56", "setarehfakhrav1", "ajibzade", "patrick_jane77"]


    twitter_account = list(TwitterAccount.objects.all().values_list("username", flat=True))
    orientations = list(TwitterAccount.objects.all().values_list("orientation", flat=True))

    if os.path.exists("all_tweets.csv"):
        colnames = ["name", "tweet", "default_orientation"]
        tweet_dataframe = pd.read_csv("all_tweets.csv", names=colnames, header=None, encoding='utf-8')
        exist_before = True
    else:
        exist_before = False

    new_tweets = False
    nest_asyncio.apply()
    for index, acc in enumerate(twitter_account):
        get_tweets(acc, output_path, start_date)
        if os.path.exists("tweets.csv"):
            new_tweets = True
            tweets = pd.read_csv(output_path)
            columns = ["name", "tweet"]
            tweets = tweets[columns]
            tweets['tweet'] = tweets['tweet'].apply(lambda x: clean_tweet(x))
            tweets['tweet'] = tweets['tweet'].str.strip()
            tweets['tweet'] = tweets['tweet'].replace('', np.nan)  # Replace blanks by NaN
            tweets.dropna(inplace=True)  # Remove rows with NaN
            tweets = tweets.reset_index(drop=True)
            tweets['default_orientation'] = orientations[index]

            if (index == 0) and (exist_before == False):
                tweet_dataframe = tweets
            else:
                tweet_dataframe = pd.concat([tweet_dataframe, tweets])
            os.remove("tweets.csv")

    if new_tweets == True:
        # columns = ["name", "tweet", "default_orientation"]
        # tweet_dataframe = tweet_dataframe[columns]
        # tweet_dataframe['tweet'] = tweet_dataframe['tweet'].apply(lambda x: clean_tweet(x))
        # tweet_dataframe['tweet'] = tweet_dataframe['tweet'].str.strip()
        # tweet_dataframe['tweet'] = tweet_dataframe['tweet'].replace('', np.nan)  # Replace blanks by NaN
        # tweet_dataframe.dropna(inplace = True)  # Remove rows with NaN
        # tweet_dataframe = tweet_dataframe.reset_index(drop=True)
        tweet_dataframe.to_csv("all_tweets.csv", index=False, header=False, encoding='utf-8')

    os.remove("last_date.txt")
    with open("last_date.txt", 'w', encoding='utf-8') as dates_file:
        dates_file.write(str(last_date))
