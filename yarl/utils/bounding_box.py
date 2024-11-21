from dataclasses import dataclass
from .vector import Vector2
from copy import deepcopy

def bbox_range(bbox,coord):  return bbox[0][coord],bbox[1][coord]
def bbox_xrange(bbox):  return bbox_range(bbox,0)
def bbox_yrange(bbox):  return bbox_range(bbox,1)

@dataclass
class Bbox:
    x_min : float
    y_min : float
    x_max : float
    y_max : float

    @classmethod
    def make(cls,other):
        if type(other) is list:
            if type(other[0]) is list:
                    #assumig [[left,top], [right,bottom]]
                    xr,yr = bbox_xrange(other), bbox_yrange(other)
                    return Bbox(xr[0],yr[0],xr[1],yr[1])
            else:
                #assumig [x_min,y_min,x_max,y_max]
                return Bbox(*other)
    
    def xrange(self):
        return self.x_min,self.x_max

    def width(self):
        return self.x_max - self.x_min
    
    def yrange(self):
        return self.y_min,self.y_max
    
    def height(self):
        return self.y_max - self.y_min

    def overlap(self, other):
        l,r = self,other if self.x_min < other.x_min else other,self
        if l.x_max > r.x_min: return False
        b,t = self,other if self.y_min < other.y_min else other,self
        if b.y_max > t.x_min: return False
        return True

class RBbox:
    def __init__(self, corners : list[Vector2]):
        self.corners = deepcopy(corners)

    def overlap(self, other):
        return False
