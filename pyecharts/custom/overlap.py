# coding=utf-8

import copy
from pyecharts.constants import PAGE_TITLE
from pyecharts.base import Base


class Overlap(Base):

    def __init__(self, page_title=PAGE_TITLE,
                 width=800,
                 height=400):
        super(Overlap, self).__init__(
            width=width, height=height
        )
        self._page_title = page_title

    def add(self, chart,
            xaxis_index=0,
            yaxis_index=0,
            is_add_xaxis=False,
            is_add_yaxis=False):
        """

        :param chart:
            chart instance
        :param xaxis_index:
            xAxis index
        :param yaxis_index:
            yAxis index
        :param is_add_xaxis:
            whether to add a new xaxis
        :param is_add_yaxis:
            whether to add a new yaxis
        :return:
        """
        if not self._option:
            self._option = copy.deepcopy(chart.options)
            self._series_id = self._option.get('series')[0].get('seriesId')
            self._js_dependencies = chart.js_dependencies
        else:
            _series = (
                chart.options.get('legend')[0].get('data'),
                chart.options.get('series'),
                chart.options.get('xAxis')[0],
                chart.options.get('yAxis')[0],
                is_add_xaxis,
                is_add_yaxis,
                xaxis_index,
                yaxis_index
            )
            self.__custom(_series)
            self._js_dependencies = self._js_dependencies.union(
                chart.js_dependencies)

    def __custom(self, series):
        """ Appends the data for the series of the chart type

        :param series:
            series data
        """
        (_name, _series, _xaxis, _yaxis, is_add_xaxis, is_add_yaxis,
         _xaxis_index, _yaxis_index) = series
        for n in _name:
            self._option.get('legend')[0].get('data').append(n)
        for s in _series:
            s.update(xAxisIndex=_xaxis_index, yAxisIndex=_yaxis_index,
                     seriesId=self._series_id)
            self._option.get('series').append(s)

        if is_add_xaxis:
            self._option.get('xAxis').append(_xaxis)
        if is_add_yaxis:
            self._option.get('yAxis').append(_yaxis)
