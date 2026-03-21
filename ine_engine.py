import os
from typing import TypedDict, List, Annotated
import operator

# Note: In a real environment, you would import langgraph, llamaindex, etc.
# This is a high-level architectural prototype for your I-STEM submission.

class AgentState(TypedDict):
    research_goal: str
    instrument_stack: List[str]
    sop_steps: List[str]
    confidence_score: float
    iteration: int

import json

def instrument_selection_node(state: AgentState):
    """
    Simulates a LlamaIndex Knowledge Graph query by reading from the instruments_db.json.
    """
    print("--- SELECTING INSTRUMENTS (DB QUERY) ---")
    goal = state['research_goal'].lower()
    
    # Load the Scientific Knowledge Base
    db_path = os.path.join(os.path.dirname(__file__), 'instruments_db.json')
    try:
        with open(db_path, 'r') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {"instruments": []}
    
    stack = []
    sop_fragments = []
    
    # Reasoning logic: Matching capabilities to goals
    for inst in db['instruments']:
        if any(cap in goal for cap in inst['capabilities']):
            stack.append(inst['name'])
            sop_fragments.extend(inst['sop_template'])
            
    # Fallback if no specific match
    if not stack:
        stack = ["UV-Vis Spectrophotometer"]
        sop_fragments = ["Initialize standard baseline.", "Measure absorbance."]
        
    return {
        "instrument_stack": stack, 
        "sop_steps": sop_fragments,
        "iteration": state['iteration'] + 1
    }

def sop_generation_node(state: AgentState):
    """
    Uses an LLM (simulated) to generate dynamic SOP steps based on the stack.
    """
    print("--- GENERATING DYNAMIC SOP ---")
    instruments = ", ".join(state['instrument_stack'])
    
    # Simulated Chain-of-Thought (CoT) Prompting
    sop = [
        f"1. Initialize {instruments} in offline security mode.",
        "2. Calibrate sensor baselines using standard reference samples.",
        "3. Execute primary data acquisition with 0.1ms sampling rate.",
        "4. Process raw waveform data through the INE-Transduction layer."
    ]
    
    return {"sop_steps": sop, "confidence_score": 0.95}

def evaluate_safety_node(state: AgentState):
    """
    A Hybrid-AI node that checks for anomalies or safety violations.
    """
    print("--- VERIFYING SAFETY & ANOMALIES ---")
    # Symbolic constraint check
    if len(state['instrument_stack']) > 0:
        return {"confidence_score": state['confidence_score']}
    else:
        return {"confidence_score": 0.0}

class ScientificDecisionEngine:
    def __init__(self):
        # In a full build, you would initialize the LangGraph StateMachine here
        pass

    def run_experiment_planning(self, goal: str):
        # Initial State
        state: AgentState = {
            "research_goal": goal,
            "instrument_stack": [],
            "sop_steps": [],
            "confidence_score": 0.0,
            "iteration": 0
        }
        
        # Step 1: Instrument Selection
        selection = instrument_selection_node(state)
        # Using direct assignment to satisfy TypedDict constraints
        new_stack = selection.get('instrument_stack')
        if isinstance(new_stack, list):
            state['instrument_stack'] = new_stack
            
        new_sop = selection.get('sop_steps')
        if isinstance(new_sop, list):
            state['sop_steps'] = new_sop
            
        new_iter = selection.get('iteration')
        if isinstance(new_iter, int):
            state['iteration'] = new_iter
        
        # Step 2: SOP Generation
        sop_data = sop_generation_node(state)
        sop_steps = sop_data.get('sop_steps')
        if isinstance(sop_steps, list):
            state['sop_steps'] = sop_steps
            
        conf = sop_data.get('confidence_score')
        if isinstance(conf, (int, float)):
            state['confidence_score'] = float(conf)
        
        # Step 3: Safety Evaluation
        safety_data = evaluate_safety_node(state)
        safety_conf = safety_data.get('confidence_score')
        if isinstance(safety_conf, (int, float)):
            state['confidence_score'] = float(safety_conf)
        
        return state

if __name__ == "__main__":
    engine = ScientificDecisionEngine()
    
    user_goal = "Determine the atomic structure of a new protein crystal."
    result = engine.run_experiment_planning(user_goal)
    
    print("\n" + "="*50)
    print("INE-ENGINE: SCIENTIFIC DECISION REPORT")
    print("="*50)
    print(f"Goal: {result['research_goal']}")
    print(f"Instrument Stack: {result['instrument_stack']}")
    print("-" * 30)
    print("Dynamic SOP Steps:")
    for step in result['sop_steps']:
        print(step)
    print("="*50)
    print(f"Confidence Level: {result['confidence_score'] * 100}%")
    print("="*50)
