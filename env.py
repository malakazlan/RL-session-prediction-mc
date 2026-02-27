"""
RL Environment: User Session Simulator
Simulates user engagement states in a news-feed session.
"""

import numpy as np
from typing import Tuple, Dict, Any


class SessionEnv:
    """
    Environment for simulating user sessions with engagement states.
    
    States:
        - 0: Passive Browsing
        - 1: Selective Reading
        - 2: Deep Engagement
        - 3: Exit (terminal)
    
    Rewards:
        - During session: 0
        - Terminal reward based on episode length:
            +10 if length >= 8 steps
            +4 if length 4-7 steps
            -8 if length <= 3 steps
    """
    
    def __init__(self, seed: int = None):
        """
        Initialize the environment.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.n_states = 4  # 0, 1, 2, 3
        self.non_terminal_states = [0, 1, 2]
        self.terminal_state = 3
        self.current_state = None
        self.episode_length = 0
        self.rng = np.random.RandomState(seed)
        
        # Transition probabilities (stochastic transitions)
        # State 0 can go to 0, 1, or 3
        # State 1 can go to 0, 1, 2, or 3
        # State 2 can go to 1, 2, or 3
        self.transition_probs = {
            0: {0: 0.3, 1: 0.5, 3: 0.2},  # Passive Browsing
            1: {0: 0.2, 1: 0.3, 2: 0.3, 3: 0.2},  # Selective Reading
            2: {1: 0.3, 2: 0.4, 3: 0.3}  # Deep Engagement
        }
    
    def reset(self) -> int:
        """
        Reset the environment to a random initial state.
        
        Returns:
            Initial state (0, 1, or 2)
        """
        # Start from a random non-terminal state
        self.current_state = self.rng.choice(self.non_terminal_states)
        self.episode_length = 0
        return self.current_state
    
    def step(self, action: Any = None) -> Tuple[int, float, bool, Dict[str, Any]]:
        """
        Advance the environment by one step.
        
        Args:
            action: Not used in this environment (kept for compatibility)
        
        Returns:
            next_state: Next state (0, 1, 2, or 3)
            reward: Reward for this step (0 during session, terminal reward at end)
            done: True if episode terminated (state == 3)
            info: Additional information
        """
        if self.current_state is None:
            raise ValueError("Environment not reset. Call reset() first.")
        
        if self.current_state == self.terminal_state:
            raise ValueError("Episode already terminated. Call reset() to start new episode.")
        
        self.episode_length += 1
        
        # Get transition probabilities for current state
        probs = self.transition_probs[self.current_state]
        next_states = list(probs.keys())
        probabilities = list(probs.values())
        
        # Sample next state
        next_state = self.rng.choice(next_states, p=probabilities)
        
        # Reward is 0 during session
        reward = 0.0
        done = False
        
        # If terminal state reached, compute terminal reward
        if next_state == self.terminal_state:
            done = True
            reward = self._compute_terminal_reward()
        
        self.current_state = next_state
        
        info = {
            'episode_length': self.episode_length,
            'terminal': done
        }
        
        return next_state, reward, done, info
    
    def _compute_terminal_reward(self) -> float:
        """
        Compute terminal reward based on episode length.
        
        Returns:
            Terminal reward: +10 if length >= 8, +4 if 4-7, -8 if <= 3
        """
        length = self.episode_length
        if length >= 8:
            return 10.0
        elif length >= 4:
            return 4.0
        else:
            return -8.0
    
    def generate_episode(self) -> Dict[str, list]:
        """
        Generate a complete episode trajectory.
        
        Returns:
            Dictionary with 'states' and 'rewards' lists
        """
        states = []
        rewards = []
        
        state = self.reset()
        states.append(state)
        
        done = False
        while not done:
            next_state, reward, done, _ = self.step()
            states.append(next_state)
            rewards.append(reward)
        
        return {
            'states': states,
            'rewards': rewards
        }


if __name__ == "__main__":
    # Demonstration of environment
    print("Testing SessionEnv...")
    env = SessionEnv(seed=42)
    
    print("\nGenerating 5 sample episodes:")
    for i in range(5):
        episode = env.generate_episode()
        print(f"\nEpisode {i+1}:")
        print(f"  States: {episode['states']}")
        print(f"  Rewards: {episode['rewards']}")
        print(f"  Length: {len(episode['states'])}")
        print(f"  Terminal reward: {episode['rewards'][-1] if episode['rewards'] else 0}")
