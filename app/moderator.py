#moderator bot for hackjobs

from badwords import bad_words

class modBot:
	def __init__(self,title,url,description):
		self.TEXT=title.lower()
		self.word_list=bad_words
		self.q_list=['what','when','why','where','how']
		self.DESCRIPTION=description.lower()
		self.URL=url.lower()

	def dirty_word_check(self):
		for i in self.word_list:
			print(i)
			res=self.TEXT.find(i)
			print(res)
			if res!=-1:
				#print (i)
				return True
		
		return False

	def description_check(self):
		for i in self.q_list:
			res=self.DESCRIPTION.find(i)
			if res!=-1:
				#print (i)
				return True
		
		return False

	def question_check(self):
		for i in self.q_list:
			res=self.TEXT.find(i)
			if res!=-1:
				#print (i)

				return True
		return False

	def url_check(self):
		for i in self.word_list:
			res=self.URL.find(i)
			if res!=-1:
				#print (i)
				return True
		return False


	def check(self):
		# print(self.dirty_word_check())
		# print(self.description_check())
		# print(self.question_check())
		# print(self.url_check())
		if self.dirty_word_check() or self.description_check() or self.question_check() or self.url_check():
			
			return False
		else:
			return True





