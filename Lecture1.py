#!/usr/bin/env python
# coding: utf-8

# # Technical Analysis with Python - an Introduction

# ## Installing and importing required Libraries/Packages

# Install pandas-datareader, plotly and cufflinks with:
# 
# * conda install pandas-datareader (웹에서 재무 데이터 불러오기)
# * pip install cufflinks (반응형 플로틀리 차트를 생성)

# _설치에 문제가 생긴 경우 아나콘다를 최신으로 업데이트 했는지 먼저 확인_

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cufflinks as cf
from pandas_datareader import data


# # Loading Financial Data from the Web

# In[2]:


start = "2010-01-02"
end = "2020-12-31"


# In[3]:


symbol = "MSFT"


# _dataframe에는 영업일만 표시 (공휴일, 주말은 표시 안됨)_

# In[4]:


df = data.DataReader(name = symbol, data_source = "yahoo", start = start, end = end)
df


# In[5]:


df.info()


# In[6]:


symbol = ['MSFT', "GE", "AAPL"]


# In[7]:


df = data.DataReader(name = symbol, data_source = "yahoo", start = start, end = end)
df


# In[8]:


df.to_csv("stocks.csv")


# # Charting - Simple Line Charts

# In[9]:


# 인덱스 포지션 표시 -> header와 index_col 사용
# datetime 인덱스를 확실히 넣기 위해 parse_dates 통해 해당 열을 datetime 형식으로 지정
df = pd.read_csv("stocks.csv", header = [0, 1], index_col = 0, parse_dates = [0])
df


# In[10]:


df.info()


# In[11]:


df.Close


# In[12]:


df.Close.GE


# In[13]:


df.Close.GE.plot(figsize = (12, 8))
plt.show()


# In[14]:


# loc 안의 , 오른편에는 열을 지정할 수 있음 -> 멀티 인덱스이므로 묶어서 지정
df.loc["2020-06":, ("Close", "GE")].plot(figsize = (12, 8))
plt.show()


# # Charting - Interactive Line Charts with Cufflinks and Plotly

# In[15]:


df


# In[16]:


cf.set_config_file(offline = True) # 로컬(커프링크스)에 저장한다는 의미


# In[17]:


# interactive한 plot을 생성할 때에는 iplot 메서드를 사용
df.loc["2020-06":, ("Close", "GE")].iplot()


# In[18]:


df.Close.iplot()


# # Customizing Plotly Charts

# In[19]:


df.Close


# In[20]:


df.Close.iplot(fill = True)


# In[21]:


cf.colors.scales()


# In[22]:


df.Close.iplot(fill = True, colorscale = "reds")


# In[23]:


cf.getThemes()


# In[24]:


df.Close.iplot(fill = True, colorscale = "rdylbu", theme = "solar")


# In[25]:


df.Close.iplot(fill = True, colorscale = "rdylbu", theme = "solar",
              title = "US Stocks", xTitle = "Time", yTitle = "Stock Price")


# In[26]:


# spread -> 두 주가의 차이 표시 // 정규화된 자료를 볼 때 유의미함
df.Close[["GE", "AAPL"]].iplot(kind = "spread", fill = True, colorscale = "rdylbu",
                              theme = "solar", title = "GE vs. AAPL", xTitle = "Time",
                              yTitle = "Stock Price")


# # Candlestick and OHLC Charts

# In[27]:


df


# In[28]:


# 종목당 Open, High, Low, Close 값을 보고 싶으면 멀티 인덱스의 순서를 바꿔줘야함
df.swaplevel(axis = 1)


# In[29]:


ge = df.swaplevel(axis = 1).GE.copy()


# In[30]:


ge


# _candlestick 차트에서는 OHLC정보를 모두 확인할 수 있음_

# In[31]:


ge.loc["5-2017"].iplot(kind = "candle")


# In[32]:


ge.loc["5-2017"].iplot(kind = "ohlc")


# # Bar Size / Granularity

# In[33]:


# 금요일 기준(한 주간의 오른쪽 막대 기준)인 datetime 인덱스를 월요일 기준으로 바꾸기 위해
from pandas.tseries.frequencies import to_offset


# In[34]:


ge


# In[35]:


ge.loc["5-2017"].iplot(kind = "candle")


# In[36]:


# Weekly-Friday : 주기를 일주일로 잡음 (월요일 - 금요일)
weekly = ge.resample("W-Fri").ohlc()


# In[37]:


weekly
# 필요 이상의 데이터가 나온 것을 확인할 수 있음 -> ohlc 메서드 말고 agg 메서드를 사용하자


# In[38]:


ge


# In[39]:


# agg 메서드 사용 -> 각 칼럼에 다른 집계 메서드를 적용할 수 있음
weekly = ge.resample("W-Fri").agg({"Open" : "first",
                                   "High" : "max",
                                   "Low" : "min",
                                   "Close" : "last"} )


# In[40]:


weekly


# In[41]:


# datetime 인덱스 월요일 기준으로 변경
weekly.index = weekly.index - to_offset("4d")


# In[42]:


weekly


# In[43]:


# 일간 차트(ge)에서 주간차트로 변경
weekly.loc["5-2017" : "9-2017"].iplot(kind = "candle")


# # Volume Charts

# In[44]:


ge


# In[45]:


# 거래량을 주가와 함께 차트에 표시하기 위해 QuantFig 개체 생성
qf = cf.QuantFig(df = ge.loc["5-2017"])


# In[46]:


type(qf)


# In[47]:


qf.add_volume(colorchange = False)


# In[48]:


qf.iplot(title = "GE", name = "GE")


# In[ ]:





# # Technical Indicators - an Overview

# In[49]:


ge


# In[50]:


qf = cf.QuantFig(df = ge.loc["2017" : "2018"])


# _이동평균선은 움직임을 좀 더 매끄럽게 해줌_

# In[51]:


# 20일간의 단순이동평균선(SMA20)
qf.add_sma(periods = 20)


# In[52]:


qf.iplot(title = "GE", name = "GE")


# In[53]:


# SMA100 추가
qf.add_sma(periods = 100)


# In[54]:


# SMA20에 볼린저밴드 적용
qf.add_bollinger_bands(periods = 20, boll_std = 2)


# In[55]:


qf.iplot(title = "GE", name = "GE")


# In[56]:


qf = cf.QuantFig(df = ge.loc["5-2017" : "9-2017"])


# In[57]:


qf.iplot(title = "GE", name = "GE")


# In[58]:


qf.add_macd()
qf.add_dmi()


# In[59]:


qf.iplot(title = "GE", name = "GE")


# # Trend Lines

# In[60]:


ge


# ### Uptrend (Higher Lows)

# In[61]:


qf = cf.QuantFig(df = ge.loc["2012"])


# In[62]:


qf.add_trendline(date0 = "2012-07-12", date1 = "2012-09-04")


# In[63]:


qf.iplot(title = "GE", name = "GE")


# ### Downtrend (Lower Highs)

# In[64]:


qf = cf.QuantFig(df = ge.loc["2018"])


# In[65]:


qf.add_trendline(date0 = "2018-05-22", date1 = "2018-10-09")


# In[66]:


qf.iplot(title = "GE", name = "GE")


# # Support and Resistance Levels

# In[67]:


ge


# ### Resistance Lines

# In[68]:


qf = cf.QuantFig(df = ge.loc["2012"])


# In[69]:


qf.add_resistance(date = "2012-03-28")


# In[70]:


qf.iplot(title = "GE", name = "GE")


# ### Support Lines

# In[71]:


qf = cf.QuantFig(df = ge.loc["2013"])


# In[72]:


qf.add_support(date = "2013-06-24")


# In[73]:


qf.iplot(title = "GE", name = "GE")

