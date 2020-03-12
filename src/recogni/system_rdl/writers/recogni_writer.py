import json
import os
import re

from jinja2 import Environment
from string import Template as text_template


################################################################################
################################################################################
################################################################################


def _arrayize(nstr):
    try:
        n = int(nstr)
    except:
        return "[%s]" % (nstr)
    if n == 1:
        return ""
    return "[%d]" % (n)


def _systemc_type(t, width_str, template_params=[]):
    if t == "logic":
        return "sc_uint<%s>" % (width_str.lstrip("$"))
    if len(template_params) > 0:
        return t + "<" + ", ".join([t[0] for t in template_params]) + ">"
    return t


def _cpp_type(t, width_str, template_params=[]):
    if t == "logic":
        return "std::bitset<%s>" % (width_str.lstrip("$"))
    if len(template_params) > 0:
        return t + "<" + ", ".join([t[0] for t in template_params]) + ">"
    return t


def _verilog_type(t, width_str):
    if t == "logic":
        try:
            w = int(width_str, 10) - 1
            if w == 0:
                return "logic"
            return "logic[%d:0]" % w
        except:
            pass
        return "logic[%s - 1 : 0]" % (width_str)
    return t


def _c_template_def(t):
    typemap = {
        # Add types that you want to convert here.
    }
    typ = typemap.get(t[0], "int")
    if t[1] == None or t[1] == -1:
        return "%s %s" % (typ, t[0])
    return "%s %s=%s" % (typ, t[0], t[1])


def _c_template_header(tts):
    # Default value initialized template types go last.
    tt = []
    for t in tts:
        if t[1] == None or t[1] == -1:
            tt.append(t)
    for t in tts:
        if t[1] != None and t[1] != -1:
            tt.append(t)
    if len(tt) == 0:
        return ""
    return "template <%s>\n" % ", ".join([_c_template_def(t) for t in tt])


def _c_template_list(tts):
    if len(tts) == 0:
        return ""
    return "<%s>" % ", ".join(["%s" % t[0] for t in tts])


env = Environment(autoescape=False)
env.filters["arrayize"] = _arrayize
env.filters["systemc_type"] = _systemc_type
env.filters["verilog_type"] = _verilog_type
env.filters["cpp_type"] = _cpp_type
env.filters["c_template_header"] = _c_template_header
env.filters["c_template_list"] = _c_template_list


def hydrate(s, d):
    """ `hydrate` takes a given string `s` and a dictionary of config values
        `d` and tries to safe_substitute values from the dictionary into the
        string. If a key is missing from the dictionary, the original string
        is left in place with no substitutions made.
    """
    re_do_eval = re.compile(r"^\$eval\((.*)\)$")
    v = text_template(str(s)).safe_substitute(d)
    m = re_do_eval.match(v)
    if m:
        try:
            return eval(m.group(1))
        except:
            return m.group(1)
    return v


################################################################################

valid_render_types = ["RT_VERILOG", "RT_SYSTEMC", "RT_CPP"]


def fatal(msg):
    print("Fatal error: %s" % (msg))
    os.exit(1)


def ensure_output_dir(base, subpath=None):
    ndir = base if subpath is None else os.path.join(base, subpath)
    os.makedirs(ndir, exist_ok=True)
    return ndir


################################################################################


class Comment:
    template = env.from_string(
        """{% if d.lines | length == 1 and not d.force_block %}
// {{ d.lines[0] }}
{%- elif d.lines | length > 1 or d.force_block %}
/*******************************************************************************
 *
{% for l in d.lines %} * {{ l }}{% endfor %}
 *
 ******************************************************************************/
{%- endif -%}"""
    )

    def __init__(self, content, force_block=False):
        self.lines = content.split("\n")
        self.force_block = force_block
        if len(self.lines) == 1 and len(self.lines[0]) == 0:
            self.lines = []

    def render(self, type="RT_VERILOG"):
        if type not in valid_render_types:
            fatal("Fatal error: Invalid render type encountered!")
        return self.template.render(d=self)


################################################################################


class EnumValue:
    template = env.from_string("    {{d.name}}, // {{d.desc}}")

    def __init__(self, name, desc, config):
        self.name = hydrate(name, config)
        self.desc = hydrate(desc, config)

    def render(self, type="RT_VERILOG"):
        self.render_type = type
        if type not in valid_render_types:
            fatal("Fatal error: Invalid render type encountered!")
        return self.template.render(d=self)


################################################################################


class Enum:
    verilog = env.from_string(
        """{% if d.values | length > 0 %}
typedef enum {{d.type}}[{{d.width | int - 1}}] {
{% for v in d.values %}{{v.render("RT_VERILOG")}}
{% endfor -%}
} {{d.name}};
{%- endif -%}"""
    )

    # TODO (sabhiram) : Fold systemc and cpp together better.
    systemc = env.from_string(
        """{% if d.values | length > 0 %}
enum class {{d.name}}
{
{% for v in d.values %}{{v.render("RT_SYSTEMC")}}
{% endfor -%}
};

inline ostream& operator<<(ostream& os, const {{d.name}}& ev)
{
    switch (ev)
    {
    {%- for v in d.values %}
    case {{d.name}}::{{v.name}}:
        os << "{{v.name}}";
        break;
    {%- endfor %}
    default:
        os << "UnknownEnumError";
    }
    return os;
}

inline void sc_trace(sc_trace_file* tf, const {{d.name}}& ev, const std::string& name)
{
    sc_trace(tf, ev, ".{{d.name}}");
}

inline void to_json(json& j, const {{d.name}}& ev)
{
    std::stringstream ss;
    ss << ev;
    j = ss.str();
}

{%- endif -%}"""
    )

    cpp = env.from_string(
        """{% if d.values | length > 0 %}
enum class {{d.name}}
{
{% for v in d.values %}{{v.render("RT_CPP")}}
{% endfor -%}
};

inline ostream& operator<<(ostream& os, const {{d.name}}& ev)
{
    switch (ev)
    {
    {%- for v in d.values %}
    case {{d.name}}::{{v.name}}:
        os << "{{v.name}}";
        break;
    {%- endfor %}
    default:
        os << "UnknownEnumError";
    }
    return os;
}

{%- endif -%}"""
    )

    def __init__(self, name, type, width, desc, values, config):
        self.name = hydrate(name, config)
        self.type = hydrate(type, config)
        self.width = hydrate(width, config)
        self.desc = hydrate(desc, config)
        self.values = [
            EnumValue(v.get("name", ""), v.get("desc", ""), config)
            for v in values
        ]

    def render(self, type="RT_VERILOG"):
        self.render_type = type
        force_block = True if len(self.values) == 0 else False
        ret = Comment(self.desc, force_block).render(type)
        if type == "RT_VERILOG":
            return ret + self.verilog.render(d=self)
        elif type == "RT_SYSTEMC":
            return ret + self.systemc.render(d=self)
        elif type == "RT_CPP":
            return ret + self.cpp.render(d=self)
        fatal("Fatal error: Invalid render type encountered!")
        return None


################################################################################


class StructField:
    verilog = env.from_string(
        """{{d.type | verilog_type(d.get_width_str())}} {{d.name}}{% if d.count_v > 1 %}[0:{{d.count_v | int - 1}}]
{%- elif d.count_v == -1 -%}[0:{{d.count}}-1]
{%- endif -%}
; {% if d.desc | count > 0 -%}// {{d.desc}} {%- endif -%}
"""
    )

    systemc = env.from_string(
        """{{d.type | systemc_type(d.get_width_str_or_tmpl(), d.type_params)}} {{d.name}}{{d.get_count_str_or_tmpl() | arrayize}};
{%- if d.desc | count > 0 %} // {{d.desc}}{%- endif -%}
"""
    )

    cpp = env.from_string(
        """{{d.type | cpp_type(d.get_width_str_or_tmpl(), d.type_params)}} {{d.name}}{{d.get_count_str_or_tmpl() | arrayize}};
{%- if d.desc | count > 0 %} // {{d.desc}}{%- endif -%}
"""
    )

    def __init__(self, name, type, width, count, desc, config):
        self.templates = []
        self.type_params = []
        self.name = hydrate(name, config)
        self.type = hydrate(type, config)
        self.desc = hydrate(desc, config)

        self.width_raw = width
        self.count_raw = count
        self.width = hydrate(width, config)
        self.count = hydrate(count, config)
        try:
            ll = eval(self.count)
            if isinstance(ll, list):
                if len(ll) > 1:
                    panic("unsupported multi-dimensional list encountered")
                self.count = int(ll[0])
        except:
            self.count = 1

        self.width_v = -1
        try:
            self.width_v = int(self.width)
        except:
            pass
        self.count_v = -1
        try:
            self.count_v = int(self.count)
        except:
            pass

        self.width_t = self.extract_template(self.width_raw, self.width_v)
        self.count_t = self.extract_template(self.count_raw, self.count_v)
        for t in [self.width_t, self.count_t]:
            if t != None:
                self.templates.append(t)

    def extract_template(self, raw, v):
        if isinstance(raw, str):
            if raw.startswith("$"):
                tn = raw.lstrip("$")
                tv = v
                return (tn, tv)
        return None

    def render(self, type="RT_VERILOG"):
        self.render_type = type
        if type == "RT_VERILOG":
            return self.verilog.render(d=self)
        elif type == "RT_SYSTEMC":
            return self.systemc.render(d=self)
        elif type == "RT_CPP":
            return self.cpp.render(d=self)
        fatal("Fatal error: Invalid render type encountered!")
        return None

    def discover_type_params(self, structs):
        for s in structs:
            if s.name == self.type:
                self.type_params = s.get_templates()

    def get_templates(self):
        """ looks through all the template parameters that were not hydrated
            from the config and returns them as a list. This can/(should?) only
            be either the width or the count.
        """
        return self.templates

    def get_width_str(self):
        if self.width_v == -1:
            return self.width
        return str(self.width_v)

    def get_width_str_or_tmpl(self):
        if self.width_t != None:
            return self.width_t[0]
        return self.width

    def get_count_str_or_tmpl(self):
        if self.count_t != None:
            return self.count_t[0]
        return self.count

    def is_width_array(self):
        return int(self.get_width_str()) > 1

    def is_count_array(self):
        return int(self.get_count_str_or_tmpl()) > 1

    def print(self):
        print(self.name, self.type, self.width, self.count)


################################################################################


class Struct:
    verilog = env.from_string(
        """{% if d.fields | length > 0 %}
typedef struct packed {
{% for f in d.fields %}    {{f.render("RT_VERILOG")}}
{% endfor -%}
} {{d.name}};
{%- endif -%}"""
    )

    systemc = env.from_string(
        """{% if d.fields | length > 0 %}
{{ d.template_params | c_template_header -}}
struct {{d.name}} : JSONable
{
    typedef {{d.name}}{{d.template_params | c_template_list}} {{d.name}}_T;

{% for f in d.fields %}    {{f.render("RT_SYSTEMC")}}
{% endfor %}
    inline bool operator==(const {{d.name}}_T& rhs) const
    {
        {%- for f in d.fields %} {%- if f.is_count_array() %}
        for (uint i = 0; i < {{f.get_count_str_or_tmpl()}}; ++i)
            if ({{f.name}}[i] != rhs.{{f.name}}[i]) return false;
        {%- else %}
        if ({{f.name}} != rhs.{{f.name}}) return false;
        {%- endif %}
        {%- endfor %}
        return true;
    }

    inline bool operator!=(const {{d.name}}_T& rhs) const
    {
        return !(*this == rhs);
    }

    virtual void MarshalJSON(json& j) const
    {
        {%- for f in d.fields %} {% if f.is_count_array() %}
        json {{f.name}}_arr = json::array();
        for (uint i = 0; i < {{f.get_count_str_or_tmpl()}}; ++i)
            {{f.name}}_arr.push_back({{f.name}}[i]);
        {%- endif %}

        {%- endfor %}
        j = json{ {% for f in d.fields %} {% if f.is_count_array() %}
            {"{{f.name}}", {{f.name}}_arr},
        {%- else %}
            {"{{f.name}}", {{f.name}}},
        {%- endif %}
        {%- endfor %}
        };
    }
};

{{ d.template_params | c_template_header -}}
inline ostream& operator<<(ostream& os, const {{d.name}}{{ d.template_params | c_template_list }}& state)
{
    {%- for f in d.fields %} {%- if f.is_count_array() %}
    for (uint i = 0; i < {{f.get_count_str_or_tmpl()}}; ++i)
        os << " {{f.name}}[" << i << "]=" << state.{{f.name}}[i];
    {%- else %}
    os << " {{f.name}}=" << state.{{f.name}};
    {%- endif %}
    {%- endfor %}
    return os;
}

{{ d.template_params | c_template_header -}}
inline void sc_trace(sc_trace_file* tf, const {{d.name}}{{ d.template_params | c_template_list }}& state, const std::string& name)
{
    char buf[64];
    {%- for f in d.fields %} {%- if f.is_count_array() %}
    for (uint i = 0; i < {{f.get_count_str_or_tmpl()}}; ++i)
    {
        sprintf(buf, "{{f.name}}.[%d]", i);
        sc_trace(tf, state.{{f.name}}[i], name + buf);
    }
    {%- else %}
    sc_trace(tf, state.{{f.name}}, ".{{f.name}}");
    {%- endif %}
    {%- endfor %}
}

{%- endif -%}"""
    )

    cpp = env.from_string(
        """{% if d.fields | length > 0 %}
{{ d.template_params | c_template_header -}}
struct {{d.name}}
{
    typedef {{d.name}}{{d.template_params | c_template_list}} {{d.name}}_T;

{% for f in d.fields %}    {{f.render("RT_CPP")}}
{% endfor %}
    inline bool operator==(const {{d.name}}_T& rhs) const
    {
        {%- for f in d.fields %} {%- if f.is_count_array() %}
        for (uint i = 0; i < {{f.get_count_str_or_tmpl()}}; ++i)
            if ({{f.name}}[i] != rhs.{{f.name}}[i]) return false;
        {%- else %}
        if ({{f.name}} != rhs.{{f.name}}) return false;
        {%- endif %}
        {%- endfor %}
        return true;
    }

    inline bool operator!=(const {{d.name}}_T& rhs) const
    {
        return !(*this == rhs);
    }

    {{d.name}}_T& operator=(const {{d.name}}_T& rhs)
    {
        {%- for f in d.fields %} {%- if f.is_count_array() %}
        for (uint i = 0; i < {{f.get_count_str_or_tmpl()}}; ++i)
            {{f.name}}[i] = rhs.{{f.name}}[i];
        {%- else %}
        {{f.name}} = rhs.{{f.name}};
        {%- endif %}
        {%- endfor %}
        return *this;
    }
};

{{ d.template_params | c_template_header -}}
inline ostream& operator<<(ostream& os, const {{d.name}}{{ d.template_params | c_template_list }}& state)
{
    {%- for f in d.fields %} {%- if f.is_count_array() %}
    for (uint i = 0; i < {{f.get_count_str_or_tmpl()}}; ++i)
        os << " {{f.name}}[" << i << "]=" << state.{{f.name}}[i];
    {%- else %}
    os << " {{f.name}}=" << state.{{f.name}};
    {%- endif %}
    {%- endfor %}
    return os;
}

{%- endif -%}"""
    )

    def __init__(self, name, desc, fields, config):
        self.name = hydrate(name, config)
        self.desc = hydrate(desc, config)
        self.fields = [
            StructField(
                f.get("id", ""),
                f.get("type") or f.get("encode") or "logic",
                f.get("width", "1"),
                f.get("num_repeat_cnts", "1"),
                f.get("desc") or "",
                config,
            )
            for f in self.expand_fields(fields, config)
        ]
        # TODO: BUG: OSDT parser grabs fields in reverse order?
        if len(self.fields) > 1:
            self.fields.reverse()
        self.template_params = []
        self.has_template = False
        for f in self.fields:
            for t in f.get_templates():
                self.add_template(t)

    def expand_fields(self, fields, config):
        """ iterates through the fields array from the yaml dictionary and
            expands any `name_template` keys into the number of `name`'d values
            in the `fields` list.
        """
        ret = []
        for f in fields:
            if f.get("name_template", False):
                nt = f.get("name_template", "ERROR")
                dt = f.get("desc_template", False)
                try:
                    start = int(eval(hydrate(f.get("start", "0"), config)))
                    end = int(eval(hydrate(f.get("end", "0"), config)))
                    incr = int(eval(hydrate(f.get("increment", "1"), config)))
                except Exception as e:
                    print("Warning: exception parsing %s :: " % nt, e)
                    continue
                for n in range(start, end, incr):
                    ff = {"name": env.from_string(nt).render(n=n)}
                    if dt:
                        ff["desc"] = env.from_string(dt).render(n=n)
                    for k in ["type", "width", "num_repeat_cnts"]:
                        if f.get(k, False):
                            ff[k] = f.get(k)

                    ret.append(ff)
            else:
                ret.append(f)
        return ret

    def get_templates(self):
        return self.template_params

    def add_template(self, t):
        self.has_template = True
        if t not in self.template_params:
            self.template_params.append(t)
            return True
        return False

    def discover_child_templates(self, structs):
        count = 0
        for f in self.fields:
            f.discover_type_params(structs)
            for s in structs:
                if f.type == s.name:
                    for t in s.get_templates():
                        if self.add_template(t):
                            count += 1
        return count

    def render(self, type="RT_VERILOG"):
        force_block = True if len(self.fields) == 0 else False
        ret = Comment(self.desc, force_block).render(type)
        if type == "RT_VERILOG":
            return ret + self.verilog.render(d=self)
        elif type == "RT_SYSTEMC":
            return ret + self.systemc.render(d=self)
        elif type == "RT_CPP":
            return ret + self.cpp.render(d=self)
        fatal("Fatal error: Invalid render type encountered!")
        return None


################################################################################
################################################################################
################################################################################


special_commands_array = {"zero_size_print": "keepZeroSizeArray"}

################################################################################


class SvWriter(object):
    def __init__(self, filenames, printer):
        self.filenames = filenames
        self.printer = printer
        self.output_dir = "."

    def print_header(self, filename, delim="//", package_def=False) -> str:
        HEADER_WIDTH = 50
        MAINTAINER_NAME = "Maintainer: Jigar Savla (jigar@recogni.com)"
        DEVELOPER_NAME = (
            "Developers: Shaba Abhiram (@shaba), "
            "Berend Ozceri (@berend), "
            "Jigar Savla (@jigar)"
        )
        WARNING_NOTE = (
            "This is an OSDT auto-generated file. Please DO-NOT modify. "
            "Refer to: scorpio/docs/osdt/README.md for more details"
        )

        header_str = ""

        # print package
        if package_def:
            header_str += "`ifndef __" + filename.upper() + "_VH__" + "\n"
            header_str += "`define __" + filename.upper() + "_VH__" + "\n"
            for incl in self.printer.includes:
                header_str += '`include "' + incl + '"' + "\n"

            if package_def:
                header_str += "\n" + "package " + filename + ";" + "\n\n"

            for incl in self.printer.includes:
                header_str += (
                    "    import "
                    + os.path.splitext(os.path.basename(incl))[0]
                    + "::*;"
                    + "\n"
                )

        # beginning of the header
        header_str += str((delim * HEADER_WIDTH + "\n"))
        header_str += str((delim + "\n") * 2)

        # body of the header
        header_str += str((delim + "  " + WARNING_NOTE + "\n"))
        header_str += str((delim + "\n") * 1)
        header_str += str((delim + "  " + MAINTAINER_NAME + "\n"))
        header_str += str((delim + "\n") * 1)
        header_str += str((delim + "  " + DEVELOPER_NAME + "\n"))

        # ending of the header
        header_str += str((delim + "\n") * 2)
        header_str += str((delim * HEADER_WIDTH + "\n"))
        header_str += "\n\n"
        return header_str

    def print_width_str(self, width: int, keepZeroSize=False) -> str:
        width_str = ""
        if width > 1 or keepZeroSize:
            width_str = "[%d:0]" % (width - 1)
        return width_str

    def print_enums(self) -> str:
        indent = 4
        enum_str = ""
        for enum in self.printer.enums:
            if enum["at_top_level"]:
                delimiter = ","
                width_str = self.print_width_str(
                    int(enum["width"]), keepZeroSize=False
                )
                enum_str += str(("typedef enum logic %s { " % width_str) + "\n")
                for idx, vals in enumerate(enum["values"]):
                    if idx == (len(enum["values"]) - 1):
                        delimiter = ""  # none
                    enum_str += (
                        str(
                            " " * indent
                            + vals["name"]
                            + " = "
                            + vals["value"]
                            + delimiter
                            + str(
                                (" // %s " % vals["desc"])
                                if vals["desc"]
                                else ""
                            )
                        )
                        + "\n"
                    )
                enum_str += str("} %s;\n\n" % enum["name"]) + "\n"
        return enum_str

    def nested_field_str(
        self, repeat_cnts_list: list, keepZeroSize=False
    ) -> str:
        ret_str = " "
        for cnt in repeat_cnts_list:
            ret_str += " %s " % self.print_width_str(
                int(cnt), keepZeroSize=keepZeroSize
            )
        return ret_str

    def check_zero_print(self, desc: str) -> bool:
        return (
            False
            if desc is None
            else special_commands_array["zero_size_print"] in desc
        )

    def print_structs(self) -> str:
        indent = 4
        struct_str = ""
        for struct in self.printer.structs:
            if struct["at_top_level"]:
                delimiter = ";"
                struct_str += (
                    str(
                        "// Total size for "
                        + struct["name"]
                        + " is "
                        + str(struct["width"])
                    )
                    + "\n"
                )
                struct_str += str(("typedef "))
                struct_str += "struct" if struct["is_not_union"] else "union"
                struct_str += str((" packed {")) + "\n"

                for idx, field in enumerate(struct["fields"].__reversed__()):
                    if idx == (len(struct["fields"]) - 1):
                        # we're in the last entry, change the delimiter
                        delimiter = (
                            ";"
                        )  # structures still keep ';' as the last entry delimiter

                    if field["encode"]:
                        # print("I see an enum usage")
                        # we're managing an enum here:
                        nested_field_string = self.nested_field_str(
                            field["num_repeat_cnts"],
                            keepZeroSize=self.check_zero_print(field["desc"]),
                        )
                        struct_str += (
                            str(
                                " " * indent
                                + field["encode"]
                                + nested_field_string
                                + field["id"]
                                + delimiter
                                + "  // "
                                + " width: "
                                + str(field["width"])
                                + str(
                                    (" || %s " % field["desc"])
                                    if field["desc"]
                                    else ""
                                )
                            )
                            + "\n"
                        )

                    elif field["type"]:
                        # we have a nested structure
                        nested_field_string = self.nested_field_str(
                            field["num_repeat_cnts"]
                        )

                        struct_str += (
                            str(
                                " " * indent
                                + field["type"]
                                + nested_field_string
                                + field["id"]
                                + delimiter
                                + "  // "
                                + " width: "
                                + str(field["width"])
                                + str(
                                    (" || %s " % field["desc"])
                                    if field["desc"]
                                    else ""
                                )
                            )
                            + "\n"
                        )
                    else:
                        struct_str += (
                            str(
                                " " * indent
                                + "logic %s "
                                % (
                                    self.print_width_str(
                                        int(field["width"]),
                                        keepZeroSize=self.check_zero_print(
                                            field["desc"]
                                        ),
                                    )
                                )
                                + field["id"]
                                + delimiter
                                + str(
                                    (" // %s" % field["desc"])
                                    if field["desc"]
                                    else ""
                                )
                            )
                            + "\n"
                        )

                struct_str += str(("} %s;\n\n" % struct["name"])) + "\n"

        return struct_str

    def print_tail(self, filename, package_def=True) -> str:
        tail_str = "\n"
        if package_def:
            tail_str += "endpackage\n"
        tail_str += "`endif " + "// " + "__" + filename.upper() + "__" + "\n"
        tail_str += "\n"
        return tail_str

    def print_width_vars(self, desc_list) -> str:
        width_str = ""
        for desc in desc_list:
            if desc["at_top_level"]:
                width_str += (
                    "$"
                    + desc["name"].upper()
                    + "_width = ".upper()
                    + str(desc["width"])
                    + ";\n"
                )
        return width_str

    def get_output_filename(self, suffix):
        base = os.path.split(self.filenames[0])[1].split(".")[0]
        return base + suffix

    def write(self, args):
        ofn = self.get_output_filename(args.output_suffix)
        self.output_dir = ensure_output_dir(args.output_dir)

        # Build the output file by sections (header, enums, struct and tail).
        struct_enum_op_str = self.print_header(
            filename=ofn, package_def=args.package_def
        )
        struct_enum_op_str += self.print_enums()
        struct_enum_op_str += self.print_structs()
        struct_enum_op_str += self.print_tail(
            filename=ofn, package_def=args.package_def
        )

        # Sanity checks for input args.
        if not os.path.isdir(args.output_dir):
            panic(
                "The --output-dir path provided %s doesn't exist, please create it prior to using"
                % args.output_dir
            )

        # write to file:
        vh_filepath = os.path.join(self.output_dir, ofn + ".vh")
        if not args.clobber_files and os.path.isfile(vh_filepath):
            panic(
                "FILE: %s already exists. Currently set to no over-ride of files. Please delete the file prior to running OSDT. "
                % vh_filepath
            )

        with open(vh_filepath, "w") as fout:
            fout.write(struct_enum_op_str)

        # ======================================= #

        # Each VH file is accompanied by a PERL file to help document things
        # like struct widths etc.

        width_var_op_str = self.print_header(filename=ofn, delim="#")
        width_var_op_str += self.print_width_vars(self.printer.enums)
        width_var_op_str += self.print_width_vars(self.printer.structs)
        width_var_op_str += "\n"

        pl_filepath = os.path.join(self.output_dir, ofn + ".pl")
        if not args.clobber_files and os.path.isfile(pl_filepath):
            panic(
                "FILE: %s already exists. Currently set to no over-ride of files. Please delete the file prior to running OSDT. "
                % pl_filepath
            )

        with open(pl_filepath, "w") as fout:
            fout.write(width_var_op_str)


################################################################################


class SystemCWriter(object):
    def __init__(self, filenames, printer):
        self.filenames = filenames
        self.printer = printer
        self.output_dir = "."

    def write(self, args):
        self.output_dir = ensure_output_dir(args.output_dir, "sc")
        lines = """/*
 *  Auto-generated file. Do not edit!
 */

using namespace std;
#include <bitset>""".split(
            "\n"
        )
        for e in [
            e for e in self.printer.enums if True or e.get("at_top_level", True)
        ]:
            n = e.get("name", "UNDEFINED")
            t = e.get("type") or "logic"
            w = e.get("width", "1")
            v = e.get("values", [])
            d = e.get("desc") or ""
            en = Enum(n, t, w, d, v, {})
            lines.extend([en.render("RT_SYSTEMC")])
        for s in [
            s
            for s in self.printer.structs
            if True or s.get("at_top_level", True)
        ]:
            n = s.get("name", "UNDEFINED")
            d = s.get("desc") or ""
            fs = s.get("fields", [])
            st = Struct(n, d, fs, {})
            lines.extend([st.render("RT_SYSTEMC")])
        fn = "sc_" + os.path.split(self.filenames[0])[1].split(".")[0] + ".h"
        fp = os.path.join(self.output_dir, fn)
        with open(fp, "w") as fout:
            fout.write("\n".join(lines))
        return True


################################################################################


class CPPWriter(object):
    def __init__(self, filenames, printer):
        self.filenames = filenames
        self.printer = printer
        self.output_dir = "."

    def write(self, args):
        self.output_dir = ensure_output_dir(args.output_dir, "cpp")
        lines = """/*
 *  Auto-generated file. Do not edit!
 */

using namespace std;
#include <bitset>""".split(
            "\n"
        )
        for e in [e for e in self.printer.enums if e.get("at_top_level", True)]:
            n = e.get("name", "UNDEFINED")
            t = e.get("type") or "logic"
            w = e.get("width") or None
            v = e.get("values", [])
            d = e.get("desc") or ""
            en = Enum(n, t, w, d, v, {})
            lines.extend([en.render("RT_CPP")])
        for s in [
            s for s in self.printer.structs if s.get("at_top_level", True)
        ]:
            n = s.get("name", "UNDEFINED")
            d = s.get("desc") or ""
            fs = s.get("fields", [])
            st = Struct(n, d, fs, {})
            lines.extend([st.render("RT_CPP")])
        fn = os.path.split(self.filenames[0])[1].split(".")[0] + ".h"
        fp = os.path.join(self.output_dir, fn)
        with open(fp, "w") as fout:
            fout.write("\n".join(lines))
        return True


################################################################################


class JSONWriter(object):
    def __init__(self, filenames, printer):
        self.filenames = filenames
        self.printer = printer
        self.output_dir = "."

    def write(self, args):
        self.output_dir = ensure_output_dir(args.output_dir, "json")
        # TODO: TextIOWrapper is not JSON serializable
        fn = os.path.split(self.filenames[0])[1].split(".")[0]
        # with open("%s_structs.json" % (fn), "w") as fout:
        #     json.dump(fout, self.printer.structs)
        # with open("%s_enums.json" % (fn), "w") as fout:
        #     json.dump(fout, self.printer.enums)
        return False


################################################################################


class RecogniWriter(object):
    def __init__(self, filenames, printer):
        self.filenames = filenames
        self.printer = printer

    def write(self, args):
        for ot in args.output_types:
            if ot == "sv":
                SvWriter(self.filenames, self.printer).write(args)
            elif ot == "sc":
                SystemCWriter(self.filenames, self.printer).write(args)
            elif ot == "cpp":
                CPPWriter(self.filenames, self.printer).write(args)
            elif ot == "json":
                JSONWriter(self.filenames, self.printer).write(args)
            else:
                print("Unknown output type %s encountered\n", ot)
        return True
