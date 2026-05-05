# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


def get_outputs(dut):
    val = dut.uo_out.value.to_unsigned()  # FIX: no deprecation
    liters = (val >> 1) & 0x7F
    valve = val & 0x1
    return liters, valve


async def insert_coin_and_wait(dut, coin_bit):
    dut.ui_in.value = (1 << coin_bit)
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    # 🔥 WAIT for FSM to reach DISP
    await ClockCycles(dut.clk, 2)


async def give_flow_pulses(dut, count):
    for _ in range(count):
        dut.ui_in.value = (1 << 4)  # flow_sensor
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)


@cocotb.test()
async def test_water_atm(dut):

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # ---------------- ₹1 → 2L ----------------
    await insert_coin_and_wait(dut, 0)
    await give_flow_pulses(dut, 2)
    await ClockCycles(dut.clk, 5)

    liters, valve = get_outputs(dut)
    assert liters == 2, f"Expected 2L, got {liters}"
    assert valve == 0

    # ---------------- ₹2 → 5L ----------------
    await insert_coin_and_wait(dut, 1)
    await give_flow_pulses(dut, 5)
    await ClockCycles(dut.clk, 5)

    liters, _ = get_outputs(dut)
    assert liters == 5

    # ---------------- ₹5 → 20L ----------------
    await insert_coin_and_wait(dut, 2)
    await give_flow_pulses(dut, 20)
    await ClockCycles(dut.clk, 10)

    liters, _ = get_outputs(dut)
    assert liters == 20

    # ---------------- ₹10 → 40L ----------------
    await insert_coin_and_wait(dut, 3)
    await give_flow_pulses(dut, 40)
    await ClockCycles(dut.clk, 20)

    liters, _ = get_outputs(dut)
    assert liters == 40
