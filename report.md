# Monte Carlo Policy Evaluation on User Sessions

**RL Project Submission - 9th Jan 2026**

---

## 1. Problem Formulation

### 1.1 States

We model user engagement in a news-feed session using four discrete states:

- **State 0: Passive Browsing** - User is casually browsing without deep engagement
- **State 1: Selective Reading** - User is actively selecting and reading content
- **State 2: Deep Engagement** - User is highly engaged with the content
- **State 3: Exit** - Terminal state indicating the end of the session

### 1.2 Episode Termination

An episode (user session) terminates when the user reaches the Exit state (state 3). Each episode represents one complete user session from initial browsing to exit.

### 1.3 Reward Design

The reward structure is **delayed and sparse**, which is realistic for user engagement scenarios:

- **During the session**: All intermediate rewards are **zero** (r_t = 0 for all non-terminal steps)
- **Terminal reward** (received only when state becomes Exit):
  - **+10** if session length ≥ 8 steps (long, engaged session)
  - **+4** if session length is 4-7 steps (moderate session)
  - **-8** if session length ≤ 3 steps (short, disengaged session)

This design encourages longer, more engaged sessions while penalizing quick exits.

### 1.4 Discount Factor

We use a discount factor **γ = 0.9**, which balances immediate and future rewards appropriately for this episodic task.

### 1.5 Transition Model

The environment uses stochastic transitions:
- State 0 (Passive Browsing) can transition to states 0, 1, or 3
- State 1 (Selective Reading) can transition to states 0, 1, 2, or 3
- State 2 (Deep Engagement) can transition to states 1, 2, or 3

Transition probabilities are designed to reflect realistic user behavior patterns.

---

## 2. First-Visit Monte Carlo Algorithm

### 2.1 Algorithm Explanation

First-Visit Monte Carlo is a model-free method that estimates the state-value function V(s) by learning from actual experience (episodic trajectories). Unlike Dynamic Programming, it does not require knowledge of transition probabilities.

**Key characteristics:**
- **Model-free**: No need for transition probabilities P(s'|s,a) or reward function R(s,a)
- **Learning from experience**: Uses actual episode trajectories
- **First-visit rule**: Each state is updated at most once per episode (using its first occurrence)

### 2.2 Algorithm Steps

1. **Initialization**: Set V(s) = 0 for all states s ∈ {0, 1, 2}
2. **Initialize returns**: Create empty lists returns[s] for each state
3. **For each episode**:
   - Generate trajectory: (s_0, r_1, s_1, r_2, ..., s_{T-1}, r_T, s_T)
   - Compute returns G_t backwards from terminal reward:
     - G_{T-1} = r_T (terminal reward)
     - G_t = r_{t+1} + γ·G_{t+1} for t = T-2, T-3, ..., 0
   - Track first visit: For each state s_t in the episode:
     - If this is the **first occurrence** of s_t in the episode:
       - Append G_t to returns[s_t]
       - Update V(s_t) = mean(returns[s_t])

### 2.3 Implementation Details

Our implementation:
- Generates 2000 episodes for robust estimates
- Correctly computes returns using discount factor γ = 0.9
- Enforces first-visit rule (each state updated once per episode)
- Tracks convergence history for visualization

---

## 3. Results

### 3.1 Final Value Estimates

After processing 2000 episodes, we obtain the following value estimates:

| State | State Name | V(s) |
|-------|------------|------|
| 0 | Passive Browsing | -0.3230 |
| 1 | Selective Reading | -0.6120 |
| 2 | Deep Engagement | -0.7408 |

### 3.2 Interpretation

**State 0 (Passive Browsing) has the highest value** (-0.3230), followed by State 1 (-0.6120), and State 2 (-0.7408) has the lowest value.

This result may seem counterintuitive at first, but it reflects the **transition dynamics** of our environment:
- State 0 has a higher probability of transitioning to Exit (0.2), which can lead to shorter episodes
- However, State 0 also has paths that can lead to longer sessions
- The negative values indicate that, on average, sessions starting from these states tend to result in negative or low positive returns due to the high frequency of short sessions (≤3 steps) that receive -8 reward

**Key insight**: The value function V(s) represents the **expected return** from state s under the current policy (implicit in the transition probabilities). Since many episodes are short (receiving -8 reward), the expected returns are negative.

### 3.3 Convergence Analysis

The convergence plot (see `convergence_plot.png`) shows:
- Value estimates stabilize after approximately 500-1000 episodes
- All three states converge to stable values
- Some variance remains due to the stochastic nature of the environment

### 3.4 Episode Statistics

From 2000 episodes:
- **Mean episode length**: 5.41 steps
- **Episode length range**: 2 to 27 steps
- **Terminal reward distribution**:
  - +10 (length ≥ 8): 328 episodes (16.4%)
  - +4 (length 4-7): 637 episodes (31.85%)
  - -8 (length ≤ 3): 1035 episodes (51.75%)

The high proportion of short episodes (51.75%) explains the negative value estimates.

---

## 4. Monte Carlo vs Dynamic Programming

### 4.1 Monte Carlo (Implemented)

**Advantages:**
- **Model-free**: No need for transition probabilities or reward models
- **Works with actual experience**: Learns from real trajectories
- **Handles delayed rewards**: Naturally handles sparse, terminal rewards
- **Suitable for episodic tasks**: Perfect for session-based scenarios

**Disadvantages:**
- **Requires many episodes**: Needs sufficient data to converge
- **Slower convergence**: May need thousands of episodes
- **Only for episodic tasks**: Requires episodes to terminate
- **High variance**: Estimates can be noisy, especially early in learning

### 4.2 Dynamic Programming

**Advantages:**
- **Fast convergence**: Iterative updates converge quickly
- **Exact values**: Computes true value function (given model)
- **Low variance**: Deterministic updates
- **Works for continuing tasks**: Not limited to episodic scenarios

**Disadvantages:**
- **Requires complete model**: Needs P(s'|s,a) and R(s,a)
- **Not always available**: In real systems, transition probabilities may be unknown
- **Computational cost**: Can be expensive for large state spaces
- **Model accuracy**: Results depend on model correctness

### 4.3 When to Use Each

- **Use Monte Carlo** when:
  - Transition probabilities are unknown
  - You have access to historical data/trajectories
  - Episodic tasks with terminal rewards
  - Model is complex or difficult to specify

- **Use Dynamic Programming** when:
  - Complete model is available and accurate
  - Fast convergence is critical
  - State space is manageable
  - You need exact value estimates

### 4.4 For Real-Time Systems

In real-time user session systems:
- **MC is more practical**: Can learn from logged user sessions without modeling
- **DP requires modeling**: Would need to estimate transition probabilities first
- **MC adapts**: Can update as user behavior changes
- **DP is faster**: But requires model maintenance

---

## 5. Limitations and Real-Time Considerations

### 5.1 Limitations of Monte Carlo

1. **Sample Efficiency**: Requires many episodes (2000+ for reliable estimates)
2. **Episodic Requirement**: Only works when episodes terminate
3. **Delayed Updates**: Must wait for episode completion
4. **High Variance**: Early estimates can be very noisy
5. **No Online Learning**: Cannot update during an episode

### 5.2 Real-Time System Challenges

**For real-time user session systems:**

1. **Cold Start Problem**: 
   - New users/states have no data
   - Need sufficient episodes before reliable estimates
   - Solution: Use prior estimates or default values

2. **Non-Stationary Environment**:
   - User behavior changes over time
   - Seasonal patterns, trends
   - Solution: Use sliding window or decayed averages

3. **Computational Cost**:
   - Processing thousands of episodes
   - Storage of returns for each state
   - Solution: Batch processing, approximate methods

4. **Delayed Feedback**:
   - Must wait for session completion
   - Cannot make real-time decisions during session
   - Solution: Combine with online methods (TD learning)

5. **Sparse Data**:
   - Some states may be rarely visited
   - Unreliable estimates for rare states
   - Solution: State aggregation, function approximation

### 5.3 Recommendations for Production

1. **Hybrid Approach**: Combine MC with Temporal Difference (TD) learning
2. **Function Approximation**: Use neural networks for large state spaces
3. **Incremental Updates**: Update estimates incrementally, not batch
4. **Exploration**: Ensure sufficient exploration of all states
5. **Monitoring**: Track convergence and estimate quality

---

## 6. Conclusion

This project successfully implements First-Visit Monte Carlo Policy Evaluation for a user session environment. Key achievements:

- ✅ Correct implementation of first-visit MC algorithm
- ✅ Proper handling of delayed, sparse rewards
- ✅ Convergence analysis with 2000 episodes
- ✅ Clear visualization of results

The results demonstrate that MC can effectively learn value functions from experience without requiring a model, making it suitable for real-world applications where transition probabilities are unknown. However, the method requires sufficient data and may not be ideal for real-time decision-making during episodes.

**Future Work:**
- Implement Temporal Difference (TD) learning for online updates
- Add function approximation for larger state spaces
- Compare with other model-free methods (SARSA, Q-learning)
- Extend to policy improvement (policy iteration)

---

## References

- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
- First-Visit Monte Carlo Method for Policy Evaluation

---

**End of Report**
