# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 20:55:13 2018

@author: THINKPAD
"""

import matplotlib.pyplot as plt
#import numpy as np/

def metrics_roc(ts_real_Y, tr_real_Y,ts_pred_prob,tr_pred_prob):
    from sklearn import metrics 
    fpr_test, tpr_test, th_test = metrics.roc_curve(ts_real_Y, ts_pred_prob)
    fpr_train, tpr_train, th_train = metrics.roc_curve(tr_real_Y, tr_pred_prob)
    plt.figure(figsize=[3, 3])
    plt.plot(fpr_test, tpr_test, 'b--')
    plt.plot(fpr_train, tpr_train, 'r-')
    plt.title('ROC curve::Test is Blue')
    print('Test AUC = %.4f' %metrics.auc(fpr_test, tpr_test))
    print('Train AUC = %.4f' %metrics.auc(fpr_train, tpr_train))
    plt.show()

def metrics_pr(ts_real_Y, tr_real_Y,ts_pred_prob,tr_pred_prob):
    from sklearn import metrics 
    precision_test, recall_test, th_test = metrics.precision_recall_curve(ts_real_Y, ts_pred_prob)
    precision_train, recall_train, th_train = metrics.precision_recall_curve(tr_real_Y, tr_pred_prob)
    plt.figure(figsize=[3, 3])
    plt.plot(recall_test,precision_test,  'b--')
    plt.plot(recall_train,precision_train,  'r-')
    plt.title('precision-Recall curve:Test is Blue')
    print('Test AP = %.4f' %metrics.average_precision_score(ts_real_Y, ts_pred_prob))
    print('Train AP = %.4f' %metrics.average_precision_score(tr_real_Y, tr_pred_prob))
    plt.show()