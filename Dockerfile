FROM cyberbotics/webots.cloud:R2022b
ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
COPY . $PROJECT_PATH
RUN cd $PROJECT_PATH/controllers/e-puck && make clean && make
RUN cd $PROJECT_PATH/plugins/robot_windows/e-puck && make clean && make
