import os

def main():
	dpath = '_docs'
	for fname in os.listdir(dpath):
		if fname.endswith('.md'):
			fpath = os.path.join(dpath, fname)
			with open(fpath, 'r+') as fp:
				lines = fp.readlines()
				if lines[0].startswith('---') \
					and lines[1].startswith('title') \
					and lines[2].startswith('') \
					and lines[3].startswith('---'):
					lines[1] = 'title: ' + fname
					lines[2] = 'description: ' + fname
				else:
					lines = [
						'---',
						'title: ' + fname,
						'description: ' + fname,
						'---'
					] + lines
				


			subdir = os.path.join(dpath, os.path.splitext(fname)[0])
			print(subdir)
			if not os.path.exists(subdir):
				os.mkdir(subdir)


if __name__ == '__main__':
	main()