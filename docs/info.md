---

## How it works

This project implements a **Water ATM system** using a Finite State Machine (FSM).  
The system dispenses a fixed amount of water based on the coin inserted.

### Working Principle:

1. **Idle State (IDLE)**  
   - The system waits for a coin input.  
   - Supported coins:
     - ₹1 → 2 liters
     - ₹2 → 5 liters
     - ₹5 → 20 liters
     - ₹10 → 40 liters  

2. **Set State (SET)**  
   - Based on the inserted coin, the system sets:
     - Target water quantity (liters)
     - Maximum time limit

3. **Dispense State (DISP)**  
   - The valve is turned ON.  
   - Water flow is measured using a **flow sensor input**.  
   - Each pulse from the flow sensor increments the liter count.

4. **Done State (DONE)**  
   - The valve is turned OFF when:
     - Target liters are reached, OR
     - Time limit expires  
   - System resets back to IDLE.

### Key Features:
- Fully synchronous design using clock
- Flow sensor synchronization to avoid metastability
- Timer-based safety cutoff
- Efficient FSM implementation

---

## How to test

### Input Mapping (ui_in)

| Bit       | Function        |
|----------|----------------|
| ui_in[0] | Coin ₹1        |
| ui_in[1] | Coin ₹2        |
| ui_in[2] | Coin ₹5        |
| ui_in[3] | Coin ₹10       |
| ui_in[4] | Flow Sensor    |

### Output Mapping (uo_out)

| Bit          | Function        |
|-------------|----------------|
| uo_out[0]   | Valve ON/OFF   |
| uo_out[7:1] | Liters Count   |

---

### Test Procedure:

1. Apply reset:
   - `rst_n = 0 → 1`

2. Insert a coin:
   - Set corresponding `ui_in[x] = 1` for one clock cycle

3. Simulate water flow:
   - Generate pulses on `ui_in[4]` (flow sensor)

4. Observe output:
   - `uo_out[0] = 1` → valve ON
   - `uo_out[7:1]` increments with each pulse

5. Completion:
   - Valve turns OFF automatically when target is reached

---

### Example:

- Insert ₹2 (`ui_in[1] = 1`)
- Provide 5 pulses on flow sensor  
- Output:
  - `liters = 5`
  - `valve_on = 0` (after completion)

---

## External hardware

This design is fully digital and does not require external hardware for simulation.

However, in a real-world implementation, the following components may be used:

- Water flow sensor (pulse-based)
- Solenoid valve (controlled via driver circuit)
- Coin detection mechanism
- Microcontroller or FPGA (for integration)

---
