#!/usr/bin/env python3
"""
Auralie - Digital Twin Dating Simulator
Main entry point for running simulations
"""

import sys
import os
import random
from typing import List, Tuple

from profile import UserProfile
from simulator import DatingSimulation
from output_formatter import OutputFormatter
from sample_profiles import create_sample_profiles, save_all_sample_profiles

def create_random_pairs(profiles: List[UserProfile], num_pairs: int = 5) -> List[Tuple[UserProfile, UserProfile]]:
    """Create random pairs from profiles"""
    pairs = []
    available = profiles.copy()
    random.shuffle(available)

    for i in range(0, min(num_pairs * 2, len(available)), 2):
        if i + 1 < len(available):
            pairs.append((available[i], available[i + 1]))

    return pairs

def run_single_simulation(profile1: UserProfile, profile2: UserProfile):
    """Run a single simulation between two profiles"""

    print(f"\nStarting simulation between {profile1.name} and {profile2.name}...")

    simulation = DatingSimulation(profile1, profile2)

    try:
        result = simulation.run_simulation()

        # Save formatted output
        output_filename = f"output/{simulation.simulation_id}.txt"
        os.makedirs("output", exist_ok=True)
        OutputFormatter.save_formatted_output(result, output_filename)

        # Print summary
        OutputFormatter.print_simulation_summary(result)

        return result

    except Exception as e:
        # Even if simulation failed, try to generate output from partial data
        print(f"\n⚠️  Simulation encountered error, but partial data may be saved")
        raise

def run_batch_simulations(num_simulations: int = 1):
    """Run multiple simulations with random pairings"""
    import time

    print("\n" + "=" * 70)
    print("AURALIE BATCH SIMULATION MODE")
    print("=" * 70)

    # Load or create sample profiles
    profiles = UserProfile.load_all("profiles")

    if len(profiles) < 2:
        print("\nNo existing profiles found. Creating sample profiles...")
        profiles = save_all_sample_profiles()
        print(f"\n✅ Created {len(profiles)} sample profiles\n")

    # Create random pairs
    pairs = create_random_pairs(profiles, num_simulations)

    print(f"\nRunning {len(pairs)} simulations...")
    print(f"⚠️  Note: Each simulation uses ~3,000-5,000 tokens")
    print(f"⚠️  Groq free tier: 100,000 tokens/day limit\n")

    results = []
    for i, (profile1, profile2) in enumerate(pairs, 1):
        print(f"\n{'='*70}")
        print(f"SIMULATION {i}/{len(pairs)}")
        print(f"{'='*70}")

        try:
            result = run_single_simulation(profile1, profile2)
            results.append(result)

            # Add delay between simulations to avoid rate limits
            if i < len(pairs):
                print(f"\n⏳ Waiting 10 seconds before next simulation...")
                time.sleep(10)

        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ Simulation failed: {error_msg}")

            # Check if it's a rate limit error
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                print("\n⚠️  RATE LIMIT ERROR")
                print("Solutions:")
                print("  1. Wait for the time mentioned in the error")
                print("  2. Use faster model: GROQ_MODEL=llama-3.1-8b-instant")
                print("  3. Run fewer simulations at once")
                print("  4. Check usage: https://console.groq.com/usage")
                break  # Stop running more simulations
            continue

    # Print batch summary
    print("\n" + "=" * 70)
    print("BATCH SIMULATION COMPLETE")
    print("=" * 70)
    print(f"\nCompleted {len(results)} simulations")

    if results:
        compatible_count = sum(1 for r in results if r["compatibility"]["score"] >= 60)
        print(f"Compatible matches: {compatible_count}/{len(results)}")

    return results

def interactive_mode():
    """Interactive mode for selecting specific profiles"""

    print("\n" + "=" * 70)
    print("AURALIE INTERACTIVE MODE")
    print("=" * 70)

    profiles = UserProfile.load_all("profiles")

    if len(profiles) < 2:
        print("\nNo profiles found. Creating sample profiles...")
        profiles = save_all_sample_profiles()

    print("\nAvailable profiles:")
    for i, profile in enumerate(profiles, 1):
        print(f"{i}. {profile.name} ({profile.age}, {profile.gender.value}, {profile.mbti.value})")
        print(f"   {profile.bio[:80]}...")

    print("\nSelect two profiles for simulation:")
    try:
        idx1 = int(input("First person (number): ")) - 1
        idx2 = int(input("Second person (number): ")) - 1

        if 0 <= idx1 < len(profiles) and 0 <= idx2 < len(profiles) and idx1 != idx2:
            run_single_simulation(profiles[idx1], profiles[idx2])
        else:
            print("Invalid selection!")
    except (ValueError, IndexError):
        print("Invalid input!")

def main():
    """Main entry point"""

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║                    A U R A L I E                          ║
    ║                                                           ║
    ║            Digital Twin Dating Simulator                  ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "batch":
            num_sims = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            run_batch_simulations(num_sims)

        elif command == "create-profiles":
            print("\nCreating sample profiles...")
            profiles = save_all_sample_profiles()
            print(f"\n✅ Created {len(profiles)} profiles in the 'profiles' directory")

        elif command == "interactive":
            interactive_mode()

        else:
            print(f"Unknown command: {command}")
            print_usage()

    else:
        print("\nNo command specified. Running default batch simulation...\n")
        run_batch_simulations(1)

def print_usage():
    """Print usage information"""
    print("""
Usage:
    python main.py                          Run 5 random simulations (default)
    python main.py batch [num]              Run batch simulations (specify number)
    python main.py interactive              Choose specific profiles to simulate
    python main.py create-profiles          Create sample profiles only

Examples:
    python main.py batch 10                 Run 10 random simulations
    python main.py interactive              Select profiles manually
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Simulation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
