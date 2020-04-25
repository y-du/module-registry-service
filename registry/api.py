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

__all__ = ("Components", "Component")


from .model import validator, ValidationError
from .util import genId, genHash
import snorkels
import falcon
import json


class Components:
    def __init__(self, kvs: snorkels.KeyValueStore):
        self.__kvs = kvs

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response):
        try:
            data = dict()
            for key in self.__kvs.keys():
                data[key.decode()] = json.loads(self.__kvs.get(key))
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.body = json.dumps(data)
        except snorkels.KVSError:
            resp.status = falcon.HTTP_500

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response):
        if not req.content_type == falcon.MEDIA_JSON:
            resp.status = falcon.HTTP_415
        else:
            try:
                data = json.load(req.bounded_stream)
                validator(data)
                c_id = genId()
                data["hash"] = genHash(data)
                self.__kvs.set(c_id, json.dumps(data))
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"id": c_id})
            except ValidationError:
                resp.status = falcon.HTTP_400
            except snorkels.KVSError:
                resp.status = falcon.HTTP_500


class Component:
    def __init__(self, kvs: snorkels.KeyValueStore):
        self.__kvs = kvs

    def on_patch(self, req: falcon.request.Request, resp: falcon.response.Response, c_id):
        if not req.content_type == falcon.MEDIA_JSON:
            resp.status = falcon.HTTP_415
        else:
            try:
                data = json.load(req.bounded_stream)
                validator(data)
                data["hash"] = genHash(data)
                self.__kvs.set(c_id, json.dumps(data))
                resp.status = falcon.HTTP_200
            except ValidationError:
                resp.status = falcon.HTTP_400
            except snorkels.KVSError:
                resp.status = falcon.HTTP_500

    def on_delete(self, req: falcon.request.Request, resp: falcon.response.Response, c_id):
        try:
            self.__kvs.delete(c_id)
            resp.status = falcon.HTTP_200
        except snorkels.KVSError:
            resp.status = falcon.HTTP_500
