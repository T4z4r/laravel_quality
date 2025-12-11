#!/usr/bin/env python3
"""
Laravel Quality Assessment GUI Application
A modern graphical interface for the Laravel project quality assessment tool.
"""

import customtkinter as ctk
import threading
import os
import sys
import json
import subprocess
from pathlib import Path
import webbrowser
from datetime import datetime
from tkinter import filedialog, messagebox

# Import the original assessment logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from laravel_quality import assess_laravel_project

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LaravelQualityGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Laravel Quality Assessor")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        self.setup_ui()
        self.assessment_results = None
        
    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self.root, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🚀 Laravel Quality Assessor", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Project selection frame
        selection_frame = ctk.CTkFrame(self.root)
        selection_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        selection_frame.grid_columnconfigure(1, weight=1)
        
        path_label = ctk.CTkLabel(selection_frame, text="Project Path:", font=ctk.CTkFont(size=14))
        path_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        
        self.path_var = ctk.StringVar()
        self.path_entry = ctk.CTkEntry(
            selection_frame, 
            textvariable=self.path_var, 
            placeholder_text="Select your Laravel project directory...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.path_entry.grid(row=0, column=1, sticky="ew", padx=(10, 10), pady=20)
        
        browse_button = ctk.CTkButton(
            selection_frame,
            text="Browse",
            command=self.browse_directory,
            width=100,
            height=40
        )
        browse_button.grid(row=0, column=2, sticky="e", padx=(10, 20), pady=20)
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(self.root)
        control_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        control_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.assess_button = ctk.CTkButton(
            control_frame,
            text="🔍 Assess Quality",
            command=self.start_assessment,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.assess_button.grid(row=0, column=0, sticky="ew", padx=10, pady=20)
        
        self.export_button = ctk.CTkButton(
            control_frame,
            text="📄 Export Report",
            command=self.export_report,
            height=50,
            state="disabled"
        )
        self.export_button.grid(row=0, column=1, sticky="ew", padx=10, pady=20)
        
        self.clear_button = ctk.CTkButton(
            control_frame,
            text="🗑️ Clear Results",
            command=self.clear_results,
            height=50
        )
        self.clear_button.grid(row=0, column=2, sticky="ew", padx=10, pady=20)
        
        self.about_button = ctk.CTkButton(
            control_frame,
            text="ℹ️ About",
            command=self.show_about,
            height=50
        )
        self.about_button.grid(row=0, column=3, sticky="ew", padx=10, pady=20)
        
        # Results frame with scrollable content
        self.results_frame = ctk.CTkScrollableFrame(self.root, label_text="Assessment Results")
        self.results_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.root, mode="indeterminate")
        self.progress_bar.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.progress_bar.set(0)
        
        # Initial message
        self.show_initial_message()
        
    def show_initial_message(self):
        welcome_frame = ctk.CTkFrame(self.results_frame)
        welcome_frame.grid(row=0, column=0, sticky="ew", pady=10)
        welcome_frame.grid_columnconfigure(0, weight=1)
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="Welcome to Laravel Quality Assessor!",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        welcome_label.pack(pady=20)
        
        instructions = ctk.CTkLabel(
            welcome_frame,
            text="1. Select your Laravel project directory using the Browse button\n2. Click 'Assess Quality' to start the analysis\n3. View detailed results and export reports\n\nThis tool will check your Laravel project for:\n• Environment configuration security\n• Code style and formatting tools\n• Test coverage and quality\n• Controller complexity\n• Form Requests usage\n• Migration health\n• Dependencies status\n• Modern Laravel patterns",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        instructions.pack(pady=(0, 20), padx=20)
        
    def browse_directory(self):
        directory = filedialog.askdirectory(
            title="Select Laravel Project Directory",
            initialdir=os.getcwd()
        )
        if directory:
            self.path_var.set(directory)
            # Validate it's a Laravel project
            path = Path(directory)
            if not (path / "artisan").exists() or not (path / "composer.json").exists():
                self.show_warning("⚠️ This doesn't appear to be a Laravel project.\nMake sure it has 'artisan' and 'composer.json' files.")
    
    def start_assessment(self):
        project_path = self.path_var.get().strip()
        if not project_path:
            messagebox.showwarning("No Directory Selected", "Please select a Laravel project directory first.")
            return
            
        if not Path(project_path).exists():
            messagebox.showerror("Invalid Path", "The selected directory does not exist.")
            return
            
        # Validate Laravel project
        path = Path(project_path)
        if not (path / "artisan").exists() or not (path / "composer.json").exists():
            messagebox.showerror("Invalid Project", "This doesn't appear to be a Laravel project.\nMake sure it has 'artisan' and 'composer.json' files.")
            return
        
        # Clear previous results
        self.clear_results()
        
        # Disable assess button and start progress
        self.assess_button.configure(state="disabled", text="🔄 Analyzing...")
        self.progress_bar.start()
        
        # Run assessment in separate thread
        thread = threading.Thread(target=self.run_assessment, args=(project_path,))
        thread.daemon = True
        thread.start()
        
    def run_assessment(self, project_path):
        try:
            # Capture the output of the assessment
            import io
            from contextlib import redirect_stdout
            
            output_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer):
                assess_laravel_project(project_path)
            
            results_text = output_buffer.getvalue()
            self.assessment_results = self.parse_results(results_text)
            
            # Schedule UI update in main thread
            self.root.after(0, self.display_results, results_text)
            
        except Exception as e:
            error_msg = f"An error occurred during assessment: {str(e)}"
            self.root.after(0, self.show_error, error_msg)
        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.assessment_finished)
            
    def parse_results(self, results_text):
        """Parse the assessment results into structured data"""
        results = {
            "score": 0,
            "feedback": [],
            "timestamp": datetime.now().isoformat(),
            "project_path": self.path_var.get()
        }
        
        lines = results_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("📊 Final Score:"):
                try:
                    score_str = line.split(":")[1].strip().split("/")[0]
                    results["score"] = int(score_str)
                except:
                    pass
            elif line and (line.startswith("✓") or line.startswith("✗") or line.startswith("⚠") or line.startswith("○")):
                results["feedback"].append(line)
                
        return results
        
    def display_results(self, results_text):
        # Clear existing results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        # Create main results container
        main_frame = ctk.CTkFrame(self.results_frame)
        main_frame.grid(row=0, column=0, sticky="ew", pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Score display
        score_frame = ctk.CTkFrame(main_frame)
        score_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=20)
        score_frame.grid_columnconfigure(0, weight=1)
        
        # Extract score for visualization
        score = 0
        for line in results_text.split('\n'):
            if "📊 Final Score:" in line:
                try:
                    score_str = line.split(":")[1].strip().split("/")[0]
                    score = int(score_str)
                    break
                except:
                    pass
        
        score_label = ctk.CTkLabel(
            score_frame,
            text=f"📊 Overall Quality Score: {score}/100",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        score_label.pack(pady=20)
        
        # Progress bar for score
        score_progress = ctk.CTkProgressBar(score_frame, height=20)
        score_progress.pack(pady=(0, 20), padx=20, fill="x")
        score_progress.set(score / 100)
        
        # Color the progress bar based on score
        if score >= 90:
            score_progress.configure(progress_color="green")
            score_label.configure(text_color="green")
        elif score >= 75:
            score_progress.configure(progress_color="orange")
            score_label.configure(text_color="orange")
        elif score >= 60:
            score_progress.configure(progress_color="yellow")
            score_label.configure(text_color="yellow")
        else:
            score_progress.configure(progress_color="red")
            score_label.configure(text_color="red")
        
        # Raw results display
        results_display = ctk.CTkTextbox(
            main_frame,
            height=400,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        results_display.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        results_display.insert("1.0", results_text)
        results_display.configure(state="disabled")
        
        # Status message
        if score >= 90:
            status_msg = "🌟 Excellent! Your Laravel project follows best practices."
        elif score >= 75:
            status_msg = "👍 Good job! Minor improvements needed."
        elif score >= 60:
            status_msg = "🆗 Not bad, but there's room for improvement."
        else:
            status_msg = "⚠️ Needs work – consider refactoring and adding tests!"
            
        status_label = ctk.CTkLabel(
            main_frame,
            text=status_msg,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        status_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
    def assessment_finished(self):
        self.progress_bar.stop()
        self.assess_button.configure(state="normal", text="🔍 Assess Quality")
        self.export_button.configure(state="normal")
        
    def export_report(self):
        if not self.assessment_results:
            messagebox.showwarning("No Results", "No assessment results to export.")
            return
            
        # Ask user for export format
        export_window = ctk.CTkToplevel(self.root)
        export_window.title("Export Report")
        export_window.geometry("400x300")
        export_window.transient(self.root)
        export_window.grab_set()
        
        # Center the window
        export_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        ctk.CTkLabel(export_window, text="Export Report", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        def export_json():
            self.save_json_report()
            export_window.destroy()
            
        def export_html():
            self.save_html_report()
            export_window.destroy()
            
        ctk.CTkButton(export_window, text="Export as JSON", command=export_json, height=40).pack(pady=10, padx=40, fill="x")
        ctk.CTkButton(export_window, text="Export as HTML", command=export_html, height=40).pack(pady=10, padx=40, fill="x")
        ctk.CTkButton(export_window, text="Cancel", command=export_window.destroy, height=40).pack(pady=10, padx=40, fill="x")
        
    def save_json_report(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save JSON Report"
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.assessment_results, f, indent=2)
                messagebox.showinfo("Success", f"Report saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")
                
    def save_html_report(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            title="Save HTML Report"
        )
        if filename:
            try:
                html_content = self.generate_html_report()
                with open(filename, 'w') as f:
                    f.write(html_content)
                messagebox.showinfo("Success", f"Report saved to:\n{filename}\n\nWould you like to open it in your browser?", "Export Complete")
                if messagebox.askyesno("Open Report", "Would you like to open the HTML report in your browser?"):
                    webbrowser.open(f"file://{os.path.abspath(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")
                
    def generate_html_report(self):
        score = self.assessment_results["score"]
        feedback = self.assessment_results["feedback"]
        
        # Determine score color and status
        if score >= 90:
            score_color = "green"
            status = "🌟 Excellent! Your Laravel project follows best practices."
        elif score >= 75:
            score_color = "orange"
            status = "👍 Good job! Minor improvements needed."
        elif score >= 60:
            score_color = "yellow"
            status = "🆗 Not bad, but there's room for improvement."
        else:
            score_color = "red"
            status = "⚠️ Needs work – consider refactoring and adding tests!"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laravel Quality Assessment Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #1a1a1a; color: #fff; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .score-card {{ background: #2d2d2d; border-radius: 10px; padding: 30px; margin-bottom: 20px; text-align: center; }}
        .score {{ font-size: 48px; font-weight: bold; color: {score_color}; }}
        .status {{ font-size: 18px; margin-top: 10px; }}
        .feedback {{ background: #2d2d2d; border-radius: 10px; padding: 20px; }}
        .feedback-item {{ margin: 10px 0; padding: 10px; border-left: 4px solid #007acc; }}
        .feedback-item.positive {{ border-left-color: #4CAF50; }}
        .feedback-item.warning {{ border-left-color: #FF9800; }}
        .feedback-item.negative {{ border-left-color: #F44336; }}
        .progress-bar {{ width: 100%; height: 20px; background: #3d3d3d; border-radius: 10px; overflow: hidden; margin: 20px 0; }}
        .progress-fill {{ height: 100%; background: {score_color}; transition: width 0.3s ease; }}
        .meta {{ color: #888; font-size: 14px; text-align: center; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Laravel Quality Assessment Report</h1>
            <div class="meta">
                Project: {self.assessment_results['project_path']}<br>
                Generated: {self.assessment_results['timestamp']}
            </div>
        </div>
        
        <div class="score-card">
            <div class="score">{score}/100</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {score}%"></div>
            </div>
            <div class="status">{status}</div>
        </div>
        
        <div class="feedback">
            <h3>📋 Detailed Feedback</h3>
            {''.join([f'<div class="feedback-item {self.get_feedback_class(item)}">{item}</div>' for item in feedback])}
        </div>
        
        <div class="meta">
            Generated by Laravel Quality Assessor GUI v1.0
        </div>
    </div>
</body>
</html>
        """
        return html
        
    def get_feedback_class(self, feedback_item):
        if feedback_item.startswith("✓"):
            return "positive"
        elif feedback_item.startswith("⚠") or feedback_item.startswith("○"):
            return "warning"
        else:
            return "negative"
        
    def clear_results(self):
        # Clear the results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        # Show initial message
        self.show_initial_message()
        
        # Reset state
        self.assessment_results = None
        self.export_button.configure(state="disabled")
        
    def show_about(self):
        about_text = """
🚀 Laravel Quality Assessor GUI v1.0

A modern graphical interface for analyzing Laravel project quality.

Features:
• Comprehensive code quality analysis
• Visual score representation
• Detailed feedback and recommendations
• Export reports (JSON/HTML)
• Modern, user-friendly interface

Checks performed:
✓ Environment configuration security
✓ Code style and formatting tools
✓ Test coverage and quality
✓ Controller complexity analysis
✓ Form Requests usage
✓ Migration health
✓ Dependencies status
✓ Modern Laravel patterns

Made with ❤️ using CustomTkinter
        """
        
        about_window = ctk.CTkToplevel(self.root)
        about_window.title("About Laravel Quality Assessor")
        about_window.geometry("500x400")
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Center the window
        about_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 100,
            self.root.winfo_rooty() + 100
        ))
        
        textbox = ctk.CTkTextbox(about_window, font=ctk.CTkFont(size=12))
        textbox.pack(fill="both", expand=True, padx=20, pady=20)
        textbox.insert("1.0", about_text)
        textbox.configure(state="disabled")
        
    def show_warning(self, message):
        messagebox.showwarning("Warning", message)
        
    def show_error(self, message):
        messagebox.showerror("Error", message)
        # Re-enable button and stop progress
        self.assessment_finished()
        
    def run(self):
        self.root.mainloop()

def main():
    app = LaravelQualityGUI()
    app.run()

if __name__ == "__main__":
    main()