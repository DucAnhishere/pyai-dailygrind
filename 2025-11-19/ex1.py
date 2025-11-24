import numpy as np

def iou(box1: tuple[int, int, int, int], 
        box2: tuple[int, int, int, int]) -> float:
    x1_inter = max(box1[0], box2[0])
    y1_inter = max(box1[1], box2[1])
    x2_inter = min(box1[2], box2[2])        
    y2_inter = min(box1[3], box2[3])
    inter_area = max(0, x2_inter - x1_inter) * max(0, y2_inter - y1_inter)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])        
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])        
    union_area = box1_area + box2_area - inter_area
    return inter_area / union_area if union_area != 0 else 0.0

def nms(boxes: list[tuple[int, int, int, int]], 
        scores: list[float], 
        iou_threshold: float) -> list[int]:
    indices = sorted(range(len(boxes)), key=lambda i: scores[i], reverse=True)
    selected_indices = []
    while indices:
        current = indices.pop(0)
        selected_indices.append(current)
        indices = [i for i in indices if iou(boxes[current], boxes[i]) < iou_threshold]
    return selected_indices

def nms_numpy(boxes: np.ndarray, scores: np.ndarray, iou_thres: float):
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h

        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= iou_thres)[0]
        order = order[inds + 1]

    return keep