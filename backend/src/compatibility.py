"""
Compatibility analysis for personality profiles
Calculates incompatibility penalties based on MBTI, values, and dealbreakers
"""

from typing import Tuple
from profile import UserProfile, MBTIType

class CompatibilityAnalyzer:
    """Analyze compatibility between two profiles"""

    # MBTI dimension opposites (more likely to clash)
    MBTI_TENSIONS = {
        'E': 'I',  # Extrovert vs Introvert
        'I': 'E',
        'S': 'N',  # Sensing vs Intuition
        'N': 'S',
        'T': 'F',  # Thinking vs Feeling
        'F': 'T',
        'J': 'P',  # Judging vs Perceiving
        'P': 'J'
    }

    # Incompatible MBTI pairs (historically clash more often)
    HIGHLY_INCOMPATIBLE_PAIRS = [
        ('INTJ', 'ESFP'), ('ESFP', 'INTJ'),
        ('INFP', 'ESTJ'), ('ESTJ', 'INFP'),
        ('INTP', 'ESFJ'), ('ESFJ', 'INTP'),
        ('INFJ', 'ESTP'), ('ESTP', 'INFJ'),
        ('ISTJ', 'ENFP'), ('ENFP', 'ISTJ'),
        ('ISTP', 'ENFJ'), ('ENFJ', 'ISTP'),
        ('ISFJ', 'ENTP'), ('ENTP', 'ISFJ'),
        ('ISFP', 'ENTJ'), ('ENTJ', 'ISFP'),
    ]

    @classmethod
    def calculate_mbti_friction(cls, type1: MBTIType, type2: MBTIType) -> int:
        """
        Calculate MBTI-based friction
        Returns: penalty value (0 to -3 per interaction)
        """
        t1 = type1.value
        t2 = type2.value

        # Check for highly incompatible pairs
        if (t1, t2) in cls.HIGHLY_INCOMPATIBLE_PAIRS:
            return -2  # Moderate friction for incompatible pairs

        # Count opposing dimensions
        friction_count = 0
        for i in range(4):
            if cls.MBTI_TENSIONS.get(t1[i]) == t2[i]:
                friction_count += 1

        # 3-4 opposites = high friction
        # 2 opposites = moderate friction
        # 0-1 opposites = minimal friction
        if friction_count >= 3:
            return -2
        elif friction_count == 2:
            return -1
        else:
            return 0

    @classmethod
    def calculate_value_mismatch(cls, profile1: UserProfile, profile2: UserProfile) -> int:
        """
        Calculate value mismatch penalty
        Returns: penalty value based on shared values
        """
        values1 = set(profile1.values)
        values2 = set(profile2.values)

        shared_values = len(values1 & values2)
        total_values = len(values1 | values2)

        if total_values == 0:
            return 0

        # Calculate overlap percentage
        overlap = shared_values / len(values1) if len(values1) > 0 else 0

        # Less than 30% shared values = friction
        if overlap < 0.3:
            return -2
        elif overlap < 0.5:
            return -1
        else:
            return 0

    @classmethod
    def check_dealbreaker_violation(cls, profile: UserProfile, partner: UserProfile) -> int:
        """
        Check if partner exhibits any of profile's dealbreakers
        Returns: severe penalty if dealbreaker is found
        """
        if not profile.dealbreakers:
            return 0

        # Check if partner's traits, values, or communication style match dealbreakers
        partner_characteristics = set([
            partner.communication_style.lower(),
            *[v.lower() for v in partner.values],
            *[i.lower() for i in partner.interests]
        ])

        # Check for dealbreaker matches
        for dealbreaker in profile.dealbreakers:
            dealbreaker_lower = dealbreaker.lower()
            # Simplistic check - in production you'd want more sophisticated matching
            for characteristic in partner_characteristics:
                if dealbreaker_lower in characteristic or characteristic in dealbreaker_lower:
                    return -3  # Severe penalty for dealbreaker violation

        return 0

    @classmethod
    def calculate_total_incompatibility_penalty(cls, profile1: UserProfile, profile2: UserProfile) -> Tuple[int, int]:
        """
        Calculate total incompatibility penalty for both profiles
        Returns: (penalty_for_profile1, penalty_for_profile2)
        """
        # MBTI friction (applies to both equally)
        mbti_friction = cls.calculate_mbti_friction(profile1.mbti, profile2.mbti)

        # Value mismatch (applies to both equally)
        value_mismatch = cls.calculate_value_mismatch(profile1, profile2)

        # Dealbreaker violations (individual)
        dealbreaker1 = cls.check_dealbreaker_violation(profile1, profile2)
        dealbreaker2 = cls.check_dealbreaker_violation(profile2, profile1)

        # Total penalties
        penalty1 = mbti_friction + value_mismatch + dealbreaker1
        penalty2 = mbti_friction + value_mismatch + dealbreaker2

        return (penalty1, penalty2)

    @classmethod
    def get_incompatibility_context(cls, profile1: UserProfile, profile2: UserProfile) -> str:
        """
        Generate a context string explaining incompatibilities
        Used to make twins aware of potential friction points
        """
        issues = []

        # MBTI friction
        mbti_friction = cls.calculate_mbti_friction(profile1.mbti, profile2.mbti)
        if mbti_friction < 0:
            issues.append(f"Your {profile1.mbti.value} and their {profile2.mbti.value} personalities may have natural friction in communication styles and energy levels")

        # Value mismatch
        value_penalty = cls.calculate_value_mismatch(profile1, profile2)
        if value_penalty < 0:
            shared = len(set(profile1.values) & set(profile2.values))
            issues.append(f"You only share {shared} core values with them, which may cause friction")

        # Dealbreakers
        dealbreaker_penalty = cls.check_dealbreaker_violation(profile1, profile2)
        if dealbreaker_penalty < 0:
            issues.append("Some of their traits may conflict with your dealbreakers")

        if not issues:
            return ""

        return "COMPATIBILITY NOTES:\n- " + "\n- ".join(issues)
