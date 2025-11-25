import mesa
import json
import os
import glob
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from agent import SubjectAgent

class SleepModel(mesa.Model):
    """
    Model to simulate sleep optimization for multiple subjects.
    """
    def __init__(self, data_path="anomaly_state_files/subject_states"):
        super().__init__()
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(20, 20, False)
        self.data_path = data_path
        
        # Find all subject files
        # Assuming files are named subject_XX_state.json
        search_pattern = os.path.join(self.data_path, "subject_*_state.json")
        subject_files = sorted(glob.glob(search_pattern))
        
        if not subject_files:
            print(f"Warning: No subject files found in {self.data_path}")
            # Fallback for absolute path if relative fails (depending on CWD)
            # Trying a likely absolute path based on user context if relative fails
            abs_path = r"c:\Projects\SleepProject\anomaly_state_files\subject_states"
            search_pattern = os.path.join(abs_path, "subject_*_state.json")
            subject_files = sorted(glob.glob(search_pattern))

        for file_path in subject_files:
            try:
                with open(file_path, 'r') as f:
                    subject_data = json.load(f)
                
                # Extract ID from filename or data
                # Filename format: subject_01_state.json
                filename = os.path.basename(file_path)
                subject_id = filename.split('_')[1] 
                
                # Create Agent
                agent = SubjectAgent(subject_id, self, subject_data)
                self.schedule.add(agent)
                
                # Place agent on grid based on initial state
                x = int(agent.current_CSI * 10)
                y = int(agent.current_CStab * 10)
                # Clamp to grid size
                x = max(0, min(x, self.grid.width - 1))
                y = max(0, min(y, self.grid.height - 1))
                self.grid.place_agent(agent, (x, y))
                
            except Exception as e:
                print(f"Error loading file {file_path}: {e}")

        # Data Collector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Average_CSI": compute_avg_csi,
                "Average_Sleep_Debt": compute_avg_sleep_debt
            },
            agent_reporters={
                "CSI": "current_CSI",
                "Sleep_Debt": "sleep_debt"
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.datacollector.collect(self)
        
        # Check if all agents have finished their data
        # If all agents are done (index >= len(nights)), stop model
        all_done = True
        for agent in self.schedule.agents:
            if agent.current_night_index < len(agent.nights):
                all_done = False
                break
        
        if all_done:
            self.running = False

def compute_avg_csi(model):
    agent_csis = [a.current_CSI for a in model.schedule.agents]
    return sum(agent_csis) / len(agent_csis) if agent_csis else 0

def compute_avg_sleep_debt(model):
    agent_debts = [a.sleep_debt for a in model.schedule.agents]
    return sum(agent_debts) / len(agent_debts) if agent_debts else 0
