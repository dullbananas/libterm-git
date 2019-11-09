try:
	import click
except ImportError:
	print('Error: click is not installed. Use "python -m pip install click" to install it.')
import sys
import os
import itertools
import re
from dulwich import porcelain as gitp
from dulwich.repo import Repo

__version__ = '0.0'


ANSI = {
	'red': '\033[31m',
	'green': '\033[32m',
	'default': '\033[39m',
}

def active_branch(repo):
	(_, ref), _ = repo.refs.follow(b'HEAD')
	match = re.search(r'/([^/]+)$', ref.decode('utf-8'))
	return match[1]


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version of libterm-git and exit')
@click.option('--change-dir', '-C', default='', help='Change to directory before doing anything')
@click.pass_context
def cli(ctx, version, change_dir):
	if version:
		click.echo(f'libterm-git version {__version__} by Dull Bananas (https://dull.pythonanywhere.com)')
		sys.exit()
	
	if change_dir != '':
		os.chdir(change_dir)
	
	ctx.ensure_object(dict)
	ctx.obj['repo'] = '.'
	ctx.obj['repo_obj'] = Repo('.')


@cli.command()
@click.argument('paths', nargs=-1)
@click.pass_context
def add(ctx, paths):
	if '.' in paths:
		click.echo('Warning: adding "." does not work yet')
	result = gitp.add(ctx.obj['repo'], list(paths))
	click.echo(result)


@cli.command()
@click.argument('source')
@click.pass_context
def clone(ctx, source):
	gitp.clone(
		source=source,
	)


@cli.command()
@click.option('--message', '-m', multiple=True)
@click.pass_context
def commit(ctx, message):
	gitp.commit(ctx.obj['repo'], '\n\n'.join(message))


@cli.command()
#@click.argument('remote')
#@click.argument('branch')
@click.pass_context
def push(ctx):
	gitp.push(ctx.obj['repo'], 'refs/remotes/origin/master', 'master')


def st_section(title, help, items, color):
	click.echo(title+':')
	for h in help:
		click.echo(f'  ({h})')
	click.echo(color)
	for item in items:
		click.echo(f'\t{item}')
	click.echo(f'{ANSI["default"]}\n')

@cli.command()
@click.pass_context
def status(ctx):
	# Get status
	st = gitp.status(ctx.obj['repo'])
	added_new = (name.decode('utf-8') for name in st.staged['add'])
	added_modified = (name.decode('utf-8') for name in st.staged['modify'])
	added_deleted = (name.decode('utf-8') for name in st.staged['delete'])
	unstaged = (name.decode('utf-8') for name in st.unstaged)
	untracked = st.untracked
	#click.echo(repr(st))
	
	if True: # <-- will be for --long
		click.echo('On branch '+active_branch(ctx.obj['repo_obj']))
		st_section(
			'Changes to be committed',
			('use "git reset HEAD <file>..." to unstage',),
			itertools.chain(
				('deleted:    '+i for i in added_deleted),
				('modified:   '+i for i in added_modified),
				('new file:   '+i for i in added_new),
			),
			ANSI['green'],
		)
		st_section(
			'Changes not staged for commit',
			('use "git add <file>..." to update what will be committed',
			'use "git checkout -- <file>..." to discard changes in working directory',),
			unstaged,
			ANSI['red'],
		)
		st_section(
			'Untracked files',
			('use "git add <file>..." to include in what will be committed',),
			untracked,
			ANSI['red'],
		)


if __name__ == '__main__':
	cli()
