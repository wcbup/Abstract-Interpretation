from __future__ import annotations
from load_class_files import load_class_files
from typing import List, Dict, Union, Tuple, Set
from enum import Enum
from copy import deepcopy
import json

JSON_CONTENT = Dict[str, Union[str, List[Union[str, Dict]], Dict]]


class AbstractMode(Enum):
    ANY_INT = "Any Int"
    SIGN = "Sign"


ABSTRACT_MODE = AbstractMode.SIGN


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
    INT = "Int"
    VOID = "Void"
    ANY_INT = "Any Int"  # any int value
    POSITIVE_INT = "Positive Int"  # positive int
    NEGATIVE_INT = "Negative Int"  # negative int
    NOT_POSITIVE_INT = "Not Positive Int"  # not positive int
    NOT_NEGATIVE_INT = "Not Negative Int"  # not negative int
    NOT_ZERO = "Not Zero"  # not zero


class ExceptionType(Enum):
    ARITHMETIC_EXCEPTION = "Arithmetic Exception"


class AbstractVariable:
    def __init__(
        self, variable: AbstractType | int, memory_id: None | int = None
    ) -> None:
        self.memory_id = memory_id  # the index in the memory
        if isinstance(variable, AbstractType):
            self.type = variable
            self.value = None
        elif isinstance(variable, int):
            self.value = variable
            self.type = AbstractType.INT
        else:
            raise Exception

    def __str__(self) -> str:
        return f"{str(self.type)}: {str(self.value)}"

    def __add__(self, b: AbstractVariable) -> AbstractVariable:
        if not isinstance(b, AbstractVariable):
            raise Exception
        match self.type:
            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.ANY_INT | AbstractType.INT | AbstractType.POSITIVE_INT:
                        return AbstractVariable(AbstractType.ANY_INT)

                    case _:
                        raise Exception(b.type)

            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return AbstractVariable(self.value + b.value)

                    case AbstractType.ANY_INT:
                        return AbstractVariable(AbstractType.ANY_INT)

                    case _:
                        raise Exception(b.type)

            case _:
                raise Exception(self.type)

    def __sub__(self, b: AbstractVariable) -> AbstractVariable:
        if not isinstance(b, AbstractVariable):
            raise Exception
        match self.type:
            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return AbstractVariable(self.value - b.value)

                    case AbstractType.ANY_INT:
                        return AbstractVariable(AbstractType.ANY_INT)

                    case AbstractType.NOT_POSITIVE_INT:
                        if self.value == 0:
                            return AbstractVariable(AbstractType.NOT_NEGATIVE_INT)
                        elif self.value > 0:
                            return AbstractVariable(AbstractType.POSITIVE_INT)
                        else:
                            return AbstractVariable(AbstractType.ANY_INT)

                    case _:
                        raise Exception(b.type)

            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.INT | AbstractType.ANY_INT:
                        return AbstractVariable(AbstractType.ANY_INT)

                    case _:
                        raise Exception(b.type)

            case _:
                raise Exception(self.type)

    def __truediv__(self, b: AbstractVariable) -> AbstractVariable:
        if not isinstance(b, AbstractVariable):
            raise Exception
        match self.type:
            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return AbstractVariable(int(self.value / b.value))

                    case AbstractType.ANY_INT:
                        return AbstractVariable(AbstractType.ANY_INT)

                    case AbstractType.POSITIVE_INT:
                        if self.value > 0:
                            return AbstractVariable(AbstractType.POSITIVE_INT)
                        elif self.value < 0:
                            return AbstractVariable(AbstractType.NEGATIVE_INT)
                        else:
                            return AbstractVariable(0)

                    case _:
                        raise Exception(b.type)

            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.INT | AbstractType.ANY_INT | AbstractType.NOT_NEGATIVE_INT | AbstractType.NOT_POSITIVE_INT:
                        return AbstractVariable(AbstractType.ANY_INT)

                    case _:
                        raise Exception(b.type)

            case _:
                raise Exception(self.type)

    def __ge__(self, b: AbstractVariable) -> bool | None:
        if not isinstance(b, AbstractVariable):
            raise Exception
        match self.type:
            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return self.value >= b.value

                    case AbstractType.ANY_INT:
                        return None

                    case _:
                        raise Exception(b.type)

            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.INT | AbstractType.ANY_INT:
                        return None

                    case _:
                        raise Exception

            case _:
                raise Exception

    def __gt__(
        self, b: AbstractVariable
    ) -> (
        bool
        | None
        | Tuple[
            Tuple[AbstractVariable, AbstractVariable],
            Tuple[AbstractVariable, AbstractVariable],
        ]
    ):
        """
        return bool if result is specific
        return None if result is unkown
        return Tuple with update variabls tuples,
            the first tuple is the variables when result is true
            the second tuple is the variables when result is false
        """
        if not isinstance(b, AbstractVariable):
            raise Exception
        match self.type:
            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return self.value > b.value

                    case AbstractType.ANY_INT:
                        return None

                    case _:
                        raise Exception(b.type)

            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.ANY_INT:
                        return None

                    case AbstractType.INT:
                        match ABSTRACT_MODE:
                            case AbstractMode.ANY_INT:
                                return None

                            case AbstractMode.SIGN:
                                true_variables = (
                                    AbstractVariable(AbstractType.POSITIVE_INT),
                                    AbstractVariable(0),
                                )
                                true_variables[0].memory_id = self.memory_id
                                true_variables[1].memory_id = b.memory_id
                                false_variables = (
                                    AbstractVariable(AbstractType.NOT_POSITIVE_INT),
                                    AbstractVariable(0),
                                )
                                false_variables[0].memory_id = self.memory_id
                                false_variables[1].memory_id = b.memory_id
                                return true_variables, false_variables

                            case _:
                                raise Exception(ABSTRACT_MODE)

                    case _:
                        raise Exception

            case _:
                raise Exception

    def __lt__(
        self, b: AbstractVariable
    ) -> (
        bool
        | None
        | Tuple[
            Tuple[AbstractVariable, AbstractVariable],
            Tuple[AbstractVariable, AbstractVariable],
        ]
    ):
        """
        return bool if result is specific
        return None if result is unkown
        return Tuple with update variabls tuples,
            the first tuple is the variables when result is true
            the second tuple is the variables when result is false
        """
        if not isinstance(b, AbstractVariable):
            raise Exception
        match self.type:
            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return self.value < b.value

                    case _:
                        raise Exception(b.type)

            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.ANY_INT:
                        return None

                    case AbstractType.INT:
                        match ABSTRACT_MODE:
                            case AbstractMode.ANY_INT:
                                return None

                            case AbstractMode.SIGN:
                                true_variables = (
                                    AbstractVariable(AbstractType.NEGATIVE_INT),
                                    AbstractVariable(0),
                                )
                                true_variables[0].memory_id = self.memory_id
                                true_variables[1].memory_id = b.memory_id
                                false_variables = (
                                    AbstractVariable(AbstractType.NOT_NEGATIVE_INT),
                                    AbstractVariable(0),
                                )
                                false_variables[0].memory_id = self.memory_id
                                false_variables[1].memory_id = b.memory_id
                                return true_variables, false_variables

                            case _:
                                raise Exception(ABSTRACT_MODE)

                    case _:
                        raise Exception(b.type)

            case AbstractType.POSITIVE_INT:
                match b.type:
                    case AbstractType.INT:
                        if b.value <= 0:
                            return False
                        else:
                            return None

                    case _:
                        raise Exception(b.type)

            case _:
                raise Exception(self.type)

    def __le__(
        self, b: AbstractVariable
    ) -> (
        bool
        | None
        | Tuple[
            Tuple[AbstractVariable, AbstractVariable],
            Tuple[AbstractVariable, AbstractVariable],
        ]
    ):
        """
        return bool if result is specific
        return None if result is unkown
        return Tuple with update variabls tuples,
            the first tuple is the variables when result is true
            the second tuple is the variables when result is false
        """
        if not isinstance(b, AbstractVariable):
            raise Exception
        match self.type:
            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return self.value <= b.value

                    case _:
                        raise Exception

            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.ANY_INT:
                        return None

                    case AbstractType.INT:
                        match ABSTRACT_MODE:
                            case AbstractMode.ANY_INT:
                                return None

                            case AbstractMode.SIGN:
                                true_variables = (
                                    AbstractVariable(AbstractType.NOT_POSITIVE_INT),
                                    AbstractVariable(0),
                                )
                                true_variables[0].memory_id = self.memory_id
                                true_variables[1].memory_id = b.memory_id
                                false_variables = (
                                    AbstractVariable(AbstractType.POSITIVE_INT),
                                    AbstractVariable(0),
                                )
                                false_variables[0].memory_id = self.memory_id
                                false_variables[1].memory_id = b.memory_id
                                return true_variables, false_variables

                            case _:
                                raise Exception(ABSTRACT_MODE)

                    case _:
                        raise Exception

            case _:
                raise Exception

    def __ne__(
        self, b: AbstractVariable
    ) -> (
        bool
        | None
        | Tuple[
            Tuple[AbstractVariable, AbstractVariable],
            Tuple[AbstractVariable, AbstractVariable],
        ]
    ):
        """
        return bool if result is specific
        return None if result is unkown
        return Tuple with update variabls tuples,
            the first tuple is the variables when result is true
            the second tuple is the variables when result is false
        """
        if not isinstance(b, AbstractVariable):
            raise Exception

        match self.type:
            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return self.value != b.value

                    case _:
                        raise Exception

            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.ANY_INT:
                        return None

                    case AbstractType.INT:
                        match ABSTRACT_MODE:
                            case AbstractMode.ANY_INT:
                                return None

                            case AbstractMode.SIGN:
                                true_variables = (
                                    AbstractVariable(AbstractType.NOT_ZERO),
                                    AbstractVariable(0),
                                )
                                true_variables[0].memory_id = self.memory_id
                                true_variables[1].memory_id = b.memory_id
                                false_variables = (
                                    AbstractVariable(0),
                                    AbstractVariable(0),
                                )
                                false_variables[0].memory_id = self.memory_id
                                false_variables[1].memory_id = b.memory_id
                                return true_variables, false_variables

                            case _:
                                raise Exception(ABSTRACT_MODE)

                    case _:
                        raise Exception

            case _:
                raise Exception

    def __eq__(self, b: AbstractVariable) -> bool | None:
        if not isinstance(b, AbstractVariable):
            raise Exception

        match self.type:
            case AbstractType.INT:
                match b.type:
                    case AbstractType.INT:
                        return self.value == b.value

                    case _:
                        raise Exception

            case AbstractType.ANY_INT:
                match b.type:
                    case AbstractType.INT | AbstractType.ANY_INT:
                        return None

                    case _:
                        raise Exception

            case _:
                raise Exception


class ProgramCounter:
    def __init__(self, java_method: JavaMethod) -> None:
        self.index = 0
        self.java_method = java_method

    def get_current_operation(self) -> JSON_CONTENT:
        return self.java_method.bytecode_json[self.index]


class AbstractMethodStack:
    def __init__(
        self,
        parameters: Dict[int, AbstractVariable],
        java_method: JavaMethod,
    ) -> None:
        self.local_variables = parameters
        self.operate_stack: List[Union[AbstractVariable, bool]] = []
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


class IdGenerator:
    def __init__(self) -> None:
        self.id = 0

    def get_new_id(self) -> int:
        self.id += 1
        return self.id


class AbstractState:
    def __init__(self, id: int, stack: List[AbstractMethodStack]) -> None:
        self.id = id
        self.stack = stack
        self.return_value = AbstractVariable(AbstractType.VOID)


class AbstractInterpreter:
    def __init__(
        self, java_program: JavaProgram, init_peremeters: List[AbstractVariable]
    ) -> None:
        self.java_program = java_program
        self.state_list: List[AbstractState] = []
        init_stack: List[AbstractMethodStack] = []
        self.id_generator = IdGenerator()

        init_local_vars: Dict[AbstractVariable] = {}
        for i in range(len(init_peremeters)):
            init_peremeters[i].memory_id = i
            init_local_vars[i] = init_peremeters[i]
        init_method_stack = AbstractMethodStack(
            init_local_vars, self.java_program.init_method
        )
        init_stack.append(init_method_stack)
        init_state = AbstractState(self.id_generator.get_new_id(), init_stack)
        self.state_list.append(init_state)

        self.yes_exception_set: Set[ExceptionType] = set()
        self.maybe_exception_set: Set[ExceptionType] = set()

    def step(self, state: AbstractState) -> List[AbstractState]:
        """
        return the next state list
        """
        top_stack = state.stack[-1]
        operation_json = top_stack.program_counter.get_current_operation()
        opr_type: str = operation_json["opr"]
        next_state_list: List[AbstractState] = []

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

                if len(state.stack) > 1 and return_value.type != AbstractType.VOID:
                    state.stack[-2].operate_stack.append(return_value)
                else:
                    state.return_value = return_value

                self.log_operation(f"{opr_type} {return_type}")

                # pop and return
                state.stack.pop()

            case "push":
                value_json: Dict[str, Union[int, str]] = operation_json["value"]
                value_type = value_json["type"]
                match value_type:
                    case "integer":
                        value_value: int = value_json["value"]
                        top_stack.operate_stack.append(AbstractVariable(value_value))
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

            case "store":
                store_type = operation_json["type"]
                store_index: int = operation_json["index"]
                store_value = top_stack.operate_stack.pop()
                match store_type:
                    case "int":
                        store_value.memory_id = store_index
                        top_stack.local_variables[store_index] = store_value
                        self.log_operation(f"{opr_type}, type: {store_type}")

                    case _:
                        raise Exception(store_type)

            case "get":
                field_json = operation_json["field"]
                field_name: str = field_json["name"]
                # hard code `$assertionsDisabled` to False
                if field_name == "$assertionsDisabled":
                    top_stack.operate_stack.append(False)
                else:
                    # TBD
                    raise Exception
                self.log_operation(f"{opr_type}, {field_name}")

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

                            case _:
                                raise Exception(binary_type)

                    case "sub":
                        match binary_type:
                            case "int":
                                result = operand_a - operand_b
                                top_stack.operate_stack.append(result)

                            case _:
                                raise Exception(binary_type)

                    case "div":
                        match binary_type:
                            case "int":
                                if (
                                    operand_b.type == AbstractType.INT
                                    and operand_b.value == 0
                                ):
                                    # record the exception
                                    exception_type = ExceptionType.ARITHMETIC_EXCEPTION
                                    self.log_operation(
                                        f"---find one exception---\n{exception_type}"
                                    )
                                    self.yes_exception_set.add(exception_type)
                                    state.stack.clear()  # empty the stack, simply return
                                    self.log_operation("exiting")
                                elif (
                                    operand_b.type == AbstractType.ANY_INT
                                    or operand_b.type == AbstractType.NOT_NEGATIVE_INT
                                    or operand_b.type == AbstractType.NOT_POSITIVE_INT
                                ):
                                    # record the exception
                                    exception_type = ExceptionType.ARITHMETIC_EXCEPTION
                                    self.log_operation(
                                        f"---find one exception---\n{exception_type}"
                                    )
                                    self.yes_exception_set.add(exception_type)
                                    result = operand_a / operand_b
                                    top_stack.operate_stack.append(result)
                                else:
                                    result = operand_a / operand_b
                                    top_stack.operate_stack.append(result)

                    case _:
                        raise Exception(binary_operant)

                self.log_operation(f"{binary_operant} {binary_type}")

            case "negate":
                negate_type = operation_json["type"]
                operand = top_stack.operate_stack.pop()
                match negate_type:
                    case "int":
                        result = AbstractVariable(0) - operand

                    case _:
                        raise Exception(negate_type)

                top_stack.operate_stack.append(result)

                self.log_operation(f"{opr_type}, {negate_type}")

            case "incr":
                incr_index: int = operation_json["index"]
                incr_amount: int = operation_json["amount"]
                incr_val = top_stack.local_variables[incr_index]
                top_stack.local_variables[incr_index] = incr_val + AbstractVariable(
                    incr_amount
                )
                self.log_operation(
                    f"{opr_type}, index: {incr_index}, amount: {incr_amount}"
                )

            case "goto":
                goto_target = operation_json["target"]
                top_stack.program_counter.index = goto_target - 1
                self.log_operation(f"{opr_type}, target: {goto_target}")

            case "if":
                if_condition: str = operation_json["condition"]
                if_target: int = operation_json["target"]
                operand_b = top_stack.operate_stack.pop()
                operand_a = top_stack.operate_stack.pop()
                self.log_operation(
                    f"{opr_type}, condition: {if_condition}, target: {if_target}"
                )
                match if_condition:
                    case "gt":
                        result = operand_a > operand_b

                    case "le":
                        result = operand_a <= operand_b

                    case "ge":
                        result = operand_a >= operand_b

                    case _:
                        raise Exception(if_condition)

                match result:
                    case False:
                        None  # do nothing

                    case True:
                        top_stack.program_counter.index = if_target - 1

                    case None:
                        new_state = deepcopy(state)
                        new_state.id = self.id_generator.get_new_id()
                        self.log_operation(
                            f"------create new state, id: {new_state.id}------"
                        )
                        self.log_state(new_state)
                        next_state_list.append(new_state)

                        top_stack.program_counter.index = if_target - 1

                    case tuple():
                        true_variables, false_variables = result
                        false_state = deepcopy(state)
                        false_state.id = self.id_generator.get_new_id()
                        for variable in false_variables:
                            if variable.memory_id != None:
                                false_state.stack[-1].local_variables[
                                    variable.memory_id
                                ] = variable
                        self.log_operation(
                            f"------create new state, id: {false_state.id}------"
                        )
                        self.log_state(false_state)
                        next_state_list.append(false_state)

                        for variable in true_variables:
                            if variable.memory_id != None:
                                state.stack[-1].local_variables[
                                    variable.memory_id
                                ] = variable
                        top_stack.program_counter.index = if_target - 1

                    case _:
                        raise Exception(result)

            case "ifz":
                operand = top_stack.operate_stack.pop()
                if isinstance(operand, bool):
                    if operand == True:
                        operand = AbstractVariable(1)
                    elif operand == False:
                        operand = AbstractVariable(0)

                ifz_condition = operation_json["condition"]
                ifz_target = operation_json["target"]

                self.log_operation(
                    f"{opr_type}, condition: {ifz_condition}, target: {ifz_target}"
                )
                match ifz_condition:
                    case "ne":
                        result = operand != AbstractVariable(0)

                    case "le":
                        result = operand <= AbstractVariable(0)

                    case "gt":
                        result = operand > AbstractVariable(0)

                    case "eq":
                        result = operand == AbstractVariable(0)

                    case "lt":
                        result = operand < AbstractVariable(0)

                    case _:
                        raise Exception(ifz_condition)

                match result:
                    case False:
                        None  # do nothing

                    case True:
                        top_stack.program_counter.index = ifz_target - 1

                    case None:
                        new_state = deepcopy(state)
                        new_state.id = self.id_generator.get_new_id()
                        self.log_operation(
                            f"------create new state, id: {new_state.id}------"
                        )
                        self.log_state(new_state)
                        next_state_list.append(new_state)

                        top_stack.program_counter.index = ifz_target - 1

                    case tuple():
                        true_variables, false_variables = result
                        false_state = deepcopy(state)
                        false_state.id = self.id_generator.get_new_id()
                        for variable in false_variables:
                            if variable.memory_id != None:
                                false_state.stack[-1].local_variables[
                                    variable.memory_id
                                ] = variable
                        self.log_operation(
                            f"------create new state, id: {false_state.id}------"
                        )
                        self.log_state(false_state)
                        next_state_list.append(false_state)

                        for variable in true_variables:
                            if variable.memory_id != None:
                                state.stack[-1].local_variables[
                                    variable.memory_id
                                ] = variable
                        top_stack.program_counter.index = ifz_target - 1

                    case _:
                        raise Exception(result)

            case "new":
                class_name = operation_json["class"]
                # hard code new `java/lang/AssertionError`
                if class_name == "java/lang/AssertionError":
                    self.log_operation(f"thorw AssertionError!")
                    # simply return
                    state.stack.clear()
                else:
                    # TBD
                    raise Exception

            case _:
                raise Exception(opr_type)

        top_stack.program_counter.index += 1  # step 1
        for new_state in next_state_list:
            new_state.stack[-1].program_counter.index += 1
        if len(state.stack) > 0:
            next_state_list.append(state)
            self.log_state(state)
        else:
            self.log_done(state)

        return next_state_list

    def log_operation(self, log_str: str) -> None:
        print("Operation:", log_str)

    def log_start(self) -> None:
        print("---starting program---")
        print("init class:", self.java_program.init_class_name)
        print("init method:", self.java_program.init_method_name)
        print()

    def log_state(self, state: AbstractState) -> None:
        print("---state---  id:", state.id)
        print("stack size:", len(state.stack))
        print("top stack")
        top_stack = state.stack[-1]
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

    def log_done(self, state: AbstractState) -> None:
        print("---final state---  id:", state.id)
        print("stack size:", len(state.stack))
        print("return value:", str(state.return_value))
        print()

    def log_exception(self) -> None:
        print("---exception---")
        print("Yes Exception:")
        for exception_type in self.yes_exception_set:
            print(" ", exception_type)
        print()

    def run(self, step_limit: int) -> None:
        self.log_start()

        index = 0
        while len(self.state_list) > 0 and index < step_limit:
            index += 1

            next_state_list: List[AbstractState] = []
            for state in self.state_list:
                next_state_list += self.step(state)
            self.state_list = next_state_list

        if index == step_limit:
            print("Reach the step limit, exit!")

        self.log_exception()


# test code
if __name__ == "__main__":
    java_program = JavaProgram(
        "course-02242-examples",
        "eu/bogoe/dtu/exceptional/Arithmetics",
        "alwaysThrows4",
    )
    java_interpreter = AbstractInterpreter(
        java_program,
        [
            AbstractVariable(AbstractType.ANY_INT),
            AbstractVariable(AbstractType.ANY_INT),
        ],
    )
    java_interpreter.run(1000)
