# importing tkinter and tkinter.ttk
# and all their functions and classes
import os
import random
import re
import subprocess
import time
import logging
from subprocess import Popen, PIPE
from pathlib import Path
from tkinter import *
# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
from abc import ABC, abstractmethod
from typing import List, Set
# from tqdm import tqdm
def __init__(
        self,
        apk_path: str,
        working_dir_path: str = None,
        obfuscated_apk_path: str = None,
        ignore_libs: bool = False,
        interactive: bool = False,
        virus_total_api_key: str = None,
        keystore_file: str = None,
        keystore_password: str = None,
        key_alias: str = None,
        key_password: str = None,
        ignore_packages_file: str = None,
        use_aapt2: bool = False,
    ):
    self.interactive: bool = interactive
    self.used_obfuscators: List[str] = []


# ----------- Global Var -----------
content = ""
file_name = ""
file_path = ""
main_smali_file_path = ""
logger = logging.getLogger(__name__)

window = Tk()
window.title("Simple Obfuscator")
window.geometry('480x300')
window.config(background="light blue")

#class ICodeObfuscator(IBaseObfuscator):
#    @abstractmethod
#    def obfuscate(self, obfuscation_info: Obfuscation):
 #       raise NotImplementedError()

invoke_pattern = re.compile(
    r"\s+(?P<invoke_type>invoke-\S+)\s"
    r"{(?P<invoke_pass>[vp0-9,.\s]*)},\s"
    r"(?P<invoke_object>\S+?)"
    r"->(?P<invoke_method>\S+?)"
    r"\((?P<invoke_param>\S*?)\)"
    r"(?P<invoke_return>\S+)",
    re.UNICODE,
)

# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    global content
    global file_name
    global file_path

    file = askopenfile(mode='r')
    progress["value"] += 20
    window.update_idletasks()
    file_name = os.path.basename(file.name)
    file_path = file.name


    loaded = Label(window, text=f"{file_name} is loaded")
    loaded.config(anchor="s")
    loaded.pack()

    if file is not None:
        if file_name.__contains__(".apk"):
            print(file)
            progress["value"] += 20
            window.update_idletasks()
            apk_decompile(file.name)

    else:
        content = file.read()

    with open(f'data_files/{file_name}', 'w') as f:
        f.write(content)
        f.close()


# def multiProc():


# decompile apk
def apk_decompile(apk_file):
    progress["value"] += 20
    apk_name = os.path.basename(apk_file)
    os.system(f"java -jar tools/apktool.jar d -f -r {apk_file} -o original_apk/{apk_name}")
    os.system(f"java -jar tools/apktool.jar d -f -r {apk_file} -o output/{apk_name}")

    loaded = Label(window, text=f"{file_name} successfully decompiled at output/{apk_name}")
    loaded.config(anchor=CENTER)
    loaded.pack()
    progress["value"] += 40
    window.update_idletasks()


# recompile and sign apk
def apk_recompile_sign(apk_file):
    apk_name = os.path.basename(apk_file)
    subprocess.call(f"java -jar tools/apktool.jar b -f -r --use-aapt2 output/{apk_file} -o data_files/obfuscated_apk/{apk_name}")
    time.sleep(3)
    subprocess.call(f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -storepass password -keystore tools/test.keystore data_files/obfuscated_apk/{apk_name} test")
    subprocess.call(f"jarsigner -verify -verbose -certs data_files/obfuscated_apk/{apk_name}")
    subprocess.call(f"tools/zipalign -v 4 data_files/obfuscated_apk/{apk_name} data_files/obfuscated_apk/aligned-{apk_name}")



# -------------------- Obfuscation Part --------------------
def obfuscate_smali_file():
    global main_smali_file_path
    folder = os.listdir(f"output/{file_name}")
    print('folder', folder)
    count = 0

    substring = "smali"
    substring2 = "example"
    for i in folder:
        if re.search(substring, i):
            f = f"output/{file_name}/{i}/com"
            sub_folder = os.listdir(f)
            print(sub_folder)
            for x in sub_folder:
                print(x)
                if re.search(substring2, x):
                    fx = f"output/{file_name}/{i}/com/{x}"
                    print(fx)
                    sub_fx = os.listdir(fx)
                    for z in sub_fx:
                        main_smali_file_path = f"output/{file_name}/{i}/com/{x}/{z}"
                        for e in Path().cwd().glob(f"{main_smali_file_path}/*.smali"):
                            count += 1
                            #print(e)
                            nocomment(e)
                            #addjunkcode(e)
    loaded = Label(window, text=f"{count} Smali file obfuscated!")
    loaded.config(anchor=CENTER)
    loaded.pack()

def nocomment(inFile):
    print(inFile)
    open_file = open(inFile, "r")
    basename = os.path.basename(inFile)
    change = ""
    regex = r'"(.*#.*)"'

    for line in open_file:
        result = re.findall(regex, line)
        if not result:
            line = line.split("#", 1)
            print(line[0])
            change = change + str(line[0])
            print(change)
        else:
            change = change + line

    open_file.close()
    outFile = open(inFile, "w")
    #outFile = open(f"data_files/{basename}", "w")
    outFile.write(change)
    outFile.close()

def addjunkcode(smaliCode):
    flag1 = 0
    flag2 = 0
    functionNameFirst = ["important_", "necessary_", "mustHave_", "coolCool_"]
    functionNameSecond = ["function()", "statement()", "detail()", "coolStuff()"]
    counter = 0
    saltNOP = "nop\n\n"
    saltFUNCTIONback = ".end method\n"
    saltFUNCTIONlocal = ".locals 0\n"
    iterator = 0

    # [ Function Salting ]
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if lines[iterator] == ".end method\n":
                saltFUNCTIONfront = "\n.method public " + functionNameFirst[flag1] + functionNameSecond[flag2] + "Z\n"
                if flag1 != 3 and flag2 != 3:
                    lines.insert(iterator + 1, saltFUNCTIONfront)
                    lines.insert(iterator + 2, saltFUNCTIONlocal)
                    lines.insert(iterator + 3, saltFUNCTIONback)
                    iterator += 4
                    flag2 += 1
                elif flag1 != 3 and flag2 == 3:
                    flag1 += 1
                    flag2 = 0
                    lines.insert(iterator + 1, saltFUNCTIONfront)
                    lines.insert(iterator + 2, saltFUNCTIONlocal)
                    lines.insert(iterator + 3, saltFUNCTIONback)
                elif flag1 == 3 and flag2 < 3:
                    lines.insert(iterator + 1, saltFUNCTIONfront)
                    lines.insert(iterator + 2, saltFUNCTIONlocal)
                    lines.insert(iterator + 3, saltFUNCTIONback)
                    flag2 += 1
                elif flag1 == 3 and flag2 == 3:
                    break
            iterator += 1
    f = open(smaliCode, "w")
    f.writelines(lines)
    f.close()

    # reset iterator [ Salt with NOP ]
    iterator = 0
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if ".method" in lines[iterator]:
                randint = random.randint(3, 5)
                for i in range(1,randint):
                    lines.insert(iterator + i, saltNOP)
                iterator += 1
            iterator += 1
    f = open(smaliCode, "w")
    f.writelines(lines)
    f.close()

    # reset iterator [ Salt with goto junk ]
    iterator = 0
    with open(smaliCode, "r") as fp:
        lines = fp.readlines()
        while iterator < len(lines):
            if "nop" in lines[iterator]:
                anotherRand = random.randint(1, 3)
                for i in range(0 ,anotherRand):
                    saltGOTOfront = "goto : gogo_" + str(counter) + "\n"
                    saltGOTOback = ": gogo_" + str(counter) + "\n\n"
                    lines.insert(iterator + i, saltGOTOfront)
                    lines.insert(iterator + 1 + i, saltGOTOback)
                    counter += 1
                    iterator += 2
            iterator += 1
    f = open(smaliCode, "w")
    f.writelines(lines)
    f.close()

def test():
    rootDir = 'output'
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        print('Found directory: %s' % dirName)
        if "smali" in dirName:
            print("yes")
    for fname in fileList:
        print('\t%s' % fname)

def test():


    return None
# .method <other_optional_stuff> <method_name>(<param>)<return_type>
method_pattern = re.compile(
    r"\.method.+?(?P<method_name>\S+?)"
    r"\((?P<method_param>\S*?)\)"
    r"(?P<method_return>\S+)",
    re.UNICODE,
)

# <spaces> value = <class_name>-><method>(<param>)<return_type>
annotation_method_pattern = re.compile(
    r"\s+value\s=\s(?P<method_object>\S+?)"
    r"->(?P<method_name>\S+?)"
    r"\((?P<method_param>\S*?)\)"
    r"(?P<method_return>\S+)",
    re.UNICODE,
)
# .class <other_optional_stuff> <class_name;>  # Every class name ends with ;
class_pattern = re.compile(r"\.class.+?(?P<class_name>\S+?;)", re.UNICODE)

# .super <class_name;>  # Every class name ends with ;
super_class_pattern = re.compile(r"\.super\s(?P<class_name>\S+?;)", re.UNICODE)
def get_non_empty_lines_from_file(file_name: str) -> List[str]:
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                # Return a list with the non blank lines contained in the file.
                return list(filter(None, (line.rstrip() for line in file)))
        except Exception as e:
            logger.error('Error during reading file "{0}": {1}'.format(file_name, e))
            raise
def get_android_class_names() -> List[str]:
    return get_non_empty_lines_from_file(
        os.path.join(
            os.path.dirname(__file__), "resources", "android_class_names_api_27.txt"
        )
    )
# .locals <number>
locals_pattern = re.compile(r"\s+\.locals\s(?P<local_count>\d+)")

# When iterating over list L, "for element in show_list_progress(L, interactive=True)"
# will show a progress bar. When setting "interactive=False", no progress bar will be
# shown. While using this method, no other code should write to standard output.
def show_list_progress(
    the_list: list,
    interactive: bool = False,
    unit: str = "file",
    description: str = None,
):
    if not interactive:
        return the_list
    #else:
    #    return tqdm(
    #        the_list,
     #       dynamic_ncols=True,
     #       unit=unit,
     #       desc=description,
     #       bar_format="{l_bar}{bar}|[{elapsed}<{remaining}, {rate_fmt}]",
     #   )

def get_api_reflection_smali_code() -> str:
    return get_text_from_file(
        os.path.join(
            os.path.dirname(__file__), "resources", "smali", "ApiReflection.smali"
        )
    )
def get_text_from_file(file_name: str) -> str:
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logger.error('Error during reading file "{0}": {1}'.format(file_name, e))
        raise

def get_smali_files(self) -> List[str]:

        if not self._is_decoded:
            self.decode_apk()

        return self._smali_files
class Reflection():
    def __init__(self):
        self.logger = logging.getLogger(
            "{0}.{1}".format(__name__, self.__class__.__name__)
        )
        super().__init__()

        self.android_class_names: Set[str] = set(get_android_class_names())

        self.methods_with_reflection: int = 0

        # Will be populated before running the reflection obfuscator.
        self.class_name_to_smali_file: dict = {}

        # Keep track of the length of the added instructions for reflection obfuscator,
        # since there is a limit for the number of maximum instructions in a try catch
        # block. Not all the instructions have the same length.
        self.obfuscator_instructions_length: int = 0
        self.obfuscator_instructions_limit: int = 60000

        self.primitive_types: Set[str] = {"I", "Z", "B", "S", "J", "F", "D", "C"}

        self.type_dict = {
            "I": "Ljava/lang/Integer;",
            "Z": "Ljava/lang/Boolean;",
            "B": "Ljava/lang/Byte;",
            "S": "Ljava/lang/Short;",
            "J": "Ljava/lang/Long;",
            "F": "Ljava/lang/Float;",
            "D": "Ljava/lang/Double;",
            "C": "Ljava/lang/Character;",
        }

        self.sget_dict = {
            "I": "Ljava/lang/Integer;->TYPE:Ljava/lang/Class;",
            "Z": "Ljava/lang/Boolean;->TYPE:Ljava/lang/Class;",
            "B": "Ljava/lang/Byte;->TYPE:Ljava/lang/Class;",
            "S": "Ljava/lang/Short;->TYPE:Ljava/lang/Class;",
            "J": "Ljava/lang/Long;->TYPE:Ljava/lang/Class;",
            "F": "Ljava/lang/Float;->TYPE:Ljava/lang/Class;",
            "D": "Ljava/lang/Double;->TYPE:Ljava/lang/Class;",
            "C": "Ljava/lang/Character;->TYPE:Ljava/lang/Class;",
        }

        self.cast_dict = {
            "I": "Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;",
            "Z": "Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;",
            "B": "Ljava/lang/Byte;->valueOf(B)Ljava/lang/Byte;",
            "S": "Ljava/lang/Short;->valueOf(S)Ljava/lang/Short;",
            "J": "Ljava/lang/Long;->valueOf(J)Ljava/lang/Long;",
            "F": "Ljava/lang/Float;->valueOf(F)Ljava/lang/Float;",
            "D": "Ljava/lang/Double;->valueOf(D)Ljava/lang/Double;",
            "C": "Ljava/lang/Character;->valueOf(C)Ljava/lang/Character;",
        }

        self.reverse_cast_dict = {
            "I": "Ljava/lang/Integer;->intValue()I",
            "Z": "Ljava/lang/Boolean;->booleanValue()Z",
            "B": "Ljava/lang/Byte;->byteValue()B",
            "S": "Ljava/lang/Short;->shortValue()S",
            "J": "Ljava/lang/Long;->longValue()J",
            "F": "Ljava/lang/Float;->floatValue()F",
            "D": "Ljava/lang/Double;->doubleValue()D",
            "C": "Ljava/lang/Character;->charValue()C",
        }

    def class_is_public_and_declared_in_smali(self, class_name: str) -> bool:
        smali_file: str = self.class_name_to_smali_file.get(class_name, None)

        # The smali of this class is not present (this is probably a system class).
        if not smali_file:
            return False

        with open(smali_file, "r", encoding="utf-8") as current_file:
            for line in current_file:
                # Check if this is a public non abstract class.
                class_match = class_pattern.match(line)
                if class_match:
                    if " public " in line and " abstract " not in line:
                        return True
                    else:
                        return False

    def method_is_all_public(
        self, class_name: str, method_signature: str, param_string: str
    ) -> bool:
        if not self.class_is_public_and_declared_in_smali(class_name):
            return False

        smali_file: str = self.class_name_to_smali_file[class_name]
        with open(smali_file, "r", encoding="utf-8") as current_file:
            for line in current_file:
                if " public " in line:
                    method_match = method_pattern.match(line)
                    if method_match:
                        signature = (
                            "{method_name}({method_param})"
                            "{method_return}".format(
                                method_name=method_match.group("method_name"),
                                method_param=method_match.group("method_param"),
                                method_return=method_match.group("method_return"),
                            )
                        )
                        if signature == method_signature:
                            # Public method declared in public class, let's check if all
                            # its parameters are public.
                            for param in self.split_method_params(param_string):
                                # System classes that are public.
                                if (
                                    param in self.primitive_types
                                    or param in self.android_class_names
                                ):
                                    continue

                                # The class of this parameter is not present in the
                                # smali files or is not public.
                                if not self.class_is_public_and_declared_in_smali(
                                    param
                                ):
                                    return False

                            return True

        return False

    def split_method_params(self, param_string: str) -> List[str]:
        params: List[str] = []

        possible_classes = param_string.split(";")
        for possible_class in possible_classes:
            # Make sure the parameter list is not empty.
            if possible_class:
                if possible_class.startswith("L"):
                    # Class.
                    params.append("{0};".format(possible_class))
                elif possible_class.startswith("["):
                    # Array + other optional parameters (e.g. [ILjava/lang/Object).
                    for string_position in range(1, len(possible_class)):
                        if possible_class[string_position] == "[":
                            # Multi-dimensional array, proceed with the next char.
                            continue
                        elif possible_class[string_position] == "L":
                            # Class array, no need to proceed with the next char.
                            params.append("{0};".format(possible_class))
                            break
                        else:
                            # Primitive type array, add it to the list and proceed with
                            # the rest of the string
                            params.append(possible_class[: string_position + 1])
                            params.extend(
                                self.split_method_params(
                                    possible_class[string_position + 1 :]
                                )
                            )
                            break
                elif possible_class[0] in self.primitive_types:
                    # Primitive type + other optional parameters
                    # (e.g. ILjava/lang/Object).
                    params.append(possible_class[0])
                    params.extend(self.split_method_params(possible_class[1:]))

        return params

    def count_needed_registers(self, params: List[str]) -> int:
        needed_registers: int = 0

        for param in params:
            # Long and double variables need 2 registers.
            if param == "J" or param == "D":
                needed_registers += 2
            else:
                needed_registers += 1

        return needed_registers

    def add_smali_reflection_code(
        self, class_name: str, method_name: str, param_string: str
    ) -> str:
        params = self.split_method_params(param_string)

        smali_code = "\n\tconst/4 v1, {param_num:#x}\n\n".format(param_num=len(params))
        self.obfuscator_instructions_length += 1

        if len(params) > 0:
            smali_code += "\tnew-array v1, v1, [Ljava/lang/Class;\n\n"
            self.obfuscator_instructions_length += 2

        for param_index, param in enumerate(params):
            smali_code += "\tconst/4 v2, {param_num:#x}\n\n".format(
                param_num=param_index
            )
            self.obfuscator_instructions_length += 1

            class_param = self.sget_dict.get(param, None)
            if class_param:
                smali_code += "\tsget-object v3, {param}\n\n".format(param=class_param)
                self.obfuscator_instructions_length += 2
            else:
                smali_code += "\tconst-class v3, {param}\n\n".format(param=param)
                self.obfuscator_instructions_length += 2

            smali_code += "\taput-object v3, v1, v2\n\n"
            self.obfuscator_instructions_length += 2

        smali_code += (
            "\tconst-class v2, {class_name}\n\n"
            '\tconst-string v3, "{method_name}"\n\n'.format(
                class_name=class_name, method_name=method_name
            )
        )
        self.obfuscator_instructions_length += 4

        smali_code += (
            "\tinvoke-virtual {v2, v3, v1}, Ljava/lang/Class;->"
            "getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)"
            "Ljava/lang/reflect/Method;\n\n"
        )
        self.obfuscator_instructions_length += 3

        smali_code += (
            "\tmove-result-object v1\n\n"
            "\tsget-object v2, Lcom/apireflectionmanager/ApiReflection;->"
            "obfuscatedMethods:Ljava/util/List;\n\n"
        )
        self.obfuscator_instructions_length += 3

        smali_code += (
            "\tinvoke-interface {v2, v1}, Ljava/util/List;->add(Ljava/lang/Object;)Z\n"
        )
        self.obfuscator_instructions_length += 3

        return smali_code

    def create_reflection_method(
        self,
        num_of_methods: int,
        local_count: int,
        is_virtual_method: bool,
        invoke_registers: str,
        invoke_parameters: str,
    ):
        # Split method passed registers (if the method has no registers there is an
        # empty line that has to be removed, that's why strip() is used).
        invoke_registers = [
            register.strip()
            for register in invoke_registers.split(", ")
            if register.strip()
        ]

        params = self.split_method_params(invoke_parameters)

        param_to_register: List[
            List[str]
        ] = []  # list[i][0] = i-th param, list[i][1] = [i-th param register(s)]

        if is_virtual_method:
            # If this is a virtual method, the first register is the object instance
            # and not a parameter.
            register_index = 1
            for param in params:
                # Long and double variables need 2 registers.
                if param == "J" or param == "D":
                    param_to_register.append(
                        [param, invoke_registers[register_index : register_index + 2]]
                    )
                    register_index += 2
                else:
                    param_to_register.append(
                        [param, [invoke_registers[register_index]]]
                    )
                    register_index += 1
        else:
            # This is a static method, so we don't need a reference to the object
            # instance. If this is a virtual method, the first register is the object
            # instance and not a parameter.
            register_index = 0
            for param in params:
                # Long and double variables need 2 registers.
                if param == "J" or param == "D":
                    param_to_register.append(
                        [param, invoke_registers[register_index : register_index + 2]]
                    )
                    register_index += 2
                else:
                    param_to_register.append(
                        [param, [invoke_registers[register_index]]]
                    )
                    register_index += 1

        smali_code = "\tconst/4 #reg1#, {register_num:#x}\n\n".format(
            register_num=len(params)
        )

        if len(params) > 0:
            smali_code += "\tnew-array #reg1#, #reg1#, [Ljava/lang/Object;\n\n"
            for param_index, param_and_register in enumerate(param_to_register):
                # param_and_register[0] = parameter type
                # param_and_register[1] = [register(s) holding the passed parameter(s)]
                cast_primitive_to_class = self.cast_dict.get(
                    param_and_register[0], None
                )

                if cast_primitive_to_class:
                    if len(param_and_register[1]) > 1:
                        # 2 register parameter.
                        smali_code += (
                            "\tinvoke-static {{{register_pair}}}, {cast}\n\n"
                            "\tmove-result-object #reg2#\n\n".format(
                                register_pair=", ".join(param_and_register[1]),
                                cast=cast_primitive_to_class,
                            )
                        )
                    else:
                        smali_code += (
                            "\tinvoke-static {{{register}}}, {cast}\n\n"
                            "\tmove-result-object #reg2#\n\n".format(
                                register=param_and_register[1][0],
                                cast=cast_primitive_to_class,
                            )
                        )

                    smali_code += (
                        "\tconst/4 #reg4#, {param_index:#x}\n\n"
                        "\taput-object #reg2#, #reg1#, #reg4#\n\n".format(
                            param_index=param_index
                        )
                    )

                else:
                    smali_code += (
                        "\tconst/4 #reg3#, {param_index:#x}\n\n"
                        "\taput-object {register}, #reg1#, #reg3#\n\n".format(
                            param_index=param_index, register=param_and_register[1][0]
                        )
                    )

        smali_code += "\tconst/16 #reg3#, {method_num:#x}\n\n".format(
            method_num=num_of_methods
        )

        if is_virtual_method:
            smali_code += (
                "\tinvoke-static {{#reg3#, {obj_instance}, #reg1#}}, "
                "Lcom/apireflectionmanager/ApiReflection;->"
                "obfuscate(ILjava/lang/Object;[Ljava/lang/Object;)"
                "Ljava/lang/Object;\n".format(obj_instance=invoke_registers[0])
            )
        else:
            smali_code += "\tconst/4 #reg4#, 0x0\n\n"
            smali_code += (
                "\tinvoke-static {#reg3#, #reg4#, #reg1#}, "
                "Lcom/apireflectionmanager/ApiReflection;->"
                "obfuscate(ILjava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;\n"
            )

        for index in range(0, 4):
            smali_code = smali_code.replace(
                "#reg{0}#".format(index + 1), "v{0}".format(local_count + index)
            )

        return smali_code


    def obfuscate(self):
        self.logger.info('Running "{0}" obfuscator'.format(self.__class__.__name__))

        try:
            for smali_file in show_list_progress(
                get_smali_files(),
                interactive= self.interactive,
                description="Class name to smali file mapping",
            ):
                with open(smali_file, "r", encoding="utf-8") as current_file:
                    class_name = None
                    for line in current_file:
                        if not class_name:
                            # Every smali file contains a class.
                            class_match = class_pattern.match(line)
                            if class_match:
                                self.class_name_to_smali_file[
                                    class_match.group("class_name")
                                ] = smali_file
                                break

            obfuscator_smali_code: str = ""

            move_result_pattern = re.compile(
                r"\s+move-result.*?\s(?P<register>[vp0-9]+)"
            )

            for smali_file in show_list_progress(
                get_smali_files(),
                interactive = self.interactive,
                description="Obfuscating using reflection",
            ):
                self.logger.debug(
                    'Obfuscating using reflection in file "{0}"'.format(smali_file)
                )

                # There is no space for further reflection instructions.
                if (
                    self.obfuscator_instructions_length
                    >= self.obfuscator_instructions_limit
                ):
                    break

                with open(smali_file, "r", encoding="utf-8") as current_file:
                    lines = current_file.readlines()

                # Line numbers where a method is declared.
                method_index: List[int] = []

                # For each method in method_index, True if there are enough registers
                # to perform some operations by using reflection, False otherwise.
                method_is_reflectable: List[bool] = []

                # The number of local registers of each method in method_index.
                method_local_count: List[int] = []

                # Find the method declarations in this smali file.
                for line_number, line in enumerate(lines):
                    method_match = method_pattern.match(line)
                    if method_match:
                        method_index.append(line_number)

                        param_count = self.count_needed_registers(
                            self.split_method_params(method_match.group("method_param"))
                        )

                        # Save the number of local registers of this method.
                        local_count = 16
                        local_match = locals_pattern.match(lines[line_number + 1])
                        if local_match:
                            local_count = int(local_match.group("local_count"))
                            method_local_count.append(local_count)
                        else:
                            # For some reason the locals declaration was not found where
                            # it should be, so assume the local registers are all used.
                            method_local_count.append(local_count)

                        # If there are enough registers available we can perform some
                        # reflection operations.
                        if param_count + local_count <= 11:
                            method_is_reflectable.append(True)
                        else:
                            method_is_reflectable.append(False)

                # Look for method invocations inside the methods declared in this
                # smali file, and change normal invocations with invocations through
                # reflection.
                for method_number, index in enumerate(method_index):

                    # If there are enough registers for reflection operations, look for
                    # method invocations inside each method's body.
                    if method_is_reflectable[method_number]:
                        current_line_number = index
                        while not lines[current_line_number].startswith(".end method"):

                            # There is no space for further reflection instructions.
                            if (
                                self.obfuscator_instructions_length
                                >= self.obfuscator_instructions_limit
                            ):
                                break

                            current_line_number += 1

                            invoke_match = invoke_pattern.match(
                                lines[current_line_number]
                            )

                            if (
                                invoke_match
                                and "<init>" not in lines[current_line_number]
                            ):

                                # The method belongs to an Android class or is
                                # invoked on an array.
                                if invoke_match.group(
                                    "invoke_object"
                                ) in self.android_class_names or invoke_match.group(
                                    "invoke_object"
                                ).startswith(
                                    "["
                                ):
                                    continue

                                method_signature = (
                                    "{method_name}({method_param})"
                                    "{method_return}".format(
                                        method_name=invoke_match.group("invoke_method"),
                                        method_param=invoke_match.group("invoke_param"),
                                        method_return=invoke_match.group(
                                            "invoke_return"
                                        ),
                                    )
                                )

                                # The method to reflect has to be public, has to be
                                # declared in a public class and all its parameters
                                # have to be public.
                                if not self.method_is_all_public(
                                    invoke_match.group("invoke_object"),
                                    method_signature,
                                    invoke_match.group("invoke_param"),
                                ):
                                    continue

                                if (
                                    invoke_match.group("invoke_type")
                                    == "invoke-virtual"
                                ):
                                    tmp_is_virtual = True
                                elif (
                                    invoke_match.group("invoke_type") == "invoke-static"
                                ):
                                    tmp_is_virtual = False
                                else:
                                    continue

                                tmp_register = invoke_match.group("invoke_pass")
                                tmp_class_name = invoke_match.group("invoke_object")
                                tmp_method = invoke_match.group("invoke_method")
                                tmp_param = invoke_match.group("invoke_param")
                                tmp_return_type = invoke_match.group("invoke_return")

                                # Check if the method invocation result is used in
                                # the following lines.
                                for move_result_index in range(
                                    current_line_number + 1,
                                    min(current_line_number + 10, len(lines) - 1),
                                ):
                                    if "invoke-" in lines[move_result_index]:
                                        # New method invocation, the previous method
                                        # result is not used.
                                        break

                                    move_result_match = move_result_pattern.match(
                                        lines[move_result_index]
                                    )
                                    if move_result_match:
                                        tmp_result_register = move_result_match.group(
                                            "register"
                                        )

                                        # Fix the move-result instruction after the
                                        # method invocation.
                                        new_move_result = ""
                                        if tmp_return_type in self.primitive_types:
                                            new_move_result += (
                                                "\tmove-result-object "
                                                "{result_register}\n\n"
                                                "\tcheck-cast {result_register}, "
                                                "{result_class}\n\n".format(
                                                    result_register=tmp_result_register,
                                                    result_class=self.type_dict[
                                                        tmp_return_type
                                                    ],
                                                )
                                            )

                                            new_move_result += "\tinvoke-virtual " "{{{result_register}}}, {cast}\n\n".format(
                                                result_register=tmp_result_register,
                                                cast=self.reverse_cast_dict[
                                                    tmp_return_type
                                                ],
                                            )

                                            if (
                                                tmp_return_type == "J"
                                                or tmp_return_type == "D"
                                            ):
                                                new_move_result += (
                                                    "\tmove-result-wide "
                                                    "{result_register}\n".format(
                                                        result_register=tmp_result_register
                                                    )
                                                )
                                            else:
                                                new_move_result += (
                                                    "\tmove-result "
                                                    "{result_register}\n".format(
                                                        result_register=tmp_result_register
                                                    )
                                                )

                                        else:
                                            new_move_result += (
                                                "\tmove-result-object "
                                                "{result_register}\n\n"
                                                "\tcheck-cast {result_register}, "
                                                "{return_type}\n".format(
                                                    result_register=tmp_result_register,
                                                    return_type=tmp_return_type,
                                                )
                                            )

                                        lines[move_result_index] = new_move_result

                                # Add the original method to the list of methods
                                # using reflection.
                                obfuscator_smali_code += self.add_smali_reflection_code(
                                    tmp_class_name, tmp_method, tmp_param
                                )

                                # Change the original code with code using reflection.
                                lines[
                                    current_line_number
                                ] = self.create_reflection_method(
                                    self.methods_with_reflection,
                                    method_local_count[method_number],
                                    tmp_is_virtual,
                                    tmp_register,
                                    tmp_param,
                                )

                                self.methods_with_reflection += 1

                                # Add the registers needed for performing reflection.
                                lines[index + 1] = "\t.locals {0}\n".format(
                                    method_local_count[method_number] + 4
                                )

                with open(smali_file, "w", encoding="utf-8") as current_file:
                    current_file.writelines(lines)

            # Add to the app the code needed for the reflection obfuscator. The code
            # can be put in any smali directory, since it will be moved to the correct
            # directory when rebuilding the application.
            destination_dir = os.path.dirname(get_smali_files()[0])
            destination_file = os.path.join(destination_dir, "ApiReflection.smali")
            with open(destination_file, "w", encoding="utf-8") as api_reflection_smali:
                reflection_code = get_api_reflection_smali_code().replace(
                    "#!code_to_replace!#", obfuscator_smali_code
                )
                api_reflection_smali.write(reflection_code)

        except Exception as e:
            self.logger.error(
                'Error during execution of "{0}" obfuscator: {1}'.format(
                    self.__class__.__name__, e
                )
            )
            raise

        finally:
            self.used_obfuscators.append(self.__class__.__name__)

# -------------------- GUI Window --------------------

btn = Button(window, text='Step 1: Open & Decompile', command=lambda: open_file()).pack(side=TOP, pady=10)
#btn2 = Button(window, text='Remove Comments', command=lambda: nocomment()).pack(side=TOP, pady=10)
btn3 = Button(window, text='Step 2: Obfuscate Smali', command=lambda: obfuscate_smali_file()).pack(side=TOP, pady=10)
btn4 = Button(window, text='Step 3: Recompile', command=lambda: apk_recompile_sign(file_name)).pack(side=TOP, pady=10)

progress = Progressbar(window, orient=HORIZONTAL, length=400, mode="determinate")
progress.pack(pady=20)

window.mainloop()