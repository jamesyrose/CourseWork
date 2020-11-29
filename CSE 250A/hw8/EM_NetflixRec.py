import pandas as pd
import numpy as np
import os


class NetflixRec:
    def __init__(self, df, rz, z, movieTitles):
        self._df, self._rz, self._z, self._movieTitles = df, rz, z, movieTitles
        self.logLikeHist = []  # log likelihood history

        self.__j = self._df.shape[1]  # Number of movies
        self.__T = self._df.shape[0]  # Number people
        self.__k = len(self._z)  # num hidden variables
        # Iterators
        self.__TS = range(self.__T)  # itter over people
        self.__KS = range(self.__k)  # itter over hidden vari
        self.__JS = range(self.__j)  # itter over movies

        # Buffers
        self.rzup = self._rz.copy()  # P(R|Z) update buffer
        self.zup = [0] * self.__k  # P(Z|i)
        self.zUpdate = [0] * self.__k  # P(Z=i | R=r) for each t (person)

        # Checks
        assert self._rz.shape[0] == self.__j  # P(R|Z) should have rows = num Movies
        assert self._rz.shape[1] == self.__k  # P(R|Z) show have cols = num hidden variables

    def __prob_Rz(self, movie, zi):
        """
        P(R = r | zi )
        movie = movie name (str)
        zi = zinit index (int)
        """
        return self._rz[movie][zi]

    def __prob_R(self, ratings):
        """
        P(R=r)
        Probability likes the movie as a product of the movies they've seen
        ratings: viewers ratings {0,1,?} (list)
        """
        total = 0
        for i in self.__KS:
            buff = 1  # Product
            for rating, movie in zip(ratings, self.__TS):
                if rating == 0:  # Not recommended
                    buff *= (1 - self.__prob_Rz(movie, i))  # P(R=0|zi)  = 1 - P(R=1|zi)
                elif rating == 1:  # Recommended
                    buff *= self.__prob_Rz(movie, i)
                # Else pass (hasent seen) / rating = ?
            total += self._z[i] * buff
        return total

    def __eStep(self, ratings):
        """
        E step
        Compute P(Z|R)
        :ratings: list
        :return:  None
        """
        zUpdate = []
        for i in self.__KS:
            pzi = self._z[i]
            for rating, movieIdx in zip(ratings, self.__JS):
                if rating == 1:
                    pzi *= self._rz[movieIdx][i]
                elif rating == 0:
                    pzi *= (1-self._rz[movieIdx][i])
            zUpdate.append(pzi)
        self.zUpdate = [buff / sum(zUpdate) for buff in zUpdate]  # list: P(Z=i| R=movie)
        self.zup = [self.zup[idx] + self.zUpdate[idx] for idx in self.__KS]


    def __mStep(self, ratings):
        """
        M step
        P(Rk = 1| Z=i)

        Does not include normalization b/c adds to self.rzup buffer along the way

        :param ratings: list
        :return: None
        """
        for i in self.__KS:
            for rating, movieIdx in zip(ratings, self.__JS):
                if rating == '?':
                    self.rzup[movieIdx][i] += self._rz[movieIdx][i] * self.zUpdate[i]
                elif rating == 1:
                    self.rzup[movieIdx][i] += self.zUpdate[i]

    def meanPopularity(self):
        """
        Displays mean popularity  of movies (sorted)
        :return:
        """

        moviePop = {}
        for mov in self.__JS:
            buff = self._df[:, mov]
            buff = [rating for rating in buff if rating != "?"]
            mean_rating = sum(buff) / len(buff)
            movie = self._movieTitles[mov]
            moviePop[mean_rating] = "\033[1m%s:\033[0m average rating of %0.4f" % (movie, mean_rating)

        pops = sorted(moviePop.keys())
        stringBuilder = ""
        for p in pops:
            stringBuilder += "\n" + moviePop[p]
        print(stringBuilder)
        return stringBuilder

    def computeAndUpdate(self, itter: int = 16):
        """
        Computes log likelihood and updates P(z=i) and P(R=1|z=i)
        :param itter: num itterations
        :return: None
        """
        for _ in range(itter + 1):
            # Update buffers
            self.rzup[:][:] = 0  # Set buffer to 0 for summations
            self.zup = [0] * self.__k  # P(Z=i) buffer
            logLike = 0
            for t in self.__TS:  # Iterate over people
                ratings = self._df[t]  # get ratings of people
                logLike += np.log(self.__prob_R(ratings))
                self.__eStep(ratings)
                self.__mStep(ratings)

            # Normalization of M step
            for i in self.__KS:
                self.rzup[:, i] = self.rzup[:, i] / self.zup[i]
                self.zup[i] = self.zup[i] / self.__T

            # Update
            self._rz = self.rzup.copy()
            self._z = self.zup.copy()

            self.logLikeHist.append(logLike / self.__T)


if __name__ == "__main__":
    # Sample data
    titles = open("hw8_movies.txt").read().split("\n")
    ids = open("hw8_ids.txt").read().split("\n")
    df = pd.read_csv("hw8_ratings.txt", sep=" ", names=titles)
    df["ids"] = ids
    df.set_index("ids", inplace=True)
    df = df.applymap(lambda x: int(x) if x != "?" else x)

    # probs
    z = [float(val) for val in open("hw8_probZ_init.txt").read().strip().split('\n')]
    rz = pd.read_csv("hw8_probRgivenZ_init.txt", sep=" ", header=None).astype(float)
    rz = rz.replace("", None)
    rz.dropna(axis=1, inplace=True)
    rz.columns = range(len(rz.columns))
    df, rz, z = df.to_numpy(), rz.to_numpy(), z

    rec = NetflixRec(df, rz, z, titles)

    rec.meanPopularity()
