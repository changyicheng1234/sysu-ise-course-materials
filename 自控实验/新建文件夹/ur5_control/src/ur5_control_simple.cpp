#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>
 
int main(int argc, char **argv)
{
    
    ros::init(argc, argv, "ur5_control_simple"); 
    ros::AsyncSpinner spinner(1);   // 多线程
    // 开启新的线程
    spinner.start();  
 
    // 初始化需要使用move group控制的机械臂中的arm group
    moveit::planning_interface::MoveGroupInterface arm("manipulator");
  
    // 允许误差  
    arm.setGoalJointTolerance(0.001);          
    // 允许的最大速度和加速度
    arm.setMaxAccelerationScalingFactor(0.2);  
    arm.setMaxVelocityScalingFactor(0.2);
 
    // 控制机械臂到达竖直位置
    arm.setNamedTarget("up"); 
    arm.move();
    ros::Duration(1).sleep();

    // 控制机械臂移动到水平位置(初始化位置)
    arm.setNamedTarget("home"); 
    arm.move();
    ros::Duration(1).sleep();
 
    ros::shutdown();
    return 0;
}




