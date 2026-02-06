#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <iostream>

using std::cout;
using std::endl;
 
int main(int argc, char **argv)
{
    ros::init(argc, argv, "get_pose");
    ros::AsyncSpinner spinner(1);
    spinner.start();

    moveit::planning_interface::MoveGroupInterface arm("manipulator");
  
    std::string end_effector_link = arm.getEndEffectorLink();  // 获取终端link的名称
   
    std::string reference_frame = "base_link";   // 设置目标位置所使用的参考坐标系
    arm.setPoseReferenceFrame(reference_frame);

    geometry_msgs::Pose now_pose = arm.getCurrentPose(end_effector_link).pose;
    cout << "now Robot position: [x, y, z]: [" 
	<< now_pose.position.x << ", " 
	<< now_pose.position.y << ", " 
	<< now_pose.position.z << "]" << endl;
    cout << "now Robot orientation: [x, y, z, w]: [" 
	<< now_pose.orientation.x << ", " 
	<< now_pose.orientation.y << ", "
	<< now_pose.orientation.z << ", "
	<< now_pose.orientation.w << "]"
	<< endl;
}
