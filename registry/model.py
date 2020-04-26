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

component = {
    "name": str,
    "description": str,
    "services": list
}

service = {
    "name": str,
    "deployment_configs": dict,
    "service_configs": (dict, type(None)),
}

deployment_configs = {
    "image": str,
    "volumes": (dict, type(None)),
    "ports": (list, type(None)),
    "devices": (dict, type(None))
}

port = {
    "container": int,
    "host": int,
    "protocol": (str, type(None))
}


class ValidationError(Exception):
    pass


def validate(candidate, model):
    if not isinstance(candidate, dict):
        raise ValidationError
    if not candidate.keys() == model.keys():
        raise ValidationError
    for key, typ in model.items():
        if not isinstance(candidate[key], typ):
            raise ValidationError


def validator(candidate):
    validate(candidate, component)
    for srv in candidate["services"]:
        validate(srv, service)
        validate(srv["deployment_configs"], deployment_configs)
        for prt in srv["deployment_configs"]["ports"] or list():
            validate(prt, port)
