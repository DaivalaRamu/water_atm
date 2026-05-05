# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


def get_outputs(dut):
    """Safe extraction of outputs (NO LogicArray error)"""
    val = dut.uo_out.value.integer
    liters = (val >> 1) & 0x7F
    valve = val & 0x1
    return liters, valve


@cocotb.test()
async def test_water_atm(dut):

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # -------- RESET --------
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # =====================================================
    # TEST 1: ₹1 → 2 Liters
    # =====================================================
    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    for _ in range(2):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 20)

    liters, valve = get_outputs(dut)
    assert liters == 2, f"Expected 2L, got {liters}"
    assert valve == 0

    # =====================================================
    # TEST 2: ₹2 → 5 Liters
    # =====================================================
    dut.ui_in.value = 0b00000010
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    for _ in range(5):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 30)

    liters, valve = get_outputs(dut)
    assert liters == 5, f"Expected 5L, got {liters}"

    # =====================================================
    # TEST 3: ₹5 → 20 Liters
    # =====================================================
    dut.ui_in.value = 0b00000100
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    for _ in range(20):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 50)

    liters, valve = get_outputs(dut)
    assert liters == 20, f"Expected 20L, got {liters}"

    # =====================================================
    # TEST 4: ₹10 → 40 Liters
    # =====================================================
    dut.ui_in.value = 0b00001000
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    for _ in range(40):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 80)

    liters, valve = get_outputs(dut)
    assert liters == 40, f"Expected 40L, got {liters}"
