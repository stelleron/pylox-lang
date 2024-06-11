from abc import ABC, abstractmethod

class Stmt(ABC):
	@abstractmethod
	def accept(self, visitor):
		pass

class StmtVisitor(ABC):
	@abstractmethod
	def visitExpression(self, obj):
		pass

	@abstractmethod
	def visitPrint(self, obj):
		pass

	@abstractmethod
	def visitVar(self, obj):
		pass

class Expression(Stmt):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitExpression(self)


class Print(Stmt):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitPrint(self)


class Var(Stmt):
	def __init__(self, name, initializer):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor):
		return visitor.visitVar(self)


