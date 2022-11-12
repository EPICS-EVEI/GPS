INT_MAX = 10000


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

#To determine if the coordinate/function q lies on the segment pr
def onSegment(p:tuple, q:tuple, r:tuple) -> bool:
    
    if((q[0] <= max(p[0], r[0])) &
       (q[0] >= min(p[0], r[0])) &
       (q[1] <= max(p[1], r[1])) &
       (q[1] >= min(p[1], r[1]))):
        return True
    return False

#Finding orientation
def orientation(p:tuple, q:tuple, r:tuple) -> int:
    
    val = (((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))) #calculating slope
    
    if (val > 0):
        return 1 #positive slope is clockwise orientation
    elif (val < 0):
        return 2 #negative slope is counterclockwise orientation
    else:
        return 0 #collinear orientation
    

#Determine if line segment p1q1 and p2q2 intersects
def doIntersect(p1, q1, p2, q2):
    
    #looking for orientation
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    
    #General Case: If the orientations are different, they intersect
    if (o1 != o2) and (o3 != o4):
        return True
    
    #Special Case (collinear): If x and y projection intersects, they intersect
    if (o1 == 0) and (onSegment(p1, p2, q1)): #p1, q1 and p2 are collinear and p2 lies on segment p1q1
        return True
    
    if (o2 == 0) and (onSegment(p1, q2, q1)): #p1, q1 and q2 are collinear and q2 lies on segment p1q1
        return True
    
    if (o3 == 0) and (onSegment(p2, p1, q2)): #p2, q2 and p1 are collinear and p1 lies on segment p2q2
        return True
    
    if (o4 == 0) and (onSegment(p2, q1, q2)): #p2, q2 and q1 are collinear and q1 lies on segment p2q2
        return True
    
    return False


#Determine if the point p lies within the polygon
def is_within_polygon(points:list, p:list) -> bool:
    
    n = len(points)
    if n < 3: #there must be at least 3 points/vertices in a polygon
        return False
    
    extreme = (INT_MAX, p[1]) #Create a point for line segment from p to infinite
    
    decrease = 0 #To calculate number of points where y-coordinate of the polygon is equal to y-coordinate of the point
    count = i = 0
    
    while True:
        next = (i + 1) % n
        
        if(points[i][1] == p[1]):
            decrease += 1
            
        if (doIntersect(points[i], points[next], p, extreme)):
            if orientation(points[i], p, points[next]) == 0:
                return onSegment(points[i], p, points[next])
                           
            count += 1
                           
        i = next
        
        if (i == 0):
            break
        
        count -= decrease
        
    return (count % 2 == 1)

"""
if __name__ == '__main__':
    polygon = [(40.430713, 86.915236),(40.430751, 86.915264),(40.430808, 86.915169),(40.430751, 86.915188)]
    p1 = [40.43120397177199, -86.91496015156082]
    if (is_within_polygon(polygon, p1)):
        print("True")
    else:
        print("False")
"""
