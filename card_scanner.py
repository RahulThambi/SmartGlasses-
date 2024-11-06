import cv2
import easyocr
import re
import json
import os
from datetime import datetime

class SimpleBusinessCardScanner:
    def __init__(self):
        # Initialize EasyOCR reader (first run will download the model)
        print("Initializing OCR model (this may take a moment on first run)...")
        self.reader = easyocr.Reader(['en'])
        
        # Regular expressions for different fields
        self.patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'phone': r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'website': r'(?:www\.)?(?!\.)[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}',
            'name': r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)',
        }
        
        # Create output directory
        self.output_dir = 'scanned_cards'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def preprocess_image(self, image):
        """Basic image preprocessing"""
        # Resize image if too large
        max_dim = 1000
        height, width = image.shape[:2]
        if max(height, width) > max_dim:
            scale = max_dim / max(height, width)
            image = cv2.resize(image, None, fx=scale, fy=scale)
            
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast
        gray = cv2.equalizeHist(gray)
        
        return gray

    def extract_text_and_info(self, image):
        """Extract text and information from image"""
        # Get text from image using EasyOCR
        results = self.reader.readtext(image)
        
        # Combine all text
        full_text = ' '.join([result[1] for result in results])
        
        # Extract information using patterns
        info = {
            'name': None,
            'email': None,
            'phone': None,
            'website': None,
            'raw_text': full_text,
            'all_text_blocks': [result[1] for result in results]
        }
        
        # Find matches for each field
        for field, pattern in self.patterns.items():
            matches = re.findall(pattern, full_text)
            if matches:
                info[field] = matches[0]
        
        # Special handling for name (use first Title Case text block if pattern fails)
        if not info['name']:
            for text_block in info['all_text_blocks']:
                if text_block.istitle() and len(text_block.split()) >= 2:
                    info['name'] = text_block
                    break
        
        return info

    def save_contact(self, info, image):
        """Save contact information and image"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        json_file = os.path.join(self.output_dir, f'contact_{timestamp}.json')
        with open(json_file, 'w') as f:
            json.dump(info, f, indent=4)
            
        # Save image
        img_file = os.path.join(self.output_dir, f'card_{timestamp}.jpg')
        cv2.imwrite(img_file, image)
        
        return json_file, img_file

    def run_camera_scanner(self):
        """Run real-time camera scanner"""
        print("\nInitializing camera...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        cv2.namedWindow("Business Card Scanner")
        scanning = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
                
            display = frame.copy()
            
            # Draw guide box (business card aspect ratio is roughly 1.75:1)
            height, width = frame.shape[:2]
            card_width = int(width * 0.7)
            card_height = int(card_width / 1.75)
            x = (width - card_width) // 2
            y = (height - card_height) // 2
            cv2.rectangle(display, (x, y), (x + card_width, y + card_height), (0, 255, 0), 2)
            
            # Display instructions
            cv2.putText(display, "Position card in green box and press 'S' to scan", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Business Card Scanner", display)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and not scanning:
                scanning = True
                print("\nScanning card...")
                
                # Extract and process card region
                card_roi = frame[y:y+card_height, x:x+card_width]
                processed_image = self.preprocess_image(card_roi)
                
                # Extract information
                info = self.extract_text_and_info(processed_image)
                
                # Save files
                json_file, img_file = self.save_contact(info, card_roi)
                
                # Display results
                print("\nExtracted Information:")
                for key, value in info.items():
                    if key != 'all_text_blocks' and key != 'raw_text':
                        print(f"{key.capitalize()}: {value}")
                
                print("\nFiles saved:")
                print(f"JSON: {json_file}")
                print(f"Image: {img_file}")
                
                print("\nReady for next scan...")
                scanning = False
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Simple Business Card Scanner")
    print("---------------------------")
    print("Controls:")
    print("- Position the business card within the green rectangle")
    print("- Press 'S' to scan")
    print("- Press 'Q' to quit")
    
    scanner = SimpleBusinessCardScanner()
    scanner.run_camera_scanner()