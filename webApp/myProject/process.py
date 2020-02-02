import numpy as np
import pandas as pd

class searchData:
    def __init__(self,data):
        self.data = data

    def __call__(self,templates):
        dfPicked = self.data[(self.data['template'].isin(templates))]
        sentCount = 0
        rejectCount = 0
        openCount = 0
        clickCount = 0
        for index, row in dfPicked.iterrows():
          sentCount += int(row['sent'])
          rejectCount += int(row['rejects'])
          openCount += int(row['opens'])
          clickCount += int(row['clicks'])
        deliveredCount = sentCount-rejectCount
        delivery_rate = deliveredCount/sentCount if sentCount>0 else 0
        open_rate = openCount/deliveredCount if deliveredCount>0 else 0
        click_rate = clickCount/deliveredCount if deliveredCount>0 else 0
        dfSorted = dfPicked.copy()
        dfSorted['time'] = pd.to_datetime(dfSorted['time']).dt.normalize()
        dfSorted=dfSorted[(dfSorted['time']>=pd.datetime(2018,1,1))&(dfSorted['time']<=pd.datetime(2019,12,31))]
        dfSorted=dfSorted.set_index('time',drop=True)
        dfSorted['sentCount'] = dfSorted['sent'].astype('int')
        dfSorted['rejectCount'] = dfSorted['rejects'].astype('int')
        dfSorted['openCount'] = dfSorted['opens'].astype('int')
        dfSorted['clickCount'] = dfSorted['clicks'].astype('int')
        dfMerged = dfSorted.resample('M').sum()
        dfMerged = dfMerged[(dfMerged['sentCount']>0)]
        dfMerged['deliveredCount'] = dfMerged['sentCount']-dfMerged['rejectCount']
        dfMerged['delivery rate'] = dfMerged['deliveredCount']/dfMerged['sentCount']
        dfMerged['open rate'] = dfMerged['openCount']/dfMerged['deliveredCount']
        dfMerged['clickrate'] = dfMerged['clickCount']/dfMerged['deliveredCount']

        dfMerged = dfMerged.to_period('M')
        return [sentCount,deliveredCount,delivery_rate,open_rate,click_rate,dfMerged]
