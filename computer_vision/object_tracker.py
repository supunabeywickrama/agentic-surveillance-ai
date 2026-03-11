import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict

class AdvancedTracker:
    def __init__(self, max_disappeared=50, max_distance=50):
        # assign new object IDs using this counter
        self.next_object_id = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()

        # max frames an object can disappear before deregistering
        self.max_disappeared = max_disappeared
        # max distance between centroids to associate them
        self.max_distance = max_distance

    def register(self, centroid, bbox):
        self.objects[self.next_object_id] = {"centroid": centroid, "bbox": bbox}
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rects):
        # rects: array of bounding boxes [x1, y1, x2, y2]
        
        # Base case: if no detections, mark all existing objects as disappeared
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        # Setup current frame centroids
        input_centroids = np.zeros((len(rects), 2), dtype="int")
        input_rects = []
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            input_centroids[i] = (cX, cY)
            input_rects.append((startX, startY, endX, endY))

        # If currently no tracking objects, register all new rects
        if len(self.objects) == 0:
            for i in range(0, len(input_centroids)):
                self.register(input_centroids[i], input_rects[i])
        else:
            object_ids = list(self.objects.keys())
            object_centroids = [obj["centroid"] for obj in self.objects.values()]

            # Compute distance between each pair of object centroids and input centroids
            D = dist.cdist(np.array(object_centroids), input_centroids)

            # Sort row/col indices to match shortest distances first
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue

                # If distance > max_distance, don't associate
                if D[row, col] > self.max_distance:
                    continue

                object_id = object_ids[row]
                self.objects[object_id]["centroid"] = input_centroids[col]
                self.objects[object_id]["bbox"] = input_rects[col]
                self.disappeared[object_id] = 0

                used_rows.add(row)
                used_cols.add(col)

            # Check for disappeared objects
            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)

            # Check for new objects
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)
            for col in unused_cols:
                self.register(input_centroids[col], input_rects[col])

        # Return tracked objects
        return self.objects
