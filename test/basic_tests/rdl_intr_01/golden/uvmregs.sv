//   Ordt 170607.01 autogenerated file 
//   Input: ./rdl_intr_01/test.rdl
//   Parms: ./rdl_intr_01/test.parms
//   Date: Wed Jun 07 12:53:06 EDT 2017
//

import uvm_pkg::*;
import ordt_uvm_reg_pkg::*;

// Register a_reg
class reg_foo_bar_a_reg extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl fld1;
  rand uvm_reg_field_rdl fld2;
  
  function new(string name = "reg_foo_bar_a_reg");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.fld1 = new("fld1");
    this.fld1.set_rdl_access_info(1, 1, 1, 1, 1, 0);
    this.fld1.configure(this, 10, 0, "RW", 1, 10'h0, 1, 1, 0);
    this.fld2 = new("fld2");
    this.fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fld2.configure(this, 1, 15, "RW", 0, 0, 1, 1, 0);
    this.fld2.has_reset(.delete(1));
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "fld1"}, 0, 10);
    add_hdl_path_slice({rdl_reg_name, "fld2"}, 15, 1);
  endfunction: build
  
  virtual function void add_callbacks();
  endfunction: add_callbacks
  
endclass : reg_foo_bar_a_reg

// Register intr_reg1
class reg_foo_bar_intr_reg1 extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl_interrupt int1;
  rand uvm_reg_field_rdl_interrupt int2;
  
  function new(string name = "reg_foo_bar_intr_reg1");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.int1 = new("int1");
    this.int1.set_rdl_access_info(1, 1, 0, 0, 0, 0);
    this.int1.add_intr(0, 0, "", 0);
    this.int1.configure(this, 1, 0, "W1C", 1, 1'h0, 1, 1, 0);
    this.int2 = new("int2");
    this.int2.set_rdl_access_info(1, 1, 0, 0, 0, 0);
    this.int2.add_intr(0, 0, "", 0);
    this.int2.configure(this, 1, 1, "W1C", 1, 1'h0, 1, 1, 0);
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "int1"}, 0, 1);
    add_hdl_path_slice({rdl_reg_name, "int2"}, 1, 1);
  endfunction: build
  
  virtual function void add_callbacks();
  endfunction: add_callbacks
  
  virtual function void get_intr_fields(ref uvm_reg_field fields[$]); // return all source interrupt fields
    uvm_reg_field f[$];
    uvm_reg_field_rdl rdl_f;
    uvm_reg_field_rdl_interrupt rdl_intr_f;
    get_fields(f);
    foreach(f[i]) begin
      $cast(rdl_f, f[i]);
      if (rdl_f.is_interrupt()) begin
        $cast(rdl_intr_f, rdl_f);
        rdl_intr_f.get_intr_fields(fields);
      end
    end
  endfunction: get_intr_fields
  
  virtual task get_active_intr_fields(ref uvm_reg_field fields[$], input bit is_halt, input uvm_path_e path = UVM_DEFAULT_PATH); // return all active source intr/halt fields
    uvm_reg_field f[$];
    uvm_reg_field_rdl rdl_f;
    uvm_reg_field_rdl_interrupt rdl_intr_f;
    uvm_status_e status;
    uvm_reg_data_t value;
    read(status, value, path);
    get_fields(f);
    foreach(f[i]) begin
      $cast(rdl_f, f[i]);
      if (rdl_f.is_interrupt() && rdl_f.get()) begin
        $cast(rdl_intr_f, rdl_f);
        rdl_intr_f.get_active_intr_fields(fields, is_halt, path);
      end
    end
  endtask: get_active_intr_fields
  
endclass : reg_foo_bar_intr_reg1

// Register log_reg1
class reg_foo_bar_log_reg1 extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl err_log;
  
  function new(string name = "reg_foo_bar_log_reg1");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.err_log = new("err_log");
    this.err_log.set_rdl_access_info(1, 1, 0, 1, 0, 1);
    this.err_log.configure(this, 10, 0, "RW", 1, 10'h0, 1, 1, 1);
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "err_log"}, 0, 10);
  endfunction: build
  
  virtual function void add_callbacks();
  endfunction: add_callbacks
  
endclass : reg_foo_bar_log_reg1

// Register log_reg2
class reg_foo_bar_log_reg2 extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl err_log;
  
  function new(string name = "reg_foo_bar_log_reg2");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.err_log = new("err_log");
    this.err_log.set_rdl_access_info(1, 1, 0, 1, 1, 0);
    this.err_log.configure(this, 10, 0, "RW", 1, 10'h0, 1, 1, 1);
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "err_log"}, 0, 10);
  endfunction: build
  
  virtual function void add_callbacks();
  endfunction: add_callbacks
  
endclass : reg_foo_bar_log_reg2

// Register log_reg3
class reg_foo_bar_log_reg3 extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl err_log;
  
  function new(string name = "reg_foo_bar_log_reg3");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.err_log = new("err_log");
    this.err_log.set_rdl_access_info(1, 1, 0, 1, 0, 1);
    this.err_log.configure(this, 10, 0, "RW", 1, 10'h0, 1, 1, 1);
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "err_log"}, 0, 10);
  endfunction: build
  
  virtual function void add_callbacks();
  endfunction: add_callbacks
  
endclass : reg_foo_bar_log_reg3

// Register intr_reg2
class reg_foo_bar_sub_intr_reg2 extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl_interrupt int1;
  rand uvm_reg_field_rdl_interrupt int2;
  
  function new(string name = "reg_foo_bar_sub_intr_reg2");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.int1 = new("int1");
    this.int1.set_rdl_access_info(1, 1, 0, 0, 0, 0);
    this.int1.add_intr(0, 0, "", 0);
    this.int1.configure(this, 1, 0, "W1C", 1, 1'h0, 1, 1, 0);
    this.int2 = new("int2");
    this.int2.set_rdl_access_info(1, 1, 0, 0, 0, 0);
    this.int2.add_intr(0, 0, "", 1);
    this.int2.configure(this, 1, 1, "W1C", 1, 1'h0, 1, 1, 0);
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "int1"}, 0, 1);
    add_hdl_path_slice({rdl_reg_name, "int2"}, 1, 1);
  endfunction: build
  
  virtual function void add_callbacks();
    rdl_mask_intr_field_cbs int2_mask_cb;
    uvm_reg_block m_root_cb_block;
    uvm_reg_block m_cb_block;
    uvm_reg m_cb_reg;
    uvm_reg_field m_cb_field;
    m_root_cb_block = this.get_ancestor(2);
    m_cb_block = m_root_cb_block;
    m_cb_reg = m_cb_block.get_reg_by_name("intr_reg1");
    m_cb_field = m_cb_reg.get_field_by_name("int1");
    int1.set_intr_mask_field(m_cb_field, 1);
    m_cb_field = m_cb_reg.get_field_by_name("int2");
    int2.set_intr_mask_field(m_cb_field, 1);
    int2_mask_cb = new("int2_mask_cb",int2);
    uvm_reg_field_cb::add(this.int2, int2_mask_cb);
  endfunction: add_callbacks
  
  virtual function void get_intr_fields(ref uvm_reg_field fields[$]); // return all source interrupt fields
    uvm_reg_field f[$];
    uvm_reg_field_rdl rdl_f;
    uvm_reg_field_rdl_interrupt rdl_intr_f;
    get_fields(f);
    foreach(f[i]) begin
      $cast(rdl_f, f[i]);
      if (rdl_f.is_interrupt()) begin
        $cast(rdl_intr_f, rdl_f);
        rdl_intr_f.get_intr_fields(fields);
      end
    end
  endfunction: get_intr_fields
  
  virtual task get_active_intr_fields(ref uvm_reg_field fields[$], input bit is_halt, input uvm_path_e path = UVM_DEFAULT_PATH); // return all active source intr/halt fields
    uvm_reg_field f[$];
    uvm_reg_field_rdl rdl_f;
    uvm_reg_field_rdl_interrupt rdl_intr_f;
    uvm_status_e status;
    uvm_reg_data_t value;
    read(status, value, path);
    get_fields(f);
    foreach(f[i]) begin
      $cast(rdl_f, f[i]);
      if (rdl_f.is_interrupt() && rdl_f.get()) begin
        $cast(rdl_intr_f, rdl_f);
        rdl_intr_f.get_active_intr_fields(fields, is_halt, path);
      end
    end
  endtask: get_active_intr_fields
  
endclass : reg_foo_bar_sub_intr_reg2

// Register intr_reg3
class reg_foo_bar_sub_intr_reg3 extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl_interrupt int1;
  rand uvm_reg_field_rdl_interrupt int2;
  
  function new(string name = "reg_foo_bar_sub_intr_reg3");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.int1 = new("int1");
    this.int1.set_rdl_access_info(1, 1, 0, 0, 0, 0);
    this.int1.add_intr(0, 0, "", 0);
    this.int1.configure(this, 1, 0, "W1C", 1, 1'h0, 1, 1, 0);
    this.int2 = new("int2");
    this.int2.set_rdl_access_info(1, 1, 0, 0, 0, 0);
    this.int2.add_intr(0, 0, "", 1);
    this.int2.configure(this, 1, 1, "W1C", 1, 1'h0, 1, 1, 0);
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "int1"}, 0, 1);
    add_hdl_path_slice({rdl_reg_name, "int2"}, 1, 1);
  endfunction: build
  
  virtual function void add_callbacks();
    rdl_mask_intr_field_cbs int2_mask_cb;
    uvm_reg_block m_root_cb_block;
    uvm_reg_block m_cb_block;
    uvm_reg m_cb_reg;
    uvm_reg_field m_cb_field;
    m_root_cb_block = this.get_ancestor(2);
    m_cb_block = uvm_reg_block::find_block("sub", m_root_cb_block);
    m_cb_reg = m_cb_block.get_reg_by_name("intr_reg2");
    m_cb_field = m_cb_reg.get_field_by_name("int1");
    int1.set_intr_mask_field(m_cb_field, 1);
    m_cb_field = m_cb_reg.get_field_by_name("int2");
    int2.set_intr_mask_field(m_cb_field, 1);
    int2_mask_cb = new("int2_mask_cb",int2);
    uvm_reg_field_cb::add(this.int2, int2_mask_cb);
  endfunction: add_callbacks
  
  virtual function void get_intr_fields(ref uvm_reg_field fields[$]); // return all source interrupt fields
    uvm_reg_field f[$];
    uvm_reg_field_rdl rdl_f;
    uvm_reg_field_rdl_interrupt rdl_intr_f;
    get_fields(f);
    foreach(f[i]) begin
      $cast(rdl_f, f[i]);
      if (rdl_f.is_interrupt()) begin
        $cast(rdl_intr_f, rdl_f);
        rdl_intr_f.get_intr_fields(fields);
      end
    end
  endfunction: get_intr_fields
  
  virtual task get_active_intr_fields(ref uvm_reg_field fields[$], input bit is_halt, input uvm_path_e path = UVM_DEFAULT_PATH); // return all active source intr/halt fields
    uvm_reg_field f[$];
    uvm_reg_field_rdl rdl_f;
    uvm_reg_field_rdl_interrupt rdl_intr_f;
    uvm_status_e status;
    uvm_reg_data_t value;
    read(status, value, path);
    get_fields(f);
    foreach(f[i]) begin
      $cast(rdl_f, f[i]);
      if (rdl_f.is_interrupt() && rdl_f.get()) begin
        $cast(rdl_intr_f, rdl_f);
        rdl_intr_f.get_active_intr_fields(fields, is_halt, path);
      end
    end
  endtask: get_active_intr_fields
  
endclass : reg_foo_bar_sub_intr_reg3

// Block sub
class block_foo_bar_sub extends uvm_reg_block_rdl;
  rand reg_foo_bar_sub_intr_reg2 intr_reg2;
  rand reg_foo_bar_sub_intr_reg3 intr_reg3;
  
  function new(string name = "block_foo_bar_sub");
    super.new(name);
  endfunction: new
  
  virtual function void add_callbacks();
    uvm_reg m_regs[$];
    uvm_reg_block  m_blks[$];
    uvm_reg_rdl rg;
    uvm_reg_block_rdl blk;
    this.get_registers(m_regs, UVM_NO_HIER);
    foreach (m_regs[rg_]) begin
      $cast(rg, m_regs[rg_]);
      rg.add_callbacks();
    end
    this.get_blocks(m_blks, UVM_NO_HIER);
    foreach (m_blks[blk_]) begin
      $cast(blk, m_blks[blk_]);
      blk.add_callbacks();
    end
  endfunction: add_callbacks
  
  virtual function void build();
    this.default_map = create_map("", 0, 4, UVM_LITTLE_ENDIAN, 1);
    this.intr_reg2 = new("intr_reg2");
    this.intr_reg2.configure(this, null, "");
    this.intr_reg2.set_rdl_tag("intr_reg2_");
    this.intr_reg2.set_reg_test_info(0, 0, 0);
    this.intr_reg2.build();
    this.default_map.add_reg(this.intr_reg2, `UVM_REG_ADDR_WIDTH'h0, "RW", 0);
    this.intr_reg3 = new("intr_reg3");
    this.intr_reg3.configure(this, null, "");
    this.intr_reg3.set_rdl_tag("intr_reg3_");
    this.intr_reg3.set_reg_test_info(0, 0, 0);
    this.intr_reg3.build();
    this.default_map.add_reg(this.intr_reg3, `UVM_REG_ADDR_WIDTH'h100, "RW", 0);
  endfunction: build
  
  `uvm_object_utils(block_foo_bar_sub)
endclass : block_foo_bar_sub

// Register rst_reg
class reg_foo_bar_rst_reg extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl fld2;
  rand uvm_reg_field_rdl fld1;
  rand uvm_reg_field_rdl fld3;
  rand uvm_reg_field_rdl fld4;
  
  function new(string name = "reg_foo_bar_rst_reg");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.fld2 = new("fld2");
    this.fld2.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fld2.configure(this, 4, 0, "RW", 0, 4'h2, 1, 1, 0);
    this.fld1 = new("fld1");
    this.fld1.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fld1.configure(this, 4, 4, "RW", 0, 4'h1, 1, 1, 0);
    this.fld3 = new("fld3");
    this.fld3.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fld3.configure(this, 3, 8, "RW", 0, 3'h3, 1, 1, 0);
    this.fld4 = new("fld4");
    this.fld4.set_rdl_access_info(1, 1, 1, 0, 0, 0);
    this.fld4.configure(this, 3, 11, "RW", 0, 3'h4, 1, 1, 0);
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "fld2"}, 0, 4);
    add_hdl_path_slice({rdl_reg_name, "fld1"}, 4, 4);
    add_hdl_path_slice({rdl_reg_name, "fld3"}, 8, 3);
    add_hdl_path_slice({rdl_reg_name, "fld4"}, 11, 3);
  endfunction: build
  
  virtual function void add_callbacks();
  endfunction: add_callbacks
  
endclass : reg_foo_bar_rst_reg

// Block bar
class block_foo_bar extends uvm_reg_block_rdl;
  rand reg_foo_bar_a_reg a_reg[2];
  rand reg_foo_bar_intr_reg1 intr_reg1;
  rand reg_foo_bar_log_reg1 log_reg1;
  rand reg_foo_bar_log_reg2 log_reg2;
  rand reg_foo_bar_log_reg3 log_reg3;
  rand block_foo_bar_sub sub;
  rand reg_foo_bar_rst_reg rst_reg;
  
  function new(string name = "block_foo_bar");
    super.new(name);
  endfunction: new
  
  virtual function void add_callbacks();
    uvm_reg m_regs[$];
    uvm_reg_block  m_blks[$];
    uvm_reg_rdl rg;
    uvm_reg_block_rdl blk;
    this.get_registers(m_regs, UVM_NO_HIER);
    foreach (m_regs[rg_]) begin
      $cast(rg, m_regs[rg_]);
      rg.add_callbacks();
    end
    this.get_blocks(m_blks, UVM_NO_HIER);
    foreach (m_blks[blk_]) begin
      $cast(blk, m_blks[blk_]);
      blk.add_callbacks();
    end
  endfunction: add_callbacks
  
  virtual function void build();
    this.default_map = create_map("", 0, 4, UVM_LITTLE_ENDIAN, 1);
    foreach (this.a_reg[i]) begin
      this.a_reg[i] = new($psprintf("a_reg [%0d]",i));
      this.a_reg[i].configure(this, null, "");
      this.a_reg[i].set_rdl_tag($psprintf("a_reg_%0d_",i));
      this.a_reg[i].set_reg_test_info(0, 0, 0);
      this.a_reg[i].build();
      this.default_map.add_reg(this.a_reg[i], `UVM_REG_ADDR_WIDTH'h0+i*`UVM_REG_ADDR_WIDTH'h4, "RW", 0);
    end
    this.intr_reg1 = new("intr_reg1");
    this.intr_reg1.configure(this, null, "");
    this.intr_reg1.set_rdl_tag("intr_reg1_");
    this.intr_reg1.set_reg_test_info(0, 0, 0);
    this.intr_reg1.build();
    this.default_map.add_reg(this.intr_reg1, `UVM_REG_ADDR_WIDTH'h100, "RW", 0);
    this.log_reg1 = new("log_reg1");
    this.log_reg1.configure(this, null, "");
    this.log_reg1.set_rdl_tag("log_reg1_");
    this.log_reg1.set_reg_test_info(0, 0, 0);
    this.log_reg1.build();
    this.default_map.add_reg(this.log_reg1, `UVM_REG_ADDR_WIDTH'h104, "RW", 0);
    this.log_reg2 = new("log_reg2");
    this.log_reg2.configure(this, null, "");
    this.log_reg2.set_rdl_tag("log_reg2_");
    this.log_reg2.set_reg_test_info(0, 0, 0);
    this.log_reg2.build();
    this.default_map.add_reg(this.log_reg2, `UVM_REG_ADDR_WIDTH'h108, "RW", 0);
    this.log_reg3 = new("log_reg3");
    this.log_reg3.configure(this, null, "");
    this.log_reg3.set_rdl_tag("log_reg3_");
    this.log_reg3.set_reg_test_info(0, 0, 0);
    this.log_reg3.build();
    this.default_map.add_reg(this.log_reg3, `UVM_REG_ADDR_WIDTH'h10c, "RW", 0);
    this.sub = block_foo_bar_sub::type_id::create("sub",, get_full_name());
    this.sub.configure(this, "");
    this.sub.set_rdl_tag("sub_");
    this.sub.build();
    this.default_map.add_submap(this.sub.default_map, `UVM_REG_ADDR_WIDTH'h200);
    this.rst_reg = new("rst_reg");
    this.rst_reg.configure(this, null, "");
    this.rst_reg.set_rdl_tag("rst_reg_");
    this.rst_reg.set_reg_test_info(0, 0, 0);
    this.rst_reg.build();
    this.default_map.add_reg(this.rst_reg, `UVM_REG_ADDR_WIDTH'h304, "RW", 0);
  endfunction: build
  
  `uvm_object_utils(block_foo_bar)
endclass : block_foo_bar

// Register merge
class reg_foo_intr_cascade_merge extends uvm_reg_rdl;
  string m_rdl_tag;
  rand uvm_reg_field_rdl_interrupt fld1;
  rand uvm_reg_field_rdl_interrupt fld2;
  
  function new(string name = "reg_foo_intr_cascade_merge");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction: new
  
  virtual function void build();
    string rdl_reg_name;
    this.fld1 = new("fld1");
    this.fld1.set_rdl_access_info(1, 0, 0, 0, 0, 0);
    this.fld1.add_intr(0, 0, "", 0);
    this.fld1.configure(this, 1, 0, "RO", 1, 1'h0, 1, 0, 0);
    this.fld2 = new("fld2");
    this.fld2.set_rdl_access_info(1, 0, 0, 0, 0, 0);
    this.fld2.add_intr(0, 0, "", 0);
    this.fld2.configure(this, 1, 1, "RO", 1, 1'h0, 1, 0, 0);
    
    rdl_reg_name = get_rdl_name("rg_");
    add_hdl_path_slice({rdl_reg_name, "fld1"}, 0, 1);
    add_hdl_path_slice({rdl_reg_name, "fld2"}, 1, 1);
  endfunction: build
  
  virtual function void add_callbacks();
    uvm_reg_block m_root_cb_block;
    uvm_reg_block m_cb_block;
    uvm_reg m_cb_reg;
    uvm_reg_field m_cb_field;
    m_root_cb_block = this.get_ancestor(2);
    m_cb_block = uvm_reg_block::find_block("bar", m_root_cb_block);
    m_cb_reg = m_cb_block.get_reg_by_name("intr_reg1");
    fld1.set_cascade_intr_reg(m_cb_reg, 0);
  endfunction: add_callbacks
  
  virtual function void get_intr_fields(ref uvm_reg_field fields[$]); // return all source interrupt fields
    uvm_reg_field f[$];
    uvm_reg_field_rdl rdl_f;
    uvm_reg_field_rdl_interrupt rdl_intr_f;
    get_fields(f);
    foreach(f[i]) begin
      $cast(rdl_f, f[i]);
      if (rdl_f.is_interrupt()) begin
        $cast(rdl_intr_f, rdl_f);
        rdl_intr_f.get_intr_fields(fields);
      end
    end
  endfunction: get_intr_fields
  
  virtual task get_active_intr_fields(ref uvm_reg_field fields[$], input bit is_halt, input uvm_path_e path = UVM_DEFAULT_PATH); // return all active source intr/halt fields
    uvm_reg_field f[$];
    uvm_reg_field_rdl rdl_f;
    uvm_reg_field_rdl_interrupt rdl_intr_f;
    uvm_status_e status;
    uvm_reg_data_t value;
    read(status, value, path);
    get_fields(f);
    foreach(f[i]) begin
      $cast(rdl_f, f[i]);
      if (rdl_f.is_interrupt() && rdl_f.get()) begin
        $cast(rdl_intr_f, rdl_f);
        rdl_intr_f.get_active_intr_fields(fields, is_halt, path);
      end
    end
  endtask: get_active_intr_fields
  
endclass : reg_foo_intr_cascade_merge

// Block intr_cascade
class block_foo_intr_cascade extends uvm_reg_block_rdl;
  rand reg_foo_intr_cascade_merge merge;
  
  function new(string name = "block_foo_intr_cascade");
    super.new(name);
  endfunction: new
  
  virtual function void add_callbacks();
    uvm_reg m_regs[$];
    uvm_reg_block  m_blks[$];
    uvm_reg_rdl rg;
    uvm_reg_block_rdl blk;
    this.get_registers(m_regs, UVM_NO_HIER);
    foreach (m_regs[rg_]) begin
      $cast(rg, m_regs[rg_]);
      rg.add_callbacks();
    end
    this.get_blocks(m_blks, UVM_NO_HIER);
    foreach (m_blks[blk_]) begin
      $cast(blk, m_blks[blk_]);
      blk.add_callbacks();
    end
  endfunction: add_callbacks
  
  virtual function void build();
    this.default_map = create_map("", 0, 4, UVM_LITTLE_ENDIAN, 1);
    this.merge = new("merge");
    this.merge.configure(this, null, "");
    this.merge.set_rdl_tag("merge_");
    this.merge.set_reg_test_info(0, 0, 0);
    this.merge.build();
    this.default_map.add_reg(this.merge, `UVM_REG_ADDR_WIDTH'h0, "RO", 0);
  endfunction: build
  
  `uvm_object_utils(block_foo_intr_cascade)
endclass : block_foo_intr_cascade

// Base block
class block_foo extends uvm_reg_block_rdl;
  rand block_foo_bar bar;
  rand block_foo_intr_cascade intr_cascade;
  
  function new(string name = "block_foo");
    super.new(name);
  endfunction: new
  
  virtual function void add_callbacks();
    uvm_reg m_regs[$];
    uvm_reg_block  m_blks[$];
    uvm_reg_rdl rg;
    uvm_reg_block_rdl blk;
    this.get_registers(m_regs, UVM_NO_HIER);
    foreach (m_regs[rg_]) begin
      $cast(rg, m_regs[rg_]);
      rg.add_callbacks();
    end
    this.get_blocks(m_blks, UVM_NO_HIER);
    foreach (m_blks[blk_]) begin
      $cast(blk, m_blks[blk_]);
      blk.add_callbacks();
    end
  endfunction: add_callbacks
  
  virtual function void build();
    this.default_map = create_map("", `UVM_REG_ADDR_WIDTH'h0, 4, UVM_LITTLE_ENDIAN, 1);
    this.set_rdl_address_map(1);
    this.set_rdl_address_map_hdl_path({`FOO_PIO_INSTANCE_PATH, ".pio_logic"});
    this.bar = block_foo_bar::type_id::create("bar",, get_full_name());
    this.bar.configure(this, "");
    this.bar.set_rdl_tag("bar_");
    this.bar.build();
    this.default_map.add_submap(this.bar.default_map, `UVM_REG_ADDR_WIDTH'h0);
    this.intr_cascade = block_foo_intr_cascade::type_id::create("intr_cascade",, get_full_name());
    this.intr_cascade.configure(this, "");
    this.intr_cascade.set_rdl_tag("intr_cascade_");
    this.intr_cascade.build();
    this.default_map.add_submap(this.intr_cascade.default_map, `UVM_REG_ADDR_WIDTH'h1000);
    set_hdl_path_root({`FOO_PIO_INSTANCE_PATH, ".pio_logic"});
    this.add_callbacks();
  endfunction: build
  
  `uvm_object_utils(block_foo)
endclass : block_foo
