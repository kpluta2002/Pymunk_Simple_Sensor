import pymunk
from pymunk.vec2d import Vec2d

space = pymunk.Space()


# Sensor class gets values as follows: 
# x and y are coordinates relative to the body, which means body's coordinates are (0, 0)
# body is a body you want to connect sensors to
# collision_type needs to be a int value and they have to be different for each sensor object, also they collide with object of collision_type == 0, you can change that
# radius is basically width of the sensor

# How does it work?
# If the sensor is colliding with object of collision_type 0, handle_collision method calculates depth of the penetration and basically cuts the sensor based on 
# penetration_depth value.
# Once sensor is cut to size the get_reading method should be called which calculates length of the sensor and normalizes it to value between (0.0, 1.0)
# After calculating length, it will call update_after_separation method which updates the sensor's length back to original and than the whole process repeats on another frame.
# To make it work you need to place get_reading method somewhere in the pygame run method.

class Sensor:
    def __init__(self, x, y, body, collision_type, radius=1):
        self.torso = body
        self.start_point = self.torso.position
        self.end_point_first = Vec2d(x, y)
        self.end_point = Vec2d(x, y)
        self.radius = radius

        self.segment = pymunk.Segment(self.torso, (0, 0), self.end_point, self.radius)
        self.segment.sensor = True
        self.max_distance = abs(self.end_point)
        self.collision_type = collision_type
        self.segment.collision_type = self.collision_type

        space.add(self.segment)

        self.handler = space.add_collision_handler(0, self.segment.collision_type)
        self.handler.pre_solve = self.handle_collision

    def update_segment(self):
        if hasattr(self, 'segment'):
            space.remove(self.segment)

        self.segment = pymunk.Segment(self.torso, (0, 0), self.end_point, self.radius)
        self.segment.sensor = True
        self.segment.collision_type = self.collision_type

    def update_after_separation(self):
            self.end_point = self.end_point_first
            self.update_segment()
            space.add(self.segment)
        
    def coordinate_calculation(self, move_distance):
        if self.end_point.x == 0:
    # Update y coordinate if x coordinate is 0
            if self.end_point.y > 0:
                    self.end_point = Vec2d(self.end_point.x, self.end_point.y + move_distance)
            else:
                    self.end_point = Vec2d(self.end_point.x, self.end_point.y - move_distance)
        elif self.end_point.y == 0:
            # Update x coordinate if y coordinate is 0
            if self.end_point.x > 0:
                # Update y coordinate based on the sign of y
                    self.end_point = Vec2d(self.end_point.x + move_distance, self.end_point.y)
            else:
                # Update y coordinate based on the sign of y
                    self.end_point = Vec2d(self.end_point.x - move_distance, self.end_point.y)
           
        else:
            # Update both x and y coordinates based on the sign of coordinates
            if self.end_point.x > 0:
                # Update y coordinate based on the sign of y
                if self.end_point.y > 0:
                    self.end_point = Vec2d(self.end_point.x + move_distance, self.end_point.y + move_distance)
                else:
                    self.end_point = Vec2d(self.end_point.x + move_distance, self.end_point.y - move_distance)
            elif self.end_point.x < 0:
                # Update y coordinate based on the sign of y
                if self.end_point.y > 0:
                    self.end_point = Vec2d(self.end_point.x - move_distance, self.end_point.y + move_distance)
                else:
                    self.end_point = Vec2d(self.end_point.x - move_distance, self.end_point.y - move_distance)
    
    def handle_collision(self, arbiter, space, data):
        contacts = arbiter.contact_point_set
        penetration_depth = contacts.points[0].distance

        # Update the endpoint position based on the collision depth
        move_distance = min(penetration_depth, 0.1)
        self.coordinate_calculation(move_distance)        

        # Update the segment with the new endpoint position
        self.update_segment()
        space.add(self.segment)

        return True


    def get_reading(self):
        distance = abs(self.end_point)
        normalized_distance = clamp(distance / self.max_distance, 0.0, 1.0)

        # Updating end_point after reading distance
        self.update_after_separation()
        return normalized_distance

# Clamping value between minimum and maximum
def clamp(value, minimum, maximum):
        return max(minimum, min(value, maximum))