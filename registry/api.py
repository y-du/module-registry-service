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

__all__ = ("Modules", "Module")


from .logger import getLogger
from .model import validator, ValidationError
from .util import genId, genHash
import snorkels
import falcon
import json


logger = getLogger(__name__.split(".", 1)[-1])


def reqDebugLog(req):
    logger.debug("method='{}' path='{}' content_type='{}'".format(req.method, req.path, req.content_type))


def reqErrorLog(req, ex):
    logger.error("method='{}' path='{}' - {}".format(req.method, req.path, ex))


class Modules:
    def __init__(self, kvs: snorkels.KeyValueStore):
        self.__kvs = kvs

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            data = dict()
            for key in self.__kvs.keys():
                data[key.decode()] = json.loads(self.__kvs.get(key))
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.body = json.dumps(data)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        if not req.content_type == falcon.MEDIA_JSON:
            resp.status = falcon.HTTP_415
        else:
            try:
                data = json.load(req.bounded_stream)
                validator(data)
                for key, srv in data["services"].items():
                    data["services"][key]["hash"] = genHash(srv)
                data["hash"] = genHash(data)
                m_id = genId()
                self.__kvs.set(m_id, json.dumps(data))
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"id": m_id})
            except ValidationError:
                resp.status = falcon.HTTP_400
                reqErrorLog(req, "validation failed")
            except Exception as ex:
                resp.status = falcon.HTTP_500
                reqErrorLog(req, ex)


class Module:
    def __init__(self, kvs: snorkels.KeyValueStore):
        self.__kvs = kvs

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, module):
        reqDebugLog(req)
        try:
            resp.body = self.__kvs.get(module)
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
        except snorkels.GetError as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_patch(self, req: falcon.request.Request, resp: falcon.response.Response, module):
        reqDebugLog(req)
        if not req.content_type == falcon.MEDIA_JSON:
            resp.status = falcon.HTTP_415
        else:
            try:
                data = json.load(req.bounded_stream)
                validator(data)
                for key, srv in data["services"].items():
                    data["services"][key]["hash"] = genHash(srv)
                data["hash"] = genHash(data)
                self.__kvs.set(module, json.dumps(data))
                resp.status = falcon.HTTP_200
            except ValidationError:
                resp.status = falcon.HTTP_400
                reqErrorLog(req, "validation failed")
            except Exception as ex:
                resp.status = falcon.HTTP_500
                reqErrorLog(req, ex)

    def on_delete(self, req: falcon.request.Request, resp: falcon.response.Response, module):
        reqDebugLog(req)
        try:
            self.__kvs.delete(module)
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)
