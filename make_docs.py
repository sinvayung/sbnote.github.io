import os

def main():
	for fname in os.listdir('_docs'):
		if fname.endswith('.md'):
			print(fname)
			subdir = os.path.join('_docs', os.path.splitext(fname)[0])
			print(subdir)
			if not os.path.exists(subdir):
				os.mkdir(subdir)


if __name__ == '__main__':
	main()