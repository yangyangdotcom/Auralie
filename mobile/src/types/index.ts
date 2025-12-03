export interface Profile {
  id: string;
  name: string;
  age: number;
  mbti: string;
  interests: string[];
  values: string[];
  spontaneity_level: number;
  emotional_expressiveness: number;
  bio?: string;
}

export interface Interaction {
  activity_type: string;
  person1_name: string;
  person1_message: string;
  person1_emotion: string;
  person1_internal_thought: string;
  person1_fondness_change: number;
  person2_name: string;
  person2_message: string;
  person2_emotion: string;
  person2_internal_thought: string;
  person2_fondness_change: number;
}

export interface Day {
  day: number;
  interactions: Interaction[];
  person1_fondness: number;
  person2_fondness: number;
}

export interface SimulationSummary {
  simulation_id: string;
  profile1: string;
  profile2: string;
  compatibility_score?: number;
  status: string;
  completed_days: number;
  created_at?: string;
  completed_at?: string;
}

export interface SimulationResult {
  simulation_id: string;
  status: string;
  profile1: string;
  profile2: string;
  compatibility_score?: number;
  days?: Day[];
  completed_days?: number;
  error?: string;
  result?: {
    days: Day[];
    compatibility: {
      score: number;
    };
    participants: {
      person1: string;
      person2: string;
    };
  };
}

export interface CreateProfileRequest {
  name: string;
  age: number;
  mbti: string;
  interests: string[];
  values: string[];
  spontaneity_level: number;
  emotional_expressiveness: number;
  bio?: string;
}
