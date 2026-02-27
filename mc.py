"""
First-Visit Monte Carlo Policy Evaluation
Estimates state-value function V(s) from episodic trajectories.
"""

import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict


class FirstVisitMC:
    """
    First-Visit Monte Carlo method for policy evaluation.
    
    For each state, only the first occurrence in an episode is used
    to update the value estimate.
    """
    
    def __init__(self, states: List[int], gamma: float = 0.9):
        """
        Initialize Monte Carlo evaluator.
        
        Args:
            states: List of non-terminal states to evaluate
            gamma: Discount factor (default: 0.9)
        """
        self.states = states
        self.gamma = gamma
        
        # Value function: V(s) for each state
        self.V = {s: 0.0 for s in states}
        
        # Returns for each state (list of all returns seen so far)
        self.returns = {s: [] for s in states}
        
        # Track convergence history
        self.history = {s: [] for s in states}
    
    def compute_returns(self, rewards: List[float]) -> List[float]:
        """
        Compute returns G_t for each time step using discount factor.
        
        Args:
            rewards: List of rewards [r_1, r_2, ..., r_T]
        
        Returns:
            List of returns [G_0, G_1, ..., G_{T-1}]
        """
        T = len(rewards)
        returns = [0.0] * T
        
        # Compute returns backwards
        G = 0.0
        for t in reversed(range(T)):
            G = rewards[t] + self.gamma * G
            returns[t] = G
        
        return returns
    
    def update(self, episode: Dict[str, list]) -> None:
        """
        Update value estimates using first-visit Monte Carlo.
        
        Args:
            episode: Dictionary with 'states' and 'rewards' keys
        """
        states = episode['states']
        rewards = episode['rewards']
        
        # Compute returns for all time steps
        returns = self.compute_returns(rewards)
        
        # Track first visit of each state in this episode
        first_visit = {s: True for s in self.states}
        
        # Update value estimates using first-visit rule
        for t in range(len(states) - 1):  # Exclude terminal state
            s_t = states[t]
            
            # Only update if this is the first visit to state s_t in this episode
            if s_t in self.states and first_visit[s_t]:
                G_t = returns[t]
                
                # Append return to returns list for this state
                self.returns[s_t].append(G_t)
                
                # Update value estimate as mean of all returns
                self.V[s_t] = np.mean(self.returns[s_t])
                
                # Mark this state as visited
                first_visit[s_t] = False
    
    def evaluate(self, episodes: List[Dict[str, list]], track_history: bool = True) -> Dict[int, float]:
        """
        Evaluate policy using multiple episodes.
        
        Args:
            episodes: List of episode dictionaries
            track_history: If True, track V(s) after each episode
        
        Returns:
            Dictionary mapping states to final value estimates
        """
        # Reset if needed
        if track_history:
            self.history = {s: [] for s in self.states}
        
        for i, episode in enumerate(episodes):
            # Update value estimates
            self.update(episode)
            
            # Track history for convergence plot
            if track_history:
                for s in self.states:
                    self.history[s].append(self.V[s])
        
        return self.V.copy()
    
    def get_history(self) -> Dict[int, List[float]]:
        """
        Get convergence history.
        
        Returns:
            Dictionary mapping states to lists of value estimates over episodes
        """
        return self.history.copy()
    
    def get_returns(self) -> Dict[int, List[float]]:
        """
        Get all returns collected for each state.
        
        Returns:
            Dictionary mapping states to lists of returns
        """
        return self.returns.copy()


if __name__ == "__main__":
    # Simple test
    from env import SessionEnv
    
    print("Testing First-Visit Monte Carlo...")
    
    env = SessionEnv(seed=42)
    mc = FirstVisitMC(states=[0, 1, 2], gamma=0.9)
    
    # Generate a few episodes
    episodes = [env.generate_episode() for _ in range(10)]
    
    # Evaluate
    V = mc.evaluate(episodes)
    
    print("\nValue estimates after 10 episodes:")
    for s in [0, 1, 2]:
        print(f"  V({s}) = {V[s]:.4f}")
