# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


def get_outputs(dut):
    val = dut.uo_out.value.to_unsigned()
    liters = (val >> 1) & 0x7F
    valve = val & 0x1
    return liters, valve


async def insert_coin(dut, bit):
    dut.ui_in.value = (1 << bit)
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0
    # Wait for IDLE→SET→DISP + sync latency margin
    await ClockCycles(dut.clk, 6)


async def flow_pulse(dut):
    # Hold HIGH long enough for 2-FF synchronizer
    dut.ui_in.value = (1 << 4)
    await ClockCycles(dut.clk, 4)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 3)


async def give_flow(dut, count):
    for _ in range(count):
        await flow_pulse(dut)


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

    # ₹1 → 2L
    await insert_coin(dut, 0)
    await give_flow(dut, 2)
    await ClockCycles(dut.clk, 10)
    liters, valve = get_outputs(dut)
    assert liters == 2, f"Expected 2L, got {liters}"
    assert valve == 0

    # ₹2 → 5L
    await insert_coin(dut, 1)
    await give_flow(dut, 5)
    await ClockCycles(dut.clk, 10)
    liters, _ = get_outputs(dut)
    assert liters == 5

    # ₹5 → 20L
    await insert_coin(dut, 2)
    await give_flow(dut, 20)
    await ClockCycles(dut.clk, 20)
    liters, _ = get_outputs(dut)
    assert liters == 20

    # ₹10 → 40L
    await insert_coin(dut, 3)
    await give_flow(dut, 40)
    await ClockCycles(dut.clk, 30)
    liters, _ = get_outputs(dut)
    assert liters == 40
