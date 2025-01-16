# tcp-servers
Simple TCP servers and test clients

## asyncio-server-command
An Asyncio TCP server that responds to client commands. Valid commands are sent to all connected clients.

```
├── asyncio-server-command
│   ├── esp-mesh-lite
│   │   └── mesh_local_control
│   └── python
│       ├── client
│       └── server
```
[mesh_local_control](https://github.com/espressif/esp-mesh-lite/tree/master/examples/mesh_local_control) is based on the esp-idf mesh-lite example and will control the on board LED for nodes in a mesh network. Commands can be sent sent from the Python client or nc.
