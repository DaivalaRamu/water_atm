# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


def get_outputs(dut):
    val = dut.uo_out.value.to_unsigned()
    liters = (val >> 1) & 0x7F
    valve = val & 0x1
    return liters, valve


@cocotb.test()
async def test_water_atm(dut):

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # RESET
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # ================= ₹1 TEST =================
    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    # 🔥 wait FSM to reach DISP (important)
    await ClockCycles(dut.clk, 5)

    # 🔥 strong pulses (sync-safe)
    for _ in range(2):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 4)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 2)

    await ClockCycles(dut.clk, 10)

    liters, valve = get_outputs(dut)
    assert liters == 2, f"Expected 2L, got {liters}"
    assert valve == 0

    # ================= ₹2 TEST =================
    dut.ui_in.value = 0b00000010
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    await ClockCycles(dut.clk, 5)

    for _ in range(5):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 4)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 2)

    await ClockCycles(dut.clk, 10)

    liters, _ = get_outputs(dut)
    assert liters == 5

    # ================= ₹5 TEST =================
    dut.ui_in.value = 0b00000100
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    await ClockCycles(dut.clk, 5)

    for _ in range(20):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 4)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 2)

    await ClockCycles(dut.clk, 20)

    liters, _ = get_outputs(dut)
    assert liters == 20

    # ================= ₹10 TEST =================
    dut.ui_in.value = 0b00001000
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    await ClockCycles(dut.clk, 5)

    for _ in range(40):
        dut.ui_in.value = 0b00010000
        await ClockCycles(dut.clk, 4)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 2)

    await ClockCycles(dut.clk, 30)

    liters, _ = get_outputs(dut)
    assert liters == 40
