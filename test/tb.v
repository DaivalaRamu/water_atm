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
    await ClockCycles(dut.clk, 6)


async def flow_pulse(dut):
    dut.ui_in.value = (1 << 4)
    await ClockCycles(dut.clk, 4)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 3)


async def give_flow(dut, count):
    for _ in range(count):
        await flow_pulse(dut)


async def wait_for_liters(dut, expected):
    for _ in range(50):
        liters, valve = get_outputs(dut)
        if liters == expected:
            return liters, valve
        await ClockCycles(dut.clk, 1)
    return liters, valve


@cocotb.test()
async def test_water_atm(dut):

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # ₹1
    await insert_coin(dut, 0)
    await give_flow(dut, 2)
    liters, valve = await wait_for_liters(dut, 2)
    assert liters == 2

    # ₹2
    await insert_coin(dut, 1)
    await give_flow(dut, 5)
    liters, _ = await wait_for_liters(dut, 5)
    assert liters == 5

    # ₹5
    await insert_coin(dut, 2)
    await give_flow(dut, 20)
    liters, _ = await wait_for_liters(dut, 20)
    assert liters == 20

    # ₹10
    await insert_coin(dut, 3)
    await give_flow(dut, 40)
    liters, _ = await wait_for_liters(dut, 40)
    assert liters == 40
