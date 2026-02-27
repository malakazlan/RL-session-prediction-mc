"""
Utility functions for plotting and analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List


def plot_convergence(history: Dict[int, List[float]], save_path: str = "convergence_plot.png"):
    """
    Plot convergence of value estimates over episodes.
    
    Args:
        history: Dictionary mapping states to lists of value estimates
        save_path: Path to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    state_names = {0: "Passive Browsing", 1: "Selective Reading", 2: "Deep Engagement"}
    colors = {0: 'blue', 1: 'green', 2: 'red'}
    
    for state in sorted(history.keys()):
        episodes = range(1, len(history[state]) + 1)
        plt.plot(episodes, history[state], 
                label=f"V({state}) - {state_names[state]}",
                color=colors[state],
                linewidth=2,
                alpha=0.7)
    
    plt.xlabel('Number of Episodes', fontsize=12)
    plt.ylabel('Value Estimate V(s)', fontsize=12)
    plt.title('First-Visit Monte Carlo: Convergence of Value Estimates', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Convergence plot saved to {save_path}")
    plt.close()


def plot_episode_length_distribution(episodes: List[Dict[str, list]], save_path: str = "episode_lengths.png"):
    """
    Plot distribution of episode lengths.
    
    Args:
        episodes: List of episode dictionaries
        save_path: Path to save the plot
    """
    lengths = [len(ep['states']) for ep in episodes]
    
    plt.figure(figsize=(10, 6))
    plt.hist(lengths, bins=range(1, max(lengths) + 2), edgecolor='black', alpha=0.7)
    plt.xlabel('Episode Length', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Episode Lengths', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Episode length distribution plot saved to {save_path}")
    plt.close()


def plot_terminal_reward_distribution(episodes: List[Dict[str, list]], save_path: str = "terminal_rewards.png"):
    """
    Plot distribution of terminal rewards.
    
    Args:
        episodes: List of episode dictionaries
        save_path: Path to save the plot
    """
    terminal_rewards = []
    for ep in episodes:
        if ep['rewards']:
            terminal_rewards.append(ep['rewards'][-1])
    
    plt.figure(figsize=(10, 6))
    plt.hist(terminal_rewards, bins=[-10, -5, 0, 5, 10, 15], edgecolor='black', alpha=0.7)
    plt.xlabel('Terminal Reward', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Terminal Rewards', fontsize=14, fontweight='bold')
    plt.xticks([-8, 4, 10])
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Terminal reward distribution plot saved to {save_path}")
    plt.close()


def print_value_table(V: Dict[int, float]):
    """
    Print value estimates in a formatted table.
    
    Args:
        V: Dictionary mapping states to value estimates
    """
    state_names = {0: "Passive Browsing", 1: "Selective Reading", 2: "Deep Engagement"}
    
    print("\n" + "="*60)
    print("Final Value Estimates V(s)")
    print("="*60)
    print(f"{'State':<20} {'State Name':<25} {'V(s)':<15}")
    print("-"*60)
    
    for s in sorted(V.keys()):
        print(f"{s:<20} {state_names[s]:<25} {V[s]:>10.4f}")
    
    print("="*60)


def analyze_state_visits(episodes: List[Dict[str, list]]) -> Dict[int, Dict[str, float]]:
    """
    Analyze which states lead to better outcomes.
    
    Args:
        episodes: List of episode dictionaries
    
    Returns:
        Dictionary with statistics for each state
    """
    state_stats = {0: {'visits': 0, 'total_return': 0.0, 'episodes': 0},
                   1: {'visits': 0, 'total_return': 0.0, 'episodes': 0},
                   2: {'visits': 0, 'total_return': 0.0, 'episodes': 0}}
    
    for episode in episodes:
        states = episode['states']
        rewards = episode['rewards']
        
        # Compute returns
        returns = compute_returns(rewards, gamma=0.9)
        
        # Track first visits
        first_visit = {0: True, 1: True, 2: True}
        
        for t in range(len(states) - 1):
            s_t = states[t]
            if s_t in [0, 1, 2] and first_visit[s_t]:
                state_stats[s_t]['visits'] += 1
                state_stats[s_t]['total_return'] += returns[t]
                state_stats[s_t]['episodes'] += 1
                first_visit[s_t] = False
    
    # Compute averages
    for s in state_stats:
        if state_stats[s]['episodes'] > 0:
            state_stats[s]['avg_return'] = state_stats[s]['total_return'] / state_stats[s]['episodes']
        else:
            state_stats[s]['avg_return'] = 0.0
    
    return state_stats


def compute_returns(rewards: List[float], gamma: float = 0.9) -> List[float]:
    """
    Compute returns G_t for each time step.
    
    Args:
        rewards: List of rewards
        gamma: Discount factor
    
    Returns:
        List of returns
    """
    T = len(rewards)
    returns = [0.0] * T
    G = 0.0
    
    for t in reversed(range(T)):
        G = rewards[t] + gamma * G
        returns[t] = G
    
    return returns
