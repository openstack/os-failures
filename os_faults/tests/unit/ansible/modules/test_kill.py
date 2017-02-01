# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import ddt
import mock

from os_faults.ansible.modules import kill
from os_faults.tests.unit import test


@ddt.ddt
class KillTestCase(test.TestCase):

    @ddt.data(['foo', 9, 'bash -c "ps ax | grep -v grep | grep \'foo\' '
                         '| awk {\'print $1\'} | xargs kill -9"'],
              ['bar', 3, 'bash -c "ps ax | grep -v grep | grep \'bar\' '
                         '| awk {\'print $1\'} | xargs kill -3"'])
    @ddt.unpack
    @mock.patch("os_faults.ansible.modules.kill.AnsibleModule")
    def test_main(self, grep, sig, cmd, mock_ansible_module):
        ansible_module_inst = mock_ansible_module.return_value
        ansible_module_inst.run_command.return_value = [
            'myrc', 'mystdout', 'mystderr']
        ansible_module_inst.params = {
            'grep': grep,
            'sig': sig,
        }
        kill.main()
        ansible_module_inst.exit_json.assert_called_once_with(
            cmd=cmd,
            rc='myrc',
            stdout='mystdout',
            stderr='mystderr',
        )
