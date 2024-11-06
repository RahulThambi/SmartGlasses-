import cv2
import numpy as np
from scipy.spatial import distance as dist
import argparse

class VirtualMeasuringTape:
    def __init__(self):
        # Known width of the reference object in inches (default: credit card width)
        self.REFERENCE_WIDTH = 3.375  # inches
        self.points = []
        self.px_per_inch = None
        self.reference_set = False
        
    def calculate_distance(self, p1, p2):
        """Calculate distance between two points in inches"""
        if self.px_per_inch is None:
            return None
        return dist.euclidean(p1, p2) / self.px_per_inch

    def set_reference(self, p1, p2):
        """Set reference scale using known object width"""
        pixel_distance = dist.euclidean(p1, p2)
        self.px_per_inch = pixel_distance / self.REFERENCE_WIDTH
        self.reference_set = True
        return True

    def draw_measurement(self, frame, p1, p2):
        """Draw measurement line and distance"""
        cv2.line(frame, p1, p2, (0, 255, 0), 2)
        
        if self.px_per_inch is not None:
            distance = self.calculate_distance(p1, p2)
            mid_point = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
            cv2.putText(frame, f"{distance:.1f} inches", 
                       mid_point, cv2.FONT_HERSHEY_SIMPLEX, 
                       0.65, (0, 0, 255), 2)

    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events for point selection"""
        frame = param
        if event == cv2.EVENT_LBUTTONUP:
            self.points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    def run(self):
        """Main execution loop"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        cv2.namedWindow("Virtual Measuring Tape")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            # Create copy of frame for drawing
            display = frame.copy()
            
            # Set mouse callback
            cv2.setMouseCallback("Virtual Measuring Tape", 
                               self.mouse_callback, 
                               display)

            # Draw existing points and measurements
            for point in self.points:
                cv2.circle(display, point, 5, (0, 0, 255), -1)

            # Handle reference calibration
            if len(self.points) == 2 and not self.reference_set:
                self.set_reference(self.points[0], self.points[1])
                self.draw_measurement(display, self.points[0], self.points[1])
                self.points = []
                print("Reference set! Now measure objects...")

            # Handle measurements
            elif len(self.points) == 2 and self.reference_set:
                self.draw_measurement(display, self.points[0], self.points[1])
                self.points = []

            # Display instructions
            if not self.reference_set:
                cv2.putText(display, "Click two points on reference object (credit card width)", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)
            else:
                cv2.putText(display, "Click two points to measure distance", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)

            # Show frame
            cv2.imshow("Virtual Measuring Tape", display)

            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    measuring_tape = VirtualMeasuringTape()
    measuring_tape.run()