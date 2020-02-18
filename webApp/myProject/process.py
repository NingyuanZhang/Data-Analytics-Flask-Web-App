import numpy as np
import pandas as pd

class searchData:
    def __init__(self,data):
        self.data = data

    def __call__(self,templates,Date1,Date2):
        startDate = Date1.split("/")
        endDate = Date2.split("/")
        dfPicked = self.data[(self.data['template'].isin(templates))]
        sentCount = 0
        rejectCount = 0
        openCount = 0
        clickCount = 0
        for index, row in dfPicked.iterrows():
          sentCount += int(row['sent'])
          rejectCount += int(row['rejects'])
          openCount += int(row['unique_opens'])
          clickCount += int(row['unique_clicks'])
        deliveredCount = sentCount-rejectCount
        delivery_rate = format(deliveredCount/sentCount if sentCount>0 else 0, '.2%')
        open_rate = format(openCount/deliveredCount if deliveredCount>0 else 0, '.2%')
        click_rate = format(clickCount/deliveredCount if deliveredCount>0 else 0, '.2%')
        dfSorted = dfPicked.copy()
        dfSorted['time'] = pd.to_datetime(dfSorted['time']).dt.normalize()
        dfSorted=dfSorted[(dfSorted['time']>=pd.datetime(int(startDate[2]),int(startDate[0]),int(startDate[1])))&(dfSorted['time']<=pd.datetime(int(endDate[2]),int(endDate[0]),int(endDate[1])))]
        dfSorted=dfSorted.set_index('time',drop=True)
        dfSorted['SentCount'] = dfSorted['sent'].astype('int')
        dfSorted['RejectCount'] = dfSorted['rejects'].astype('int')
        dfSorted['OpenCount'] = dfSorted['unique_opens'].astype('int')
        dfSorted['ClickCount'] = dfSorted['unique_clicks'].astype('int')
        dfSorted['Hard_bouncesCount'] = dfSorted['hard_bounces'].astype('int')
        dfSorted['Soft_bounceCount'] = dfSorted['soft_bounces'].astype('int')
        dfMerged = dfSorted[['ClickCount','OpenCount','SentCount','Hard_bouncesCount','Soft_bounceCount']].resample('M').sum()
        dfMerged = dfMerged[(dfMerged['SentCount']>0)]
        dfMerged['DeliveredCount'] = dfMerged['SentCount']-dfMerged['Hard_bouncesCount']-dfMerged['Soft_bounceCount']
        dfMerged['Delivery Rate'] = dfMerged['DeliveredCount']/dfMerged['SentCount']
        dfMerged['Open Rate'] = dfMerged['OpenCount']/dfMerged['DeliveredCount']
        dfMerged['Click Rate'] = dfMerged['ClickCount']/dfMerged['DeliveredCount']
        dfMerged = dfMerged.to_period('M')
        dfMerged['Click Rate'] = dfMerged['Click Rate'].apply(lambda x: format(x, '.2%'))
        dfMerged['Open Rate'] = dfMerged['Open Rate'].apply(lambda x: format(x, '.2%'))
        dfMerged['Delivery Rate'] = dfMerged['Delivery Rate'].apply(lambda x: format(x, '.2%'))
        dfMerged = dfMerged[['SentCount','Hard_bouncesCount','Soft_bounceCount','DeliveredCount','OpenCount','ClickCount','Open Rate','Click Rate']]

        dfDay = dfSorted[['ClickCount','OpenCount','SentCount','Hard_bouncesCount','Soft_bounceCount']].resample('D').sum()
        dfDay['DeliveredCount'] = dfDay['SentCount']-dfDay['Hard_bouncesCount']-dfDay['Soft_bounceCount']
        dfDay['Delivery Rate'] = dfDay['DeliveredCount']/dfDay['SentCount']
        dfDay['Open Rate'] = dfDay['OpenCount']/dfDay['DeliveredCount']
        dfDay['Click Rate'] = dfDay['ClickCount']/dfDay['DeliveredCount']
        dfDay = dfDay[(dfDay['SentCount']>0)]
        dfDay['Click Rate'] = dfDay['Click Rate'].apply(lambda x: format(x, '.2%'))
        dfDay['Open Rate'] = dfDay['Open Rate'].apply(lambda x: format(x, '.2%'))
        dfDay['Delivery Rate'] = dfDay['Delivery Rate'].apply(lambda x: format(x, '.2%'))
        dfDay = dfDay[['SentCount','Hard_bouncesCount','Soft_bounceCount','DeliveredCount','OpenCount','ClickCount','Open Rate','Click Rate']]

        return [sentCount,deliveredCount,delivery_rate,open_rate,click_rate,dfMerged,dfDay]
