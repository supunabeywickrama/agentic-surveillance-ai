import time

class EventDetector:
    def __init__(self, loiter_threshold=120, restricted_zones=None, crowd_threshold=5):
        self.loiter_threshold = loiter_threshold  # seconds
        self.restricted_zones = restricted_zones or [] # list of polygons [(x1,y1), (x2,y2)...]
        self.crowd_threshold = crowd_threshold
        
        # Track when a person was first active in the frame
        self.person_first_seen = {}
        # Track active abandoned objects
        self.abandoned_objects = {}

    def is_point_in_polygon(self, point, polygon):
        # Ray casting algorithm
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def detect_events(self, tracked_objects, current_time=None):
        if current_time is None:
            current_time = time.time()
            
        events = []
        active_ids = []

        # 1. Crowd Detection
        people_count = len(tracked_objects)
        if people_count > self.crowd_threshold:
            events.append({
                "event": "crowd_detected",
                "people_count": people_count,
                "timestamp": current_time
            })

        for object_id, data in tracked_objects.items():
            active_ids.append(object_id)
            centroid = data["centroid"]

            # 2. Loitering Detection
            if object_id not in self.person_first_seen:
                self.person_first_seen[object_id] = current_time
            
            time_spent = current_time - self.person_first_seen[object_id]
            if time_spent > self.loiter_threshold:
                events.append({
                    "event": "loitering",
                    "person_id": object_id,
                    "time_spent": time_spent,
                    "timestamp": current_time
                })

            # 3. Restricted Area Entry
            for zone_id, polygon in enumerate(self.restricted_zones):
                if self.is_point_in_polygon(centroid, polygon):
                    events.append({
                        "event": "restricted_area_entry",
                        "person_id": object_id,
                        "zone_id": zone_id,
                        "timestamp": current_time
                    })

        # Cleanup lost tracks from tracking dictionaries
        lost_ids = set(self.person_first_seen.keys()) - set(active_ids)
        for obj_id in lost_ids:
            del self.person_first_seen[obj_id]

        return events
