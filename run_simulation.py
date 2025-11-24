import csv
import os
from model import SleepModel

# Try to import matplotlib
try:
    import matplotlib.pyplot as plt
    PLOT_AVAILABLE = True
except ImportError:
    PLOT_AVAILABLE = False
    print("Warning: matplotlib not found. Plots will not be generated.")

def run_simulation():
    print("Starting simulation...")
    model = SleepModel()
    
    # Run until model stops
    step_count = 0
    while model.running:
        model.step()
        step_count += 1
        # Safety break
        if step_count > 1000:
            print("Simulation exceeded 1000 steps, stopping.")
            break
            
    print(f"Simulation finished in {step_count} steps.")
    
    # Collect data
    all_results = []
    for agent in model.schedule.agents:
        all_results.extend(agent.history)
        
    # Save to CSV using csv module
    output_csv = "simulation_results.csv"
    if all_results:
        keys = all_results[0].keys()
        with open(output_csv, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(all_results)
        print(f"Results saved to {output_csv}")
        
        # Generate Plots
        if PLOT_AVAILABLE:
            generate_plots(all_results)
    else:
        print("No results to save.")

def generate_plots(data):
    # Convert list of dicts to a structure easier to plot without pandas
    # We need to group by subject_id
    subjects = {}
    for row in data:
        sid = row['subject_id']
        if sid not in subjects:
            subjects[sid] = {'CSI': [], 'Sleep_Debt': [], 'Actions': []}
        subjects[sid]['CSI'].append(row['resulting_CSI'])
        subjects[sid]['Sleep_Debt'].append(row['sleep_debt'])
        subjects[sid]['Actions'].append(row['chosen_action'])
        
    # 1. CSI Trend over nights
    plt.figure(figsize=(12, 6))
    for sid, sdata in subjects.items():
        plt.plot(range(len(sdata['CSI'])), sdata['CSI'], label=f"Subject {sid}")
    
    plt.title("CSI Trend over Nights")
    plt.xlabel("Night Index")
    plt.ylabel("CSI")
    plt.legend()
    plt.grid(True)
    plt.savefig("csi_trend.png")
    print("Saved csi_trend.png")
    
    # 2. Sleep Debt accumulation curve
    plt.figure(figsize=(12, 6))
    for sid, sdata in subjects.items():
        plt.plot(range(len(sdata['Sleep_Debt'])), sdata['Sleep_Debt'], label=f"Subject {sid}")
        
    plt.title("Sleep Debt Accumulation")
    plt.xlabel("Night Index")
    plt.ylabel("Sleep Debt")
    plt.legend()
    plt.grid(True)
    plt.savefig("sleep_debt_trend.png")
    print("Saved sleep_debt_trend.png")
    
    # 3. Action distribution histogram
    # Count all actions
    action_counts = {}
    for sid, sdata in subjects.items():
        for action in sdata['Actions']:
            action_counts[action] = action_counts.get(action, 0) + 1
            
    plt.figure(figsize=(10, 6))
    plt.bar(action_counts.keys(), action_counts.values())
    plt.title("Action Distribution")
    plt.xlabel("Action")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("action_distribution.png")
    print("Saved action_distribution.png")

if __name__ == "__main__":
    run_simulation()
