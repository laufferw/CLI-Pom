# CLI Pomodoro Timer

A simple and effective command-line Pomodoro timer to boost your productivity and manage your work sessions efficiently.

## Overview

The CLI Pomodoro Timer is a Python-based application that implements the Pomodoro Technique, a time management method that uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks. This technique helps improve focus and productivity by encouraging you to work with the time you have, rather than against it.

## Features

- **Work Sessions**: Default 25-minute focused work intervals
- **Short Breaks**: Default 5-minute short breaks between work sessions
- **Long Breaks**: Default 15-minute extended breaks after completing a set of work sessions
- **Session Tracking**: Automatically tracks completed work sessions and cycles
- **Command-line Notifications**: Receive notifications when sessions start and end
- **Progress Bar**: Visual representation of time remaining in current session
- **Customizable Settings**: Modify session durations and cycle counts via command-line arguments
- **Minimal Interface**: Distraction-free command-line interface

## Installation

### Prerequisites
- Python 3.6 or higher

### Basic Installation

1. Clone the repository:
```bash
git clone https://github.com/username/CLI-Pom-Timer.git
cd CLI-Pom-Timer
```

2. Make the script executable:
```bash
chmod +x pomodoro.py
```

3. You're ready to go!

## Usage

### Basic Usage

Run the timer with default settings:
```bash
./pomodoro.py
```

### Command-line Options

The timer supports the following command-line arguments:

| Option | Description | Default |
|--------|-------------|---------|
| `--work` | Duration of work sessions in minutes | 25 |
| `--short-break` | Duration of short breaks in minutes | 5 |
| `--long-break` | Duration of long breaks in minutes | 15 |
| `--pomodoros` | Number of work sessions before a long break | 4 |

## Example Usage

### Default Pomodoro Session
```bash
./pomodoro.py
```

### Custom Work Duration and Break Times
```bash
./pomodoro.py --work 30 --short-break 8 --long-break 20
```

### Shorter Cycle with Only 3 Work Sessions Before Long Break
```bash
./pomodoro.py --pomodoros 3
```

### Full Customization
```bash
./pomodoro.py --work 45 --short-break 10 --long-break 30 --pomodoros 2
```

## Customizing the Timer

You can customize every aspect of the timer using command-line arguments:

1. **Work Session Duration**: Use `--work` followed by the number of minutes
2. **Short Break Duration**: Use `--short-break` followed by the number of minutes
3. **Long Break Duration**: Use `--long-break` followed by the number of minutes
4. **Work Sessions Count**: Use `--pomodoros` followed by the number of work sessions before a long break

## Stopping the Timer

- To exit the timer at any time, press `Ctrl+C` on your keyboard
- The timer will gracefully exit and display a goodbye message

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

