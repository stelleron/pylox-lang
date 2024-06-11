from abc import ABC, abstractmethod

class Expr(ABC):
	@abstractmethod
	def accept(self, visitor):
		pass

class ExprVisitor(ABC):
	@abstractmethod
	def visitAssign(self, obj):
		pass

	@abstractmethod
	def visitBinary(self, obj):
		pass

	@abstractmethod
	def visitGrouping(self, obj):
		pass

	@abstractmethod
	def visitLiteral(self, obj):
		pass

	@abstractmethod
	def visitUnary(self, obj):
		pass

	@abstractmethod
	def visitVariable(self, obj):
		pass

class Assign(Expr):
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def accept(self, visitor):
		return visitor.visitAssign(self)


class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visitBinary(self)


class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitGrouping(self)


class Literal(Expr):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visitLiteral(self)


class Unary(Expr):
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visitUnary(self)


class Variable(Expr):
	def __init__(self, name):
		self.name = name

	def accept(self, visitor):
		return visitor.visitVariable(self)


