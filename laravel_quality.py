#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
        return result.stdout.strip()
    except:
        return ""

def assess_laravel_project(project_path):
    path = Path(project_path).resolve()
    if not path.exists():
        print("❌ Project path does not exist!")
        return

    if not (path / "artisan").exists() or not (path / "composer.json").exists():
        print("❌ This doesn't look like a Laravel project (missing artisan or composer.json)")
        return

    score = 100
    feedback = []

    # 1. .env example exists, .env not committed
    if (path / ".env.example").exists():
        feedback.append("✓ .env.example exists")
    else:
        score -= 10
        feedback.append("✗ Missing .env.example")

    if (path / ".env").exists():
        git_check = run_command(["git", "check-ignore", ".env"], cwd=path)
        if not git_check:
            score -= 15
            feedback.append("⚠ .env is tracked in git! (security risk)")

    # 2. Laravel Pint or PHP CS Fixer
    composer_json = json.loads((path / "composer.json").read_text())
    scripts = composer_json.get("scripts", {})

    if "pint" in str(scripts) or os.path.exists(path / "pint.json"):
        feedback.append("✓ Laravel Pint is configured")
    elif any("cs-fixer" in s for s in str(scripts)):
        feedback.append("✓ PHP CS Fixer is configured")
    else:
        score -= 12
        feedback.append("✗ No code style fixer (Pint or CS Fixer) detected")

    # 3. Tests exist
    if (path / "tests").exists() and any((path / "tests").rglob("*.php")):
        test_count = len(list((path / "tests").rglob("*.php")))
        if test_count > 10:
            feedback.append(f"✓ Great! {test_count} test files found")
        else:
            score -= 8
            feedback.append(f"⚠ Only {test_count} test files (consider writing more)")
    else:
        score -= 20
        feedback.append("✗ No tests found!")

    # 4. Thin controllers (average < 100 lines)
    controllers = list((path / "app" / "Http" / "Controllers").rglob("*.php"))
    large_controllers = [c for c in controllers if c.stat().st_size > 15000]  # ~500 lines
    if large_controllers:
        score -= 10
        feedback.append(f"⚠ {len(large_controllers)} large controller(s) detected")

    # 5. Form Requests used?
    requests = list((path / "app" / "Http" / "Requests").rglob("*.php"))
    if len(requests) > 3:
        feedback.append(f"✓ Using Form Requests ({len(requests)} found)")
    elif len(requests) > 0:
        feedback.append(f"○ Some Form Requests ({len(requests)})")
    else:
        score -= 8
        feedback.append("✗ No Form Requests – validation likely in controllers")

    # 6. Migrations look clean
    migrations = list((path / "database" / "migrations").rglob("*.php"))
    if migrations:
        feedback.append(f"✓ {len(migrations)} migration(s)")
    else:
        score -= 5
        feedback.append("✗ No migrations found")

    # 7. Outdated packages?
    outdated = run_command(["composer", "outdated", "--direct"], cwd=path)
    if "0 packages" in outdated.lower():
        feedback.append("✓ All direct dependencies up to date")
    elif outdated:
        score -= 7
        feedback.append("⚠ Some outdated direct dependencies")

    # 8. Bonus: Uses Laravel actions or resources
    if (path / "app" / "Actions").exists():
        feedback.append("✓ Using Actions pattern!")
        score += 5
    if (path / "app" / "Http" / "Resources").exists():
        feedback.append("✓ Using API Resources!")

    # Final score cap
    score = max(0, min(100, score))

    # Output
    print("\n🚀 Laravel Code Quality Report")
    print("=" * 50)
    for line in feedback:
        print(line)
    print("=" * 50)
    print(f"📊 Final Score: {score}/100")

    if score >= 90:
        print("🌟 Excellent! Your Laravel project follows best practices.")
    elif score >= 75:
        print("👍 Good job! Minor improvements needed.")
    elif score >= 60:
        print("🆗 Not bad, but there's room for improvement.")
    else:
        print("⚠ Needs work – consider refactoring and adding tests!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python laravel_quality.py /path/to/laravel/project")
        sys.exit(1)

    project_path = sys.argv[1]
    assess_laravel_project(project_path)