### /components

**GET**

_List all components._

    Response media type: application/json
    
    Example: 
    
    {
      "tFAqmEAaNtm6OrszjvKX4w": {
        "name": "Test Component",
        "description": "Test description",
        "hash": "78e6cc4779a0c0f4c98edf2ffe92438b7843c298ca3e72cb1a7ea759bc4e5559",
        "services": [
          {
            "name": "test-service",
            "deployment_configs": {
              "image": "test:1.5",
              "volumes": {
                "data": "/data",
                "data2": "/data2"
              },
              "ports": [
                {
                  "container": 80,
                  "host": 80,
                  "protocol": null
                },
                {
                  "container": 9000,
                  "host": 9000,
                  "protocol": "udp"
                }
              ]
            },
            "service_configs": {
              "DELAY": "12",
              "LEVEL": "info"
            }
          }
        ]
      }
    }

**POST**

_Add a new component._

    Request media type: application/json
    
    {
      "name": <string>,
      "description": <string>,
      "services": [
        {
          "name": <string>,
          "deployment_configs": {
            "image": <string>,
            "volumes": {<string>:<string>},
            "ports": [
              {
                "container": <number>,
                "host": <number>,
                "protocol": <string/null>       # "tcp", "udp", "sctp"
              }
            ]
          },
          "service_configs": {<string>:<string/number>}
        }
      ]
    }

### /components/{component}

**PATCH**

_Update existing component._

    Request media type: application/json
    
    Example:

    {
      "name": "Test Component 2",
      "description": "Test description 2",
      "services": [
        {
          "name": "test-service-2",
          "deployment_configs": {
            "image": "test2:1.2.5",
            "volumes": {
              "data": "/app/data"
            },
            "ports": [
              {
                "container": 80,
                "host": 80,
                "protocol": null
              }
            ]
          },
          "service_configs": {
            "LEVEL": "info"
          }
        }
      ]
    }

**DELETE**

_Remove component._
