import os

def main():
	dpath = '_docs'
	for fname in os.listdir(dpath):
		if fname.endswith('.md'):
			fpath = os.path.join(dpath, fname)
			print(fpath)
			with open(fpath, 'r+') as fp:
				lines = fp.readlines()
				if lines[0].startswith('---') \
					and lines[1].startswith('title') \
					and lines[2].startswith('description') \
					and lines[3].startswith('---'):
					lines = lines[4:]
				for idx in range(len(lines)):
					if lines[idx].strip() != '':
						title = lines[idx].strip('# \n')
						print('title: ' + title)
						break
				lines = [
					'---',
					'title: ' + title + '\n',
					'description: ' + title + '\n',
					'---'
				] + lines
				#fp.writelines(lines)


			subdir = os.path.join(dpath, os.path.splitext(fname)[0])
			# print(subdir)
			if not os.path.exists(subdir):
				os.mkdir(subdir)




if __name__ == '__main__':
	main()