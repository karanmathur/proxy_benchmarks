module dbram_4096_60bit (
    clk,
    address_a,
    address_b,
    wren_a,
    wren_b,
    data_a,
    data_b,
    out_a,
    out_b
); 

parameter AWIDTH=12;
parameter NUM_WORDS=4096;
parameter DWIDTH=60;
input clk;
input [(AWIDTH-1):0] address_a;
input [(AWIDTH-1):0] address_b;
input  wren_a;
input  wren_b;
input [(DWIDTH-1):0] data_a;
input [(DWIDTH-1):0] data_b;
output reg [(DWIDTH-1):0] out_a;
output reg [(DWIDTH-1):0] out_b;

reg count; 

always@(posedge clk) begin 

if (reset) begin 
	count <= 1'b0; 
end
else begin 
	count <= count + 1'b1; 
end

end

wire [(AWIDTH-1):0] address_a1,address_a2;
wire [(AWIDTH-1):0] address_b1,address_b2;
wire  wren_a1,wren_a2;
wire  wren_b1,wren_b2;
wire [(DWIDTH-1):0] data_a1,data_a2;
wire [(DWIDTH-1):0] data_b1,data_b2;
wire [(DWIDTH-1):0] out_a1,out_a2;
wire [(DWIDTH-1):0] out_b1,out_b2;

assign address_a = count?address_a1:address_a2; 
assign address_b = count?address_b1:address_b2;
assign wren_a = count?wren_a1:wren_a2;
assign wren_b = count?wren_b1:wren_b2;
assign data_a = count?data_a1:data_a2;
assign data_b = count?data_b1:data_b2;
assign out_a = count?out_a1:out_a2;
assign out_b = count?out_b1:out_b2;

dpram_4096_60bit_db inst1(.clk(clk),.address_a(address_a1),.address_b(address_b1),.wren_a(wren_a1),.wren_b(wren_b1),.data_a(data_a1),.data_b(data_b1),.out_a(out_a1),.out_b(out_b1));
dpram_4096_60bit_db inst2(.clk(clk),.address_a(address_a2),.address_b(address_b2),.wren_a(wren_a2),.wren_b(wren_b2),.data_a(data_a2),.data_b(data_b2),.out_a(out_a2),.out_b(out_b2));


endmodule

module dpram_4096_60bit_db (
    clk,
    address_a,
    address_b,
    wren_a,
    wren_b,
    data_a,
    data_b,
    out_a,
    out_b
);
parameter AWIDTH=12;
parameter NUM_WORDS=4096;
parameter DWIDTH=60;
input clk;
input [(AWIDTH-1):0] address_a;
input [(AWIDTH-1):0] address_b;
input  wren_a;
input  wren_b;
input [(DWIDTH-1):0] data_a;
input [(DWIDTH-1):0] data_b;
output reg [(DWIDTH-1):0] out_a;
output reg [(DWIDTH-1):0] out_b;

`ifdef SIMULATION_MEMORY

reg [DWIDTH-1:0] ram[NUM_WORDS-1:0];
always @ (posedge clk) begin 
  if (wren_a) begin
      ram[address_a] <= data_a;
  end
  else begin
      out_a <= ram[address_a];
  end
end
  
always @ (posedge clk) begin 
  if (wren_b) begin
      ram[address_b] <= data_b;
  end 
  else begin
      out_b <= ram[address_b];
  end
end

`else

dual_port_ram u_dual_port_ram(
.addr1(address_a),
.we1(wren_a),
.data1(data_a),
.out1(out_a),
.addr2(address_b),
.we2(wren_b),
.data2(data_b),
.out2(out_b),
.clk(clk)
);

`endif
endmodule
