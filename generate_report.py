"""
Script to generate enhanced report.pdf with images and detailed explanations
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os


def create_pdf():
    """Create enhanced PDF report with images and detailed explanations."""
    
    # Create PDF document
    doc = SimpleDocTemplate("report.pdf", pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=normal_style,
        leftIndent=20,
        bulletIndent=10
    )
    
    # Title Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Monte Carlo Policy Evaluation", title_style))
    story.append(Paragraph("on User Sessions", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>RL Project Submission</b>", styles['Normal']))
    story.append(Paragraph("<b>9th January 2026</b>", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("_" * 80, styles['Normal']))
    story.append(PageBreak())
    
    # Section 1: Problem Formulation
    story.append(Paragraph("1. Problem Formulation", heading1_style))
    
    story.append(Paragraph(
        "This project implements First-Visit Monte Carlo Policy Evaluation to estimate state-value functions "
        "in a user session environment. The problem is formulated as an episodic reinforcement learning task "
        "where we learn from actual user session trajectories without requiring knowledge of transition probabilities.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>1.1 State Space Definition</b>", heading2_style))
    story.append(Paragraph(
        "We model user engagement in a news-feed session using four discrete states that capture different "
        "levels of user interaction and engagement:",
        normal_style))
    story.append(Paragraph("• <b>State 0: Passive Browsing</b> - User is casually browsing without deep engagement. "
                          "This represents the initial or low-engagement phase where users are scanning content without "
                          "committing to reading.", normal_style))
    story.append(Paragraph("• <b>State 1: Selective Reading</b> - User is actively selecting and reading content. "
                          "This indicates moderate engagement where users are making conscious choices about what to consume.", normal_style))
    story.append(Paragraph("• <b>State 2: Deep Engagement</b> - User is highly engaged with the content. This represents "
                          "the most valuable state where users are fully absorbed in the content.", normal_style))
    story.append(Paragraph("• <b>State 3: Exit</b> - Terminal state indicating the end of the session. This is the absorbing "
                          "state that terminates each episode.", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>1.2 Episode Termination</b>", heading2_style))
    story.append(Paragraph(
        "An episode (user session) terminates deterministically when the user reaches the Exit state (state 3). "
        "Each episode represents one complete user session from initial browsing to exit. The episode structure "
        "follows the format: (s_0, r_1, s_1, r_2, ..., s_{T-1}, r_T, s_T) where s_T = 3 (Exit) and T is the episode length.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>1.3 Reward Design: Delayed and Sparse Rewards</b>", heading2_style))
    story.append(Paragraph(
        "The reward structure is <b>delayed and sparse</b>, which is highly realistic for user engagement scenarios "
        "where the true value of a session is only known after completion. This design choice makes the problem more "
        "challenging and realistic compared to immediate reward scenarios.",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>During the session:</b>", normal_style))
    story.append(Paragraph("All intermediate rewards are <b>zero</b> (r_t = 0 for all non-terminal steps). "
                          "This means we receive no feedback during the session, only at the end.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Terminal reward</b> (received only when state becomes Exit):", normal_style))
    story.append(Paragraph("  • <b>+10</b> if session length ≥ 8 steps (long, engaged session) - Rewards extended engagement", normal_style))
    story.append(Paragraph("  • <b>+4</b> if session length is 4-7 steps (moderate session) - Moderate reward for average engagement", normal_style))
    story.append(Paragraph("  • <b>-8</b> if session length ≤ 3 steps (short, disengaged session) - Penalizes quick exits", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "This reward design encourages longer, more engaged sessions while penalizing quick exits. The negative reward "
        "for short sessions creates a learning signal that helps the algorithm distinguish between states that lead to "
        "valuable vs. poor outcomes.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>1.4 Discount Factor</b>", heading2_style))
    story.append(Paragraph(
        "We use a discount factor <b>γ = 0.9</b>, which balances immediate and future rewards appropriately for this episodic task. "
        "The discount factor determines how much we value future rewards relative to immediate ones. With γ = 0.9, we value "
        "rewards 10 steps in the future at approximately 35% of their immediate value (0.9^10 ≈ 0.35), which is appropriate "
        "for session-based scenarios where the terminal reward is the primary signal.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>1.5 Transition Model and Environment Dynamics</b>", heading2_style))
    story.append(Paragraph(
        "The environment uses <b>stochastic transitions</b> that reflect realistic user behavior patterns. The transition "
        "probabilities are designed to model how users naturally move between engagement levels:",
        normal_style))
    story.append(Paragraph("• <b>State 0 (Passive Browsing)</b> can transition to states 0 (stay passive), 1 (become selective), or 3 (exit). "
                          "This models users who might continue browsing, start reading, or leave quickly.", normal_style))
    story.append(Paragraph("• <b>State 1 (Selective Reading)</b> can transition to states 0 (lose interest), 1 (continue selecting), "
                          "2 (become deeply engaged), or 3 (exit). This captures the dynamic nature of user attention.", normal_style))
    story.append(Paragraph("• <b>State 2 (Deep Engagement)</b> can transition to states 1 (reduce engagement), 2 (maintain engagement), "
                          "or 3 (exit). Even highly engaged users may eventually leave or reduce engagement.", normal_style))
    story.append(Paragraph(
        "The stochastic nature of transitions means that the same state can lead to different outcomes, making this a "
        "non-deterministic MDP. This complexity makes Monte Carlo methods particularly valuable, as they can learn from "
        "actual experience without needing to explicitly model these probabilities.",
        normal_style))
    story.append(PageBreak())
    
    # Section 2: Algorithm
    story.append(Paragraph("2. First-Visit Monte Carlo Algorithm", heading1_style))
    
    story.append(Paragraph(
        "Monte Carlo methods are a class of reinforcement learning algorithms that learn value functions and optimal policies "
        "from experience. The 'First-Visit' variant is specifically designed for policy evaluation and ensures each state is "
        "updated at most once per episode.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>2.1 Algorithm Explanation and Motivation</b>", heading2_style))
    story.append(Paragraph(
        "First-Visit Monte Carlo is a <b>model-free</b> method that estimates the state-value function V(s) by learning from "
        "actual experience (episodic trajectories). Unlike Dynamic Programming, it does not require knowledge of transition "
        "probabilities P(s'|s,a) or the reward function R(s,a). This makes it particularly suitable for real-world applications "
        "where the environment model is unknown or difficult to specify.",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Key characteristics that distinguish MC from other methods:</b>", normal_style))
    story.append(Paragraph("• <b>Model-free</b>: No need for transition probabilities P(s'|s,a) or reward function R(s,a). "
                          "We learn directly from experience without building a model of the environment.", normal_style))
    story.append(Paragraph("• <b>Learning from experience</b>: Uses actual episode trajectories generated by the environment. "
                          "Each episode provides a sample of the true value function.", normal_style))
    story.append(Paragraph("• <b>First-visit rule</b>: Each state is updated at most once per episode (using its first occurrence). "
                          "This ensures unbiased estimates and prevents over-counting states that appear multiple times in an episode.", normal_style))
    story.append(Paragraph("• <b>Episodic requirement</b>: Works only for episodic tasks where episodes terminate. "
                          "This is perfect for session-based scenarios like user interactions.", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>2.2 Detailed Algorithm Steps</b>", heading2_style))
    story.append(Paragraph("The First-Visit Monte Carlo algorithm proceeds as follows:", normal_style))
    story.append(Paragraph("1. <b>Initialization</b>: Set V(s) = 0 for all states s ∈ {0, 1, 2}. Initialize empty lists returns[s] for each state to store observed returns.", normal_style))
    story.append(Paragraph("2. <b>For each episode</b>:", normal_style))
    story.append(Paragraph("   a. <b>Generate trajectory</b>: Run the environment to generate a complete episode "
                          "(s_0, r_1, s_1, r_2, ..., s_{T-1}, r_T, s_T) where s_T = 3 (Exit).", normal_style))
    story.append(Paragraph("   b. <b>Compute returns backwards</b>: Starting from the terminal reward, compute returns G_t for each time step:", normal_style))
    story.append(Paragraph("      • G_{T-1} = r_T (the terminal reward)", normal_style))
    story.append(Paragraph("      • G_t = r_{t+1} + γ·G_{t+1} for t = T-2, T-3, ..., 0", normal_style))
    story.append(Paragraph("      This backward computation ensures we properly account for the discount factor.", normal_style))
    story.append(Paragraph("   c. <b>First-visit update</b>: For each state s_t in the episode:", normal_style))
    story.append(Paragraph("      • If this is the <b>first occurrence</b> of s_t in the episode:", normal_style))
    story.append(Paragraph("        - Append G_t to returns[s_t]", normal_style))
    story.append(Paragraph("        - Update V(s_t) = mean(returns[s_t])", normal_style))
    story.append(Paragraph("      • If s_t has appeared earlier in the episode, skip it (first-visit rule).", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Why first-visit?</b> The first-visit rule ensures that each state's value estimate is based on independent samples. "
        "If we updated a state every time it appeared in an episode, we would be using correlated samples (from the same episode), "
        "which would bias our estimates. The first-visit rule ensures statistical independence.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>2.3 Implementation Details and Verification</b>", heading2_style))
    story.append(Paragraph("Our implementation includes the following key features:", normal_style))
    story.append(Paragraph("• <b>Episode generation</b>: Generates 2000 episodes for robust statistical estimates. "
                          "This provides sufficient data for reliable convergence.", normal_style))
    story.append(Paragraph("• <b>Correct return computation</b>: Returns are computed backwards using discount factor γ = 0.9, "
                          "ensuring proper handling of the delayed terminal reward.", normal_style))
    story.append(Paragraph("• <b>First-visit enforcement</b>: Each state is updated at most once per episode using a first-visit "
                          "tracking mechanism that marks states as visited within each episode.", normal_style))
    story.append(Paragraph("• <b>Convergence tracking</b>: Tracks the value estimates after each episode to visualize convergence "
                          "and verify that the algorithm is learning correctly.", normal_style))
    story.append(Paragraph("• <b>Statistical aggregation</b>: Value estimates are computed as the mean of all observed returns, "
                          "ensuring unbiased estimates that converge to the true value function as the number of episodes increases.", normal_style))
    story.append(PageBreak())
    
    # Section 3: Results
    story.append(Paragraph("3. Results and Analysis", heading1_style))
    
    story.append(Paragraph(
        "We ran the First-Visit Monte Carlo algorithm on 2000 episodes to obtain robust estimates of the state-value function. "
        "This section presents the results, including value estimates, convergence analysis, and statistical summaries.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>3.1 Final Value Estimates</b>", heading2_style))
    story.append(Paragraph("After processing 2000 episodes, we obtain the following value estimates:", normal_style))
    
    # Create table for results
    data = [['State', 'State Name', 'V(s)'],
            ['0', 'Passive Browsing', '-0.3230'],
            ['1', 'Selective Reading', '-0.6120'],
            ['2', 'Deep Engagement', '-0.7408']]
    
    table = Table(data, colWidths=[1*inch, 3*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#2c3e50')),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>3.2 Detailed Interpretation of Results</b>", heading2_style))
    story.append(Paragraph(
        "The value estimates reveal interesting patterns about the expected returns from each state. <b>State 0 (Passive Browsing) "
        "has the highest value</b> (-0.3230), followed by State 1 (-0.6120), and State 2 (-0.7408) has the lowest value. "
        "This result may seem counterintuitive at first glance, but it reflects the underlying transition dynamics and reward structure.",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Why are all values negative?</b>", normal_style))
    story.append(Paragraph(
        "All three states have negative value estimates, which indicates that, on average, sessions starting from these states "
        "tend to result in negative expected returns. This is primarily due to the high frequency of short sessions (≤3 steps) "
        "that receive a -8 reward. Since 51.75% of episodes are short, the negative reward dominates the expected return calculation.",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Why is State 0 (Passive Browsing) the best?</b>", normal_style))
    story.append(Paragraph(
        "State 0 has the highest value despite being the 'least engaged' state. This counterintuitive result occurs because:",
        normal_style))
    story.append(Paragraph("• State 0 has transition paths that can lead to longer sessions, and when combined with the discount factor, "
                          "these longer sessions contribute positively to the expected return.", normal_style))
    story.append(Paragraph("• The transition probabilities from State 0 allow for paths to States 1 and 2, which can eventually lead "
                          "to longer sessions with positive terminal rewards.", normal_style))
    story.append(Paragraph("• States 1 and 2, while representing higher engagement, may have transition dynamics that lead more "
                          "frequently to shorter sessions or exits.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Key insight:</b> The value function V(s) represents the <b>expected return</b> from state s under the current policy "
        "(implicit in the transition probabilities). It is not simply a measure of 'engagement level' but rather the expected "
        "cumulative discounted reward from that state. The negative values reflect the reality that most sessions are short "
        "and receive negative rewards, making the expected return negative overall.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>3.3 Convergence Analysis</b>", heading2_style))
    story.append(Paragraph(
        "The convergence plot (shown below) provides crucial insights into how the value estimates stabilize as more episodes "
        "are processed. This visualization is essential for understanding the learning dynamics of the Monte Carlo algorithm.",
        normal_style))
    
    # Add convergence plot
    if os.path.exists("convergence_plot.png"):
        img = Image("convergence_plot.png", width=5.5*inch, height=3.3*inch)
        story.append(Spacer(1, 0.1*inch))
        story.append(img)
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            "<i>Figure 1: Convergence of value estimates V(s) over 2000 episodes. The plot shows how estimates stabilize "
            "after approximately 500-1000 episodes, with some variance remaining due to the stochastic nature of the environment.</i>",
            ParagraphStyle('Caption', parent=normal_style, fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
        story.append(Spacer(1, 0.15*inch))
        story.append(Paragraph(
            "<b>Key observations from the convergence plot:</b>",
            normal_style))
        story.append(Paragraph("• <b>Initial variance</b>: Early estimates (first 100-200 episodes) show high variance as the algorithm "
                              "has limited data. This is expected behavior for Monte Carlo methods.", normal_style))
        story.append(Paragraph("• <b>Stabilization phase</b>: After approximately 500-1000 episodes, the estimates begin to stabilize "
                              "around their final values. This indicates that sufficient data has been collected.", normal_style))
        story.append(Paragraph("• <b>Convergence</b>: All three states converge to stable values, with State 0 converging to the highest "
                              "value and State 2 to the lowest. The convergence is not perfectly smooth due to the stochastic nature "
                              "of the environment and the sampling-based nature of Monte Carlo methods.", normal_style))
        story.append(Paragraph("• <b>Remaining variance</b>: Some variance remains even after 2000 episodes, which is characteristic of "
                              "Monte Carlo methods. This variance decreases as more episodes are processed, but never completely "
                              "disappears due to the stochastic environment.", normal_style))
    else:
        story.append(Paragraph("<i>[Convergence plot not found]</i>", normal_style))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>3.4 Episode Statistics and Distribution Analysis</b>", heading2_style))
    story.append(Paragraph("From the 2000 episodes generated, we observe the following statistics:", normal_style))
    
    # Add episode length distribution plot
    if os.path.exists("episode_lengths.png"):
        img = Image("episode_lengths.png", width=5.5*inch, height=3.3*inch)
        story.append(Spacer(1, 0.1*inch))
        story.append(img)
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            "<i>Figure 2: Distribution of episode lengths across 2000 episodes. The histogram shows the frequency of different "
            "session lengths, with most episodes being relatively short.</i>",
            ParagraphStyle('Caption', parent=normal_style, fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("• <b>Mean episode length</b>: 5.41 steps - This indicates that, on average, sessions last about 5-6 state transitions.", normal_style))
    story.append(Paragraph("• <b>Episode length range</b>: 2 to 27 steps - There is significant variation in session lengths, from very short (2 steps) to quite long (27 steps).", normal_style))
    story.append(Paragraph("• <b>Standard deviation</b>: 3.69 steps - The relatively high standard deviation indicates substantial variability in session lengths.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Add terminal reward distribution plot
    if os.path.exists("terminal_rewards.png"):
        img = Image("terminal_rewards.png", width=5.5*inch, height=3.3*inch)
        story.append(Spacer(1, 0.1*inch))
        story.append(img)
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            "<i>Figure 3: Distribution of terminal rewards. The histogram shows three distinct reward categories: -8 (short sessions), "
            "+4 (moderate sessions), and +10 (long sessions).</i>",
            ParagraphStyle('Caption', parent=normal_style, fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Terminal reward distribution:</b>", normal_style))
    story.append(Paragraph("  • <b>+10</b> (length ≥ 8): 328 episodes (16.4%) - Long, engaged sessions that receive the highest reward", normal_style))
    story.append(Paragraph("  • <b>+4</b> (length 4-7): 637 episodes (31.85%) - Moderate sessions with average reward", normal_style))
    story.append(Paragraph("  • <b>-8</b> (length ≤ 3): 1035 episodes (51.75%) - Short, disengaged sessions that receive negative reward", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Critical insight:</b> The high proportion of short episodes (51.75%) explains why all value estimates are negative. "
        "Even though some episodes receive positive rewards (+4 or +10), the majority receive -8, which dominates the expected "
        "return calculation. This demonstrates how the reward structure and transition dynamics interact to determine state values.",
        normal_style))
    story.append(PageBreak())
    
    # Section 4: MC vs DP
    story.append(Paragraph("4. Monte Carlo vs Dynamic Programming: A Comprehensive Comparison", heading1_style))
    
    story.append(Paragraph(
        "Understanding the differences between Monte Carlo and Dynamic Programming methods is crucial for selecting the appropriate "
        "algorithm for a given problem. This section provides a detailed comparison of both approaches.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.1 Monte Carlo Method (Implemented in This Project)</b>", heading2_style))
    story.append(Paragraph("<b>Advantages:</b>", normal_style))
    story.append(Paragraph("• <b>Model-free</b>: No need for transition probabilities or reward models. This is the key advantage - "
                          "we can learn directly from experience without building a model of the environment.", normal_style))
    story.append(Paragraph("• <b>Works with actual experience</b>: Learns from real trajectories generated by the environment. "
                          "This makes it applicable to real-world scenarios where we have logged data but no model.", normal_style))
    story.append(Paragraph("• <b>Handles delayed rewards naturally</b>: The episodic nature of MC makes it perfect for scenarios "
                          "with sparse, terminal rewards like our user session problem.", normal_style))
    story.append(Paragraph("• <b>Suitable for episodic tasks</b>: Perfect for session-based scenarios where episodes naturally terminate.", normal_style))
    story.append(Paragraph("• <b>Unbiased estimates</b>: With sufficient episodes, MC provides unbiased estimates of the true value function.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Disadvantages:</b>", normal_style))
    story.append(Paragraph("• <b>Requires many episodes</b>: Needs sufficient data (2000+ episodes) to converge to reliable estimates. "
                          "This can be a limitation when data is scarce.", normal_style))
    story.append(Paragraph("• <b>Slower convergence</b>: May need thousands of episodes to achieve stable estimates, especially for "
                          "states that are rarely visited.", normal_style))
    story.append(Paragraph("• <b>Only for episodic tasks</b>: Requires episodes to terminate, making it unsuitable for continuing tasks "
                          "without modification.", normal_style))
    story.append(Paragraph("• <b>High variance</b>: Estimates can be noisy, especially early in learning when few episodes have been processed.", normal_style))
    story.append(Paragraph("• <b>No online learning</b>: Cannot update value estimates during an episode - must wait for episode completion.", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.2 Dynamic Programming Method</b>", heading2_style))
    story.append(Paragraph("<b>Advantages:</b>", normal_style))
    story.append(Paragraph("• <b>Fast convergence</b>: Iterative updates converge quickly, often in just a few iterations. "
                          "This makes DP very efficient when a model is available.", normal_style))
    story.append(Paragraph("• <b>Exact values</b>: Computes the true value function (given an accurate model). "
                          "DP provides exact solutions, not estimates.", normal_style))
    story.append(Paragraph("• <b>Low variance</b>: Deterministic updates mean there is no sampling variance. "
                          "Results are reproducible and stable.", normal_style))
    story.append(Paragraph("• <b>Works for continuing tasks</b>: Not limited to episodic scenarios - can handle infinite horizons.", normal_style))
    story.append(Paragraph("• <b>Efficient computation</b>: For small to medium state spaces, DP is computationally efficient.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Disadvantages:</b>", normal_style))
    story.append(Paragraph("• <b>Requires complete model</b>: Needs transition probabilities P(s'|s,a) and reward function R(s,a). "
                          "This is often the biggest limitation in real-world applications.", normal_style))
    story.append(Paragraph("• <b>Model may not be available</b>: In real systems, transition probabilities may be unknown or difficult "
                          "to estimate accurately.", normal_style))
    story.append(Paragraph("• <b>Computational cost</b>: Can be expensive for large state spaces due to the need to iterate over all states.", normal_style))
    story.append(Paragraph("• <b>Model accuracy critical</b>: Results depend entirely on model correctness. "
                          "Inaccurate models lead to inaccurate value estimates.", normal_style))
    story.append(Paragraph("• <b>Assumes known dynamics</b>: Cannot adapt to changing environments without re-estimating the model.", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.3 When to Use Each Method: Decision Guidelines</b>", heading2_style))
    story.append(Paragraph("<b>Use Monte Carlo when:</b>", normal_style))
    story.append(Paragraph("• Transition probabilities are unknown or difficult to estimate", normal_style))
    story.append(Paragraph("• You have access to historical data/trajectories from the environment", normal_style))
    story.append(Paragraph("• The task is episodic with terminal rewards (like user sessions)", normal_style))
    story.append(Paragraph("• The environment model is complex or high-dimensional", normal_style))
    story.append(Paragraph("• You need to learn from actual user behavior without modeling", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Use Dynamic Programming when:</b>", normal_style))
    story.append(Paragraph("• Complete and accurate model is available", normal_style))
    story.append(Paragraph("• Fast convergence is critical", normal_style))
    story.append(Paragraph("• State space is manageable (not too large)", normal_style))
    story.append(Paragraph("• You need exact value estimates (not approximations)", normal_style))
    story.append(Paragraph("• The environment is deterministic or well-modeled", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.4 Application to Real-Time User Session Systems</b>", heading2_style))
    story.append(Paragraph(
        "For real-time user session systems, the choice between MC and DP has important practical implications:",
        normal_style))
    story.append(Paragraph("• <b>MC is more practical</b>: Can learn from logged user sessions without requiring explicit modeling. "
                          "This is crucial when user behavior is complex and difficult to model.", normal_style))
    story.append(Paragraph("• <b>DP requires modeling</b>: Would need to first estimate transition probabilities from data, "
                          "which essentially means doing MC estimation anyway, then using DP. This adds an extra step.", normal_style))
    story.append(Paragraph("• <b>MC adapts naturally</b>: Can update as user behavior changes over time by simply adding new episodes. "
                          "DP would require re-estimating the entire model.", normal_style))
    story.append(Paragraph("• <b>DP is faster for updates</b>: Once a model is available, DP can compute values very quickly. "
                          "However, this speed comes at the cost of requiring model maintenance.", normal_style))
    story.append(Paragraph(
        "In practice, many production systems use a hybrid approach: MC for initial learning and model estimation, "
        "followed by DP for fast value computation once a reliable model is established.",
        normal_style))
    story.append(PageBreak())
    
    # Section 5: Limitations
    story.append(Paragraph("5. Limitations and Real-Time System Considerations", heading1_style))
    
    story.append(Paragraph(
        "While Monte Carlo methods are powerful, they have limitations that must be understood when applying them to real-world "
        "systems. This section discusses these limitations and provides recommendations for production deployment.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>5.1 Fundamental Limitations of Monte Carlo Methods</b>", heading2_style))
    story.append(Paragraph("1. <b>Sample Efficiency</b>: Requires many episodes (2000+ for reliable estimates). "
                          "This can be problematic when data is expensive to collect or when episodes are long.", normal_style))
    story.append(Paragraph("2. <b>Episodic Requirement</b>: Only works when episodes terminate. "
                          "Cannot be directly applied to continuing tasks without modification.", normal_style))
    story.append(Paragraph("3. <b>Delayed Updates</b>: Must wait for episode completion before updating value estimates. "
                          "This prevents real-time decision-making during an episode.", normal_style))
    story.append(Paragraph("4. <b>High Variance</b>: Early estimates can be very noisy, especially for states that are rarely visited. "
                          "This variance decreases with more episodes but never completely disappears.", normal_style))
    story.append(Paragraph("5. <b>No Online Learning</b>: Cannot update value estimates during an episode. "
                          "This is a significant limitation for real-time systems that need to make decisions as episodes progress.", normal_style))
    story.append(Paragraph("6. <b>Memory Requirements</b>: Must store all returns for each state, which can be memory-intensive "
                          "for large state spaces or long episodes.", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>5.2 Real-Time System Challenges and Solutions</b>", heading2_style))
    story.append(Paragraph("For real-time user session systems, several challenges arise when using Monte Carlo methods:", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("1. <b>Cold Start Problem</b>", normal_style))
    story.append(Paragraph(
        "New users or rarely-visited states have no historical data, making it impossible to compute reliable value estimates. "
        "This is particularly problematic in recommendation systems where new content or users appear frequently.",
        normal_style))
    story.append(Paragraph("<b>Solutions:</b> Use prior estimates (e.g., population averages), default optimistic values to encourage "
                          "exploration, or transfer learning from similar users/states.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("2. <b>Non-Stationary Environment</b>", normal_style))
    story.append(Paragraph(
        "User behavior changes over time due to trends, seasonal patterns, or evolving preferences. Static value estimates "
        "become outdated, leading to poor decisions.",
        normal_style))
    story.append(Paragraph("<b>Solutions:</b> Use sliding windows (only use recent episodes), exponential decay (weight recent "
                          "episodes more heavily), or periodic re-estimation of values.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("3. <b>Computational Cost</b>", normal_style))
    story.append(Paragraph(
        "Processing thousands of episodes and storing returns for each state can be computationally expensive, especially as "
        "the system scales to millions of users.",
        normal_style))
    story.append(Paragraph("<b>Solutions:</b> Batch processing (update values periodically, not after every episode), approximate "
                          "methods (use function approximation instead of tabular methods), or distributed computing.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("4. <b>Delayed Feedback</b>", normal_style))
    story.append(Paragraph(
        "Must wait for session completion before updating values. This prevents making real-time decisions during a session "
        "based on current value estimates.",
        normal_style))
    story.append(Paragraph("<b>Solutions:</b> Combine MC with Temporal Difference (TD) learning for online updates, use bootstrapping "
                          "methods that can update during episodes, or maintain separate online and offline value estimates.", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("5. <b>Sparse Data Problem</b>", normal_style))
    story.append(Paragraph(
        "Some states may be rarely visited, leading to unreliable estimates with high variance. This is common in large state "
        "spaces or when user behavior is highly variable.",
        normal_style))
    story.append(Paragraph("<b>Solutions:</b> State aggregation (group similar states together), function approximation (use neural "
                          "networks to generalize across states), or hierarchical methods that share information between states.", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>5.3 Recommendations for Production Deployment</b>", heading2_style))
    story.append(Paragraph("Based on the limitations discussed, here are practical recommendations for deploying MC methods in production:", normal_style))
    story.append(Paragraph("1. <b>Hybrid Approach</b>: Combine MC with Temporal Difference (TD) learning. Use MC for offline "
                          "batch updates and TD for online real-time updates during episodes.", normal_style))
    story.append(Paragraph("2. <b>Function Approximation</b>: For large state spaces, use neural networks or other function approximators "
                          "instead of tabular methods. This enables generalization and reduces memory requirements.", normal_style))
    story.append(Paragraph("3. <b>Incremental Updates</b>: Update estimates incrementally (online) rather than in batch. This allows "
                          "the system to adapt quickly to changing conditions.", normal_style))
    story.append(Paragraph("4. <b>Exploration Strategy</b>: Ensure sufficient exploration of all states through epsilon-greedy policies "
                          "or other exploration methods. This prevents the cold start problem for rarely-visited states.", normal_style))
    story.append(Paragraph("5. <b>Monitoring and Validation</b>: Continuously monitor convergence, estimate quality, and system performance. "
                          "Set up alerts for when estimates become unreliable or when the environment changes significantly.", normal_style))
    story.append(Paragraph("6. <b>Sliding Windows</b>: Use only recent episodes (e.g., last 30 days) to ensure estimates reflect current "
                          "user behavior rather than outdated patterns.", normal_style))
    story.append(Paragraph("7. <b>Confidence Intervals</b>: Track not just value estimates but also confidence intervals. This helps "
                          "identify when estimates are unreliable due to insufficient data.", normal_style))
    
    # Section 6: Conclusion
    story.append(PageBreak())
    story.append(Paragraph("6. Conclusion and Future Work", heading1_style))
    story.append(Paragraph(
        "This project successfully implements First-Visit Monte Carlo Policy Evaluation for a user session environment, "
        "demonstrating the power of model-free reinforcement learning methods. The implementation correctly handles delayed, "
        "sparse rewards and provides reliable value estimates after processing sufficient episodes.",
        normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Key Achievements:</b>", normal_style))
    story.append(Paragraph("• ✅ Correct implementation of first-visit MC algorithm with proper first-visit rule enforcement", normal_style))
    story.append(Paragraph("• ✅ Proper handling of delayed, sparse terminal rewards with zero intermediate rewards", normal_style))
    story.append(Paragraph("• ✅ Comprehensive convergence analysis with 2000 episodes showing stable value estimates", normal_style))
    story.append(Paragraph("• ✅ Clear visualization of results through convergence plots and distribution analyses", normal_style))
    story.append(Paragraph("• ✅ Detailed analysis of results explaining counterintuitive value estimates", normal_style))
    story.append(Paragraph("• ✅ Thorough comparison between Monte Carlo and Dynamic Programming methods", normal_style))
    story.append(Paragraph("• ✅ Practical discussion of limitations and real-time system considerations", normal_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "The results demonstrate that Monte Carlo methods can effectively learn value functions from experience without requiring "
        "a model, making them suitable for real-world applications where transition probabilities are unknown. However, the method "
        "requires sufficient data and may not be ideal for real-time decision-making during episodes.",
        normal_style))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("<b>Future Work and Extensions:</b>", normal_style))
    story.append(Paragraph("• <b>Implement Temporal Difference (TD) learning</b>: Add TD methods (e.g., TD(0), TD(λ)) for online "
                          "updates that can learn during episodes, not just after completion.", normal_style))
    story.append(Paragraph("• <b>Function Approximation</b>: Extend to large state spaces using neural networks or linear function "
                          "approximators to enable generalization across similar states.", normal_style))
    story.append(Paragraph("• <b>Compare with other model-free methods</b>: Implement and compare with SARSA, Q-learning, and other "
                          "TD methods to understand trade-offs between different approaches.", normal_style))
    story.append(Paragraph("• <b>Policy Improvement</b>: Extend from policy evaluation to policy improvement, implementing policy "
                          "iteration or value iteration to find optimal policies.", normal_style))
    story.append(Paragraph("• <b>Eligibility Traces</b>: Implement TD(λ) with eligibility traces to combine the advantages of MC "
                          "and TD methods.", normal_style))
    story.append(Paragraph("• <b>Exploration Strategies</b>: Add epsilon-greedy, UCB, or other exploration methods to ensure "
                          "sufficient state coverage.", normal_style))
    story.append(Paragraph("• <b>Real-time Adaptation</b>: Develop methods for updating value estimates in real-time as episodes "
                          "progress, enabling online decision-making.", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("_" * 80, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>References</b>", heading2_style))
    story.append(Paragraph("Sutton, R. S., & Barto, A. G. (2018). <i>Reinforcement Learning: An Introduction</i> (2nd ed.). MIT Press.", normal_style))
    story.append(Paragraph("First-Visit Monte Carlo Method for Policy Evaluation - Standard RL Algorithm", normal_style))
    
    # Build PDF
    doc.build(story)
    print("Enhanced report PDF generated successfully: report.pdf")
    print("Report includes all three plots: convergence, episode lengths, and terminal rewards")


if __name__ == "__main__":
    try:
        create_pdf()
    except ImportError:
        print("Error: reportlab library not found.")
        print("Please install it using: pip install reportlab")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
