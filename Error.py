from enum import Enum


class Error(Enum):
    # Main and function blocks errors:
    INV_MAIN = "Missing 'main' keyword."
    LBRACE = "Missing '{'."
    RBRACE = "Missing '}'."

    # If errors:
    OP_ERR = "Invalid conditional operator in if statement."
    COND_IF = "Missing condition in if statement."
    THEN_IF = "Missing 'then' after if condition."
    STMT_IF = "Missing statement after if condition."
    END_IF = "Missing 'endif' after if statement."
    COND_ELSEIF = "Missing condition in elseif statement."
    THEN_ELSEIF = "Missing 'then' after elseif condition."
    STMT_ELSEIF = "Missing statement after elseif condition."
    ELSE = "Missing 'else' after last elseif statement."
    END_ELSE = "Missing 'endif' after else statement."

    # While errors:
    COND_WHILE = "Missing condition in while statement."
    END_WHILE = "Missing 'endwhile' after while statement."
    THEN_WHILE = "Missing 'then' keyword in while statement."

    # Do errors:
    COND_DO = "Missing condition in do-while statement."
    WHILE_DO = "Missing 'whiledo' in do-while statement."

    # For errors:
    SET_MISS = "Missing 'set' keyword in for statement."
    FOR_VAR = "Variable specified in for statement has already been defined."
    IN_MISS = "Missing 'in' keyword in for statement."
    RANGE_MISS = "Missing 'range' keyword in for statement."
    LBRACKET_MISS = "Missing '(' keyword in for range statement."
    COMMA_MISS = "Missing ',' keyword in for range statement."
    RBRACKET_MISS = "Missing ')' keyword in for range statement."
    UNSET_VAR_FOR = "Variable specified in for statement doesn't exists."
    THEN_FOR = "Missing 'then' keyword in for statement."
    END_FOR = "Missing 'endfor' keyword in for statement."

    # Print errors:
    INV_PRINT = "Invalid syntax after print statement. It must be an expression."

    # Rear errors:
    INV_READ = "Invalid syntax after read statement. It must be a variable name."

    # Assigment errors:
    UNSET_VAR = "Specified variable doesn't exists."
    INV_VAR = "You must specify a valid variable name."
    EQ_MISS = "Missing '=' after variable name during assigment."

