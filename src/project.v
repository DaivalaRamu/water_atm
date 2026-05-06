module water_atm(
    input clk,
    input rst,
    input coin_1,
    input coin_2,
    input coin_5,
    input coin_10,
    input flow_sensor,

    output reg valve_on,
    output reg [7:0] liters
);

localparam IDLE = 2'd0,
           SET  = 2'd1,
           DISP = 2'd2,
           DONE = 2'd3;

reg [1:0] state;

reg [7:0] target;
reg [7:0] coin_reg;
reg [15:0] timer;
reg [15:0] time_limit;

// 🔹 Flow sensor synchronizer (for safe hardware operation)
reg flow_d1, flow_d2;
always @(posedge clk) begin
    flow_d1 <= flow_sensor;
    flow_d2 <= flow_d1;
end

wire flow_sync = flow_d2;

always @(posedge clk or posedge rst) begin
    if (rst) begin
        state <= IDLE;
        liters <= 0;
        valve_on <= 0;
        coin_reg <= 0;
        target <= 0;
        timer <= 0;
        time_limit <= 0;
    end else begin
        case (state)

        // -------- IDLE --------
        IDLE: begin
            liters <= 0;
            valve_on <= 0;
            timer <= 0;

            if (coin_1)      begin coin_reg <= 8'd1;  state <= SET; end
            else if (coin_2) begin coin_reg <= 8'd2;  state <= SET; end
            else if (coin_5) begin coin_reg <= 8'd5;  state <= SET; end
            else if (coin_10)begin coin_reg <= 8'd10; state <= SET; end
        end

        // -------- SET --------
        SET: begin
            case (coin_reg)
                8'd1:  begin target <= 8'd2;  time_limit <= 16'd20;  end
                8'd2:  begin target <= 8'd5;  time_limit <= 16'd50;  end
                8'd5:  begin target <= 8'd20; time_limit <= 16'd200; end
                8'd10: begin target <= 8'd40; time_limit <= 16'd400; end
                default: begin target <= 8'd0; time_limit <= 16'd0; end
            endcase

            timer <= 0;
            state <= DISP;
        end

        // -------- DISP --------
        DISP: begin
            valve_on <= 1;
            timer <= timer + 1;

            if (flow_sync && (liters < target)) begin
                liters <= liters + 1;
            end

            if ((liters >= target && target != 0) || (timer >= time_limit)) begin
                valve_on <= 0;
                state <= DONE;
            end
        end

        // -------- DONE --------
        DONE: begin
            state <= IDLE;
        end

        endcase
    end
end

endmodule
