#!/usr/bin/python
################################################################################
#
# Node to wrap the OccupancyGrid2d class.
#
################################################################################

from occ_grid import OccupancyGrid2d

import rospy
import sys

if __name__ == "__main__":
    rospy.init_node("mapping_node")

    og = OccupancyGrid2d("/node/map_points", 50, 50, 0.5, 0.75, "occ_grid/grid", "occ_grid/vis")
    
    rospy.spin()
