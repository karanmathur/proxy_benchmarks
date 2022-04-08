module dsp_chain_4_int_sop_2 (clk,reset,ax1,ay1,bx1,by1,ax2,ay2,bx2,by2,ax3,ay3,bx3,by3,ax4,ay4,bx4,by4,result);

input clk; 
input reset; 
input [17:0] ax1, bx1, ax2, bx2, ax3, bx3, ax4, bx4; 
input [18:0] ay1, by1, ay2, by2, ay3, by3, ay4, by4; 
output reg [36:0] result; 

wire [36:0] chainout0, chainout1, chainout2, chainout3; 
wire [36:0] chainin0, chainin1, chainin2, chainin3; 
wire [36:0] resulta1, resulta2, resulta3, resulta4;

assign chainin0 = 37'd0;

int_sop_2 inst1 (.clk(clk),.reset(reset),.ax(ax1),.bx(bx1),.ay(ay1),.by(by1),.mode_sigs(11'd0),.chainin(chainin0),.resulta(resulta1),.chainout(chainout0));
int_sop_2 inst2 (.clk(clk),.reset(reset),.ax(ax2),.bx(bx2),.ay(ay2),.by(by2),.mode_sigs(11'd0),.chainin(chainout0),.resulta(resulta2),.chainout(chainout1));
int_sop_2 inst3 (.clk(clk),.reset(reset),.ax(ax3),.bx(bx3),.ay(ay3),.by(by3),.mode_sigs(11'd0),.chainin(chainout1),.resulta(resulta3),.chainout(chainout2));
int_sop_2 inst4 (.clk(clk),.reset(reset),.ax(ax4),.bx(bx4),.ay(ay4),.by(by4),.mode_sigs(11'd0),.chainin(chainout2),.resulta(resulta4),.chainout(chainout3));

assign result = resulta3;



endmodule 
