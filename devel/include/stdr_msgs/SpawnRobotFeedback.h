// Generated by gencpp from file stdr_msgs/SpawnRobotFeedback.msg
// DO NOT EDIT!


#ifndef STDR_MSGS_MESSAGE_SPAWNROBOTFEEDBACK_H
#define STDR_MSGS_MESSAGE_SPAWNROBOTFEEDBACK_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace stdr_msgs
{
template <class ContainerAllocator>
struct SpawnRobotFeedback_
{
  typedef SpawnRobotFeedback_<ContainerAllocator> Type;

  SpawnRobotFeedback_()
    {
    }
  SpawnRobotFeedback_(const ContainerAllocator& _alloc)
    {
  (void)_alloc;
    }







  typedef boost::shared_ptr< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> const> ConstPtr;

}; // struct SpawnRobotFeedback_

typedef ::stdr_msgs::SpawnRobotFeedback_<std::allocator<void> > SpawnRobotFeedback;

typedef boost::shared_ptr< ::stdr_msgs::SpawnRobotFeedback > SpawnRobotFeedbackPtr;
typedef boost::shared_ptr< ::stdr_msgs::SpawnRobotFeedback const> SpawnRobotFeedbackConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace stdr_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'nav_msgs': ['/opt/ros/kinetic/share/nav_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'stdr_msgs': ['/home/alexfeng2000/Desktop/tesroomba/src/stdr_simulator/stdr_msgs/msg', '/home/alexfeng2000/Desktop/tesroomba/devel/share/stdr_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd41d8cd98f00b204ULL;
  static const uint64_t static_value2 = 0xe9800998ecf8427eULL;
};

template<class ContainerAllocator>
struct DataType< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "stdr_msgs/SpawnRobotFeedback";
  }

  static const char* value(const ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n\
#feedback\n\
\n\
";
  }

  static const char* value(const ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream&, T)
    {}

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SpawnRobotFeedback_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream&, const std::string&, const ::stdr_msgs::SpawnRobotFeedback_<ContainerAllocator>&)
  {}
};

} // namespace message_operations
} // namespace ros

#endif // STDR_MSGS_MESSAGE_SPAWNROBOTFEEDBACK_H
