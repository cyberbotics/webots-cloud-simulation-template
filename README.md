# Template for webots.cloud simulations
This repository can be used as a template to deploy a simulation on [webots.cloud](https://webots.cloud).

## Structure
The template contains a generic project featuring the e-puck robot.
The world `e-puck.wbt` is located in the `worlds` folder.
The controller `e-puck.py` is located in the `controllers/e-puck` folder.
The robot window `simple_e-puck` is located in the `plugins/robot_windows` folder.

The defined `Dockerfile` is placed at the root of the project and implements the four lines of `Dockerfile.default`, which would have been used by [webots.cloud](https://webots.cloud) if no Dockerfile was defined.

```dockerfile
FROM cyberbotics/webots.cloud:R2022b
ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
COPY . $PROJECT_PATH
```

The following additional line allows to compile the plugin when [webots.cloud](https://webots.cloud) creates the Docker image.

```dockerfile
RUN cd $PROJECT_PATH/plugins/robot_windows/simple_e-puck && make clean && make
```

**Note**: It is also possible to directly provide the built binaries in the corresponding folders and use the default Dockerfile without any "on-the-fly" compilation.
However, it is currently not possible to compile C/C++ controllers and robot windows directly from the running simulation on [webots.cloud](https://webots.cloud).

`webots.yaml` defines the type of the simulation as a `demo`.
The `publish` parameter allows to publish the simulation to [webots.cloud](https://webots.cloud) and make it visible in the public list of simulations.
Finally, `dockerCompose:theia` sets the workspace for the online IDE.
This means that with `webots-project/controllers/` every user who logs into the simulation is allowed to modify all controllers located in the `controllers` folder.

More information is available in the [Webots User Guide](https://cyberbotics.com/doc/guide/webots-cloud?version=master#publish-cloud-based-simulations).
For more complex projects and other configurations you can head to the examples repository: [webots.cloud Simulation Examples](https://github.com/cyberbotics/webots-cloud-simulation-examples).
