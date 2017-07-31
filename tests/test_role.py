import unittest
from __init__ import testdb
from wenuapi.models.common import Base
from wenuapi.models.role import Role


class TestRole(unittest.TestCase):
	def setUp(self):
		engine, self.session = testdb()
		Base.metadata.create_all(engine)

		self.rolename = 'admin'

	def test_role_insert_returns_truthy(self):
		self.assertTrue(Role.set_Role(self.rolename, self.session))
		
	def test_role_insert_returns_falsey(self):
		self.assertFalse(Role.set_Role(42242, self.session))
		
	def test_role_correct_returns_role_instance(self):
		self.assertIsInstance(Role.set_Role(self.rolename, self.session), Role)

	
if __name__ == '__main__':
    unittest.main()
