from __future__ import annotations
from load_class_files import load_class_files
from typing import List, Dict, Union, Tuple
from enum import Enum
from copy import deepcopy
import json

JSON_CONTENT = Dict[str, Union[str, List[Union[str, Dict]], Dict]]


class JavaMethod:
    def __init__(self, json_content: JSON_CONTENT) -> None:
        self.json_content = json_content
        self.id = self.json_content["name"]
        self.bytecode_json: List[JSON_CONTENT] = json_content["code"]["bytecode"]


class JavaClass:
    def __init__(self, json_str: str) -> None:
        self.json_content: JSON_CONTENT = json.loads(json_str)
        self.id = self.json_content["name"]

        self.method_dict: Dict[str, JavaMethod] = {}
        for method_json in self.json_content["methods"]:
            # only handle method with "@Case"
            annotations_json: List[JSON_CONTENT] = method_json["annotations"]
            for annotation_json in annotations_json:
                if annotation_json["type"] == "dtu/compute/exec/Case":
                    java_method = JavaMethod(method_json)
                    self.method_dict[java_method.id] = java_method
                    break


class AbstractType(Enum):
    VOID = "Void"
    ANY_INT = "Any Int"  # any int value


class AbstractVariable:
    def __init__(self, variable_type: AbstractType) -> None:
        self.type = variable_type

    def __str__(self) -> str:
        return f"{str(self.type)}"

    def __add__(self, b: AbstractVariable | int) -> AbstractVariable:
        if isinstance(b, AbstractVariable):
            match self.type:
                case AbstractType.ANY_INT:
                    match b.type:
                        case AbstractType.ANY_INT:
                            return AbstractVariable(AbstractType.ANY_INT)

                        case _:
                            raise Exception(b.type)

                case _:
                    raise Exception(self.type)
        elif isinstance(b, int):
            return AbstractVariable(AbstractType.ANY_INT)
        else:
            raise Exception(b)
    
    def __radd(self, a: AbstractVariable | int) -> AbstractVariable:
        return self.__add__(a)


class ProgramCounter:
    def __init__(self, java_method: JavaMethod) -> None:
        self.index = 0
        self.java_method = java_method

    def get_current_operation(self) -> JSON_CONTENT:
        return self.java_method.bytecode_json[self.index]


class AbstractMethodStack:
    def __init__(
        self, parameters: Dict[int, AbstractVariable], java_method: JavaMethod
    ) -> None:
        self.local_variables = parameters
        self.operate_stack: List[Union[AbstractVariable, int]] = []
        self.program_counter = ProgramCounter(java_method)


class JavaProgram:
    def __init__(
        self, project_name: str, init_class_name: str, init_method_name: str
    ) -> None:
        self.java_class_dict: Dict[str, JavaClass] = {}
        for json_str in load_class_files(project_name):
            java_class = JavaClass(json_str)
            self.java_class_dict[java_class.id] = java_class

        self.init_class_name = init_class_name
        self.init_method_name = init_method_name
        self.init_method = self.java_class_dict[init_class_name].method_dict[
            init_method_name
        ]


class AbstractInterpreter:
    def __init__(
        self, java_program: JavaProgram, init_peremeters: List[AbstractVariable]
    ) -> None:
        self.java_program = java_program
        self.stack: List[AbstractMethodStack] = []

        init_local_vars: Dict[int, AbstractVariable] = {}
        for i in range(len(init_peremeters)):
            init_local_vars[i] = init_peremeters[i]
        init_method_stack = AbstractMethodStack(
            init_local_vars, self.java_program.init_method
        )
        self.stack.append(init_method_stack)

        self.return_value = AbstractVariable(AbstractType.VOID)

    def step(self) -> bool:
        """
        return true indicates operation continues
        return false indicates operation ends
        """
        top_stack = self.stack[-1]
        operation_json = top_stack.program_counter.get_current_operation()
        opr_type: str = operation_json["opr"]

        match opr_type:
            case "return":
                return_type: None | str = operation_json["type"]
                match return_type:
                    case None:
                        return_value = AbstractVariable(AbstractType.VOID)

                    case "int":
                        return_value = top_stack.operate_stack.pop()

                    case _:
                        raise Exception(return_type)

                if len(self.stack) > 1 and return_value.type != AbstractType.VOID:
                    self.stack[-2].operate_stack.append(return_value)
                else:
                    self.return_value = return_value

                self.log_operation(f"{opr_type} {return_type}")

                # pop and return
                self.stack.pop()

            case "push":
                value_json: Dict[str, Union[int, str]] = operation_json["value"]
                value_type = value_json["type"]
                match value_type:
                    case "integer":
                        value_value: int = value_json["value"]
                        top_stack.operate_stack.append(value_value)
                        self.log_operation(f"{opr_type} {value_value}")

                    case _:
                        raise Exception(value_type)

            case "load":
                load_type: str = operation_json["type"]
                match load_type:
                    case "int":
                        load_index: int = operation_json["index"]
                        top_stack.operate_stack.append(
                            deepcopy(top_stack.local_variables[load_index])
                        )
                        self.log_operation(
                            f"{opr_type}, type: {load_type}, index: {load_index}"
                        )

                    case _:
                        raise Exception(load_type)

            case "binary":
                binary_operant = operation_json["operant"]
                binary_type = operation_json["type"]
                operand_b = top_stack.operate_stack.pop()
                operand_a = top_stack.operate_stack.pop()

                match binary_operant:
                    case "add":
                        match binary_type:
                            case "int":
                                result = operand_a + operand_b
                                top_stack.operate_stack.append(result)
                                self.log_operation(f"{binary_operant} {binary_type}")
                            
                            case _:
                                raise Exception

            case _:
                raise Exception(opr_type)

        top_stack.program_counter.index += 1  # step 1
        if len(self.stack) > 0:
            return True
        else:
            return False

    def log_operation(self, log_str: str) -> None:
        print("Operation:", log_str)

    def log_start(self) -> None:
        print("---starting program---")
        print("init class:", self.java_program.init_class_name)
        print("init method:", self.java_program.init_method_name)
        print()

    def log_state(self) -> None:
        print("---state---")
        print("stack size:", len(self.stack))
        print("top stack")
        top_stack = self.stack[-1]
        var_str = ""
        for i in top_stack.local_variables.keys():
            var_str += f"{i}: {top_stack.local_variables[i]}"
            if i != len(top_stack.local_variables) - 1:
                var_str += ", "
        print(" ", "local variables:", f"{{{var_str}}}")
        print(
            " ",
            "operate stack:",
            f"[{', '.join(str(x) for x in top_stack.operate_stack)}]",
        )
        print(" ", "program counter index:", top_stack.program_counter.index)
        print()

    def log_done(self) -> None:
        print("---final state---")
        print("stack size:", len(self.stack))
        print("return value:", str(self.return_value))

    def run(self) -> None:
        self.log_start()
        self.log_state()
        while self.step():
            self.log_state()
        self.log_done()


# test code
if __name__ == "__main__":
    java_program = JavaProgram(
        "course-02242-examples", "dtu/compute/exec/Simple", "add"
    )
    java_interpreter = AbstractInterpreter(
        java_program,
        [
            AbstractVariable(AbstractType.ANY_INT),
            1,
        ],
    )
    java_interpreter.run()
