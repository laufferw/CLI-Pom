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
- Sound effects for session start/end and transitions
- Customizable session lengths via command-line arguments
- Simple command-line interface showing the time remaining
- Sound effects can be muted with --mute option
"""

import argparse
import time
import os
import sys
import signal
import datetime
import subprocess
import shutil

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

# Set to True to enable debug output, False to disable
DEBUG = False
MUTE_SOUNDS = False

# Sound file paths - these are terminal bell codes that will work when sound files aren't available
SOUND_WORK_START = '\a'
SOUND_WORK_END = '\a'
SOUND_SHORT_BREAK_START = '\a'
SOUND_SHORT_BREAK_END = '\a'
SOUND_LONG_BREAK_START = '\a'
SOUND_LONG_BREAK_END = '\a'

def play_sound(sound_type):
    """Play a sound effect based on the type of event.
    
    Args:
        sound_type: Type of sound to play (work_start, work_end, short_break_start, etc.)
    """
    if MUTE_SOUNDS:
        debug_print(f"Sound muted for event: {sound_type}")
        return
    
    debug_print(f"Playing sound for event: {sound_type}")
    
    # Map of sound types to their respective sound files/codes
    sound_map = {
        'work_start': SOUND_WORK_START,
        'work_end': SOUND_WORK_END,
        'short_break_start': SOUND_SHORT_BREAK_START,
        'short_break_end': SOUND_SHORT_BREAK_END,
        'long_break_start': SOUND_LONG_BREAK_START,
        'long_break_end': SOUND_LONG_BREAK_END
    }
    
    sound = sound_map.get(sound_type, '\a')  # Default to terminal bell
    
    # Check if the sound is a terminal bell code
    if sound == '\a':
        debug_print("Using terminal bell")
        print(sound, end='', flush=True)
        return
    
    # Try to play the sound file using various available players
    try:
        if shutil.which('aplay'):
            debug_print(f"Playing sound with aplay: {sound}")
            subprocess.run(['aplay', '-q', sound], stderr=subprocess.DEVNULL)
        elif shutil.which('play'):  # Part of SoX
            debug_print(f"Playing sound with play (sox): {sound}")
            subprocess.run(['play', '-q', sound], stderr=subprocess.DEVNULL)
        else:
            debug_print("No sound player found, using terminal bell")
            print('\a', end='', flush=True)
    except Exception as e:
        debug_print(f"Error playing sound: {e}")
        print('\a', end='', flush=True)  # Fallback to terminal bell

def debug_print(message):
    """Print debug messages if DEBUG is True."""
    if DEBUG:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{COLORS['CYAN']}[DEBUG {timestamp}] {message}{COLORS['RESET']}")

def parse_arguments():
    """Parse command line arguments."""
    debug_print("Entering parse_arguments()")
    parser = argparse.ArgumentParser(description='A simple Pomodoro timer.')
    parser.add_argument('--work', type=int, default=25,
                        help='Work session duration in minutes (default: 25)')
    parser.add_argument('--short-break', type=int, default=5,
                        help='Short break duration in minutes (default: 5)')
    parser.add_argument('--long-break', type=int, default=15,
                        help='Long break duration in minutes (default: 15)')
    parser.add_argument('--pomodoros', type=int, default=4,
                        help='Number of pomodoros before a long break (default: 4)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug output')
    parser.add_argument('--mute', action='store_true',
                        help='Mute all sound effects')
    args = parser.parse_args()
    
    # Set DEBUG flag if --debug argument is provided
    global DEBUG
    if args.debug:
        DEBUG = True
        debug_print("Debug mode enabled")
    
    global MUTE_SOUNDS
    if args.mute:
        MUTE_SOUNDS = True
        debug_print("Sound effects muted")
    
    debug_print(f"Arguments parsed: {args}")
    return args

def clear_screen():
    """Clear the terminal screen."""
    debug_print("Clearing screen")
    if not DEBUG:  # Skip clearing screen in debug mode to preserve debug messages
        os.system('cls' if os.name == 'nt' else 'clear')

def send_notification(title, message):
    """Send a system notification."""
    debug_print(f"Sending notification - Title: '{title}', Message: '{message}'")
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
    debug_print(f"Displaying timer - Session: {session_type}, Remaining: {remaining_seconds}s, Total: {total_seconds}s")
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
    debug_print(f"Entering run_timer() - Duration: {duration_minutes}m, Session: {session_type}")
    duration_seconds = duration_minutes * 60
    end_time = time.time() + duration_seconds
    debug_print(f"Timer set - End time: {datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')}")
    
    # Notify session start
    # Notify session start
    send_notification("Pomodoro Timer", f"{session_type} session started")
    print(f"\n{COLORS['YELLOW']}Starting {session_type} session ({duration_minutes} minutes){COLORS['RESET']}")
    debug_print(f"{session_type} session officially started")
    
    # Play sound for session start
    if session_type == "Work":
        play_sound('work_start')
    elif session_type == "Short Break":
        play_sound('short_break_start')
    elif session_type == "Long Break":
        play_sound('long_break_start')
    
    time.sleep(1)  # Small pause to read the message
    try:
        while time.time() < end_time:
            current_time = time.time()
            remaining_seconds = int(end_time - current_time)
            
            # Log every 30 seconds or on the last second
            if remaining_seconds % 30 == 0 or remaining_seconds <= 1:
                debug_print(f"Timer update - Remaining: {format_time(remaining_seconds)}")
                
            display_timer(session_type, remaining_seconds, duration_seconds)
            time.sleep(1)
        
        # Notify session end
        debug_print(f"{session_type} session completed normally")
        clear_screen()
        print(f"\n{COLORS['YELLOW']}{session_type} session completed!{COLORS['RESET']}")
        send_notification("Pomodoro Timer", f"{session_type} session completed!")
        
        # Play sound for session end
        if session_type == "Work":
            play_sound('work_end')
        elif session_type == "Short Break":
            play_sound('short_break_end')
        elif session_type == "Long Break":
            play_sound('long_break_end')
        
    except KeyboardInterrupt:
        debug_print(f"{session_type} session interrupted by user")
        clear_screen()
        print(f"\n{COLORS['YELLOW']}Timer stopped.{COLORS['RESET']}")
        sys.exit(0)
    finally:
        debug_print(f"Exiting run_timer() - Session: {session_type}")

def handle_interrupt(sig, frame):
    """Handle keyboard interrupt."""
    debug_print(f"Signal handler called with signal {sig}")
    clear_screen()
    print(f"\n{COLORS['YELLOW']}Timer stopped.{COLORS['RESET']}")
    sys.exit(0)

def main():
    """Main function to run the Pomodoro timer."""
    debug_print("Entering main()")
    args = parse_arguments()
    
    # Register signal handler for clean exits
    signal.signal(signal.SIGINT, handle_interrupt)
    debug_print("Registered signal handler for SIGINT")
    
    # Set up custom sound files if they exist in the same directory
    global SOUND_WORK_START, SOUND_WORK_END
    global SOUND_SHORT_BREAK_START, SOUND_SHORT_BREAK_END
    global SOUND_LONG_BREAK_START, SOUND_LONG_BREAK_END
    
    sound_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
    
    if os.path.isdir(sound_dir):
        debug_print(f"Found sounds directory: {sound_dir}")
        
        work_start = os.path.join(sound_dir, "work_start.wav")
        if os.path.isfile(work_start):
            SOUND_WORK_START = work_start
            debug_print(f"Using custom sound for work start: {work_start}")
            
        work_end = os.path.join(sound_dir, "work_end.wav")
        if os.path.isfile(work_end):
            SOUND_WORK_END = work_end
            debug_print(f"Using custom sound for work end: {work_end}")
            
        short_break_start = os.path.join(sound_dir, "short_break_start.wav")
        if os.path.isfile(short_break_start):
            SOUND_SHORT_BREAK_START = short_break_start
            debug_print(f"Using custom sound for short break start: {short_break_start}")
            
        short_break_end = os.path.join(sound_dir, "short_break_end.wav")
        if os.path.isfile(short_break_end):
            SOUND_SHORT_BREAK_END = short_break_end
            debug_print(f"Using custom sound for short break end: {short_break_end}")
            
        long_break_start = os.path.join(sound_dir, "long_break_start.wav")
        if os.path.isfile(long_break_start):
            SOUND_LONG_BREAK_START = long_break_start
            debug_print(f"Using custom sound for long break start: {long_break_start}")
            
        long_break_end = os.path.join(sound_dir, "long_break_end.wav")
        if os.path.isfile(long_break_end):
            SOUND_LONG_BREAK_END = long_break_end
            debug_print(f"Using custom sound for long break end: {long_break_end}")
    else:
        debug_print("No sounds directory found, using terminal bell for all sounds")
    
    pomodoro_count = 0
    debug_print("Starting pomodoro cycle")
    
    try:
        while True:
            # Work session
            pomodoro_count += 1
            debug_print(f"Starting pomodoro #{pomodoro_count}")
            run_timer(args.work, "Work")
            
            # Determine break type
            if pomodoro_count % args.pomodoros == 0:
                # Long break after specified number of pomodoros
                debug_print(f"Taking long break after {args.pomodoros} pomodoros")
                run_timer(args.long_break, "Long Break")
            else:
                # Short break
                debug_print("Taking short break")
                run_timer(args.short_break, "Short Break")
                
    except KeyboardInterrupt:
        debug_print("Main loop interrupted by user")
        clear_screen()
        print(f"\n{COLORS['YELLOW']}Pomodoro timer stopped.{COLORS['RESET']}")
        sys.exit(0)
    except Exception as e:
        debug_print(f"Unexpected error in main loop: {str(e)}")
        raise
    finally:
        debug_print("Exiting main()")

if __name__ == "__main__":
    debug_print("Script started")
    main()
    debug_print("Script ended")

