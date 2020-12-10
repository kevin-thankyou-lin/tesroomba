#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
import geometry_msgs.msg


if __name__ == '__main__':
    rospy.init_node('transform_listener')
    static_frame = rospy.get_param('~static_frame')
    dynamic_frame = rospy.get_param('~dynamic_frame')

    listener = tf.TransformListener()

    publ = rospy.Publisher('transform' + static_frame, geometry_msgs.msg.Transform, queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform(static_frame, dynamic_frame, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        cmd = geometry_msgs.msg.Transform()
        cmd.translation = trans
        cmd.rotation = rot
        publ.publish(cmd)

        rate.sleep()