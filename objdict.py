#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#    Copyright 2020 Cristhian Willrich Bilhalva
#
#   This file is part of python-facebook-api.
#
#   python - facebook - api is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   python - facebook - api is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with python-facebook-api.  If not, see <https://www.gnu.org/licenses/>
#


class objdict(dict):
    def __init__(self,*args,**kwargs):
        dict.__init__(self,*args,**kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        if item in self:
            return self[item]
        else:
            raise AttributeError('This item does\'t exist!')

    def __delattr__(self, item):
        if self.get(item):
            del self[item]
        else:
            raise AttributeError('This item does\'t exist!')

