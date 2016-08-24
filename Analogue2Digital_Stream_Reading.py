# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:39:11 2016

@author: Yaqub
"""

import DAQT7_Objective as DAQ
import matplotlib.pyplot as plt
import numpy as np
import time
import h5py
import datetime

#%%
DAQ1 = DAQ.DetectDAQT7()

SamplingRate = 10000  # 10kHz
Read, Starting, Ending = DAQ1.streamRead(SamplingRate, 'AIN1')

plt.plot(Read[0])
plt.show()