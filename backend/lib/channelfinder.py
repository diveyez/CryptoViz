import pandas as pd
import numpy as np


class ChannelFinder:
    def find_maximums(self,data,increment):
        start = 0
        end = increment
        maximums = pd.Series([])
        for _ in range(int(len(data)/increment)):
            maximums = maximums.append(pd.Series(float(data[start:end].max())))
            start += increment
            end += increment
        maximums = sorted(maximums)
        return maximums

    def find_minimums(self,data,increment):
        start = 0
        end = increment
        minimums = pd.Series([])
        for _ in range(int(len(data)/increment)):
            minimums = minimums.append(pd.Series(int(data[start:end].min())))
            start += increment
            end += increment
        minimums = sorted(minimums)
        return minimums

    def find_resistance(self,data):
        cutoff = 2
        increment = 10
        maximums = self.find_maximums(data=data,increment=increment)

        histogram = np.histogram(maximums,bins=(int(len(maximums)/increment*increment)))
        histogram_occurences = pd.DataFrame(histogram[0])
        histogram_occurences.columns = ['occurence']
        histogram_splits = pd.DataFrame(histogram[1])
        histogram_splits.columns = ['bins']

        histogram_bins = []
        for x in histogram_splits.index:
            if x < len(histogram_splits.index)-1:
                element = [int(histogram_splits.iloc[x]), int(histogram_splits.iloc[x+1])]
                histogram_bins.append(element)

        histogram_bins = pd.DataFrame(histogram_bins)
        histogram_bins['occurence'] = histogram_occurences
        histogram_bins.columns = ['start','end','occurence']

        histogram_bins = histogram_bins[histogram_bins['occurence'] >= cutoff]
        histogram_bins.index = range(len(histogram_bins))

        data = sorted(data)
        data = pd.Series(data)

        lst_maxser = [
            data[
                (data > histogram_bins['start'][i])
                & (data < histogram_bins['end'][i])
            ]
            for i in histogram_bins.index
        ]

        lst_maxser = pd.Series(lst_maxser)

        lst_resistance = [lst_maxser[i].mean() for i in lst_maxser.index]

        resistance_df = pd.DataFrame(lst_resistance)
        resistance_df.columns = ['resistance']
        resistance_df.dropna(inplace=True)
        resistance_df.index = range(len(resistance_df))
        return pd.Series(resistance_df['resistance'])

    def find_support(self,data):
        cutoff = 2
        increment = 10

        minimums = self.find_minimums(data=data,increment=increment)

        histogram = np.histogram(minimums,bins=(int(len(minimums)/increment*increment)))
        histogram_occurences = pd.DataFrame(histogram[0])
        histogram_occurences.columns = ['occurence']
        histogram_splits = pd.DataFrame(histogram[1])
        histogram_splits.columns = ['bins']

        histogram_bins = []
        for x in histogram_splits.index:
            if x < len(histogram_splits.index)-1:
                element = [int(histogram_splits.iloc[x]), int(histogram_splits.iloc[x+1])]
                histogram_bins.append(element)

        histogram_bins = pd.DataFrame(histogram_bins)
        histogram_bins['occurence'] = histogram_occurences
        histogram_bins.columns = ['start','end','occurence']

        histogram_bins = histogram_bins[histogram_bins['occurence'] >= cutoff]
        histogram_bins.index = range(len(histogram_bins))

        data = sorted(data)
        data = pd.Series(data)

        lst_minser = [
            data[
                (data > histogram_bins['start'][i])
                & (data < histogram_bins['end'][i])
            ]
            for i in histogram_bins.index
        ]

        lst_minser = pd.Series(lst_minser)

        lst_support = [lst_minser[i].mean() for i in lst_minser.index]

        support_df = pd.DataFrame(lst_support)
        support_df.columns = ['support']
        support_df.dropna(inplace=True)
        support_df.index = range(len(support_df))
        return pd.Series(support_df['support'])