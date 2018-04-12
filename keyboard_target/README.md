# keyboard_target
Using keyboard to change a target's pose and publish the pose in the meantime.
#Launch
To run: `rosrun keyboard_target keyboard_target.py`

#Usage
```
Reading from the keyboard to gain an offset and add it to the pose's position.
In the meantime publishing the pose in 30fps.
--------------------------------------------
Moving Around:
q/Q top right  w/W upward    e/E top left
a/A left       s/S backward  d/D right
z/Z back left  d/D right     c/C back right
--------------------------------------------
Ctrl+C to Exit
```

