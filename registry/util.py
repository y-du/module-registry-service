"""
   Copyright 2020 Yann Dumont

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import hashlib
import time
import base64
import uuid


def genId():
    uuid_time_str = '{}{}'.format(
        hashlib.md5(uuid.uuid4().bytes).hexdigest(),
        time.time()
    )
    return base64.urlsafe_b64encode(hashlib.md5(uuid_time_str.encode()).digest()).decode().rstrip('=')


def flatten(data):
    li = list()
    for key, val in data.items():
        if not isinstance(val, (list, dict)):
            li.append("{}{}".format(key, val))
        elif isinstance(val, list):
            li.append(key)
            for i in val:
                li = li + flatten(i)
        elif isinstance(val, dict):
            li.append(key)
            li = li + flatten(val)
    return li


def genHash(data):
    res = flatten(data)
    res.sort()
    res = "".join(res)
    return hashlib.sha256(res.encode()).hexdigest()
