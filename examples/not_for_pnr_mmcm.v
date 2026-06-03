module MMCME2_ADV (
    input CLKIN1,
    input RST,
    input PWRDWN,
    output CLKFBOUT,
    output CLKOUT0,
    output LOCKED
);
endmodule

module top(
    input clk,
    input rst,
    output clk_out,
    output locked
);
    wire clkfb;

    MMCME2_ADV mmcm (
        .CLKIN1(clk),
        .RST(rst),
        .PWRDWN(1'b0),
        .CLKFBOUT(clkfb),
        .CLKOUT0(clk_out),
        .LOCKED(locked)
    );
endmodule
