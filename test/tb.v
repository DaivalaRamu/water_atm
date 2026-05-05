`default_nettype none
`timescale 1ns / 1ps

module tb ();
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;

  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // -------- DUT --------
  tt_um_water_atm user_project (

`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif

      .ui_in  (ui_in),
      .uo_out (uo_out),
      .uio_in (uio_in),
      .uio_out(uio_out),
      .uio_oe (uio_oe),
      .ena    (ena),
      .clk    (clk),
      .rst_n  (rst_n)
  );

  // -------- CLOCK --------
  always #5 clk = ~clk;

  // -------- TEST --------
  initial begin
    clk = 0;
    rst_n = 0;
    ena = 1;
    ui_in = 0;
    uio_in = 0;

    // Reset
    #20;
    rst_n = 1;

    // -------- ₹1 TEST --------
    // coin_1 = ui_in[0]
    #10 ui_in[0] = 1;  
    #10 ui_in[0] = 0;

    repeat (2) begin
      #10 ui_in[4] = 1;  // flow_sensor
      #10 ui_in[4] = 0;
    end

    #100;

    // -------- ₹2 TEST --------
    #10 ui_in[1] = 1;
    #10 ui_in[1] = 0;

    repeat (5) begin
      #10 ui_in[4] = 1;
      #10 ui_in[4] = 0;
    end

    #100;

    // -------- ₹5 TEST --------
    #10 ui_in[2] = 1;
    #10 ui_in[2] = 0;

    repeat (20) begin
      #10 ui_in[4] = 1;
      #10 ui_in[4] = 0;
    end

    #100;

    // -------- ₹10 TEST --------
    #10 ui_in[3] = 1;
    #10 ui_in[3] = 0;

    repeat (40) begin
      #10 ui_in[4] = 1;
      #10 ui_in[4] = 0;
    end

    #200;
    $finish;
  end

endmodule
