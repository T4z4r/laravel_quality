# Laravel Quality Assessor GUI

A modern graphical user interface for analyzing Laravel project quality and code standards compliance.

## 🚀 Features

- **Modern GUI Interface**: Built with CustomTkinter for a sleek, dark-themed user experience
- **Visual Score Representation**: Color-coded progress bars and clear scoring system
- **Comprehensive Analysis**: Checks for:
  - Environment configuration security
  - Code style and formatting tools (Pint/CS Fixer)
  - Test coverage and quality
  - Controller complexity
  - Form Requests usage
  - Migration health
  - Dependencies status
  - Modern Laravel patterns (Actions, Resources)
- **Export Functionality**: Save reports as JSON or HTML
- **User-Friendly**: Progress indicators, error handling, and clear feedback

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Windows Users**: Double-click `run_gui.bat`
2. **Unix/Linux/Mac Users**: Run `./run_gui.sh`
3. **Manual Installation**:
   ```bash
   pip install -r requirements.txt
   python laravel_quality_gui.py
   ```

The launcher scripts will automatically install dependencies and start the application.

## 🎯 Usage

1. **Select Project**: Click "Browse" and select your Laravel project directory
2. **Analyze**: Click "🔍 Assess Quality" to start the analysis
3. **Review Results**: View the detailed assessment with visual score
4. **Export**: Save your report as JSON or HTML using "📄 Export Report"
5. **Clear**: Use "🗑️ Clear Results" to reset for a new analysis

## 📊 Scoring System

- **90-100**: 🌟 Excellent! Best practices followed
- **75-89**: 👍 Good job! Minor improvements needed  
- **60-74**: 🆗 Not bad, but there's room for improvement
- **Below 60**: ⚠️ Needs work – consider refactoring and adding tests

## 🛠️ Technical Details

### Files
- `laravel_quality_gui.py` - Main GUI application
- `laravel_quality.py` - Original command-line assessment logic
- `requirements.txt` - Python dependencies
- `run_gui.bat` - Windows launcher script
- `run_gui.sh` - Unix/Linux/Mac launcher script

### Dependencies
- `customtkinter>=5.2.0` - Modern GUI framework
- Built-in Python libraries: `threading`, `os`, `sys`, `json`, `subprocess`, `pathlib`, `webbrowser`, `datetime`, `tkinter`

### Architecture
- Uses threading to prevent GUI freezing during analysis
- Integrates seamlessly with existing CLI assessment logic
- Provides structured data export (JSON) and web-friendly reports (HTML)

## 🎨 Interface Overview

The GUI features:
- **Header**: Application title and branding
- **Project Selection**: Directory browser with path validation
- **Control Panel**: Main action buttons (Assess, Export, Clear, About)
- **Results Area**: Scrollable display with visual scoring
- **Progress Indicator**: Shows analysis progress
- **Modal Windows**: Export options and About dialog

## 📈 Example Assessment Output

```
📊 Overall Quality Score: 85/100
[Visual progress bar at 85%]

Detailed Feedback:
✓ .env.example exists
✓ Laravel Pint is configured  
✓ Great! 25 test files found
✓ Using Form Requests (8 found)
✓ 15 migration(s)
✓ All direct dependencies up to date
✓ Using Actions pattern!
✓ Using API Resources!

👍 Good job! Minor improvements needed.
```

## 🔧 Development

To modify or extend the application:

1. **GUI Changes**: Edit `laravel_quality_gui.py`
2. **Assessment Logic**: Modify `laravel_quality.py` (CLI compatibility maintained)
3. **Dependencies**: Update `requirements.txt`
4. **Testing**: Run the application and test with various Laravel projects

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Made with ❤️ using CustomTkinter**