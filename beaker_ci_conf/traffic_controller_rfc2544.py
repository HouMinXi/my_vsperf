# Copyright 2015-2017 Intel Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""RFC2544 Traffic Controller implementation.
"""
from core.traffic_controller import TrafficController
from core.results.results import IResults
from conf import settings


class TrafficControllerRFC2544(TrafficController, IResults):
    """Traffic controller for RFC2544 traffic

    Used to setup and control a traffic generator for an RFC2544 deployment
    traffic scenario.
    """

    def __init__(self, traffic_gen_class):
        """Initialise the trafficgen and store.

        :param traffic_gen_class: The traffic generator class to be used.
        """
        super().__init__(traffic_gen_class)
        self._type = 'rfc2544'
        self._tests = None

    def configure(self, traffic):
        """See TrafficController for description
        """
        super().configure(traffic)
        self._tests = int(settings.getValue('TRAFFICGEN_RFC2544_TESTS'))

    def send_traffic(self, traffic):
        """See TrafficController for description
        """
        if not self.traffic_required():
            return

        super().send_traffic(traffic)

        for packet_size in self._packet_sizes:
            # Merge framesize with the default traffic definition
            if 'l2' in traffic:
                traffic['l2'] = dict(traffic['l2'],
                                     **{'framesize': packet_size})
            else:
                traffic['l2'] = {'framesize': packet_size}
            if traffic['traffic_type'] == 'rfc2544_back2back':
                result = self._traffic_gen_class.send_rfc2544_back2back(
                    traffic, tests=self._tests, duration=self._duration, lossrate=self._lossrate)
            elif traffic['traffic_type'] == 'rfc2544_continuous':
                result = self._traffic_gen_class.send_cont_traffic(
                    traffic, duration=self._duration)
            elif traffic['traffic_type'] == 'rfc2544_throughput':
                result = self._traffic_gen_class.send_rfc2544_throughput(
                    traffic, tests=self._tests, duration=self._duration, lossrate=self._lossrate)
            elif traffic['traffic_type'] == 'rfc2544_latency':
                result = self._traffic_gen_class.send_rfc2544_latency(
                    traffic, tests=self._tests, duration=self._duration, lossrate=self._lossrate)
            else:
                raise RuntimeError("Unsupported traffic type {} was "
                                   "detected".format(traffic['traffic_type']))

            result = self._append_results(result, packet_size)
            self._results.append(result)

    def send_traffic_async(self, traffic, function):
        """See TrafficController for description
        """
        if not self.traffic_required():
            return

        super().send_traffic_async(traffic, function)

        for packet_size in self._packet_sizes:
            traffic['l2'] = {'framesize': packet_size}
            self._traffic_gen_class.start_rfc2544_throughput(
                traffic,
                tests=self._tests,
                duration=self._duration)
            self._traffic_started = True
            if len(function['args']) > 0:
                function['function'](function['args'])
            else:
                function['function']()
            result = self._traffic_gen_class.wait_rfc2544_throughput()
            result = self._append_results(result, packet_size)
            self._results.append(result)
