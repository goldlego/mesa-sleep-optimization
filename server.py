import mesa
from model import SleepModel
from agent import SubjectAgent

def agent_portrayal(agent):
    if agent is None:
        return
    
    # Calculate distance to center (10, 10)
    # Grid is 20x20, so center is (10, 10)
    x, y = agent.pos
    dist = ((x - 10)**2 + (y - 10)**2)**0.5
    
    color = "red"
    if dist < 3:
        color = "green"
    elif dist < 6:
        color = "yellow"
        
    portrayal = {
        "Shape": "circle",
        "Color": color,
        "Filled": "true",
        "Layer": 0,
        "r": 0.8,
        "text": agent.unique_id,
        "text_color": "black"
    }
        
    return portrayal

class StatusElement(mesa.visualization.TextElement):
    def render(self, model):
        return f"Step: {model.schedule.steps}"

# Grid Visualization
grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 20, 500, 500)

# Chart for CSI
chart_element = mesa.visualization.ChartModule([
    {"Label": "Average_CSI", "Color": "Blue"},
    {"Label": "Average_Sleep_Debt", "Color": "Red"}
])

model_params = {
    "data_path": "anomaly_state_files/subject_states"
}

server = mesa.visualization.ModularServer(
    SleepModel,
    [grid, StatusElement(), chart_element],
    "Sleep Optimization Simulation",
    model_params
)

server.port = 8521 # The default
server.launch()
