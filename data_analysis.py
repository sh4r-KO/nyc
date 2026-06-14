#1 create the view if didnt exist
#2 update views
#

#input : SQL views
#out put aggregates view in json format to whoever asks (run by a cron job)
import dataRetrieval

if __name__ == "__main__":

    conn = dataRetrieval.connect_with_retry()


