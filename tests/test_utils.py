from datetime import datetime

from relayer import utils

from . import BaseTestCase


class TestUtils(BaseTestCase):

    def test_elapsed_time_in_milliseconds(self):
        start_time = datetime(2016, 6, 21, 15, 12, 5, 500000)
        end_time = datetime(2016, 6, 21, 15, 12, 6, 600000)
        milliseconds = utils.get_elapsed_time_in_milliseconds(start_time, end_time)
        milliseconds.should.equal(1100.0)
        end_time = datetime(2016, 6, 21, 15, 12, 6, 600500)
        milliseconds = utils.get_elapsed_time_in_milliseconds(start_time, end_time)
        milliseconds.should.equal(1100.5)
