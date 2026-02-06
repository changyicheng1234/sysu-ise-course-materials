#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <vector>
 
int main(int argc, char **argv)
{
    ros::init(argc, argv, "ur5_control_cartesian");
    ros::AsyncSpinner spinner(1);
    spinner.start();

    moveit::planning_interface::MoveGroupInterface arm("manipulator");

    // 获取终端link的名称
    std::string end_effector_link = arm.getEndEffectorLink();  
    std::cout << "end_effector_link: " << end_effector_link << std::endl;
   
    std::string reference_frame = "base_link";   // 目标位置所使用的参考坐标系
    arm.setPoseReferenceFrame(reference_frame);

    // 当运动规划失败后，允许重新规划
    arm.allowReplanning(true);  
    arm.setGoalJointTolerance(0.001);
    //设置位置(单位：米)和姿态（单位：弧度）的允许误差
    arm.setGoalPositionTolerance(0.01);
    arm.setGoalOrientationTolerance(0.1);
    // 设置允许的最大速度和最大加速度
    arm.setMaxAccelerationScalingFactor(0.2); 
    arm.setMaxVelocityScalingFactor(0.2);

    // 控制机械臂移动到初始化位置
    arm.setNamedTarget("home");
    arm.move();
    ros::Duration(1).sleep();

    std::vector<geometry_msgs::Pose> waypoints;

    geometry_msgs::Pose start_pose = arm.getCurrentPose(end_effector_link).pose;
    
    double target_position[3] = {0.749964, 0.358583, 0.158541};
    double target_orientation[4] = {-0.707509, -0.706703, 0.0012239, 0.00121894};
    geometry_msgs::Pose target_pose1;
    target_pose1.position.x = target_position[0];
    target_pose1.position.y = target_position[1];
    target_pose1.position.z = target_position[2]; 
    target_pose1.orientation.x = target_orientation[0];
    target_pose1.orientation.y = target_orientation[1];
    target_pose1.orientation.z = target_orientation[2];
    target_pose1.orientation.w = target_orientation[3];
    waypoints.push_back(target_pose1);

    geometry_msgs::Pose target_pose2 = target_pose1;
    target_pose2.position.x -= 0.1;
    target_pose2.position.z += 0.2;
    waypoints.push_back(target_pose2);

    geometry_msgs::Pose target_pose3 = target_pose2;
    target_pose3.position.x -= 0.15;
    target_pose3.position.y += 0.15;
    waypoints.push_back(target_pose3);

    geometry_msgs::Pose target_pose4 = target_pose3;
    target_pose4.position.x -= 0.15;
    target_pose4.position.y += 0.15;
    target_pose4.position.z -= 0.15;
    waypoints.push_back(target_pose4);

	// 笛卡尔空间下的路径规划
	moveit_msgs::RobotTrajectory trajectory;
	const double jump_threshold = 0.0;
	const double eef_step = 0.002;
	double fraction = 0.0;
    int maxtries = 100;   // 最大尝试规划次数
    int attempts = 0;     // 已经尝试规划次数

    while(fraction < 1.0 && attempts < maxtries)
    {
        fraction = arm.computeCartesianPath(
            waypoints, eef_step, jump_threshold, trajectory);
        attempts++;
        
        if(attempts % 10 == 0)
            ROS_INFO("Still trying after %d attempts...", attempts);
    }
    
    if(fraction == 1)
    {   
        ROS_INFO("Path computed successfully. Moving the arm.");

	    // 生成机械臂的运动规划数据
	    moveit::planning_interface::MoveGroupInterface::Plan plan;
	    plan.trajectory_ = trajectory;
	    // 执行运动
	    arm.execute(plan);
        
        ros::Duration(2).sleep();
    }
    else
    {
        ROS_INFO("Path planning failed with only %0.6f success after %d attempts.", 
            fraction, maxtries);
    }

    // 控制机械臂移动到初始化位置
    arm.setNamedTarget("home");
    arm.move();
    ros::Duration(1).sleep();
    
	ros::shutdown(); 
	return 0;
}

