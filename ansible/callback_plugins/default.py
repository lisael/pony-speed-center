# upstream: https://gist.github.com/cliffano/9868180

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# For some reason this has to be done
import imp
path = imp.find_module('ansible')[1]
default_path = path + '/plugins/callback/default.py'
default = imp.load_source('ansible.plugins.callback.default', default_path)


class CallbackModule(default.CallbackModule):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'default'

    def _dump_results(self, result):
        result['_ansible_verbose_always'] = True

        save = {}
        for key in ['stdout', 'stdout_lines', 'stderr', 'stderr_lines', 'msg']:
            if key in result:
                save[key] = result.pop(key)

        output = super(CallbackModule, self)._dump_results(result)

        for key in ['stdout', 'stderr', 'msg']:
            if key in save and save[key]:
                output += '\n\n%s:\n\n%s\n' % (key.upper(), save[key])

        for key, value in save.items():
            result[key] = value

        return output
