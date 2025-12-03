from profile import UserProfile, MBTIType, Gender

def create_sample_profiles():
    """Create 10 diverse sample profiles for testing"""

    profiles = [
        UserProfile(
            name="David Chen",
            age=28,
            gender=Gender.MALE,
            mbti=MBTIType.ENFP,
            bio="Adventure seeker and dog dad. Love spontaneous road trips and deep conversations over coffee.",
            instagram_style="travel enthusiast with lots of dog photos",
            linkedin_summary="Product Manager at a tech startup, passionate about user experience",
            interests=["hiking", "photography", "cooking", "dogs", "live music"],
            values=["authenticity", "adventure", "growth", "kindness"],
            love_language="quality time",
            dealbreakers=["dishonesty", "close-mindedness"],
            communication_style="warm and expressive, loves to share stories"
        ),

        UserProfile(
            name="Clare Martinez",
            age=26,
            gender=Gender.FEMALE,
            mbti=MBTIType.INFJ,
            bio="Creative soul with a passion for meaningful connections. Dog lover, bookworm, and aspiring chef.",
            instagram_style="aesthetic photos of books, food, and her puppy Cookie",
            linkedin_summary="UX Designer focused on creating delightful user experiences",
            interests=["reading", "baking", "yoga", "dogs", "art galleries"],
            values=["empathy", "creativity", "authenticity", "family"],
            love_language="words of affirmation",
            dealbreakers=["arrogance", "lack of ambition"],
            communication_style="thoughtful and genuine, takes time to express deep feelings"
        ),

        UserProfile(
            name="Marcus Johnson",
            age=30,
            gender=Gender.MALE,
            mbti=MBTIType.ISTJ,
            bio="Fitness enthusiast and finance professional. Believe in working hard and living balanced.",
            instagram_style="gym progress, healthy meals, and occasional travel",
            linkedin_summary="Financial Analyst with focus on sustainable investments",
            interests=["fitness", "investing", "basketball", "meal prep", "podcasts"],
            values=["discipline", "loyalty", "integrity", "health"],
            love_language="acts of service",
            dealbreakers=["unreliability", "laziness", "financial irresponsibility"],
            communication_style="direct and practical, values efficiency"
        ),

        UserProfile(
            name="Sophie Laurent",
            age=27,
            gender=Gender.FEMALE,
            mbti=MBTIType.ESFP,
            bio="Life of the party who also loves quiet Sunday mornings. Wine enthusiast and amateur dancer.",
            instagram_style="vibrant party photos, wine tastings, dance videos",
            linkedin_summary="Marketing Manager with passion for brand storytelling",
            interests=["dancing", "wine tasting", "social events", "fashion", "concerts"],
            values=["fun", "friendship", "living in the moment", "positivity"],
            love_language="physical touch",
            dealbreakers=["being too serious", "judgmental attitude"],
            communication_style="energetic and enthusiastic, very expressive"
        ),

        UserProfile(
            name="Alex Kim",
            age=29,
            gender=Gender.NON_BINARY,
            mbti=MBTIType.INTP,
            bio="Tech nerd with a soft spot for cats and sci-fi. Building cool things by day, gaming by night.",
            instagram_style="minimal aesthetic, tech setups, cat photos, memes",
            linkedin_summary="Software Engineer specializing in AI/ML systems",
            interests=["programming", "gaming", "sci-fi", "cats", "philosophy"],
            values=["curiosity", "logic", "independence", "innovation"],
            love_language="quality time",
            dealbreakers=["anti-intellectualism", "neediness"],
            communication_style="analytical and precise, enjoys deep debates"
        ),

        UserProfile(
            name="Emma Thompson",
            age=25,
            gender=Gender.FEMALE,
            mbti=MBTIType.ENFJ,
            bio="Teacher who believes in changing the world one student at a time. Love volunteering and outdoor adventures.",
            instagram_style="teaching moments, volunteering activities, nature photos",
            linkedin_summary="Elementary School Teacher passionate about inclusive education",
            interests=["teaching", "volunteering", "camping", "board games", "gardening"],
            values=["compassion", "education", "community", "growth"],
            love_language="words of affirmation",
            dealbreakers=["selfishness", "closed-mindedness"],
            communication_style="encouraging and warm, natural motivator"
        ),

        UserProfile(
            name="Ryan O'Brien",
            age=31,
            gender=Gender.MALE,
            mbti=MBTIType.ESTP,
            bio="Entrepreneur and adrenaline junkie. Building businesses and chasing thrills. Let's make life exciting!",
            instagram_style="action shots of extreme sports, business wins, luxury travel",
            linkedin_summary="Founder of two successful startups, angel investor",
            interests=["rock climbing", "surfing", "entrepreneurship", "poker", "fast cars"],
            values=["ambition", "freedom", "boldness", "winning"],
            love_language="physical touch",
            dealbreakers=["pessimism", "lack of drive", "boring lifestyle"],
            communication_style="confident and direct, persuasive speaker"
        ),

        UserProfile(
            name="Maya Patel",
            age=28,
            gender=Gender.FEMALE,
            mbti=MBTIType.ISFJ,
            bio="Nurse with a big heart. Family-oriented, love cozy nights in, and believe in traditional values with modern twist.",
            instagram_style="family gatherings, home cooking, cozy aesthetics",
            linkedin_summary="Registered Nurse in pediatrics, dedicated to patient care",
            interests=["cooking", "knitting", "family time", "medical dramas", "gardening"],
            values=["family", "stability", "caring", "tradition"],
            love_language="acts of service",
            dealbreakers=["insensitivity", "unpredictability", "lack of family values"],
            communication_style="gentle and supportive, avoids conflict"
        ),

        UserProfile(
            name="Jordan Lee",
            age=26,
            gender=Gender.MALE,
            mbti=MBTIType.INTJ,
            bio="Architect designing the future. Chess player, classical music lover, and weekend philosopher.",
            instagram_style="architectural photography, chess boards, minimalist aesthetic",
            linkedin_summary="Architect focused on sustainable urban design",
            interests=["architecture", "chess", "classical music", "reading", "museums"],
            values=["excellence", "intelligence", "vision", "efficiency"],
            love_language="quality time",
            dealbreakers=["mediocrity", "lack of depth", "emotional drama"],
            communication_style="thoughtful and strategic, values substance over style"
        ),

        UserProfile(
            name="Zara Williams",
            age=29,
            gender=Gender.FEMALE,
            mbti=MBTIType.ENTP,
            bio="Startup founder who thrives on debate and innovation. Life's too short for boring conversations!",
            instagram_style="startup life, debate club, travel adventures, thought-provoking quotes",
            linkedin_summary="Tech Entrepreneur and Innovation Consultant",
            interests=["debating", "startups", "travel", "podcasting", "improv comedy"],
            values=["innovation", "freedom", "intellectual growth", "humor"],
            love_language="words of affirmation",
            dealbreakers=["rigidity", "taking things too personally", "narrow-mindedness"],
            communication_style="witty and challenging, loves intellectual sparring"
        )
    ]

    return profiles

def save_all_sample_profiles():
    """Save all sample profiles to files"""
    profiles = create_sample_profiles()
    for profile in profiles:
        filepath = profile.save()
        print(f"Created profile: {filepath}")
    return profiles

if __name__ == "__main__":
    save_all_sample_profiles()
