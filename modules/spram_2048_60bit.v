module spram_2048_60bit (
    clk,
    address,
    wren,
    data,
    out
);
parameter AWIDTH=11;
parameter NUM_WORDS=2048;
parameter DWIDTH=60;
input clk;
input [(AWIDTH-1):0] address;
input  wren;
input [(DWIDTH-1):0] data;
output reg [(DWIDTH-1):0] out;

`ifdef SIMULATION_MEMORY

reg [DWIDTH-1:0] ram[NUM_WORDS-1:0];
always @ (posedge clk) begin 
  if (wren) begin
      ram[address] <= data;
  end
  else begin
      out <= ram[address];
  end
end
  
`else

defparam u_single_port_ram.ADDR_WIDTH = AWIDTH;
defparam u_single_port_ram.DATA_WIDTH = DWIDTH;

single_port_ram u_single_port_ram(
.addr(address),
.we(wren),
.data(data),
.out(out),
.clk(clk)
);

`endif

endmodule

