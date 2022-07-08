# Template for webots.cloud simulations
Use this repository as a template to deploy a simulation on [webots.cloud](webots.cloud).

## Structure
The template contains a generic project featuring the e-puck robot.
The world `e-puck.wbt` is located in the `worlds` folder.
The controller `e-puck.c` is located in the `controllers/e-puck` folder.
The `e-puck` robot window is located in the `plugins` folder.
The `E-puck.proto` PROTO is located in the `protos` folder.

The defined `Dockerfile` is placed at the root of the project and implements the four lines of `Dockerfile.default`, which would have been used by [webots.cloud](webots.cloud) if no Dockerfile was defined.

```dockerfile
FROM cyberbotics/webots.cloud:R2022b
ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
COPY . $PROJECT_PATH
```

The following two additional lines allow to compile the controller and the plugin when [webots.cloud](webots.cloud) creates the Docker image.

```dockerfile
RUN cd $PROJECT_PATH/controllers/e-puck && make clean && make
RUN cd $PROJECT_PATH/plugins/robot_windows/e-puck && make clean && make
```

**Note**: It is also possible to directly provide the built binaries in the corresponding folders and use the default Dockerfile without any "on-the-fly" compilation.

`webots.yaml` defines the type of the simulation as a `demo`.
The `publish` parameter allows to publish the simulation to [webots.cloud](webots.cloud) and make it visible in the public list of simulations.
Finally, `dockerCompose:theia` sets the workspace for the online IDE.
This means that with `webots-project/controllers/` each user which connects to the simulation is allowed to edit all controllers located in the `controllers` folder.

More information is available in the [Webots User Guide](https://cyberbotics.com/doc/guide/webots-cloud?version=master#publish-cloud-based-simulations).
