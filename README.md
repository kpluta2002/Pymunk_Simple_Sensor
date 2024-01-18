# Pymunk_Simple_Sensor
So basically I was looking for a guide on how to make sensor's for my ML project and i couldn't find anything so i made one.
Feel free to use it on whatever you want and i hope it helps.

### Guide on how to use it is in code but i will also add it here:
## Sensor class gets values as follows: 
- x and y are coordinates relative to the body, which means body's coordinates are (0, 0).
- body is a body you want to connect sensors to.
- collision_type needs to be a int value and they have to be different for each sensor object, also they collide with object of collision_type == 0, you can change that
- radius is basically width of the sensor

## How does it work?
If the sensor is colliding with object of collision_type 0, handle_collision method calculates depth of the penetration and basically cuts the sensor based on 
penetration_depth value.

Once sensor is cut to size the get_reading method should be called which calculates length of the sensor and normalizes it to value between (0.0, 1.0).

After calculating length, it will call update_after_separation method which updates the sensor's length back to original and than the whole process repeats on another frame.

To make it work you need to place get_reading method somewhere in the pygame run method.
