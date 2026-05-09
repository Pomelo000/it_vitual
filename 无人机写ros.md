## mavros常用函数及流程：  
## 流程：



**blodinclude要用到的包名和消息  
根据自己要发的消息写回调**

--------------------------------------------------------------------------------------------------------------

int main()
{



----------------------------------------------------------------------------------------------------------------
```
{注册发布者，订阅者，服务端
-----------------------------------------------------
订阅者
ros::Subscriber state_sub = nh.subscribe<mavros_msgs::State>("mavros/state", 10, state_cb);
<消息类型>(话题名字，缓冲区间隔，所执行的回调)
-----------------------------------------------------
发布者
ros::Publisher local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>("mavros/setpoint_position/local", 10);
<消息类型>(话题名字，缓冲区间隔)
----------------------------------------------------
服务端
ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>("mavros/cmd/arming");
<服务类型>(服务名)
}
```

```
{
该程序节点配置
-----------------------------------------------------
ros::init(argc, argv, "my_awesome_drone_node");注册节点  
ros::NodeHandle nh;节点句柄  
ros::Rate rate(20.0);  
}
```
------------------------------------------------------------------------------------------------------------------



------------------------------------------------------------------------------------------------------------------
准备服务/发送---的数据  
写服务的if
------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------





```while配置：
while(ros::ok){

ros::Time current_time = ros::Time::now();

（make）

ros::spinOnce();
rate.sleep();
}
}```















}
// --- 在 main 函数 while 循环外 ---发布·························································
// 1. 实例化消息对象
geometry_msgs::PoseStamped target_pose;

// 2. 填充静态坐标系信息（MAVROS 通常要求 frame_id）
target_pose.header.frame_id = "base_link"; 

// --- 在 while 循环内 ---
// 3. 更新时间戳（保证数据的时效性，飞控会检查）
target_pose.header.stamp = ros::Time::now();

// 4. 填充具体的数值（比如你从 OpenCV 拿到的坐标）
target_pose.pose.position.x = 1.0; 
target_pose.pose.position.y = 2.0;
target_pose.pose.position.z = 1.5;

// 5. 最终执行发布
local_pos_pub.publish(target_pose);
·····································································································
····································································································订阅
#include <ros/ros.h>
#include <geometry_msgs/Point.h>

// 1. 定义动作 (回调)
void color_cb(const geometry_msgs::Point::ConstPtr& msg) {
    ROS_INFO("Detected: x=%f, y=%f", msg->x, msg->y);
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "subscriber_node");
    ros::NodeHandle nh;

    // 2. 登记订阅 (挂号)
    ros::Subscriber sub = nh.subscribe("red_circle_topic", 10, color_cb);

    // 3. 持续监听 (循环)
    // 如果是纯订阅节点，直接用 spin()
    ros::spin(); 

    return 0;
}·······································································

·····································································服务
服务端流程补充 (Service Client)
服务端是“一问一答”模式。它的流程流是：准备申请单 -> 填写内容 -> 递交并等待回执。

在 main 循环外准备：

C++
// 实例化服务类
mavros_msgs::CommandBool arm_cmd; 
mavros_msgs::SetMode mode_cmd;
在 while 循环内的 if 逻辑中触发：

C++
// 1. 填写申请内容
arm_cmd.request.value = true;      // 想要解锁
mode_cmd.request.custom_mode = "OFFBOARD"; // 想要切模式

// 2. 递交申请 (Call) 并处理回执 (Response)
if (arming_client.call(arm_cmd) && arm_cmd.response.success) {
    ROS_INFO("Vehicle armed!"); // 只有 call 返回 true 且 response 为 success 才算成功
}
