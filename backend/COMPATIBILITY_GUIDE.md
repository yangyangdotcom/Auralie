# Compatibility Guide - How Matching Works in Auralie

## 📊 How Compatibility is Calculated

### Current System

Compatibility in Auralie is based on **Fondness Levels** that evolve during the 7-day simulation.

```
Compatibility = (Person1 Fondness + Person2 Fondness) / 2

Ratings:
- 75-100: "Highly compatible" ❤️❤️❤️
- 60-74:  "Compatible" ❤️❤️
- 40-59:  "Moderately compatible" ❤️
- 0-39:   "Not compatible" 💔
```

### Fondness System

Each person starts at **50/100** fondness and changes based on interactions:

```
Starting: 50/100 (neutral, curious)
After 7 days:
- 80+: Very interested and excited
- 60-79: Genuinely interested
- 40-59: Somewhat interested
- 20-39: Losing interest
- 0-19: Not compatible
```

## 🎯 What Influences Compatibility

The LLM (AI) considers these factors when updating fondness:

### 1. **Shared Interests** (Major Factor)
```python
interests: ["hiking", "photography", "cooking"]
```
**High compatibility**: 3+ shared interests
**Example**: Both love dogs → +5 fondness

### 2. **Aligned Values** (Major Factor)
```python
values: ["authenticity", "adventure", "growth"]
```
**High compatibility**: 2+ shared core values
**Example**: Both value "family" → +7 fondness

### 3. **Personality Compatibility** (Major Factor)
```python
mbti: "ENFP" vs "INFJ"
```
**Compatible pairs**:
- ENFP ↔ INFJ (extravert/introvert balance)
- ENTJ ↔ INTP (thinking types)
- ESFP ↔ ISFJ (sensing types)

**Less compatible**:
- INTJ ↔ ESFP (very different approaches)
- ISTJ ↔ ENFP (structure vs spontaneity clash)

### 4. **Communication Style Match**
```python
communication_style: "warm and expressive" vs "direct and concise"
```
**Compatible**: Similar or complementary styles
**Example**:
- "Thoughtful and careful" + "Patient listener" = Good match
- "Direct and concise" + "Warm and expressive" = Can work
- "Direct and blunt" + "Sensitive and careful" = Friction

### 5. **Lifestyle Compatibility**
```python
spontaneity_level: 8/10 vs 3/10
emotional_expressiveness: 7/10 vs 2/10
```
**Rule**: Difference > 5 points = potential issues
**Example**:
- Spontaneity 9 + Spontaneity 3 = Conflict (-3 fondness)
- Spontaneity 7 + Spontaneity 5 = Complementary (+2 fondness)

### 6. **Dealbreakers** (Can Kill Compatibility)
```python
dealbreakers: ["dishonesty", "lack of ambition"]
```
If partner exhibits dealbreaker → **-10 to -20 fondness** immediately

### 7. **Love Language Compatibility**
```python
love_language: "physical touch" vs "words of affirmation"
```
**Best**: Matching or complementary
**Challenging**: Very different needs

## 🎨 How to Create Compatible Pairs

### Method 1: Profile Similarity (Easy)

Match people with similar:
- **Interests** (3+ shared)
- **Values** (2+ shared)
- **Communication style**
- **Lifestyle traits** (within 3-4 points)

**Example - High Compatibility:**
```python
# Person A
interests = ["reading", "yoga", "art galleries", "coffee"]
values = ["empathy", "creativity", "authenticity"]
mbti = "INFJ"
spontaneity_level = 5
communication_style = "thoughtful and genuine"

# Person B
interests = ["reading", "museums", "coffee", "writing"]
values = ["authenticity", "creativity", "growth"]
mbti = "INFP"
spontaneity_level = 6
communication_style = "gentle and expressive"

# Result: 85/100 compatibility ✅
```

### Method 2: Complementary Traits (Interesting)

Match opposites that balance:
- **Extravert + Introvert** (social balance)
- **Planner + Spontaneous** (adventure + stability)
- **Logical + Emotional** (head + heart)

**Example - Complementary Match:**
```python
# Person A - The Planner
mbti = "ISTJ"
spontaneity_level = 3
values = ["stability", "loyalty", "discipline"]
interests = ["fitness", "meal prep", "investing"]

# Person B - The Adventurer (but not too extreme)
mbti = "ENFP"
spontaneity_level = 7
values = ["adventure", "authenticity", "growth"]
interests = ["hiking", "travel", "photography", "fitness"]

# Shared: "fitness", value adventure but also appreciate planning
# Result: 72/100 compatibility ✅
```

### Method 3: Avoid Conflict Zones (Important)

**Red Flags** (will reduce compatibility):

1. **Dealbreaker Violations**
   ```python
   Person A dealbreakers = ["laziness"]
   Person B linkedin = "looking for balance, not career-focused"
   # Result: -15 fondness
   ```

2. **Extreme Trait Differences**
   ```python
   Person A: spontaneity_level = 10 (chaotic)
   Person B: spontaneity_level = 2 (rigid)
   # Result: -8 fondness, frequent friction
   ```

3. **Value Conflicts**
   ```python
   Person A values = ["family", "tradition", "stability"]
   Person B values = ["freedom", "independence", "adventure"]
   # Result: Moderate conflict, 45/100
   ```

4. **MBTI Clashes**
   ```python
   # High conflict pairs:
   INTJ + ESFP  # Logic vs Feelings, Planning vs Spontaneity
   ISTJ + ENFP  # Structure vs Chaos
   ENTJ + ISFP  # Domineering vs Gentle
   ```

## 🧪 Testing Compatibility Hypotheses

### Test 1: Shared Interests Importance

Create two profiles with:
- **Many shared interests** (5+) but different values
- **Few shared interests** (1-2) but aligned values

**Hypothesis**: Values matter more than interests
**Expected**: Value-aligned pair scores higher

### Test 2: Personality Type Compatibility

Test classic MBTI compatible pairs:
- ENFP + INFJ (The Advocate + The Protagonist)
- ENTP + INTJ (The Debater + The Architect)
- ESFJ + ISFP (The Consul + The Adventurer)

**Expected**: 70-85 compatibility

### Test 3: Dealbreaker Impact

Create profiles where one person exhibits another's dealbreaker:
```python
Person A dealbreakers = ["arrogance"]
Person B bio = "confident and know what I want, don't settle"
```

**Expected**: <50 compatibility

## 📝 Example Compatible Profiles

### High Compatibility Example (85-90)

**Person A - Clare Martinez**
```python
mbti = "INFJ"
interests = ["reading", "baking", "yoga", "dogs", "art galleries"]
values = ["empathy", "creativity", "authenticity", "family"]
communication_style = "thoughtful and genuine"
spontaneity_level = 5
love_language = "words of affirmation"
dealbreakers = ["arrogance", "lack of ambition"]
```

**Person B - David Chen**
```python
mbti = "ENFP"
interests = ["hiking", "photography", "cooking", "dogs", "live music"]
values = ["authenticity", "adventure", "growth", "kindness"]
communication_style = "warm and expressive"
spontaneity_level = 7
love_language = "quality time"
dealbreakers = ["dishonesty", "close-mindedness"]
```

**Why They're Compatible:**
- ✅ Shared interest: Dogs
- ✅ Shared values: Authenticity
- ✅ Complementary MBTI (ENFP + INFJ)
- ✅ Communication styles mesh well
- ✅ Spontaneity difference manageable (5 vs 7)
- ✅ No dealbreaker conflicts
- ✅ Similar age/life stage

**Expected Result**: 82-88/100

### Moderate Compatibility Example (55-65)

**Person A - Marcus Johnson**
```python
mbti = "ISTJ"
interests = ["fitness", "investing", "basketball", "meal prep"]
values = ["discipline", "loyalty", "integrity", "health"]
communication_style = "direct and practical"
spontaneity_level = 3
dealbreakers = ["unreliability", "laziness", "financial irresponsibility"]
```

**Person B - Sophie Laurent**
```python
mbti = "ESFP"
interests = ["dancing", "wine tasting", "social events", "fashion"]
values = ["fun", "friendship", "living in the moment", "positivity"]
communication_style = "energetic and enthusiastic"
spontaneity_level = 9
dealbreakers = ["being too serious", "judgmental attitude"]
```

**Why Lower Compatibility:**
- ❌ Very different interests (fitness vs parties)
- ❌ Different values (discipline vs fun)
- ❌ MBTI clash (structured vs spontaneous)
- ❌ Large spontaneity gap (3 vs 9)
- ⚠️ Potential dealbreaker: Marcus might seem "too serious"

**Expected Result**: 42-58/100

## 🛠️ How to Manually Create a Compatible Pair

### Step 1: Start with MBTI Compatibility

Choose complementary types:
```
Good combinations:
- ENFP + INFJ
- ENTP + INTJ
- ESFJ + ISTP
- ENFJ + INFP
```

### Step 2: Add Shared Core Values (2-3)

Pick from these value categories:
- **Traditional**: family, stability, loyalty, tradition
- **Adventurous**: freedom, adventure, growth, independence
- **Intellectual**: curiosity, innovation, learning, excellence
- **Social**: community, empathy, friendship, kindness

### Step 3: Add Some Shared Interests (2-4)

```python
# Option 1: Outdoor couple
["hiking", "camping", "photography", "travel"]

# Option 2: Creative couple
["art", "music", "cooking", "museums"]

# Option 3: Active couple
["fitness", "sports", "yoga", "healthy eating"]

# Option 4: Intellectual couple
["reading", "podcasts", "board games", "debates"]
```

### Step 4: Balance Personality Traits

Keep trait differences **< 4 points**:
```python
# Good balance
Person A: spontaneity_level = 5
Person B: spontaneity_level = 7

# Too different
Person A: spontaneity_level = 2
Person B: spontaneity_level = 9
```

### Step 5: Avoid Dealbreaker Conflicts

Make sure Person B doesn't exhibit Person A's dealbreakers:
```python
# Person A dealbreakers
dealbreakers = ["lack of ambition", "dishonesty"]

# Person B must have
bio = "driven and honest"  # ✅
values = ["integrity", "growth"]  # ✅
```

## 📊 Quick Compatibility Checklist

Use this to predict compatibility before running simulation:

- [ ] MBTI types are compatible (+10 points)
- [ ] 2+ shared values (+15 points)
- [ ] 2+ shared interests (+10 points)
- [ ] Spontaneity difference < 4 (+10 points)
- [ ] Expressiveness difference < 4 (+5 points)
- [ ] Communication styles compatible (+10 points)
- [ ] No dealbreaker violations (+20 points)
- [ ] Similar life stage/age (+5 points)

**Total Score:**
- 70-85 points: Highly compatible
- 50-69 points: Compatible
- 30-49 points: Moderately compatible
- <30 points: Not compatible

## 🎯 Pro Tips

### 1. Use Complementary, Not Identical
Don't make clones! Slight differences create interest:
```python
# Too similar (boring)
Both: spontaneity_level = 5, same interests, same values

# Better (complementary)
Person A: spontaneity_level = 5, interests = ["reading", "yoga"]
Person B: spontaneity_level = 7, interests = ["reading", "hiking"]
```

### 2. Values > Interests
Shared values are more important than shared hobbies:
```python
# High compatibility despite different interests
Different interests but shared values: "authenticity", "growth"
Result: 78/100

# Lower compatibility despite shared interests
Same interests but different values: "stability" vs "freedom"
Result: 52/100
```

### 3. One Dealbreaker Can Ruin Everything
Even with great alignment, dealbreakers matter:
```python
# Everything perfect but...
Person A dealbreakers = ["smoking"]
Person B bio mentions "occasional smoker"
Result: Drops from 85 to 45
```

### 4. Test Edge Cases
Create intentionally mismatched pairs to see system boundaries:
- Extreme opposites (INTJ + ESFP)
- All shared interests, no shared values
- Perfect on paper but conflicting dealbreakers

## 🔮 Future Enhancements

Ideas to improve compatibility algorithm:

1. **Weighted Factors**
   - Values: 40% weight
   - Personality: 25%
   - Interests: 20%
   - Communication: 15%

2. **Dynamic Dealbreakers**
   - Some dealbreakers are "hard" (instant -30)
   - Others are "soft" (gradual -10 over time)

3. **Attachment Styles**
   - Secure + Secure = Best
   - Anxious + Avoidant = Worst

4. **Long-term Factors**
   - Life goals alignment
   - Family planning compatibility
   - Financial compatibility

---

**Want to test?** Create profiles using this guide and see what compatibility you get!
