import os

def fix_title(dpath, fname):
	fpath = os.path.join(dpath, fname)
	print(fpath)
	with open(fpath, 'r') as fp:
		lines = fp.readlines()
		if lines[0].startswith('---') \
				and lines[1].startswith('title') \
				and lines[2].startswith('description') \
				and lines[3].startswith('---'):
			if lines[4].strip() == '':
				lines = lines[5:]
			else:
				lines = lines[4:]

		for idx in range(len(lines)):
			if lines[idx].strip() != '':
				title = lines[idx].strip('# \n')
				print('title: ' + title)
				break
		lines = [
					'---\n',
					'title: ' + title + '\n',
					'description: ' + title + '\n',
					'---\n',
					'\n'
				] + lines
	with open(fpath, 'w') as fp:
		fp.writelines(lines)




def main():
	dpath = '_docs'
	for fname in os.listdir(dpath):
		if fname.endswith('.md'):
			fix_title(dpath, fname)
			subdir = os.path.join(dpath, os.path.splitext(fname)[0])
			if not os.path.exists(subdir):
				os.mkdir(subdir)
			for subfname in os.listdir(subdir):
				if subfname.endswith('.md'):
					print('subfname: ', subfname, 'xxx', subdir)
					fix_title(subdir, subfname)






if __name__ == '__main__':
	main()