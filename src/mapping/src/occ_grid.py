import rospy
import tf2_ros as tf
import tf

from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point

HEIGHT_THRESHOLD = 1

class OccupancyGrid2d(object):
    def __init__(self, pointcloud_topic, x_num, y_num, occupied_update, occupied_threshold, 
        vis_topic, x_max = 25, x_min = -25, y_max = 25, y_min = -25):
        self._x_num = x_num
        self._y_num = y_num
        self._x_max = x_max
        self._y_min = y_min
        self._x_min = x_min
        self._y_max = y_max
        self._x_res = (self._x_max - self._x_min) / self._x_num
        self._y_res = (self._y_max - self._y_min) / self._y_num
        self._occupied_update = occupied_update
        self._occupied_threshold = occupied_threshold
        self._tf_buffer = tf2_ros.Buffer()
        self._tf_listener = tf2_ros.TransformListener(self._tf_buffer)
        self._map = np.zeros((self._x_num, self._y_num))
        self._pointcloud_topic = pointcloud_topic
        self._vis_topic = vis_topic


    def RegisterCallbacks(self):
        # Subscriber.
        self._sensor_sub = rospy.Subscriber(self._pointcloud_topic,
                                            PointCloud2,
                                            self.update_grid,
                                            queue_size=1)

        # Publisher.
        self._vis_pub = rospy.Publisher(self._vis_topic,
                                        Marker,
                                        queue_size=10)

        return True


    def update_grid(self, msg):
        for p in msg.points:
            if p.y <= HEIGHT_THRESHOLD:
                grid_point = self.PointToVoxel(p.x, p.y)
                self._map += self._occupied_update


    # Convert (x, y) coordinates in fixed frame to grid coordinates.
    def PointToVoxel(self, x, y):
        grid_x = int((x - self._x_min) / self._x_res)
        grid_y = int((y - self._y_min) / self._y_res)

        return (grid_x, grid_y)

    # Get the center point (x, y) corresponding to the given voxel.
    def VoxelCenter(self, ii, jj):
        center_x = self._x_min + (0.5 + ii) * self._x_res
        center_y = self._y_min + (0.5 + jj) * self._y_res

        return (center_x, center_y)

    # Convert between probabity and log-odds.
    def ProbabilityToLogOdds(self, p):
        return np.log(p / (1.0 - p))

    def LogOddsToProbability(self, l):
        return 1.0 / (1.0 + np.exp(-l))


    # Colormap to take log odds at a voxel to a RGBA color.
    def Colormap(self, ii, jj):
        p = self.LogOddsToProbability(self._map[ii, jj])

        c = ColorRGBA()
        c.r = p
        c.g = 0.1
        c.b = 1.0 - p
        c.a = 0.75
        return c

    # Visualize the map as a collection of flat cubes instead of
    # as a built-in OccupancyGrid message, since that gives us more
    # flexibility for things like color maps and stuff.
    # See http://wiki.ros.org/rviz/DisplayTypes/Marker for a brief tutorial.
    def Visualize(self):
        m = Marker()
        m.header.stamp = rospy.Time.now()
        m.header.frame_id = self._fixed_frame
        m.ns = "map"
        m.id = 0
        m.type = Marker.CUBE_LIST
        m.action = Marker.ADD
        m.scale.x = self._x_res
        m.scale.y = self._y_res
        m.scale.z = 0.01

        for ii in range(self._x_num):
            for jj in range(self._y_num):
                p = Point(0.0, 0.0, 0.0)
                (p.x, p.y) = self.VoxelCenter(ii, jj)

                m.points.append(p)
                m.colors.append(self.Colormap(ii, jj))

        self._vis_pub.publish(m)

