import os

def _fix_title(dpath, fname, alines=None):
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

def fix_doc_title():
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
					title = _fix_title(subdir, subfname)
					lines.append('- [%s](%s)\n' % (title, os.path.join(subdir, subfname)[len(dpath)+1:-3]))
			lines.sort()

			_fix_title(dpath, fname, lines)



arr = ['01.历史和标准',
'02.基本概念',
'03.系统编程概念',
'04.文件I/O：通用的I/O模型',
'05.深入探究文件I/O',
'06.进程',
'07.内存分配',
'08.用户和组',
'09.进程凭证',
'10.时间',
'11.系统限制和选项',
'12.系统和进程信息',
'13.文件I/O缓冲',
'14.系统编程概念',
'15.文件属性',
'16.扩展属性',
'17.访问控制列表',
'18.目录与链接',
'19.监控文件事件',
'20.信号：基本概念',
'21.信号：信号处理器函数',
'22.信号：高级特性',
'23.定时器与休眠',
'24.进程的创建',
'25.进程的终止',
'26.监控子进程',
'27.程序的执行',
'28.详述进程创建和程序执行',
'29.线程：介绍',
'30.线程：线程同步',
'31.线程：线程安全和每线程存储',
'32.线程：线程取消',
'33.线程：更多细节',
'34.进程组、会话和作业控制',
'35.进程优先级和调度',
'36.进程资源',
'37.DAEMON',
'38.编写安全的特权程序',
'39.能力',
'40.登录记账',
'41.共享库基础',
'42.共享库高级特性',
'43.进程间通信简介',
'44.管道和FIFO',
'45.System V IPC介绍',
'46.System V消息队列',
'47.System V信号量',
'48.System V共享内存',
'49.内存映射',
'50.虚拟内存操作',
'51.POSIX IPC介绍',
'52.POSIX消息队列',
'53.POSIX信号量',
'54.POSIX共享内存',
'55.文件加锁',
'56.SOCKET：介绍',
'57.SOCKET：UNIX DOMAIN',
'58.SOCKET：TCP/IP网络基础',
'59.SOCKET：Internet DOMAIN',
'60.SOCKET：服务器设计',
'61.SOCKET：高级主题',
'62.终端',
'63.其他备选的I/O模型',
'64.伪终端']


def test():
	for fname in arr:
		with open('_docs/tlpi/%s.md' % (fname.replace('/', '')), 'w') as fp:
			fp.write(fname)


def main():
	fix_doc_title()

if __name__ == '__main__':
	main()
	# test()