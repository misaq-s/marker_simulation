#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker as mrker
from visualization_msgs.msg import MarkerArray
import random as rand
import threading

pose={"x":[],
      "y":[]}


class Marker(threading.Thread):


    def __init__(self):
        rospy.Subscriber('/slam_out_pose', PoseStamped, self.posecallback)
        self.x=1
        rospy.Subscriber('/joy', Joy,self.joy_callback)

        self.thred = threading.Thread(target=self.run_thread)
        self.thred.deamon = True
        self.thred.start()

        
        self.pub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=100)

        self.source_frame_name = "map"
        self.marker_array = MarkerArray()
        # self.msg = mrker()

        self.x=float(0)
        self.y=float(0)
        


    
        
    def joy_callback(self,msg):
        x=1
        if msg.buttons[5]==1 :
            if len(pose["x"]) == 0 :
                pose["x"].append(self.x)
                pose["y"].append(self.y)
            else:
                for i in range(len(pose["x"])):

                    if (abs(int(pose["x"][i]*10) - int(self.x * 10))<2) and (abs(int(pose["y"][i]*10) - int(self.y * 10))<2):
                        x=0
                        break   
                        

                if x:
                    pose["x"].append(self.x)
                    pose["y"].append(self.y)
            
            # rospy.logwarn(pose)
        
            
    
    def posecallback(self,data):
        self.x=data.pose.position.x
        self.y=data.pose.position.y

    def marker(self):
        r = rospy.Rate(10)
        
        msg = mrker()
        # while not rospy.is_shutdown():
        for i in range(len(pose["x"])):
            msg.id = i
            msg.header.frame_id = self.source_frame_name
            msg.pose.position.x = pose["x"][i]
            msg.pose.position.y = pose["y"][i]
            msg.pose.position.z = 0.1
            msg.ns = "misaq"
            msg.type = 1
            msg.action = 0
            msg.color.r = 0.0
            msg.color.g = 0.1
            msg.color.b = 0.7
            
            msg.scale.x = 0.1
            msg.scale.y = 0.1
            msg.scale.z = 0.1
            msg.color.a = 1.0
            msg.text=''
            msg.mesh_resource=''
            msg.mesh_use_embedded_materials=False
            msg.lifetime.secs = 1
            msg.frame_locked=False
            self.marker_array.markers.append(msg)
        
        
            self.pub.publish(self.marker_array)
            
            r.sleep()

    def run_thread(self):
        rate = rospy.Rate(20)
        while not rospy.is_shutdown():
            try:
                self.marker()
                rate.sleep()
            except KeyboardInterrupt:

                break

       
        
        


   
    


if __name__ == "__main__":
    
    rospy.init_node('robot_marker')

    Marker()

    rospy.spin()