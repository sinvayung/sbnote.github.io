import os

def fix_title(dpath, fname, alines=None):
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
		header_lines = [
					'---\n',
					'title: ' + title + '\n',
					'description: ' + title + '\n',
					'---\n',
					'\n'
				]
		if alines is not None:
			header_lines.append('# ' + title + '\n')
			header_lines.append('\n')
			lines = alines
		lines = header_lines + lines
	with open(fpath, 'w') as fp:
		fp.writelines(lines)
	return title




def main():
	dpath = '_docs'
	for fname in os.listdir(dpath):
		if fname.endswith('.md'):
			# 子目录
			subdir = os.path.join(dpath, os.path.splitext(fname)[0])
			if not os.path.exists(subdir):
				os.mkdir(subdir)

			lines = []
			for subfname in os.listdir(subdir):
				if subfname.endswith('.md'):
					print('subfname: ', subfname, 'xxx', subdir)
					title = fix_title(subdir, subfname)
					lines.append('- [%s](%s)\n' % (title, os.path.join(subdir, subfname)[len(dpath)+1:-3]))

			fix_title(dpath, fname, lines)






if __name__ == '__main__':
	main()