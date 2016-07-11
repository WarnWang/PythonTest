#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: adf_filter
# Author: warn
# Date: 29/12/2015 10:24

import numpy as np


def get_pvalue(test_list):
    regression = 'c'
    x = np.asarray(test_list)
    nobs = x.shape[0]

    maxlag = int(np.ceil(12 * np.power(nobs / 100.0, 1 / 4.0)))

    xdiff = np.diff(x)

    # TODO: lagmat
    xdall = lagmat(xdiff[:, None], maxlag, trim='both', original='in')
    nobs = xdall.shape[0]
    xdall[:, 0] = x[-nobs - 1: -1]
    xdshort = xdiff[-nobs:]
    fullRHS = add_constant(xdall, prepend=True, has_constant='skip')
    startlag = fullRHS.shape[1] - xdall.shape[1] + 1
    icbest, bestlag = _autolag(OLS, xdshort, fullRHS, startlag, maxlag, autolag)
    bestlag -= startlag
    xdall = lagmat(xdiff[:, None], bestlag, trim='both', original='in')
    nobs = xdall.shape[0]
    xdall[:, 0] = x[-nobs - 1:-1]  # replace 0 xdiff with level of path
    xdshort = xdiff[-nobs:]
    usedlag = bestlag
    resols = OLS(xdshort, add_constant(xdall[:, :usedlag + 1], prepend=True, has_constant='skip')).fit()
    adfstat = resols.tvalues[0]
    pvalue = mackinnonp(adfstat, regression=regression, N=1)
    return pvalue
