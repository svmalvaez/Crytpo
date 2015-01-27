from .Tools import clean_data, list_xor, mod

class ECB:
	"""Electronic code book"""
	def __init__(self, cipher_instance, *args, **kwargs):
		self.cipher = cipher_instance

	def encrypt(self, p):
		return_string = False
		if type(p) is str or type(p) is unicode:
			return_string = True
		
		p = clean_data(data=p)
		encrypted = self.cipher.encrypt(plain_text=p)

		if return_string:
			return ''.join(encrypted)
		return encrypted

	def decrypt(self, c):
		return self.cipher.decrypt(cipher_text=c)

class CBC:
	"""Cipher block chaining"""
	def __init__(self, cipher_instance, init_vector, *args, **kwargs):
		self.prev = init_vector
		self.cipher = cipher_instance
		
	def encrypt(self, p):
		p = clean_data(data=p)
		xored = list_xor(self.prev, p)
		encrypted = self.cipher.encrypt(plain_text=xored)
		self.prev = list(mod(encrypted, 256))

		return encrypted

	def decrypt(self, c):
		c = clean_data(c)
		encrypted = self.cipher.decrypt(cipher_text=c)
		xored = list_xor(encrypted, self.prev)
		self.prev = c

		return xored


class CFB:
	"""Cipher feedback"""
	def __init__(self, cipher_instance, init_vector, *args, **kwargs):
		self.prev = init_vector
		self.cipher = cipher_instance
		
	def encrypt(self, p):
		p = clean_data(data=p)
		encrypted = self.cipher.encrypt(plain_text=self.prev)
		xored = list_xor(encrypted, p)
		self.prev = list(mod(xored, 256))

		return xored

	def decrypt(self, c):
		c = clean_data(c)
		encrypted = self.cipher.encrypt(plain_text=self.prev)
		xored = list_xor(encrypted, c)
		self.prev = c
		return xored

class OFB:
	"""Output feedback"""
	def __init__(self, cipher_instance, init_vector, *args, **kwargs):
		self.prev = init_vector
		self.cipher = cipher_instance
		
	def encrypt(self, p):
		p = clean_data(data=p)
		encrypted = self.cipher.encrypt(plain_text=self.prev)
		self.prev = list(mod(encrypted, 256)) #Output FEEDBACK
		xored = list_xor(encrypted, p) #Sale para C1

		return xored

	def decrypt(self, c):
		c = clean_data(c)
		encrypted = self.cipher.encrypt(plain_text=self.prev)
		xored = list_xor(encrypted, c)

		self.prev = list(mod(encrypted, 256))
		return xored

class CTR:
	"""Counter Mode"""
	def __rgb_plus_one(self,color):
		i = self.index
		color[i] += 1
		if color[i] > 255:
			color[i] = 0
			self.index -= 1

		if self.index < 0:
			self.index = 2

		return color

	def __init__(self, cipher_instance, init_vector, *args, **kwargs):
		self.prev = init_vector
		print init_vector
		self.cipher = cipher_instance
		self.index = 2
		
	def encrypt(self, p):
		p = clean_data(data=p)
		encrypted = self.cipher.encrypt(plain_text=self.prev)
		xored = list_xor(encrypted, p)

		self.prev = self.__rgb_plus_one(self.prev)
		return xored

	def decrypt(self, c):
		c = clean_data(data=c)
		encrypted = self.cipher.encrypt(plain_text=self.prev)
		xored = list_xor(encrypted, c)
		self.prev = self.__rgb_plus_one(self.prev)
		return xored
