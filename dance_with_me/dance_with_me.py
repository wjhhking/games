import tkinter as tk
from tkinter import ttk, messagebox
from pytubefix import YouTube
import cv2
import tempfile
import os
from PIL import Image, ImageTk
import threading
import time
from playsound import playsound
import multiprocessing
import mediapipe as mp

class YouTubePlayer:
    def __init__(self, root):
        # Window Setup Module
        self.root = root
        self.root.title("Dance With Me")
        
        # MediaPipe Module with optimized settings
        self.mp_pose = mp.solutions.pose
        self.youtube_pose = self.mp_pose.Pose(
            model_complexity=0,  # Use simplest model (0, 1, or 2)
            min_detection_confidence=0.3,  # Lower threshold
            min_tracking_confidence=0.3,   # Lower threshold
            enable_segmentation=False,     # Disable unnecessary features
            smooth_landmarks=True)         # Enable smoothing for better tracking
        self.webcam_pose = self.mp_pose.Pose(
            model_complexity=0,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3,
            enable_segmentation=False,
            smooth_landmarks=True)
        self.mp_draw = mp.solutions.drawing_utils
        
        # Main Layout Module
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        """
        Layout of the application:
        +--------------------------------+-----------------+
        |                                |                 |
        |                                | Target Pose     |
        |     Original Video             | (320x180)       |
        |     (640x360)                  |                 |
        |                                +-----------------+
        |                                |                 |
        |                                | User Pose       |
        |                                | (320x180)       |
        |                                |                 |
        +--------------------------------+-----------------+
        |      Video Controls            |   Performance   |
        | [     YouTube URL     ]        |     Scores      |
        | [Play]          [Stop]         |  Current: 0%    |
        |                                |  Session: 0%    |
        +--------------------------------+-----------------+
        """
        
        # Create video frames container with labels
        self.videos_frame = ttk.Frame(self.main_frame)
        self.videos_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Original Video Module
        self.video_container = ttk.Frame(self.videos_frame)
        self.video_container.grid(row=0, column=0, rowspan=2, padx=5)
        self.video_label_text = ttk.Label(self.video_container, text="Original Video", font=('Arial', 12, 'bold'))
        self.video_label_text.grid(row=0, column=0, pady=(0, 5))
        self.video_frame = ttk.Frame(self.video_container, width=640, height=360)
        self.video_frame.grid(row=1, column=0)
        self.video_frame.grid_propagate(False)
        
        # Target Pose Module
        self.pose_container = ttk.Frame(self.videos_frame)
        self.pose_container.grid(row=0, column=1, padx=5)
        self.pose_label_text = ttk.Label(self.pose_container, text="Target Pose", font=('Arial', 12, 'bold'))
        self.pose_label_text.grid(row=0, column=0, pady=(0, 5))
        self.pose_frame = ttk.Frame(self.pose_container, width=320, height=180)  # Half size
        self.pose_frame.grid(row=1, column=0)
        self.pose_frame.grid_propagate(False)
        
        # User Pose Module
        self.webcam_container = ttk.Frame(self.videos_frame)
        self.webcam_container.grid(row=1, column=1, padx=5)
        self.webcam_label_text = ttk.Label(self.webcam_container, text="User Pose", font=('Arial', 12, 'bold'))
        self.webcam_label_text.grid(row=0, column=0, pady=(0, 5))
        self.webcam_frame = ttk.Frame(self.webcam_container, width=320, height=180)  # Half size
        self.webcam_frame.grid(row=1, column=0)
        self.webcam_frame.grid_propagate(False)
        
        # Video Display Module
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.grid(row=0, column=0, sticky='nsew')
        
        self.pose_label = ttk.Label(self.pose_frame)
        self.pose_label.grid(row=0, column=0, sticky='nsew')
        
        self.webcam_label = ttk.Label(self.webcam_frame)
        self.webcam_label.grid(row=0, column=0, sticky='nsew')
        
        # Create style for centered LabelFrame title
        self.style = ttk.Style()
        self.style.configure('Centered.TLabelframe')
        self.style.configure('Centered.TLabelframe.Label', anchor='center', justify='center')
        
        # Controls Module (YouTube URL + Play/Stop) with border and centered title
        controls_container = ttk.Frame(self.main_frame)
        controls_container.grid(row=1, column=0, pady=10, padx=5)
        
        controls_title = ttk.Label(controls_container, text="Video Controls", font=('Arial', 12, 'bold'))
        controls_title.grid(row=0, column=0, pady=(0, 5))
        
        self.controls_frame = ttk.Frame(controls_container, width=640, height=150)
        self.controls_frame.grid(row=1, column=0)
        self.controls_frame.grid_propagate(False)
        
        # Center container for controls
        center_container = ttk.Frame(self.controls_frame)
        center_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # YouTube Link Input
        self.link_label = ttk.Label(center_container, text="Enter youtube link:")
        self.link_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.link_entry = ttk.Entry(center_container, width=50)
        self.link_entry.grid(row=1, column=0, sticky='ew', pady=5)
        self.link_entry.insert(0, "https://www.youtube.com/watch?v=pzj78YA1zws")
        
        # Play/Stop Controls - Center the buttons
        button_frame = ttk.Frame(center_container)
        button_frame.grid(row=2, column=0, pady=5)
        
        self.play_button = ttk.Button(button_frame, text="Play", command=self.play_video, width=15)
        self.play_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_video, width=15)
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Configure grid weights for controls frame
        self.controls_frame.columnconfigure(0, weight=1)
        
        # Score Display Module with border and centered title
        score_outer_container = ttk.Frame(self.main_frame)
        score_outer_container.grid(row=1, column=1, pady=10)
        
        score_title = ttk.Label(score_outer_container, text="Scores", font=('Arial', 12, 'bold'))
        score_title.grid(row=0, column=0, pady=(0, 5))
        
        self.score_frame = ttk.Frame(score_outer_container, width=320, height=150)
        self.score_frame.grid(row=1, column=0)
        self.score_frame.grid_propagate(False)
        
        # Center container for scores
        score_container = ttk.Frame(self.score_frame)
        score_container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.current_score_label = ttk.Label(score_container, text="Current:", font=('Arial', 20, 'bold'))
        self.current_score_label.grid(row=0, column=0, pady=5)
        self.current_score_value = ttk.Label(score_container, text="0%", font=('Arial', 30, 'bold'))
        self.current_score_value.grid(row=0, column=1, padx=10)
        
        self.session_score_label = ttk.Label(score_container, text="Session:", font=('Arial', 20, 'bold'))
        self.session_score_label.grid(row=1, column=0, pady=5)
        self.session_score_value = ttk.Label(score_container, text="0%", font=('Arial', 30, 'bold'))
        self.session_score_value.grid(row=1, column=1, padx=10)
        
        # Add warning message label under scores
        self.warning_label = ttk.Label(score_container, text="", 
                                     font=('Arial', 12), 
                                     foreground='red',
                                     wraplength=280)  # Allow text to wrap
        self.warning_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Configure grid weights for score frame
        self.score_frame.columnconfigure(1, weight=1)

        # Update main frame grid configuration
        self.main_frame.columnconfigure(0, weight=3)  # Controls frame takes more space
        self.main_frame.columnconfigure(1, weight=1)  # Score frame takes less space
        
        # State Variables Module
        self.webcam = None
        self.is_webcam_active = True
        self.webcam_thread = None
        
        self.temp_file = None
        self.is_playing = False
        self.video_thread = None
        self.audio_process = None
        
        # Score Variables
        self.scores = []
        self.current_score = 0
        self.session_score = 0
        
        # Add variable to store YouTube pose results
        self.youtube_pose_results = None
        
        # Add queue for pose processing
        self.pose_queue = []
        self.pose_processing = False
        
        # Initialization Module
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.start_webcam()
    
    def start_webcam(self):
        """Start webcam in a separate thread"""
        self.webcam_thread = threading.Thread(target=self.process_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

    def process_pose(self, frame, pose_detector):
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the image and detect poses using the specified detector
        results = pose_detector.process(rgb_frame)
        return results

    def draw_pose_on_frame(self, frame, pose_results):
        # Draw pose landmarks on a copy of the frame
        annotated_image = frame.copy()
        if pose_results and pose_results.pose_landmarks:
            self.mp_draw.draw_landmarks(
                annotated_image, 
                pose_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),  # Green landmarks
                self.mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2))  # White connections
        return annotated_image

    def play_audio_thread(self):
        try:
            playsound(self.temp_file)
        except:
            pass
    
    def play_video_thread(self):
        try:
            self.audio_process = multiprocessing.Process(target=playsound, args=(self.temp_file,))
            self.audio_process.start()
            
            cap = cv2.VideoCapture(self.temp_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_time = 1/fps  # Time per frame
            print(f"Video FPS: {fps}")
            
            # For FPS calculation
            frame_count = 0
            start_time = time.time()
            next_frame_time = start_time  # Track when next frame should be shown
            pose_interval = 3  # Process every 3rd frame
            
            # For timing statistics
            stats_interval = int(fps)  # Use video's FPS for stats interval
            resize_times = []
            pose_times = []
            draw_times = []
            display_times = []
            
            # Frame buffer
            buffer_size = 200  # Increased buffer (~8 seconds at 25fps)
            frame_buffer = []
            underrun_count = 0
            
            print("Pre-filling buffer...")
            # Pre-fill buffer with processed frames
            for i in range(buffer_size):
                ret, frame = cap.read()
                if ret:
                    t0 = time.time()
                    frame_small = cv2.resize(frame, (320, 180))
                    t1 = time.time()
                    resize_times.append(t1 - t0)
                    
                    # Process pose only every 3rd frame
                    if i % pose_interval == 0:
                        t0 = time.time()
                        self.youtube_pose_results = self.process_pose(frame_small, self.youtube_pose)
                        t1 = time.time()
                        pose_times.append(t1 - t0)
                        
                        t0 = time.time()
                        pose_frame = self.draw_pose_on_frame(frame_small, self.youtube_pose_results)
                        t1 = time.time()
                        draw_times.append(t1 - t0)
                    else:
                        pose_frame = self.draw_pose_on_frame(frame_small, self.youtube_pose_results)
                    
                    pose_rgb = cv2.cvtColor(pose_frame, cv2.COLOR_BGR2RGB)
                    frame_buffer.append(pose_rgb)
            
            print(f"Buffer pre-filled with {len(frame_buffer)} frames")
            
            buffer_index = 0
            while self.is_playing and cap.isOpened():
                current_time = time.time()
                
                if current_time >= next_frame_time:
                    if frame_buffer:
                        # Get current frame from buffer
                        pose_rgb = frame_buffer[buffer_index]
                        
                        # Read and process next frame for buffer
                        ret, frame = cap.read()
                        if ret:
                            t0 = time.time()
                            frame_small = cv2.resize(frame, (320, 180))
                            t1 = time.time()
                            resize_times.append(t1 - t0)
                            
                            # Process pose only every 3rd frame
                            if frame_count % pose_interval == 0:
                                t0 = time.time()
                                self.youtube_pose_results = self.process_pose(frame_small, self.youtube_pose)
                                t1 = time.time()
                                pose_times.append(t1 - t0)
                                
                                t0 = time.time()
                                pose_frame = self.draw_pose_on_frame(frame_small, self.youtube_pose_results)
                                t1 = time.time()
                                draw_times.append(t1 - t0)
                            else:
                                pose_frame = self.draw_pose_on_frame(frame_small, self.youtube_pose_results)
                            
                            new_pose_rgb = cv2.cvtColor(pose_frame, cv2.COLOR_BGR2RGB)
                            frame_buffer[buffer_index] = new_pose_rgb
                        
                        # Display current frame
                        t0 = time.time()
                        target_image = Image.fromarray(pose_rgb)
                        target_photo = ImageTk.PhotoImage(image=target_image)
                        self.pose_label.configure(image=target_photo)
                        self.pose_label.image = target_photo
                        t1 = time.time()
                        display_times.append(t1 - t0)
                        
                        buffer_index = (buffer_index + 1) % buffer_size
                        frame_count += 1
                        
                        if frame_count % stats_interval == 0:
                            current_fps = frame_count / (time.time() - start_time)
                            print(f"Current FPS: {current_fps:.2f}")
                            print(f"Average times (ms):")
                            print(f"  Resize: {1000*sum(resize_times[-stats_interval:])/stats_interval:.1f}")
                            if pose_times:
                                print(f"  Pose: {1000*sum(pose_times[-stats_interval:])/len(pose_times[-stats_interval:]):.1f}")
                            if draw_times:
                                print(f"  Draw: {1000*sum(draw_times[-stats_interval:])/len(draw_times[-stats_interval:]):.1f}")
                            print(f"  Display: {1000*sum(display_times[-stats_interval:])/stats_interval:.1f}")
                        
                        # Update next frame time with drift correction
                        ideal_time = start_time + (frame_count + 1) * frame_time
                        drift = current_time - ideal_time
                        if abs(drift) > frame_time:
                            next_frame_time = current_time + frame_time
                            start_time = current_time - frame_count * frame_time
                        else:
                            next_frame_time = ideal_time
                        
                        self.root.update()
                    else:
                        underrun_count += 1
                        time.sleep(0.001)
                else:
                    sleep_time = min(0.0005, (next_frame_time - current_time) / 2)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
            
        except Exception as e:
            if self.is_playing:  # Only show error if not stopped intentionally
                messagebox.showerror("Error", f"Error playing media: {str(e)}")

    def play_video(self):
        try:
            url = self.link_entry.get()
            if not url:
                messagebox.showwarning("Warning", "Please enter a YouTube URL")
                return

            # Initialize YouTube object with OAuth
            yt = YouTube(
                url,
                use_oauth=True,
                allow_oauth_cache=True
            )

            # Get available streams and select the best one
            streams = yt.streams.filter(progressive=True, file_extension='mp4')
            if not streams:
                messagebox.showerror("Error", "No suitable video stream found")
                return

            stream = streams.get_highest_resolution()

            # Download to a temporary file
            temp_dir = tempfile.gettempdir()
            self.temp_file = os.path.join(temp_dir, "temp_video.mp4")

            # Show download progress
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Downloading...")
            progress_label = ttk.Label(progress_window, text="Downloading video... Please wait.")
            progress_label.pack(padx=20, pady=10)
            progress_window.update()

            try:
                stream.download(output_path=temp_dir, filename="temp_video.mp4")
            finally:
                progress_window.destroy()

            # Stop any currently playing video
            self.stop_video()
            
            # Start video playback in a separate thread
            self.is_playing = True
            self.video_thread = threading.Thread(target=self.play_video_thread)
            self.video_thread.daemon = True
            self.video_thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Error playing video: {str(e)}")

    def stop_video(self):
        self.is_playing = False
        if hasattr(self, 'audio_process') and self.audio_process:
            self.audio_process.terminate()
            self.audio_process.join(timeout=1.0)
        self.video_label.configure(image='')
        # Reset scores for new session
        self.scores = []
        self.current_score = 0
        self.session_score = 0
        self.current_score_value.config(text="0%")
        self.session_score_value.config(text="0%")

    def process_webcam(self):
        self.webcam = cv2.VideoCapture(0)
        
        while self.is_webcam_active:
            ret, frame = self.webcam.read()
            if ret:
                # Process pose detection for webcam
                webcam_pose_results = self.process_pose(frame, self.webcam_pose)
                pose_frame = self.draw_pose_on_frame(frame, webcam_pose_results)
                
                # Update scores if video is playing
                if self.is_playing and hasattr(self, 'youtube_pose_results'):
                    self.update_scores(self.youtube_pose_results, webcam_pose_results)
                
                # Convert BGR to RGB for display
                frame_rgb = cv2.cvtColor(pose_frame, cv2.COLOR_BGR2RGB)
                
                # Resize frame
                frame_resized = cv2.resize(frame_rgb, (320, 180))
                
                # Convert to PhotoImage
                image = Image.fromarray(frame_resized)
                photo = ImageTk.PhotoImage(image=image)
                
                # Update webcam label
                self.webcam_label.configure(image=photo)
                self.webcam_label.image = photo
                        
        if self.webcam:
            self.webcam.release()

    def on_closing(self):
        """Clean up resources before closing the window"""
        self.stop_video()
        self.is_webcam_active = False  # Stop webcam thread
        if self.webcam:
            self.webcam.release()
        self.youtube_pose.close()  # Close YouTube pose detector
        self.webcam_pose.close()   # Close webcam pose detector
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except:
                pass
        self.root.destroy()

    def calculate_pose_similarity(self, pose1, pose2):
        """Calculate similarity between two poses focusing on limb positions"""
        if not pose1 or not pose2 or not pose1.pose_landmarks or not pose2.pose_landmarks:
            return 0
        
        # Get landmarks from both poses
        lm1 = pose1.pose_landmarks.landmark
        lm2 = pose2.pose_landmarks.landmark
        
        # Define key points for different body parts with weights
        key_points = {
            # Arms (30%)
            'right_arm': {'points': [12, 14, 16], 'weight': 15},  # right shoulder, elbow, wrist
            'left_arm': {'points': [11, 13, 15], 'weight': 15},   # left shoulder, elbow, wrist
            # Legs (60%)
            'right_leg': {'points': [24, 26, 28], 'weight': 30},  # right hip, knee, ankle
            'left_leg': {'points': [23, 25, 27], 'weight': 30},   # left hip, knee, ankle
            # Head/Shoulders (10%)
            'head_shoulders': {'points': [0, 11, 12], 'weight': 10}  # nose and shoulders
        }
        
        # Check visibility for each body part
        visibility_checks = {
            'legs': {'points': [23, 24, 25, 26, 27, 28], 'threshold': 0.5},
            'arms': {'points': [11, 12, 13, 14, 15, 16], 'threshold': 0.5},
            'head': {'points': [0, 11, 12], 'threshold': 0.5}
        }
        
        visibility_status = {}
        warning_messages = []
        
        # Check visibility for each body part
        for part, check in visibility_checks.items():
            visible = True
            for point in check['points']:
                if (lm2[point].visibility < check['threshold'] or
                    lm2[point].y > 0.95 or
                    lm2[point].y < 0.05):
                    visible = False
                    break
            visibility_status[part] = visible
            if not visible:
                warning_messages.append(f"Cannot see {part}")
        
        # Update warning label
        if warning_messages:
            self.warning_label.config(text="Please adjust camera: " + ", ".join(warning_messages))
        else:
            self.warning_label.config(text="")
        
        total_score = 0
        
        # Calculate scores for each body part
        for part_name, part_info in key_points.items():
            points = part_info['points']
            weight = part_info['weight']
            
            # Check if this part should be scored
            if ('leg' in part_name and not visibility_status['legs']):
                continue  # Skip legs if not visible, score will remain 0 for this part
            elif ('arm' in part_name and not visibility_status['arms']):
                continue  # Skip arms if not visible
            elif ('head' in part_name and not visibility_status['head']):
                continue  # Skip head if not visible
            
            # Calculate angles and score for visible parts
            angle1 = self.calculate_angle(lm1[points[0]], lm1[points[1]], lm1[points[2]])
            angle2 = self.calculate_angle(lm2[points[0]], lm2[points[1]], lm2[points[2]])
            
            # Compare angles and calculate weighted score
            angle_diff = abs(angle1 - angle2)
            part_score = max(0, 100 - (angle_diff / 1.8))  # More lenient scoring
            weighted_score = (part_score * weight) / 100
            
            total_score += weighted_score
        
        return min(100, total_score)  # Cap at 100%

    def calculate_angle(self, p1, p2, p3):
        """Calculate angle between three points"""
        import math
        
        # Get vectors
        v1 = [p1.x - p2.x, p1.y - p2.y]
        v2 = [p3.x - p2.x, p3.y - p2.y]
        
        # Calculate angle in degrees
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        v1_norm = math.sqrt(v1[0]**2 + v1[1]**2)
        v2_norm = math.sqrt(v2[0]**2 + v2[1]**2)
        
        cos_angle = dot_product / (v1_norm * v2_norm)
        cos_angle = min(1.0, max(-1.0, cos_angle))  # Handle numerical errors
        angle_rad = math.acos(cos_angle)
        
        return math.degrees(angle_rad)

    def update_scores(self, youtube_pose, webcam_pose):
        """Update current and session scores"""
        self.current_score = self.calculate_pose_similarity(youtube_pose, webcam_pose)
        self.scores.append(self.current_score)
        self.session_score = sum(self.scores) / len(self.scores)
        
        # Update score display with colors
        self.current_score_value.config(
            text=f"{self.current_score:.1f}%",
            foreground='green' if self.current_score >= self.session_score else 'red'
        )
        self.session_score_value.config(
            text=f"{self.session_score:.1f}%",
            foreground='black'  # Session score stays black
        )

def main():
    multiprocessing.freeze_support()
    root = tk.Tk()
    app = YouTubePlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 