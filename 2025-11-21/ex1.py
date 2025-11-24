import numpy as np

def clip_boxes(boxes: np.ndarray, img_shape: tuple[int, int]) -> np.ndarray:
    """Clip boxes to image boundaries.

    Args:
        boxes (np.ndarray): Array of shape (N, 4) containing bounding boxes in
            (x1, y1, x2, y2) format.
        img_shape (tuple[int, int]): Tuple containing image height and width.

    Returns:
        np.ndarray: Array of shape (N, 4) containing clipped bounding boxes.
    """
    h, w = img_shape
    boxes[:, 0] = np.clip(boxes[:, 0], 0, w - 1)  # x1
    boxes[:, 1] = np.clip(boxes[:, 1], 0, h - 1)  # y1
    boxes[:, 2] = np.clip(boxes[:, 2], 0, w - 1)  # x2
    boxes[:, 3] = np.clip(boxes[:, 3], 0, h - 1)  # y2
    return boxes

if __name__ == "__main__":
    boxes = np.array([[50, 50, 150, 150],
                      [-10, -10, 200, 200],
                      [30, 40, 300, 400]])
    img_shape = (200, 200)
    clipped_boxes = clip_boxes(boxes, img_shape)
    print("Clipped Boxes:\n", clipped_boxes)