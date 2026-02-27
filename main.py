"""
Main script for Monte Carlo Policy Evaluation on User Sessions
"""

import numpy as np
from env import SessionEnv
from mc import FirstVisitMC
from utils import (
    plot_convergence,
    plot_episode_length_distribution,
    plot_terminal_reward_distribution,
    print_value_table,
    analyze_state_visits
)


def generate_trajectories(env: SessionEnv, n_episodes: int = 2000, seed: int = 42) -> list:
    """
    Generate episodic trajectories.
    
    Args:
        env: SessionEnv instance
        n_episodes: Number of episodes to generate
        seed: Random seed
    
    Returns:
        List of episode dictionaries
    """
    print(f"Generating {n_episodes} episodes...")
    episodes = []
    
    for i in range(n_episodes):
        episode = env.generate_episode()
        episodes.append(episode)
        
        if (i + 1) % 500 == 0:
            print(f"  Generated {i + 1} episodes...")
    
    print(f"[OK] Generated {len(episodes)} episodes")
    return episodes


def main():
    """
    Main execution function.
    """
    print("="*70)
    print("Monte Carlo Policy Evaluation on User Sessions")
    print("="*70)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Initialize environment
    print("\n[Step 1] Initializing environment...")
    env = SessionEnv(seed=42)
    print("[OK] Environment initialized")
    
    # Generate trajectories
    print("\n[Step 2] Generating trajectories...")
    n_episodes = 2000  # Use 2000 for strong results
    episodes = generate_trajectories(env, n_episodes=n_episodes, seed=42)
    
    # Analyze episode statistics
    print("\n[Step 3] Analyzing episode statistics...")
    lengths = [len(ep['states']) for ep in episodes]
    terminal_rewards = [ep['rewards'][-1] if ep['rewards'] else 0 for ep in episodes]
    
    print(f"  Episode length statistics:")
    print(f"    Mean: {np.mean(lengths):.2f}")
    print(f"    Min: {min(lengths)}")
    print(f"    Max: {max(lengths)}")
    print(f"    Std: {np.std(lengths):.2f}")
    
    print(f"\n  Terminal reward distribution:")
    print(f"    +10 (length >= 8): {sum(1 for r in terminal_rewards if r == 10)} episodes")
    print(f"    +4 (length 4-7): {sum(1 for r in terminal_rewards if r == 4)} episodes")
    print(f"    -8 (length <= 3): {sum(1 for r in terminal_rewards if r == -8)} episodes")
    
    # Initialize Monte Carlo evaluator
    print("\n[Step 4] Initializing First-Visit Monte Carlo evaluator...")
    mc = FirstVisitMC(states=[0, 1, 2], gamma=0.9)
    print("[OK] MC evaluator initialized (gamma=0.9)")
    
    # Run Monte Carlo evaluation
    print("\n[Step 5] Running First-Visit Monte Carlo evaluation...")
    V = mc.evaluate(episodes, track_history=True)
    print("[OK] MC evaluation completed")
    
    # Print results
    print("\n[Step 6] Results:")
    print_value_table(V)
    
    # Get convergence history
    history = mc.get_history()
    
    # Analyze which states lead to better outcomes
    print("\n[Step 7] State analysis:")
    state_stats = analyze_state_visits(episodes)
    state_names = {0: "Passive Browsing", 1: "Selective Reading", 2: "Deep Engagement"}
    
    print(f"\n{'State':<20} {'Name':<25} {'Avg Return':<15} {'Episodes':<10}")
    print("-"*70)
    for s in [0, 1, 2]:
        print(f"{s:<20} {state_names[s]:<25} {state_stats[s]['avg_return']:>10.4f} {state_stats[s]['episodes']:>10}")
    
    # Generate plots
    print("\n[Step 8] Generating plots...")
    plot_convergence(history, save_path="convergence_plot.png")
    plot_episode_length_distribution(episodes, save_path="episode_lengths.png")
    plot_terminal_reward_distribution(episodes, save_path="terminal_rewards.png")
    print("[OK] All plots generated")
    
    # Discussion points
    print("\n" + "="*70)
    print("Key Observations:")
    print("="*70)
    print("1. State values reflect expected returns from each state.")
    print("2. Higher values indicate states that lead to longer, more rewarding sessions.")
    print("3. The convergence plot shows how estimates stabilize with more episodes.")
    print("4. First-Visit MC only uses the first occurrence of each state per episode.")
    print("\nSee report.pdf for detailed analysis and MC vs DP comparison.")
    print("="*70)


if __name__ == "__main__":
    main()
