import mesa
import math

class SubjectAgent(mesa.Agent):
    """
    Agent representing a subject in the sleep study.
    """
    def __init__(self, unique_id, model, subject_data):
        super().__init__(unique_id, model)
        self.subject_data = subject_data
        self.nights = subject_data['nights']
        self.current_night_index = 0
        
        # Initialize state from the first night
        first_night = self.nights[0]
        self.current_CSI = first_night.get('CSI', 0.0)
        self.current_CStab = first_night.get('CStab', 0.0)
        self.sleep_debt = 0
        
        # To track history
        self.history = []

    def step(self):
        if self.current_night_index >= len(self.nights):
            return # End of data for this subject

        current_night = self.nights[self.current_night_index]
        night_label = current_night.get('night_index', 'Unknown')
        night_status = current_night.get('night_status', 'moderate')
        action_effects = current_night.get('action_effects', {})

        # Decision Making: A* Search (Simplified to greedy 1-step lookahead as per requirements)
        # Requirement: "For the current night... Use A* ... to choose the action that moves ... closest to (1.0, 1.0)"
        # Since we only have effects for the *current* night, this is effectively a greedy choice 
        # unless we predict future nights (which we don't have info for in a way that allows true A* over time).
        # The prompt asks for "A* (A-Star)" but describes a heuristic for the "current night". 
        # I will implement it as finding the action that minimizes the heuristic cost (distance to goal).
        
        best_action = None
        min_distance = float('inf')
        best_dCSI = 0
        best_dCStab = 0

        # Target state
        target_CSI = 1.0
        target_CStab = 1.0

        for action, effects in action_effects.items():
            dCSI = effects.get('dCSI', 0)
            dCStab = effects.get('dCStab', 0)
            
            predicted_CSI = self.current_CSI + dCSI
            predicted_CStab = self.current_CStab + dCStab
            
            # Heuristic: Euclidean distance to (1.0, 1.0)
            distance = math.sqrt((predicted_CSI - target_CSI)**2 + (predicted_CStab - target_CStab)**2)
            
            if distance < min_distance:
                min_distance = distance
                best_action = action
                best_dCSI = dCSI
                best_dCStab = dCStab

        # State Update
        self.current_CSI += best_dCSI
        self.current_CStab += best_dCStab
        
        # Sleep Debt Update
        if night_status == 'bad':
            self.sleep_debt += 1
        elif night_status == 'good':
            self.sleep_debt -= 1
        # 'moderate' stays same

        # Record results
        result = {
            'subject_id': self.unique_id,
            'night_index': night_label,
            'chosen_action': best_action,
            'resulting_CSI': self.current_CSI,
            'resulting_CStab': self.current_CStab,
            'sleep_debt': self.sleep_debt,
            'night_status': night_status
        }
        self.history.append(result)

        # Advance to next night
        self.current_night_index += 1
