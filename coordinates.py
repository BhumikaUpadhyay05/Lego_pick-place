import cv2
import numpy as np
import time  # Import time module for timestamp

xy = []

def calculate_pixel_to_cm_ratio(height):
    ratio = (height * 0.00085)  # Example ratio
    return ratio

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_lower = np.array([0])
    gray_upper = np.array([80])
    mask = cv2.inRange(gray, gray_lower, gray_upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    return result

def detect_blocks(image, pixel_to_cm_ratio):
    edges = cv2.Canny(image, 50, 100)
    kernel1 = np.ones((40, 40), np.uint8)
    kernel2 = np.ones((30, 30), np.uint8)
    edges = cv2.dilate(edges, kernel1, iterations=1)
    edges = cv2.erode(edges, kernel2, iterations=1)
    edges = cv2.Canny(edges, 50, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blocks = []
    min_area = 1000
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= min_area:
            epsilon = 0.1 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) == 4:  # Check if it is a rectangle
                x, y, w, h = cv2.boundingRect(approx)
                width = w * pixel_to_cm_ratio
                length = h * pixel_to_cm_ratio
                blocks.append(((x, y, w, h), width, length))
    
    return blocks

def transform_coordinates(midpoint):
    x_new = midpoint[1] * 0.00039 + 0.048
    y_new = (midpoint[0] - 335) * 0.00039
    new_tuple=(x_new,y_new)
    xy.append(new_tuple)
    
    return x_new, y_new

def main(height):
    pixel_to_cm_ratio = calculate_pixel_to_cm_ratio(height)
    
    # Generate timestamp-based filename for image capture
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_path = f"image_{timestamp}.jpg"
    
    # Initialize the camera
    cap = cv2.VideoCapture(2)  # 0 is the default camera on most systems

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        return

    # Release the camera
    cap.release()

    # Save the captured image in the same directory as the script
    cv2.imwrite(image_path, frame)
    print(f"Image saved as {image_path}")

    # Process the captured image
    frame = cv2.imread(image_path)
    
    if frame is None:
        print(f"Error: Failed to read image from {image_path}.")
        return
    
    preprocessed_image = preprocess_image(frame)
    blocks = detect_blocks(preprocessed_image, pixel_to_cm_ratio)
    
    for block in blocks:
        ((x, y, w, h), width, length) = block
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        midpoint = (x + w // 2, y + h // 2)
        coordinates = transform_coordinates(midpoint)
        cv2.putText(frame, f"W: {width:.2f}cm, L: {length:.2f}cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"X: {coordinates[0]:.2f}, Y: {coordinates[1]:.2f}", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow('Frame', frame)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

# Example usage
height = 36  # Example height from plane to camera in cm
main(height)
print(xy)
