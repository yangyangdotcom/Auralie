from typing import Dict
import json

class OutputFormatter:
    """Format simulation results in a readable format"""

    @staticmethod
    def format_simulation_output(simulation_result: Dict) -> str:
        """Format the complete simulation in the requested output format"""

        output_lines = []

        # Header
        output_lines.append("=" * 70)
        output_lines.append("AURALIE - VIRTUAL DATING SIMULATION RESULTS")
        output_lines.append("=" * 70)
        output_lines.append("")

        person1_name = simulation_result["participants"]["person1"]
        person2_name = simulation_result["participants"]["person2"]

        output_lines.append(f"Participants: {person1_name} & {person2_name}")
        output_lines.append("")

        # Format each day
        for day_data in simulation_result["days"]:
            day_num = day_data["day"]
            output_lines.append("-" * 70)
            output_lines.append(f"DAY {day_num}")
            output_lines.append("-" * 70)
            output_lines.append("")

            # Texting sessions
            for session in day_data["texting_sessions"]:
                time = session["time"]
                output_lines.append(f"📱 {time.upper()} - Texting each other")
                output_lines.append("")

                for exchange in session["exchanges"]:
                    sender = exchange["sender"]
                    message = exchange["message"]
                    emotion = exchange["emotion"]
                    thought = exchange["internal_thought"]

                    output_lines.append(f"[{sender}]: {message}")
                    output_lines.append(f"    💭 {thought} — feeling {emotion}")
                    output_lines.append("")

            # Activities
            for activity_data in day_data.get("activities", []):
                activity = activity_data["activity"]
                output_lines.append(f"🎯 {activity['name'].upper()}")
                output_lines.append(f"   {activity['description']}")
                output_lines.append("")

                for interaction in activity_data["interactions"]:
                    sender = interaction["sender"]
                    message = interaction["message"]
                    emotion = interaction["emotion"]
                    thought = interaction["internal_thought"]

                    output_lines.append(f"[{sender}]: {message}")
                    output_lines.append(f"    💭 {thought} — feeling {emotion}")
                    output_lines.append("")

            output_lines.append("")

        # Final assessment
        output_lines.append("=" * 70)
        output_lines.append("VIRTUAL DATING OUTCOME")
        output_lines.append("=" * 70)
        output_lines.append("")

        compatibility = simulation_result["compatibility"]
        output_lines.append(f"Overall Compatibility: {compatibility['rating']} ({compatibility['score']:.1f}/100)")
        output_lines.append("")

        for person, assessment in simulation_result["final_assessment"].items():
            output_lines.append(f"[{person}]: {assessment['statement']}")
            output_lines.append(f"    Final fondness level: {assessment['final_fondness']}/100")
            output_lines.append("")

        return "\n".join(output_lines)

    @staticmethod
    def save_formatted_output(simulation_result: Dict, filepath: str):
        """Save formatted output to a text file"""
        formatted = OutputFormatter.format_simulation_output(simulation_result)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted)

        print(f"📄 Formatted output saved to: {filepath}")

    @staticmethod
    def print_simulation_summary(simulation_result: Dict):
        """Print a quick summary of the simulation"""
        person1_name = simulation_result["participants"]["person1"]
        person2_name = simulation_result["participants"]["person2"]

        person1_fondness = simulation_result["final_assessment"][person1_name]["final_fondness"]
        person2_fondness = simulation_result["final_assessment"][person2_name]["final_fondness"]

        compatibility = simulation_result["compatibility"]

        print("\n" + "=" * 70)
        print("SIMULATION COMPLETE!")
        print("=" * 70)
        print(f"\n{person1_name} ❤️  {person2_name}")
        print(f"\nCompatibility: {compatibility['rating']} ({compatibility['score']:.1f}/100)")
        print(f"{person1_name} fondness: {person1_fondness}/100")
        print(f"{person2_name} fondness: {person2_fondness}/100")
        print("\n" + "=" * 70)
