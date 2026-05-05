# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_water_atm(dut):
    dut._log.info("Start Water ATM Test")

    # Clock: 100 KHz
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # -------- RESET --------
    dut._log.info("Reset DUT")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # =========================================================
    # -------- TEST 1: ₹1 → 2 Liters --------
    # =========================================================
    dut._log.info("Test ₹1 coin → expect 2 liters")

    # coin_1 = ui_in[0]
    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    # Generate 2 flow pulses
    for _ in range(2):
        dut.ui_in.value = 0b00010000  # flow_sensor = ui_in[4]
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 20)

    # Check output
    liters = (dut.uo_out.value >> 1) & 0x7F
    valve  = dut.uo_out.value & 0x1

    assert liters == 2, f"Expected 2L, got {liters}"
    assert valve == 0, "Valve should be OFF after completion"

    # =========================================================
    # -------- TEST 2: ₹2 → 5 Liters --------
    # =========================================================
    dut._log.info("Test ₹2 coin → expect 5 liters")

    dut.ui_in.value = 0b00000010
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    for _ in range(5):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 30)

    liters = (dut.uo_out.value >> 1) & 0x7F
    valve  = dut.uo_out.value & 0x1

    assert liters == 5, f"Expected 5L, got {liters}"
    assert valve == 0, "Valve should be OFF after completion"

    # =========================================================
    # -------- TEST 3: ₹5 → 20 Liters --------
    # =========================================================
    dut._log.info("Test ₹5 coin → expect 20 liters")

    dut.ui_in.value = 0b00000100
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    for _ in range(20):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 50)

    liters = (dut.uo_out.value >> 1) & 0x7F
    valve  = dut.uo_out.value & 0x1

    assert liters == 20, f"Expected 20L, got {liters}"
    assert valve == 0, "Valve should be OFF after completion"

    # =========================================================
    # -------- TEST 4: ₹10 → 40 Liters --------
    # =========================================================
    dut._log.info("Test ₹10 coin → expect 40 liters")

    dut.ui_in.value = 0b00001000
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    for _ in range(40):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 80)

    liters = (dut.uo_out.value >> 1) & 0x7F
    valve  = dut.uo_out.value & 0x1

    assert liters == 40, f"Expected 40L, got {liters}"
    assert valve == 0, "Valve should be OFF after completion"

    dut._log.info("All tests PASSED ✅")
