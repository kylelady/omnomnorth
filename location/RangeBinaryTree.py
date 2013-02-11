
# Holds a range of minutes that represent time from the beginning
# of the week.
class MinuteRange:
	left, right = None, None
	start = 0
	end   = 0
	
	def __init__(self, start, end):
		# initializes the data members
		self.left  = None
		self.right = None
		self.start = start
		self.end   = end

class RangeBinaryTree:
	root = None

	def __init__ (self):
		self.root = None

	"""
	Insert a range into the tree.
	ex: RangeBinaryTree.insert(50, 100)
	"""
	def insert (self, start, end, root=None, internal=False):
		# if we didn't get passed a "root" node, use our stored one
		if root == None:
			if self.root == None:
				self.root = MinuteRange(start, end)
				return
			elif internal == False:
				root = self.root
			else:
				return MinuteRange(start, end)
		
		# enters into the tree
		if end <= root.start:
			# if the data is less than the stored one
			# goes into the left-sub-tree
			root.left = self.insert(start, end, root.left, True)
		else:
			root.right = self.insert(start, end, root.right, True)
		return root
	
	"""
	Check if a particular time is in any range in the tree.
	"""
	def in_range (self, minute, root=None, internal=False):
		# looks for a value into the tree
		if root == None:
			if self.root == None:
				return False
			elif internal == False:
				return self.in_range(minute, self.root, True)
			else:
				return False
		else:
			# if it has found it...
			if minute >= root.start and minute <= root.end:
				return True
			else:
				if minute < root.start:
					# left side
					return self.in_range(minute, root.left, True)
				else:
					# right side
					return self.in_range(minute, root.right, True)
		
	def printTree(self, root=None):
		# prints the tree path
		if root == None:
			if self.root == None:
				print 'No root. Tree empty.'
				return
			root = self.root

		if root.left != None:
			self.printTree(root.left)
		print 'start: {0}, end: {1}'.format(root.start, root.end)
		if root.right != None:
			self.printTree(root.right)

			
	def getString (self, root=None):
		out = ''
		if root == None:
			if self.root == None:
				return 'No root. Tree empty.'
			root = self.root

		if root.left != None:
			out += self.getString(root.left)
		out += 'start: {0}, end: {1}\n'.format(root.start, root.end)
		if root.right != None:
			out += self.getString(root.right)

		return out			

	def __str__ (self, root=None):
		return self.getString()



if __name__ == '__main__':
	tree = RangeBinaryTree()
	tree.insert(100,150)
	print tree.in_range(125)
	print tree.in_range(160)
	tree.insert(80,85)
	tree.insert(200,250)
	tree.insert(260,300)
	tree.insert(325,335)
	tree.insert(252,259)
	tree.insert(86,87)
	print tree.in_range(86)
	print tree.in_range(330)
	print tree.in_range(255)
	print tree.in_range(251)

	tree.printTree()