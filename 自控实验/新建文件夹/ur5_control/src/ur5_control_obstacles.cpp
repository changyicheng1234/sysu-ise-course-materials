#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "ur5_control_obstacles");
    ros::AsyncSpinner spinner(1);
    spinner.start();

    moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

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

    // 定义一个障碍物
    moveit_msgs::CollisionObject collision_object;
    collision_object.header.frame_id = arm.getPlanningFrame();
    collision_object.id = "box1";

    // 定义一个长方体
    shape_msgs::SolidPrimitive primitive;
    primitive.type = primitive.BOX;
    primitive.dimensions.resize(3);
    primitive.dimensions[0] = 0.1;
    primitive.dimensions[1] = 0.1;
    primitive.dimensions[2] = 0.1;

    // 定义长方体的位姿
    geometry_msgs::Pose box_pose;
    box_pose.orientation.w = 1.0;
    box_pose.position.x =  0.7;
    box_pose.position.y =  0.25;
    box_pose.position.z =  0.2;

    collision_object.primitives.push_back(primitive);
    collision_object.primitive_poses.push_back(box_pose);
    collision_object.operation = collision_object.ADD;

    std::vector<moveit_msgs::CollisionObject> collision_objects;
    collision_objects.push_back(collision_object);

    // 将障碍物加入到场景中
    ROS_INFO("Add an object into the world");
    planning_scene_interface.addCollisionObjects(collision_objects);
    ros::Duration(2).sleep();

    double target_position[3] = {0.691922, 0.228451, 0.31877};
    double target_orientation[4] = {-0.707503, -0.706708, 0.00130151, 0.00130772};
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

    ros::shutdown(); 
    return 0;
}
