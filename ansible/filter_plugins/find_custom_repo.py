# Copyright 2019 Caoyingjun
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

DOCUMENTATION = '''
author: Caoyingjun
'''

# kubez-ansible custom jinja2 filters
#
# k3s 之后 to_socket / get_runtime_type 已无用（不再拼 kubeadm join 的
# --container-runtime-endpoint），此处仅保留自定义源所需的 find_custom_repo。


def find_custom_repo(ctx, *args, **kwargs):
    """优先使用 repo_dir 下与目标文件同名的自定义源文件。

    例如 dest=/etc/apt/sources.list、repo_dir=/etc/kubez/repo 时，
    如果 /etc/kubez/repo/sources.list 存在就用它，否则回落到内置模板。
    """
    dest = kwargs.get('dest')
    repo_dir = kwargs.get('repo_dir')

    parts = dest.split('/')
    repo_name = parts[len(parts) - 1]

    custom_repo = os.path.join(repo_dir, repo_name)
    if os.path.exists(custom_repo):
        return custom_repo
    else:
        return ctx


class FilterModule(object):
    '''Kubez-ansible custom jinja2 filters '''

    def filters(self):
        return {
            'find_custom_repo': find_custom_repo
        }
