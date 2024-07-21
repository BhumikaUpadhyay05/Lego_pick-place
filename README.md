# The Pick and Place of Lego Pieces using Open Manipulator-X

## Abstract

This project focuses on automating the picking and placing of Lego pieces using the Open Manipulator-X robot. By placing Lego pieces on the robot's platform, it can detect them and calculate thier coordinates and sizes and then perform pick and place

## Repository Contents


### 1) Coordinates File

The coordinates file provides the central coordinates of the detected Lego pieces as well as calculates the length and width of each detected piece. These coordinates are crucial as they are imported in the Lego_pick&place and Random_piece files for accurately picking up and placing the pieces.  

### 2) Lego Pick & Place File

The Lego Pick & Place file is responsible for automating the process of picking up and placing each detected Lego block. It utilizes the coordinate data and passes it to the Open Manipulator-X robot.

### 3) Random Piece File

The Random Piece file is for picking and placing one Lego piece randomly from all the detected blocks. 

---



## Installation

To run this project, ensure you have the following dependencies and hardware set up:

- **Open Manipulator-X Robot** 
- **OpenCV Library:** Install OpenCV, which is used for computer vision tasks such as detecting Lego pieces from a webcam feed.
- **Webcam:** Ensure you have a webcam connected to provide the live video feed necessary for the OpenCV library to detect Lego pieces.
- **Mount:** Use a mount to position the webcam for optimal viewing.

  ## Project Setup

This project setup was done using a mount of approximately 36cm height, using hp 720p 200w webcam
and the visible platform in the webcam feed has dimensions of 18 cm x 25.3 cm. Adjustments and transformations are applied accordingly in the project setup.








