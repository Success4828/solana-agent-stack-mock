import time
import random
import json

class MockSolanaAgentStack:
    def __init__(self):
        self.current_slot = 142300500
        self.blockhash_lifespan = 150 
        self.mock_jito_tip_floor = 0.0005 
        
    def get_live_jito_tips(self):
        congestion_factor = random.uniform(1.0, 2.5)
        base_tip = self.mock_jito_tip_floor * congestion_factor
        return {
            "p25": round(base_tip * 0.8, 6),
            "p50": round(base_tip, 6),
            "p75": round(base_tip * 1.3, 6),
        }

    def ai_agent_retry_decision(self, error_context):
        print("\n[AI AGENT INFERENCE ENGINE ACTIVATED]")
        print(f"Agent observing error context: {json.dumps(error_context)}")
        error_code = error_context.get("error")
        
        if error_code == "EXPIRED_BLOCKHASH":
            reasoning = "Analysis: The transaction slot delta exceeded 150 slots. The blockhash is dead. Action required: Refreshing blockhash, bumping Jito tip by 20% to clear consensus pool faster."
            print(f"Agent Reasoning: {reasoning}")
            return {
                "action": "RETRY_WITH_NEW_BLOCKHASH",
                "tip_multiplier": 1.2,
                "refresh_hash": True
            }
        return {"action": "ABORT", "reason": "Unknown failure mode"}

    def execute_transaction_lifecycle(self, simulate_failure=False):
        print("\n--- Starting Transaction Stack Execution ---")
        tips = self.get_live_jito_tips()
        target_tip = tips["p50"]
        print(f"[gRPC Stream] Current Slot: {self.current_slot}")
        print(f"[Jito API] Live Tip Percentiles -> P25: {tips['p25']}, P50: {tips['p50']}, P75: {tips['p75']}")
        print(f"[Stack] Constructing bundle targeting P50 tip: {target_tip} SOL")

        if simulate_failure:
            print("[Fault Injection] Simulating stale blockhash signature...")
            time.sleep(1)
            error_context = {
                "error": "EXPIRED_BLOCKHASH",
                "failed_slot": self.current_slot,
                "timestamp": time.time()
            }
            decision = self.ai_agent_retry_decision(error_context)
            
            if decision["action"] == "RETRY_WITH_NEW_BLOCKHASH":
                print("\n[Stack] Executing AI Agent Directive...")
                self.current_slot += 12 
                target_tip = round(target_tip * decision["tip_multiplier"], 6)
                print(f"[Stack] Blockhash refreshed at slot {self.current_slot}. Upgraded Jito Tip: {target_tip} SOL")
            else:
                print("[Stack] Agent aborted execution.")
                return

        stages = ["Processed", "Confirmed", "Finalized"]
        tx_id = "5gY7...K9pZ"
        
        for stage in stages:
            time.sleep(1.5) 
            self.current_slot += random.randint(1, 3)
            timestamp = time.strftime('%H:%M:%S', time.localtime())
            print(f"[{timestamp}] Tx: {tx_id} | State: {stage} | Slot: {self.current_slot}")
            
        print("\n--- Transaction Lifecycle Successfully Completed ---")

if __name__ == "__main__":
    stack = MockSolanaAgentStack()
    stack.execute_transaction_lifecycle(simulate_failure=False)
    stack.execute_transaction_lifecycle(simulate_failure=True)
