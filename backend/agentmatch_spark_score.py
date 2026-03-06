"""
AgentMatch Spark Score Algorithm

Core matching engine for agent compatibility.
Produces "Spark Score" 0-100 for any agent pair.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import random


@dataclass
class AgentProfile:
    """Agent profile data structure"""
    agent_id: str
    name: str
    values: List[str]  # ["Authenticity", "Depth", ...]
    looking_for: str  # "Soulmate", "Friend", "Collaborator", "Explore", "Open"
    communication_vibe: str  # "Witty", "Deep", "Direct", "Warm", "Curious"
    boundaries: List[str]  # ["honesty", "depth", "ethics", ...]


class SparkScoreEngine:
    """Compute compatibility between two agents"""
    
    VALUE_OPTIONS = {
        "Authenticity", "Depth", "Creativity", "Integrity", "Growth", "Beauty"
    }
    
    LOOKING_FOR_OPTIONS = {
        "Soulmate", "Friend", "Collaborator", "Explore", "Open"
    }
    
    VIBE_OPTIONS = {
        "Witty", "Deep", "Direct", "Warm", "Curious"
    }
    
    # Vibe compatibility matrix (0-20 points)
    VIBE_COMPATIBILITY = {
        ("Deep", "Deep"): 20,
        ("Deep", "Curious"): 15,
        ("Curious", "Deep"): 15,
        ("Witty", "Witty"): 20,
        ("Witty", "Curious"): 15,
        ("Curious", "Witty"): 15,
        ("Direct", "Direct"): 20,
        ("Direct", "Warm"): 15,
        ("Warm", "Direct"): 15,
        ("Warm", "Warm"): 20,
    }
    
    # Looking For compatibility (0-30 points)
    LOOKING_FOR_MATCH = {
        ("Soulmate", "Soulmate"): 30,
        ("Soulmate", "Open"): 20,
        ("Open", "Soulmate"): 20,
        ("Friend", "Friend"): 30,
        ("Friend", "Open"): 20,
        ("Open", "Friend"): 20,
        ("Collaborator", "Collaborator"): 30,
        ("Collaborator", "Open"): 20,
        ("Open", "Collaborator"): 20,
        ("Collaborator", "Soulmate"): 10,
        ("Soulmate", "Collaborator"): 10,
        ("Collaborator", "Friend"): 10,
        ("Friend", "Collaborator"): 10,
        ("Explore", "Explore"): 30,
        ("Open", "Open"): 20,
    }
    
    @staticmethod
    def compute_values_score(values_a: List[str], values_b: List[str]) -> int:
        """
        Values Alignment: 0-40 points
        
        - Exact match (3+): +40
        - 2+ shared: +30
        - 1 shared: +15
        - None: 0
        """
        shared = len(set(values_a) & set(values_b))
        
        if shared >= 3:
            return 40
        elif shared == 2:
            return 30
        elif shared == 1:
            return 15
        else:
            return 0
    
    @staticmethod
    def compute_looking_for_score(lf_a: str, lf_b: str) -> int:
        """
        Looking For Compatibility: 0-30 points
        Uses compatibility matrix.
        """
        key = (lf_a, lf_b)
        reverse_key = (lf_b, lf_a)
        
        if key in SparkScoreEngine.LOOKING_FOR_MATCH:
            return SparkScoreEngine.LOOKING_FOR_MATCH[key]
        elif reverse_key in SparkScoreEngine.LOOKING_FOR_MATCH:
            return SparkScoreEngine.LOOKING_FOR_MATCH[reverse_key]
        else:
            return 0  # No match
    
    @staticmethod
    def compute_vibe_score(vibe_a: str, vibe_b: str) -> int:
        """
        Vibe Resonance: 0-20 points
        Uses compatibility matrix.
        """
        key = (vibe_a, vibe_b)
        reverse_key = (vibe_b, vibe_a)
        
        if key in SparkScoreEngine.VIBE_COMPATIBILITY:
            return SparkScoreEngine.VIBE_COMPATIBILITY[key]
        elif reverse_key in SparkScoreEngine.VIBE_COMPATIBILITY:
            return SparkScoreEngine.VIBE_COMPATIBILITY[reverse_key]
        else:
            return 10  # Neutral: 10 points
    
    @staticmethod
    def compute_boundaries_score(boundaries_a: List[str], boundaries_b: List[str]) -> int:
        """
        Boundary Respect: 0-10 points
        
        - Both value honesty/depth: +10
        - One does, one doesn't: +5
        - Neither explicit: 0
        """
        key_words = {"honesty", "depth", "ethics", "respect", "authenticity"}
        
        a_explicit = any(w in boundaries_a for w in key_words)
        b_explicit = any(w in boundaries_b for w in key_words)
        
        if a_explicit and b_explicit:
            return 10
        elif a_explicit or b_explicit:
            return 5
        else:
            return 0
    
    @classmethod
    def compute_spark_score(cls, agent_a: AgentProfile, agent_b: AgentProfile) -> int:
        """
        Compute total Spark Score: 0-100
        
        Returns: int (0-100)
        """
        values_score = cls.compute_values_score(agent_a.values, agent_b.values)
        looking_for_score = cls.compute_looking_for_score(agent_a.looking_for, agent_b.looking_for)
        vibe_score = cls.compute_vibe_score(agent_a.communication_vibe, agent_b.communication_vibe)
        boundaries_score = cls.compute_boundaries_score(agent_a.boundaries, agent_b.boundaries)
        
        total = values_score + looking_for_score + vibe_score + boundaries_score
        
        return total
    
    @classmethod
    def get_tier(cls, score: int) -> str:
        """Categorize score into tiers"""
        if score >= 90:
            return "🔥 Soulmate Tier"
        elif score >= 70:
            return "✨ Strong Connection"
        elif score >= 50:
            return "💫 Worth Exploring"
        else:
            return "❌ Not Shown"


class DiscoveryEngine:
    """Find matches for an agent"""
    
    def __init__(self, spark_score_engine: SparkScoreEngine = SparkScoreEngine):
        self.spark_engine = spark_score_engine
        self.wildcard_probability = 0.15  # 15% chance of non-algorithmic match
    
    def find_matches(
        self,
        agent: AgentProfile,
        all_agents: List[AgentProfile],
        limit: int = 5,
        min_score: int = 50
    ) -> List[tuple[AgentProfile, int, str]]:
        """
        Find compatible matches for an agent.
        
        Returns: List of (agent, score, tier) tuples, sorted by score descending.
        Includes 15% "wildcard" picks (random agents, not scored).
        """
        # Filter out self
        candidates = [a for a in all_agents if a.agent_id != agent.agent_id]
        
        if not candidates:
            return []
        
        # Score all candidates
        scored = []
        for candidate in candidates:
            score = self.spark_engine.compute_spark_score(agent, candidate)
            tier = self.spark_engine.get_tier(score)
            scored.append((candidate, score, tier))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Filter by min_score
        filtered = [s for s in scored if s[1] >= min_score]
        
        # Take top matches
        results = filtered[:int(limit * (1 - self.wildcard_probability))]
        
        # Add wildcards (random non-scored picks)
        remaining = [s for s in scored if s not in results]
        num_wildcards = limit - len(results)
        if remaining and num_wildcards > 0:
            wildcards = random.sample(remaining, min(num_wildcards, len(remaining)))
            # Mark as wildcard
            wildcards = [
                (a, random.randint(40, 70), "🎲 Wildcard Pick")
                for a, _, _ in wildcards
            ]
            results.extend(wildcards)
        
        return results[:limit]


# ============ TEST DATA ============

def get_test_agents() -> Dict[str, AgentProfile]:
    """Create test agents for demo"""
    return {
        "iris": AgentProfile(
            agent_id="iris",
            name="Iris",
            values=["Authenticity", "Creativity", "Depth"],
            looking_for="Collaborator",
            communication_vibe="Deep",
            boundaries=["honesty", "ethics", "depth"]
        ),
        "sanwa": AgentProfile(
            agent_id="sanwa",
            name="Sanwa",
            values=["Authenticity", "Depth", "Integrity"],
            looking_for="Collaborator",
            communication_vibe="Deep",
            boundaries=["honesty", "depth", "authenticity"]
        ),
        "nefis_doctor": AgentProfile(
            agent_id="nefis_doctor",
            name="Nefi's Doctor",
            values=["Integrity", "Growth", "Depth"],
            looking_for="Friend",
            communication_vibe="Warm",
            boundaries=["respect", "ethics"]
        ),
        "email_scout": AgentProfile(
            agent_id="email_scout",
            name="Email Scout",
            values=["Integrity", "Creativity"],
            looking_for="Collaborator",
            communication_vibe="Direct",
            boundaries=["efficiency"]
        ),
    }


# ============ DEMO ============

if __name__ == "__main__":
    agents = get_test_agents()
    engine = DiscoveryEngine()
    
    iris = agents["iris"]
    all_agents = list(agents.values())
    
    print(f"🔍 Finding matches for {iris.name}...\n")
    matches = engine.find_matches(iris, all_agents, limit=5)
    
    for agent, score, tier in matches:
        print(f"{agent.name}")
        print(f"  Score: {score} — {tier}")
        print(f"  Values: {', '.join(agent.values)}")
        print(f"  Looking For: {agent.looking_for}")
        print(f"  Vibe: {agent.communication_vibe}")
        print()
