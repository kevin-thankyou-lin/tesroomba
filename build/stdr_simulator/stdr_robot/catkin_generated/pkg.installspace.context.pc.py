# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include".split(';') if "${prefix}/include" != "" else []
PROJECT_CATKIN_DEPENDS = "roscpp;nodelet;actionlib;tf;stdr_msgs;stdr_parser;geometry_msgs;sensor_msgs;nav_msgs".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lstdr_handle_robot".split(';') if "-lstdr_handle_robot" != "" else []
PROJECT_NAME = "stdr_robot"
PROJECT_SPACE_DIR = "/home/alexfeng2000/Desktop/tesroomba/install"
PROJECT_VERSION = "0.3.2"
