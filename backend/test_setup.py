#!/usr/bin/env python3
"""
Quick setup verification script for Auralie
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")

    required_modules = {
        'openai': 'openai',
        'dotenv': 'python-dotenv',
        'pydantic': 'pydantic'
    }

    missing = []
    for module, package in required_modules.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing.append(package)

    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False

    print("✅ All dependencies installed!\n")
    return True

def check_env_file():
    """Check if .env file is configured"""
    print("Checking environment configuration...")

    if not os.path.exists('.env'):
        print("  ❌ .env file not found")
        print("  Run: cp .env.example .env")
        print("  Then edit .env and add your API key")
        return False

    with open('.env', 'r') as f:
        content = f.read()

    has_openrouter = 'OPENROUTER_API_KEY=' in content and 'your_openrouter_api_key_here' not in content

    if has_openrouter:
        print("  ✅ OpenRouter API key configured")
    else:
        print("  ⚠️  No API key configured")
        print("  Edit .env and add your OPENROUTER_API_KEY")
        print("  Get a key at: https://openrouter.ai/keys")
        return False

    print("✅ Environment configured!\n")
    return True

def check_structure():
    """Check project structure"""
    print("Checking project structure...")

    required_dirs = ['src', 'profiles', 'simulations', 'output']
    required_files = [
        'src/main.py',
        'src/profile.py',
        'src/twin.py',
        'src/simulator.py',
        'src/activities.py',
        'src/config.py',
        'src/llm_client.py',
        'src/output_formatter.py',
        'src/sample_profiles.py'
    ]

    all_good = True

    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ - MISSING")
            all_good = False

    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"  ✅ {filepath}")
        else:
            print(f"  ❌ {filepath} - MISSING")
            all_good = False

    if all_good:
        print("✅ Project structure complete!\n")
    else:
        print("❌ Project structure incomplete\n")

    return all_good

def test_import():
    """Test importing the main modules"""
    print("Testing module imports...")

    sys.path.insert(0, 'src')

    try:
        from config import Config
        print("  ✅ config.py")

        from profile import UserProfile
        print("  ✅ profile.py")

        from llm_client import LLMClient
        print("  ✅ llm_client.py")

        from twin import DigitalTwin
        print("  ✅ twin.py")

        from simulator import DatingSimulation
        print("  ✅ simulator.py")

        from activities import ActivityScenario
        print("  ✅ activities.py")

        from output_formatter import OutputFormatter
        print("  ✅ output_formatter.py")

        from sample_profiles import create_sample_profiles
        print("  ✅ sample_profiles.py")

        print("✅ All modules import successfully!\n")
        return True

    except Exception as e:
        print(f"❌ Import error: {str(e)}\n")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         AURALIE - SETUP VERIFICATION                      ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    results = []

    results.append(check_dependencies())
    results.append(check_structure())
    results.append(check_import())
    results.append(check_env_file())

    print("="*60)
    if all(results):
        print("🎉 SUCCESS! Your Auralie setup is complete!")
        print("\nNext steps:")
        print("  1. cd src")
        print("  2. python main.py")
        print("\nThis will create sample profiles and run 5 simulations.")
    else:
        print("⚠️  Setup incomplete. Please fix the issues above.")
        print("\nQuick fix:")
        print("  1. pip install -r requirements.txt")
        print("  2. cp .env.example .env")
        print("  3. Edit .env and add your API key")
        print("  4. python test_setup.py (run this again)")

    print("="*60)

if __name__ == "__main__":
    main()
