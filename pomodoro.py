#!/usr/bin/env python3
"""
Pomodoro Timer

A simple command-line pomodoro timer with customizable work sessions,
short breaks, and long breaks.

Features:
- 25-minute work sessions by default
- 5-minute short breaks by default
- 15-minute long breaks after 4 work sessions by default
- Command-line notifications when sessions start/end
- Customizable session lengths via command-line arguments
- Simple command-line interface showing the time remaining
"""

import argparse
import time
import os
import sys
import signal

# ANSI color codes for prettier output
COLORS = {
    'RESET': '\033[0m',
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
}

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='A simple Pomodoro timer.')
    parser.add_argument('--work', type=int, default=25,
                        help='Work session duration in minutes (default: 25)')
    parser.add_argument('--short-break', type=int, default=5,
                        help='Short break duration in minutes (default: 5)')
    parser.add_argument('--long-break', type=int, default=15,
                        help='Long break duration in minutes (default: 15)')
    parser.add_argument('--pomodoros', type=int, default=4,
                        help='Number of pomodoros before a long break (default: 4)')
    return parser.parse_args()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def send_notification(title, message):
    """Send a system notification."""
    if sys.platform == 'darwin':  # macOS
        os.system(f"""osascript -e 'display notification "{message}" with title "{title}"'""")
    elif sys.platform.startswith('linux'):  # Linux
        os.system(f"""notify-send "{title}" "{message}" """)
    elif os.name == 'nt':  # Windows
        # This is a simple implementation for Windows notifications
        # For more robust notifications, consider using the win10toast package
        from subprocess import call
        call(['powershell', '-Command', f"""[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms')
              [System.Windows.Forms.MessageBox]::Show('{message}', '{title}')"""])

def format_time(seconds):
    """Format seconds into mm:ss format."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def display_timer(session_type, remaining_seconds, total_seconds):
    """Display the timer with a progress bar."""
    clear_screen()
    if session_type == "Work":
        color = COLORS['RED']
    elif session_type == "Short Break":
        color = COLORS['GREEN']
    else:  # Long Break
        color = COLORS['BLUE']
    
    # Calculate progress bar
    width = 30
    progress = int(width * (total_seconds - remaining_seconds) / total_seconds)
    bar = f"[{'#' * progress}{' ' * (width - progress)}]"
    
    print(f"\n{color}=== POMODORO TIMER ==={COLORS['RESET']}")
    print(f"\n{color}Session: {session_type}{COLORS['RESET']}")
    print(f"\nTime Remaining: {color}{format_time(remaining_seconds)}{COLORS['RESET']}")
    print(f"\n{bar} {int((total_seconds - remaining_seconds) / total_seconds * 100)}%")
    print("\nPress Ctrl+C to exit\n")

def run_timer(duration_minutes, session_type):
    """Run a timer for the specified duration."""
    duration_seconds = duration_minutes * 60
    end_time = time.time() + duration_seconds
    
    # Notify session start
    send_notification("Pomodoro Timer", f"{session_type} session started")
    print(f"\n{COLORS['YELLOW']}Starting {session_type} session ({duration_minutes} minutes){COLORS['RESET']}")
    time.sleep(1)  # Small pause to read the message
    
    try:
        while time.time() < end_time:
            remaining_seconds = int(end_time - time.time())
            display_timer(session_type, remaining_seconds, duration_seconds)
            time.sleep(1)
        
        # Notify session end
        clear_screen()
        print(f"\n{COLORS['YELLOW']}{session_type} session completed!{COLORS['RESET']}")
        send_notification("Pomodoro Timer", f"{session_type} session completed!")
        
        # Add a sound alert
        print('\a')  # Terminal bell
        
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{COLORS['YELLOW']}Timer stopped.{COLORS['RESET']}")
        sys.exit(0)

def handle_interrupt(sig, frame):
    """Handle keyboard interrupt."""
    clear_screen()
    print(f"\n{COLORS['YELLOW']}Timer stopped.{COLORS['RESET']}")
    sys.exit(0)

def main():
    """Main function to run the Pomodoro timer."""
    args = parse_arguments()
    
    # Register signal handler for clean exits
    signal.signal(signal.SIGINT, handle_interrupt)
    
    pomodoro_count = 0
    
    try:
        while True:
            # Work session
            pomodoro_count += 1
            run_timer(args.work, "Work")
            
            # Determine break type
            if pomodoro_count % args.pomodoros == 0:
                # Long break after specified number of pomodoros
                run_timer(args.long_break, "Long Break")
            else:
                # Short break
                run_timer(args.short_break, "Short Break")
                
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{COLORS['YELLOW']}Pomodoro timer stopped.{COLORS['RESET']}")
        sys.exit(0)

if __name__ == "__main__":
    main()

