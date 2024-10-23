import c3d
import csv
from flask import Flask, request, send_file
import os

app = Flask(__name__)

# Function to convert C3D to CSV
def convert_c3d_to_csv(c3d_file_path, csv_file_path):
    with open(c3d_file_path, 'rb') as handle:
        reader = c3d.Reader(handle)
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            # Write header with the point labels
            writer.writerow(['Frame', 'X', 'Y', 'Z'])
            
            # Read frames and write points data to CSV
            for i, frame_data in enumerate(reader.read_frames()):
                points = frame_data[0]  # First value contains points
                print(f"Frame {i}: Points data - {points}")  # Debug: Inspect points
                
                # Check if points is iterable (array or list) before processing
                if hasattr(points, '__iter__'):
                    for point in points:
                        # Flatten points and round values for simplicity
                        writer.writerow([i] + list(point[:3].round(2)))
                else:
                    print(f"Warning: Points for frame {i} is not iterable. Skipping.")
                    continue

# Route to upload C3D file and return CSV download
@app.route('/upload', methods=['POST'])
def upload_c3d():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file:
        # Save the uploaded C3D file temporarily
        c3d_file_path = os.path.join('uploads', file.filename)
        file.save(c3d_file_path)

        # Convert to CSV
        csv_file_path = os.path.splitext(c3d_file_path)[0] + '.csv'
        convert_c3d_to_csv(c3d_file_path, csv_file_path)

        # Return the CSV file as a download
        return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
