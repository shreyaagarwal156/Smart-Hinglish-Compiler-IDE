from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass

# --- Data Types ---
@dataclass
class Number(ASTNode):
    value: float

@dataclass
class StringLiteral(ASTNode):
    value: str

@dataclass
class Identifier(ASTNode):
    name: str

# --- Operations ---
@dataclass
class BinOp(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode

# --- Statements ---
@dataclass
class Assign(ASTNode):
    target: Identifier
    value: ASTNode

@dataclass
class Print(ASTNode):
    expression: ASTNode

@dataclass
class IfElse(ASTNode):
    condition: ASTNode
    true_block: List[ASTNode]
    false_block: Optional[List[ASTNode]] = None

@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

# --- Advanced Constructs ---
@dataclass
class ImportModule(ASTNode):
    module_name: str

@dataclass
class FunctionDef(ASTNode):
    name: str
    params: List[Identifier]
    body: List[ASTNode]

@dataclass
class ReturnStmt(ASTNode):
    value: ASTNode

@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]

@dataclass
class Poocho(ASTNode):
    # Represents taking user input: poocho()
    pass

@dataclass
class ArrayLiteral(ASTNode):
    elements: list

@dataclass
class ArrayIndex(ASTNode):
    name: str
    index: ASTNode

@dataclass
class ArrayAssign(ASTNode):
    name: str
    index: ASTNode
    value: ASTNode