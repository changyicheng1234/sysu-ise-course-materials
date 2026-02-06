#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "ur5_control_inverse_kinematics");
    ros::AsyncSpinner spinner(1);  // 多线程
    // 开启新的线程
    spinner.start();  

    // 初始化需要使用move group控制的机械臂中的arm group
    moveit::planning_interface::MoveGroupInterface arm("manipulator");

    // 获取终端link的名称
    std::string end_effector_link = arm.getEndEffectorLink();

    // 设置目标位置所使用的参考坐标系
    std::string reference_frame = "base_link";
    arm.setPoseReferenceFrame(reference_frame);
    
    // 当运动规划失败后，允许重新规划
    arm.allowReplanning(true);

    // 设置位置(单位：米)和姿态（单位：弧度）的允许误差
    arm.setGoalPositionTolerance(0.01);
    arm.setGoalOrientationTolerance(0.05);
    // 设置允许的最大速度和加速度
    arm.setMaxAccelerationScalingFactor(0.2);
    arm.setMaxVelocityScalingFactor(0.2);

    // 控制机械臂移动到初始化位置
    arm.setNamedTarget("home");
    arm.move();
    ros::Duration(1).sleep();

    // 设置机器人终端的目标位置
    double target_position[3] = {0.749964, 0.358583, 0.158541};
    double target_orientation[4] = {-0.707509, -0.706703, 0.0012239, 0.00121894};
    geometry_msgs::Pose target_pose;
    target_pose.position.x = target_position[0];
    target_pose.position.y = target_position[1];
    target_pose.position.z = target_position[2]; 
    target_pose.orientation.x = target_orientation[0];
    target_pose.orientation.y = target_orientation[1];
    target_pose.orientation.z = target_orientation[2];
    target_pose.orientation.w = target_orientation[3];
  
    // 设置机器臂当前的状态作为运动初始状态
    arm.setStartStateToCurrentState();

    arm.setPoseTarget(target_pose, end_effector_link);

    // 进行运动规划，计算机器人移动到目标的运动轨迹，此时只是计算出轨迹，并不会控制机械臂运动
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    moveit::planning_interface::MoveItErrorCode success = arm.plan(plan);

    ROS_INFO("Plan (pose goal) %s", success?"":"FAILED");

    // 机械臂按照规划的轨迹开始运动
    if (success)
        arm.execute(plan);
    ros::Duration(1).sleep();

    // 控制机械臂先回到初始化位置
    arm.setNamedTarget("home");
    arm.move();
    ros::Duration(1).sleep();

    ros::shutdown(); 
    return 0;
}


