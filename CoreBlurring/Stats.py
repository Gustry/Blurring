# -*- coding: utf-8 -*-
'''
Created on 7 août 2014

@author: etienne
'''

import math

class Stats:

    def __init__(self,listStats):
        listStats.sort()
        self.listStats = listStats 
        self.nbItems = len(listStats)
    
    def count(self):
        return self.nbItems

    def min(self):
        return self.listStats[0]
    
    def max(self):
        return self.listStats[-1]
    
    def range(self):
        return self.max() - self.min()

    def average(self) :
        return sum(self.listStats) / self.nbItems
    
    def stat_variance(self) :
        mq = self.average()**2
        s = sum( [ x**2 for x in self.listStats ] )
        variance = s / self.nbItems - mq
        return variance

    def stat_ecart_type(self):
        variance = self.stat_variance()
        ecart_type = math.sqrt(variance)
        return ecart_type       