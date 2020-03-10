import os

special_commands_array = {"zero_size_print": "keepZeroSizeArray"}


def check_zero_print(desc: str) -> bool:
    """
    Checks for Zero print statements in comments / description field
    """
    if desc is None:
        return False
    else:
        return special_commands_array["zero_size_print"] in desc


def print_width_str(width: int, language="sv", keepZeroSize=False) -> str:
    """
    Handles width printing. Takes care of width == 1 case

    Args:
        width:
        language:
        keepZeroSize: bool value to identify if we need to print the [0:0] values as well

    Returns:

    """
    width_str = ""
    if language == "sv":

        # if keepZeroSize:
        #     print('keepZeroSize set')

        if width > 1 or keepZeroSize:
            width_str = "[%d:0]" % (width - 1)

    else:
        panic(
            "I'm currently only supporting SystemVerilog language, feel free to add your own here"
        )

    return width_str


def print_enums(enum_list, language="sv") -> str:
    """
    Pretty prints the enums in SV for now
    :param enum_list:
    :return enum_str:
    """

    indent = 4
    # print(dict)
    enum_str = ""

    if language == "sv":
        for enum in enum_list:
            if enum["at_top_level"]:
                # skip printing if not at top level, it's just an include file

                delimiter = ","
                # print("enum is "+ enum)

                width_str = print_width_str(
                    int(enum["width"]), language="sv", keepZeroSize=False
                )

                enum_str += str(("typedef enum logic %s { " % width_str) + "\n")

                for idx, vals in enumerate(enum["values"]):

                    if idx == (len(enum["values"]) - 1):
                        # we're in the last entry, change the delimiter
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
    else:
        panic(
            "I'm currently only supporting SystemVerilog language, feel free to add your own here"
        )

    return enum_str


def nested_field_str(
    repeat_cnts_list: list, language="sv", keepZeroSize=False
) -> str:
    ret_str = " "

    if language == "sv":

        for cnt in repeat_cnts_list:
            ret_str += " %s " % print_width_str(
                int(cnt), language="sv", keepZeroSize=keepZeroSize
            )
    else:

        panic(
            "I'm currently only supporting SystemVerilog language, feel free to add your own here"
        )

    return ret_str


def print_structs(struct_list, language="sv") -> str:
    """
    Pretty prints the structs in SV for now
    :param struct_list:
    :return:
    """
    indent = 4
    struct_str = ""

    if language == "sv":
        for struct in struct_list:
            if struct["at_top_level"]:
                # skip printing if not at top level, it's just an include file

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
                        nested_field_string = nested_field_str(
                            field["num_repeat_cnts"],
                            keepZeroSize=check_zero_print(field["desc"]),
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
                        nested_field_string = nested_field_str(
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
                                    print_width_str(
                                        int(field["width"]),
                                        language="sv",
                                        keepZeroSize=check_zero_print(
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

    else:
        panic(
            "I'm currently only supporting SystemVerilog language, feel free to add your own here"
        )

    return struct_str


def print_header(
    filename="osdt_test_file", includes=[], package_def=True, language="sv"
) -> str:
    """
    We'll print the header of the output file based on the language
    :param filename:
    :param language:
    :return:
    """
    # parameters
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
    # "OSDT == Open Structure Definition Tool"

    header_str = ""

    comment_style_dict = {"sv": "//", "pl": "#", "py": "#"}

    if language == "sv":
        # print package
        header_str += "`ifndef __" + filename.upper() + "_VH__" + "\n"
        header_str += "`define __" + filename.upper() + "_VH__" + "\n"
        for incl in includes:
            header_str += '`include "' + incl + '"' + "\n"

        if package_def:
            header_str += "\n" + "package " + filename + ";" + "\n\n"

        for incl in includes:
            header_str += (
                "    import "
                + os.path.splitext(os.path.basename(incl))[0]
                + "::*;"
                + "\n"
            )

    # beginning of the header
    header_str += str((comment_style_dict[language] * HEADER_WIDTH + "\n"))
    header_str += str((comment_style_dict[language] + "\n") * 2)

    # body of the header
    header_str += str(
        (comment_style_dict[language] + "  " + WARNING_NOTE + "\n")
    )
    header_str += str((comment_style_dict[language] + "\n") * 1)
    header_str += str(
        (comment_style_dict[language] + "  " + MAINTAINER_NAME + "\n")
    )
    header_str += str((comment_style_dict[language] + "\n") * 1)
    header_str += str(
        (comment_style_dict[language] + "  " + DEVELOPER_NAME + "\n")
    )

    # ending of the header
    header_str += str((comment_style_dict[language] + "\n") * 2)
    header_str += str((comment_style_dict[language] * HEADER_WIDTH + "\n"))
    header_str += "\n\n"

    return header_str


def print_tail(
    filename="osdt_test_file", package_def=True, language="sv"
) -> str:
    """
    Print tail message

    Args:
        filename:
        language:

    Returns:

    """
    tail_str = "\n"
    if language == "sv":
        if package_def:
            tail_str += "endpackage\n"
        tail_str += "`endif " + "// " + "__" + filename.upper() + "__" + "\n"
        # add one more newline to make some parsing tools happy
        tail_str += "\n"

    return tail_str


def print_width_vars(struct_list, language="pl") -> str:
    """
    When creating a seperate file for just widths of structures / enums.
    Useful for memory size generation in RTL

    Args:
        struct_list:
        language:

    Returns:

    """
    width_str = ""

    if language == "pl":
        for struct in struct_list:
            if struct["at_top_level"]:
                width_str += (
                    "$"
                    + struct["name"].upper()
                    + "_width = ".upper()
                    + str(struct["width"])
                    + ";"
                    + "\n"
                )
    else:
        panic(
            "We currently only support Perl o/p for width vars. You're free to contribute support for other languages"
        )

    return width_str


################################################################################


class SvWriter(object):
    def __init__(self, filenames, printer):
        self.filenames = filenames
        self.printer = printer

    def write(self, args):
        ip_filename_no_ext = os.path.split(self.filenames[0])[1].split(".")[0]
        op_filename_no_ext = ip_filename_no_ext + args.output_suffix

        # Build the output file by sections (header, enums, struct and tail).
        struct_enum_op_str = ""
        struct_enum_op_str += print_header(
            filename=op_filename_no_ext,
            includes=self.printer.includes,
            package_def=args.package_def,
            language="sv",
        )
        struct_enum_op_str += print_enums(self.printer.enums, language="sv")
        struct_enum_op_str += print_structs(self.printer.structs, language="sv")
        struct_enum_op_str += print_tail(
            filename=op_filename_no_ext,
            package_def=args.package_def,
            language="sv",
        )

        # Sanity checks for input args.
        if not os.path.isdir(args.output_dir):
            panic(
                "The --output-dir path provided %s doesn't exist, please create it prior to using"
                % args.output_dir
            )

        # write to file:
        base_vh_filepath = (
            args.output_dir
        )  # can be made args.output_vh_dir later
        vh_filepath = os.path.join(base_vh_filepath, op_filename_no_ext + ".vh")

        # Sanity checking for file clobbering.
        if not args.clobber_files and os.path.isfile(vh_filepath):
            panic(
                "FILE: %s already exists. Currently set to no over-ride of files. Please delete the file prior to running OSDT. "
                % vh_filepath
            )

        with open(vh_filepath, "w") as fout:
            fout.write(struct_enum_op_str)

        # ======================================= #
        #### perl language width prints ####
        width_var_op_str = ""
        width_var_op_str += print_header(
            filename=op_filename_no_ext,
            includes=self.printer.includes,
            language="pl",
        )
        width_var_op_str += print_width_vars(self.printer.enums, language="pl")
        width_var_op_str += print_width_vars(
            self.printer.structs, language="pl"
        )
        width_var_op_str += print_tail(
            filename=op_filename_no_ext, language="pl"
        )
        #  print(width_var_op_str)

        base_pl_filepath = (
            args.output_dir
        )  # can be made args.output_pl_dir later
        pl_filepath = os.path.join(base_pl_filepath, op_filename_no_ext + ".pl")

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

    def write(self, args):
        print("TOOD: Implement SystemC Writer\n")
        return False


################################################################################


class JSONWriter(object):
    def __init__(self, filenames, printer):
        self.filenames = filenames
        self.printer = printer

    def write(self, args):
        print("TOOD: Implement JSON Writer\n")
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
            elif ot == "json":
                JSONWriter(self.filenames, self.printer).write(args)
            else:
                print("Unknown output type %s encountered\n", ot)
        return True
