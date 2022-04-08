import yaml
import random


# need to add some random no. xor/or/and operations
def interface_algorithm(f, interface_name, input_bits, output_bits):

    f.writelines("\n")
    f.writelines("module " + interface_name + "(input reg [" + str(int(input_bits - 1)) + ":0] inp, " + "output reg [" + str(int(output_bits - 1)) + ":0] outp);" + "\n")

    list1 = ["fsm","xor_module"]
    func = random.choice(list1)

    if input_bits == output_bits:
        f.writelines("always@(posedge clk) begin \n")
        f.writelines("outp <= inp" + " ; \n") # remove FFFF and make random integer
        f.writelines("end \n")
        f.writelines("endmodule \n")
        print("module " + interface_name + " generated \n")
        return

    if input_bits < output_bits:
        round_down = int(output_bits/input_bits)
        f.writelines("always@(posedge clk) begin \n")

        for i in range(round_down):
            f.writelines("outp[" + str(int(((i+1)*input_bits)-1)) + ":" + str(int(i*input_bits)) + "] <= inp ; \n" )
        if output_bits%input_bits != 0:
            f.writelines("outp[" + str(int(output_bits - 1)) + ":" + str(int(output_bits - (output_bits%input_bits) )) + "] <= inp[" + str(int( (output_bits%input_bits) - 1 )) + ":0] ; \n")
        f.writelines("end \n")
        f.writelines("endmodule \n")
        print("module " + interface_name + " generated \n")
        return

    if input_bits > output_bits:
        #iter = int(input_bits/output_bits)
        L = "intermediate_reg"
        i = 0
        #f.writelines("reg [" + str(int(input_bits -1 )) + ":0]" + L + "_" + str(i) + "; \n" )
        #f.writelines("always@(posedge clk) begin \n")
        #f.writelines(L + "_" + str(i) + " <= inp; \n" )
        #f.writelines("end \n \n")
        #if int(input_bits/output_bits) > 2:
        loop = 1
        new_input_bits = input_bits

        while loop:

            if i == 0:
                f.writelines("reg [" + str(int(new_input_bits -1 )) + ":0]" + L + "_" + str(i) + "; \n" )
                f.writelines("always@(posedge clk) begin \n")
                f.writelines(L + "_" + str(i) + " <= inp; \n" )
                f.writelines("end \n \n")
                #continue   # not sure if this is needed here
            else:
                pass

            if new_input_bits%2 == 1:  #if it is odd
                if output_bits%2 == 1:
                    if i == 0:
                        f.writelines("always@(posedge clk) begin \n")
                        f.writelines("outp[" + str(int(output_bits - 1)) + "] <= " + L + "_" + str(i) + "[" + str(int(new_input_bits - 1)) + "]; \n" )
                        f.writelines("end \n \n")
                    else:
                        f.writelines("always@(posedge clk) begin \n")
                        f.writelines("outp[" + str(int(output_bits - 1)) + "] <= " + L + "_" + str(int(i-1)) + "[" + str(int(new_input_bits - 1)) + "]; \n" )
                        f.writelines("end \n \n")
                    output_bits = output_bits -1
                    new_input_bits = new_input_bits -1
                    #now both are even
                else: #if output bits are not odd, we need to make input_bits as even
                    if i ==0:
                        f.writelines("always@(posedge clk) begin \n")
                        f.writelines(L + "_" + str(i) + "[" + str(int(new_input_bits-2)) + "]" " <= " + L + "_" + str(i) + "[" + str(int(new_input_bits-1)) + "]" + "^" + L + "_" + str(i) + "[" + str(int(new_input_bits-2)) + "] ; \n" )
                        f.writelines("end \n \n")
                    else:
                        f.writelines("always@(posedge clk) begin \n")
                        f.writelines(L + "_" + str(int(i-1)) + "[" + str(int(new_input_bits-2)) + "]" " <= " + L + "_" + str(int(i-1)) + "[" + str(int(new_input_bits-1)) + "]" + "^" + L + "_" + str(int(i-1)) + "[" + str(int(new_input_bits-2)) + "] ; \n" )
                        f.writelines("end \n \n")
                    new_input_bits = new_input_bits -1 #we have reduced the intermediate_reg bitwidth by 1 (made it even)
            else:
                pass
            if i == 0:
                i = i + 1
                continue
            else:
                #since new_input_bits is even we can divide it by two.
                if new_input_bits > output_bits: #if input bits greater than output bits

                    f.writelines("reg [" + str(int((new_input_bits/2) -1 )) + ":0]" + L + "_" + str(i) + "; \n \n" )
                    #f.writelines("always@(posedge clk) begin \n")


                    for k in range(int(new_input_bits/2)):
                        #f.writelines(L + "_" + str(i) + "[" + str(int((new_input_bits/2) -1 - k)) + "]" "<= " + L +"_" + str(int(i-1)) + "[" + str(int(new_input_bits - 1 - (2*k)) ) + "]" + "^" + L + "_" + str(int(i-1)) + "[" + str(int(new_input_bits - 2 - (2*k)) ) + "] ;\n" )
                        func = random.choice(list1)
                        f.writelines(func + " " + func + "_inst" + "_" + str(i) + "_" + str(k) + "(.i1(" + L +"_" + str(int(i-1)) + "[" + str(int(new_input_bits - 1 - (2*k)) ) + "]" + "),.i2(" + L + "_" + str(int(i-1)) + "[" + str(int(new_input_bits - 2 - (2*k)) ) + "]" + "),.o(" + L + "_" + str(i) + "[" + str(int((new_input_bits/2) -1 - k)) + "]" + "); \n")

                    #f.writelines("end \n \n")
                    new_input_bits = new_input_bits/2
                    i = i + 1
                    continue

                if new_input_bits < output_bits:

                    round_down = int(output_bits/new_input_bits)
                    f.writelines("always@(posedge clk) begin \n")
                    for z in range(round_down):
                        f.writelines("outp [" + str(int(((z+1)*new_input_bits)-1)) + ":" + str(int(z*new_input_bits)) + "] <= " + L + "_" + str(int(i-1)) + "; \n" )
                    if output_bits%new_input_bits != 0:
                        f.writelines("outp[" + str(int(output_bits - 1)) + ":" + str(int(output_bits - (output_bits%new_input_bits) )) + "] <= " + L + "_" + str(int(i-1)) + "[" + str(int( (output_bits%new_input_bits) - 1 )) + ":0] ; \n")
                    f.writelines("end \n")
                    i = i+1
                    loop = 0
                    break

                if new_input_bits == output_bits:

                    f.writelines("always@(posedge clk) begin \n")
                    f.writelines("outp[" + str(int(output_bits - 1)) +  "] <= " + L + "_" + str(int(i-1)) + " ; \n")
                    f.writelines("end \n")
                    i = i+1
                    loop = 0
                    break

            if new_input_bits == 0:
                loop = 0
                continue;

    f.writelines("endmodule \n \n")
    print("module " + interface_name + " generated \n")
