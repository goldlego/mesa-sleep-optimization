import mesa
from model import SleepModel
from agent import SubjectAgent

def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {
        "Shape": "circle",
        "Color": "blue",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
        "text": agent.unique_id,
        "text_color": "white"
    }
    
    # Color based on status
    if agent.sleep_debt > 5:
        portrayal["Color"] = "red"
    elif agent.sleep_debt < -5:
        portrayal["Color"] = "green"
        
    return portrayal

# Since we don't have a grid, we can't easily use CanvasGrid without adding positions to agents.
# But the user asked for "simple Grid or ChartModule".
# To use a Grid, I would need to assign positions. 
# Let's stick to ChartModule which is more useful for data.
# If I MUST use a grid, I'd have to modify the model to place agents on a grid.
# Given the nature of the data (time series), Charts are better.
# I will add a TextElement to show status.

class StatusElement(mesa.visualization.TextElement):
    def render(self, model):
        return f"Step: {model.schedule.steps}"

# Chart for CSI
csi_chart = mesa.visualization.ChartModule(
    [{"Label": "Avg_CSI", "Color": "Black"}],
    data_collector_name='datacollector'
)

# I need to add a DataCollector to the model to use ChartModule
# Let's modify model.py to include DataCollector
# But first, let's just define the server. 
# Wait, without DataCollector in model, ChartModule won't work.
# I should update model.py to include DataCollector.

# Let's create the server assuming DataCollector exists or I'll add it now.
# Actually, I'll update model.py first or just handle it here if possible? No, must be in model.

# Let's write this server file, but I'll need to update model.py to support it.
# Or I can define a custom visualization that pulls from agents directly.

# Let's keep it simple. I will update model.py to have a DataCollector.
# But for now, I'll write the server code that expects it.

# Actually, let's just use a simple text visualization if Charts are too complex to wire up without DataCollector.
# But the user asked for "CSI Trend over nights" and "Sleep Debt accumulation curve" in the OUTPUTS section (CSV/Plots).
# In VISUALIZATION section: "simple Grid or ChartModule".

# I will use ChartModule. I need to update model.py.

# Let's write the server code.
model_params = {
    "data_path": "anomaly_state_files/subject_states"
}

# To visualize individual agents in a chart, we need a collector that collects for each agent?
# ChartModule collects model-level variables. 
# So we'd need "Agent 1 CSI", "Agent 2 CSI", etc.
# That's dynamic. Mesa ChartModule usually takes a fixed list of series.
# With 10 agents, I can hardcode 10 series if I expose them in the model.

# Alternative: Just show Average CSI and Average Sleep Debt.
chart_element = mesa.visualization.ChartModule([
    {"Label": "Average_CSI", "Color": "Blue"},
    {"Label": "Average_Sleep_Debt", "Color": "Red"}
])

server = mesa.visualization.ModularServer(
    SleepModel,
    [StatusElement(), chart_element],
    "Sleep Optimization Simulation",
    model_params
)

server.port = 8521 # The default
server.launch()
