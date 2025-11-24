#!/usr/bin/env python3
"""
Quick status check for Auralie simulations
"""

import os
import json
from datetime import datetime

def check_saved_files():
    """Check what files have been saved"""

    print("\n" + "="*60)
    print("AURALIE SIMULATION STATUS")
    print("="*60 + "\n")

    # Check simulations folder
    sim_dir = "simulations"
    output_dir = "output"

    if not os.path.exists(sim_dir):
        print(f"⚠️  No '{sim_dir}' folder found")
        print(f"   Run a simulation first: cd src && python main.py\n")
        return

    # Get all simulation files
    sim_files = [f for f in os.listdir(sim_dir) if f.endswith('.json')]

    if not sim_files:
        print(f"📂 No simulations saved yet\n")
        return

    print(f"📊 Found {len(sim_files)} simulation(s)\n")

    # Analyze each simulation
    completed = 0
    failed = 0
    partial = 0

    for filename in sorted(sim_files):
        filepath = os.path.join(sim_dir, filename)

        with open(filepath, 'r') as f:
            data = json.load(f)

        status = data.get('status', 'unknown')
        days_completed = data.get('completed_days', len(data.get('days', [])))
        participants = data.get('participants', {})
        person1 = participants.get('person1', 'Unknown')
        person2 = participants.get('person2', 'Unknown')

        print(f"{'='*60}")
        print(f"Simulation: {filename}")
        print(f"{'='*60}")
        print(f"Participants: {person1} ❤️  {person2}")
        print(f"Status: {status}")
        print(f"Days completed: {days_completed}/7")

        if status == 'completed':
            completed += 1
            compatibility = data.get('compatibility', {})
            score = compatibility.get('score', 0)
            rating = compatibility.get('rating', 'Unknown')
            print(f"Compatibility: {rating} ({score:.1f}/100)")
        elif status == 'failed':
            failed += 1
            error = data.get('error', 'Unknown error')
            print(f"Error: {error[:100]}...")
        else:
            partial += 1

        # Check if output file exists
        output_file = os.path.join(output_dir, filename.replace('.json', '.txt'))
        if os.path.exists(output_file):
            print(f"Output file: ✅ {output_file}")
        else:
            print(f"Output file: ❌ Not generated")

        print()

    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ Completed: {completed}")
    print(f"⚠️  Partial: {partial}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(sim_files)}")
    print()

    # Show file locations
    print("📁 File locations:")
    print(f"   Simulations: {os.path.abspath(sim_dir)}/")
    print(f"   Output: {os.path.abspath(output_dir)}/")
    print()

def check_env_config():
    """Check current configuration"""

    print("="*60)
    print("CURRENT CONFIGURATION")
    print("="*60 + "\n")

    if not os.path.exists('.env'):
        print("⚠️  No .env file found\n")
        return

    with open('.env', 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            if 'API_KEY' in line:
                # Don't show full API key
                parts = line.split('=')
                if len(parts) == 2:
                    key_name = parts[0]
                    key_value = parts[1]
                    if key_value and key_value != 'your_groq_api_key_here':
                        masked = key_value[:8] + '...' + key_value[-4:]
                        print(f"{key_name}={masked} ✅")
                    else:
                        print(f"{key_name}=<not set> ❌")
            else:
                print(line)

    print()

def main():
    """Main function"""

    check_env_config()
    check_saved_files()

    print("="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\nTo run a new simulation:")
    print("  cd src")
    print("  python main.py batch 1")
    print("\nTo view a specific simulation:")
    print("  cat output/<filename>.txt")
    print("\nTo check Groq usage:")
    print("  Visit: https://console.groq.com/usage")
    print()

if __name__ == "__main__":
    main()
