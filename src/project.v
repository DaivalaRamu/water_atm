`default_nettype none

module tt_um_water_atm (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire coin_1      = ui_in[0];
    wire coin_2      = ui_in[1];
    wire coin_5      = ui_in[2];
    wire coin_10     = ui_in[3];
    wire flow_sensor = ui_in[4];

    reg valve_on;
    reg [7:0] liters;

    assign uo_out[0]   = valve_on;
    assign uo_out[7:1] = liters[6:0];

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    localparam IDLE=0, SET=1, DISP=2, DONE=3;
    reg [1:0] state;

    reg [7:0] target;
    reg [7:0] coin_reg;
    reg [15:0] timer;
    reg [15:0] time_limit;

    reg flow_d1, flow_d2;
    always @(posedge clk) begin
        flow_d1 <= flow_sensor;
        flow_d2 <= flow_d1;
    end
    wire flow_sync = flow_d2;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            liters <= 0;
            valve_on <= 0;
            coin_reg <= 0;
            target <= 0;
            timer <= 0;
            time_limit <= 0;
        end else begin
            case(state)

            IDLE: begin
                liters <= 0;
                valve_on <= 0;
                timer <= 0;

                if (coin_1)      begin coin_reg <= 1;  state <= SET; end
                else if (coin_2) begin coin_reg <= 2;  state <= SET; end
                else if (coin_5) begin coin_reg <= 5;  state <= SET; end
                else if (coin_10)begin coin_reg <= 10; state <= SET; end
            end

            SET: begin
                case(coin_reg)
                    1:  begin target <= 2;  time_limit <= 20;  end
                    2:  begin target <= 5;  time_limit <= 50;  end
                    5:  begin target <= 20; time_limit <= 200; end
                    10: begin target <= 40; time_limit <= 400; end
                endcase
                timer <= 0;
                state <= DISP;
            end

            DISP: begin
                valve_on <= 1;
                timer <= timer + 1;

                if (flow_sync && liters < target)
                    liters <= liters + 1;

                if ((liters >= target && target != 0) || (timer >= time_limit)) begin
                    valve_on <= 0;
                    state <= DONE;
                end
            end

            DONE: state <= IDLE;

            endcase
        end
    end

    wire _unused = &{ena, uio_in, 1'b0};

endmodule
