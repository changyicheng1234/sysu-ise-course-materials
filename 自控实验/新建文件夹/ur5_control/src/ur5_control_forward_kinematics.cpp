#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "ur5_control_forward_kinematics");
    ros::AsyncSpinner spinner(1);  // 多线程
    spinner.start();  // 开启新的线程

    // 初始化需要使用move group控制的机械臂中的arm group
    moveit::planning_interface::MoveGroupInterface arm("manipulator");

    // 允许误差  
    arm.setGoalJointTolerance(0.001);          
    // 允许的最大速度和加速度
    arm.setMaxAccelerationScalingFactor(0.2);  
    arm.setMaxVelocityScalingFactor(0.2);

    // 控制机械臂移动到初始化位置
    arm.setNamedTarget("home");
    arm.move();
    ros::Duration(1).sleep();

    // 各个关节的旋转角度
    double targetPose[6] = {0.391410, -0.676384, -0.376217, 0.0, 1.052834, 0.454125};
    std::vector<double> joint_group_positions(6);
    joint_group_positions[0] = targetPose[0];
    joint_group_positions[1] = targetPose[1];
    joint_group_positions[2] = targetPose[2];
    joint_group_positions[3] = targetPose[3];
    joint_group_positions[4] = targetPose[4];
    joint_group_positions[5] = targetPose[5];

    arm.setJointValueTarget(joint_group_positions);
    arm.move();
    ros::Duration(1).sleep();

    // 控制机械臂移动到初始化位置
    arm.setNamedTarget("home");
    arm.move();
    sleep(1);

    ros::shutdown(); 

    return 0;
}



