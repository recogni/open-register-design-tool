//   Ordt 170607.01 autogenerated file 
//   Input: ./rdl_fieldstruct/test.rdl
//   Parms: ./rdl_fieldstruct/test.parms
//   Date: Wed Jun 07 12:53:02 EDT 2017
//

import uvm_pkg::*;
import ordt_uvm_reg_pkg::*;

// Register areg
class reg_foo_areg extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl hier_fs_fs1_fld1;
  rand uvm_reg_field_rdl hier_fs_fs1_fld2;
  rand uvm_reg_field_rdl hier_fs_fld1;
  rand uvm_reg_field_rdl hier_fs_fs2_fld1;
  rand uvm_reg_field_rdl hier_fs_fs2_fld2;
  rand uvm_reg_field_rdl fs3_fld1;
  rand uvm_reg_field_rdl fs3_fld2;
  
  function new(string name = "reg_foo_areg");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.hier_fs_fs1_fld1 = new("hier_fs_fs1_fld1");
    this.hier_fs_fs1_fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.hier_fs_fs1_fld1.configure(this, 4, 0, "RW", 1, 4'h0, 1, 1, 0);
    this.hier_fs_fs1_fld2 = new("hier_fs_fs1_fld2");
    this.hier_fs_fs1_fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.hier_fs_fs1_fld2.configure(this, 1, 4, "RW", 0, 0, 1, 1, 0);
    this.hier_fs_fs1_fld2.has_reset(.delete(1));
    this.hier_fs_fld1 = new("hier_fs_fld1");
    this.hier_fs_fld1.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.hier_fs_fld1.configure(this, 1, 5, "RW", 0, 0, 1, 1, 0);
    this.hier_fs_fld1.has_reset(.delete(1));
    this.hier_fs_fs2_fld1 = new("hier_fs_fs2_fld1");
    this.hier_fs_fs2_fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.hier_fs_fs2_fld1.configure(this, 4, 6, "RW", 1, 4'h0, 1, 1, 0);
    this.hier_fs_fs2_fld2 = new("hier_fs_fs2_fld2");
    this.hier_fs_fs2_fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.hier_fs_fs2_fld2.configure(this, 1, 14, "RW", 0, 0, 1, 1, 0);
    this.hier_fs_fs2_fld2.has_reset(.delete(1));
    this.fs3_fld1 = new("fs3_fld1");
    this.fs3_fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.fs3_fld1.configure(this, 4, 24, "RW", 1, 4'h0, 1, 1, 0);
    this.fs3_fld2 = new("fs3_fld2");
    this.fs3_fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fs3_fld2.configure(this, 1, 28, "RW", 0, 0, 1, 1, 0);
    this.fs3_fld2.has_reset(.delete(1));
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "hier_fs_fs1_fld1"}, 0, 4);
    add_hdl_path_slice({rdl_reg_name, "hier_fs_fs1_fld2"}, 4, 1);
    add_hdl_path_slice({rdl_reg_name, "hier_fs_fld1"}, 5, 1);
    add_hdl_path_slice({rdl_reg_name, "hier_fs_fs2_fld1"}, 6, 4);
    add_hdl_path_slice({rdl_reg_name, "hier_fs_fs2_fld2"}, 14, 1);
    add_hdl_path_slice({rdl_reg_name, "fs3_fld1"}, 24, 4);
    add_hdl_path_slice({rdl_reg_name, "fs3_fld2"}, 28, 1);
  endfunction: build
  
  virtual function void add_callbacks();
  endfunction: add_callbacks
  
endclass : reg_foo_areg

// Register blabla
class reg_foo_blabla extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl fs1_0_fld1;
  rand uvm_reg_field_rdl fs1_0_fld2;
  rand uvm_reg_field_rdl fs1_1_fld1;
  rand uvm_reg_field_rdl fs1_1_fld2;
  rand uvm_reg_field_rdl fs1_2_fld1;
  rand uvm_reg_field_rdl fs1_2_fld2;
  rand uvm_reg_field_rdl fs3_0_fld1;
  rand uvm_reg_field_rdl fs3_0_fld2;
  rand uvm_reg_field_rdl fs3_1_fld1;
  rand uvm_reg_field_rdl fs3_1_fld2;
  
  function new(string name = "reg_foo_blabla");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.fs1_0_fld1 = new("fs1_0_fld1");
    this.fs1_0_fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.fs1_0_fld1.configure(this, 4, 0, "RW", 1, 4'h0, 1, 1, 0);
    this.fs1_0_fld2 = new("fs1_0_fld2");
    this.fs1_0_fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fs1_0_fld2.configure(this, 1, 4, "RW", 0, 0, 1, 1, 0);
    this.fs1_0_fld2.has_reset(.delete(1));
    this.fs1_1_fld1 = new("fs1_1_fld1");
    this.fs1_1_fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.fs1_1_fld1.configure(this, 4, 5, "RW", 1, 4'h0, 1, 1, 0);
    this.fs1_1_fld2 = new("fs1_1_fld2");
    this.fs1_1_fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fs1_1_fld2.configure(this, 1, 9, "RW", 0, 0, 1, 1, 0);
    this.fs1_1_fld2.has_reset(.delete(1));
    this.fs1_2_fld1 = new("fs1_2_fld1");
    this.fs1_2_fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.fs1_2_fld1.configure(this, 4, 10, "RW", 1, 4'h0, 1, 1, 0);
    this.fs1_2_fld2 = new("fs1_2_fld2");
    this.fs1_2_fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fs1_2_fld2.configure(this, 1, 14, "RW", 0, 0, 1, 1, 0);
    this.fs1_2_fld2.has_reset(.delete(1));
    this.fs3_0_fld1 = new("fs3_0_fld1");
    this.fs3_0_fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.fs3_0_fld1.configure(this, 4, 15, "RW", 1, 4'h0, 1, 1, 0);
    this.fs3_0_fld2 = new("fs3_0_fld2");
    this.fs3_0_fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fs3_0_fld2.configure(this, 1, 19, "RW", 0, 0, 1, 1, 0);
    this.fs3_0_fld2.has_reset(.delete(1));
    this.fs3_1_fld1 = new("fs3_1_fld1");
    this.fs3_1_fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.fs3_1_fld1.configure(this, 4, 23, "RW", 1, 4'h0, 1, 1, 0);
    this.fs3_1_fld2 = new("fs3_1_fld2");
    this.fs3_1_fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fs3_1_fld2.configure(this, 1, 27, "RW", 0, 0, 1, 1, 0);
    this.fs3_1_fld2.has_reset(.delete(1));
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "fs1_0_fld1"}, 0, 4);
    add_hdl_path_slice({rdl_reg_name, "fs1_0_fld2"}, 4, 1);
    add_hdl_path_slice({rdl_reg_name, "fs1_1_fld1"}, 5, 4);
    add_hdl_path_slice({rdl_reg_name, "fs1_1_fld2"}, 9, 1);
    add_hdl_path_slice({rdl_reg_name, "fs1_2_fld1"}, 10, 4);
    add_hdl_path_slice({rdl_reg_name, "fs1_2_fld2"}, 14, 1);
    add_hdl_path_slice({rdl_reg_name, "fs3_0_fld1"}, 15, 4);
    add_hdl_path_slice({rdl_reg_name, "fs3_0_fld2"}, 19, 1);
    add_hdl_path_slice({rdl_reg_name, "fs3_1_fld1"}, 23, 4);
    add_hdl_path_slice({rdl_reg_name, "fs3_1_fld2"}, 27, 1);
  endfunction: build
  
  virtual function void add_callbacks();
  endfunction: add_callbacks
  
endclass : reg_foo_blabla

// Base block
class block_foo extends uvm_reg_block_rdl;
  rand reg_foo_areg areg[2];
  rand reg_foo_blabla blabla;
  
  function new(string name = "block_foo");
    super.new(name);
  endfunction: new
  
  virtual function void build();
    this.default_map = create_map("", `UVM_REG_ADDR_WIDTH'h0, 4, UVM_LITTLE_ENDIAN, 1);
    this.set_rdl_address_map(1);
    this.set_rdl_address_map_hdl_path({`FOO_PIO_INSTANCE_PATH, ".pio_logic"});
    foreach (this.areg[i]) begin
      this.areg[i] = new($psprintf("areg [%0d]",i));
      this.areg[i].configure(this, null, "");
      this.areg[i].set_rdl_tag($psprintf("areg_%0d_",i));
      this.areg[i].set_reg_test_info(0, 0, 0);
      this.areg[i].build();
      this.default_map.add_reg(this.areg[i], `UVM_REG_ADDR_WIDTH'h0+i*`UVM_REG_ADDR_WIDTH'h4, "RW", 0);
    end
    this.blabla = new("blabla");
    this.blabla.configure(this, null, "");
    this.blabla.set_rdl_tag("blabla_");
    this.blabla.set_reg_test_info(0, 0, 0);
    this.blabla.build();
    this.default_map.add_reg(this.blabla, `UVM_REG_ADDR_WIDTH'h8, "RW", 0);
    set_hdl_path_root({`FOO_PIO_INSTANCE_PATH, ".pio_logic"});
    this.add_callbacks();
  endfunction: build
  
  `uvm_object_utils(block_foo)
endclass : block_foo
