# -*- coding: utf-8 -*-
#
# Poio Tools for Linguists
#
# Copyright (C) 2009-2013 Poio Project
# Author: Peter Bouda <pbouda@cidles.eu>
# URL: <http://media.cidles.eu/poio/>
# For license information, see LICENSE

from __future__ import absolute_import, unicode_literals

import abc

class Observer(object):
    """
    Base class for classes that want to observer other classes, e.g. the
    PredictorActivator.

    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update(self, observable):
        raise NotImplementedError("Method must be implemented")


class Oberservable(object):
    """
    Base class for everything that needs observation, e.g. the predictors.

    """

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

class Dispatcher(object):
    """
    Dispatches observable notifications.

    """

    def __init__(self, obj):
        self.observables = []
        self.dispatch_dict = {}
        self.obj = obj

    def map(self, observable, func):
        observable.attach(obj)
        self.observables.append(observable)
        self.dispatch_dict[observable] = func
        self.dispatch(observable)

    def dispatch(self, observable):
        handler_func = self.dispatch_dict[observable]
        handler_func(observable)
