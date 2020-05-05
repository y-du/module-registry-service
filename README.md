### /modules

**GET**

_List all modules._

    Response media type: application/json
    
    Example: 
    
    {
      "sdfFqsWdfgYafhYh5VQ": {
        "name": "Gateway-Core",
        "description": "Core gateway services.",
        "services": {
          "dm": {
            "deployment_configs": {
              "image": "repository/dm-service:dev",
              "volumes": null,
              "devices": null,
              "ports": [
                {
                  "container": 80,
                  "host": 6001,
                  "protocol": null
                }
              ]
            },
            "service_configs": {
              "LOGGER_LEVEL": "debug"
            }
          }
        },
        "hash": "258cb56ee0550f7afae35133eeb7cde36d84a863bac713e3b7f4910a957d8ecd"
      }
    }

**POST**

_Add a new module._

    Request media type: application/json
    
    {
      "name": <string>,
      "description": <string>,
      "services": {
        <string>: {
          "deployment_configs": {
            "image": <string>,
            "volumes": {<string>:<string>},                 # can be null
            "devices": {<string>:<string>},                 # can be null
            "ports": [                                      # can be null
              {
                "container": <number>,
                "host": <number>,
                "protocol": <string/null>                   # "tcp", "udp", "sctp"
              }
            ]
          },
          "service_configs": {<string>:<string/number>}     # can be null
        }
      }
    }

### /modules/{module}

**PATCH**

_Update existing module._

    Request media type: application/json
    
    Example:
    
    PATCH /modules/sdfFqsWdfgYafhYh5VQ

    {
      "name": "Gateway-Core",
      "description": "Core gateway services.",
      "services": {
        "dm": {
          "deployment_configs": {
            "image": "repository/dm-service:latest",
            "volumes": null,
            "devices": null,
            "ports": [
              {
                "container": 8000,
                "host": 6001,
                "protocol": null
              }
            ]
          },
          "service_configs": {
            "LOGGER_LEVEL": "info"
          }
        }
      }
    }

**DELETE**

_Remove module._
